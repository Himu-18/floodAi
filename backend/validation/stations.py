# validation/stations.py
# ============================================================
# FloodAI Validation — Phase 1 Station List
# ============================================================
# advisor-এর সুপারিশকৃত ১২টা representative station (বড় flood-source
# gauge, বিভিন্ন নদী-আচরণ কভার করার জন্য বাছাই করা)। সব কয়টার তথ্য
# ইতিমধ্যে data/stations.py ও data/districts_profiles/-এ verified আছে,
# এখানে শুধু validation-এর জন্য একসাথে সংগঠিত করা হলো।
#
# ⚠️ নোট: "Sirajganj" নামে stations.py-তে আলাদা কোনো gauge পাওয়া যায়নি —
# Kazipur ও Baghabari দুটোই সিরাজগঞ্জ জেলার আওতায় পড়ে (ভিন্ন নদী-সিস্টেম),
# তাই আপাতত এই দুটোকেই সিরাজগঞ্জের প্রতিনিধি হিসেবে রাখা হলো। ভবিষ্যতে
# BWDB-র হাইড্রোলজি পোর্টাল থেকে সিরাজগঞ্জ শহরের নিজস্ব gauge (যদি থাকে)
# যাচাই করে যোগ করা যেতে পারে।

VALIDATION_STATIONS = [
    {
        "name": "Bahadurabad", "ffwc_id": "SW46.9L", "river": "Jamuna/Brahmaputra",
        "district": "জামালপুর", "danger_level_m": 19.05,
        "lat": 25.14, "lon": 89.60,
        "note": "⚠️ coordinate নিয়ে uncertainty আছে (profile অনুযায়ী প্রকৃত lat=25.1303, lon=89.7346 হতে পারে — BWDB hydrology survey অনুযায়ী) — validation চালানোর আগে দুটো coordinate-এই test করে দেখা ভালো",
        "category": "mega_trunk",
    },
    {
        "name": "Aricha", "ffwc_id": "SW50.6", "river": "Jamuna",
        "district": "মানিকগঞ্জ", "danger_level_m": 8.95,
        "lat": 23.90, "lon": 89.83,
        "category": "mega_trunk",
    },
    {
        "name": "Kazipur", "ffwc_id": "SW49A", "river": "Jamuna",
        "district": "সিরাজগঞ্জ", "danger_level_m": 14.80,
        "lat": 24.60, "lon": 89.72,
        "category": "mega_trunk",
    },
    {
        "name": "Baghabari", "ffwc_id": "SW151", "river": "Karatoa-Atrai-GGH",
        "district": "সিরাজগঞ্জ", "danger_level_m": 9.95,
        "lat": 24.20, "lon": 89.55,
        "note": "Jamuna trunk না — উত্তর-পশ্চিম বাংলাদেশের সম্মিলিত নিষ্কাশন ব্যবস্থার outlet, ভিন্ন নদী-আচরণ কভার করার জন্য রাখা",
        "category": "secondary_drainage",
    },
    {
        "name": "Jamalpur", "ffwc_id": "SW225", "river": "Old Brahmaputra",
        "district": "জামালপুর", "danger_level_m": 16.55,
        "lat": 24.92, "lon": 89.94,
        "note": "Jamuna trunk না — পুরাতন ব্রহ্মপুত্র distributary",
        "category": "distributary",
    },
    {
        "name": "Goalondo", "ffwc_id": "SW91.9R", "river": "Ganges/Padma",
        "district": "রাজবাড়ী", "danger_level_m": 8.20,
        "lat": 23.71, "lon": 89.74,
        "category": "mega_trunk",
    },
    {
        "name": "Hardinge-RB", "ffwc_id": "SW90", "river": "Ganges",
        "district": "পাবনা", "danger_level_m": 13.80,
        "lat": 24.07, "lon": 89.05,
        "note": "সবচেয়ে বেশি cite করা গঙ্গা gauge",
        "category": "mega_trunk",
    },
    {
        "name": "Sureshswar", "ffwc_id": "SW95", "river": "Padma",
        "district": "শরীয়তপুর", "danger_level_m": 4.00,
        "lat": 23.27, "lon": 90.35,
        "category": "mega_trunk",
    },
    {
        "name": "Kurigram", "ffwc_id": "SW77", "river": "Dharla",
        "district": "কুড়িগ্রাম", "danger_level_m": 26.05,
        "lat": 25.81, "lon": 89.66,
        "note": "Brahmaputra trunk না — Dharla উপনদী",
        "category": "tributary",
    },
    {
        "name": "Gaibandha", "ffwc_id": "SW97", "river": "Ghagot",
        "district": "গাইবান্ধা", "danger_level_m": 21.25,
        "lat": 25.33, "lon": 89.55,
        "note": "Jamuna trunk না — Ghagot উপনদী",
        "category": "tributary",
    },
    {
        "name": "Kaunia", "ffwc_id": "SW294", "river": "Teesta",
        "district": "রংপুর", "danger_level_m": 29.31,
        "lat": 25.78, "lon": 89.47,
        "note": "ব্যারেজ-প্রভাবিত (Teesta Barrage upstream) — dry/wet season flow-এ বিশাল তফাত থাকতে পারে",
        "category": "barrage_affected",
    },
]

if __name__ == "__main__":
    print(f"মোট validation station: {len(VALIDATION_STATIONS)}")
    for s in VALIDATION_STATIONS:
        print(f"  {s['name']} ({s['ffwc_id']}) — {s['river']}, danger={s['danger_level_m']}m, category={s['category']}")
