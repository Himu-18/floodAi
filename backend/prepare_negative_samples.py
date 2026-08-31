# backend/prepare_negative_samples.py
# ============================================================
# FloodAI — Real-Data ML Training, ধাপ ১: Negative (স্বাভাবিক দিন) sample
# ============================================================
# backtest_results.csv (backtest_dfo.py-র output)-এর প্রতিটা row-ই একটা
# real DFO-recorded বন্যার ঘটনা — মানে সবগুলোই "flood হয়েছিল" (label=1)
# example। কিন্তু ML train করতে হলে "flood হয়নি" (label=0) example-ও
# লাগবে, নাহলে model শুধু "সবসময় flood" বলতে শিখবে (advisor-এর সতর্কতা
# অনুযায়ী — এটাই "accuracy paradox")।
#
# এই script প্রতিটা flood event-এর জন্য একই জেলার একটা "স্বাভাবিক" তারিখ
# (event-এর ৯০-১৮০ দিন আগে বা পরে, যাতে মৌসুম/event window-এর বাইরে পড়ে)
# বেছে নিয়ে, সেই তারিখের real historical rainfall/discharge/soil-moisture
# এনে negative_samples.csv-এ সেভ করে।
#
# ⚠️ এটাও network access লাগে (Open-Meteo) — লোকালি চালাতে হবে।
# ⚠️ সরলীকৃত অনুমান: event-তারিখ থেকে ৯০-১৮০ দিন দূরে সরালে সেটা flood-মুক্ত
#   সময় হবে বলে ধরে নেওয়া হচ্ছে — এটা সবসময় ১০০% নিশ্চিত না (ঐ জেলায়
#   অন্য কোনো অ-DFO-তালিকাভুক্ত ছোট বন্যা থাকতে পারে), কিন্তু বাস্তবসম্মত
#   একটা approximation।

import csv
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta

BACKTEST_CSV = Path(__file__).parent / "backtest_results.csv"
OUT_PATH = Path(__file__).parent / "negative_samples.csv"
REQUEST_DELAY = 0.3

import sys
sys.path.insert(0, str(Path(__file__).parent))
from data.districts_base import DISTRICTS_BASE
from data.flood_config import FLOOD_CONFIG
DISTRICTS = {name: {**base, **FLOOD_CONFIG.get(name, {})} for name, base in DISTRICTS_BASE.items()}


def fetch_historical_rain(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "precipitation_sum"},
            timeout=15
        )
        val = r.json().get("daily", {}).get("precipitation_sum", [None])[0]
        return round(val, 2) if val is not None else 0.0
    except Exception as e:
        print(f"    [rain fetch error] {e}")
        return 0.0


def fetch_historical_discharge(lat, lon, date_str):
    try:
        r = requests.get(
            "https://flood-api.open-meteo.com/v1/flood",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "river_discharge"},
            timeout=15
        )
        val = r.json().get("daily", {}).get("river_discharge", [None])[0]
        return round(val, 1) if val is not None else 0.0
    except Exception as e:
        print(f"    [discharge fetch error] {e}")
        return 0.0


def fetch_historical_soil_moisture(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "soil_moisture_0_to_7cm_mean"},
            timeout=15
        )
        val = r.json().get("daily", {}).get("soil_moisture_0_to_7cm_mean", [None])[0]
        return round(val, 3) if val is not None else 0.4  # শুকনো মৌসুমের ধারণা, বন্যার সময়ের 0.6 থেকে ইচ্ছাকৃতভাবে কম
    except Exception:
        return 0.4


def pick_normal_date(flood_date: datetime, offset_days: int = 120) -> datetime:
    """
    flood event থেকে offset_days দূরে একটা তারিখ বেছে নেওয়া। আগে-পরে
    দুটোই চেষ্টা করা যায়; এখানে সরলভাবে flood-তারিখের ঠিক বিপরীত
    মৌসুমে (৬ মাস+ দূরে) নেওয়া হচ্ছে, যাতে একই ধরনের মৌসুমি বৃষ্টিপাতের
    প্রভাব এড়ানো যায় (শুষ্ক মৌসুমের real example পাওয়া যায়)।
    """
    return flood_date + timedelta(days=180)


def run():
    if not BACKTEST_CSV.exists():
        print(f"❌ {BACKTEST_CSV} পাওয়া যায়নি — আগে backtest_dfo.py চালান।")
        return

    with open(BACKTEST_CSV, encoding="utf-8-sig") as f:
        flood_rows = list(csv.DictReader(f))

    results = []
    for i, row in enumerate(flood_rows, 1):
        district_name = row["district"]
        info = DISTRICTS.get(district_name)
        if not info:
            continue

        flood_date = datetime.strptime(row["date"], "%Y-%m-%d")
        normal_date = pick_normal_date(flood_date)
        date_str = normal_date.strftime("%Y-%m-%d")

        print(f"[{i}/{len(flood_rows)}] {district_name} — স্বাভাবিক তারিখ {date_str} চেক হচ্ছে...")

        local_rain = fetch_historical_rain(info["lat"], info["lon"], date_str)
        time.sleep(REQUEST_DELAY)
        discharge = fetch_historical_discharge(info.get("river_lat", info["lat"]),
                                                 info.get("river_lon", info["lon"]), date_str)
        time.sleep(REQUEST_DELAY)
        soil_moisture = fetch_historical_soil_moisture(info["lat"], info["lon"], date_str)
        time.sleep(REQUEST_DELAY)

        results.append({
            "district": district_name, "date": date_str,
            "local_rain_mm": local_rain, "upstream_rain_mm": round(local_rain * 0.5, 2),
            "discharge_m3s": discharge, "soil_moisture": soil_moisture,
            "actual_flood": False,
        })

    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ শেষ! {len(results)}টা negative (স্বাভাবিক দিন) sample সেভ হয়েছে: {OUT_PATH}")


if __name__ == "__main__":
    run()
