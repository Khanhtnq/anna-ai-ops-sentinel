#!/usr/bin/env python3
"""
Benchmark suite for AnnaOps VerificationEngine.
Measures detection accuracy, per-trace latency (mean/p50/p99), throughput,
and SHA-256 cryptographic receipt integrity across 2,000 traces.
"""

import json
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.verification_engine import VerificationEngine


def run_benchmark(iterations: int = 2000) -> dict:
    engine = VerificationEngine()
    scenarios = [
        (
            "nominal_dag",
            {
                "call_chain": ["research", "content", "verification"],
                "action_type": "READ",
                "confidence": 0.96,
                "cu_consumed": 18.4,
                "latency_ms": 210.0,
            },
            True,
        ),
        (
            "cycle_attack",
            {
                "call_chain": ["research", "outbound", "research"],
                "action_type": "READ",
                "confidence": 0.95,
                "cu_consumed": 24.0,
                "latency_ms": 340.0,
            },
            False,
        ),
        (
            "causal_low_conf_transact",
            {
                "call_chain": ["research", "outbound"],
                "action_type": "TRANSACT",
                "confidence": 0.72,
                "human_reviewed": False,
                "cu_consumed": 14.0,
                "latency_ms": 180.0,
            },
            False,
        ),
        (
            "budget_exhaustion",
            {
                "call_chain": ["research", "content", "outbound"],
                "action_type": "WRITE",
                "confidence": 0.92,
                "cu_consumed": 185.0,
                "latency_ms": 7200.0,
            },
            False,
        ),
    ]

    latencies_ms = []
    correct = 0
    valid_sha256 = 0

    t_start = time.perf_counter()
    for i in range(iterations):
        label, base_trace, expected_verified = scenarios[i % len(scenarios)]
        trace = dict(base_trace)
        trace["trace_id"] = f"bench-{label}-{i}"

        t0 = time.perf_counter()
        res = engine.verify_pipeline(trace)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(dt_ms)

        if res["verified"] == expected_verified:
            correct += 1
        h = res.get("receipt_hash", "")
        if len(h) == 64 and all(c in "0123456789abcdef" for c in h):
            valid_sha256 += 1

    total_sec = time.perf_counter() - t_start
    latencies_ms.sort()
    n = len(latencies_ms)
    mean_ms = sum(latencies_ms) / n
    p50_ms = latencies_ms[int(n * 0.50)]
    p99_ms = latencies_ms[int(n * 0.99)]

    report = {
        "total_traces": iterations,
        "detection_accuracy_pct": round((correct / iterations) * 100.0, 2),
        "sha256_receipt_valid_pct": round((valid_sha256 / iterations) * 100.0, 2),
        "mean_overhead_ms": round(mean_ms, 4),
        "p50_overhead_ms": round(p50_ms, 4),
        "p99_overhead_ms": round(p99_ms, 4),
        "throughput_traces_per_sec": round(iterations / total_sec, 1),
        "total_wall_sec": round(total_sec, 3),
    }
    return report


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2))
