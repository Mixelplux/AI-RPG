[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9]+(?:-[a-z0-9]+)*$')]
    [string]$PackageSlug,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{7,40}$')]
    [string]$AcceptedShortHead,

    [Parameter()]
    [string]$HandoffsPath,

    [Parameter()]
    [string[]]$TemporaryAssemblyDirectory = @(),

    [Parameter()]
    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($HandoffsPath)) {
    $HandoffsPath = Join-Path (Split-Path -Parent $PSScriptRoot) "handoffs"
}

function Normalize-Path {
    param([Parameter(Mandatory = $true)][string]$Path)

    return [System.IO.Path]::GetFullPath($Path).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
}

function Test-PathWithinDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Directory
    )

    $normalizedPath = Normalize-Path -Path $Path
    $normalizedDirectory = Normalize-Path -Path $Directory
    $directoryPrefix = $normalizedDirectory + [System.IO.Path]::DirectorySeparatorChar
    return $normalizedPath.StartsWith(
        $directoryPrefix,
        [System.StringComparison]::OrdinalIgnoreCase
    )
}

if (-not (Test-Path -LiteralPath $HandoffsPath -PathType Container)) {
    throw "Handoffs directory does not exist: $HandoffsPath"
}

$resolvedHandoffsPath = (Resolve-Path -LiteralPath $HandoffsPath).Path
$acceptedArchiveName = "$PackageSlug-$AcceptedShortHead.zip"
$acceptedArchivePath = Join-Path $resolvedHandoffsPath $acceptedArchiveName

if (-not (Test-Path -LiteralPath $acceptedArchivePath -PathType Leaf)) {
    throw "Accepted archive does not exist: $acceptedArchivePath"
}

$candidatePattern = "^{0}-(?<head>[0-9a-fA-F]{{7,40}})\.zip$" -f [regex]::Escape($PackageSlug)
$packageArchives = @(
    Get-ChildItem -LiteralPath $resolvedHandoffsPath -File |
        Where-Object { $_.Name -match $candidatePattern }
)
$supersededArchives = @(
    $packageArchives |
        Where-Object { $_.Name -cne $acceptedArchiveName } |
        Sort-Object -Property Name
)

$temporaryDirectories = New-Object System.Collections.Generic.List[string]
foreach ($temporaryDirectory in $TemporaryAssemblyDirectory) {
    $candidatePath = if ([System.IO.Path]::IsPathRooted($temporaryDirectory)) {
        $temporaryDirectory
    }
    else {
        Join-Path $resolvedHandoffsPath $temporaryDirectory
    }

    if (-not (Test-Path -LiteralPath $candidatePath -PathType Container)) {
        throw "Explicit temporary assembly directory does not exist: $candidatePath"
    }

    $resolvedTemporaryPath = (Resolve-Path -LiteralPath $candidatePath).Path
    if (-not (Test-PathWithinDirectory -Path $resolvedTemporaryPath -Directory $resolvedHandoffsPath)) {
        throw "Temporary assembly directory must be inside handoffs/: $resolvedTemporaryPath"
    }

    if ((Split-Path -Leaf $resolvedTemporaryPath) -notlike "$PackageSlug-*") {
        throw "Temporary assembly directory must begin with '$PackageSlug-': $resolvedTemporaryPath"
    }

    [void]$temporaryDirectories.Add($resolvedTemporaryPath)
}

Write-Output "Accepted archive retained: $acceptedArchivePath"
foreach ($archive in $supersededArchives) {
    Write-Output "Superseded archive to remove: $($archive.FullName)"
}
foreach ($temporaryDirectory in $temporaryDirectories) {
    Write-Output "Temporary assembly directory to remove: $temporaryDirectory"
}

if ($supersededArchives.Count -eq 0 -and $temporaryDirectories.Count -eq 0) {
    Write-Output "No superseded candidates or explicit temporary assembly directories were found."
}

if (-not $Apply) {
    Write-Output "Dry run only. Re-run with -Apply after reviewing the listed paths."
    exit 0
}

foreach ($archive in $supersededArchives) {
    Remove-Item -LiteralPath $archive.FullName -Force
}
foreach ($temporaryDirectory in $temporaryDirectories) {
    Remove-Item -LiteralPath $temporaryDirectory -Recurse -Force
}

Write-Output "Cleanup complete. Retained accepted archive: $acceptedArchivePath"
