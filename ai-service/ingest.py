import os
import hashlib
import json
from datetime import datetime
import pandas as pd


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _row_checksum(row: pd.Series) -> str:
    s = row.to_json(date_format="iso")
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def ingest_csv_to_bronze(csv_path: str, bronze_dir: str) -> str:
    """Read a CSV and write raw rows to a bronze parquet + metadata JSON.

    Returns path to written parquet file.
    """
    _ensure_dir(bronze_dir)
    df = pd.read_csv(csv_path)
    # add metadata
    df["_ingest_ts"] = datetime.utcnow().isoformat()
    df["_checksum"] = df.apply(_row_checksum, axis=1)

    out_path = os.path.join(bronze_dir, f"bronze_{os.path.basename(csv_path)}.parquet")
    df.to_parquet(out_path, index=False)

    meta = {
        "source": os.path.abspath(csv_path),
        "rows": len(df),
        "written_at": datetime.utcnow().isoformat(),
    }
    with open(out_path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return out_path


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--bronze", default="data/bronze")
    args = p.parse_args()
    print(ingest_csv_to_bronze(args.csv, args.bronze))
