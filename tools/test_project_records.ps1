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
    param([Parameter(Mandatory = $true)][ValidateSet('active', 'complete')][string]$Mode)

    $active = $Mode -eq 'active'
    $sprintId = if ($active) { '10.75' } else { '10.74' }
    $status = if ($active) { 'active' } else { 'complete' }
    $record = [ordered]@{
        schema_version = '1.2.0'
        document_type = 'current_sprint'
        sprint_count = 1
        lifecycle_authority = [ordered]@{
            machine_readable = 'docs/current_sprint.json'
            markdown_role = 'explanatory_records'
            yaml_required = $false
        }
        active_sprint = if ($active) { $sprintId } else { $null }
        active_capability_package = if ($active) { $sprintId } else { $null }
        latest_completed_sprint = [ordered]@{ id = if ($active) { '10.74' } else { $sprintId } }
        next_sprint = $null
        sprint = [ordered]@{
            id = $sprintId
            title = 'Fixture lifecycle record'
            type = 'maintenance-package'
            status = $status
            risk_level = 'routine'
            goal = 'Fixture lifecycle goal.'
            platform = [ordered]@{
                official_interpreter = '.\.venv\Scripts\python.exe'
                save_version = 1
                provider_requests = 'forbidden'
            }
        }
    }

    return $record | ConvertTo-Json -Depth 10
}

function New-Fixture {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][ValidateSet('active', 'complete')][string]$Mode
    )

    $fixtureRoot = Join-Path $tempRoot $Name
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'AGENTS.md' -Text 'JSON is the sole machine-enforced lifecycle authority.'
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'WORKFLOW.md' -Text 'Markdown lifecycle records are explanatory, not machine authorities.'
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_sprint.json' -Text (New-JsonFixture -Mode $Mode)
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_sprint.md' -Text 'This is explanatory Markdown, deliberately not a lifecycle table.'
    Write-FixtureFile -Root $fixtureRoot -RelativePath 'docs/current_capability_package.md' -Text 'This is explanatory package context, deliberately not a lifecycle table.'
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

function Add-FixtureSprintProperty {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)]$Value
    )

    $path = Join-Path $Root 'docs/current_sprint.json'
    $record = [IO.File]::ReadAllText($path) | ConvertFrom-Json
    $record.sprint | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
    [IO.File]::WriteAllText($path, ($record | ConvertTo-Json -Depth 10), [Text.UTF8Encoding]::new($false))
}

function Invoke-FixtureValidator {
    param([Parameter(Mandatory = $true)][string]$FixtureRoot)

    $global:LASTEXITCODE = 0
    $output = & $validator -ProjectRoot $FixtureRoot *>&1 | Out-String
    return [pscustomobject]@{ ExitCode = $LASTEXITCODE; Output = $output }
}

function Assert-Accepted {
    param([Parameter(Mandatory = $true)][string]$Name, [Parameter(Mandatory = $true)][string]$FixtureRoot)

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
    if (-not (($result.Output -replace '\s+', ' ').Trim()).Contains(($ExpectedMessage -replace '\s+', ' ').Trim())) {
        throw "$Name did not report the expected conflict '$ExpectedMessage':`n$($result.Output)"
    }
    $script:Passed += 1
    Write-Output "PASS fixture rejection: $Name"
}

try {
    [IO.Directory]::CreateDirectory($tempRoot) | Out-Null

    Assert-Accepted -Name 'complete record with explanatory Markdown' -FixtureRoot (New-Fixture -Name 'complete' -Mode complete)
    Assert-Accepted -Name 'active record with explanatory Markdown' -FixtureRoot (New-Fixture -Name 'active' -Mode active)

    $fixture = New-Fixture -Name 'integer-save-version' -Mode complete
    Assert-Accepted -Name 'integer save version' -FixtureRoot $fixture

    $fixture = New-Fixture -Name 'active-sprint-mismatch' -Mode active
    Replace-FixtureText $fixture 'docs/current_sprint.json' '"active_sprint": "10.75"' '"active_sprint":  "10.76"'
    Assert-Rejected 'active sprint mismatch' $fixture "active_sprint mismatch: active_sprint is '10.76'; sprint.id is '10.75'."

    $fixture = New-Fixture -Name 'unexpected-next-sprint' -Mode complete
    Replace-FixtureText $fixture 'docs/current_sprint.json' '"next_sprint": null' '"next_sprint":  "10.75"'
    Assert-Rejected 'unexpected next sprint' $fixture "next_sprint must remain null until separately authorized; found '10.75'."

    $fixture = New-Fixture -Name 'unsafe-save-version' -Mode complete
    Replace-FixtureText $fixture 'docs/current_sprint.json' '"save_version": 1' '"save_version":  2'
    Assert-Rejected 'unsafe save version' $fixture "sprint.platform.save_version must be exactly integer 1; found '2'."

    foreach ($invalidSaveVersion in @(
        @{ Name = 'string save version'; Value = '"1"' },
        @{ Name = 'fractional save version'; Value = '1.5' },
        @{ Name = 'null save version'; Value = 'null' },
        @{ Name = 'boolean save version'; Value = 'true' }
    )) {
        $fixture = New-Fixture -Name ($invalidSaveVersion.Name -replace ' ', '-') -Mode complete
        Replace-FixtureText $fixture 'docs/current_sprint.json' '"save_version": 1' ('"save_version":  ' + $invalidSaveVersion.Value)
        Assert-Rejected $invalidSaveVersion.Name $fixture 'sprint.platform.save_version must be exactly integer 1;'
    }
    $fixture = New-Fixture -Name 'unsupported-risk-level' -Mode complete
    Replace-FixtureText $fixture 'docs/current_sprint.json' '"risk_level": "routine"' '"risk_level":  "unclassified"'
    Assert-Rejected 'unsupported risk level' $fixture "sprint.risk_level must be 'critical' or 'routine'; found 'unclassified'."

    $fixture = New-Fixture -Name 'ephemeral-candidate-field' -Mode complete
    Add-FixtureSprintProperty -Root $fixture -Name 'candidate_state' -Value 'prepared'
    Assert-Rejected 'ephemeral candidate state' $fixture "sprint declares removed ephemeral lifecycle field: candidate_state."

    $fixture = New-Fixture -Name 'forbidden-yaml-reference' -Mode complete
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
