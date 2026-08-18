"""
FloodAI — calibrate_river_coords.py

সমস্যা: Open-Meteo Flood API (GloFAS) মাত্র ~৫ কিমি resolution-এ কাজ করে।
তাদের নিজস্ব documentation-ই বলে: "the closest river might not be selected
correctly. Varying coordinates by 0.1° can help." — মানে আমাদের বসানো
upazila-ভিত্তিক coordinate যদি এক-দুই grid cell এদিক-ওদিক হয়, তাহলে সেটা
মূল নদীর বদলে পাশের ছোট খাল/শাখা ধরে ফেলতে পারে, ফলে discharge প্রায়
শূন্য দেখায় (এটাই কিশোরগঞ্জে যা হচ্ছে)।

এই script প্রতিটা জেলার বর্তমান river_lat/river_lon-এর চারপাশে একটা ছোট
grid (±0.15° পর্যন্ত, 0.05° ধাপে) try করে দেখে — কোন point-এ সবচেয়ে বেশি
discharge (আজকের মান) আসে সেটাই "মূল নদী channel" হওয়ার সম্ভাবনা বেশি
(কারণ বড় নদীর discharge ছোট খালের চেয়ে বহুগুণ বেশি হওয়ার কথা)।

⚠️ এটা একটা heuristic (আন্দাজ), নিশ্চিত সঠিক উত্তর না — কিন্তু "current
point vs আশেপাশের সেরা point"-এর মধ্যে discharge-এ যদি অনেক পার্থক্য
থাকে (যেমন ৫ vs ৫০০০), সেটা জোরালো ইঙ্গিত যে নতুন point-টাই আসল নদী।
যদি সব point-ই কাছাকাছি কম discharge দেয়, সেটা normal (dry season) বা
গভীর কোনো সমস্যা (জেলাটাই ছোট নদীর) হতে পারে — script সবকিছু রিপোর্ট
করবে, তুমি নিজে চোখে দেখে সিদ্ধান্ত নেবে।

ব্যবহার:
    py backend/calibrate_river_coords.py
    (রিপোর্ট backend/river_coord_report.csv এ সেভ হবে)

⚠️ এটা Open-Meteo-কে অনেকগুলো call করবে (৬৪ জেলা x ~২৫ grid point =
~১৬০০ call!) — তাই সময় নেবে (কয়েক মিনিট) এবং rate-limit এড়াতে প্রতি
call-এর মাঝে ছোট delay আছে। শুধু একবার/মাঝেমধ্যে চালানোর জন্য, বারবার
না।
"""

import sys
import time
import csv
import requests

sys.path.insert(0, ".")
from data.districts_base import DISTRICTS_BASE
from data.flood_config import FLOOD_CONFIG

DISTRICTS = {
    name: {**base, **FLOOD_CONFIG.get(name, {})}
    for name, base in DISTRICTS_BASE.items()
}

# ±0.15° পর্যন্ত, 0.05° ধাপে grid — মোট 7x7 = ৪৯ point (কেন্দ্রসহ)।
# সময় বাঁচাতে অপেক্ষাকৃত ছোট grid রাখা হলো; দরকার হলে OFFSETS বাড়ানো যায়।
OFFSETS = [-0.10, -0.05, 0.0, 0.05, 0.10]
REQUEST_DELAY_SECONDS = 0.4  # সরকারি/free API-কে ভদ্রভাবে ব্যবহার করার জন্য


def fetch_discharge(lat, lon):
    try:
        r = requests.get(
            "https://flood-api.open-meteo.com/v1/flood",
            params={"latitude": lat, "longitude": lon, "daily": "river_discharge", "forecast_days": 1},
            timeout=8
        )
        data = r.json()
        return float(data["daily"]["river_discharge"][0])
    except Exception:
        return None


def calibrate_district(name, info):
    base_lat = info.get("river_lat", info.get("lat"))
    base_lon = info.get("river_lon", info.get("lon"))
    if base_lat is None or base_lon is None:
        return None

    best = {"lat": base_lat, "lon": base_lon, "discharge": None}
    current_discharge = None

    for dlat in OFFSETS:
        for dlon in OFFSETS:
            lat = round(base_lat + dlat, 4)
            lon = round(base_lon + dlon, 4)
            discharge = fetch_discharge(lat, lon)
            time.sleep(REQUEST_DELAY_SECONDS)

            if dlat == 0.0 and dlon == 0.0:
                current_discharge = discharge

            if discharge is not None and (best["discharge"] is None or discharge > best["discharge"]):
                best = {"lat": lat, "lon": lon, "discharge": discharge}

    return {
        "district": name,
        "river": info.get("river"),
        "current_lat": base_lat,
        "current_lon": base_lon,
        "current_discharge": current_discharge,
        "best_lat": best["lat"],
        "best_lon": best["lon"],
        "best_discharge": best["discharge"],
        "improved": (best["discharge"] or 0) > (current_discharge or 0) * 3  # অন্তত ৩ গুণ বেশি হলে "উল্লেখযোগ্য উন্নতি" ধরা হচ্ছে
    }


if __name__ == "__main__":
    print(f"মোট {len(DISTRICTS)} টা জেলা, প্রতিটাতে {len(OFFSETS)*len(OFFSETS)} টা grid point — সময় লাগবে, ধৈর্য ধরো...\n")
    results = []
    for i, (name, info) in enumerate(DISTRICTS.items(), 1):
        print(f"[{i}/{len(DISTRICTS)}] {name} চেক হচ্ছে...")
        res = calibrate_district(name, info)
        if res:
            results.append(res)
            flag = "🔺 উল্লেখযোগ্য উন্নতি সম্ভব!" if res["improved"] else ""
            print(f"    বর্তমান discharge: {res['current_discharge']} | "
                  f"সেরা পাওয়া গেছে: {res['best_discharge']} @ ({res['best_lat']}, {res['best_lon']}) {flag}")

    out_path = "river_coord_report.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "district", "river", "current_lat", "current_lon", "current_discharge",
            "best_lat", "best_lon", "best_discharge", "improved"
        ])
        writer.writeheader()
        writer.writerows(results)

    improved_count = sum(1 for r in results if r["improved"])
    print(f"\n✅ শেষ! {improved_count} টা জেলায় উল্লেখযোগ্য ভালো coordinate পাওয়া গেছে।")
    print(f"পুরো রিপোর্ট সেভ হয়েছে: {out_path} (এক্সেল/শীটে খুলে দেখতে পারো)")