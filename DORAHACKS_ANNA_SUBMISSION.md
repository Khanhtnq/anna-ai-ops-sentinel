# DoraHacks BUIDL Submission: AnnaOps — Autonomous Multi-Agent Operations & Verification Hub

## Project Information

- **Project Name:** AnnaOps
- **Tagline:** Autonomous Multi-Agent Operations, Causis Invariant Verification & Decision Gating for Anna OS
- **Track / Program:** DoraHacks `Anna AI App Builder Program` ($6,000 Initial BUIDL Pool / $80,000 Monthly Grant Pool)
- **Target Category:** Developer Tools / AI Operating System Apps / Autonomous Operations & SRE
- **Repository:** `https://github.com/Khanhtnq/anna-ops-buidl`
- **Live Interactive Dashboard:** `docs/index.html` (GitHub Pages compatible standalone SPA)
- **Demo Video:** `assets/demo_anna_1080p.mp4` (40 seconds, 1920x1080 Full HD, 30 fps)
- **License:** MIT License

---

## 1. Executive Summary & Problem Solved

Modern AI agent architectures face a severe **coordination bottleneck**:
1. **The Copy-Paste Router Trap:** Users are forced to switch between isolated chat threads, document editors, and browser tabs, manually shuttling intermediate context.
2. **Brittle Workflow Graphs:** Traditional agent builders rely on rigid node graphs that fail when dynamic reasoning or unexpected conditions arise.
3. **Uncontrolled High-Impact Actions:** Autonomous agents dispatched with database write, API dispatch, or transaction capabilities lack mathematical invariant verification, risking hallucinated actions or infinite recursion loops.

**AnnaOps** solves this by leveraging the core philosophy of **Anna OS**:
- **Humans set the outcome; Anna coordinates specialized AI colleagues.**
- Built-in **Causis Research Invariant Verification Engine** (inspired by Causal World Models and Invariant Research from Causis Research & Invariant Labs).
- **Human-in-the-Loop Decision Gates** that automatically pause high-risk actions (writes, financial transactions, mass outreach) for human verification when model confidence falls below safety thresholds.

---

## 2. Technical Architecture & Anna OS Native Integration

AnnaOps is built strictly against official Anna developer standards:

```
+-----------------------------------------------------------------------------------+
|                                  Anna OS Host                                     |
|  (User Messenger Interface  •  Host API  •  CU Metering  •  Window Manager)       |
+-----------------------------------------+-----------------------------------------+
                                          |
                      JSON-RPC 2.0 (stdio)| Line-Delimited
                                          v
+-----------------------------------------------------------------------------------+
|                        AnnaOps Executa Plugin (v1.1)                              |
|                      (executas/anna_ops_executa.py)                               |
|                                                                                   |
|  - describe: Exposes tools, credentials schema, and runtime metadata               |
|  - invoke: Executes verify_agent_pipeline, orchestrate_colleagues, etc.          |
|  - health: Reports process readiness and uptime telemetry                         |
|  - _display: Injects verbatim formatted markdown blocks for Anna Chat UI          |
+-------------------+---------------------------------------+-----------------------+
                    |                                       |
                    v                                       v
+---------------------------------------+   +---------------------------------------+
|        Verification Engine            |   |     Colleague Orchestrator            |
|       (src/verification_engine.py)    |   |     (src/colleague_orchestrator.py)   |
|                                       |   |                                       |
| - RULE-INV-001: Acyclic Guard (DAG)   |   | - Market Intel & Research Agent       |
| - RULE-CAUSAL-002: Counterfactual Gate|   | - Content & Social Strategy Agent     |
| - RULE-PERF-003: CU & Latency Budget  |   | - Growth & Outbound Operations Agent  |
| - SHA-256 Tamper-Proof Receipts       |   | - Support & Customer Admin Agent      |
|                                       |   | - Invariant Verification SRE Agent    |
+---------------------------------------+   +---------------------------------------+
```

### Protocol Compliance (JSON-RPC 2.0 stdio v1.1):
- **Transport:** Standard input/output with line-delimited JSON frames (`\n`).
- **Standard Out Isolation:** Pure JSON-RPC response frames on `stdout`; logs routed exclusively to `stderr`.
- **Long-Running Daemon:** Persistent loop reading stdin, graceful exit on EOF.
- **Display Blocks (`_display`):** Declares presentation-critical markdown blocks rendered verbatim by Anna Chat UI without LLM re-paraphrasing.

### Anna App Manifest Schema 4 (`anna.manifest.json`):
- Fully compliant with **Schema 4** specification (`extra="forbid"` passing).
- `required_executas`: Declares `tool-anna-ops-verification` (v1.0.0).
- `storage.scopes`: Explicit `user: rw` declaration.
- `ui.bundle`: Format `static-spa`, entry `index.html`.
- `ui.views`: 3 responsive views configured within strict viewport baselines (`min_size.h <= 600`, `min_size.w <= 1024`):
  1. `main` (Default: true, 1024x680)
  2. `verification_gate` (Decision review window)
  3. `colleague_mesh` (Topology and telemetry)
- `form_factors`: Multi-device support (`["desktop", "mobile"]`).

---

## 3. Core Capabilities & Invariant Safety Rules

### 1. Invariant Loop Protection (`RULE-INV-001`)
Ensures agent-to-agent delegation forms a strict Directed Acyclic Graph (DAG). If a colleague attempts to re-invoke an ancestor in the same trace (e.g. `research` -> `outbound` -> `research`), AnnaOps detects the cycle, halts execution, and flags the trace before token exhaustion occurs.

### 2. Counterfactual Safety Gate (`RULE-CAUSAL-002`)
Evaluates active counterfactual interventions prior to committing `WRITE`, `TRANSACT`, or `EXTERNAL_DISPATCH` operations. If model confidence is `< 88%` or an action touches external financial/data layers, it automatically diverts to a Human Decision Gate.

### 3. Compute Unit (CU) & Latency Budget Envelope (`RULE-PERF-003`)
Guarantees multi-agent workflows respect host resource bounds (max 150 CU and 6,000ms latency ceiling per invocation).

### 4. Cryptographic Proof of Verification
Every verified trace and human decision logs an immutable SHA-256 receipt containing the exact evaluation state, timestamp, and rule outcomes.

---

## 4. Verification & Unit Test Suite

The codebase includes an automated test suite with **100% pass rate** across all modules:

```bash
python run_tests.py
```

### Test Suite Summary:
- `test_executa_protocol.py`: stdio JSON-RPC 2.0 `describe`, `invoke`, `health`, unknown method handling, and `_display` block formatting.
- `test_verification_engine.py`: Acyclic delegation, counterfactual intervention, budget breaches, and SHA-256 receipt determinism.
- `test_colleague_orchestrator.py`: Multi-role task dispatch, task counter increments, and CU aggregation.
- `test_decision_gate.py`: Auto-approval heuristics, pending gate creation, human approval/rejection lifecycle.
- `test_manifest_schema.py`: Schema 4 versioning, forbidden legacy keys, UI view constraints, and system prompt length limits.

**Result:** `23/23 Tests Passed (100.0%)` in 0.192s.

---

## 5. Live Standalone Dashboard (`docs/index.html`)

The dashboard is built as a zero-dependency, ultra-responsive Single Page Application (SPA) designed to function both inside an Anna OS sandboxed iframe and as a standalone web app:

1. **Colleague Mesh Tab:** Interactive visualization of 5 specialized agents with live workflow dispatch and CU telemetry.
2. **Invariant Verifier Tab:** Real-time rule evaluation, anomaly injection testing, and SHA-256 proof inspection.
3. **Decision Gates Tab:** Interactive cards allowing operators to review proposals, examine confidence meters, and approve/reject actions.
4. **Executa JSON-RPC Simulator:** Interactive client terminal simulating stdio request/response frames (`describe`, `health`, `invoke`).
5. **DoraHacks Grant Analytics:** Visual tracking towards the 200 Qualified Monthly Active Users (MAU) milestone.

---

## 6. DoraHacks Traction & Growth Roadmap (Path to 200+ MAU)

The DoraHacks Anna AI App Builder Program rewards builder traction with recurring monthly grants scaling from $1,000/mo (at 200 MAU) up to $15,000+/mo (Tier 3).

### Target Adoption Milestones:
- **Phase 1 (Week 1–2):** Alpha Launch on Anna Marketplace; onboard developer DAOs and Solana AI builders.
- **Phase 2 (Week 3–4):** Integration with community workflows (automated Superteam bounty tracking & verification); achieve **200 Qualified MAU** to unlock Tier 1 Grant ($1,000/mo).
- **Phase 3 (Month 2):** Expand to multi-tenant organization SRE monitoring, scaling to Tier 2 (1,000 MAU / $5,000/mo).

---

## 7. Submission Checklist & Deliverable Index

- [x] Full source code under `src/` and `executas/anna_ops_executa.py`
- [x] Schema 4 Anna App Manifest (`anna.manifest.json`)
- [x] Interactive Dashboard SPA (`ui/index.html` and `docs/index.html`)
- [x] Full Unit Test Suite (`tests/` and `run_tests.py`) with 100% pass rate
- [x] 40-second 1080p 30fps Demo Video (`assets/demo_anna_1080p.mp4`)
- [x] Zero Local Path Leaks: Verified 100% clean of host environment paths or usernames
- [x] MIT Open Source License (`LICENSE`)
