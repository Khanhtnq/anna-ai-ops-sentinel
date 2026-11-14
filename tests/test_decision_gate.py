"""
Unit tests for DecisionGate and cryptographic receipts.
"""

import unittest
from src.decision_gate import DecisionGate

class TestDecisionGate(unittest.TestCase):
    def setUp(self):
        self.gate = DecisionGate()

    def test_create_auto_approve_gate(self):
        rec = self.gate.create_gate(
            title="Read Readme",
            proposal="Fetch public repo readme",
            context={"action_type": "READ"},
            confidence=0.95
        )
        self.assertTrue(rec["auto_approved"])
        self.assertEqual(rec["status"], "APPROVED")
        self.assertIsNotNone(rec["receipt_hash"])

    def test_create_pending_gate_for_high_impact(self):
        rec = self.gate.create_gate(
            title="Transfer Funds",
            proposal="Send 100 USDC grant reward",
            context={"action_type": "TRANSACT"},
            confidence=0.99
        )
        self.assertFalse(rec["auto_approved"])
        self.assertEqual(rec["status"], "PENDING_REVIEW")
        self.assertEqual(len(self.gate.list_pending()), 1)

    def test_human_approval_flow(self):
        rec = self.gate.create_gate(
            title="Mass Dispatch",
            proposal="Send email campaign",
            context={"action_type": "TRANSACT"},
            confidence=0.80
        )
        gate_id = rec["gate_id"]

        decided = self.gate.submit_decision(gate_id, approved=True, reviewer="Alice", notes="LGTM")
        self.assertEqual(decided["status"], "APPROVED")
        self.assertEqual(decided["decision"], "HUMAN_APPROVE")
        self.assertIsNotNone(decided["receipt_hash"])
        self.assertEqual(len(self.gate.list_pending()), 0)
        self.assertGreaterEqual(len(self.gate.list_history()), 1)

    def test_human_rejection_flow(self):
        rec = self.gate.create_gate(
            title="Delete Database",
            proposal="Drop audit logs",
            context={"action_type": "TRANSACT"},
            confidence=0.50
        )
        gate_id = rec["gate_id"]

        decided = self.gate.submit_decision(gate_id, approved=False, reviewer="Bob", notes="Unsafe")
        self.assertEqual(decided["status"], "REJECTED")
        self.assertEqual(decided["decision"], "HUMAN_REJECT")

if __name__ == "__main__":
    unittest.main()
