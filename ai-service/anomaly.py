import os
import json
import numpy as np
import pandas as pd


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def add_anomaly_scores(valid_parquet: str, out_dir: str) -> str:
    """Add simple z-score based anomaly_score and is_anomaly columns.

    This function avoids heavy ML deps and provides a simple anomaly detector.
    """
    _ensure_dir(out_dir)
    df = pd.read_parquet(valid_parquet)

    # focus on numeric `amount` field
    if "amount" not in df.columns:
        df["anomaly_score"] = 0.0
        df["is_anomaly"] = False
    else:
        vals = df["amount"].astype(float)
        mu = vals.mean()
        sigma = vals.std(ddof=0) if vals.std(ddof=0) > 0 else 1.0
        z = (vals - mu) / sigma
        score = np.abs(z)
        df["anomaly_score"] = score
        df["is_anomaly"] = score > 3.0

    out_path = os.path.join(out_dir, "silver_with_anomalies.parquet")
    df.to_parquet(out_path, index=False)

    summary = {
        "rows": len(df),
        "anomalies": int(df["is_anomaly"].sum()),
    }
    with open(out_path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return out_path


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("valid")
    p.add_argument("--out", default="data/gold")
    args = p.parse_args()
    print(add_anomaly_scores(args.valid, args.out))
