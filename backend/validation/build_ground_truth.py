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


def run():
    all_rows = from_v3_waterlevel() + from_v6_district_events()
    all_rows.sort(key=lambda r: (r["year"], r["district"]))

    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "district", "station", "river", "flood_occurred", "granularity", "source"])
        writer.writeheader()
        writer.writerows(all_rows)

    flood_count = sum(1 for r in all_rows if r["flood_occurred"] == 1)
    print(f"✅ {OUT_PATH} — মোট {len(all_rows)}টা real ground-truth এন্ট্রি "
          f"({flood_count} flood, {len(all_rows) - flood_count} below-danger)")
    print(f"   station-level (v3, সবচেয়ে নির্ভরযোগ্য): {sum(1 for r in all_rows if r['granularity']=='station')}")
    print(f"   district-level (v6): {sum(1 for r in all_rows if r['granularity']=='district')}")
    years = sorted(set(r["year"] for r in all_rows))
    print(f"   বছর কভার করা হয়েছে: {years}")


if __name__ == "__main__":
    run()
