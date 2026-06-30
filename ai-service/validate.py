import os
import json
from typing import Dict
import pandas as pd


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


DEFAULT_RULES = {
    "null_transaction_id": lambda df: df["transaction_id"].isnull(),
    "negative_amount": lambda df: df["amount"] < 0,
    "invalid_timestamp": lambda df: pd.to_datetime(
        df["timestamp"], errors="coerce"
    ).isna(),
}


def validate_bronze(bronze_parquet: str, silver_dir: str) -> Dict[str, str]:
    _ensure_dir(silver_dir)
    df = pd.read_parquet(bronze_parquet)

    rules = DEFAULT_RULES
    mask = pd.Series(False, index=df.index)
    failed_reasons = {}
    for name, fn in rules.items():
        reason_mask = fn(df)
        mask = mask | reason_mask
        failed_reasons[name] = int(reason_mask.sum())

    invalid = df[mask].copy()
    valid = df[~mask].copy()

    valid_path = os.path.join(silver_dir, "valid_transactions.parquet")
    invalid_path = os.path.join(silver_dir, "invalid_transactions.parquet")

    valid.to_parquet(valid_path, index=False)
    invalid.to_parquet(invalid_path, index=False)

    metrics = {
        "total_rows": len(df),
        "valid_rows": len(valid),
        "invalid_rows": len(invalid),
        "invalid_by_rule": failed_reasons,
    }

    with open(os.path.join(silver_dir, "dq_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return {
        "valid": valid_path,
        "invalid": invalid_path,
        "metrics": os.path.join(silver_dir, "dq_metrics.json"),
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("bronze")
    p.add_argument("--silver", default="data/silver")
    args = p.parse_args()
    print(validate_bronze(args.bronze, args.silver))
