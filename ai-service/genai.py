import os
import json
import random
from typing import List


def build_genai_prompt(metrics_path: str, sample_anomalies: List[dict]) -> str:
    """Construct a structured prompt for an LLM using aggregated metrics and samples.

    This function does NOT send data to an LLM; it returns a sanitized prompt string.
    """
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    parts = [
        "You are a data-platform assistant. Provide a concise daily summary.",
        f"Total rows: {metrics.get('total_rows')}",
        f"Invalid rows: {metrics.get('invalid_rows')} ({metrics.get('invalid_rows')/metrics.get('total_rows'):.2%} if available)",
        f"Anomalies detected: {metrics.get('anomalies') if 'anomalies' in metrics else 'unknown'}",
        "Provide: 1) short summary 2) top suspected reasons 3) recommended next steps",
    ]

    if sample_anomalies:
        parts.append("Sample anomalies (sanitized):")
        for s in sample_anomalies[:5]:
            parts.append(f"- transaction_id={s.get('transaction_id')} amount={s.get('amount')}")

    prompt = "\n".join(parts)
    return prompt


def simulate_llm_response(prompt: str) -> str:
    # Very small deterministic-ish fake response for testing/demo
    choices = [
        "Store 102 shows 34% higher anomaly rate than average. Investigate store's POS configuration.",
        "12% of records failed timestamp validation. Suggest re-processing the ingestion with timezone parsing.",
        "High duplicate rate — run deduplication and notify upstream provider.",
    ]
    return random.choice(choices) + "\n\nPrompt summary:\n" + prompt[:400]


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("metrics")
    args = p.parse_args()
    print(build_genai_prompt(args.metrics, []))
