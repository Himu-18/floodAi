"""
FloodAI — calibrate_river_coords_v3.py (OSM geometry + category range, combined)

দুই ধাপে কাজ করে:

ধাপ ১ (OSM geometry) — Overpass API (OpenStreetMap) দিয়ে সেই নির্দিষ্ট
নামের নদীর real line (একগুচ্ছ lat/lon, যেগুলো ভৌগোলিকভাবে নিশ্চিতভাবে
সেই নদীর উপরই) খুঁজে বের করা, জেলার আনুমানিক কেন্দ্রের ৪০ কিমি
radius-এর মধ্যে। এতে "ভুল নদীতে চলে যাওয়া" (যেমন গড়াই ভুল করে পদ্মায়)
আটকানো যায়, কারণ candidate point-গুলো শুরু থেকেই শুধু সঠিক নদীর
line থেকেই আসছে।

ধাপ ২ (category range) — সেই OSM-candidate point-গুলোর মধ্যে discharge
মেপে, river_categories.py-র physically-grounded রেঞ্জের মধ্যে যেটা
সবচেয়ে বেশি সেটা বেছে নেওয়া — এতে GloFAS-এর নিজস্ব grid-resolution
ভুল (braided channel-এ ভুল spot ধরা) অনেকটা কমে।

Fallback: যদি OSM-এ সেই নদীর geometry না পাওয়া যায় (ট্যাগ না থাকা,
নাম ভিন্ন বানান ইত্যাদি), পুরনো grid-search পদ্ধতিতে ফিরে যাওয়া হয়
(calibrate_river_coords_v2.py-র মতোই), আর "osm_used": False দিয়ে
স্পষ্ট চিহ্নিত করা হয় যাতে বোঝা যায় কোনগুলো কম নিশ্চিত।

⚠️ এরপরও এটা ১০০% ground-truth verified না — দুইটা independent
plausibility filter (geometry + physical range), কোনো সরাসরি
real-measurement cross-check না।

ব্যবহার:
    py backend/calibrate_river_coords_v3.py
    (রিপোর্ট backend/river_coord_report_v3.csv এ সেভ হবে)

⚠️ Overpass (OSM) পাবলিক সার্ভার ব্যবহার হচ্ছে — সৌজন্যের জন্য প্রতি
জেলার মাঝে ১.৫ সেকেন্ড বিরতি রাখা হয়েছে, তাই আগের script-গুলোর
চেয়েও বেশি সময় লাগবে (~২০-৩০ মিনিট হতে পারে ৬৪ জেলার জন্য)।
"""

import sys
import time
import csv
import requests

sys.path.insert(0, ".")
from data.districts_base import DISTRICTS_BASE
from data.flood_config import FLOOD_CONFIG
from data.river_categories import RIVER_CATEGORY_RANGES, DISTRICT_RIVER_CATEGORY
from data.river_names import DISTRICT_RIVER_NAMES

DISTRICTS = {
    name: {**base, **FLOOD_CONFIG.get(name, {})}
    for name, base in DISTRICTS_BASE.items()
}

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OSM_SEARCH_RADIUS_M = 40000       # জেলার কেন্দ্র থেকে ৪০ কিমি-র মধ্যে নদী খোঁজা
MAX_OSM_CANDIDATES = 14           # OSM থেকে পাওয়া পয়েন্ট থেকে সর্বোচ্চ কতগুলো টেস্ট করা হবে
GRID_OFFSETS = [-0.10, -0.05, 0.0, 0.05, 0.10]  # OSM ব্যর্থ হলে fallback grid
REQUEST_DELAY_SECONDS = 0.4
OVERPASS_DELAY_SECONDS = 1.5


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


def fetch_osm_river_points(name_bn, name_en, center_lat, center_lon):
    """Overpass API দিয়ে নির্দিষ্ট নামের নদীর line geometry খুঁজে বের করা,
    জেলার কেন্দ্রের আশেপাশে। রিটার্ন: [(lat, lon), ...] বা খালি লিস্ট।"""
    query = f"""
    [out:json][timeout:25];
    (
      way["waterway"="river"]["name"~"{name_bn}",i](around:{OSM_SEARCH_RADIUS_M},{center_lat},{center_lon});
      way["waterway"="river"]["name:en"~"{name_en}",i](around:{OSM_SEARCH_RADIUS_M},{center_lat},{center_lon});
    );
    out geom;
    """
    try:
        r = requests.post(OVERPASS_URL, data={"data": query}, timeout=30)
        data = r.json()
    except Exception as e:
        print(f"    [OSM error] {e}")
        return []

    points = []
    for element in data.get("elements", []):
        geometry = element.get("geometry", [])
        for node in geometry:
            points.append((node["lat"], node["lon"]))
    return points


def sample_points(points, max_count):
    """অনেক পয়েন্ট থাকলে সমান দূরত্বে sample করে সংখ্যা কমানো (API call বাঁচাতে)"""
    if len(points) <= max_count:
        return points
    step = len(points) // max_count
    return points[::step][:max_count]


def calibrate_district(name, info):
    base_lat = info.get("river_lat", info.get("lat"))
    base_lon = info.get("river_lon", info.get("lon"))
    if base_lat is None or base_lon is None:
        return None

    category = DISTRICT_RIVER_CATEGORY.get(name, "medium")
    range_min, range_max = RIVER_CATEGORY_RANGES[category]
    names = DISTRICT_RIVER_NAMES.get(name, {})

    osm_points = []
    if names:
        osm_points = fetch_osm_river_points(names["bn"], names["en"], base_lat, base_lon)
        time.sleep(OVERPASS_DELAY_SECONDS)

    osm_used = len(osm_points) > 0

    if osm_used:
        test_points = sample_points(osm_points, MAX_OSM_CANDIDATES)
    else:
        # fallback: পুরনো grid পদ্ধতি
        test_points = [
            (round(base_lat + dlat, 4), round(base_lon + dlon, 4))
            for dlat in GRID_OFFSETS for dlon in GRID_OFFSETS
        ]

    candidates = []
    current_discharge = None
    for lat, lon in test_points:
        discharge = fetch_discharge(lat, lon)
        time.sleep(REQUEST_DELAY_SECONDS)
        if discharge is not None:
            candidates.append((lat, lon, discharge))
        if abs(lat - base_lat) < 0.001 and abs(lon - base_lon) < 0.001:
            current_discharge = discharge

    if current_discharge is None:
        current_discharge = fetch_discharge(base_lat, base_lon)
        time.sleep(REQUEST_DELAY_SECONDS)

    in_range = [c for c in candidates if range_min <= c[2] <= range_max]

    if in_range:
        best_lat, best_lon, best_discharge = max(in_range, key=lambda c: c[2])
        in_range_found = True
    elif candidates:
        best_lat, best_lon, best_discharge = base_lat, base_lon, current_discharge
        in_range_found = False
    else:
        best_lat, best_lon, best_discharge = base_lat, base_lon, None
        in_range_found = False

    return {
        "district": name,
        "river": info.get("river"),
        "category": category,
        "osm_used": osm_used,
        "osm_points_found": len(osm_points),
        "current_lat": base_lat,
        "current_lon": base_lon,
        "current_discharge": current_discharge,
        "best_lat": best_lat,
        "best_lon": best_lon,
        "best_discharge": best_discharge,
        "in_range_found": in_range_found,
    }


if __name__ == "__main__":
    print(f"মোট {len(DISTRICTS)} টা জেলা — OSM geometry + category range দিয়ে calibration শুরু হচ্ছে...\n")
    results = []
    for i, (name, info) in enumerate(DISTRICTS.items(), 1):
        print(f"[{i}/{len(DISTRICTS)}] {name} চেক হচ্ছে...")
        res = calibrate_district(name, info)
        if res:
            results.append(res)
            osm_flag = f"OSM: {res['osm_points_found']} পয়েন্ট পাওয়া গেছে" if res["osm_used"] else "OSM ব্যর্থ, grid fallback ব্যবহার হয়েছে"
            range_flag = "✅ রেঞ্জে পাওয়া গেছে" if res["in_range_found"] else "⚠️ রেঞ্জে কিছু পাওয়া যায়নি"
            print(f"    {osm_flag} | বর্তমান: {res['current_discharge']} | সেরা: {res['best_discharge']} @ ({res['best_lat']}, {res['best_lon']}) {range_flag}")

    out_path = "river_coord_report_v3.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "district", "river", "category", "osm_used", "osm_points_found",
            "current_lat", "current_lon", "current_discharge",
            "best_lat", "best_lon", "best_discharge", "in_range_found"
        ])
        writer.writeheader()
        writer.writerows(results)

    osm_success = sum(1 for r in results if r["osm_used"])
    in_range_success = sum(1 for r in results if r["in_range_found"])
    print(f"\n✅ শেষ! {osm_success}/{len(results)} জেলায় OSM geometry পাওয়া গেছে।")
    print(f"✅ {in_range_success}/{len(results)} জেলায় category range-এর মধ্যে ভালো coordinate পাওয়া গেছে।")
    print(f"রিপোর্ট: {out_path}")