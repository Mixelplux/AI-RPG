# F01/F05 API environment repair and preflight

Owner-authorized tooling maintenance, October 16, 2026. Uncommitted, not published.
Protected baseline/HEAD: `d2ededee58294002f522cef5ab61577270311997`.
Checkout: `D:/AI RPG/.artifacts/f01-f05-bounded-playable-integration-v1`;
branch `codex/f01-f05-bounded-playable-integration-v1`.
Local main, origin/main and actual remote main independently match the baseline.
Current accepted WORKFLOW/PROJECT/AGENTS and the gate implementation handoff were
read before changes. This is the separately authorized environment maintenance
task; the existing scenario lifecycle and candidate remain unchanged.

## Root cause and evidence

The earlier handoff's statement that no key was configured was incomplete.
Absence of `OPENAI_API_KEY` from the process/user environment did not establish
absence of the established credential configuration.

1. The previously working F01 launchers resolve **registered** Local AppData
   from `HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`,
   read `AI RPG/NarratorSmoke/credential.dpapi`, decrypt with CurrentUser DPAPI,
   and inject the key only into their Python child's environment. The registered
   store still exists and decrypts successfully under this task's Windows user.
2. The gate's direct Python launcher reads only its inherited environment through
   the accepted provider adapter. It performs no credential-store loading. The
   established bridge was historical/untracked tooling, absent from the protected
   main tree and this new checkout. A virtual-environment junction supplies
   packages and an interpreter, not another process's credentials.
3. This sandbox redirects `LOCALAPPDATA` and `TEMP` under its package's `AC`
   directory. A loader using the inherited Local AppData path would miss the
   existing profile store. Prior F01 launchers already used the registered-folder
   resolution to avoid this. No new credential, rotation or secret export is needed.
4. Redirected Temp also hid the existing tokenizer cache. An otherwise restored
   credential would encounter a cache miss/download attempt. The repaired launch
   environment resolves the default cache from registered Local AppData's
   `Temp/data-gym-cache`; it preserves an explicit `TIKTOKEN_CACHE_DIR` override.

Observed failure class: **local credential-loading/process-context configuration**,
plus the cache-location dependency. Credential file access and DPAPI decryption
now pass; there is no observed OS permission failure. No authentication failure,
API permission denial, malformed request or model-access failure has been observed,
because no API request was made. Those remain unverified, not implicitly passed.

The installed HTTPX client trusts inherited environment/system proxy settings.
The checked process has no effective proxy. No proxy interference was observed
here, and no proxy, NO_PROXY rule, TLS setting, firewall or sandbox policy was
removed or bypassed. Other process contexts must run their own readiness check.

The accepted provider source remains `gpt-6-luna`, low reasoning, 20-second
timeout and zero retries; accepted F01 requests its existing 2048-token output
budget. Installed SDK 2.45.0, HTTPX 0.28.1 and tiktoken 0.13.0 construct/load
successfully in the official environment. These are local compatibility checks,
not evidence of server-side model availability or credential validity.

## Reusable offline check

From the isolated repository root, in PowerShell 7 on Windows:

```powershell
.\tools\Invoke-ApiTask.ps1
```

This performs **no API request** and consumes **zero narration generations**.
It uses `.\.venv\Scripts\python.exe -B -m tools.api_readiness` in the selected
checkout. The key reaches only the required child environment; neither the
parent environment nor the stored credential is modified. Output consists of
fixed diagnostic codes; stdout/stderr from arbitrary tasks and exception details
are suppressed. No key, fragment, hash, ciphertext, headers or response body is
logged. Temporary unmanaged BSTR memory is zeroed and references are dropped;
managed memory cannot be reliably wiped. The existing store remains outside Git.

Success ends with:

```text
API_LOCAL_READY authentication=unverified permissions=unverified connectivity=unverified requests=0 generations=0
```

This means local prerequisites are ready. It does not contact the provider or
certify authentication, account/model permissions, quota, DNS/TLS connectivity,
or generated fidelity. Tokenizer misses fail without downloading. Explicit
non-default endpoints fail for local review; their values are never printed.
Valid-looking proxies are preserved and reported as unverified, not tested or
silently disabled. Known local discard-port proxies and malformed proxy settings
block readiness. SDK construction checks local proxy/TLS configuration only.

For a **separately owner-authorized**, trusted, noninteractive Python evaluation
script, the same launcher can preserve this environment for execution:

```powershell
.\tools\Invoke-ApiTask.ps1 -TaskScript tools/my_authorized_evaluation.py -TaskArguments @('--live')
```

The example path is illustrative, not a new evaluation entrypoint. Task paths
must be existing relative `.py` files within this checkout; path escapes and
reparse paths are rejected. Arguments are separate process arguments, never
shell-expanded command text. Never put secrets in task arguments. A task runs
only after readiness passes, has a sixty-second process timeout, and returns
its exit code with output suppressed. Use it for trusted scripted evaluations
with their own approved evidence handling; it is not an interactive game runner.
Default invocation never executes a task. Supplying a script does not grant
provider authority. The earlier eight-generation allowance is untouched; the
current maintenance request expressly forbids resuming fidelity evaluation.

## Actionable failures

| Code/stage | Meaning and local action |
|---|---|
| `platform`, `interpreter` | Use PowerShell 7 on Windows and the existing official virtual environment in this checkout. Do not install a substitute interpreter. |
| `profile_lookup`, `store_path` | Registered profile path unavailable or unsafe. Run as the intended Windows user; review the path locally without dumping environment/store contents. Reparse/store-in-repo paths are rejected. |
| `store_missing` | Registered DPAPI store is absent. Restore the established outside-repo setup using its secure local prompt; do not put a key in chat, argv or repository files. This repair does not create or replace credentials. |
| `store_read` | Store exists but cannot be read; check the intended account and local access. No automatic ACL repair is attempted. |
| `dpapi_decrypt` | CurrentUser decryption or nonempty credential check failed; use the owning Windows account/profile. This is distinct from provider authentication. |
| `credential_missing_or_whitespace` | Python child lacks valid local configuration. Use this launcher; do not mistake direct Python invocation for the credential bridge. |
| `endpoint_override` | Review `OPENAI_BASE_URL` locally; no alternate endpoint is silently trusted. |
| `proxy_configuration_blocked` | Review inherited/system proxies in the intended authorized execution context. No automatic proxy removal or network-policy bypass. |
| `dependency_or_tokenizer_unavailable` | Use the official environment and an existing verified tokenizer cache. Downloads/installations are not part of this check. |
| `client_configuration_failed` | Review local SDK, proxy and certificate configuration; raw SDK exceptions are suppressed. |
| `task_path`, `task_execution`, `child_launch`, `readiness_protocol` | Check the selected trusted script/path, timeout, process permissions and checker output protocol locally. Child traceback contents stay suppressed. |

The existing provider adapter intentionally collapses HTTP status errors into a
generic provider-request failure; that does not establish their cause. It was
not modified. The small `classify_failure` utility accepts an already-caught SDK
exception and returns only a fixed category: 401 authentication, 403 permission,
404 model/endpoint, 429 rate/quota, other HTTP request/server error, or connection/
timeout/client error. It sends no request and never formats error text, bodies or
headers. Categories follow [official OpenAI error guidance](https://developers.openai.com/api/docs/guides/error-codes).
Credential handling follows the [official authentication boundary](https://developers.openai.com/api/reference/overview#authentication).
Only a separately authorized actual API probe could validate service access;
none was necessary to diagnose or repair this local failure, and none was run.

## Validation and preservation

- Changed Python syntax and both PowerShell parser checks passed before execution.
- Eight Python tests pass: ready/unverified distinctions, missing/whitespace key,
  endpoint/proxy suppression, proxy classification, cache miss, local SDK error,
  immutable environment and fixed error categories. Network DNS/socket calls
  are denied in the test harness; SDK/encoding behavior is injected.
- Ten PowerShell integration checks pass using an isolated **synthetic** DPAPI
  credential and mocked profile lookup, never the actual store. They cover
  missing/unreadable encryption, child delivery, discard proxy, download-free
  cache failure, task output suppression, path escape rejection and preservation
  of parent key/proxy/cache environment. The unique synthetic store was removed.
- Actual local readiness passes with the existing store and cache. This verifies
  decryption, child inheritance and offline client/encoding construction only.
  Zero live provider requests/probes and zero narration generations were used.
- Shared GitWorkflowTools verification passed, reporting unchanged repository
  state during its checks. Its worktree-bound profile/log are new ignored
  artifacts in `.artifacts/api-environment-verification/`; prior gate verification
  evidence and shared profiles/tools were not overwritten. Lifecycle/preflight,
  tracked/index diff checks, new-file whitespace and scope checks passed. The
  pre-existing nine tracked scenario-diff paths remain the same; all five changes
  from this maintenance task are new tooling, test or operational-document files.

Changes are confined to `tools/Invoke-ApiTask.ps1`, `tools/api_readiness.py`,
`tools/Test-ApiTask.ps1`, `test_api_readiness.py` and this tooling handoff. No
gameplay/narrative/scenario/doctrine/architecture file changed in this maintenance
task. The pre-existing 13-path uncommitted scenario candidate, original checkout,
saves, historical launchers, evidence, accepted source, virtual environment,
credential store, main and remote baseline are preserved. No staging, commit,
push, merge or publication occurred; the index remains empty.

Documentation reconciliation is this operational handoff. No architecture,
system manifest, doctrine, ADR or lifecycle change is warranted: only a tooling
launch environment was repaired, with no runtime interface or gameplay change.
The old gate report remains preserved as historical handoff; this report corrects
its earlier environment conclusion without claiming a completed live evaluation.

**Readiness outcome:** local environment blocker repaired. Live authentication,
permissions, connectivity and fidelity remain unverified. Stop here pending
separate owner authorization for a probe or resumed live evaluation.
