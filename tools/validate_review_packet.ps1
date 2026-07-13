[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PacketPath,
    [string]$RepoRoot,
    [switch]$Legacy
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Fail([string]$Message) { throw "Review packet validation failed: $Message" }
function Get-ByteHash([byte[]]$Bytes) { ([Security.Cryptography.SHA256]::Create().ComputeHash($Bytes) | ForEach-Object ToString x2) -join '' }
function Get-EntryBytes($Entry) { $buffer = [IO.MemoryStream]::new(); $stream = $Entry.Open(); try { $stream.CopyTo($buffer); return $buffer.ToArray() } finally { $stream.Dispose(); $buffer.Dispose() } }
function Get-EntryText($Entry) { [Text.Encoding]::UTF8.GetString((Get-EntryBytes $Entry)) }
function ConvertTo-CanonicalValue($Value) {
    if ($null -eq $Value) { return $null }
    if ($Value -is [string] -or $Value -is [ValueType]) { return $Value }
    if ($Value -is [System.Collections.IDictionary]) { $result = [ordered]@{}; foreach ($key in @($Value.Keys | Sort-Object)) { $result[[string]$key] = ConvertTo-CanonicalValue $Value[$key] }; return ,$result }
    if ($Value -is [pscustomobject]) { $result = [ordered]@{}; foreach ($name in @($Value.PSObject.Properties | ForEach-Object Name | Sort-Object)) { $result[$name] = ConvertTo-CanonicalValue $Value.$name }; return ,$result }
    if ($Value -is [System.Collections.IEnumerable]) { $result = [System.Collections.Generic.List[object]]::new(); foreach ($item in $Value) { $result.Add((ConvertTo-CanonicalValue $item)) }; return ,$result.ToArray() }
    Fail "unsupported canonical JSON type $($Value.GetType().FullName)"
}
function Get-CanonicalJson($Value) { (ConvertTo-CanonicalValue $Value | ConvertTo-Json -Depth 100 -Compress) }
function Test-SafeArchivePath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path) -or $Path.Contains('//') -or $Path.EndsWith('/') -or $Path -match '(^|/)(\.|\.\.)(/|$)|^[A-Za-z]:|^/|\\') { Fail "unsafe path: $Path" }
}
function Test-SubstantiveText([string]$Text, [string]$Description) {
    $normalized = (($Text -replace '\s+', ' ').Trim()).ToLowerInvariant()
    if ($normalized.Length -lt 3 -or $normalized -in @('todo', 'tbd', 'n/a', 'none', 'placeholder', 'evidence', 'pass', 'x')) { Fail "non-substantive $Description" }
}
function Get-RequiredText($ByName, [string]$Path, [string]$Description) {
    if (-not $ByName.ContainsKey($Path)) { Fail "missing $Description" }
    $text = Get-EntryText $ByName[$Path]
    Test-SubstantiveText $text $Description
    return $text
}
function Get-ExactEvidenceField([string]$Text, [string]$Label) {
    $found = [regex]::Matches($Text, "(?mi)^\s*$([regex]::Escape($Label)):\s*([^\r\n]+)\s*$")
    if ($found.Count -ne 1) { Fail "git evidence $Label field count" }
    return $found[0].Groups[1].Value.Trim()
}
function Test-PhaseHeadingSection([string]$Text, [string]$Heading, [string]$Description) {
    if (([regex]::Matches($Text, "(?m)^$([regex]::Escape($Heading))\s*$")).Count -ne 1) { Fail "phase heading $Heading" }
    $body = [regex]::Match($Text, "(?ms)^$([regex]::Escape($Heading))\s*$\s*(.*?)(?=^## |\z)").Groups[1].Value
    Test-SubstantiveText $body $Description
    if ((($body -replace '\s+', ' ').Trim()).Length -lt 40) { Fail "shallow $Description" }
}
function Test-PhaseSynthesis([string]$Text, [string]$Role) {
    switch ($Role) {
        'capability_dependency_map' {
            Test-PhaseHeadingSection $Text '## Capability Dependencies' 'phase dependency map'
            if (([regex]::Matches($Text, '(?m)^\|\s*Capability\s*\|\s*Dependencies\s*\|\s*Decision Relevance\s*\|\s*$')).Count -ne 1) { Fail 'phase dependency table heading' }
            $rows = @([regex]::Matches($Text, '(?m)^\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*$') | Where-Object { $_.Groups[1].Value.Trim() -ne 'Capability' -and $_.Groups[1].Value.Trim() -notmatch '^-+$' })
            if ($rows.Count -eq 0) { Fail 'phase dependency row' }
            foreach ($row in $rows) { foreach ($index in 1..3) { if ($row.Groups[$index].Value.Trim().Length -lt 12) { Fail 'shallow phase dependency row' } } }
        }
        'architecture_decision_index' {
            Test-PhaseHeadingSection $Text '## ADR Index' 'phase ADR index'
            if (([regex]::Matches($Text, '(?m)^\|\s*ADR Identifier\s*\|\s*Status\s*\|\s*Decision Relevance\s*\|\s*$')).Count -ne 1) { Fail 'phase ADR table heading' }
            $rows = @([regex]::Matches($Text, '(?m)^\|\s*(ADR-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*$'))
            if ($rows.Count -eq 0) { Fail 'phase ADR row' }
            foreach ($row in $rows) { if ($row.Groups[2].Value.Trim() -notmatch '(?i)^(accepted|proposed|deferred|superseded)$' -or $row.Groups[3].Value.Trim().Length -lt 12) { Fail 'invalid phase ADR row' } }
        }
        'phase_decision_context' {
            foreach ($heading in @('## Unresolved Phase Questions', '## Alternatives', '## Decision Context')) { Test-PhaseHeadingSection $Text $heading 'phase decision context' }
        }
    }
}

$requiredRoles = @{
    'package-review' = @('packet_manifest', 'package_record', 'sprint_record', 'verification_evidence', 'git_evidence')
    'post-package-architecture-review' = @('packet_manifest', 'package_record', 'sprint_record', 'verification_evidence', 'git_evidence', 'owner_review_brief', 'architecture_snapshot', 'simulation_capability_map', 'simulation_scenarios', 'authoritative_architecture_source', 'authoritative_simulation_source', 'authoritative_simulation_principles_source', 'authoritative_roadmap_source', 'authoritative_decision_source')
    'phase-architecture-review' = @('packet_manifest', 'package_record', 'sprint_record', 'verification_evidence', 'git_evidence', 'owner_review_brief', 'architecture_snapshot', 'simulation_capability_map', 'simulation_scenarios', 'authoritative_architecture_source', 'authoritative_simulation_source', 'authoritative_simulation_principles_source', 'authoritative_roadmap_source', 'authoritative_decision_source', 'capability_dependency_map', 'architecture_decision_index', 'phase_decision_context')
}
$roleKinds = @{
    packet_manifest = 'manifest'; package_record = 'evidence'; sprint_record = 'evidence'; verification_evidence = 'evidence'; git_evidence = 'evidence'; supporting_evidence = 'evidence'
    owner_review_brief = 'packet_synthesis'; architecture_snapshot = 'packet_synthesis'; simulation_capability_map = 'packet_synthesis'; simulation_scenarios = 'packet_synthesis'; capability_dependency_map = 'packet_synthesis'; architecture_decision_index = 'packet_synthesis'; phase_decision_context = 'packet_synthesis'
    authoritative_architecture_source = 'authoritative_source'; authoritative_simulation_source = 'authoritative_source'; authoritative_simulation_principles_source = 'authoritative_source'; authoritative_roadmap_source = 'authoritative_source'; authoritative_decision_source = 'authoritative_source'
    implementation_source = 'implementation'; test_source = 'test'
}
$commonRoles = @('implementation_source', 'test_source', 'supporting_evidence')
$authorityPaths = @{ authoritative_architecture_source='docs/architecture.md'; authoritative_simulation_source='docs/simulation_model.md'; authoritative_simulation_principles_source='docs/simulation_principles.md'; authoritative_roadmap_source='docs/roadmap.md'; authoritative_decision_source='docs/decisions.md' }
$allowedRoles = @{
    'package-review' = @($requiredRoles['package-review'] + $commonRoles)
    'post-package-architecture-review' = @($requiredRoles['post-package-architecture-review'] + $commonRoles)
    'phase-architecture-review' = @($requiredRoles['phase-architecture-review'] + $commonRoles)
}

$archive = [IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $PacketPath))
try {
    $byName = @{}
    foreach ($entry in @($archive.Entries)) {
        if ($entry.FullName.EndsWith('/')) { Fail "directory entry: $($entry.FullName)" }
        Test-SafeArchivePath $entry.FullName
        if ($byName.ContainsKey($entry.FullName)) { Fail 'duplicate archive entry' }
        $byName[$entry.FullName] = $entry
    }
    if ($Legacy) { Write-Output 'PASS: readable safe legacy archive'; exit 0 }
    if (-not $byName.ContainsKey('review_packet_manifest.json')) { Fail 'manifest absent' }

    try { $manifest = Get-EntryText $byName['review_packet_manifest.json'] | ConvertFrom-Json } catch { Fail "manifest JSON: $($_.Exception.Message)" }
    if ($manifest.schema_version -ne '1.0.0') { Fail 'unsupported schema' }
    if ($manifest.legacy -ne $false) { Fail 'profiled packet cannot be legacy' }
    if (-not $requiredRoles.ContainsKey($manifest.profile)) { Fail 'unknown profile' }
    if ($manifest.reviewed_head -notmatch '^[0-9a-f]{40}$') { Fail 'invalid reviewed head' }
    if (-not $manifest.PSObject.Properties['creation_source_state']) { Fail 'creation source state absent' }
    foreach ($field in @('branch', 'head', 'status')) { if ([string]::IsNullOrWhiteSpace([string]$manifest.creation_source_state.$field)) { Fail "creation source state $field absent" } }
    if ($manifest.creation_source_state.head -notmatch '^[0-9a-f]{40}$' -or $manifest.creation_source_state.head -ne $manifest.reviewed_head) { Fail 'reviewed head mismatch' }
    foreach ($field in @('packet_id', 'review_identity', 'verification_evidence_path', 'git_evidence_path')) { if ([string]::IsNullOrWhiteSpace([string]$manifest.$field)) { Fail "required manifest field $field absent" } }

    $members = @($manifest.members)
    if ($members.Count -eq 0) { Fail 'manifest members absent' }
    $declaredPaths = @()
    foreach ($member in $members) {
        foreach ($field in @('path', 'role', 'artifact_kind', 'sha256')) { if ([string]::IsNullOrWhiteSpace([string]$member.$field)) { Fail "member field $field absent" } }
        Test-SafeArchivePath $member.path
        if ($member.role -notin $allowedRoles[$manifest.profile]) { Fail "role outside profile $($member.role)" }
        if (-not $roleKinds.ContainsKey($member.role) -or $member.artifact_kind -ne $roleKinds[$member.role]) { Fail "invalid role/artifact-kind $($member.role)" }
        if ($member.sha256 -notmatch '^[0-9a-f]{64}$') { Fail "invalid hash $($member.path)" }
        if ($declaredPaths -contains $member.path) { Fail "duplicate manifest path $($member.path)" }
        $declaredPaths += $member.path
        if ($member.artifact_kind -eq 'packet_synthesis') {
            if (-not $member.PSObject.Properties['sources'] -or $null -eq $member.sources) { Fail "source pins $($member.path)" }
            [object[]]$pins = $member.sources
            if ($pins.Length -eq 0) { Fail "source pins $($member.path)" }
            foreach ($pin in $pins) { if ($null -eq $pin -or -not $pin.PSObject.Properties['repository_path'] -or -not $pin.PSObject.Properties['sha256'] -or [string]::IsNullOrWhiteSpace([string]$pin.repository_path) -or $pin.repository_path.Contains('//') -or $pin.repository_path -match '(^|/)(\.|\.\.)(/|$)|^[A-Za-z]:|^/|\\' -or $pin.sha256 -notmatch '^[0-9a-f]{64}$') { Fail "invalid source pin $($member.path)" } }
        }
        if ($authorityPaths.ContainsKey($member.role) -and $member.repository_path -ne $authorityPaths[$member.role]) { Fail "authoritative repository path $($member.role)" }
    }
    if ($declaredPaths.Count -ne $byName.Count -or (($declaredPaths | Sort-Object) -join '|') -ne (($byName.Keys | Sort-Object) -join '|')) { Fail 'manifest membership mismatch' }
    foreach ($role in $requiredRoles[$manifest.profile]) { $count=@($members | Where-Object role -eq $role).Count; if ($count -ne 1) { Fail "required role count $role" } }
    $manifestMember = @($members | Where-Object path -eq 'review_packet_manifest.json')
    if ($manifestMember.Count -ne 1 -or $manifestMember[0].role -ne 'packet_manifest') { Fail 'invalid manifest member' }
    $savedSelfHash = $manifestMember[0].sha256; $manifestMember[0].sha256 = 'SELF'; $expectedSelfHash = Get-ByteHash ([Text.Encoding]::UTF8.GetBytes((Get-CanonicalJson $manifest))); $manifestMember[0].sha256 = $savedSelfHash
    if ($savedSelfHash -ne $expectedSelfHash) { Fail 'manifest self hash' }

    foreach ($member in $members) {
        if ($member.path -ne 'review_packet_manifest.json' -and (Get-ByteHash (Get-EntryBytes $byName[$member.path])) -ne $member.sha256) { Fail "hash $($member.path)" }
    }
    foreach ($role in @($requiredRoles[$manifest.profile] | Where-Object { $_ -ne 'packet_manifest' })) {
        $member = @($members | Where-Object role -eq $role)[0]
        [void](Get-RequiredText $byName $member.path $role)
    }
    $verificationMember = @($members | Where-Object role -eq 'verification_evidence')[0]
    $gitMember = @($members | Where-Object role -eq 'git_evidence')[0]
    if ($manifest.verification_evidence_path -ne $verificationMember.path -or $manifest.git_evidence_path -ne $gitMember.path) { Fail 'evidence path mismatch' }
    $gitText = Get-RequiredText $byName $gitMember.path 'git evidence'
    $gitBranch = Get-ExactEvidenceField $gitText 'branch'; $gitHead = Get-ExactEvidenceField $gitText 'HEAD'
    if ($gitHead -ne $manifest.reviewed_head -or $gitBranch -ne $manifest.creation_source_state.branch) { Fail 'git evidence identity mismatch' }

    $briefs = @($members | Where-Object role -eq 'owner_review_brief')
    if ($briefs.Count -eq 1) {
        $briefText = Get-EntryText $byName[$briefs[0].path]
        foreach ($heading in @('## Review Type', '## Review Purpose', '## Authoritative Repository State', '## Plain-Language Outcome', '## Decision Card', '## Decision Requested', '## Owner Decision Request')) { if (([regex]::Matches($briefText, "(?m)^$([regex]::Escape($heading))\s*$")).Count -ne 1) { Fail "brief heading $heading" };$section=[regex]::Match($briefText,"(?ms)^$([regex]::Escape($heading))\s*$\s*(.*?)(?=^## |\z)");Test-SubstantiveText $section.Groups[1].Value "brief section $heading" }
        foreach($row in @('Recommended capability','Why now','Player or project value','Technical risk','Persistence impact','New ADR','Expected scope','Major alternatives deferred')){if($briefText-notmatch("(?m)^\|\s*"+[regex]::Escape($row)+"\s*\|\s*[^|\s].*\|\s*$")){Fail "decision card row $row"}}
        $request = [regex]::Match($briefText, '(?ms)^## Owner Decision Request\s*$\s*(.*?)(?=^## |\z)')
        if (-not $request.Success) { Fail 'decision request absent' }
        Test-SubstantiveText $request.Groups[1].Value 'decision request'
        if ($request.Groups[1].Value -notmatch '(?i)\b(accept|reject|defer|request a deeper review)\b') { Fail 'decision request action' }
        if ($briefText.Length -lt 500 -or $briefText -notmatch '(?m)^1\. ' -or $briefText -notmatch '(?m)^5\. ') { Fail 'insufficient plain-language outcome' }
        foreach($row in @('Recommended capability','Why now','Player or project value','Technical risk','Persistence impact','New ADR','Expected scope','Major alternatives deferred')){$value=[regex]::Match($briefText,"(?m)^\|\s*"+[regex]::Escape($row)+"\s*\|\s*([^|]+)\|").Groups[1].Value.Trim();switch($row){'Technical risk'{if($value-notmatch'(?i)^(low|medium|high)$'){Fail "invalid decision card row $row"}}'Persistence impact'{if($value-notmatch'(?i)^(none|compatible extension|compatibility change)$'){Fail "invalid decision card row $row"}}'New ADR'{if($value-notmatch'(?i)^(required|not required)$'){Fail "invalid decision card row $row"}}'Expected scope'{if($value-notmatch'(?i)^(health check|one bounded sprint|short sequence|deep design work)$'){Fail "invalid decision card row $row"}}default{if($value.Length-lt15-or$value-match'(?i)^(accept package|safe reviews|gameplay|banana)$'){Fail "shallow decision card row $row"}}}}
    }
    foreach($role in @('architecture_snapshot','simulation_capability_map')){ $item=@($members|Where-Object role -eq $role);if($item.Count-eq1){$text=Get-EntryText $byName[$item[0].path];if($text.Length-lt 300-or$text-notmatch'(?i)authoritative (repository )?sources'){Fail "shallow $role"}}}
    foreach($role in @('capability_dependency_map','architecture_decision_index','phase_decision_context')) { $item=@($members|Where-Object role -eq $role);if($item.Count-eq1){Test-PhaseSynthesis (Get-EntryText $byName[$item[0].path]) $role} }
    $scenarioMembers = @($members | Where-Object role -eq 'simulation_scenarios')
    if ($scenarioMembers.Count -eq 1) {
        $blocks = @([regex]::Split((Get-EntryText $byName[$scenarioMembers[0].path]), '(?m)^## Scenario\s*$') | Select-Object -Skip 1)
        if ($blocks.Count -eq 0) { Fail 'scenario absent' }
        if ($manifest.profile -eq 'phase-architecture-review' -and $blocks.Count -lt 2) { Fail 'phase scenario count' }
        foreach ($block in $blocks) { foreach ($heading in @('### Initial State', '### Trigger', '### Authoritative State Transitions', '### Causal History', '### Player-Facing Projection', '### Decision Relevance')) { if ($block -notmatch [regex]::Escape($heading)) { Fail "scenario heading $heading" };$body=[regex]::Match($block,"(?ms)"+[regex]::Escape($heading)+"\s*(.*?)(?=^### |\z)").Groups[1].Value;if($body.Trim().Length-lt20){Fail "shallow scenario section $heading"} } }
    }
    if ($RepoRoot) {
        $resolvedRoot = (Resolve-Path -LiteralPath $RepoRoot).Path; $rootPrefix = $resolvedRoot.TrimEnd('\') + '\'
        $candidateHead = (& git -C $resolvedRoot rev-parse HEAD).Trim(); if ($LASTEXITCODE -ne 0 -or $candidateHead -ne $manifest.reviewed_head) { Fail 'candidate repository HEAD mismatch' }
        $candidateBranch = (& git -C $resolvedRoot branch --show-current).Trim(); if ($LASTEXITCODE -ne 0 -or $candidateBranch -ne $manifest.creation_source_state.branch) { Fail 'candidate repository branch mismatch' }
        foreach ($member in @($members | Where-Object artifact_kind -eq 'packet_synthesis')) { foreach ($pin in @($member.sources)) { $source = Join-Path $resolvedRoot $pin.repository_path; if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { Fail "source missing $($pin.repository_path)" }; $resolvedSource = (Resolve-Path -LiteralPath $source).Path; if (-not $resolvedSource.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase) -or (Get-ByteHash ([IO.File]::ReadAllBytes($resolvedSource))) -ne $pin.sha256) { Fail "stale source $($pin.repository_path)" } } }
        $profileAuthorities=@($authorityPaths.Keys|Where-Object{$requiredRoles[$manifest.profile] -contains $_})
        foreach($role in $profileAuthorities){$member=@($members|Where-Object role -eq $role)[0];$source=Join-Path $resolvedRoot $authorityPaths[$role];if((Get-ByteHash (Get-EntryBytes $byName[$member.path]))-ne(Get-ByteHash ([IO.File]::ReadAllBytes($source)))){Fail "authoritative member mismatch $role"};foreach($synthesis in @($members|Where-Object artifact_kind -eq 'packet_synthesis')){$pinPaths=@($synthesis.sources.repository_path);if(@($pinPaths|Where-Object{$_ -eq $authorityPaths[$role]}).Count-ne 1){Fail "synthesis authority pin $($authorityPaths[$role])"}}}
        foreach($synthesis in @($members|Where-Object artifact_kind -eq 'packet_synthesis')){foreach($pin in @($synthesis.sources)){if($pin.repository_path -notin @($profileAuthorities|ForEach-Object{$authorityPaths[$_]})){Fail "unbundled synthesis pin $($pin.repository_path)"}}}
    }
    Write-Output "PASS: $($manifest.profile)"
}
finally { $archive.Dispose() }
