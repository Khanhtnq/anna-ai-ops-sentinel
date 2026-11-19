# DoraHacks BUIDL Submission: AnnaOps — Autonomous Multi-Agent Operations & Verification Hub

## Project Information

- **Project Name:** AnnaOps
- **Tagline:** Autonomous Multi-Agent Operations, Causis Invariant Verification & Decision Gating for Anna OS
- **Track / Program:** DoraHacks `Anna AI App Builder Program` ($6,000 Initial BUIDL Pool / $80,000 Monthly Grant Pool)
- **Target Category:** Developer Tools / AI Operating System Apps / Autonomous Operations & SRE
- **Repository:** `https://github.com/Khanhtnq/anna-ai-ops-sentinel`
- **Live Interactive Dashboard & Invariant Sandbox:** `https://khanhtnq.github.io/anna-ai-ops-sentinel/` (`docs/index.html`)
- **Demo Video:** `assets/demo_anna_1080p.mp4` (40 seconds, 1920x1080 Full HD, 30 fps)
- **Cover Thumbnail:** `assets/thumbnail_1280x800.png` (1280x800)
- **License:** MIT License

---

## `< 60s` Judge Quickstart

1. **Interactive Live Demo (Browser):** Open `https://khanhtnq.github.io/anna-ai-ops-sentinel/`
   - **Invariant Sandbox Tab (default):** Load presets (`Nominal DAG`, `Break RULE-INV-001`, `Break RULE-CAUSAL-002`, `Break RULE-PERF-003`) or customize call chains, action types, confidence sliders, and CU/latency inputs to compute real browser SHA-256 receipts in sub-millisecond evaluation time.
   - **Executa JSON-RPC Tab:** Simulate `describe`, `health`, and `invoke` frames (`verify_agent_pipeline`, `orchestrate_colleagues`) with verbatim `_display` output.
   - **Decision Gates & Colleague Mesh Tabs:** Test human-in-the-loop gate approval/rejection and multi-agent workflow dispatch.
2. **Local Automated Verification:**
   ```bash
   pytest -v
   python benchmarks/benchmark_suite.py
   ```

---

## 1. Executive Summary & Problem Solved

Modern AI agent architectures face a severe **coordination bottleneck**:
1. **The Copy-Paste Router Trap:** Users switch between isolated chat threads, document editors, and browser tabs, manually shuttling intermediate context.
2. **Brittle Workflow Graphs:** Traditional agent builders rely on rigid node graphs that fail when dynamic reasoning or unexpected conditions arise.
3. **Uncontrolled High-Impact Actions:** Autonomous agents dispatched with database write, API dispatch, or transaction capabilities lack mathematical invariant verification, risking hallucinated actions or infinite recursion loops.

**AnnaOps** solves this inside **Anna OS**:
- **Humans set the outcome; Anna coordinates specialized AI colleagues** (Market Intel, Content & Social, Outbound Growth, Support & Admin, Verification SRE).
- Built-in **Causis Research Invariant Verification Engine** enforces acyclic delegation (`RULE-INV-001`), counterfactual confidence gates (`RULE-CAUSAL-002`), and compute/latency ceilings (`RULE-PERF-003`) with sub-millisecond overhead.
- **Human-in-the-Loop Decision Gates** pause high-risk operations (`TRANSACT`, `EXTERNAL_DISPATCH`, or `WRITE` below confidence thresholds) for operator confirmation and immutable SHA-256 receipt logging.

---

## 2. Technical Architecture & Anna OS Native Integration

```text
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
|  - describe: Exposes 4 tools, schema, and runtime metadata                        |
|  - invoke: Executes verify_agent_pipeline, orchestrate_colleagues,                |
|            audit_decision_gate, export_audit_receipt                              |
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
- **Long-Running Daemon:** Persistent loop reading `stdin`, flushing `stdout` after each frame, exiting cleanly on EOF.
- **Display Blocks (`_display`):** Declares presentation-critical markdown blocks rendered verbatim by Anna Chat UI.

### Anna App Manifest Schema 4 (`anna.manifest.json`):
- Compliant with **Schema 4** (`extra="forbid"` — zero retired `permissions` or `host_capabilities` keys).
- `required_executas`: Declares `tool-anna-ops-verification` (`version: "1.0.0"`).
- `storage.scopes`: Explicit `user: rw` declaration.
- `ui.bundle`: Format `static-spa`, entry `index.html`.
- `ui.views`: 3 responsive views within strict small-screen baselines (`min_size.h <= 600`, `min_size.w <= 1024`), wired with hash routing in `index.html`:
  1. `main` (`default: true`, `1024x680`, `index.html`)
  2. `verification_gate` (`800x580`, `index.html#gate`)
  3. `colleague_mesh` (`900x600`, `index.html#mesh`)
- `form_factors`: `["desktop", "mobile"]`.
- `browser_permissions`: `["fullscreen", "clipboard-read"]`.

---

## 3. Core Invariant Safety Rules & Real Benchmark Metrics

1. **`RULE-INV-001` (Acyclic Delegation Guard — CRITICAL):** Guarantees agent-to-agent delegation forms a strict DAG (`research -> content -> verification`). Any circular re-invocation (e.g. `research -> outbound -> research`) is intercepted before CU exhaustion.
2. **`RULE-CAUSAL-002` (Counterfactual Safety Gate — HIGH):** Validates `WRITE`, `TRANSACT`, and `EXTERNAL_DISPATCH` actions against a `0.85` confidence floor (or explicit `human_reviewed: true`) in `VerificationEngine`, paired with a `0.88` auto-approval threshold and mandatory review for `TRANSACT`/`EXTERNAL_DISPATCH` in `DecisionGate`.
3. **`RULE-PERF-003` (CU & Latency Budget Envelope — MEDIUM):** Enforces `<= 150.0 CU` and `<= 6,000.0 ms` limits per workflow, reconciling both `cu_consumed` and orchestrator `total_cu`.

### Benchmark Results (`python benchmarks/benchmark_suite.py` — 2,000 Traces):
- **Detection Accuracy:** `100.0%` (`2,000 / 2,000` traces across nominal DAG, cycle attacks, counterfactual low-confidence transactions, and budget exhaustion)
- **Mean Per-Trace Overhead:** `0.0658 ms` (`0.0202 ms` P50, `1.0658 ms` P99)
- **Throughput:** `12,003.6 traces/sec`
- **SHA-256 Receipt Integrity:** `100.0%` valid 64-char hex digests

---

## 4. Verification & Unit Test Suite

```bash
pytest -v
# or
python run_tests.py
```

- `test_executa_protocol.py`: stdio JSON-RPC 2.0 `describe` (including repo `homepage`), `health`, `invoke` (`verify_agent_pipeline`, `orchestrate_colleagues`, `audit_decision_gate`), unknown method `-32601`, and `_display` blocks.
- `test_verification_engine.py`: Acyclic delegation, cycle detection, counterfactual intervention, `cu_consumed` + `total_cu` budget breaches, and SHA-256 receipts.
- `test_colleague_orchestrator.py`: Multi-role task dispatch, task counters, and CU aggregation.
- `test_decision_gate.py`: Auto-approval heuristics, pending gate creation, and human approval/rejection lifecycle.
- `test_manifest_schema.py`: Schema 4 versioning, forbidden legacy keys, UI view constraints, and system prompt bounds.

**Result:** `25/25 Tests Passed (100.0%)`.

---

## 5. DoraHacks Traction & Growth Roadmap (Path to 200+ MAU)

The DoraHacks Anna AI App Builder Program rewards builder traction with recurring monthly grants scaling from $1,000/mo (at 200 Qualified MAU) up to $15,000+/mo (Tier 3).

- **Phase 1 (Week 1–2):** Alpha Launch on Anna Marketplace; onboard developer DAOs and Solana AI builders.
- **Phase 2 (Week 3–4):** Integrate with automated community SRE & bounty verification workflows to cross **200 Qualified MAU** (Tier 1 Grant: $1,000/mo).
- **Phase 3 (Month 2):** Expand to multi-tenant organization SRE monitoring, scaling toward Tier 2 (1,000 MAU / $5,000/mo).

---

## 6. Submission Checklist & Deliverable Index

- [x] Full source code under `src/` and `executas/anna_ops_executa.py`
- [x] Schema 4 Anna App Manifest (`anna.manifest.json`)
- [x] Interactive Dashboard SPA & Invariant Sandbox (`ui/index.html` and `docs/index.html`)
- [x] Full Unit & JSON-RPC Test Suite (`tests/` and `run_tests.py`) — `25/25 PASS (100%)`
- [x] 2,000-Trace Benchmark Suite (`benchmarks/benchmark_suite.py`)
- [x] 40-second 1080p 30fps Demo Video (`assets/demo_anna_1080p.mp4`) & 1280x800 Thumbnail (`assets/thumbnail_1280x800.png`)
- [x] Zero Local Path Leaks & MIT Open Source License (`LICENSE`)
