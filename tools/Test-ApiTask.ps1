#requires -Version 7.0
# Offline launcher integration: a synthetic DPAPI credential, never the real store.
[CmdletBinding()]
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repository = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$artifact = Join-Path $repository '.artifacts\api-environment-tests'
$storeRoot = Join-Path ([IO.Path]::GetTempPath()) ('api-readiness-test-' + [Guid]::NewGuid().ToString('N'))
$store = Join-Path $storeRoot 'AI RPG\NarratorSmoke'
$path = Join-Path $store 'credential.dpapi'
$dummy = 'offline-placeholder-for-child-test'
$secure = $null
$beforeKey = [Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'Process')
$beforeProxy = [Environment]::GetEnvironmentVariable('HTTPS_PROXY', 'Process')
$beforeCache = [Environment]::GetEnvironmentVariable('TIKTOKEN_CACHE_DIR', 'Process')
$passed = 0
function Assert-Api([bool]$Condition, [string]$Name) {
    if (-not $Condition) { throw $Name }
    $script:passed++
    Write-Output ('PASS: ' + $Name)
}
try {
    $null = [IO.Directory]::CreateDirectory($artifact)
    $null = [IO.Directory]::CreateDirectory($store)
    # Mock only the profile lookup in a separate PowerShell process. No registry writes.
    $wrapper = Join-Path $artifact 'wrapper.ps1'
    @'
param([string]$Launcher,[string]$ProfileDirectory,[string]$Cache,[string]$Mode)
function Get-ItemProperty { param($LiteralPath,$Name) return @{ 'Local AppData' = $ProfileDirectory } }
$env:TIKTOKEN_CACHE_DIR=$Cache
if ($Mode -eq 'proxy') { $env:HTTPS_PROXY='http://127.0.0.1:9' }
if ($Mode -eq 'task') { & $Launcher -TaskScript '.artifacts/api-environment-tests/child.py'; exit $LASTEXITCODE }
if ($Mode -eq 'escape') { & $Launcher -TaskScript '../outside.py'; exit $LASTEXITCODE }
& $Launcher
exit $LASTEXITCODE
'@ | Set-Content -LiteralPath $wrapper -Encoding utf8
    @'
import os, sys
assert os.environ['OPENAI_API_KEY'] == 'offline-placeholder-for-child-test'
# Intentionally hostile dummy output verifies that none is forwarded.
print(os.environ['OPENAI_API_KEY'])
print('private stderr fixture', file=sys.stderr)
'@ | Set-Content -LiteralPath (Join-Path $artifact 'child.py') -Encoding utf8
    $profileLocal = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' -Name 'Local AppData').'Local AppData'
    $cache = Join-Path ([Environment]::ExpandEnvironmentVariables($profileLocal)) 'Temp\data-gym-cache'
    $launcher = Join-Path $PSScriptRoot 'Invoke-ApiTask.ps1'
    function Run-ApiFixture([string]$Mode='check',[string]$CacheDirectory=$cache) {
        $text = @(& (Join-Path $PSHOME 'pwsh.exe') -NoProfile -File $wrapper -Launcher $launcher -ProfileDirectory $storeRoot -Cache $CacheDirectory -Mode $Mode 2>&1) -join "`n"
        return [pscustomobject]@{ Code=$LASTEXITCODE; Text=$text }
    }
    $result=Run-ApiFixture
    Assert-Api ($result.Code -eq 1 -and $result.Text.Contains('stage=store_missing')) 'Missing store fails before child execution'
    [IO.File]::WriteAllText($path,'deliberately-invalid-test-ciphertext')
    $result=Run-ApiFixture
    Assert-Api ($result.Code -eq 1 -and $result.Text.Contains('stage=dpapi_decrypt') -and -not $result.Text.Contains('deliberately-invalid')) 'DPAPI failure is distinct and contents are suppressed'
    $secure=ConvertTo-SecureString $dummy -AsPlainText -Force
    [IO.File]::WriteAllText($path,(ConvertFrom-SecureString $secure))
    $result=Run-ApiFixture
    Assert-Api ($result.Code -eq 0 -and $result.Text.Contains('API_LOCAL_READY') -and -not $result.Text.Contains($dummy)) 'Synthetic credential reaches offline checker with safe diagnostics'
    $result=Run-ApiFixture 'proxy'
    Assert-Api ($result.Code -eq 1 -and $result.Text.Contains('proxy_configuration_blocked')) 'Known discard proxy blocks without bypassing it'
    $missingCache=Join-Path $storeRoot 'missing-tokenizer-cache'
    $result=Run-ApiFixture 'check' $missingCache
    Assert-Api ($result.Code -eq 1 -and $result.Text.Contains('dependency_or_tokenizer_unavailable') -and -not (Test-Path -LiteralPath $missingCache)) 'Cache miss fails without downloading or creating files'
    $result=Run-ApiFixture 'task'
    Assert-Api ($result.Code -eq 0 -and $result.Text.Contains('API_TASK_EXIT=0') -and -not $result.Text.Contains($dummy) -and -not $result.Text.Contains('private stderr fixture')) 'Optional offline child inherits credential; stdout and stderr stay suppressed'
    $result=Run-ApiFixture 'escape'
    Assert-Api ($result.Code -eq 1 -and $result.Text.Contains('stage=task_path')) 'Task path escape is rejected'
    Assert-Api ([Environment]::GetEnvironmentVariable('OPENAI_API_KEY','Process') -ceq $beforeKey) 'Parent credential environment unchanged'
    Assert-Api ([Environment]::GetEnvironmentVariable('HTTPS_PROXY','Process') -ceq $beforeProxy) 'Parent proxy environment unchanged'
    Assert-Api ([Environment]::GetEnvironmentVariable('TIKTOKEN_CACHE_DIR','Process') -ceq $beforeCache) 'Parent tokenizer environment unchanged'
}
finally {
    if ($null -ne $secure) { $secure.Dispose() }
    # Only the exact unique fixture directory under this process's temp root.
    $resolved = [IO.Path]::GetFullPath($storeRoot)
    $tempRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\') + '\'
    if (-not $resolved.StartsWith($tempRoot,[StringComparison]::OrdinalIgnoreCase) -or
        [IO.Path]::GetFileName($resolved) -notlike 'api-readiness-test-*') { throw 'Unsafe fixture cleanup path' }
    if ([IO.Directory]::Exists($resolved)) { [IO.Directory]::Delete($resolved,$true) }
    $dummy=$null
    $beforeKey=$null
    $beforeProxy=$null
    $beforeCache=$null
}
Write-Output ('API_TOOLING_TESTS_PASS checks=' + $passed + ' requests=0 generations=0')
