# ============================================================
# FloodAI — data/district_profiles/gazipur.py — জেলা #২৪
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

GAZIPUR_PROFILE = {
    "district": "গাজীপুর",
    "district_lat": 23.87, "district_lon": 90.27,
    "station_count": 2,
    "station_count_note": "✅ দুইটা station-ই flood_config.py-তে সঠিকভাবে linked, কোনো gap নেই।",

    "stations": [
        {
            "name": "Kaliakoir", "ffwc_id": "SW301", "is_primary": True,
            "river": "তুরাগ (Turag)", "upazila": "Kaliakoir", "union": None,
            "river_structure": {"category": "urban_tidal_river", "catchment": "ঢাকার তুরাগের একই সিস্টেম, কিন্তু গাজীপুরের শিল্পাঞ্চলের কাছাকাছি (industrial pollution/encroachment বাড়তি factor)", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
            "danger_level_m": 7.95, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 795, "corrected_estimate": None, "note": "ঢাকার প্যাটার্নের একই — drainage-capacity ভিত্তিক approach দরকার", "confidence": "none"},
                "cn": {"old_value": 95, "reviewed_estimate": 95, "reasoning": "✅ ঢাকার মতোই সঠিক ও উচ্চ — শিল্পাঞ্চল/আবাসিক impervious surface", "confidence": "high"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "টঙ্গী/চান্দনা চৌরাস্তা/বোর্ডবাজার — ঘনবসতিপূর্ণ শিল্পাঞ্চল, বন্যায় শিল্প উৎপাদন ক্ষতিও যুক্ত হয় সাধারণ বাসিন্দাদের ক্ষতির সাথে, ঢাকার সাথে সঙ্গতি রাখতে upgrade করা হলো"},
            },
            "flood_type": "Urban Waterlogging",
            "inundation_bands": {"affected_areas": "টঙ্গী, চান্দনা চৌরাস্তা, বোর্ডবাজার (flood_config.py-তে নির্দিষ্টভাবে উল্লেখিত)", "status": "⚠️ placeholder"},
        },
        {
            "name": "Tongi", "ffwc_id": "SW299", "is_primary": False,
            "river": "টঙ্গী খাল (Tongi Khal)", "upazila": "Gazipur Sadar", "union": None,
            "river_structure": {"category": "urban_khal (ছোট শহুরে খাল, নদী না)", "catchment": "ঢাকা-গাজীপুর সীমান্তবর্তী শিল্পাঞ্চলীয় খাল", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
            "danger_level_m": 5.65, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 565, "corrected_estimate": None, "note": "ছোট urban khal — discharge_ratio ধারণাটাই এখানে সবচেয়ে কম প্রাসঙ্গিক এই framework-এ", "confidence": "none"},
                "cn": {"old_value": None, "reviewed_estimate": 95, "confidence": "high"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Kaliakoir station-এর অনুরূপ শিল্পাঞ্চলীয় ঝুঁকি"},
            },
            "flood_type": "Urban Waterlogging",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "ঢাকার একই যুক্তি — drainage-capacity/rainfall-intensity ভিত্তিক approach দরকার, soil_moisture অপ্রাসঙ্গিক।",

    "confluence_note": "গাজীপুর CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "ঢাকার সাথে একই তুরাগ নদী সিস্টেম, drainage-capacity সমস্যাও একই ধরনের — যৌথভাবে একটা 'Dhaka Metro urban cluster' হিসেবে model করা যেতে পারে গাজীপুর+নারায়ণগঞ্জ+ঢাকা মিলিয়ে।",
}