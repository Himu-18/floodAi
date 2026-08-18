# ============================================================
# FloodAI — data/district_profiles/naogaon.py — জেলা #৩৭
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NAOGAON_PROFILE = {
    "district": "নওগাঁ", "district_lat": 24.79, "district_lon": 88.94,
    "station_count": 3,

    "stations": [
        {
            "name": "Mohadevpur", "ffwc_id": "SW145", "is_primary": True,
            "river": "আত্রাই (Atrai)", "upazila": "Manda", "union": None,
            "river_structure": {"category": "medium/large_regional", "catchment": "উত্তরবঙ্গের গুরুত্বপূর্ণ regional নদী, চলন বিল সিস্টেমের সাথে যুক্ত", "upstream_reference": "Malda, IN", "lag_time_hours": 24},
            "danger_level_m": 18.15, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1815, "corrected_estimate": 2500, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, regional river হিসেবে অনুমান", "confidence": "low"},
                "cn": {"old_value": 77, "reviewed_estimate": 87, "confidence": "low-moderate"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "নির্দিষ্ট বড় বন্যার ইতিহাস খুঁজে পাওয়া যায়নি"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Naogaon", "ffwc_id": "SW133", "is_primary": False,
            "river": "ছোট যমুনা (Little Jamuna)", "upazila": "Naogaon Sadar", "union": None,
            "river_structure": {"category": "medium (যমুনার সাথে নামের মিল থাকলেও সম্পূর্ণ আলাদা, ছোট স্থানীয় নদী)", "catchment": "নওগাঁ শহরের প্রধান নদী", "upstream_reference": "Malda, IN", "lag_time_hours": 24},
            "danger_level_m": 14.80, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1480, "corrected_estimate": 800, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 86, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "Mohadevpur station-এর অনুরূপ"}},
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Atrai", "ffwc_id": "SW147", "is_primary": False,
            "river": "আত্রাই (Atrai)", "upazila": "Atrai", "union": None,
            "river_structure": {"category": "medium/large_regional", "catchment": "Mohadevpur-এর একই আত্রাই নদী, ভিন্ন gauge point", "upstream_reference": "Malda, IN", "lag_time_hours": 24},
            "danger_level_m": 13.25, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "gap_found": "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র নওগাঁর rivers লিস্টে নেই (শুধু Mohadevpur/আত্রাই ও Naogaon/ছোট যমুনা আছে) — একই নদীর দুই gauge point-এর একটা বাদ পড়েছে, মুন্সিগঞ্জ/সিরাজগঞ্জের প্যাটার্নের পুনরাবৃত্তি।",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1325, "corrected_estimate": 2500, "confidence": "low — Mohadevpur station-এর অনুরূপ ধরা হয়েছে"}, "cn": {"old_value": None, "reviewed_estimate": 87, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "একই আত্রাই নদী"}},
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "regional নদী — discharge ও rainfall উভয়ই মোটামুটি সমান গুরুত্বপূর্ণ।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "নাটোরের গুড় নদী ও চলন বিল সিস্টেমের সাথে সংযুক্ত, চাঁপাইনবাবগঞ্জের পুনর্ভবাও এই এলাকায় প্রবাহিত।",
}