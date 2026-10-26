#requires -Version 7.0
# Readiness is offline by default. Optional tasks require their own owner authority.
[CmdletBinding()]
param(
    [string]$TaskScript,
    [string[]]$TaskArguments = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$secure = $null
$plaintext = $null
$pointer = [IntPtr]::Zero
$info = $null
$child = $null
$stage = 'platform'
$code = 1
try {
    if (-not $IsWindows -or $PSVersionTable.PSVersion.Major -lt 7) { throw 'platform' }
    $repository = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
    $python = Join-Path $repository '.venv\Scripts\python.exe'
    $stage = 'interpreter'
    if (-not [IO.File]::Exists($python)) { throw 'interpreter' }
    $stage = 'profile_lookup'
    # LOCALAPPDATA/TEMP may be sandbox redirected. Match the working F01 bridge.
    $profileLocal = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' -Name 'Local AppData').'Local AppData'
    $local = [IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($profileLocal))
    $store = Join-Path $local 'AI RPG\NarratorSmoke\credential.dpapi'
    $stage = 'store_path'
    if ($store.StartsWith($repository + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'repository store rejected' }
    $ancestor = $store
    while ($ancestor) {
        if ((Test-Path -LiteralPath $ancestor) -and
            ((Get-Item -LiteralPath $ancestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'reparse' }
        $ancestor = Split-Path -Parent $ancestor
    }
    $stage = 'store_missing'
    if (-not [IO.File]::Exists($store)) { throw 'missing' }
    $stage = 'store_read'
    $encrypted = [IO.File]::ReadAllText($store)
    $stage = 'dpapi_decrypt'
    $secure = ConvertTo-SecureString -String $encrypted
    $encrypted = $null
    if ($secure.Length -eq 0) { throw 'empty' }

    function Start-ApiChild([string[]]$PythonArguments) {
        $script:info = [Diagnostics.ProcessStartInfo]::new()
        $info.FileName = $python
        $info.WorkingDirectory = $repository
        $info.UseShellExecute = $false
        $info.CreateNoWindow = $true
        $info.RedirectStandardOutput = $true
        $info.RedirectStandardError = $true
        $info.StandardOutputEncoding = [Text.Encoding]::UTF8
        foreach ($argument in $PythonArguments) { $info.ArgumentList.Add($argument) }
        $info.Environment['PYTHONIOENCODING'] = 'utf-8'
        $info.Environment['PYTHONDONTWRITEBYTECODE'] = '1'
        if (-not $info.Environment['TIKTOKEN_CACHE_DIR']) {
            $info.Environment['TIKTOKEN_CACHE_DIR'] = Join-Path $local 'Temp\data-gym-cache'
        }
        # Never put the key into argv, the caller environment, or a file.
        $info.Environment['OPENAI_API_KEY'] = $plaintext
        $script:child = [Diagnostics.Process]::new()
        $child.StartInfo = $info
        $null = $child.Start()
        $null = $info.Environment.Remove('OPENAI_API_KEY')
        $stdout = $child.StandardOutput.ReadToEndAsync()
        $stderr = $child.StandardError.ReadToEndAsync()
        if (-not $child.WaitForExit(60000)) { $child.Kill($true); throw 'timeout' }
        $result = [pscustomobject]@{ Code = $child.ExitCode; Output = $stdout.GetAwaiter().GetResult() }
        $null = $stderr.GetAwaiter().GetResult()  # exception contents never emitted
        $child.Dispose()
        $script:child = $null
        return $result
    }

    $stage = 'child_launch'
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    $plaintext = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    $pointer = [IntPtr]::Zero
    $check = Start-ApiChild @('-B', '-m', 'tools.api_readiness')
    $stage = 'readiness_protocol'
    $report = ConvertFrom-Json -InputObject $check.Output
    # Emit fixed diagnostics only; never forward raw child stdout/stderr.
    foreach ($item in $report.checks) {
        if ($item.name -notmatch '^(credential|endpoint|proxy|model|tokenizer|client)$' -or
            $item.status -notmatch '^(pass|blocked)$' -or $item.code -notmatch '^[a-z_]+$') { throw 'protocol' }
        Write-Output ('API_CHECK ' + $item.name + '=' + $item.status + ' code=' + $item.code)
    }
    if ($check.Code -ne 0 -or -not $report.ready) { throw 'readiness blocked' }
    Write-Output 'API_LOCAL_READY authentication=unverified permissions=unverified connectivity=unverified requests=0 generations=0'
    $code = 0
    if ($TaskScript) {
        $stage = 'task_path'
        if ([IO.Path]::IsPathRooted($TaskScript)) { throw 'relative task required' }
        $task = [IO.Path]::GetFullPath((Join-Path $repository $TaskScript))
        if (-not $task.StartsWith($repository + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
            [IO.Path]::GetExtension($task) -ne '.py' -or -not [IO.File]::Exists($task)) { throw 'task path' }
        $ancestor = $task
        while ($ancestor -ne $repository) {
            if ((Get-Item -LiteralPath $ancestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'task reparse' }
            $ancestor = Split-Path -Parent $ancestor
        }
        $stage = 'task_execution'
        $result = Start-ApiChild (@('-B', $task) + $TaskArguments)
        $code = $result.Code
        # A reusable launcher must not turn arbitrary task output into a secret log.
        Write-Output ('API_TASK_EXIT=' + $code + ' output=suppressed')
    }
}
catch {
    Write-Output ('API_ENVIRONMENT_BLOCKED stage=' + $stage + ' See docs/api_environment_preflight.md for local corrective steps; no exception contents disclosed.')
    $code = 1
}
finally {
    if ($pointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
    if ($null -ne $secure) { $secure.Dispose() }
    if ($null -ne $info) { $null = $info.Environment.Remove('OPENAI_API_KEY') }
    if ($null -ne $child) {
        try { if (-not $child.HasExited) { $child.Kill($true) } } catch { }
        $child.Dispose()
    }
    $plaintext = $null
    $encrypted = $null
    $check = $null
    $report = $null
    $result = $null
}
exit $code
