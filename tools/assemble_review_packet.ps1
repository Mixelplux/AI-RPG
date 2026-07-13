[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$DefinitionPath,
    [Parameter(Mandatory = $true)][string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-ByteHash([byte[]]$Bytes) {
    ([Security.Cryptography.SHA256]::Create().ComputeHash($Bytes) | ForEach-Object ToString x2) -join ''
}

function ConvertTo-CanonicalValue($Value) {
    if ($null -eq $Value) { return $null }
    if ($Value -is [string] -or $Value -is [ValueType]) { return $Value }
    if ($Value -is [System.Collections.IDictionary]) {
        $result = [ordered]@{}
        foreach ($key in @($Value.Keys | Sort-Object)) {
            $result[[string]$key] = ConvertTo-CanonicalValue $Value[$key]
        }
        return ,$result
    }
    if ($Value -is [pscustomobject]) {
        $result = [ordered]@{}
        foreach ($name in @($Value.PSObject.Properties | ForEach-Object Name | Sort-Object)) {
            $result[$name] = ConvertTo-CanonicalValue $Value.$name
        }
        return ,$result
    }
    if ($Value -is [System.Collections.IEnumerable]) {
        $result = [System.Collections.Generic.List[object]]::new()
        foreach ($item in $Value) { $result.Add((ConvertTo-CanonicalValue $item)) }
        return ,$result.ToArray()
    }
    throw "Unsupported canonical JSON value type: $($Value.GetType().FullName)"
}

function Get-CanonicalJson($Value) {
    (ConvertTo-CanonicalValue $Value | ConvertTo-Json -Depth 100 -Compress)
}

function Test-SafeArchivePath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path) -or $Path.Contains('//') -or $Path.EndsWith('/') -or $Path -match '(^|/)(\.|\.\.)(/|$)|^[A-Za-z]:|^/|\\') {
        throw "Unsafe archive path $Path"
    }
}

$definition = Get-Content -Raw $DefinitionPath | ConvertFrom-Json
if ($definition.profile -notin @('package-review', 'post-package-architecture-review', 'phase-architecture-review')) {
    throw 'Unsupported profile'
}

$root = (Resolve-Path (Split-Path -Parent $DefinitionPath)).Path
$rootPrefix = $root.TrimEnd('\') + '\'
$members = @()
foreach ($member in @($definition.members)) {
    foreach ($field in @('source_path', 'path', 'role', 'artifact_kind')) {
        if ([string]::IsNullOrWhiteSpace([string]$member.$field)) { throw "Member field $field is required" }
    }
    Test-SafeArchivePath $member.path
    $candidate = Join-Path $root $member.source_path
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { throw "Missing input $($member.source_path)" }
    $sourceFile = (Resolve-Path -LiteralPath $candidate).Path
    if (-not $sourceFile.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Input escapes definition root: $($member.source_path)"
    }
    $pins = if ($member.PSObject.Properties['sources']) { @($member.sources) } else { @() }
    $members += [pscustomobject]@{
        path = $member.path
        role = $member.role
        artifact_kind = $member.artifact_kind
        sha256 = Get-ByteHash ([IO.File]::ReadAllBytes($sourceFile))
        sources = $pins
        repository_path = if ($member.PSObject.Properties['repository_path']) { $member.repository_path } else { $null }
    }
}

$manifest = [ordered]@{
    schema_version = '1.0.0'
    profile = $definition.profile
    packet_id = $definition.packet_id
    review_identity = $definition.review_identity
    reviewed_head = $definition.reviewed_head
    creation_source_state = $definition.creation_source_state
    members = @([pscustomobject]@{ path = 'review_packet_manifest.json'; role = 'packet_manifest'; artifact_kind = 'manifest'; sha256 = 'SELF'; sources = @() }) + $members
    verification_evidence_path = $definition.verification_evidence_path
    git_evidence_path = $definition.git_evidence_path
    legacy = $false
}
$manifest = ($manifest | ConvertTo-Json -Depth 100) | ConvertFrom-Json
$manifest.members[0].sha256 = Get-ByteHash ([Text.Encoding]::UTF8.GetBytes((Get-CanonicalJson $manifest)))
$manifestBytes = [Text.Encoding]::UTF8.GetBytes(($manifest | ConvertTo-Json -Depth 100))

if (Test-Path -LiteralPath $OutputPath) { Remove-Item -LiteralPath $OutputPath -Force }
$output = $null
$zip = $null
try {
    $output = [IO.File]::Open($OutputPath, [IO.FileMode]::CreateNew)
    $zip = [IO.Compression.ZipArchive]::new($output, [IO.Compression.ZipArchiveMode]::Create, $true)
    $entries = @([pscustomobject]@{ path = 'review_packet_manifest.json'; bytes = $manifestBytes })
    foreach ($member in @($definition.members)) {
        $entries += [pscustomobject]@{ path = $member.path; bytes = [IO.File]::ReadAllBytes((Join-Path $root $member.source_path)) }
    }
    $seen = @{}
    foreach ($entry in $entries) {
        Test-SafeArchivePath $entry.path
        if ($seen[$entry.path]) { throw "Duplicate archive path $($entry.path)" }
        $seen[$entry.path] = $true
        $zipEntry = $zip.CreateEntry($entry.path)
        $stream = $zipEntry.Open()
        try { $stream.Write($entry.bytes, 0, $entry.bytes.Length) } finally { $stream.Dispose() }
    }
}
finally {
    if ($zip) { $zip.Dispose() }
    if ($output) { $output.Dispose() }
}
