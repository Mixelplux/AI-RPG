[CmdletBinding()]
param(
    [Parameter()]
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),

    [Parameter()]
    [switch]$SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$interpreter = Join-Path $root '.venv\Scripts\python.exe'
$validator = Join-Path $root 'tools\validate_project_records.ps1'
$validatorFixtures = Join-Path $root 'tools\test_project_records.ps1'
$liveSmokeEntryPoint = [IO.Path]::GetFullPath((Join-Path $root 'tools\run_openai_responses_live_smoke.py'))
$powerShellExecutable = (Get-Process -Id $PID).Path
$buildRoot = [IO.Path]::GetFullPath((Join-Path $root '.build'))
$runTemp = [IO.Path]::GetFullPath((Join-Path $buildRoot ('offline-verification-' + [guid]::NewGuid().ToString('N'))))
$childEnvironment = @{
    TEMP = $runTemp
    TMP = $runTemp
}

if (-not (Test-Path -LiteralPath $interpreter -PathType Leaf)) {
    Write-Host "FAIL: Official interpreter is unavailable: $interpreter"
    exit 1
}

function ConvertTo-ProcessArgument {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Argument)

    if ($Argument.Length -gt 0 -and $Argument -notmatch '[\s"]') {
        return $Argument
    }

    $builder = New-Object Text.StringBuilder
    [void]$builder.Append('"')
    $backslashCount = 0
    foreach ($character in $Argument.ToCharArray()) {
        if ($character -eq '\') {
            $backslashCount += 1
            continue
        }

        if ($character -eq '"') {
            [void]$builder.Append(('\' * (($backslashCount * 2) + 1)))
            [void]$builder.Append('"')
            $backslashCount = 0
            continue
        }

        if ($backslashCount -gt 0) {
            [void]$builder.Append(('\' * $backslashCount))
            $backslashCount = 0
        }
        [void]$builder.Append($character)
    }

    if ($backslashCount -gt 0) {
        [void]$builder.Append(('\' * ($backslashCount * 2)))
    }
    [void]$builder.Append('"')
    return $builder.ToString()
}

function Format-Command {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]]$Arguments
    )

    $parts = New-Object System.Collections.Generic.List[string]
    $parts.Add((ConvertTo-ProcessArgument -Argument $FilePath))
    foreach ($argument in $Arguments) {
        $parts.Add((ConvertTo-ProcessArgument -Argument $argument))
    }
    return $parts -join ' '
}

function New-CommandDescriptor {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]]$Arguments
    )

    return [pscustomobject]@{
        Name = $Name
        FilePath = $FilePath
        Arguments = $Arguments
        Display = Format-Command -FilePath $FilePath -Arguments $Arguments
    }
}

function Get-OfflineBehavioralTestSelection {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]]$DiscoveredPaths,
        [Parameter(Mandatory = $true)][string]$ForbiddenLiveSmokePath
    )

    $forbiddenPath = [IO.Path]::GetFullPath($ForbiddenLiveSmokePath)
    $selected = New-Object System.Collections.Generic.List[string]
    foreach ($path in $DiscoveredPaths) {
        $fullPath = [IO.Path]::GetFullPath($path)
        if ($fullPath.Equals($forbiddenPath, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Forbidden live-provider smoke entry point entered offline behavioral discovery: $forbiddenPath"
        }
        $selected.Add($fullPath)
    }

    if ($selected.Count -eq 0) {
        throw 'No stable root test_*.py behavioral tests were found.'
    }

    $ordered = $selected.ToArray()
    [Array]::Sort($ordered, [StringComparer]::Ordinal)
    return $ordered
}

function Write-OfflineVerificationSummary {
    param(
        [Parameter(Mandatory = $true)][int]$CommandCount,
        [Parameter(Mandatory = $true)][int]$BehavioralTestCount,
        [Parameter(Mandatory = $true)][bool]$LiveSmokeGuardPassed
    )

    if (-not $LiveSmokeGuardPassed) {
        throw 'The exact live-smoke exclusion guard has not passed; refusing to report offline completion.'
    }

    Write-Host "Offline behavioral verification summary: $CommandCount command(s) passed; $BehavioralTestCount behavioral test script(s); live provider smoke excluded."
}

function Remove-VerificationTempDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$TempPath,
        [Parameter(Mandatory = $true)][string]$AllowedBuildRoot
    )

    $fullTempPath = [IO.Path]::GetFullPath($TempPath)
    $fullBuildRoot = [IO.Path]::GetFullPath($AllowedBuildRoot)
    $expectedPrefix = $fullBuildRoot.TrimEnd('\') + '\'
    if (-not $fullTempPath.StartsWith($expectedPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove unexpected verification temp path: $fullTempPath"
    }
    if (Test-Path -LiteralPath $fullTempPath) {
        Remove-Item -LiteralPath $fullTempPath -Recurse -Force
    }
}

function Set-ChildEnvironmentOverrides {
    param(
        [Parameter(Mandatory = $true)]$StartInfo,
        [Parameter(Mandatory = $true)][hashtable]$Overrides
    )

    $keys = @($Overrides.Keys)
    if ($keys.Count -eq 0) {
        return
    }

    $firstKey = [string]$keys[0]
    $firstValue = [string]$Overrides.Item($firstKey)
    $firstApplied = $false
    try {
        $StartInfo.EnvironmentVariables.set_Item($firstKey, $firstValue)
        $firstApplied = $true
    }
    catch {
        $knownLazyInitializationFailure = $_.Exception.Message -match (
            'null-valued expression|Cannot index into a null array|Item has already been added'
        )
        if (-not $knownLazyInitializationFailure) {
            throw
        }
    }

    if (-not $firstApplied) {
        # Windows PowerShell 5.1 can fail the first legacy collection access
        # while materializing a case-insensitive parent environment that has
        # case-variant keys. The failed access initializes the maintained
        # EnvironmentVariables collection; one bounded retry then succeeds.
        $StartInfo.EnvironmentVariables.set_Item($firstKey, $firstValue)
    }

    foreach ($key in @($keys | Select-Object -Skip 1)) {
        $overrideValue = [string]$Overrides.Item($key)
        $StartInfo.EnvironmentVariables.set_Item([string]$key, $overrideValue)
    }
}

function Invoke-NativeProcess {
    param(
        [Parameter(Mandatory = $true)]$Command,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][hashtable]$Environment
    )

    $startInfo = New-Object Diagnostics.ProcessStartInfo
    $startInfo.FileName = $Command.FilePath
    $startInfo.Arguments = (($Command.Arguments | ForEach-Object {
        ConvertTo-ProcessArgument -Argument $_
    }) -join ' ')
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    Set-ChildEnvironmentOverrides -StartInfo $startInfo -Overrides $Environment

    $process = New-Object Diagnostics.Process
    $process.StartInfo = $startInfo
    try {
        [void]$process.Start()
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        $stdout = $stdoutTask.GetAwaiter().GetResult()
        $stderr = $stderrTask.GetAwaiter().GetResult()
        return [pscustomobject]@{
            Name = $Command.Name
            Display = $Command.Display
            ExitCode = $process.ExitCode
            Stdout = $stdout
            Stderr = $stderr
            Started = $true
        }
    }
    catch {
        return [pscustomobject]@{
            Name = $Command.Name
            Display = $Command.Display
            ExitCode = 1
            Stdout = ''
            Stderr = $_.Exception.ToString()
            Started = $false
        }
    }
    finally {
        $process.Dispose()
    }
}

function Write-ProcessStream {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('STDOUT', 'STDERR')][string]$Label,
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text,
        [Parameter(Mandatory = $true)][string]$CommandName
    )

    if ([string]::IsNullOrEmpty($Text)) {
        return
    }

    Write-Host "${Label}: $CommandName"
    Write-Host -NoNewline $Text
    if (-not $Text.EndsWith("`n")) {
        Write-Host ''
    }
}

function Invoke-VerificationSequence {
    param(
        [Parameter(Mandatory = $true)][object[]]$Commands,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][hashtable]$Environment,
        [Parameter()][switch]$ShowOutput
    )

    $executed = @()
    foreach ($command in $Commands) {
        if ($ShowOutput) {
            Write-Host "RUN: $($command.Name)"
        }
        $result = Invoke-NativeProcess -Command $command -WorkingDirectory $WorkingDirectory -Environment $Environment
        $executed += $result

        if ($ShowOutput) {
            Write-ProcessStream -Label STDOUT -Text $result.Stdout -CommandName $command.Name
            Write-ProcessStream -Label STDERR -Text $result.Stderr -CommandName $command.Name
        }

        if ($result.ExitCode -ne 0) {
            if ($ShowOutput) {
                Write-Host "FAIL: $($command.Name) (exit $($result.ExitCode))"
                Write-Host "COMMAND: $($command.Display)"
            }
            return [pscustomobject]@{
                ExitCode = $result.ExitCode
                FailedCommand = $command.Name
                Executed = $executed
            }
        }

        if ($ShowOutput) {
            $detail = if ([string]::IsNullOrEmpty($result.Stderr)) { '' } else { ' (stderr emitted; exit 0)' }
            Write-Host "PASS: $($command.Name)$detail"
        }
    }

    return [pscustomobject]@{
        ExitCode = 0
        FailedCommand = $null
        Executed = $executed
    }
}

function Assert-SelfTest {
    param(
        [Parameter(Mandatory = $true)][bool]$Condition,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if (-not $Condition) {
        throw "Runner self-test failed: $Name"
    }
    Write-Host "PASS runner fixture: $Name"
}

function Write-SelfTestPython {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Source
    )

    $path = Join-Path $runTemp $Name
    [IO.File]::WriteAllText($path, $Source, [Text.UTF8Encoding]::new($false))
    return $path
}

function Invoke-RunnerSelfTest {
    $stdoutPath = Write-SelfTestPython -Name 'stdout_zero.py' -Source "print('fixture stdout')`n"
    $stderrZeroPath = Write-SelfTestPython -Name 'stderr_zero.py' -Source "import sys`nsys.stderr.write('fixture stderr\\n')`n"
    $stderrFailurePath = Write-SelfTestPython -Name 'stderr_nonzero.py' -Source "import sys`nsys.stderr.write('fixture failure\\n')`nsys.exit(7)`n"
    $tracebackPath = Write-SelfTestPython -Name 'traceback_nonzero.py' -Source "raise RuntimeError('fixture traceback')`n"
    $singleEnvironmentKey = 'CODEX_RUNNER_SINGLE_' + [guid]::NewGuid().ToString('N')
    $multipleEnvironmentKey = 'CODEX_RUNNER_MULTIPLE_' + [guid]::NewGuid().ToString('N')
    $emptyEnvironmentKey = 'CODEX_RUNNER_EMPTY_' + [guid]::NewGuid().ToString('N')
    $singleEnvironmentPath = Write-SelfTestPython -Name 'single_environment.py' -Source "import os,sys`nsys.exit(0 if os.environ.get('$singleEnvironmentKey') == 'child-only' else 12)`n"
    $multipleEnvironmentPath = Write-SelfTestPython -Name 'multiple_environment.py' -Source "import os,sys`nsys.exit(0 if os.environ.get('$multipleEnvironmentKey') == 'multiple' and os.environ.get('$emptyEnvironmentKey') == '' else 13)`n"
    $ordinaryLaterPath = Write-SelfTestPython -Name 'test_zeta.py' -Source "print('ordinary zeta')`n"
    $ordinaryEarlierPath = Write-SelfTestPython -Name 'test_alpha.py' -Source "print('ordinary alpha')`n"

    $stdoutCommand = New-CommandDescriptor -Name 'stdout zero' -FilePath $interpreter -Arguments @($stdoutPath)
    $stderrZeroCommand = New-CommandDescriptor -Name 'stderr zero' -FilePath $interpreter -Arguments @($stderrZeroPath)
    $stderrFailureCommand = New-CommandDescriptor -Name 'stderr nonzero' -FilePath $interpreter -Arguments @($stderrFailurePath)
    $tracebackCommand = New-CommandDescriptor -Name 'traceback nonzero' -FilePath $interpreter -Arguments @($tracebackPath)
    $singleEnvironmentCommand = New-CommandDescriptor -Name 'single child environment override' -FilePath $interpreter -Arguments @($singleEnvironmentPath)
    $multipleEnvironmentCommand = New-CommandDescriptor -Name 'multiple child environment overrides' -FilePath $interpreter -Arguments @($multipleEnvironmentPath)

    $stdoutResult = Invoke-NativeProcess $stdoutCommand $root @{}
    Assert-SelfTest ($stdoutResult.ExitCode -eq 0 -and $stdoutResult.Stdout -match 'fixture stdout' -and [string]::IsNullOrEmpty($stdoutResult.Stderr)) 'stdout with exit zero'

    $stderrZeroResult = Invoke-NativeProcess $stderrZeroCommand $root $childEnvironment
    Assert-SelfTest ($stderrZeroResult.ExitCode -eq 0 -and $stderrZeroResult.Stderr -match 'fixture stderr') 'stderr with exit zero remains successful'

    $stderrFailureResult = Invoke-NativeProcess $stderrFailureCommand $root $childEnvironment
    Assert-SelfTest ($stderrFailureResult.ExitCode -eq 7 -and $stderrFailureResult.Stderr -match 'fixture failure') 'stderr with nonzero preserves exit code'

    $tracebackResult = Invoke-NativeProcess $tracebackCommand $root $childEnvironment
    Assert-SelfTest ($tracebackResult.ExitCode -ne 0 -and $tracebackResult.Stderr -match 'Traceback' -and $tracebackResult.Stderr -match 'fixture traceback') 'Python traceback remains complete and nonzero'

    $parentTempBefore = $env:TEMP
    $parentTmpBefore = $env:TMP
    $parentHadSingleBefore = Test-Path -LiteralPath ("Env:\{0}" -f $singleEnvironmentKey)
    $parentHadMultipleBefore = Test-Path -LiteralPath ("Env:\{0}" -f $multipleEnvironmentKey)
    $parentHadEmptyBefore = Test-Path -LiteralPath ("Env:\{0}" -f $emptyEnvironmentKey)

    $singleEnvironment = @{
        TEMP = $runTemp
        TMP = $runTemp
    }
    $singleEnvironment.set_Item($singleEnvironmentKey, 'child-only')
    $singleEnvironmentResult = Invoke-NativeProcess $singleEnvironmentCommand $root $singleEnvironment
    $parentHadSingleAfter = Test-Path -LiteralPath ("Env:\{0}" -f $singleEnvironmentKey)
    Assert-SelfTest ($singleEnvironmentResult.ExitCode -eq 0 -and $parentHadSingleBefore -eq $parentHadSingleAfter) 'one child-only environment override'

    $multipleEnvironment = @{
        TEMP = $runTemp
        TMP = $runTemp
    }
    $multipleEnvironment.set_Item($multipleEnvironmentKey, 'multiple')
    $multipleEnvironment.set_Item($emptyEnvironmentKey, '')
    $multipleEnvironmentResult = Invoke-NativeProcess $multipleEnvironmentCommand $root $multipleEnvironment
    Assert-SelfTest ($multipleEnvironmentResult.ExitCode -eq 0) 'multiple child environment overrides including empty value'

    $parentHadMultipleAfter = Test-Path -LiteralPath ("Env:\{0}" -f $multipleEnvironmentKey)
    $parentHadEmptyAfter = Test-Path -LiteralPath ("Env:\{0}" -f $emptyEnvironmentKey)
    $parentEnvironmentUnchanged = (
        $env:TEMP -ceq $parentTempBefore -and
        $env:TMP -ceq $parentTmpBefore -and
        $parentHadMultipleBefore -eq $parentHadMultipleAfter -and
        $parentHadEmptyBefore -eq $parentHadEmptyAfter
    )
    Assert-SelfTest $parentEnvironmentUnchanged 'parent environment remains unchanged'

    $singleOrdinarySelection = @(Get-OfflineBehavioralTestSelection -DiscoveredPaths @($ordinaryLaterPath) -ForbiddenLiveSmokePath $liveSmokeEntryPoint)
    Assert-SelfTest ($singleOrdinarySelection.Count -eq 1 -and $singleOrdinarySelection[0] -ceq $ordinaryLaterPath) 'ordinary deterministic root test is selected'

    $orderedOrdinarySelection = @(Get-OfflineBehavioralTestSelection -DiscoveredPaths @($ordinaryLaterPath, $ordinaryEarlierPath) -ForbiddenLiveSmokePath $liveSmokeEntryPoint)
    Assert-SelfTest (
        $orderedOrdinarySelection.Count -eq 2 -and
        $orderedOrdinarySelection[0] -ceq $ordinaryEarlierPath -and
        $orderedOrdinarySelection[1] -ceq $ordinaryLaterPath
    ) 'all ordinary root tests remain selected in ordinal filename order'

    $smokeGuardMessage = ''
    $smokeCommandCreationReached = $false
    try {
        [void](Get-OfflineBehavioralTestSelection -DiscoveredPaths @($ordinaryEarlierPath, $liveSmokeEntryPoint) -ForbiddenLiveSmokePath $liveSmokeEntryPoint)
        $smokeCommandCreationReached = $true
    }
    catch {
        $smokeGuardMessage = $_.Exception.Message
    }
    Assert-SelfTest (
        -not $smokeCommandCreationReached -and
        $smokeGuardMessage.Contains($liveSmokeEntryPoint)
    ) 'established live-smoke entry point is rejected before command creation or process launch'

    $summaryWithoutGuard = & {
        try {
            Write-OfflineVerificationSummary -CommandCount 1 -BehavioralTestCount 1 -LiveSmokeGuardPassed $false
        }
        catch {
            Write-Output $_.Exception.Message
        }
    } *>&1 | Out-String -Width 4096
    $summaryWithGuard = & {
        Write-OfflineVerificationSummary -CommandCount 1 -BehavioralTestCount 1 -LiveSmokeGuardPassed $true
    } *>&1 | Out-String -Width 4096
    $summaryBlockedWithoutGuard = (
        $summaryWithoutGuard -notmatch [regex]::Escape('live provider smoke excluded') -and
        $summaryWithoutGuard -match [regex]::Escape('guard has not passed')
    )
    $summaryAllowedAfterGuard = $summaryWithGuard -match [regex]::Escape('live provider smoke excluded')
    Assert-SelfTest (
        $summaryBlockedWithoutGuard -and
        $summaryAllowedAfterGuard
    ) 'live-smoke exclusion summary requires a passed exact-path guard'

    $fixtureCommand = New-CommandDescriptor -Name 'expected negative project-record fixtures' -FilePath $powerShellExecutable -Arguments @(
        '-NoLogo',
        '-NoProfile',
        '-NonInteractive',
        '-File',
        $validatorFixtures,
        '-ProjectRoot',
        $root
    )
    $fixtureResult = Invoke-NativeProcess $fixtureCommand $root $childEnvironment
    Assert-SelfTest ($fixtureResult.ExitCode -eq 0 -and $fixtureResult.Stdout -match 'Project-record fixture summary: 23 passed') 'expected negative fixtures do not leak failure'

    $script:firstFailureResult = $null
    $firstFailureOutput = & {
        $script:firstFailureResult = Invoke-VerificationSequence -Commands @($stdoutCommand, $stderrFailureCommand, $tracebackCommand) -WorkingDirectory $root -Environment $childEnvironment -ShowOutput
    } *>&1 | Out-String
    Assert-SelfTest (
        $script:firstFailureResult.ExitCode -eq 7 -and
        $script:firstFailureResult.FailedCommand -eq 'stderr nonzero' -and
        $script:firstFailureResult.Executed.Count -eq 2 -and
        ([regex]::Matches($firstFailureOutput, 'fixture failure')).Count -eq 1 -and
        -not $firstFailureOutput.Contains('fixture traceback')
    ) 'aggregate returns first genuine failure without duplicate failure output'

    $allPass = Invoke-VerificationSequence -Commands @($stdoutCommand, $stderrZeroCommand) -WorkingDirectory $root -Environment $childEnvironment
    Assert-SelfTest ($allPass.ExitCode -eq 0 -and $allPass.Executed.Count -eq 2) 'aggregate returns zero when all commands pass'

    $script:visibleSequenceResult = $null
    $visibleSequenceOutput = & {
        $script:visibleSequenceResult = Invoke-VerificationSequence -Commands @($stdoutCommand, $stderrZeroCommand) -WorkingDirectory $root -Environment $childEnvironment -ShowOutput
    } *>&1 | Out-String
    Assert-SelfTest (
        $script:visibleSequenceResult.ExitCode -eq 0 -and
        $visibleSequenceOutput.Contains('STDOUT: stdout zero') -and
        $visibleSequenceOutput.Contains('fixture stdout') -and
        $visibleSequenceOutput.Contains('STDERR: stderr zero') -and
        $visibleSequenceOutput.Contains('fixture stderr')
    ) 'successful stdout and stderr cross the aggregate reporting boundary independently'

    $successCleanupPath = Join-Path $runTemp 'cleanup-success'
    [IO.Directory]::CreateDirectory($successCleanupPath) | Out-Null
    Remove-VerificationTempDirectory -TempPath $successCleanupPath -AllowedBuildRoot $buildRoot
    Assert-SelfTest (-not (Test-Path -LiteralPath $successCleanupPath)) 'temporary directory is cleaned after success'

    $failureCleanupPath = Join-Path $runTemp 'cleanup-failure'
    [IO.Directory]::CreateDirectory($failureCleanupPath) | Out-Null
    $simulatedFailureObserved = $false
    try {
        try {
            throw 'simulated verification failure'
        }
        finally {
            Remove-VerificationTempDirectory -TempPath $failureCleanupPath -AllowedBuildRoot $buildRoot
        }
    }
    catch {
        $simulatedFailureObserved = $_.Exception.Message -eq 'simulated verification failure'
    }
    Assert-SelfTest (
        $simulatedFailureObserved -and
        -not (Test-Path -LiteralPath $failureCleanupPath)
    ) 'temporary directory is cleaned while preserving failure'

    Write-Host 'Runner self-test summary: 17 passed.'
}

$finalExitCode = 1
try {
    [IO.Directory]::CreateDirectory($runTemp) | Out-Null

    if ($SelfTest) {
        Invoke-RunnerSelfTest
        $finalExitCode = 0
    }
    else {
        $commands = @()
        $commands += (New-CommandDescriptor -Name 'current project records' -FilePath $powerShellExecutable -Arguments @(
            '-NoLogo',
            '-NoProfile',
            '-NonInteractive',
            '-File',
            $validator,
            '-ProjectRoot',
            $root
        ))
        $commands += (New-CommandDescriptor -Name 'project-record fixture suite' -FilePath $powerShellExecutable -Arguments @(
            '-NoLogo',
            '-NoProfile',
            '-NonInteractive',
            '-File',
            $validatorFixtures,
            '-ProjectRoot',
            $root
        ))

        $discoveredBehavioralPaths = @(Get-ChildItem -LiteralPath $root -Filter 'test_*.py' -File | ForEach-Object FullName)
        $behavioralTests = @(Get-OfflineBehavioralTestSelection -DiscoveredPaths $discoveredBehavioralPaths -ForbiddenLiveSmokePath $liveSmokeEntryPoint)
        $liveSmokeGuardPassed = $true
        foreach ($testPath in $behavioralTests) {
            $commands += (New-CommandDescriptor -Name ([IO.Path]::GetFileName($testPath)) -FilePath $interpreter -Arguments @($testPath))
        }

        $sequenceResult = Invoke-VerificationSequence -Commands $commands -WorkingDirectory $root -Environment $childEnvironment -ShowOutput
        $finalExitCode = $sequenceResult.ExitCode
        if ($finalExitCode -eq 0) {
            Write-OfflineVerificationSummary -CommandCount $commands.Count -BehavioralTestCount $behavioralTests.Count -LiveSmokeGuardPassed $liveSmokeGuardPassed
        }
    }
}
catch {
    Write-Host "FAIL: Offline behavioral verification runner error: $($_.Exception.Message)"
    if (-not [string]::IsNullOrWhiteSpace($_.ScriptStackTrace)) {
        Write-Host $_.ScriptStackTrace
    }
    $finalExitCode = 1
}
finally {
    try {
        Remove-VerificationTempDirectory -TempPath $runTemp -AllowedBuildRoot $buildRoot
    }
    catch {
        Write-Host "FAIL: Could not remove verification temp path: $($_.Exception.Message)"
        $finalExitCode = 1
    }
}

exit $finalExitCode
