import json
import os
import time
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FRED_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: FRED_API_KEY tidak ditemukan di .env")

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES = ["DGS10", "DFF", "VIXCLS", "CPIAUCSL", "UNRATE"]
LOOKBACK_DAYS = 730
RAW_DIR = Path("data/raw/fred")



def fetch_series(series_id):
    start = date.today() - timedelta(days=LOOKBACK_DAYS)
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start.isoformat(),
        "realtime_start": start.isoformat(),
        "realtime_end": "9999-12-31",
        "output_type": 4,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)        
    if response.status_code != 200:
        message = response.json().get("error_message", "unknown error")
        raise SystemExit(f"ERROR FRED {series_id}: HTTP {response.status_code} - {message}")
    return response.json()



def save_raw_snapshot(series_id, data):
    out_dir = RAW_DIR / series_id
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{date.today().isoformat()}.json"
    with open(out_path, "w") as f:
        json.dump(data, f)

    return out_path


def main():
    for i, series_id in enumerate(SERIES):
        if i > 0:
            time.sleep(1)

        data = fetch_series(series_id)
        path = save_raw_snapshot(series_id, data)
        print(f"[OK] {series_id}: {len(data['observations'])} observasi -> {path}")


if __name__ == "__main__":
    main()
