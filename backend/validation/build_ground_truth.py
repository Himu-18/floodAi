# build_ground_truth.py
# ============================================================
# FloodAI Validation — Real ground-truth সংকলন
# ============================================================
# v3 (station-level, ১৯৯৮+২০১২, FFWC/BWDB Annual Flood Report থেকে সরাসরি
# পর্যবেক্ষিত peak water-level বনাম danger-level) ও v6 (district-level,
# ২০১৭+২০২০, FFWC Annual Flood Report-এ explicit রিপোর্ট করা) — দুটো real
# সূত্রকে একটা একক canonical ground-truth ফাইলে একত্র করে, যাতে
# backtest_v2.py ও ভবিষ্যতের script গুলো flood_events.csv-এর মোটা দাগের
# জাতীয় date-range অনুমানের বদলে এই বেশি নির্ভুল, station/district-নির্দিষ্ট
# তথ্য ব্যবহার করতে পারে।
#
# ⚠️ network লাগে না — সবই static ইনপুট ফাইল থেকে, তাই এটা Claude-এর
# sandbox-এই চালানো সম্ভব হয়েছে।

import csv
from pathlib import Path

REAL_DATA_DIR = Path(__file__).parent / "real_data"
OUT_PATH = Path(__file__).parent / "ground_truth.csv"


def from_v3_waterlevel():
    """v3: station-level, ১৯৯৮ ও ২০১২ — সবচেয়ে নির্ভরযোগ্য (সরাসরি gauge observation)।"""
    rows = []
    path = REAL_DATA_DIR / "1788143402457_floodai_real_waterlevel_v3.csv"
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            danger = float(r["danger_level_mPWD"])

            # ২০১২ (সব station-এই আছে)
            peak_2012 = float(r["peak_2012_mPWD"])
            rows.append({
                "year": 2012, "district": r["district"], "station": r["station"],
                "river": r["river"], "flood_occurred": 1 if peak_2012 >= danger else 0,
                "granularity": "station", "source": r["source"],
            })

            # ১৯৯৮ (কিছু station-এ missing)
            if r["peak_1998_mPWD"]:
                peak_1998 = float(r["peak_1998_mPWD"])
                rows.append({
                    "year": 1998, "district": r["district"], "station": r["station"],
                    "river": r["river"], "flood_occurred": 1 if peak_1998 >= danger else 0,
                    "granularity": "station", "source": r["source"],
                })
    return rows


def from_v6_district_events():
    """v6: district-level, ২০১৭ ও ২০২০ — FFWC-র annual report-এ explicit উল্লেখ করা।"""
    rows = []
    path = REAL_DATA_DIR / "1788143429916_floodai_district_flood_events_v6.csv"
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": int(r["year"]), "district": r["district"], "station": None,
                "river": r["river_or_system"], "flood_occurred": int(r["flood_occurred"]),
                "granularity": "district", "source": r["source"],
            })
    return rows


def from_researched_stations():
    """
    Claude ওয়েব সার্চ করে সংগ্রহ করা station-নির্দিষ্ট real observation
    (FFWC bulletin/ReliefWeb/Daily Star/Prothom Alo সূত্রে) — ২০০৪, ২০০৭,
    ২০১৯, ২০২২, ২০২৪ সালের জন্য, যেগুলো আগে flood_events.csv-এর মোটা
    জাতীয় date-range অনুমানের উপর নির্ভরশীল ছিল।
    """
    rows = []
    path = REAL_DATA_DIR / "station_level_events_researched.csv"
    if not path.exists():
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": int(r["year"]), "district": r["district_en"], "station": r["station"],
                "river": r["river"], "flood_occurred": int(r["flood_occurred"]),
                "granularity": "station", "source": r["source"],
            })
    return rows


STATION_TO_DISTRICT = {"Bahadurabad": "Jamalpur", "Hardinge Bridge": "Pabna"}


def from_v1_hydrology_seed():
    """
    v1: discharge-based annual flood flag (bankfull_exceeded), Bahadurabad+
    Hardinge Bridge, ১৯৮৫-২০১৫। v3 (waterlevel-based) ইতিমধ্যে ১৯৯৮ ও ২০১২
    কভার করে, তাই ডুপ্লিকেট এড়াতে সেই দুই বছর বাদ দিয়ে বাকি ৩১টা নতুন
    বছর যোগ করা হচ্ছে — এটা independent evidence (discharge, water-level না)।
    """
    rows = []
    path = REAL_DATA_DIR / "1788143382153_floodai_real_hydrology_seed_v1.csv"
    if not path.exists():
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            year = int(r["year"])
            if year in (1998, 2012):
                continue  # v3-তে waterlevel-ভিত্তিক এন্ট্রি ইতিমধ্যে আছে
            district = STATION_TO_DISTRICT.get(r["station"])
            if not district:
                continue
            rows.append({
                "year": year, "district": district, "station": r["station"],
                "river": r["river"], "flood_occurred": int(r["bankfull_exceeded"]),
                "granularity": "station",
                "source": f"BWDB hydrology seed (discharge, {r['source_class']})",
            })
    return rows


def from_v13_station_master():
    """
    v13: station-level feature (peak vs danger water-level, ২০১৭+২০২০)
    district-level verified label (v9/v10)-এর সাথে join করা। শুধু
    label_join_status == "LABELED" row নেওয়া হচ্ছে (unverified বাদ)।
    granularity="district" কারণ flood_occurred আসলে FFWC-র district-level
    verified determination, station-টা শুধু hydrological context।
    """
    rows = []
    path = REAL_DATA_DIR / "floodai_district_station_master_v13.csv"
    if not path.exists():
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["label_join_status"] != "LABELED":
                continue
            rows.append({
                "year": int(r["year"]), "district": r["district"], "station": r["station"],
                "river": r["river"], "flood_occurred": int(float(r["flood_occurred"])),
                "granularity": "district", "source": r["source"],
            })
    return rows


def from_ffwc_2019_annual_report():
    """
    FFWC Annual Flood Report 2019 (old.ffwc.gov.bd/images/annual19.pdf)-এর
    Section 3.1-3.4 থেকে হাতে তোলা ৬২টা station-এর exact peak/danger-level/
    days-above-danger ডেটা — এখন পর্যন্ত সবচেয়ে সমৃদ্ধ, নির্ভরযোগ্য একক-বছর
    উৎস (২০১৯-এর আগের entry ছিল মাত্র ১০টা, এটা দিয়ে অনেক বেশি বেড়ে যাবে)।
    """
    rows = []
    path = REAL_DATA_DIR / "ffwc_2019_annual_report_stations.csv"
    if not path.exists():
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": int(r["year"]), "district": r["district"], "station": r["station"],
                "river": r["river"], "flood_occurred": int(r["exceeded_danger"]),
                "granularity": "station", "source": r["source"],
            })
    return rows


def from_ffwc_2020_annual_report():
    """
    FFWC Annual Flood Report 2020 (old.ffwc.gov.bd/images/annual20.pdf)-এর
    Table 3.1-3.5 থেকে হাতে তোলা ৯৯টা station-এর exact danger_level/peak_2020/
    days-above-danger — ২০১৯-এর চেয়েও বেশি station কভার করে (২০২০ ছিল একটা
    বড়, দীর্ঘস্থায়ী বছর — ৬টা পৃথক flood spell, জুন-অক্টোবর জুড়ে)।
    """
    rows = []
    path = REAL_DATA_DIR / "ffwc_2020_annual_report_stations.csv"
    if not path.exists():
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": int(r["year"]), "district": r["district"], "station": r["station"],
                "river": r["river"], "flood_occurred": int(r["exceeded_danger"]),
                "granularity": "station", "source": r["source"],
            })
    return rows


def run():
    all_rows = (from_v3_waterlevel() + from_v6_district_events()
                + from_researched_stations() + from_v13_station_master()
                + from_v1_hydrology_seed() + from_ffwc_2019_annual_report()
                + from_ffwc_2020_annual_report())
    all_rows.sort(key=lambda r: (r["year"], r["district"]))

    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "district", "station", "river", "flood_occurred", "granularity", "source"])
        writer.writeheader()
        writer.writerows(all_rows)

    flood_count = sum(1 for r in all_rows if r["flood_occurred"] == 1)
    print(f"✅ {OUT_PATH} — মোট {len(all_rows)}টা real ground-truth এন্ট্রি "
          f"({flood_count} flood, {len(all_rows) - flood_count} below-danger)")
    print(f"   station-level (v3, সবচেয়ে নির্ভরযোগ্য): {sum(1 for r in all_rows if r['granularity']=='station')}")
    print(f"   district-level (v6/v13): {sum(1 for r in all_rows if r['granularity']=='district')}")
    years = sorted(set(r["year"] for r in all_rows))
    print(f"   বছর কভার করা হয়েছে: {years}")


if __name__ == "__main__":
    run()
