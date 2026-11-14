"""
Human-in-the-Loop Decision Gate and Audit Receipt Ledger.
Allows humans to intervene, review confidence flags, approve, or reject high-impact AI colleague operations.
"""

import time
import hashlib
import json
from typing import Dict, List, Any, Optional

class DecisionGate:
    def __init__(self):
        self.pending_gates: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def create_gate(self, title: str, proposal: str, context: Dict[str, Any], confidence: float) -> Dict[str, Any]:
        gate_id = f"gate-{int(time.time()*1000)}-{len(self.pending_gates)+1}"
        auto_approved = confidence >= 0.88 and context.get("action_type") not in ["TRANSACT", "EXTERNAL_DISPATCH"]

        gate_record = {
            "gate_id": gate_id,
            "title": title,
            "proposal": proposal,
            "confidence": confidence,
            "action_type": context.get("action_type", "READ"),
            "status": "APPROVED" if auto_approved else "PENDING_REVIEW",
            "auto_approved": auto_approved,
            "created_at": time.time(),
            "decision": "AUTO_APPROVE" if auto_approved else None,
            "reviewer_notes": "Automatically passed confidence threshold" if auto_approved else "Requires human operator confirmation",
            "receipt_hash": None
        }

        if auto_approved:
            gate_record["receipt_hash"] = self._generate_receipt(gate_record)
            self.audit_log.append(gate_record)
        else:
            self.pending_gates[gate_id] = gate_record

        return gate_record

    def submit_decision(self, gate_id: str, approved: bool, reviewer: str = "operator", notes: str = "") -> Dict[str, Any]:
        if gate_id not in self.pending_gates:
            raise KeyError(f"Gate {gate_id} not found or already decided")

        record = self.pending_gates.pop(gate_id)
        record["status"] = "APPROVED" if approved else "REJECTED"
        record["decision"] = "HUMAN_APPROVE" if approved else "HUMAN_REJECT"
        record["reviewer"] = reviewer
        record["reviewer_notes"] = notes or ("Approved via human operator" if approved else "Rejected via human operator")
        record["decided_at"] = time.time()
        record["receipt_hash"] = self._generate_receipt(record)

        self.audit_log.append(record)
        return record

    def list_pending(self) -> List[Dict[str, Any]]:
        return list(self.pending_gates.values())

    def list_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.audit_log[-limit:]

    def _generate_receipt(self, record: Dict[str, Any]) -> str:
        clean = {k: v for k, v in record.items() if k != "receipt_hash"}
        raw = json.dumps(clean, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
