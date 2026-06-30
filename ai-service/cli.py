"""Simple CLI to run pipeline stages locally for testing/demo."""

import argparse
from pathlib import Path

from ai_service import ingest, validate, anomaly, genai, agent


def run_all(sample_csv: str):
    bronze = "data/bronze"
    silver = "data/silver"
    gold = "data/gold"
    agent_out = "data/agent"

    bpath = ingest.ingest_csv_to_bronze(sample_csv, bronze)
    res = validate.validate_bronze(bpath, silver)
    gpath = anomaly.add_anomaly_scores(res["valid"], gold)

    # prepare metrics for agent
    import json

    with open(res["metrics"], "r", encoding="utf-8") as f:
        metrics = json.load(f)
    # add anomalies count if available from anomaly output
    try:
        with open(gpath + ".meta.json", "r", encoding="utf-8") as f:
            meta = json.load(f)
            metrics["anomalies"] = meta.get("anomalies")
    except Exception:
        metrics["anomalies"] = 0

    metrics["run_at"] = "now"
    metrics["__out_dir"] = agent_out

    a = agent.default_agent_setup()
    decisions = a.evaluate(metrics)

    prompt = genai.build_genai_prompt(res["metrics"], [])
    summary = genai.simulate_llm_response(prompt)

    print("Decisions:", decisions)
    print("GenAI Summary:\n", summary)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="path to sample CSV to ingest")
    args = p.parse_args()
    run_all(args.csv)


if __name__ == "__main__":
    main()
