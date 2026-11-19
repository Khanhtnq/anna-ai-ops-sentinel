"""
Unit tests for VerificationEngine and Causis Research Invariant Rules.
"""

import unittest
from src.verification_engine import (
    VerificationEngine,
    InvariantLoopRule,
    CausalInterventionRule,
    BudgetGuardRule
)

class TestVerificationEngine(unittest.TestCase):
    def setUp(self):
        self.verifier = VerificationEngine()

    def test_acyclic_delegation_pass(self):
        trace = {
            "call_chain": ["research", "content", "verification"],
            "action_type": "READ",
            "confidence": 0.95
        }
        res = self.verifier.verify_pipeline(trace)
        self.assertTrue(res["verified"])
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(res["failed_count"], 0)
        self.assertIn("receipt_hash", res)
        self.assertEqual(len(res["receipt_hash"]), 64)

    def test_cycle_detection_fails(self):
        trace = {
            "call_chain": ["research", "outbound", "research"],
            "action_type": "READ",
            "confidence": 0.95
        }
        res = self.verifier.verify_pipeline(trace)
        self.assertFalse(res["verified"])
        self.assertEqual(res["status"], "FLAGGED_FOR_HUMAN_GATE")
        self.assertGreaterEqual(res["failed_count"], 1)

    def test_causal_intervention_high_impact_requires_confidence(self):
        # Action is TRANSACT but confidence is only 0.70 and no human review -> fail
        trace = {
            "call_chain": ["outbound"],
            "action_type": "TRANSACT",
            "confidence": 0.70,
            "human_reviewed": False
        }
        res = self.verifier.verify_pipeline(trace)
        self.assertFalse(res["verified"])

        # With human review -> pass
        trace["human_reviewed"] = True
        res_approved = self.verifier.verify_pipeline(trace)
        self.assertTrue(res_approved["verified"])

    def test_budget_envelope_breach(self):
        trace = {
            "call_chain": ["research"],
            "cu_consumed": 200.0,  # exceeds default max 150.0
            "latency_ms": 200.0
        }
        res = self.verifier.verify_pipeline(trace)
        self.assertFalse(res["verified"])

    def test_total_cu_fallback_from_orchestrator(self):
        trace = {
            "call_chain": ["research", "content"],
            "total_cu": 165.0,
            "latency_ms": 120.0
        }
        res = self.verifier.verify_pipeline(trace)
        self.assertFalse(res["verified"])
        budget_eval = next(e for e in res["evaluations"] if e["rule_id"] == "RULE-PERF-003")
        self.assertFalse(budget_eval["passed"])

    def test_receipt_hash_determinism(self):
        trace = {
            "trace_id": "static-trace-1",
            "call_chain": ["research", "verification"],
            "cu_consumed": 10.0,
            "latency_ms": 100.0
        }
        res1 = self.verifier.verify_pipeline(trace)
        self.assertIn("receipt_hash", res1)
        self.assertTrue(isinstance(res1["receipt_hash"], str))

if __name__ == "__main__":
    unittest.main()
