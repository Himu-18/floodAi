# ============================================================
# FloodAI — data/district_profiles/moulvibazar.py — জেলা #৪৬
# সিলেটের সুরমা-কুশিয়ারা গবেষণা আংশিকভাবে reuse করা হয়েছে (Sherpur-Sylhet station)।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MOULVIBAZAR_PROFILE = {
    "district": "মৌলভীবাজার", "district_lat": 24.57, "district_lon": 91.70,
    "station_count": 4,

    "stations": [
        {
            "name": "Moulvibazar", "ffwc_id": "SW202", "is_primary": True,
            "river": "মনু (Manu)", "upazila": "Rajnagar", "union": None,
            "river_structure": {"category": "medium (মেঘালয়/ত্রিপুরা পাহাড় থেকে সরাসরি নেমে আসা)", "catchment": "মৌলভীবাজার শহরের প্রধান নদী", "upstream_reference": "Agartala, IN", "lag_time_hours": 12},
            "danger_level_m": 11.30, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1130, "corrected_estimate": 700, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, সিলেট/সুনামগঞ্জের মাঝারি উপনদীর সাথে তুলনীয়", "confidence": "low"},
                "cn": {"old_value": 82, "reviewed_estimate": 86, "confidence": "moderate"},
                "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত)", "reasoning": "সিলেট বিভাগের flash-flood-প্রবণ জেলা হিসেবে সুপরিচিত"},
            },
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Kamalganj", "ffwc_id": "SW67", "is_primary": False,
            "river": "ঢলাই (Dhalai)", "upazila": "Kamalganj", "union": None,
            "river_structure": {"category": "small (এই framework-এ danger_level সবচেয়ে বেশি — ১৯.৩৫ মি, তবে ছোট নদী, উঁচু elevation-এর কারণে)", "catchment": "ত্রিপুরা সীমান্তের কাছাকাছি", "upstream_reference": "Agartala, IN", "lag_time_hours": 12},
            "danger_level_m": 19.35, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1935, "corrected_estimate": 400, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 86, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Moulvibazar primary-র অনুরূপ"}},
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Sherpur-Sylhet", "ffwc_id": "SW175.5", "is_primary": False,
            "river": "কুশিয়ারা (Kushiyara)", "upazila": "Maulvi Bazar Sadar", "union": None,
            "river_structure": {"category": "large_regional", "catchment": "সিলেটের একই কুশিয়ারা, ভাটির দিকে", "upstream_reference": "Shillong, IN", "upstream_reference_note": "✅ এখানে সঠিক (কুশিয়ারার জন্য), কিন্তু জেলার বাকি ৩ station-এ 'Agartala,IN' — একই জেলার মধ্যেই দুই ভিন্ন upstream reference ব্যবহার হচ্ছে, যা আসলে সঠিক (মনু/ঢলাই ত্রিপুরা থেকে, কুশিয়ারা মেঘালয় থেকে) — এই জেলাটা একই সাথে দুই hill-source-এর সংযোগস্থল।", "lag_time_hours": 12},
            "danger_level_m": 8.55, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 855, "corrected_estimate": 900, "corrected_range": "সিলেটের কুশিয়ারা রেফারেন্স reuse", "source": "সিলেট profile", "confidence": "moderate"}, "cn": {"old_value": None, "reviewed_estimate": 84, "confidence": "moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "কুশিয়ারার সরাসরি সংস্পর্শ"}},
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Manu-RB", "ffwc_id": "SW201", "is_primary": False,
            "river": "মনু (Manu)", "upazila": "Kulaura", "union": None,
            "river_structure": {"category": "medium", "catchment": "Moulvibazar(SW202)-র একই মনু নদী, উজানে (Kulaura)", "upstream_reference": "Agartala, IN", "lag_time_hours": 12},
            "danger_level_m": 17.55, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "gap_found": "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র মৌলভীবাজারের rivers লিস্টে নেই (মনু নদীর ২টা gauge point-এর একটা, Moulvibazar/SW202, তালিকায় আছে কিন্তু Manu-RB/SW201 নেই) — নওগাঁ/সিরাজগঞ্জের প্যাটার্নের পুনরাবৃত্তি।",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1755, "corrected_estimate": 700, "confidence": "low — Moulvibazar primary-র অনুরূপ ধরা হয়েছে"}, "cn": {"old_value": None, "reviewed_estimate": 86, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "একই মনু নদী, উজানের gauge"}},
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "সিলেট/সুনামগঞ্জের একই যুক্তি — rainfall primary predictor।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "সিলেট/সুনামগঞ্জের সাথে কুশিয়ারা ভাগাভাগি করে, কিন্তু মনু/ঢলাই ত্রিপুরা-নির্দিষ্ট বলে কুমিল্লা/ফেনীর মতো দ্বিতীয় hill-source cluster-এরও অংশ — এই জেলাটা দুই cluster-এর সংযোগস্থল।",
}