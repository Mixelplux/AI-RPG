[CmdletBinding()]
param(
    [Parameter()]
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

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

function Get-PropertyValue {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        Add-Failure "Missing required field: $Path"
        return $null
    }

    return $property.Value
}

function Test-RequiredString {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $value = Get-PropertyValue -Object $Object -Name $Name -Path $Path
    if ($value -isnot [string] -or [string]::IsNullOrWhiteSpace($value)) {
        Add-Failure "Required non-empty string field is invalid: $Path"
        return $null
    }

    return $value.Trim()
}

function Get-NullableIdentifier {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        Add-Failure "Missing required field: $Path"
        return $null
    }

    if ($null -eq $property.Value) {
        return $null
    }

    if ($property.Value -isnot [string] -or [string]::IsNullOrWhiteSpace($property.Value)) {
        Add-Failure "Field must be null or a non-empty string: $Path"
        return $null
    }

    return $property.Value.Trim()
}

function ConvertTo-RecordToken {
    param([AllowNull()]$Value)

    if ($null -eq $Value) {
        return $null
    }

    return (([string]$Value).Trim().ToLowerInvariant() -replace '[^a-z0-9]+', '_').Trim('_')
}

function Test-ForbiddenYamlAuthorityReference {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string[]]$RelativePaths
    )

    $patterns = @(
        'docs[/\\]current_sprint\.ya?ml',
        '(?i)(?:markdown\s*/\s*)?json\s*/\s*yaml\s+agreement',
        '(?i)json\s+and\s+yaml\s+agreement',
        '(?i)multi[- ]format\s+canonical\s+sprint\s+state'
    )

    foreach ($relativePath in $RelativePaths) {
        $path = Join-Path $Root $relativePath
        $text = Get-Content -LiteralPath $path -Raw
        foreach ($pattern in $patterns) {
            $match = [regex]::Match($text, $pattern)
            if ($match.Success) {
                Add-Failure "Forbidden YAML lifecycle authority reference in $($relativePath.Replace('\', '/')): '$($match.Value)'."
            }
        }
    }
}

try {
    $root = (Resolve-Path -LiteralPath $ProjectRoot).Path
    Add-Pass "Project root resolved: $root"
}
catch {
    Write-Host "FAIL: Project root could not be resolved: $($_.Exception.Message)"
    exit 1
}

$requiredPaths = @(
    'AGENTS.md',
    'WORKFLOW.md',
    'docs/current_sprint.json',
    'docs/current_sprint.md',
    'docs/current_capability_package.md'
)
foreach ($relativePath in $requiredPaths) {
    $recordPath = Join-Path $root $relativePath
    if (Test-Path -LiteralPath $recordPath -PathType Leaf) {
        Add-Pass "Found $relativePath."
    }
    else {
        Add-Failure "Missing required project record: $relativePath"
    }
}

if ($script:Failures.Count -gt 0) {
    Write-Host 'Validation stopped because a required project record is missing.'
    exit 1
}

Test-ForbiddenYamlAuthorityReference -Root $root -RelativePaths @(
    'AGENTS.md',
    'WORKFLOW.md',
    'docs/current_sprint.md',
    'docs/current_capability_package.md'
)

$jsonPath = Join-Path $root 'docs/current_sprint.json'
$jsonRecord = $null
try {
    $jsonText = Get-Content -LiteralPath $jsonPath -Raw
    if ($jsonText -notmatch '^\s*\{[\s\S]*\}\s*$') {
        throw 'The document must contain exactly one JSON object.'
    }
    $jsonRecord = $jsonText | ConvertFrom-Json -ErrorAction Stop
    Add-Pass 'docs/current_sprint.json parsed as one JSON object.'
}
catch {
    Add-Failure "docs/current_sprint.json is invalid JSON: $($_.Exception.Message)"
}

if ($null -ne $jsonRecord) {
    $schemaVersion = Test-RequiredString -Object $jsonRecord -Name 'schema_version' -Path 'schema_version'
    $documentType = Test-RequiredString -Object $jsonRecord -Name 'document_type' -Path 'document_type'
    $sprintCount = Get-PropertyValue -Object $jsonRecord -Name 'sprint_count' -Path 'sprint_count'
    $authority = Get-PropertyValue -Object $jsonRecord -Name 'lifecycle_authority' -Path 'lifecycle_authority'
    $activeSprint = Get-NullableIdentifier -Object $jsonRecord -Name 'active_sprint' -Path 'active_sprint'
    $activePackage = Get-NullableIdentifier -Object $jsonRecord -Name 'active_capability_package' -Path 'active_capability_package'
    $latestCompleted = Get-PropertyValue -Object $jsonRecord -Name 'latest_completed_sprint' -Path 'latest_completed_sprint'
    $nextSprint = Get-NullableIdentifier -Object $jsonRecord -Name 'next_sprint' -Path 'next_sprint'
    $sprint = Get-PropertyValue -Object $jsonRecord -Name 'sprint' -Path 'sprint'

    if ($schemaVersion -ne $null -and $schemaVersion -ne '1.2.0') {
        Add-Failure "schema_version must be '1.2.0'; found '$schemaVersion'."
    }
    if ($documentType -ne $null -and $documentType -ne 'current_sprint') {
        Add-Failure "document_type must be 'current_sprint'; found '$documentType'."
    }
    if ($sprintCount -ne 1) {
        Add-Failure "sprint_count must be 1; found '$sprintCount'."
    }

    if ($null -eq $authority) {
        Add-Failure 'Required object field is invalid: lifecycle_authority'
    }
    else {
        $machineReadable = Test-RequiredString -Object $authority -Name 'machine_readable' -Path 'lifecycle_authority.machine_readable'
        $markdownRole = Test-RequiredString -Object $authority -Name 'markdown_role' -Path 'lifecycle_authority.markdown_role'
        $yamlRequired = Get-PropertyValue -Object $authority -Name 'yaml_required' -Path 'lifecycle_authority.yaml_required'
        if ($machineReadable -ne $null -and $machineReadable -ne 'docs/current_sprint.json') {
            Add-Failure "lifecycle_authority.machine_readable must be 'docs/current_sprint.json'; found '$machineReadable'."
        }
        if ($markdownRole -ne $null -and $markdownRole -ne 'explanatory_records') {
            Add-Failure "lifecycle_authority.markdown_role must be 'explanatory_records'; found '$markdownRole'."
        }
        if ($yamlRequired -isnot [bool] -or $yamlRequired) {
            Add-Failure 'lifecycle_authority.yaml_required must be false.'
        }
    }

    $latestCompletedId = $null
    if ($null -eq $latestCompleted) {
        Add-Failure 'Required object field is invalid: latest_completed_sprint'
    }
    else {
        $latestCompletedId = Test-RequiredString -Object $latestCompleted -Name 'id' -Path 'latest_completed_sprint.id'
    }

    $jsonSprintId = $null
    $jsonSprintStatus = $null
    $jsonRiskLevel = $null
    if ($null -eq $sprint) {
        Add-Failure 'Required object field is invalid: sprint'
    }
    else {
        $jsonSprintId = Test-RequiredString -Object $sprint -Name 'id' -Path 'sprint.id'
        [void](Test-RequiredString -Object $sprint -Name 'title' -Path 'sprint.title')
        [void](Test-RequiredString -Object $sprint -Name 'type' -Path 'sprint.type')
        $jsonSprintStatus = Test-RequiredString -Object $sprint -Name 'status' -Path 'sprint.status'
        $jsonRiskLevel = Test-RequiredString -Object $sprint -Name 'risk_level' -Path 'sprint.risk_level'
        [void](Test-RequiredString -Object $sprint -Name 'goal' -Path 'sprint.goal')

        foreach ($removedField in @('candidate_state', 'merge_state')) {
            if ($null -ne $sprint.PSObject.Properties[$removedField]) {
                Add-Failure "sprint declares removed ephemeral lifecycle field: $removedField."
            }
        }

        if ((ConvertTo-RecordToken -Value $jsonSprintStatus) -notin @('active', 'complete', 'blocked')) {
            Add-Failure "sprint.status is not a supported workflow state: '$jsonSprintStatus'."
        }
        if ((ConvertTo-RecordToken -Value $jsonRiskLevel) -notin @('critical', 'elevated', 'routine')) {
            Add-Failure "sprint.risk_level must be 'routine', 'elevated', or 'critical'; found '$jsonRiskLevel'."
        }

        $platform = Get-PropertyValue -Object $sprint -Name 'platform' -Path 'sprint.platform'
        if ($null -eq $platform) {
            Add-Failure 'Required object field is invalid: sprint.platform'
        }
        else {
            $officialInterpreter = Test-RequiredString -Object $platform -Name 'official_interpreter' -Path 'sprint.platform.official_interpreter'
            $saveVersion = Get-PropertyValue -Object $platform -Name 'save_version' -Path 'sprint.platform.save_version'
            $providerRequests = Test-RequiredString -Object $platform -Name 'provider_requests' -Path 'sprint.platform.provider_requests'
            if ($officialInterpreter -ne $null -and $officialInterpreter.Replace('/', '\').ToLowerInvariant() -cne '.\.venv\scripts\python.exe') {
                Add-Failure "sprint.platform.official_interpreter must be '.\.venv\Scripts\python.exe'; found '$officialInterpreter'."
            }
            if (($saveVersion -isnot [System.Int32] -and $saveVersion -isnot [System.Int64]) -or $saveVersion -ne 1) {
                Add-Failure "sprint.platform.save_version must be exactly integer 1; found '$saveVersion'."
            }
            if ($providerRequests -ne $null -and (ConvertTo-RecordToken -Value $providerRequests) -cne 'forbidden') {
                Add-Failure "sprint.platform.provider_requests must normalize to required value 'forbidden'; found '$providerRequests'."
            }
        }
    }

    if ($null -ne $nextSprint) {
        Add-Failure "next_sprint must remain null until separately authorized; found '$nextSprint'."
    }

    if ($null -eq $activeSprint) {
        if ($null -ne $activePackage) {
            Add-Failure "active_capability_package mismatch: active_sprint is 'null'; active_capability_package is '$activePackage'."
        }
        if ($jsonSprintStatus -ne $null -and (ConvertTo-RecordToken -Value $jsonSprintStatus) -notin @('complete', 'blocked')) {
            Add-Failure "sprint.status must be terminal when active_sprint is null; found '$jsonSprintStatus'."
        }
        if ($jsonSprintId -ne $null -and $latestCompletedId -ne $null -and $jsonSprintId -ne $latestCompletedId) {
            Add-Failure "latest_completed_sprint.id mismatch: sprint.id is '$jsonSprintId'; latest_completed_sprint.id is '$latestCompletedId'."
        }
    }
    else {
        if ($activePackage -ne $activeSprint) {
            Add-Failure "active_capability_package mismatch: active_capability_package is '$activePackage'; active_sprint is '$activeSprint'."
        }
        if ($jsonSprintId -ne $activeSprint) {
            Add-Failure "active_sprint mismatch: active_sprint is '$activeSprint'; sprint.id is '$jsonSprintId'."
        }
        if ($jsonSprintStatus -ne $null -and (ConvertTo-RecordToken -Value $jsonSprintStatus) -ne 'active') {
            Add-Failure "sprint.status must be 'active' while active_sprint is set; found '$jsonSprintStatus'."
        }
    }
}

Write-Host ''
Write-Host ('Validation summary: {0} passed, {1} failed.' -f $script:Passes.Count, $script:Failures.Count)

if ($script:Failures.Count -gt 0) {
    exit 1
}

exit 0
