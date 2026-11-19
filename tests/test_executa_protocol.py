"""
Unit tests for Anna Executa Plugin (JSON-RPC 2.0 over stdio Protocol v1.1).
"""

import unittest
import json
import subprocess
import sys
import os

class TestExecutaProtocol(unittest.TestCase):
    def setUp(self):
        self.plugin_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "executas",
            "anna_ops_executa.py"
        )

    def _call_rpc(self, request_obj):
        proc = subprocess.Popen(
            [sys.executable, self.plugin_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        req_line = json.dumps(request_obj) + "\n"
        stdout, stderr = proc.communicate(input=req_line, timeout=5)
        for line in stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)
        self.fail(f"No JSON response from plugin. Stdout: {stdout}, Stderr: {stderr}")

    def test_describe_method(self):
        req = {"jsonrpc": "2.0", "method": "describe", "id": 1}
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("jsonrpc"), "2.0")
        self.assertEqual(resp.get("id"), 1)
        res = resp.get("result", {})
        self.assertEqual(res.get("name"), "anna-ops-verification")
        self.assertEqual(res.get("homepage"), "https://github.com/Khanhtnq/anna-ai-ops-sentinel")
        self.assertIn("tools", res)
        tool_names = [t["name"] for t in res["tools"]]
        self.assertIn("verify_agent_pipeline", tool_names)
        self.assertIn("orchestrate_colleagues", tool_names)
        self.assertIn("audit_decision_gate", tool_names)

    def test_health_method(self):
        req = {"jsonrpc": "2.0", "method": "health", "id": 2}
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("id"), 2)
        res = resp.get("result", {})
        self.assertEqual(res.get("status"), "ready")
        self.assertIn("uptime_seconds", res)

    def test_invoke_verify_agent_pipeline(self):
        req = {
            "jsonrpc": "2.0",
            "method": "invoke",
            "id": 3,
            "params": {
                "tool": "verify_agent_pipeline",
                "arguments": {
                    "call_chain": ["research", "verification"],
                    "cu_consumed": 14.2,
                    "latency_ms": 180.0
                }
            }
        }
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("id"), 3)
        res = resp.get("result", {})
        self.assertTrue(res.get("success"))
        data = res.get("data", {})
        self.assertTrue(data.get("verified"))
        self.assertIn("_display", data)
        self.assertIn("receipt_hash", data)

    def test_invoke_orchestrate_colleagues(self):
        req = {
            "jsonrpc": "2.0",
            "method": "invoke",
            "id": 4,
            "params": {
                "tool": "orchestrate_colleagues",
                "arguments": {
                    "objective": "Review DoraHacks grant applications",
                    "roles": ["research", "content", "verification"]
                }
            }
        }
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("id"), 4)
        res = resp.get("result", {})
        self.assertTrue(res.get("success"))
        data = res.get("data", {})
        self.assertEqual(data.get("colleagues_involved"), 3)
        self.assertIn("_display", data)

    def test_unknown_method_error(self):
        req = {"jsonrpc": "2.0", "method": "non_existent_method", "id": 99}
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("id"), 99)
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32601)

    def test_invoke_audit_decision_gate_and_export(self):
        req = {
            "jsonrpc": "2.0",
            "method": "invoke",
            "id": 5,
            "params": {
                "tool": "audit_decision_gate",
                "arguments": {
                    "action": "create",
                    "title": "External Payout",
                    "proposal": "Disburse 100 USDC bounty",
                    "action_type": "TRANSACT",
                    "confidence": 0.78
                }
            }
        }
        resp = self._call_rpc(req)
        self.assertEqual(resp.get("id"), 5)
        res = resp.get("result", {})
        self.assertTrue(res.get("success"))
        data = res.get("data", {})
        self.assertEqual(data.get("status"), "PENDING_REVIEW")
        self.assertIn("_display", data)

if __name__ == "__main__":
    unittest.main()
