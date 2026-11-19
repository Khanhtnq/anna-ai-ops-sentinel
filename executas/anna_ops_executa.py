#!/usr/bin/env python3
"""
AnnaOps Executa Plugin - Protocol v1.1 (JSON-RPC 2.0 over stdio).
Autonomous Multi-Agent Operations & Verification Engine for Anna OS.
"""

import sys
import os
import json
import time
import traceback
from typing import Dict, Any

# Ensure project root src is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.verification_engine import VerificationEngine
from src.colleague_orchestrator import ColleagueOrchestrator
from src.decision_gate import DecisionGate

class AnnaOpsExecuta:
    def __init__(self):
        self.verifier = VerificationEngine()
        self.orchestrator = ColleagueOrchestrator()
        self.gate = DecisionGate()
        self.started_at = time.time()

    def get_manifest(self) -> Dict[str, Any]:
        return {
            "name": "anna-ops-verification",
            "display_name": "AnnaOps Verification & Operations Hub",
            "version": "1.0.0",
            "description": "Multi-agent coordination, Causis Research invariant checking, and human-in-the-loop decision gating for Anna OS.",
            "author": "Khanhtnq",
            "homepage": "https://github.com/Khanhtnq/anna-ai-ops-sentinel",
            "icon": "⚡",
            "category": "developer-tools",
            "license": "MIT",
            "tools": [
                {
                    "name": "verify_agent_pipeline",
                    "description": "Verify multi-agent execution traces against invariant loops, causal safety boundaries, and CU budgets.",
                    "timeout": 30,
                    "streaming": False,
                    "parameters": [
                        {"name": "trace_id", "type": "string", "description": "Unique identifier for execution trace", "required": False},
                        {"name": "call_chain", "type": "array", "items": {"type": "string"}, "description": "Sequence of colleague role IDs called", "required": True},
                        {"name": "cu_consumed", "type": "number", "description": "Compute Units consumed in trace", "required": False, "default": 12.5},
                        {"name": "latency_ms", "type": "number", "description": "Execution latency in milliseconds", "required": False, "default": 240.0},
                        {"name": "action_type", "type": "string", "description": "Action category: READ, WRITE, TRANSACT, EXTERNAL_DISPATCH", "required": False, "default": "READ"},
                        {"name": "confidence", "type": "number", "description": "Model confidence score (0.0 to 1.0)", "required": False, "default": 0.95}
                    ]
                },
                {
                    "name": "orchestrate_colleagues",
                    "description": "Dispatch tasks across specialized AI colleagues (Research, Content, Outbound, Support, Verification SRE).",
                    "timeout": 45,
                    "streaming": False,
                    "parameters": [
                        {"name": "objective", "type": "string", "description": "High-level goal for the multi-agent team", "required": True},
                        {"name": "roles", "type": "array", "items": {"type": "string"}, "description": "List of colleague roles to engage", "required": False},
                        {"name": "action_type", "type": "string", "description": "Intended action type (READ, WRITE, TRANSACT)", "required": False, "default": "READ"}
                    ]
                },
                {
                    "name": "audit_decision_gate",
                    "description": "Create or review a human-in-the-loop gate before committing high-stakes external actions.",
                    "timeout": 20,
                    "streaming": False,
                    "parameters": [
                        {"name": "action", "type": "string", "description": "create, decide, or list", "required": True},
                        {"name": "gate_id", "type": "string", "description": "Gate ID for decision action", "required": False},
                        {"name": "title", "type": "string", "description": "Gate title for creation", "required": False},
                        {"name": "proposal", "type": "string", "description": "Proposal summary for creation", "required": False},
                        {"name": "approved", "type": "boolean", "description": "True to approve, False to reject", "required": False},
                        {"name": "notes", "type": "string", "description": "Operator review notes", "required": False}
                    ]
                },
                {
                    "name": "export_audit_receipt",
                    "description": "Export tamper-evident cryptographic receipts (SHA-256) of verified operations.",
                    "timeout": 15,
                    "streaming": False,
                    "parameters": [
                        {"name": "limit", "type": "integer", "description": "Maximum number of audit records to return", "required": False, "default": 10}
                    ]
                }
            ],
            "credentials": [],
            "runtime": {"type": "python", "min_version": "3.10"}
        }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        t0 = time.perf_counter()

        if tool_name == "verify_agent_pipeline":
            trace = {
                "trace_id": arguments.get("trace_id", f"trace-{int(time.time()*1000)}"),
                "call_chain": arguments.get("call_chain", []),
                "cu_consumed": float(arguments.get("cu_consumed", 12.5)),
                "latency_ms": float(arguments.get("latency_ms", 240.0)),
                "action_type": arguments.get("action_type", "READ"),
                "confidence": float(arguments.get("confidence", 0.95)),
                "human_reviewed": arguments.get("human_reviewed", False)
            }
            res = self.verifier.verify_pipeline(trace)
            
            # Format display block for Anna chat UI verbatim rendering
            status_symbol = "✅" if res["verified"] else "⚠️"
            display_text = (
                f"{status_symbol} **AnnaOps Invariant Verification Report**\n"
                f"- **Trace ID:** `{res['trace_id']}`\n"
                f"- **Verdict:** {res['status']}\n"
                f"- **Rules Evaluated:** {res['rule_count']} ({res['passed_count']} passed, {res['failed_count']} failed)\n"
                f"- **Cryptographic Receipt:** `{res['receipt_hash'][:16]}...`\n"
            )
            for eval_item in res["evaluations"]:
                mark = "✓" if eval_item["passed"] else "✗"
                display_text += f"  • [{mark}] {eval_item['name']}: {eval_item['details']}\n"

            res["_display"] = display_text
            duration = round((time.perf_counter() - t0) * 1000.0, 2)
            return {"success": True, "data": res, "duration_ms": duration}

        elif tool_name == "orchestrate_colleagues":
            objective = arguments.get("objective", "Execute operations")
            roles = arguments.get("roles")
            action_type = arguments.get("action_type", "READ")
            
            dispatch_ctx = {"action_type": action_type}
            wf_trace = self.orchestrator.dispatch_workflow(objective, roles, dispatch_ctx)
            
            # Automatically run verifier on the orchestrated workflow
            verification_result = self.verifier.verify_pipeline(wf_trace)
            wf_trace["verification"] = verification_result

            display_text = (
                f"🤖 **Anna Colleague Team Dispatched**\n"
                f"- **Objective:** {objective}\n"
                f"- **Roles Involved:** {', '.join(wf_trace['call_chain'])}\n"
                f"- **Total CU Consumed:** `{wf_trace['total_cu']} CU`\n"
                f"- **Latency:** `{wf_trace['latency_ms']} ms`\n"
                f"- **Verification Status:** {'VERIFIED SAFE' if verification_result['verified'] else 'REQUIRES HUMAN GATE'}\n"
            )
            wf_trace["_display"] = display_text
            duration = round((time.perf_counter() - t0) * 1000.0, 2)
            return {"success": True, "data": wf_trace, "duration_ms": duration}

        elif tool_name == "audit_decision_gate":
            action = arguments.get("action", "list")
            if action == "create":
                title = arguments.get("title", "Review Proposal")
                proposal = arguments.get("proposal", "Execute critical action")
                confidence = float(arguments.get("confidence", 0.75))
                action_type = arguments.get("action_type", "TRANSACT")
                gate_rec = self.gate.create_gate(title, proposal, {"action_type": action_type}, confidence)
                display_text = (
                    f"🚪 **Decision Gate Registered** (`{gate_rec['gate_id']}`)\n"
                    f"- **Title:** {gate_rec['title']}\n"
                    f"- **Status:** {gate_rec['status']}\n"
                    f"- **Confidence:** {gate_rec['confidence']*100:.1f}%\n"
                )
                gate_rec["_display"] = display_text
                return {"success": True, "data": gate_rec, "duration_ms": round((time.perf_counter() - t0)*1000.0, 2)}

            elif action == "decide":
                gate_id = arguments.get("gate_id")
                approved = bool(arguments.get("approved", False))
                notes = arguments.get("notes", "")
                if not gate_id:
                    return {"success": False, "error": "gate_id is required for decide action"}
                decided_rec = self.gate.submit_decision(gate_id, approved, reviewer="AnnaOperator", notes=notes)
                display_text = (
                    f"⚖️ **Decision Gate Decided** (`{decided_rec['gate_id']}`)\n"
                    f"- **Outcome:** {decided_rec['status']}\n"
                    f"- **Reviewer Notes:** {decided_rec['reviewer_notes']}\n"
                    f"- **Receipt SHA-256:** `{decided_rec['receipt_hash'][:16]}...`\n"
                )
                decided_rec["_display"] = display_text
                return {"success": True, "data": decided_rec, "duration_ms": round((time.perf_counter() - t0)*1000.0, 2)}

            else:  # list
                pending = self.gate.list_pending()
                return {"success": True, "data": {"pending_gates": pending, "count": len(pending)}, "duration_ms": round((time.perf_counter() - t0)*1000.0, 2)}

        elif tool_name == "export_audit_receipt":
            limit = int(arguments.get("limit", 10))
            history = self.gate.list_history(limit)
            return {"success": True, "data": {"audit_trail": history, "total_records": len(history)}, "duration_ms": round((time.perf_counter() - t0)*1000.0, 2)}

        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}


def main():
    plugin = AnnaOpsExecuta()
    sys.stderr.write("[AnnaOps] Executa Plugin running on stdio (JSON-RPC 2.0)...\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "describe":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": plugin.get_manifest()
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "health":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "status": "ready",
                    "uptime_seconds": round(time.time() - plugin.started_at, 2),
                    "details": {"version": "1.0.0", "colleagues_ready": 5}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "invoke":
            tool_name = params.get("tool")
            arguments = params.get("arguments", {})
            context = params.get("context", {})
            try:
                res = plugin.execute_tool(tool_name, arguments, context)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": res
                }
            except Exception as e:
                sys.stderr.write(f"[AnnaOps] Tool execution error: {traceback.format_exc()}\n")
                sys.stderr.flush()
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"success": False, "error": str(e)}
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
