[CmdletBinding()]
param(
    [Parameter()]
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),

    [Parameter()]
    [string[]]$RequiredPythonModule = @(),

    [Parameter()]
    [string[]]$RequiredDocument = @(
        "AGENTS.md",
        "current_sprint.md",
        "current_sprint.yaml",
        "current_sprint.json",
        "next_chat_handoff.md"
    ),

    [Parameter()]
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:Checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [ValidateSet("PASS", "WARN", "FAIL")]
        [string]$Status,

        [Parameter(Mandatory = $true)]
        [string]$Detail
    )

    $script:Checks.Add([pscustomobject]@{
        name = $Name
        status = $Status
        detail = $Detail
    })
}

function Invoke-OfficialPython {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Interpreter,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $global:LASTEXITCODE = 0
    $output = & $Interpreter @Arguments 2>&1 | Out-String
    return [pscustomobject]@{
        exit_code = $LASTEXITCODE
        output = $output.Trim()
    }
}

try {
    $resolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
    Add-Check -Name "repository-root" -Status "PASS" -Detail $resolvedRepoRoot
}
catch {
    Add-Check -Name "repository-root" -Status "FAIL" -Detail $_.Exception.Message
    $resolvedRepoRoot = $null
}

if ($env:OS -eq "Windows_NT") {
    Add-Check -Name "operating-system" -Status "PASS" -Detail "Windows"
}
else {
    Add-Check -Name "operating-system" -Status "FAIL" -Detail "Expected Windows; detected $([System.Environment]::OSVersion.Platform)."
}

if ($PSVersionTable.PSVersion.Major -ge 7) {
    Add-Check -Name "powershell-version" -Status "PASS" -Detail $PSVersionTable.PSVersion.ToString()
}
elseif ($PSVersionTable.PSVersion.Major -ge 5) {
    Add-Check -Name "powershell-version" -Status "WARN" -Detail "$($PSVersionTable.PSVersion) is supported for bootstrap checks; PowerShell 7+ is preferred."
}
else {
    Add-Check -Name "powershell-version" -Status "FAIL" -Detail "$($PSVersionTable.PSVersion) is unsupported."
}

foreach ($commandName in @("ConvertFrom-Json", "Compress-Archive")) {
    if (Get-Command $commandName -ErrorAction SilentlyContinue) {
        Add-Check -Name "command-$commandName" -Status "PASS" -Detail "$commandName is available."
    }
    else {
        Add-Check -Name "command-$commandName" -Status "FAIL" -Detail "$commandName is unavailable."
    }
}

try {
    $jsonProbe = '{"preflight":true}' | ConvertFrom-Json
    if ($jsonProbe.preflight -eq $true) {
        Add-Check -Name "json-support" -Status "PASS" -Detail "PowerShell JSON parsing succeeded."
    }
    else {
        Add-Check -Name "json-support" -Status "FAIL" -Detail "PowerShell JSON parsing returned an unexpected value."
    }
}
catch {
    Add-Check -Name "json-support" -Status "FAIL" -Detail $_.Exception.Message
}

if ($null -ne $resolvedRepoRoot) {
    foreach ($document in $RequiredDocument) {
        $documentPath = Join-Path $resolvedRepoRoot $document
        if (Test-Path -LiteralPath $documentPath -PathType Leaf) {
            Add-Check -Name "document-$document" -Status "PASS" -Detail $documentPath
        }
        else {
            Add-Check -Name "document-$document" -Status "FAIL" -Detail "Missing required document: $documentPath"
        }
    }

    $gitCommand = Get-Command git -ErrorAction SilentlyContinue
    if ($null -eq $gitCommand) {
        Add-Check -Name "git" -Status "FAIL" -Detail "git is unavailable."
    }
    else {
        $global:LASTEXITCODE = 0
        $gitRoot = git -C $resolvedRepoRoot rev-parse --show-toplevel 2>&1 | Out-String
        $gitRootExitCode = $LASTEXITCODE
        if ($gitRootExitCode -ne 0) {
            Add-Check -Name "git-repository" -Status "FAIL" -Detail $gitRoot.Trim()
        }
        else {
            Add-Check -Name "git-repository" -Status "PASS" -Detail $gitRoot.Trim()

            $global:LASTEXITCODE = 0
            $gitStatus = git -C $resolvedRepoRoot status --porcelain=v1 2>&1 | Out-String
            if ($LASTEXITCODE -ne 0) {
                Add-Check -Name "git-status" -Status "FAIL" -Detail $gitStatus.Trim()
            }
            elseif ([string]::IsNullOrWhiteSpace($gitStatus)) {
                Add-Check -Name "git-status" -Status "PASS" -Detail "Working tree is clean."
            }
            else {
                $changedCount = @($gitStatus.Trim().Split([Environment]::NewLine, [System.StringSplitOptions]::RemoveEmptyEntries)).Count
                Add-Check -Name "git-status" -Status "WARN" -Detail "Working tree has $changedCount changed path(s); preserve them during hardening."
            }
        }
    }

    foreach ($relativeDirectory in @(".build", ".artifacts", "handoffs")) {
        $directoryPath = Join-Path $resolvedRepoRoot $relativeDirectory
        $probePath = Join-Path $directoryPath (".preflight-{0}.tmp" -f [guid]::NewGuid().ToString("N"))
        try {
            [void](New-Item -ItemType Directory -Force -Path $directoryPath)
            [System.IO.File]::WriteAllText($probePath, "preflight")
            Remove-Item -LiteralPath $probePath -Force
            Add-Check -Name "writable-$relativeDirectory" -Status "PASS" -Detail $directoryPath
        }
        catch {
            if (Test-Path -LiteralPath $probePath) {
                Remove-Item -LiteralPath $probePath -Force -ErrorAction SilentlyContinue
            }
            Add-Check -Name "writable-$relativeDirectory" -Status "FAIL" -Detail $_.Exception.Message
        }
    }

    $officialInterpreter = Join-Path $resolvedRepoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $officialInterpreter -PathType Leaf)) {
        Add-Check -Name "official-interpreter" -Status "FAIL" -Detail "Missing official interpreter: $officialInterpreter"
    }
    else {
        Add-Check -Name "official-interpreter" -Status "PASS" -Detail $officialInterpreter

        try {
            $versionProbe = Invoke-OfficialPython -Interpreter $officialInterpreter -Arguments @("--version")
            if ($versionProbe.exit_code -eq 0) {
                Add-Check -Name "python-direct-launch" -Status "PASS" -Detail $versionProbe.output
            }
            else {
                Add-Check -Name "python-direct-launch" -Status "FAIL" -Detail "Exit $($versionProbe.exit_code): $($versionProbe.output)"
            }
        }
        catch {
            Add-Check -Name "python-direct-launch" -Status "FAIL" -Detail $_.Exception.Message
        }

        try {
            $inlineProbe = Invoke-OfficialPython -Interpreter $officialInterpreter -Arguments @(
                "-c",
                "import json,sys; print(json.dumps({'executable': sys.executable}, sort_keys=True))"
            )
            if ($inlineProbe.exit_code -eq 0) {
                Add-Check -Name "python-c-probe" -Status "PASS" -Detail $inlineProbe.output
            }
            else {
                Add-Check -Name "python-c-probe" -Status "FAIL" -Detail "Exit $($inlineProbe.exit_code): $($inlineProbe.output)"
            }
        }
        catch {
            Add-Check -Name "python-c-probe" -Status "FAIL" -Detail $_.Exception.Message
        }

        $scriptProbeDirectory = Join-Path $resolvedRepoRoot ".build\preflight"
        $scriptProbePath = Join-Path $scriptProbeDirectory "python_file_probe.py"
        try {
            [void](New-Item -ItemType Directory -Force -Path $scriptProbeDirectory)
            $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
            [System.IO.File]::WriteAllText(
                $scriptProbePath,
                "import json`nprint(json.dumps({'file_probe': True}, sort_keys=True))`n",
                $utf8NoBom
            )
            $fileProbe = Invoke-OfficialPython -Interpreter $officialInterpreter -Arguments @($scriptProbePath)
            if ($fileProbe.exit_code -eq 0) {
                Add-Check -Name "python-file-probe" -Status "PASS" -Detail $fileProbe.output
            }
            else {
                Add-Check -Name "python-file-probe" -Status "FAIL" -Detail "Exit $($fileProbe.exit_code): $($fileProbe.output)"
            }
        }
        catch {
            Add-Check -Name "python-file-probe" -Status "FAIL" -Detail $_.Exception.Message
        }
        finally {
            if (Test-Path -LiteralPath $scriptProbePath) {
                Remove-Item -LiteralPath $scriptProbePath -Force -ErrorAction SilentlyContinue
            }
        }

        foreach ($moduleName in $RequiredPythonModule) {
            if ($moduleName -notmatch '^[A-Za-z_][A-Za-z0-9_.]*$') {
                Add-Check -Name "python-module-$moduleName" -Status "FAIL" -Detail "Invalid Python import name."
                continue
            }

            try {
                $moduleProbe = Invoke-OfficialPython -Interpreter $officialInterpreter -Arguments @(
                    "-c",
                    "import importlib; importlib.import_module('$moduleName'); print('$moduleName')"
                )
                if ($moduleProbe.exit_code -eq 0) {
                    Add-Check -Name "python-module-$moduleName" -Status "PASS" -Detail "Import succeeded."
                }
                else {
                    Add-Check -Name "python-module-$moduleName" -Status "FAIL" -Detail "Exit $($moduleProbe.exit_code): $($moduleProbe.output)"
                }
            }
            catch {
                Add-Check -Name "python-module-$moduleName" -Status "FAIL" -Detail $_.Exception.Message
            }
        }
    }
}

$failureCount = @($script:Checks | Where-Object { $_.status -eq "FAIL" }).Count
$warningCount = @($script:Checks | Where-Object { $_.status -eq "WARN" }).Count
$summary = [pscustomobject]@{
    repository = $resolvedRepoRoot
    official_interpreter = if ($null -ne $resolvedRepoRoot) { Join-Path $resolvedRepoRoot ".venv\Scripts\python.exe" } else { $null }
    passed = @($script:Checks | Where-Object { $_.status -eq "PASS" }).Count
    warnings = $warningCount
    failures = $failureCount
    checks = $script:Checks
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 8
}
else {
    $script:Checks | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host ("Preflight summary: {0} passed, {1} warning(s), {2} failure(s)." -f $summary.passed, $warningCount, $failureCount)
}

if ($failureCount -gt 0) {
    exit 1
}

exit 0
