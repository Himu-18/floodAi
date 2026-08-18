"""
FloodAI — backtest_dfo.py

DFO (Dartmouth Flood Observatory) archive-এর ঐতিহাসিক বাংলাদেশ বন্যার
ঘটনাগুলোর জন্য Open-Meteo-র historical weather archive থেকে real
ডেটা টেনে এনে, আমাদের আসল predict_flood() মডেল সেই সময় "উচ্চ ঝুঁকি"
বলত কিনা টেস্ট করে — এটাই প্রকৃত back-testing, শুধু frequency/severity
sanity-check না।

⚠️ গুরুত্বপূর্ণ সীমাবদ্ধতা (আগে থেকে জানিয়ে রাখছি):
- soil_moisture এখন real historical archive থেকে আনা হচ্ছে (আগে fixed
  0.6 ছিল, সেটা ঠিক করা হয়েছে)। fetch ব্যর্থ হলে 0.6-এ fallback করে।
- discharge historical archive Open-Meteo-র flood API সাপোর্ট করে,
  কিন্তু পুরনো তারিখে (১৯৮৫-এর মতো) মাঝেমধ্যে কভারেজ না থাকলে None/０
  দেয় — সেই ক্ষেত্রে discharge=0 ধরা হয় (এটা probability-কে কমই দেখাবে,
  বাড়াবে না, তাই hit-rate ভালো এলে সেটা জোরালো সংকেত)।
- confluence_data, rainfall_intensity_data, upstream_rain_history —
  এই নতুন multi-day feature গুলো এই simple back-test-এ যুক্ত করা হয়নি,
  শুধু single-day base scoring টেস্ট হচ্ছে।
- ~১০৪টা event x ৪টা করে API call, তাই সময় লাগবে।

🔧 এই ভার্সনে দুটো ফিক্স:
1. Bangladesh filter — আগে শুধু Country == "Bangladesh" (strict, ৮৯টা
   event) ছিল, এখন Country বা OtherCountry-তে Bangladesh থাকলেই ধরা
   হচ্ছে (loose, ১০৪টা event) — এতে সীমান্ত-সংলগ্ন আঞ্চলিক বন্যাও (যেখানে
   বাংলাদেশ secondary affected country ছিল) অন্তর্ভুক্ত হয়, আগের
   district-matching বিশ্লেষণের সাথেও consistent থাকে।
2. None-handling — Open-Meteo পুরনো তারিখে প্রায়ই [None] রিটার্ন করে
   (খালি লিস্ট না, কিন্তু ভেতরের মান None) — আগে এটা সরাসরি predict_flood()-এ
   গিয়ে TypeError দিয়ে crash করাতো, এখন আলাদাভাবে None-চেক করে 0-এ
   fallback করে।

ব্যবহার:
    py backend/backtest_dfo.py        (রুট থেকে)
    py backtest_dfo.py                (backend/ ফোল্ডারের ভেতর থেকে)
    (floodarchive.xlsx ফাইলটা backend/ ফোল্ডারে থাকতে হবে, backtest_dfo.py-র পাশে)
"""

import sys
import time
import csv
import math
import requests
from datetime import datetime
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("❌ openpyxl নেই। ইনস্টল করো: py -m pip install openpyxl")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from model import predict_flood
from data.districts_base import DISTRICTS_BASE
from data.flood_config import FLOOD_CONFIG
from data.upstream_cities import get_upstream_coords

DISTRICTS = {name: {**base, **FLOOD_CONFIG.get(name, {})} for name, base in DISTRICTS_BASE.items()}

XLSX_PATH = BASE_DIR / "floodarchive.xlsx"
OUT_PATH = BASE_DIR / "backtest_results.csv"
REQUEST_DELAY = 0.3


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def nearest_district(lat, lon):
    best_name, best_dist = None, float("inf")
    for name, info in DISTRICTS_BASE.items():
        d = haversine(lat, lon, info["lat"], info["lon"])
        if d < best_dist:
            best_dist, best_name = d, name
    return best_name, best_dist


def is_full_moon_on(target_date):
    known_new_moon = datetime(2024, 1, 11)
    days_since = (target_date - known_new_moon).days
    moon_age = days_since % 29.53
    return 13.5 <= moon_age <= 16.5


def fetch_historical_rain(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": lat, "longitude": lon,
                "start_date": date_str, "end_date": date_str,
                "daily": "precipitation_sum",
                "timezone": "auto",
            },
            timeout=10,
        )
        data = r.json()
        values = data.get("daily", {}).get("precipitation_sum", [])
        if values and values[0] is not None:
            return values[0]
        return 0
    except Exception as e:
        print(f"    [rain fetch error] {e}")
        return 0


def fetch_historical_discharge(lat, lon, date_str):
    try:
        r = requests.get(
            "https://flood-api.open-meteo.com/v1/flood",
            params={
                "latitude": lat, "longitude": lon,
                "start_date": date_str, "end_date": date_str,
                "daily": "river_discharge",
            },
            timeout=10,
        )
        data = r.json()
        values = data.get("daily", {}).get("river_discharge", [])
        if values and values[0] is not None:
            return values[0]
        return 0
    except Exception as e:
        print(f"    [discharge fetch error] {e}")
        return 0


def fetch_historical_soil_moisture(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": lat, "longitude": lon,
                "start_date": date_str, "end_date": date_str,
                "hourly": "soil_moisture_0_to_7cm",
                "timezone": "auto",
            },
            timeout=10,
        )
        data = r.json()
        values = data.get("hourly", {}).get("soil_moisture_0_to_7cm", [])
        values = [v for v in values if v is not None]
        if values:
            return round(sum(values) / len(values), 3)
        return 0.6
    except Exception as e:
        print(f"    [soil moisture fetch error] {e}")
        return 0.6


def run_backtest():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb["FloodArchive"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    # loose filter: Country == Bangladesh অথবা OtherCountry-তে Bangladesh —
    # আগের district-matching বিশ্লেষণের সাথে consistent রাখতে
    bd_events = [r for r in rows if r[2] == "Bangladesh" or (r[3] and "Bangladesh" in str(r[3]))]

    results = []
    for i, r in enumerate(bd_events, 1):
        lon, lat, began = r[4], r[5], r[7]
        cause, severity = r[12], r[13]
        district_name, match_km = nearest_district(lat, lon)
        info = DISTRICTS[district_name]
        date_str = began.strftime("%Y-%m-%d")

        print(f"[{i}/{len(bd_events)}] {district_name} ({date_str}) চেক হচ্ছে...")

        local_rain = fetch_historical_rain(info["lat"], info["lon"], date_str)
        time.sleep(REQUEST_DELAY)

        upstream_coords = get_upstream_coords(info.get("upstream"))
        upstream_rain = 0
        if upstream_coords:
            upstream_rain = fetch_historical_rain(upstream_coords[0], upstream_coords[1], date_str)
            time.sleep(REQUEST_DELAY)

        discharge = fetch_historical_discharge(info.get("river_lat", info["lat"]),
                                                 info.get("river_lon", info["lon"]), date_str)
        time.sleep(REQUEST_DELAY)

        soil_moisture = fetch_historical_soil_moisture(info["lat"], info["lon"], date_str)
        time.sleep(REQUEST_DELAY)

        prediction = predict_flood(
            discharge=discharge,
            upstream_rain=upstream_rain or 0,
            local_rain=local_rain or 0,
            soil_moisture=soil_moisture,
            lag_time=info.get("lag_time", 24),
            cn=info.get("cn", 80),
            risk_category=info.get("risk", "মাঝারি"),
            district_name=district_name,
            flood_type=info.get("flood_type", "Riverine"),
            danger_level=info.get("danger_level"),
            month=began.month,
            is_full_moon=is_full_moon_on(began),
        )

        would_flag = prediction["probability"] >= 50
        results.append({
            "district": district_name, "match_km": round(match_km, 1),
            "date": date_str, "dfo_cause": cause, "dfo_severity": severity,
            "local_rain_mm": local_rain, "upstream_rain_mm": upstream_rain,
            "discharge_m3s": round(discharge, 1), "soil_moisture": soil_moisture,
            "model_probability": prediction["probability"],
            "model_level": prediction["level"],
            "would_have_flagged": would_flag,
        })

    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    hits = sum(1 for r in results if r["would_have_flagged"])
    print(f"\n✅ শেষ! মোট {len(results)}টা ঐতিহাসিক বড় বন্যার মধ্যে "
          f"{hits}টাতে ({100*hits/len(results):.1f}%) আমাদের মডেল 'সতর্ক' বা তার বেশি ফ্ল্যাগ করত।")
    print(f"বিস্তারিত রিপোর্ট: {OUT_PATH}")


if __name__ == "__main__":
    run_backtest()