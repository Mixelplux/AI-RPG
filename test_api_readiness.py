"""Local API tooling tests: synthetic credentials and denied network only."""
import json
import os
import socket
import unittest
from unittest.mock import MagicMock, patch

from tools.api_readiness import check_readiness, classify_failure


class ApiReadinessTests(unittest.TestCase):
    def setUp(self):
        self.environment = {"OPENAI_API_KEY": "offline-placeholder"}
        for guard in (
            patch.dict(os.environ, self.environment, clear=True),
            patch.object(socket.socket, "connect", side_effect=AssertionError("offline")),
            patch("socket.getaddrinfo", side_effect=AssertionError("offline")),
            patch("httpx._utils.get_environment_proxies", return_value={}),
            patch("tiktoken.encoding_for_model", return_value=MagicMock()),
            patch("openai.OpenAI"),
        ):
            guard.start()
            self.addCleanup(guard.stop)

    def test_ready_does_not_certify_service_access_or_mutate_environment(self):
        before = dict(os.environ)
        report = check_readiness()
        self.assertTrue(report["ready"])
        self.assertEqual(report["provider_requests"], 0)
        self.assertEqual(report["narration_generations"], 0)
        self.assertEqual(report["authentication"], "unverified")
        self.assertEqual(report["permissions"], "unverified")
        self.assertEqual(report["connectivity"], "unverified")
        self.assertEqual(dict(os.environ), before)
        self.assertNotIn(self.environment["OPENAI_API_KEY"], json.dumps(report))

    def test_missing_and_whitespace_credentials(self):
        for value in ("", "  ", " offline-placeholder "):
            os.environ["OPENAI_API_KEY"] = value
            report = check_readiness()
            self.assertFalse(report["ready"])
            self.assertEqual(report["checks"][0]["code"], "credential_missing_or_whitespace")

    def test_endpoint_override_blocks_without_disclosing_value(self):
        os.environ["OPENAI_BASE_URL"] = "https://private.invalid/secret-path"
        report = check_readiness()
        self.assertFalse(report["ready"])
        self.assertNotIn("private.invalid", json.dumps(report))
        self.assertNotIn("secret-path", json.dumps(report))

    def test_proxy_presence_is_not_proof_of_interference(self):
        with patch("httpx._utils.get_environment_proxies", return_value={"https://": "http://user:private@proxy.invalid:3128", "all://internal": None}):
            report = check_readiness()
        self.assertTrue(report["ready"])
        self.assertEqual(report["checks"][2]["code"], "proxy_present_unverified")
        self.assertNotIn("private", json.dumps(report))
        self.assertNotIn("proxy.invalid", json.dumps(report))

    def test_invalid_proxy_and_known_discard_proxy_block(self):
        for address in ("http://localhost:9", "http://127.0.0.1:9", "http://[::1]:9", "http://host:invalid", "invalid://host"):
            with patch("httpx._utils.get_environment_proxies", return_value={"https://": address}):
                report = check_readiness()
            self.assertFalse(report["ready"])
            self.assertEqual(report["checks"][2]["code"], "proxy_configuration_blocked")

    def test_tokenizer_cache_miss_does_not_download(self):
        with patch("tiktoken.encoding_for_model", side_effect=RuntimeError("private cache detail")):
            report = check_readiness()
        self.assertFalse(report["ready"])
        self.assertNotIn("private cache detail", json.dumps(report))

    def test_local_sdk_error_is_not_an_authentication_failure(self):
        with patch("openai.OpenAI", side_effect=ValueError("Bearer private SDK detail")):
            report = check_readiness()
        self.assertFalse(report["ready"])
        self.assertEqual(report["checks"][-1]["code"], "client_configuration_failed")
        self.assertEqual(report["authentication"], "unverified")
        self.assertNotIn("private SDK detail", json.dumps(report))

    def test_secret_safe_error_categories(self):
        for status, expected in ((401, "authentication_failed"), (403, "permission_denied"),
                                 (404, "model_or_endpoint_unavailable"), (400, "request_rejected"),
                                 (429, "rate_or_quota_limit"), (503, "provider_server_error"),
                                 (None, "connection_timeout_or_client_error")):
            error = RuntimeError("untrusted private message")
            error.status_code = status
            error.body = {"secret": "untrusted body"}
            self.assertEqual(classify_failure(error), expected)


if __name__ == "__main__":
    unittest.main()
