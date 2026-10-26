#requires -Version 7.0
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$pwsh = Join-Path $PSHOME 'pwsh.exe'
$legacyShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$passed = 0

function Assert-Workflow {
    param([bool]$Condition, [string]$Description)
    if (-not $Condition) { throw "Workflow regression failed: $Description" }
    $script:passed++
    Write-Output "PASS: $Description"
}

Assert-Workflow ($PSVersionTable.PSEdition -eq 'Core' -and $PSVersionTable.PSVersion.Major -ge 7) 'PowerShell 7 Core executes verification'
foreach ($scriptFile in Get-ChildItem -LiteralPath (Join-Path $root 'tools') -Filter '*.ps1' -File) {
    $tokens = $null
    $parseErrors = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($scriptFile.FullName, [ref]$tokens, [ref]$parseErrors)
    Assert-Workflow ($parseErrors.Count -eq 0) ("syntax: " + $scriptFile.Name)
    if ($scriptFile.Name -ne 'preflight.ps1') {
        Assert-Workflow ($ast.ScriptRequirements.RequiredPSVersion.Major -ge 7) ("version guard: " + $scriptFile.Name)
    }
}

foreach ($entryPoint in @('validate_project_records.ps1', 'test_project_records.ps1', 'run_offline_behavioral_verification.ps1')) {
    $output = @(& $legacyShell -NoProfile -NonInteractive -File (Join-Path $root "tools\$entryPoint") -ProjectRoot $root 2>&1)
    $exitCode = $LASTEXITCODE
    Assert-Workflow ($exitCode -ne 0 -and ($output -join ' ') -match 'ScriptRequiresUnmatchedPSVersion') ("Windows PowerShell 5.1 rejects " + $entryPoint)
}

$output = @(& $legacyShell -NoProfile -NonInteractive -File (Join-Path $root 'tools\preflight.ps1') -RepoRoot $root -ExpectedRepoRoot $root -Json 2>&1)
$exitCode = $LASTEXITCODE
$preflight = ($output -join [Environment]::NewLine) | ConvertFrom-Json
$versionCheck = @($preflight.checks | Where-Object name -eq 'powershell-version')
Assert-Workflow ($exitCode -eq 1 -and $versionCheck.Count -eq 1 -and $versionCheck[0].status -eq 'FAIL') 'Windows PowerShell 5.1 fails mandatory preflight'

foreach ($layout in @('Pretty', 'Compact', 'LegacyWhitespace')) {
    $output = @(& $pwsh -NoProfile -NonInteractive -File (Join-Path $root 'tools\test_project_records.ps1') -ProjectRoot $root -JsonLayout $layout 2>&1)
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) { $output | Select-Object -First 35 | Write-Output }
    Assert-Workflow ($exitCode -eq 0 -and ($output -join ' ') -match 'Project-record fixture summary: 16 passed\.') ("all 16 lifecycle cases: " + $layout)
}
Write-Output "PowerShell workflow regression summary: $passed passed."
