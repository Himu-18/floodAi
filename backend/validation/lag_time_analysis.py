# validation/lag_time_analysis.py
# ============================================================
# FloodAI — empirical lag_time বিশ্লেষণ (upstream rainfall vs downstream discharge)
# ============================================================
# ⚠️ network লাগে (Open-Meteo historical archive + flood API) — লোকাল মেশিনে চালাতে হবে।
#
# উদ্দেশ্য: flood_config.py-তে প্রতিটা জেলার lag_time (ঘণ্টা) এখন
# distance-based অনুমান (আগে ট্রাই করে ব্যর্থ হয়েছিল)। এই script
# আসল ঐতিহাসিক flood event-এর সময় upstream শহরের দৈনিক rainfall ও
# downstream FFWC station-এর দৈনিক discharge — দুটো time series
# নিয়ে cross-correlation করে দেখে কত দিনের delay-তে correlation
# সবচেয়ে বেশি, এবং সেটাকে বর্তমান hardcoded lag_time-এর সাথে তুলনা করে।
#
# ⚠️ সীমাবদ্ধতা (honestly স্বীকার করা প্রয়োজন):
# - Open-Meteo daily resolution দেয়, তাই lag resolution = ১ দিন (২৪ ঘণ্টা)।
#   বর্তমান lag_time-এর অনেকগুলোই ২৪ ঘণ্টার কম (৫-২০ ঘণ্টা) — এই ছোট
#   lag-গুলো দৈনিক resolution দিয়ে নির্ভুলভাবে ধরা সম্ভব না। এই script
#   শুধু ~২৪ ঘণ্টা বা তার বেশি lag থাকা জেলাগুলোর (কুড়িগ্রাম ১৮, শেরপুর ২০,
#   চট্টগ্রাম ২০, ঢাকা/গাজীপুর/নারায়ণগঞ্জ ২৪) জন্য অর্থবহ সংকেত দিতে পারে।
# - ছোট lag (ফেনী ৬, বান্দরবান ৫, খাগড়াছড়ি ৬) — এই ফলাফল অবিশ্বাস্য/noisy
#   হওয়ার সম্ভাবনা বেশি, শুধু reference হিসেবে দেখানো হচ্ছে, সিদ্ধান্ত না।
# - Dhaka,BD-কে "upstream" হিসেবে ব্যবহার করা জেলা (Urban Waterlogging
#   type — ঢাকা/চট্টগ্রাম/গাজীপুর/নারায়ণগঞ্জ) বাদ দেওয়া হয়েছে, কারণ
#   ওখানে আসল upstream cross-border rainfall না, local rainfall-ই কারণ।

import sys
import csv
import time
import requests
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from data.flood_config import FLOOD_CONFIG

OUTPUT_CSV = Path(__file__).parent / "lag_time_analysis_results.csv"

# ৯টা upstream শহরের lat/lon (হাতে verified, ছোট fixed তালিকা)
UPSTREAM_CITIES = {
    "Shillong,IN": (25.5788, 91.8933),
    "Guwahati,IN": (26.1445, 91.7362),
    "Jalpaiguri,IN": (26.5432, 88.7195),
    "Siliguri,IN": (26.7271, 88.3953),
    "Agartala,IN": (23.8315, 91.2868),
    "Kolkata,IN": (22.5726, 88.3639),
    "Malda,IN": (25.0108, 88.1411),
    "Raiganj,IN": (25.6186, 88.1239),
}

# একটা প্রকৃত ঐতিহাসিক flood event window (২০২০ বর্ষা — সব basin-এই বড় বন্যা,
# তাই rainfall/discharge উভয়েই signal থাকার সম্ভাবনা বেশি)
EVENT_START = "2020-06-20"
EVENT_END = "2020-08-20"
DAYS_BEFORE = 10  # upstream rainfall event শুরুর কত আগে থেকে দেখা হবে


def fetch_daily_series(lat, lon, start, end, variable, base_url, daily_key):
    try:
        r = requests.get(
            base_url,
            params={"latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
                    "daily": daily_key},
            timeout=30,
        )
        data = r.json()
        vals = data.get("daily", {}).get(daily_key)
        if not vals:
            return None
        return [float(v) if v is not None else 0.0 for v in vals]
    except Exception as e:
        print(f"  ⚠️ fetch error ({variable}): {e}")
        return None


def fetch_rain_series(lat, lon, start, end):
    return fetch_daily_series(lat, lon, start, end, "rain",
                               "https://archive-api.open-meteo.com/v1/archive", "precipitation_sum")


def fetch_discharge_series(lat, lon, start, end):
    return fetch_daily_series(lat, lon, start, end, "discharge",
                               "https://flood-api.open-meteo.com/v1/flood", "river_discharge")


def best_lag_days(rain, discharge, max_lag=6):
    """rain[t] বনাম discharge[t+lag] — কোন lag (দিনে) সবচেয়ে বেশি Pearson correlation দেয়।"""
    rain = np.array(rain)
    discharge = np.array(discharge)
    best_lag, best_corr = 0, -2.0
    for lag in range(0, max_lag + 1):
        if lag >= len(rain):
            break
        r = rain[: len(rain) - lag]
        d = discharge[lag:]
        n = min(len(r), len(d))
        if n < 5:
            continue
        r, d = r[:n], d[:n]
        if np.std(r) == 0 or np.std(d) == 0:
            continue
        corr = np.corrcoef(r, d)[0, 1]
        if corr > best_corr:
            best_corr, best_lag = corr, lag
    return best_lag, best_corr


def run():
    start = (datetime.strptime(EVENT_START, "%Y-%m-%d") - timedelta(days=DAYS_BEFORE)).strftime("%Y-%m-%d")
    end = EVENT_END

    rows_out = []
    print(f"বিশ্লেষণের সময়কাল: {start} থেকে {end}\n")

    for district, cfg in FLOOD_CONFIG.items():
        if cfg.get("flood_type") == "Urban Waterlogging":
            continue  # local rainfall-চালিত, upstream cross-border lag অর্থহীন
        upstream = cfg.get("upstream")
        if upstream not in UPSTREAM_CITIES:
            continue
        u_lat, u_lon = UPSTREAM_CITIES[upstream]
        d_lat, d_lon = cfg["river_lat"], cfg["river_lon"]
        current_lag_hours = cfg.get("lag_time")

        print(f"=== {district} (upstream: {upstream}, বর্তমান lag_time={current_lag_hours}h) ===")
        rain = fetch_rain_series(u_lat, u_lon, start, end)
        discharge = fetch_discharge_series(d_lat, d_lon, start, end)

        if not rain or not discharge or len(rain) < 10 or len(discharge) < 10:
            print("  ⚠️ ডেটা অপর্যাপ্ত, বাদ দেওয়া হলো\n")
            continue

        lag_days, corr = best_lag_days(rain, discharge)
        empirical_lag_hours = lag_days * 24
        diff_hours = empirical_lag_hours - current_lag_hours

        print(f"  empirical lag ≈ {lag_days} দিন ({empirical_lag_hours}h), correlation={corr:.2f}, "
              f"বর্তমান vs empirical পার্থক্য={diff_hours:+d}h\n")

        rows_out.append({
            "district": district, "upstream": upstream, "river": cfg.get("river"),
            "current_lag_hours": current_lag_hours, "empirical_lag_days": lag_days,
            "empirical_lag_hours": empirical_lag_hours, "correlation": round(corr, 3),
            "diff_hours": diff_hours,
        })
        time.sleep(0.3)  # rate-limit সৌজন্যে

    if rows_out:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
            w.writeheader()
            w.writerows(rows_out)
        print(f"✅ ফলাফল সেভ হয়েছে: {OUTPUT_CSV} ({len(rows_out)} জেলা)")
    else:
        print("⚠️ কোনো জেলার জন্য যথেষ্ট ডেটা পাওয়া যায়নি।")


if __name__ == "__main__":
    run()
