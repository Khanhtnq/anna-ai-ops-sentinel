# AnnaOps — Autonomous Multi-Agent Operations & Verification Hub

> **DoraHacks Anna AI App Builder Program Submission** ($6,000 Initial BUIDL Pool / $80,000 Monthly Grant Pool)  
> *Autonomous multi-agent colleague orchestration, Causis Research invariant checking, and human-in-the-loop decision gating for Anna OS.*

- **Live Interactive Demo & Invariant Sandbox:** https://khanhtnq.github.io/anna-ai-ops-sentinel/
- **Repository:** https://github.com/Khanhtnq/anna-ai-ops-sentinel
- **YouTube Demo Video (1080p Narrated):** [https://youtu.be/eZOwxTcMM4A](https://youtu.be/eZOwxTcMM4A) ([Watch on YouTube](https://www.youtube.com/watch?v=eZOwxTcMM4A))
- **Demo Video:** [`assets/demo_anna_1080p.mp4`](assets/demo_anna_1080p.mp4) (40s, 1920x1080 Full HD, 30 fps) | [Hosted MP4](https://khanhtnq.github.io/anna-ai-ops-sentinel/demo_anna_1080p.mp4)

---

## ⚡ `< 60s` Judge Quickstart

Verify everything locally or in the browser in under 60 seconds:

1. **Try the Live Interactive Invariant Sandbox (Zero Install):**
   Open **https://khanhtnq.github.io/anna-ai-ops-sentinel/** — test `RULE-INV-001` (cycle injection), `RULE-CAUSAL-002` (counterfactual confidence gate), and `RULE-PERF-003` (CU/latency ceiling) with live browser `crypto.subtle` SHA-256 receipt signing, Colleague Mesh dispatch, and Executa JSON-RPC 2.0 simulation.

2. **Run Full Test Suite (Unit + JSON-RPC 2.0 Stdio + Schema 4 Validation):**
   ```bash
   pytest -v
   # or: python run_tests.py
   ```
   Expected result: `25 passed (100%)` covering `VerificationEngine`, `ColleagueOrchestrator`, `DecisionGate`, `anna.manifest.json` Schema 4, and live `subprocess` stdio JSON-RPC 2.0 `describe` / `health` / `invoke` frames.

3. **Run the 2,000-Trace Invariant Benchmark:**
   ```bash
   python benchmarks/benchmark_suite.py
   ```

4. **Test the Anna Executa Plugin over `stdio` (JSON-RPC 2.0 v1.1):**
   ```bash
   echo '{"jsonrpc":"2.0","method":"describe","id":1}' | python executas/anna_ops_executa.py
   ```

---

## 📊 Measured Benchmark Metrics

Executed via [`benchmarks/benchmark_suite.py`](benchmarks/benchmark_suite.py) across **2,000 traces** (nominal DAGs, cyclic delegations, low-confidence high-impact counterfactual writes/transactions, and CU/latency envelope breaches):

| Metric | Measured Result |
|---|---|
| **Invariant Detection Accuracy** | **100.0%** (`2,000 / 2,000` traces classified accurately) |
| **Mean Verification Overhead** | **0.0658 ms** (sub-millisecond) |
| **Median (P50) Overhead** | **0.0202 ms** |
| **P99 Verification Overhead** | **1.0658 ms** |
| **Verification Throughput** | **12,003.6 traces/sec** |
| **SHA-256 Receipt Integrity** | **100.0%** valid 64-char hex SHA-256 tamper-evident digests |
| **Automated Test Pass Rate** | **25 / 25 PASSED (100.0%)** |

---

## 🛡️ Causis Research Invariant Rules

| Rule ID | Rule Name | Enforcement Logic | Severity |
|---|---|---|---|
| `RULE-INV-001` | Acyclic Delegation Guard | Enforces strict DAG topology; intercepts and halts circular delegation loops (e.g. `research -> outbound -> research`) | CRITICAL |
| `RULE-CAUSAL-002` | Counterfactual Safety Gate | Requires confidence `>= 0.85` (or explicit `human_reviewed`) before committing `WRITE`, `TRANSACT`, or `EXTERNAL_DISPATCH`; `DecisionGate` enforces `>= 0.88` auto-approve floor | HIGH |
| `RULE-PERF-003` | CU & Latency Budget Envelope | Enforces `<= 150.0` CU and `<= 6,000.0 ms` latency boundaries per workflow (supports both `cu_consumed` and orchestrator `total_cu`) | MEDIUM |

---

## 🌟 Anna OS Native Integration Highlights

- **Anna App Manifest Schema 4 ([`anna.manifest.json`](anna.manifest.json)):** Validated against `AppManifest` (`extra="forbid"`), zero retired fields (`permissions`, `host_capabilities`), declares `required_executas` (`tool-anna-ops-verification` v1.0.0), `storage.scopes` (`user: rw`), `static-spa` bundle, 3 responsive views (`main`, `verification_gate`, `colleague_mesh` with `#gate` / `#mesh` hash routing), and desktop/mobile form factors.
- **Anna Executa Protocol v1.1 ([`executas/anna_ops_executa.py`](executas/anna_ops_executa.py)):** Line-delimited JSON-RPC 2.0 over `stdin`/`stdout` (logs isolated to `stderr`), persistent daemon loop exiting cleanly on EOF, and verbatim `_display` markdown blocks for Anna Chat UI.
- **Coordinated Colleague Mesh ([`src/colleague_orchestrator.py`](src/colleague_orchestrator.py)):** Orchestrates 5 specialized colleagues (`research`, `content`, `outbound`, `support`, `verification`) with automatic CU metering and invariant verification.
- **Human-in-the-Loop Decision Gates ([`src/decision_gate.py`](src/decision_gate.py)):** Intercepts low-confidence or financial/external actions and logs immutable SHA-256 receipts on operator approval/rejection.

---

## 📁 Repository Structure

```text
anna_ai_buidl_6k/
├── anna.manifest.json              # Schema 4 Anna OS App Manifest
├── DORAHACKS_ANNA_SUBMISSION.md    # Complete DoraHacks BUIDL submission & field guide
├── LICENSE                         # MIT License
├── README.md                       # Judge quickstart, benchmarks, architecture
├── pytest.ini                      # Pytest path & discovery config
├── run_tests.py                    # Unittest runner (25/25 pass)
├── assets/
│   ├── demo_anna_1080p.mp4         # 40s 1920x1080 30fps Full HD demo video
│   └── thumbnail_1280x800.png      # DoraHacks BUIDL cover thumbnail
├── benchmarks/
│   └── benchmark_suite.py          # 2,000-trace accuracy & latency benchmark
├── docs/
│   ├── index.html                  # GitHub Pages live SPA + Invariant Sandbox
│   ├── demo_anna_1080p.mp4
│   └── thumbnail_1280x800.png
├── ui/
│   └── index.html                  # Anna App SPA iframe bundle entry (synced)
├── executas/
│   └── anna_ops_executa.py         # JSON-RPC 2.0 stdio Executa plugin v1.1
├── src/
│   ├── colleague_orchestrator.py   # Multi-agent team coordination logic
│   ├── decision_gate.py            # Human-in-the-loop gate & SHA-256 ledger
│   └── verification_engine.py      # Causis invariant rules & receipt hashing
└── tests/
    ├── test_colleague_orchestrator.py
    ├── test_decision_gate.py
    ├── test_executa_protocol.py
    ├── test_manifest_schema.py
    └── test_verification_engine.py
```

---

## 📜 License

Distributed under the [MIT License](LICENSE).
