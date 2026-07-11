[CmdletBinding()]
param(
    [Parameter()]
    [string]$PackageRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:Failures = New-Object System.Collections.Generic.List[string]
$script:Passes = New-Object System.Collections.Generic.List[string]

function Add-Pass {
    param([Parameter(Mandatory = $true)][string]$Message)
    $script:Passes.Add($Message)
    Write-Host "PASS: $Message"
}

function Add-Failure {
    param([Parameter(Mandatory = $true)][string]$Message)
    $script:Failures.Add($Message)
    Write-Host "FAIL: $Message"
}

function ConvertTo-CanonicalNode {
    param([Parameter(ValueFromPipeline = $true)][AllowNull()]$Value)

    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [string] -or $Value -is [char] -or $Value.GetType().IsPrimitive -or $Value -is [decimal]) {
        return $Value
    }

    if ($Value -is [System.Collections.IDictionary]) {
        $map = [ordered]@{}
        foreach ($key in @($Value.Keys | Sort-Object)) {
            $map[$key] = ConvertTo-CanonicalNode -Value $Value[$key]
        }
        return [pscustomobject]$map
    }

    if ($Value -is [System.Collections.IEnumerable]) {
        $items = @()
        foreach ($item in $Value) {
            $items += ,(ConvertTo-CanonicalNode -Value $item)
        }
        return ,$items
    }

    $propertyNames = @(
        $Value.PSObject.Properties |
            Where-Object { $_.MemberType -in @("NoteProperty", "Property") } |
            Select-Object -ExpandProperty Name |
            Sort-Object
    )

    if ($propertyNames.Count -gt 0) {
        $objectMap = [ordered]@{}
        foreach ($propertyName in $propertyNames) {
            $objectMap[$propertyName] = ConvertTo-CanonicalNode -Value $Value.$propertyName
        }
        return [pscustomobject]$objectMap
    }

    return $Value.ToString()
}

function ConvertTo-CanonicalJson {
    param([Parameter(Mandatory = $true)]$Value)
    $canonical = ConvertTo-CanonicalNode -Value $Value
    return ($canonical | ConvertTo-Json -Depth 100 -Compress)
}

try {
    $root = (Resolve-Path -LiteralPath $PackageRoot).Path
    Add-Pass "Package root resolved: $root"
}
catch {
    Write-Host "FAIL: Package root could not be resolved: $($_.Exception.Message)"
    exit 1
}

$jsonPath = Join-Path $root "docs/current_sprint.json"
$yamlPath = Join-Path $root "docs/current_sprint.yaml"
$markdownPath = Join-Path $root "docs/current_sprint.md"

$requiredManifestPaths = @($jsonPath, $yamlPath, $markdownPath)
foreach ($manifestPath in $requiredManifestPaths) {
    if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
        Add-Pass "Found $(Split-Path -Leaf $manifestPath)."
    }
    else {
        Add-Failure "Missing manifest: $manifestPath"
    }
}

if ($script:Failures.Count -gt 0) {
    Write-Host "Validation stopped because a canonical manifest is missing."
    exit 1
}

try {
    $jsonManifest = Get-Content -LiteralPath $jsonPath -Raw | ConvertFrom-Json
    Add-Pass "docs/current_sprint.json parsed as JSON."
}
catch {
    Add-Failure "docs/current_sprint.json is invalid: $($_.Exception.Message)"
}

try {
    # JSON syntax is a strict subset of YAML 1.2, avoiding a bootstrap YAML dependency.
    $yamlManifest = Get-Content -LiteralPath $yamlPath -Raw | ConvertFrom-Json
    Add-Pass "docs/current_sprint.yaml parsed as JSON-compatible YAML 1.2."
}
catch {
    Add-Failure "docs/current_sprint.yaml is not valid JSON-compatible YAML: $($_.Exception.Message)"
}

try {
    $markdownText = Get-Content -LiteralPath $markdownPath -Raw
    $pattern = '(?ms)<!-- CANONICAL-MANIFEST-START -->\s*```json\s*(?<manifest>\{.*\})\s*```\s*<!-- CANONICAL-MANIFEST-END -->'
    $match = [regex]::Match($markdownText, $pattern)
    if (-not $match.Success) {
        throw "Canonical JSON block markers were not found."
    }
    $markdownManifest = $match.Groups["manifest"].Value | ConvertFrom-Json
    Add-Pass "docs/current_sprint.md canonical JSON block parsed."
}
catch {
    Add-Failure "docs/current_sprint.md canonical block is invalid: $($_.Exception.Message)"
}

if ($script:Failures.Count -eq 0) {
    $jsonCanonical = ConvertTo-CanonicalJson -Value $jsonManifest
    $yamlCanonical = ConvertTo-CanonicalJson -Value $yamlManifest
    $markdownCanonical = ConvertTo-CanonicalJson -Value $markdownManifest

    if ($jsonCanonical -eq $yamlCanonical -and $jsonCanonical -eq $markdownCanonical) {
        Add-Pass "Markdown, YAML, and JSON manifests agree structurally."
    }
    else {
        Add-Failure "Markdown, YAML, and JSON manifests do not agree structurally."
    }

    if ($jsonManifest.sprint_count -eq 1 -and $jsonManifest.sprint.mode -eq "single-sprint") {
        Add-Pass "Manifest declares exactly one active sprint container."
    }
    else {
        Add-Failure "Manifest must declare sprint_count 1 and mode single-sprint."
    }

    if (@("bounded-maintenance", "bounded-feature") -contains $jsonManifest.sprint.type) {
        Add-Pass "Sprint type is bounded."
    }
    else {
        Add-Failure "Sprint type must be bounded-maintenance or bounded-feature."
    }

    $expectedInterpreter = ".\.venv\Scripts\python.exe"
    if ($jsonManifest.sprint.platform.official_interpreter -ceq $expectedInterpreter) {
        Add-Pass "Official interpreter path is exact."
    }
    else {
        Add-Failure "Official interpreter must be $expectedInterpreter"
    }

    $principles = @($jsonManifest.project.principles)
    if ($principles -contains "provider-neutral" -and $principles -contains "deterministic-core") {
        Add-Pass "Provider-neutral and deterministic-core principles are present."
    }
    else {
        Add-Failure "Required provider-neutral and deterministic-core principles are missing."
    }

    $phaseIds = @($jsonManifest.sprint.execution_phases | ForEach-Object { $_.id })
    if (($phaseIds -join ",") -ceq "setup,implementation,verification,closeout") {
        Add-Pass "Execution phases are setup, implementation, verification, and closeout in order."
    }
    else {
        Add-Failure "Execution phases are missing, duplicated, or out of order."
    }

    $governanceText = @($jsonManifest.sprint.governance) -join "`n"
    if ($governanceText -match "Do not substitute bundled, system, Windows Store, or alternate Python") {
        Add-Pass "Alternate-Python substitution is prohibited."
    }
    else {
        Add-Failure "Governance must prohibit alternate-Python substitution."
    }

    if ($null -eq $jsonManifest.sprint.closeout.next_sprint) {
        Add-Pass "No next sprint is defined."
    }
    else {
        Add-Failure "next_sprint must be null for this one-sprint package."
    }

    if ($jsonManifest.sprint.id -eq "ENV-HARDENING-001") {
        foreach ($deliverable in @($jsonManifest.sprint.deliverables)) {
            $deliverablePath = Join-Path $root $deliverable.path
            if (Test-Path -LiteralPath $deliverablePath -PathType Leaf) {
                Add-Pass "Found deliverable $($deliverable.path)."
            }
            else {
                Add-Failure "Missing deliverable $($deliverable.path)."
            }
        }
    }
    else {
        Add-Pass "Hardening deliverable checks are not applicable to this product sprint."
    }
}

$powerShellScripts = @(
    (Join-Path $root "tools\preflight.ps1"),
    (Join-Path $root "tools\validate_hardening_package.ps1")
)

foreach ($scriptPath in $powerShellScripts) {
    if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
        Add-Failure "Cannot parse missing script: $scriptPath"
        continue
    }

    $tokens = $null
    $parseErrors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $scriptPath,
        [ref]$tokens,
        [ref]$parseErrors
    )

    if (@($parseErrors).Count -eq 0) {
        Add-Pass "PowerShell syntax is valid for $(Split-Path -Leaf $scriptPath)."
    }
    else {
        foreach ($parseError in @($parseErrors)) {
            Add-Failure "$(Split-Path -Leaf $scriptPath): line $($parseError.Extent.StartLineNumber): $($parseError.Message)"
        }
    }
}

$preflightPath = Join-Path $root "tools\preflight.ps1"
if (Test-Path -LiteralPath $preflightPath -PathType Leaf) {
    $preflightText = Get-Content -LiteralPath $preflightPath -Raw
    if ($preflightText -match [regex]::Escape(".venv\Scripts\python.exe")) {
        Add-Pass "Preflight contains the canonical interpreter path."
    }
    else {
        Add-Failure "Preflight does not contain the canonical interpreter path."
    }

    if ($preflightText -match '(?im)&\s+(python|python3|py)(\.exe)?\b') {
        Add-Failure "Preflight appears to invoke a generic or alternate Python command."
    }
    else {
        Add-Pass "Preflight contains no generic Python command invocation."
    }
}

Write-Host ""
Write-Host ("Validation summary: {0} passed, {1} failed." -f $script:Passes.Count, $script:Failures.Count)

if ($script:Failures.Count -gt 0) {
    exit 1
}

exit 0


