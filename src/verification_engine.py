"""
Core Verification & Invariant Analysis Engine for AnnaOps.
Inspired by Causis Research (Causal World Models, Invariant Verification).
Evaluates multi-agent traces, ensures safety boundaries, and issues cryptographic receipts.
"""

import hashlib
import json
import time
from typing import Dict, List, Any, Optional

class VerificationRule:
    def __init__(self, rule_id: str, name: str, description: str, severity: str = "HIGH"):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity

    def evaluate(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class InvariantLoopRule(VerificationRule):
    """Ensures multi-agent delegations do not form infinite recursion or cycles."""
    def __init__(self):
        super().__init__(
            rule_id="RULE-INV-001",
            name="Acyclic Delegation Guard",
            description="Prevents cyclic delegation between autonomous AI colleagues",
            severity="CRITICAL"
        )

    def evaluate(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        call_chain = trace_data.get("call_chain", [])
        seen = set()
        has_cycle = False
        repeated_node = None

        for node in call_chain:
            if node in seen:
                has_cycle = True
                repeated_node = node
                break
            seen.add(node)

        passed = not has_cycle
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "passed": passed,
            "severity": self.severity,
            "details": f"Cycle detected on colleague '{repeated_node}'" if has_cycle else "Call chain is strictly acyclic"
        }


class CausalInterventionRule(VerificationRule):
    """Verifies counterfactual interventions before committing external actions."""
    def __init__(self):
        super().__init__(
            rule_id="RULE-CAUSAL-002",
            name="Counterfactual Safety Gate",
            description="Validates counterfactual sensitivity before write/spend actions",
            severity="HIGH"
        )

    def evaluate(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        action_type = trace_data.get("action_type", "READ")
        confidence = trace_data.get("confidence", 1.0)
        has_human_review = trace_data.get("human_reviewed", False)

        if action_type in ["WRITE", "TRANSACT", "EXTERNAL_DISPATCH"]:
            # If high-impact action, confidence must exceed threshold or have human approval
            passed = confidence >= 0.85 or has_human_review
            reason = "Confidence >= 0.85 or approved by human gate" if passed else "High-risk action below 0.85 confidence requires human gate approval"
        else:
            passed = True
            reason = "Read-only operations automatically satisfy safety envelope"

        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "passed": passed,
            "severity": self.severity,
            "details": reason
        }


class BudgetGuardRule(VerificationRule):
    """Enforces CU (Compute Unit) and latency ceilings per invocation."""
    def __init__(self, max_cu: float = 100.0, max_latency_ms: float = 5000.0):
        super().__init__(
            rule_id="RULE-PERF-003",
            name="CU & Latency Envelope Guard",
            description="Prevents compute exhaustion and latency degradation",
            severity="MEDIUM"
        )
        self.max_cu = max_cu
        self.max_latency_ms = max_latency_ms

    def evaluate(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        cu_consumed = float(trace_data.get("cu_consumed", trace_data.get("total_cu", 0.0)))
        latency_ms = float(trace_data.get("latency_ms", 0.0))

        passed = (cu_consumed <= self.max_cu) and (latency_ms <= self.max_latency_ms)
        details = (
            f"CU: {cu_consumed:.2f}/{self.max_cu}, Latency: {latency_ms:.1f}/{self.max_latency_ms}ms"
            if passed else
            f"Limit breached! Consumed CU={cu_consumed:.2f} (max {self.max_cu}), Latency={latency_ms:.1f}ms (max {self.max_latency_ms}ms)"
        )

        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "passed": passed,
            "severity": self.severity,
            "details": details
        }


class VerificationEngine:
    def __init__(self):
        self.rules: List[VerificationRule] = [
            InvariantLoopRule(),
            CausalInterventionRule(),
            BudgetGuardRule(max_cu=150.0, max_latency_ms=6000.0)
        ]

    def add_rule(self, rule: VerificationRule) -> None:
        self.rules.append(rule)

    def verify_pipeline(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.perf_counter()
        results = []
        overall_passed = True

        for rule in self.rules:
            res = rule.evaluate(trace_data)
            results.append(res)
            if not res["passed"]:
                overall_passed = False

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Cryptographic receipt generation (SHA-256)
        receipt_payload = {
            "trace_id": trace_data.get("trace_id", f"trace-{int(time.time()*1000)}"),
            "timestamp": time.time(),
            "overall_passed": overall_passed,
            "evaluations": results
        }
        raw_bytes = json.dumps(receipt_payload, sort_keys=True).encode("utf-8")
        receipt_hash = hashlib.sha256(raw_bytes).hexdigest()

        return {
            "trace_id": receipt_payload["trace_id"],
            "verified": overall_passed,
            "status": "APPROVED" if overall_passed else "FLAGGED_FOR_HUMAN_GATE",
            "evaluations": results,
            "receipt_hash": receipt_hash,
            "rule_count": len(results),
            "passed_count": sum(1 for r in results if r["passed"]),
            "failed_count": sum(1 for r in results if not r["passed"]),
            "evaluation_duration_ms": round(duration_ms, 2)
        }
