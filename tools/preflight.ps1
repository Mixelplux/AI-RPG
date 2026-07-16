[CmdletBinding()]
param(
    [Parameter()]
    [string]$RepoRoot,

    [Parameter()]
    [string]$ExpectedRepoRoot = "D:\AI RPG",

    [Parameter()]
    [string[]]$RequiredPythonModule = @(),

    [Parameter()]
    [string[]]$RequiredDocument = @(
        "AGENTS.md",
        "PROJECT.md",
        "WORKFLOW.md",
        "docs/current_capability_package.md",
        "docs/current_sprint.md",
        "docs/current_sprint.json"
    ),

    [Parameter()]
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}

$script:Checks = New-Object System.Collections.Generic.List[object]
$resolvedRepoRoot = $null
$activeRepoRoot = $null
$workspaceRootIsValid = $false

function Add-Check {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [ValidateSet("PASS", "WARN", "BLOCKED", "FAIL")]
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

function Test-ExecutionContextDenial {
    param([AllowEmptyString()][string]$Text)
    return $Text -match '(?i)access is denied|unable to create process'
}

function Normalize-Path {
    param([Parameter(Mandatory = $true)][string]$Path)

    return [System.IO.Path]::GetFullPath($Path).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
}

function Test-NormalizedPathEqual {
    param(
        [Parameter(Mandatory = $true)][string]$Left,
        [Parameter(Mandatory = $true)][string]$Right
    )

    return [string]::Equals(
        (Normalize-Path -Path $Left),
        (Normalize-Path -Path $Right),
        [System.StringComparison]::OrdinalIgnoreCase
    )
}

function Get-WorkspaceRemediation {
    param([Parameter(Mandatory = $true)][string]$ExpectedRoot)

    return "Workspace-context failure. Reopen $ExpectedRoot directly as the Codex workspace, or open the existing AI RPG.code-workspace, then rerun the startup gate. Do not recreate .venv, change permissions, run as Administrator, or substitute another Python interpreter."
}

function Add-PythonProbeResult {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)]$Probe
    )

    if ($Probe.exit_code -eq 0) {
        Add-Check -Name $Name -Status "PASS" -Detail $Probe.output
    }
    elseif (Test-ExecutionContextDenial -Text $Probe.output) {
        Add-Check -Name $Name -Status "BLOCKED" -Detail "$(Get-WorkspaceRemediation -ExpectedRoot $ExpectedRepoRoot) Exit $($Probe.exit_code): $($Probe.output)"
    }
    else {
        Add-Check -Name $Name -Status "FAIL" -Detail "Exit $($Probe.exit_code): $($Probe.output)"
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

    $recordValidatorPath = Join-Path $resolvedRepoRoot "tools\validate_project_records.ps1"
    if (-not (Test-Path -LiteralPath $recordValidatorPath -PathType Leaf)) {
        Add-Check -Name "project-record-validation" -Status "FAIL" -Detail "Missing project-record validator: $recordValidatorPath"
    }
    else {
        try {
            $global:LASTEXITCODE = 0
            $validatorOutput = & $recordValidatorPath -ProjectRoot $resolvedRepoRoot 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                Add-Check -Name "project-record-validation" -Status "PASS" -Detail "Current project records validated."
            }
            else {
                Add-Check -Name "project-record-validation" -Status "FAIL" -Detail "Current project record validation failed: $($validatorOutput.Trim())"
            }
        }
        catch {
            Add-Check -Name "project-record-validation" -Status "FAIL" -Detail $_.Exception.Message
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

            $activeRepoRoot = $gitRoot.Trim()
            if (Test-NormalizedPathEqual -Left $activeRepoRoot -Right $ExpectedRepoRoot) {
                $workspaceRootIsValid = $true
                Add-Check -Name "workspace-root" -Status "PASS" -Detail (Normalize-Path -Path $activeRepoRoot)
            }
            else {
                Add-Check -Name "workspace-root" -Status "FAIL" -Detail "Expected Git root $(Normalize-Path -Path $ExpectedRepoRoot); got $(Normalize-Path -Path $activeRepoRoot). $(Get-WorkspaceRemediation -ExpectedRoot $ExpectedRepoRoot)"
            }

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

    if ($workspaceRootIsValid) {
        foreach ($relativeDirectory in @(".build", ".artifacts", "handoffs")) {
            $directoryPath = Join-Path $activeRepoRoot $relativeDirectory
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
    }

    if (-not $workspaceRootIsValid) {
        Add-Check -Name "official-interpreter" -Status "BLOCKED" -Detail "Official-interpreter preflight skipped because the workspace-root check failed."
    }
    else {
        $officialInterpreter = Join-Path $activeRepoRoot ".venv\Scripts\python.exe"
        if (-not (Test-Path -LiteralPath $officialInterpreter -PathType Leaf)) {
            Add-Check -Name "official-interpreter" -Status "FAIL" -Detail "Missing official interpreter: $officialInterpreter"
        }
        else {
            Add-Check -Name "official-interpreter" -Status "PASS" -Detail $officialInterpreter
            $pythonProbeSucceeded = $false

            try {
                $inlineProbe = Invoke-OfficialPython -Interpreter $officialInterpreter -Arguments @(
                    "-c",
                    "import sys; print(sys.executable); print(sys.version)"
                )
                Add-PythonProbeResult -Name "python-c-probe" -Probe $inlineProbe
                $pythonProbeSucceeded = $inlineProbe.exit_code -eq 0
            }
            catch {
                $status = if (Test-ExecutionContextDenial -Text $_.Exception.Message) { "BLOCKED" } else { "FAIL" }
                $detail = if ($status -eq "BLOCKED") { "$(Get-WorkspaceRemediation -ExpectedRoot $ExpectedRepoRoot) $($_.Exception.Message)" } else { $_.Exception.Message }
                Add-Check -Name "python-c-probe" -Status $status -Detail $detail
            }

            if ($pythonProbeSucceeded) {
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
                        Add-PythonProbeResult -Name "python-module-$moduleName" -Probe $moduleProbe
                    }
                    catch {
                        $status = if (Test-ExecutionContextDenial -Text $_.Exception.Message) { "BLOCKED" } else { "FAIL" }
                        $detail = if ($status -eq "BLOCKED") { "$(Get-WorkspaceRemediation -ExpectedRoot $ExpectedRepoRoot) $($_.Exception.Message)" } else { $_.Exception.Message }
                        Add-Check -Name "python-module-$moduleName" -Status $status -Detail $detail
                    }
                }
            }
        }
    }
}

$failureCount = @($script:Checks | Where-Object { $_.status -eq "FAIL" }).Count
$warningCount = @($script:Checks | Where-Object { $_.status -eq "WARN" }).Count
$blockedCount = @($script:Checks | Where-Object { $_.status -eq "BLOCKED" }).Count
$summary = [pscustomobject]@{
    repository = if ($null -ne $activeRepoRoot) { $activeRepoRoot } else { $resolvedRepoRoot }
    official_interpreter = if ($workspaceRootIsValid) { Join-Path $activeRepoRoot ".venv\Scripts\python.exe" } else { $null }
    passed = @($script:Checks | Where-Object { $_.status -eq "PASS" }).Count
    warnings = $warningCount
    blocked = $blockedCount
    failures = $failureCount
    checks = $script:Checks
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 8
}
else {
    $script:Checks | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host ("Preflight summary: {0} passed, {1} warning(s), {2} blocked, {3} failure(s)." -f $summary.passed, $warningCount, $blockedCount, $failureCount)
    if ($failureCount -eq 0 -and $blockedCount -eq 0) {
        Write-Host "Resolved repository root: $($summary.repository)"
        Write-Host "Official interpreter: $($summary.official_interpreter)"
    }
}

if ($failureCount -gt 0) {
    exit 1
}

if ($blockedCount -gt 0) {
    exit 2
}

exit 0


