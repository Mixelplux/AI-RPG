[CmdletBinding()]
param(
    [Parameter()]
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$validator = Join-Path $root 'tools\validate_project_records.ps1'
$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('project-record-fixtures-' + [guid]::NewGuid().ToString('N'))
$script:Passed = 0

function Write-FixtureFile {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$RelativePath,
        [Parameter(Mandatory = $true)][string]$Text
    )

    $path = Join-Path $Root $RelativePath
    [IO.Directory]::CreateDirectory((Split-Path -Parent $path)) | Out-Null
    [IO.File]::WriteAllText($path, $Text, [Text.UTF8Encoding]::new($false))
}

function New-JsonFixture {
    param([Parameter(Mandatory = $true)][ValidateSet('active', 'idle')][string]$Mode)

    $active = $Mode -eq 'active'
    $sprintId = if ($active) { '10.74' } else { '10.73' }
    $title = if ($active) {
        'Canonical Lifecycle Authority and Behavioral Verification Gate'
    }
    else {
        'Representative Bryn Shander Traversal Region and Topology Integrity'
    }
    $status = if ($active) { 'active' } else { 'complete' }
    $reviewState = if ($active) { 'implementation' } else { 'merged' }
    $candidateState = if ($active) { 'not_created' } else { 'accepted' }
    $mergeState = if ($active) { 'not_merged' } else { 'merged' }
    $predecessorId = if ($active) { '10.73' } else { '10.72' }

    $record = [ordered]@{
        schema_version = '1.1.0'
        document_type = 'current_sprint'
        sprint_count = 1
        lifecycle_authority = [ordered]@{
            machine_readable = 'docs/current_sprint.json'
            markdown_role = 'scope_rationale_acceptance_and_readable_status'
            yaml_required = $false
        }
        active_sprint = if ($active) { '10.74' } else { $null }
        active_capability_package = if ($active) { '10.74' } else { $null }
        latest_completed_sprint = [ordered]@{
            id = '10.73'
            status = 'complete'
            review_state = 'merged'
        }
        project = [ordered]@{ name = 'AI Narrative RPG Engine' }
        sprint = [ordered]@{
            id = $sprintId
            title = $title
            type = 'maintenance-package'
            mode = 'maintenance-package'
            status = $status
            review_state = $reviewState
            candidate_state = $candidateState
            merge_state = $mergeState
            goal = 'Fixture lifecycle goal.'
            predecessor = [ordered]@{
                id = $predecessorId
                status = 'complete'
                review_state = 'merged'
            }
            platform = [ordered]@{
                official_interpreter = '.\.venv\Scripts\python.exe'
                save_version = 1
                provider_requests = 'forbidden'
            }
            verification = [ordered]@{
                required_command = '& .\tools\run_offline_behavioral_verification.ps1'
                contract = 'complete_offline_behavioral'
            }
            closeout = [ordered]@{ next_sprint = $null }
        }
    }

    return $record | ConvertTo-Json -Depth 12
}

function New-MarkdownFixture {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('active', 'idle')][string]$Mode,
        [Parameter(Mandatory = $true)][string]$RecordKind
    )

    $active = $Mode -eq 'active'
    $sprintId = if ($active) { '10.74' } else { '10.73' }
    $title = if ($active) {
        'Canonical Lifecycle Authority and Behavioral Verification Gate'
    }
    else {
        'Representative Bryn Shander Traversal Region and Topology Integrity'
    }
    $status = if ($active) { 'Active' } else { 'Complete' }
    $reviewState = if ($active) { 'Implementation' } else { 'Merged' }
    $activeSprint = if ($active) { '10.74' } else { 'null' }
    $activePackage = if ($active) { '10.74' } else { 'null' }
    $candidateState = if ($active) { 'not_created' } else { 'accepted' }
    $mergeState = if ($active) { 'not_merged' } else { 'merged' }

    return @"
# Sprint $sprintId - $title

Status: $status.

Review state: $reviewState.

## Lifecycle Summary

This $RecordKind fixture is readable context. JSON is authoritative.

| Lifecycle field | Value |
|---|---|
| active_sprint | $activeSprint |
| active_capability_package | $activePackage |
| latest_completed_sprint | 10.73 |
| latest_completed_status | complete |
| next_sprint | null |
| candidate_state | $candidateState |
| merge_state | $mergeState |
| save_version | 1 |
| provider_requests | forbidden |
| official_interpreter | .\.venv\Scripts\python.exe |
| required_verification_command | & .\tools\run_offline_behavioral_verification.ps1 |

Verification contract: complete_offline_behavioral.

## Goal

Exercise project-record validation without changing repository state.
"@
}

function New-Fixture {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][ValidateSet('active', 'idle')][string]$Mode
    )

    $fixtureRoot = Join-Path $tempRoot $Name
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'AGENTS.md' -Text 'JSON is the sole machine-readable lifecycle authority.'
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'WORKFLOW.md' -Text 'Readable records must agree with JSON lifecycle state.'
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_sprint.json' -Text (New-JsonFixture -Mode $Mode)
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_sprint.md' -Text (New-MarkdownFixture -Mode $Mode -RecordKind 'sprint')
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_capability_package.md' -Text (New-MarkdownFixture -Mode $Mode -RecordKind 'package')
    return $fixtureRoot
}

function Replace-FixtureText {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$RelativePath,
        [Parameter(Mandatory = $true)][string]$OldValue,
        [Parameter(Mandatory = $true)][string]$NewValue
    )

    $path = Join-Path $Root $RelativePath
    $text = [IO.File]::ReadAllText($path)
    if (-not $text.Contains($OldValue)) {
        throw "Fixture mutation target not found in ${RelativePath}: $OldValue"
    }
    [IO.File]::WriteAllText($path, $text.Replace($OldValue, $NewValue), [Text.UTF8Encoding]::new($false))
}

function Set-FixtureJsonValue {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][ValidateSet('platform', 'verification', 'sprint', 'sprint_predecessor', 'latest_completed_sprint')][string]$Section,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)]$Value
    )

    $path = Join-Path $Root 'docs/current_sprint.json'
    $record = [IO.File]::ReadAllText($path) | ConvertFrom-Json
    $sectionObject = switch ($Section) {
        'sprint' { $record.sprint }
        'sprint_predecessor' { $record.sprint.predecessor }
        'latest_completed_sprint' { $record.latest_completed_sprint }
        default { $record.sprint.PSObject.Properties[$Section].Value }
    }
    $property = $sectionObject.PSObject.Properties[$Name]
    if ($null -eq $property) {
        throw "Fixture JSON field not found: sprint.$Section.$Name"
    }
    $property.Value = $Value
    $text = $record | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($path, $text, [Text.UTF8Encoding]::new($false))
}

function Invoke-FixtureValidator {
    param([Parameter(Mandatory = $true)][string]$FixtureRoot)

    $global:LASTEXITCODE = 0
    $output = & $validator -ProjectRoot $FixtureRoot *>&1 | Out-String
    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output = $output
    }
}

function Assert-Accepted {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$FixtureRoot
    )

    $result = Invoke-FixtureValidator -FixtureRoot $FixtureRoot
    if ($result.ExitCode -ne 0) {
        throw "$Name unexpectedly failed:`n$($result.Output)"
    }
    $script:Passed += 1
    Write-Output "PASS fixture: $Name"
}

function Assert-Rejected {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$FixtureRoot,
        [Parameter(Mandatory = $true)][string]$ExpectedMessage
    )

    $result = Invoke-FixtureValidator -FixtureRoot $FixtureRoot
    if ($result.ExitCode -eq 0) {
        throw "$Name unexpectedly passed."
    }
    $normalizedOutput = ($result.Output -replace '\s+', ' ').Trim()
    $normalizedExpected = ($ExpectedMessage -replace '\s+', ' ').Trim()
    if (-not $normalizedOutput.Contains($normalizedExpected)) {
        throw "$Name did not report the expected conflict '$ExpectedMessage':`n$($result.Output)"
    }
    $script:Passed += 1
    Write-Output "PASS fixture rejection: $Name"
}

try {
    [IO.Directory]::CreateDirectory($tempRoot) | Out-Null

    Assert-Accepted -Name 'consistent idle state' -FixtureRoot (New-Fixture -Name 'idle' -Mode idle)
    Assert-Accepted -Name 'consistent active-package state' -FixtureRoot (New-Fixture -Name 'active' -Mode active)

    $fixture = New-Fixture -Name 'established-review-ready-wording' -Mode active
    Set-FixtureJsonValue $fixture 'sprint' 'status' 'review_ready'
    foreach ($markdownPath in @('docs/current_sprint.md', 'docs/current_capability_package.md')) {
        Replace-FixtureText $fixture $markdownPath 'Status: Active.' 'Status: Ready for Independent Review.'
    }
    Assert-Accepted -Name 'established review-ready Markdown wording' -FixtureRoot $fixture

    $fixture = New-Fixture -Name 'mismatched-active-sprint' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| active_sprint | 10.74 |' '| active_sprint | 10.75 |'
    Assert-Rejected 'mismatched active sprint' $fixture "active_sprint mismatch: docs/current_sprint.md is '10.75'; docs/current_sprint.json is '10.74'."

    $fixture = New-Fixture -Name 'mismatched-active-package' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' '| active_capability_package | 10.74 |' '| active_capability_package | package-10.75 |'
    Assert-Rejected 'mismatched active capability package' $fixture "active_capability_package mismatch: docs/current_capability_package.md is 'package-10.75'; docs/current_sprint.json is '10.74'."

    $fixture = New-Fixture -Name 'mismatched-status' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' 'Status: Active.' 'Status: Planned.'
    Assert-Rejected 'mismatched sprint status' $fixture "sprint_status mismatch: docs/current_capability_package.md is 'Planned'; docs/current_sprint.json sprint.status is 'active'."

    $fixture = New-Fixture -Name 'mismatched-next-sprint' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| next_sprint | null |' '| next_sprint | 10.75 |'
    Assert-Rejected 'mismatched next_sprint' $fixture "next_sprint mismatch: docs/current_sprint.md is '10.75'; docs/current_sprint.json is 'null'."

    $fixture = New-Fixture -Name 'mismatched-review-state' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' 'Review state: Implementation.' 'Review state: Staged.'
    Assert-Rejected 'mismatched review state' $fixture "review_state mismatch: docs/current_sprint.md is 'Staged'; docs/current_sprint.json sprint.review_state is 'implementation'."

    $fixture = New-Fixture -Name 'mismatched-candidate-state' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| candidate_state | not_created |' '| candidate_state | created |'
    Assert-Rejected 'mismatched candidate state' $fixture "candidate_state mismatch: docs/current_sprint.md is 'created'; docs/current_sprint.json is 'not_created'."

    $fixture = New-Fixture -Name 'mismatched-merge-state' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' '| merge_state | not_merged |' '| merge_state | merged |'
    Assert-Rejected 'mismatched merge state' $fixture "merge_state mismatch: docs/current_capability_package.md is 'merged'; docs/current_sprint.json is 'not_merged'."

    $fixture = New-Fixture -Name 'mismatched-save-version' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' '| save_version | 1 |' '| save_version | 2 |'
    Assert-Rejected 'mismatched save version' $fixture "save_version mismatch: docs/current_capability_package.md is '2'; docs/current_sprint.json is '1'."

    $fixture = New-Fixture -Name 'mismatched-provider-policy' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| provider_requests | forbidden |' '| provider_requests | allowed |'
    Assert-Rejected 'mismatched provider policy' $fixture "provider_requests mismatch: docs/current_sprint.md is 'allowed'; docs/current_sprint.json is 'forbidden'."

    $fixture = New-Fixture -Name 'mismatched-interpreter' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| official_interpreter | .\.venv\Scripts\python.exe |' '| official_interpreter | python.exe |'
    Assert-Rejected 'mismatched official interpreter' $fixture "official_interpreter mismatch: docs/current_sprint.md is 'python.exe'; docs/current_sprint.json is '.\.venv\Scripts\python.exe'."

    $fixture = New-Fixture -Name 'mismatched-verification-command' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' '| required_verification_command | & .\tools\run_offline_behavioral_verification.ps1 |' '| required_verification_command | pytest |'
    Assert-Rejected 'mismatched verification command' $fixture "required_verification_command mismatch: docs/current_capability_package.md is 'pytest'; docs/current_sprint.json is '& .\tools\run_offline_behavioral_verification.ps1'."

    $fixture = New-Fixture -Name 'synchronized-unsafe-save-version' -Mode active
    Set-FixtureJsonValue $fixture 'platform' 'save_version' 2
    foreach ($markdownPath in @('docs/current_sprint.md', 'docs/current_capability_package.md')) {
        Replace-FixtureText $fixture $markdownPath '| save_version | 1 |' '| save_version | 2 |'
    }
    Assert-Rejected 'synchronized unsafe save version' $fixture "sprint.platform.save_version must be exactly integer 1; found '2'."

    $fixture = New-Fixture -Name 'synchronized-unsafe-provider-policy' -Mode active
    Set-FixtureJsonValue $fixture 'platform' 'provider_requests' 'allowed'
    foreach ($markdownPath in @('docs/current_sprint.md', 'docs/current_capability_package.md')) {
        Replace-FixtureText $fixture $markdownPath '| provider_requests | forbidden |' '| provider_requests | allowed |'
    }
    Assert-Rejected 'synchronized unsafe provider policy' $fixture "sprint.platform.provider_requests must normalize to required value 'forbidden'; found 'allowed'."

    $fixture = New-Fixture -Name 'synchronized-unsafe-verification-command' -Mode active
    Set-FixtureJsonValue $fixture 'verification' 'required_command' 'pytest'
    foreach ($markdownPath in @('docs/current_sprint.md', 'docs/current_capability_package.md')) {
        Replace-FixtureText $fixture $markdownPath '| required_verification_command | & .\tools\run_offline_behavioral_verification.ps1 |' '| required_verification_command | pytest |'
    }
    Assert-Rejected 'synchronized unsafe verification command' $fixture "sprint.verification.required_command must normalize to required value '& .\tools\run_offline_behavioral_verification.ps1'; found 'pytest'."

    $fixture = New-Fixture -Name 'synchronized-unsafe-verification-contract' -Mode active
    Set-FixtureJsonValue $fixture 'verification' 'contract' 'replacement_contract'
    foreach ($markdownPath in @('docs/current_sprint.md', 'docs/current_capability_package.md')) {
        Replace-FixtureText $fixture $markdownPath 'Verification contract: complete_offline_behavioral.' 'Verification contract: replacement_contract.'
    }
    Assert-Rejected 'synchronized unsafe verification contract' $fixture "sprint.verification.contract must normalize to required value 'complete_offline_behavioral'; found 'replacement_contract'."

    $fixture = New-Fixture -Name 'synchronized-stale-predecessor-review-state' -Mode active
    Set-FixtureJsonValue $fixture 'latest_completed_sprint' 'review_state' 'candidate_prepared'
    Set-FixtureJsonValue $fixture 'sprint_predecessor' 'review_state' 'candidate_prepared'
    Assert-Rejected 'synchronized stale predecessor review state' $fixture "latest_completed_sprint.review_state must normalize to required value 'merged'; found 'candidate_prepared'."

    $fixture = New-Fixture -Name 'mismatched-latest-completed' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '| latest_completed_sprint | 10.73 |' '| latest_completed_sprint | 10.72 |'
    Assert-Rejected 'mismatched latest completed sprint' $fixture "latest_completed_sprint mismatch: docs/current_sprint.md is '10.72'; docs/current_sprint.json is '10.73'."

    $fixture = New-Fixture -Name 'mismatched-latest-status' -Mode active
    Replace-FixtureText $fixture 'docs/current_capability_package.md' '| latest_completed_status | complete |' '| latest_completed_status | active |'
    Assert-Rejected 'mismatched latest completed status' $fixture "latest_completed_status mismatch: docs/current_capability_package.md is 'active'; docs/current_sprint.json is 'complete'."

    $fixture = New-Fixture -Name 'mismatched-title' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.md' '# Sprint 10.74 - Canonical Lifecycle Authority and Behavioral Verification Gate' '# Sprint 10.74 - Wrong Title'
    Assert-Rejected 'mismatched retained sprint title' $fixture "sprint_title mismatch: docs/current_sprint.md is 'Wrong Title'; docs/current_sprint.json sprint.title is 'Canonical Lifecycle Authority and Behavioral Verification Gate'."

    $fixture = New-Fixture -Name 'forbidden-yaml-reference' -Mode active
    Write-FixtureFile $fixture 'WORKFLOW.md' 'Validate Markdown/JSON/YAML agreement as canonical lifecycle state.'
    Assert-Rejected 'forbidden YAML lifecycle authority reference' $fixture "Forbidden YAML lifecycle authority reference in WORKFLOW.md: 'Markdown/JSON/YAML agreement'."

    Write-Output "Project-record fixture summary: $script:Passed passed."
}
finally {
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}

exit 0
