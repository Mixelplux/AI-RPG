[CmdletBinding()]
param(
    [Parameter()]
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:Failures = New-Object System.Collections.Generic.List[string]
$script:Passes = New-Object System.Collections.Generic.List[string]
$script:LifecycleFields = @(
    'active_sprint',
    'active_capability_package',
    'latest_completed_sprint',
    'latest_completed_status',
    'next_sprint',
    'candidate_state',
    'merge_state',
    'save_version',
    'provider_requests',
    'official_interpreter',
    'required_verification_command'
)

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

function Normalize-FieldValue {
    param(
        [Parameter(Mandatory = $true)][string]$Field,
        [AllowNull()]$Value
    )

    if ($null -eq $Value) {
        return $null
    }

    $text = ([string]$Value).Trim()
    switch ($Field) {
        'sprint_status' {
            $normalizedStatus = ConvertTo-RecordToken -Value $text
            if ($normalizedStatus -in @('ready_for_independent_review', 'ready_for_review', 'review_ready')) {
                return 'review_ready'
            }
            return $normalizedStatus
        }
        { $_ -in @('latest_completed_status', 'review_state', 'candidate_state', 'merge_state', 'provider_requests') } {
            return ConvertTo-RecordToken -Value $text
        }
        'official_interpreter' {
            return $text.Replace('/', '\').ToLowerInvariant()
        }
        'required_verification_command' {
            return (($text -replace '\s+', ' ').Replace('/', '\')).Trim()
        }
        default {
            return $text
        }
    }
}

function Format-FieldValue {
    param([AllowNull()]$Value)

    if ($null -eq $Value) {
        return 'null'
    }

    return [string]$Value
}

function Compare-RecordField {
    param(
        [Parameter(Mandatory = $true)][string]$Field,
        [Parameter(Mandatory = $true)][string]$LeftLabel,
        [AllowNull()]$LeftValue,
        [Parameter(Mandatory = $true)][string]$RightLabel,
        [AllowNull()]$RightValue
    )

    $left = Normalize-FieldValue -Field $Field -Value $LeftValue
    $right = Normalize-FieldValue -Field $Field -Value $RightValue
    $matches = if ($null -eq $left -or $null -eq $right) {
        $null -eq $left -and $null -eq $right
    }
    else {
        $left -ceq $right
    }

    if (-not $matches) {
        Add-Failure "$Field mismatch: $LeftLabel is '$(Format-FieldValue -Value $LeftValue)'; $RightLabel is '$(Format-FieldValue -Value $RightValue)'."
    }
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
    $reviewState = [regex]::Match($text, '(?im)^Review state:\s*(?<state>[^\r\n.]+)\.?\s*$')

    if (-not $heading.Success) {
        Add-Failure "$Label must declare '# Sprint <id> - <title>'."
    }
    if (-not $status.Success) {
        Add-Failure "$Label must declare a Status line."
    }
    if (-not $reviewState.Success) {
        Add-Failure "$Label must declare a Review state line."
    }

    $lifecycle = @{}
    foreach ($line in ($text -split '\r?\n')) {
        $match = [regex]::Match(
            $line,
            '^\|\s*`?(?<key>[a-z_]+)`?\s*\|\s*(?<value>.*?)\s*\|\s*$'
        )
        if (-not $match.Success) {
            continue
        }

        $key = $match.Groups['key'].Value
        if ($script:LifecycleFields -notcontains $key) {
            continue
        }
        if ($lifecycle.ContainsKey($key)) {
            Add-Failure "$Label declares duplicate lifecycle field: $key"
            continue
        }

        $value = $match.Groups['value'].Value.Trim()
        if ($value.Length -ge 2 -and $value.StartsWith('`') -and $value.EndsWith('`')) {
            $value = $value.Substring(1, $value.Length - 2).Trim()
        }
        if ($value -ieq 'null') {
            $lifecycle[$key] = $null
        }
        elseif ([string]::IsNullOrWhiteSpace($value)) {
            Add-Failure "$Label lifecycle field is empty: $key"
        }
        else {
            $lifecycle[$key] = $value
        }
    }

    foreach ($field in $script:LifecycleFields) {
        if (-not $lifecycle.ContainsKey($field)) {
            Add-Failure "$Label is missing lifecycle field: $field"
        }
    }

    if (-not $heading.Success -or -not $status.Success -or -not $reviewState.Success) {
        return $null
    }

    return [pscustomobject]@{
        id = $heading.Groups['id'].Value.Trim()
        title = $heading.Groups['title'].Value.Trim()
        status = $status.Groups['status'].Value.Trim()
        review_state = $reviewState.Groups['state'].Value.Trim()
        lifecycle = $lifecycle
    }
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
$sprintMarkdownPath = Join-Path $root 'docs/current_sprint.md'
$packageMarkdownPath = Join-Path $root 'docs/current_capability_package.md'

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
        Add-Pass 'docs/current_sprint.md declares readable sprint and lifecycle status.'
    }
}
catch {
    Add-Failure "docs/current_sprint.md could not be read: $($_.Exception.Message)"
}

try {
    $packageMarkdown = Get-MarkdownSprintRecord -Path $packageMarkdownPath -Label 'docs/current_capability_package.md'
    if ($null -ne $packageMarkdown) {
        Add-Pass 'docs/current_capability_package.md declares readable package and lifecycle status.'
    }
}
catch {
    Add-Failure "docs/current_capability_package.md could not be read: $($_.Exception.Message)"
}

if ($null -ne $jsonRecord) {
    $schemaVersion = Test-RequiredString -Object $jsonRecord -Name 'schema_version' -Path 'schema_version'
    $documentType = Test-RequiredString -Object $jsonRecord -Name 'document_type' -Path 'document_type'
    $sprintCount = Get-PropertyValue -Object $jsonRecord -Name 'sprint_count' -Path 'sprint_count'
    $authority = Get-PropertyValue -Object $jsonRecord -Name 'lifecycle_authority' -Path 'lifecycle_authority'
    $activeSprint = Get-NullableIdentifier -Object $jsonRecord -Name 'active_sprint' -Path 'active_sprint'
    $activePackage = Get-NullableIdentifier -Object $jsonRecord -Name 'active_capability_package' -Path 'active_capability_package'
    $latestCompleted = Get-PropertyValue -Object $jsonRecord -Name 'latest_completed_sprint' -Path 'latest_completed_sprint'
    $sprint = Get-PropertyValue -Object $jsonRecord -Name 'sprint' -Path 'sprint'

    if ($schemaVersion -ne $null -and $schemaVersion -ne '1.1.0') {
        Add-Failure "schema_version must be '1.1.0'; found '$schemaVersion'."
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
        if ($markdownRole -ne $null -and $markdownRole -ne 'scope_rationale_acceptance_and_readable_status') {
            Add-Failure "lifecycle_authority.markdown_role is invalid: '$markdownRole'."
        }
        if ($yamlRequired -isnot [bool] -or $yamlRequired) {
            Add-Failure 'lifecycle_authority.yaml_required must be false.'
        }
    }

    $latestCompletedId = $null
    $latestCompletedStatus = $null
    $latestCompletedReviewState = $null
    if ($null -eq $latestCompleted) {
        Add-Failure 'Required object field is invalid: latest_completed_sprint'
    }
    else {
        $latestCompletedId = Test-RequiredString -Object $latestCompleted -Name 'id' -Path 'latest_completed_sprint.id'
        $latestCompletedStatus = Test-RequiredString -Object $latestCompleted -Name 'status' -Path 'latest_completed_sprint.status'
        $latestCompletedReviewState = Test-RequiredString -Object $latestCompleted -Name 'review_state' -Path 'latest_completed_sprint.review_state'
        if ((ConvertTo-RecordToken -Value $latestCompletedStatus) -ne 'complete') {
            Add-Failure "latest_completed_sprint.status must be 'complete'; found '$latestCompletedStatus'."
        }
        if ((ConvertTo-RecordToken -Value $latestCompletedReviewState) -ne 'merged') {
            Add-Failure "latest_completed_sprint.review_state must normalize to required value 'merged'; found '$latestCompletedReviewState'."
        }
    }

    $jsonSprintId = $null
    $jsonSprintTitle = $null
    $jsonSprintStatus = $null
    $jsonReviewState = $null
    $jsonCandidateState = $null
    $jsonMergeState = $null
    $jsonSaveVersion = $null
    $jsonProviderRequests = $null
    $jsonOfficialInterpreter = $null
    $jsonRequiredVerification = $null
    $jsonVerificationContract = $null
    $jsonNextSprint = $null
    if ($null -eq $sprint) {
        Add-Failure 'Required object field is invalid: sprint'
    }
    else {
        $jsonSprintId = Test-RequiredString -Object $sprint -Name 'id' -Path 'sprint.id'
        $jsonSprintTitle = Test-RequiredString -Object $sprint -Name 'title' -Path 'sprint.title'
        [void](Test-RequiredString -Object $sprint -Name 'type' -Path 'sprint.type')
        [void](Test-RequiredString -Object $sprint -Name 'mode' -Path 'sprint.mode')
        $jsonSprintStatus = Test-RequiredString -Object $sprint -Name 'status' -Path 'sprint.status'
        $jsonReviewState = Test-RequiredString -Object $sprint -Name 'review_state' -Path 'sprint.review_state'
        $jsonCandidateState = Test-RequiredString -Object $sprint -Name 'candidate_state' -Path 'sprint.candidate_state'
        $jsonMergeState = Test-RequiredString -Object $sprint -Name 'merge_state' -Path 'sprint.merge_state'
        [void](Test-RequiredString -Object $sprint -Name 'goal' -Path 'sprint.goal')

        if ((ConvertTo-RecordToken -Value $jsonSprintStatus) -notin @('planned', 'active', 'review_ready', 'complete', 'blocked')) {
            Add-Failure "sprint.status is not a supported workflow state: '$jsonSprintStatus'."
        }
        if ((ConvertTo-RecordToken -Value $jsonCandidateState) -notin @('not_created', 'created', 'accepted', 'rejected')) {
            Add-Failure "sprint.candidate_state is not supported: '$jsonCandidateState'."
        }
        if ((ConvertTo-RecordToken -Value $jsonMergeState) -notin @('not_merged', 'merged')) {
            Add-Failure "sprint.merge_state is not supported: '$jsonMergeState'."
        }

        $predecessor = Get-PropertyValue -Object $sprint -Name 'predecessor' -Path 'sprint.predecessor'
        if ($null -eq $predecessor) {
            Add-Failure 'Required object field is invalid: sprint.predecessor'
        }
        else {
            $predecessorId = Test-RequiredString -Object $predecessor -Name 'id' -Path 'sprint.predecessor.id'
            $predecessorStatus = Test-RequiredString -Object $predecessor -Name 'status' -Path 'sprint.predecessor.status'
            $predecessorReview = Test-RequiredString -Object $predecessor -Name 'review_state' -Path 'sprint.predecessor.review_state'
            if ($null -ne $activeSprint) {
                Compare-RecordField -Field 'latest_completed_sprint' -LeftLabel 'docs/current_sprint.json sprint.predecessor.id' -LeftValue $predecessorId -RightLabel 'docs/current_sprint.json latest_completed_sprint.id' -RightValue $latestCompletedId
                Compare-RecordField -Field 'latest_completed_status' -LeftLabel 'docs/current_sprint.json sprint.predecessor.status' -LeftValue $predecessorStatus -RightLabel 'docs/current_sprint.json latest_completed_sprint.status' -RightValue $latestCompletedStatus
                Compare-RecordField -Field 'review_state' -LeftLabel 'docs/current_sprint.json sprint.predecessor.review_state' -LeftValue $predecessorReview -RightLabel 'docs/current_sprint.json latest_completed_sprint.review_state' -RightValue $latestCompletedReviewState
            }
        }

        $platform = Get-PropertyValue -Object $sprint -Name 'platform' -Path 'sprint.platform'
        if ($null -eq $platform) {
            Add-Failure 'Required object field is invalid: sprint.platform'
        }
        else {
            $jsonOfficialInterpreter = Test-RequiredString -Object $platform -Name 'official_interpreter' -Path 'sprint.platform.official_interpreter'
            $jsonSaveVersion = Get-PropertyValue -Object $platform -Name 'save_version' -Path 'sprint.platform.save_version'
            $jsonProviderRequests = Test-RequiredString -Object $platform -Name 'provider_requests' -Path 'sprint.platform.provider_requests'
            if ((Normalize-FieldValue -Field 'official_interpreter' -Value $jsonOfficialInterpreter) -cne '.\.venv\scripts\python.exe') {
                Add-Failure "sprint.platform.official_interpreter must be '.\.venv\Scripts\python.exe'; found '$jsonOfficialInterpreter'."
            }
            if ($jsonSaveVersion -isnot [int] -or $jsonSaveVersion -ne 1) {
                Add-Failure "sprint.platform.save_version must be exactly integer 1; found '$jsonSaveVersion'."
            }
            if (
                $null -ne $jsonProviderRequests -and
                (Normalize-FieldValue -Field 'provider_requests' -Value $jsonProviderRequests) -cne 'forbidden'
            ) {
                Add-Failure "sprint.platform.provider_requests must normalize to required value 'forbidden'; found '$jsonProviderRequests'."
            }
        }

        $verification = Get-PropertyValue -Object $sprint -Name 'verification' -Path 'sprint.verification'
        if ($null -eq $verification) {
            Add-Failure 'Required object field is invalid: sprint.verification'
        }
        else {
            $jsonRequiredVerification = Test-RequiredString -Object $verification -Name 'required_command' -Path 'sprint.verification.required_command'
            $jsonVerificationContract = Test-RequiredString -Object $verification -Name 'contract' -Path 'sprint.verification.contract'
            if (
                $null -ne $jsonRequiredVerification -and
                (Normalize-FieldValue -Field 'required_verification_command' -Value $jsonRequiredVerification) -cne '& .\tools\run_offline_behavioral_verification.ps1'
            ) {
                Add-Failure "sprint.verification.required_command must normalize to required value '& .\tools\run_offline_behavioral_verification.ps1'; found '$jsonRequiredVerification'."
            }
            if (
                $null -ne $jsonVerificationContract -and
                (ConvertTo-RecordToken -Value $jsonVerificationContract) -cne 'complete_offline_behavioral'
            ) {
                Add-Failure "sprint.verification.contract must normalize to required value 'complete_offline_behavioral'; found '$jsonVerificationContract'."
            }
        }

        $closeout = Get-PropertyValue -Object $sprint -Name 'closeout' -Path 'sprint.closeout'
        if ($null -eq $closeout) {
            Add-Failure 'Required object field is invalid: sprint.closeout'
        }
        else {
            $nextProperty = $closeout.PSObject.Properties['next_sprint']
            if ($null -eq $nextProperty) {
                Add-Failure 'Missing required field: sprint.closeout.next_sprint'
            }
            else {
                $jsonNextSprint = $nextProperty.Value
                if ($null -ne $jsonNextSprint) {
                    Add-Failure "sprint.closeout.next_sprint must remain null until separately authorized; found '$jsonNextSprint'."
                }
            }
        }
    }

    if ($null -eq $activeSprint) {
        if ($null -ne $activePackage) {
            Add-Failure "active_capability_package mismatch: docs/current_sprint.json active_sprint is 'null'; docs/current_sprint.json active_capability_package is '$activePackage'."
        }
        if ($null -ne $jsonSprintStatus -and (ConvertTo-RecordToken -Value $jsonSprintStatus) -notin @('complete', 'blocked')) {
            Add-Failure "sprint.status must be terminal when active_sprint is null; found '$jsonSprintStatus'."
        }
        Compare-RecordField -Field 'latest_completed_sprint' -LeftLabel 'docs/current_sprint.json sprint.id' -LeftValue $jsonSprintId -RightLabel 'docs/current_sprint.json latest_completed_sprint.id' -RightValue $latestCompletedId
        Compare-RecordField -Field 'latest_completed_status' -LeftLabel 'docs/current_sprint.json sprint.status' -LeftValue $jsonSprintStatus -RightLabel 'docs/current_sprint.json latest_completed_sprint.status' -RightValue $latestCompletedStatus
        Compare-RecordField -Field 'review_state' -LeftLabel 'docs/current_sprint.json sprint.review_state' -LeftValue $jsonReviewState -RightLabel 'docs/current_sprint.json latest_completed_sprint.review_state' -RightValue $latestCompletedReviewState
    }
    else {
        Compare-RecordField -Field 'active_sprint' -LeftLabel 'docs/current_sprint.json active_sprint' -LeftValue $activeSprint -RightLabel 'docs/current_sprint.json sprint.id' -RightValue $jsonSprintId
        Compare-RecordField -Field 'active_capability_package' -LeftLabel 'docs/current_sprint.json active_capability_package' -LeftValue $activePackage -RightLabel 'docs/current_sprint.json active_sprint' -RightValue $activeSprint
        if ($null -ne $jsonSprintStatus -and (ConvertTo-RecordToken -Value $jsonSprintStatus) -notin @('planned', 'active', 'review_ready')) {
            Add-Failure "sprint.status must be nonterminal while active_sprint is set; found '$jsonSprintStatus'."
        }
    }

    $canonicalLifecycle = @{
        active_sprint = $activeSprint
        active_capability_package = $activePackage
        latest_completed_sprint = $latestCompletedId
        latest_completed_status = $latestCompletedStatus
        next_sprint = $jsonNextSprint
        candidate_state = $jsonCandidateState
        merge_state = $jsonMergeState
        save_version = $jsonSaveVersion
        provider_requests = $jsonProviderRequests
        official_interpreter = $jsonOfficialInterpreter
        required_verification_command = $jsonRequiredVerification
    }

    foreach ($markdownEntry in @(
        @{ Label = 'docs/current_sprint.md'; Record = $sprintMarkdown },
        @{ Label = 'docs/current_capability_package.md'; Record = $packageMarkdown }
    )) {
        $record = $markdownEntry.Record
        if ($null -eq $record) {
            continue
        }

        Compare-RecordField -Field 'sprint_id' -LeftLabel $markdownEntry.Label -LeftValue $record.id -RightLabel 'docs/current_sprint.json sprint.id' -RightValue $jsonSprintId
        Compare-RecordField -Field 'sprint_title' -LeftLabel $markdownEntry.Label -LeftValue $record.title -RightLabel 'docs/current_sprint.json sprint.title' -RightValue $jsonSprintTitle
        Compare-RecordField -Field 'sprint_status' -LeftLabel $markdownEntry.Label -LeftValue $record.status -RightLabel 'docs/current_sprint.json sprint.status' -RightValue $jsonSprintStatus
        Compare-RecordField -Field 'review_state' -LeftLabel $markdownEntry.Label -LeftValue $record.review_state -RightLabel 'docs/current_sprint.json sprint.review_state' -RightValue $jsonReviewState
        foreach ($field in $script:LifecycleFields) {
            if ($record.lifecycle.ContainsKey($field)) {
                Compare-RecordField -Field $field -LeftLabel $markdownEntry.Label -LeftValue $record.lifecycle[$field] -RightLabel 'docs/current_sprint.json' -RightValue $canonicalLifecycle[$field]
            }
        }
    }
}

Write-Host ''
Write-Host ('Validation summary: {0} passed, {1} failed.' -f $script:Passes.Count, $script:Failures.Count)

if ($script:Failures.Count -gt 0) {
    exit 1
}

exit 0
