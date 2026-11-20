import json
import os
import time
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: COINGECKO_API_KEY tidak ditemukan di .env")

BASE_URL = "https://api.coingecko.com/api/v3"
COINS = ["bitcoin", "ethereum", "solana"]
RAW_DIR = Path("data/raw/coingecko")



def fetch_market_chart(coin_id):
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 365}
    headers = {"x-cg-demo-api-key": API_KEY}

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()



def save_raw_snapshot(coin_id, data):
    out_dir = RAW_DIR / coin_id
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{date.today().isoformat()}.json"
    with open(out_path, "w") as f:
        json.dump(data, f)

    return out_path



def main():
    for i, coin_id in enumerate(COINS):
        if i > 0:
            time.sleep(2)

        data = fetch_market_chart(coin_id)
        path = save_raw_snapshot(coin_id, data)
        print(f"[OK] {coin_id}: {len(data['prices'])} titik -> {path}")


if __name__ == "__main__":
    main()
