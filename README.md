# AnnaOps — Autonomous Multi-Agent Operations & Verification Hub

> **DoraHacks Anna AI App Builder Program Submission** ($6,000 Initial BUIDL Pool / $80,000 Monthly Grant Pool)  
> *Autonomous multi-agent colleague orchestration, Causis Research invariant checking, and human-in-the-loop decision gating for Anna OS.*

---

## 🌟 Highlights & Features

- **Coordinated Colleague Mesh:** Dynamic orchestration across specialized agents (Market Intel & Research, Content & Social Strategy, Growth & Outbound, Support & Admin, Invariant SRE).
- **Causis Research Invariant Engine:** Evaluates multi-agent delegation traces with counterfactual safety checks, acyclic execution proofs (DAG), and compute unit (CU) budget enforcement.
- **Human-in-the-Loop Decision Gates:** Automatic diversion of high-impact writes or financial transactions below confidence thresholds to human review before commit.
- **Cryptographic Audit Trail:** SHA-256 tamper-evident receipts for every verification event and decision gate.
- **Anna Executa Protocol v1.1:** Full JSON-RPC 2.0 stdio plugin implementation with verbatim `_display` block formatting.
- **Anna App Manifest Schema 4:** Compliant with official Anna OS app specifications, including bundle definitions and responsive desktop/mobile views.
- **Interactive Standalone UI:** Live dashboard available at `docs/index.html` (and `ui/index.html`).
- **100% Test Pass Rate:** 23/23 unit tests covering protocol, verification logic, orchestration, and schema validation.

---

## 📁 Repository Structure

```
anna_ai_buidl_6k/
├── anna.manifest.json            # Schema 4 Anna OS App Manifest
├── DORAHACKS_ANNA_SUBMISSION.md  # Complete DoraHacks BUIDL documentation
├── LICENSE                       # MIT License
├── README.md                     # Architecture and setup guide
├── run_tests.py                  # Test runner (100% pass rate)
├── assets/
│   └── demo_anna_1080p.mp4       # 40s 1920x1080 30fps Full HD demo video
├── docs/
│   └── index.html                # Standalone & GitHub Pages interactive dashboard
├── ui/
│   └── index.html                # Anna App SPA iframe bundle entry
├── executas/
│   └── anna_ops_executa.py       # JSON-RPC 2.0 stdio Executa plugin v1.1
├── src/
│   ├── colleague_orchestrator.py # Multi-agent team coordination logic
│   ├── decision_gate.py          # Human-in-the-loop gate & ledger
│   └── verification_engine.py    # Causis invariant rules & receipt hashing
└── tests/
    ├── test_colleague_orchestrator.py
    ├── test_decision_gate.py
    ├── test_executa_protocol.py
    ├── test_manifest_schema.py
    └── test_verification_engine.py
```

---

## 🚀 Quickstart & Testing

### 1. Run All Tests
```bash
python run_tests.py
```
Output:
```text
Ran 23 tests in 0.192s
OK
AnnaOps Test Summary: 23/23 Passed (100.0%)
```

### 2. Run Executa Plugin via stdio (JSON-RPC 2.0)
```bash
python executas/anna_ops_executa.py
```
Send a JSON-RPC 2.0 frame on stdin:
```json
{"jsonrpc": "2.0", "method": "describe", "id": 1}
```

### 3. Open Standalone UI Dashboard
Open `docs/index.html` in any modern web browser or serve via GitHub Pages.

---

## 🛡️ Invariant Rules

| Rule ID | Rule Name | Description | Severity |
|---|---|---|---|
| `RULE-INV-001` | Acyclic Delegation Guard | Guarantees DAG topology; intercepts and halts circular delegation loops | CRITICAL |
| `RULE-CAUSAL-002` | Counterfactual Safety Gate | Validates confidence (≥ 88%) on high-impact external actions (WRITE/TRANSACT) | HIGH |
| `RULE-PERF-003` | CU & Latency Budget Envelope | Enforces ≤ 150 CU and ≤ 6,000ms latency boundaries per workflow | MEDIUM |

---

## 📜 License

Distributed under the [MIT License](LICENSE).
