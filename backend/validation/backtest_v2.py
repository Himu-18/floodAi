# validation/backtest_v2.py
# ============================================================
# FloodAI Validation — Phase 1 Backtest (advisor-এর methodology অনুযায়ী)
# ============================================================
# ⚠️ এই script network access লাগে (Open-Meteo historical archive) —
# Claude-এর sandbox-এ flood-api.open-meteo.com/archive-api.open-meteo.com
# allowlist-এ নেই, তাই এটা লোকাল মেশিনে (VS Code) চালাতে হবে।
#
# Target (advisor-এর সংজ্ঞা অনুযায়ী):
#   "আগামী N ঘণ্টায় একটি station-এর water level danger level cross করবে কি না?"
#
# পদ্ধতি: প্রতিটা validation station-এর জন্য, প্রতিটা major flood-year
# event-এর period-এ কিছু sample তারিখ নিয়ে (event শুরুর ৭ দিন আগে থেকে
# event শেষ পর্যন্ত), সেই দিনের real historical rainfall/discharge/soil-moisture
# আনা হয়, current predict_flood() model ও simple danger-level baseline
# দুটো দিয়েই "flood হবে" prediction নেওয়া হয়, তারপর actual_flood label
# (DFO/flood_events.csv অনুযায়ী, সেই তারিখ কোনো known flood period-এর
# মধ্যে পড়ে কিনা) এর সাথে তুলনা করে metrics বের করা হয়।
#
# ⚠️ সীমাবদ্ধতা (honestly স্বীকার করা প্রয়োজন):
# - এটা true lead-time forecast backtest না (২০২১-পূর্ববর্তী ঘটনার জন্য
#   "সেই সময় forecast কী বলেছিল" এই ঐতিহাসিক তথ্য Open-Meteo দেয় না,
#   শুধু reanalysis/observed data দেয়) — তাই এটা classification accuracy
#   (Precision/Recall/F1/FAR/Miss-rate) মাপে, lead-time না।
# - actual_flood label station-level না, event-level (পুরো দেশের flood
#   period অনুযায়ী) — station-নির্দিষ্ট প্রকৃত local flooding হয়েছিল
#   কিনা যাচাই করার জন্য আরও নির্ভুল সোর্স (FFWC historical bulletin)
#   ভবিষ্যতে যোগ করা উচিত।

import csv
import sys
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))  # backend/ folder থেকে import করার জন্য

from stations import VALIDATION_STATIONS
from metrics import PredictionRecord, compute_metrics, compare_models

from model import predict_flood, get_reference_discharge

OUTPUT_CSV = Path(__file__).parent / "backtest_v2_results.csv"

# stations.py (বাংলা জেলা নাম) কে ground_truth.csv (v3/v6, ইংরেজি জেলা নাম)
# এর সাথে মেলানোর জন্য mapping — শুধু এই ১২ station-এর জেলাগুলোই যথেষ্ট
DISTRICT_BN_TO_EN = {
    "জামালপুর": "Jamalpur", "মানিকগঞ্জ": "Manikganj", "সিরাজগঞ্জ": "Sirajganj",
    "রাজবাড়ী": "Rajbari", "পাবনা": "Pabna", "শরীয়তপুর": "Shariatpur",
    "কুড়িগ্রাম": "Kurigram", "গাইবান্ধা": "Gaibandha", "রংপুর": "Rangpur",
}


def fetch_historical_rain(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "precipitation_sum"},
            timeout=15
        )
        data = r.json()
        val = data.get("daily", {}).get("precipitation_sum", [None])[0]
        return float(val) if val is not None else 0.0
    except Exception as e:
        print(f"  ⚠️ rain fetch error ({date_str}): {e}")
        return 0.0


def fetch_historical_discharge(lat, lon, date_str):
    try:
        r = requests.get(
            "https://flood-api.open-meteo.com/v1/flood",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "river_discharge"},
            timeout=15
        )
        data = r.json()
        val = data.get("daily", {}).get("river_discharge", [None])[0]
        return float(val) if val is not None else 0.0
    except Exception as e:
        print(f"  ⚠️ discharge fetch error ({date_str}): {e}")
        return 0.0


def fetch_historical_soil_moisture(lat, lon, date_str):
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={"latitude": lat, "longitude": lon, "start_date": date_str, "end_date": date_str,
                    "daily": "soil_moisture_0_to_7cm_mean"},
            timeout=15
        )
        data = r.json()
        val = data.get("daily", {}).get("soil_moisture_0_to_7cm_mean", [None])[0]
        return float(val) if val is not None else 0.6
    except Exception:
        return 0.6


def load_flood_events():
    events = []
    with open(Path(__file__).parent / "flood_events.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            events.append(row)
    return events


def load_ground_truth():
    """
    build_ground_truth.py-র output — v3 (station-level, ১৯৯৮/২০১২) ও v6
    (district-level, ২০১৭/২০২০) থেকে আসা real, নির্ভুল ground-truth।
    এটা পাওয়া গেলে flood_events.csv-এর মোটা দাগের জাতীয় date-range
    অনুমানের চেয়ে অগ্রাধিকার পাবে (নিচের actual_flood_label() দেখুন)।

    ⚠️ FIX: শুধু (year, district) দিয়ে key করলে multi-station জেলায়
    (যেমন জামালপুর — Bahadurabad ও Jamalpur town আলাদা নদীতে, একই বছরে
    ভিন্ন ফলাফল থাকতে পারে) তথ্য হারিয়ে যায়/ভুল হয়ে যায় (dict-এ পরের
    row আগেরটাকে overwrite করে ফেলে)। তাই এখন দুটো আলাদা lookup রাখা
    হচ্ছে: (ক) station-নির্দিষ্ট (সবচেয়ে নির্ভুল), (খ) district-level
    aggregate (কোনো একটা station-এ বন্যা হলেই "হ্যাঁ", fallback হিসেবে)।
    """
    path = Path(__file__).parent / "ground_truth.csv"
    by_station, by_district = {}, {}
    if not path.exists():
        print("⚠️ ground_truth.csv পাওয়া যায়নি (আগে build_ground_truth.py চালান) — "
              "শুধু flood_events.csv-এর জাতীয় date-range অনুমান দিয়ে চলবে।")
        return by_station, by_district
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            year = int(row["year"])
            flood = int(row["flood_occurred"])
            if row["station"]:
                by_station[(year, row["station"].strip().lower())] = flood
            dkey = (year, row["district"])
            by_district[dkey] = max(by_district.get(dkey, 0), flood)  # any station flooded -> district flooded
    return by_station, by_district


def actual_flood_label(date_obj, district_name, station_name, events, ground_truth):
    """
    অগ্রাধিকার-ক্রম: (১) সঠিক station-নির্দিষ্ট real observation
    (সবচেয়ে নির্ভুল), (২) district-level aggregate real observation,
    (৩) flood_events.csv-এর মোটা দাগের জাতীয় date-range অনুমান (fallback,
    কম নির্ভুল কিন্তু কভারেজ বেশি)।
    """
    by_station, by_district = ground_truth
    year = date_obj.year

    station_key = (year, station_name.strip().lower())
    if station_key in by_station:
        return bool(by_station[station_key])

    district_key = (year, district_name)
    if district_key in by_district:
        return bool(by_district[district_key])

    return date_in_any_flood_event(date_obj, events)


def date_in_any_flood_event(date_obj, events):
    for ev in events:
        start = datetime.strptime(ev["start_date"], "%Y-%m-%d")
        end = datetime.strptime(ev["end_date"], "%Y-%m-%d")
        if start <= date_obj <= end:
            return True
    return False


def sample_dates_for_event(event, days_before=7, step_days=3):
    """event period-এর কয়েকদিন আগে থেকে শেষ পর্যন্ত, প্রতি step_days দিনে একটা করে sample তারিখ।"""
    start = datetime.strptime(event["start_date"], "%Y-%m-%d") - timedelta(days=days_before)
    end = datetime.strptime(event["end_date"], "%Y-%m-%d")
    dates = []
    d = start
    while d <= end:
        dates.append(d)
        d += timedelta(days=step_days)
    return dates


def run_backtest():
    events = load_flood_events()
    ground_truth = load_ground_truth()
    floodai_records = []
    baseline_records = []
    rows_out = []

    for station in VALIDATION_STATIONS:
        print(f"\n=== {station['name']} ({station['river']}) ===")
        for event in events:
            dates = sample_dates_for_event(event)
            for date_obj in dates:
                date_str = date_obj.strftime("%Y-%m-%d")
                rain = fetch_historical_rain(station["lat"], station["lon"], date_str)
                discharge = fetch_historical_discharge(station["lat"], station["lon"], date_str)
                soil = fetch_historical_soil_moisture(station["lat"], station["lon"], date_str)
                time.sleep(0.5)  # rate-limit সৌজন্যে

                actual_flood = actual_flood_label(
                    date_obj, DISTRICT_BN_TO_EN.get(station["district"], station["district"]),
                    station["name"], events, ground_truth
                )

                try:
                    pred = predict_flood(
                        discharge=discharge, upstream_rain=rain * 0.7, local_rain=rain,
                        soil_moisture=soil, lag_time=20, cn=80, risk_category="মাঝারি",
                        district_name=station["district"], danger_level=station["danger_level_m"],
                        month=date_obj.month,  # ⚠️ historical তারিখের আসল মাস — না দিলে predict_flood()
                                                # ডিফল্টে আজকের (রান করার সময়ের) মাস ধরে নিত, যেটা
                                                # ঐতিহাসিক backtest-এর জন্য ভুল হতো
                    )
                    predicted_flood = pred.get("probability", 0) >= 50
                    predicted_prob = pred.get("probability", 0)
                except Exception as e:
                    print(f"  ⚠️ predict_flood error: {e}")
                    predicted_flood, predicted_prob = False, None

                # ⚠️ FIX: প্রথম ভার্সনে ভুলবশত danger_level (মিটার) দিয়ে
                # discharge (m³/s)-এর সাথে তুলনা করার চেষ্টা করা হয়েছিল —
                # ঠিক সেই একই unit-mismatch bug যেটা এই প্রজেক্টেই আগে
                # সুনামগঞ্জে পাওয়া গিয়েছিল। এখানে সেটা এড়াতে discharge-কে
                # station-এর নিজস্ব reference_discharge_m3s (bankfull, একই
                # unit) এর সাথে তুলনা করা হচ্ছে — এটাই সবচেয়ে সরল,
                # unit-consistent baseline: "discharge >= bankfull হলেই flood"।
                reference_discharge = get_reference_discharge(station["danger_level_m"], station["district"])
                baseline_flood = bool(reference_discharge) and discharge >= reference_discharge

                floodai_records.append(PredictionRecord(station["name"], date_str, predicted_flood, actual_flood))
                baseline_records.append(PredictionRecord(station["name"], date_str, baseline_flood, actual_flood))

                rows_out.append({
                    "station": station["name"], "date": date_str, "event_year": event["event_year"],
                    "rain_mm": rain, "discharge_m3s": discharge, "soil_moisture": soil,
                    "predicted_probability": predicted_prob, "predicted_flood": predicted_flood,
                    "baseline_flood": baseline_flood, "actual_flood": actual_flood,
                })
                print(f"  {date_str}: rain={rain}mm discharge={discharge}m³/s -> "
                      f"FloodAI={predicted_flood}({predicted_prob}%) baseline={baseline_flood} actual={actual_flood}")

    # ফলাফল CSV-তে সেভ
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"\n✅ ফলাফল সেভ হয়েছে: {OUTPUT_CSV}")

    # মেট্রিক প্রিন্ট
    comparison = compare_models(baseline_records, floodai_records)
    print("\n=== Danger-Level Baseline ===")
    print(comparison["danger_level_baseline"])
    print("\n=== FloodAI ===")
    print(comparison["floodai"])


if __name__ == "__main__":
    run_backtest()
