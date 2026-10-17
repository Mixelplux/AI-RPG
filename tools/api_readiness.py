"""Local-only API readiness. No provider probe, retries, downloads or secret output."""
import json
import os
from unittest.mock import patch
from urllib.parse import urlsplit


def classify_failure(error):
    """Fixed categories only; never render exception messages, bodies or headers."""
    status = getattr(error, "status_code", None)
    if status == 401:
        return "authentication_failed"
    if status == 403:
        return "permission_denied"
    if status == 404:
        return "model_or_endpoint_unavailable"
    if status == 429:
        return "rate_or_quota_limit"
    if isinstance(status, int) and status >= 500:
        return "provider_server_error"
    if isinstance(status, int):
        return "request_rejected"
    return "connection_timeout_or_client_error"


def check_readiness():
    checks = []

    def add(name, ok, code, action):
        checks.append(dict(name=name, status="pass" if ok else "blocked", code=code, action=action))

    key = os.environ.get("OPENAI_API_KEY", "")
    add("credential", bool(key.strip()) and key == key.strip(),
        "credential_present" if key.strip() and key == key.strip() else "credential_missing_or_whitespace",
        "Use Invoke-ApiTask.ps1 to load the existing DPAPI store into the child; do not paste keys into commands.")
    key = None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    add("endpoint", base.rstrip("/") == "https://api.openai.com/v1", "endpoint_default" if base.rstrip("/") == "https://api.openai.com/v1" else "endpoint_override",
        "Review OPENAI_BASE_URL locally before using a non-default endpoint; its value is suppressed.")
    try:
        from httpx._utils import get_environment_proxies
        proxies = get_environment_proxies()  # matches installed SDK: environment/system config
        for address in proxies.values():
            if address is None:  # NO_PROXY bypass, retained unchanged
                continue
            parsed = urlsplit(address)
            port = parsed.port  # validate even for a non-loopback host
            if parsed.scheme not in {"http", "https", "socks5", "socks5h"} or not parsed.hostname:
                raise ValueError("Invalid proxy")
            if parsed.hostname in {"localhost", "127.0.0.1", "::1"} and port == 9:
                raise ValueError("Local deny proxy")
        add("proxy", True, "proxy_present_unverified" if any(proxies.values()) else "no_effective_proxy",
            "Inherited proxy and NO_PROXY settings are preserved. Reachability is untested; use an authorized network context for any future probe.")
    except Exception:
        add("proxy", False, "proxy_configuration_blocked",
            "Review proxy settings locally; malformed or local discard-port proxies block readiness. No proxy was removed.")
    try:
        from engine import narration_source as source
        import tiktoken
        add("model", (source.OPENAI_MODEL, source.OPENAI_REASONING_EFFORT) == ("gpt-6-luna", "low"),
            "accepted_model_configuration" if (source.OPENAI_MODEL, source.OPENAI_REASONING_EFFORT) == ("gpt-6-luna", "low") else "model_configuration_changed",
            "Use the accepted narration source configuration; no model substitution is performed.")
        # tiktoken validates cache integrity. A cache miss must not download.
        with patch("tiktoken.load.read_file", side_effect=RuntimeError("Offline cache miss")):
            tiktoken.encoding_for_model(source.OPENAI_TOKENIZER_MODEL).encode("readiness")
        add("tokenizer", True, "tokenizer_cached", "No tokenizer download was needed.")
    except Exception:
        add("tokenizer", False, "dependency_or_tokenizer_unavailable",
            "Use the official virtual environment and an existing TIKTOKEN_CACHE_DIR; dependency/cache download needs separate authorization.")
    try:
        from openai import OpenAI
        # Construction only: validates local SDK, proxy and TLS configuration.
        with OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or "offline-readiness-placeholder",
                    timeout=20.0, max_retries=0):
            pass
        add("client", True, "client_constructed_offline", "No HTTP request was sent.")
    except Exception:
        add("client", False, "client_configuration_failed",
            "Check installed SDK, proxy and TLS certificate configuration in the official environment; exception contents suppressed.")
    return dict(ready=all(c["status"] == "pass" for c in checks), checks=checks,
                authentication="unverified", permissions="unverified", connectivity="unverified",
                provider_requests=0, narration_generations=0)


def main():
    try:
        report = check_readiness()
        print(json.dumps(report))
        return 0 if report["ready"] else 1
    except Exception:
        print(json.dumps({"ready": False, "code": "local_check_failed", "provider_requests": 0}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
