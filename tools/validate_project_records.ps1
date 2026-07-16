[CmdletBinding()]
param(
    [Parameter()]
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
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

function Get-MarkdownSprintRecord {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $text = Get-Content -LiteralPath $Path -Raw
    $heading = [regex]::Match(
        $text,
        '(?m)^#\s+Sprint\s+(?<id>[^\s]+)\s+-\s+(?<title>[^\r\n]+?)\s*$'
    )
    $status = [regex]::Match($text, '(?im)^Status:\s*(?<status>[^\r\n.]+)\.?\s*$')

    if (-not $heading.Success) {
        Add-Failure "$Label must declare '# Sprint <id> - <title>'."
        return $null
    }

    if (-not $status.Success) {
        Add-Failure "$Label must declare a Status line."
        return $null
    }

    return [pscustomobject]@{
        id = $heading.Groups['id'].Value.Trim()
        title = $heading.Groups['title'].Value.Trim()
        status = $status.Groups['status'].Value.Trim()
    }
}

function ConvertTo-RecordStatus {
    param([Parameter(Mandatory = $true)][string]$Status)

    $normalized = ($Status.Trim().ToLowerInvariant() -replace '[^a-z0-9]+', '_').Trim('_')
    switch ($normalized) {
        'ready_for_independent_review' { return 'review_ready' }
        'ready_for_review' { return 'review_ready' }
        default { return $normalized }
    }
}

function Compare-RecordField {
    param(
        [Parameter(Mandatory = $true)][string]$Field,
        [Parameter(Mandatory = $true)][string]$LeftLabel,
        [AllowNull()]$LeftValue,
        [Parameter(Mandatory = $true)][string]$RightLabel,
        [AllowNull()]$RightValue
    )

    if ($null -ne $LeftValue -and $null -ne $RightValue -and $LeftValue -ne $RightValue) {
        Add-Failure "$Field mismatch: $LeftLabel is '$LeftValue'; $RightLabel is '$RightValue'."
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

$jsonPath = Join-Path $root 'docs/current_sprint.json'
$sprintMarkdownPath = Join-Path $root 'docs/current_sprint.md'
$packageMarkdownPath = Join-Path $root 'docs/current_capability_package.md'

foreach ($recordPath in @($jsonPath, $sprintMarkdownPath, $packageMarkdownPath)) {
    if (Test-Path -LiteralPath $recordPath -PathType Leaf) {
        Add-Pass "Found $(Split-Path -Leaf $recordPath)."
    }
    else {
        Add-Failure "Missing required project record: $recordPath"
    }
}

if ($script:Failures.Count -gt 0) {
    Write-Host 'Validation stopped because a required project record is missing.'
    exit 1
}

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

$sprintMarkdown = $null
$packageMarkdown = $null
try {
    $sprintMarkdown = Get-MarkdownSprintRecord -Path $sprintMarkdownPath -Label 'docs/current_sprint.md'
    if ($null -ne $sprintMarkdown) {
        Add-Pass 'docs/current_sprint.md declares sprint identity and status.'
    }
}
catch {
    Add-Failure "docs/current_sprint.md could not be read: $($_.Exception.Message)"
}

try {
    $packageMarkdown = Get-MarkdownSprintRecord -Path $packageMarkdownPath -Label 'docs/current_capability_package.md'
    if ($null -ne $packageMarkdown) {
        Add-Pass 'docs/current_capability_package.md declares sprint identity and status.'
    }
}
catch {
    Add-Failure "docs/current_capability_package.md could not be read: $($_.Exception.Message)"
}

if ($null -ne $jsonRecord) {
    $schemaVersion = Test-RequiredString -Object $jsonRecord -Name 'schema_version' -Path 'schema_version'
    $documentType = Test-RequiredString -Object $jsonRecord -Name 'document_type' -Path 'document_type'
    $sprintCount = Get-PropertyValue -Object $jsonRecord -Name 'sprint_count' -Path 'sprint_count'
    $sprint = Get-PropertyValue -Object $jsonRecord -Name 'sprint' -Path 'sprint'

    if ($documentType -ne $null -and $documentType -ne 'current_sprint') {
        Add-Failure "document_type must be 'current_sprint'; found '$documentType'."
    }
    if ($sprintCount -ne 1) {
        Add-Failure "sprint_count must be 1; found '$sprintCount'."
    }

    $jsonSprintId = $null
    $jsonSprintTitle = $null
    $jsonSprintStatus = $null
    if ($null -eq $sprint) {
        Add-Failure 'Required object field is invalid: sprint'
    }
    else {
        $jsonSprintId = Test-RequiredString -Object $sprint -Name 'id' -Path 'sprint.id'
        $jsonSprintTitle = Test-RequiredString -Object $sprint -Name 'title' -Path 'sprint.title'
        $jsonSprintType = Test-RequiredString -Object $sprint -Name 'type' -Path 'sprint.type'
        $jsonSprintMode = Test-RequiredString -Object $sprint -Name 'mode' -Path 'sprint.mode'
        $jsonSprintStatus = Test-RequiredString -Object $sprint -Name 'status' -Path 'sprint.status'
        $jsonSprintGoal = Test-RequiredString -Object $sprint -Name 'goal' -Path 'sprint.goal'

        if ($jsonSprintStatus -ne $null -and @('planned', 'active', 'review_ready', 'complete', 'blocked') -notcontains $jsonSprintStatus) {
            Add-Failure "sprint.status is not a supported workflow state: '$jsonSprintStatus'."
        }

        $closeout = Get-PropertyValue -Object $sprint -Name 'closeout' -Path 'sprint.closeout'
        if ($null -eq $closeout) {
            Add-Failure 'Required object field is invalid: sprint.closeout'
        }
        else {
            $nextSprintProperty = $closeout.PSObject.Properties['next_sprint']
            if ($null -eq $nextSprintProperty) {
                Add-Failure 'Missing required field: sprint.closeout.next_sprint'
            }
            elseif ($null -eq $nextSprintProperty.Value) {
                Add-Pass 'next_sprint is null; no next package is required.'
            }
            else {
                Add-Failure 'sprint.closeout.next_sprint must be null until a next package is explicitly authorized.'
            }
        }
    }

    if ($null -ne $sprintMarkdown) {
        Compare-RecordField -Field 'Sprint id' -LeftLabel 'docs/current_sprint.md' -LeftValue $sprintMarkdown.id -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintId
        Compare-RecordField -Field 'Sprint title' -LeftLabel 'docs/current_sprint.md' -LeftValue $sprintMarkdown.title -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintTitle
        Compare-RecordField -Field 'Sprint status' -LeftLabel 'docs/current_sprint.md' -LeftValue (ConvertTo-RecordStatus -Status $sprintMarkdown.status) -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintStatus
    }

    if ($null -ne $packageMarkdown) {
        Compare-RecordField -Field 'Package/sprint id' -LeftLabel 'docs/current_capability_package.md' -LeftValue $packageMarkdown.id -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintId
        Compare-RecordField -Field 'Package/sprint title' -LeftLabel 'docs/current_capability_package.md' -LeftValue $packageMarkdown.title -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintTitle
        Compare-RecordField -Field 'Package/sprint status' -LeftLabel 'docs/current_capability_package.md' -LeftValue (ConvertTo-RecordStatus -Status $packageMarkdown.status) -RightLabel 'docs/current_sprint.json' -RightValue $jsonSprintStatus
    }
}

Write-Host ''
Write-Host ('Validation summary: {0} passed, {1} failed.' -f $script:Passes.Count, $script:Failures.Count)

if ($script:Failures.Count -gt 0) {
    exit 1
}

exit 0
