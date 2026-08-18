# ============================================================
# FloodAI — data/district_profiles/gopalganj.py — জেলা #৪৫
# কুষ্টিয়া/মাগুরা/নড়াইলের গড়াই-মধুমতী গবেষণা এখানে reuse করা হয়েছে।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

GOPALGANJ_PROFILE = {
    "district": "গোপালগঞ্জ", "district_lat": 23.01, "district_lon": 89.83,
    "station_count": 1,
    "stations": [{
        "name": "Haridaspur", "ffwc_id": "SW198", "is_primary": True,
        "river": "মধুমতী (Madhumati)", "upazila": "Gopalganj Sadar", "union": None,
        "river_structure": {
            "category": "large_regional (গড়াই-মধুমতী সিস্টেমের সবচেয়ে ভাটির অংশ)",
            "catchment": "কুষ্টিয়া→মাগুরা→নড়াইল→গোপালগঞ্জ — একই গড়াই-মধুমতী নদী, এখানে সবচেয়ে ভাটিতে, বরিশাল অঞ্চলের বিল-জলাভূমির কাছাকাছি",
            "note": "flood_config.py-তে ffwc_station নাম 'Madaripur BR' (Madaripur Beel Route) লেখা — এটা মধুমতীরই একটা স্থানীয় নামকরণ এই reach-এ, বিভ্রান্তিকর মনে হলেও একই নদী।",
            "upstream_reference": "Malda, IN", "lag_time_hours": 48,
        },
        "danger_level_m": 3.35, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 335, "corrected_estimate": 3000, "corrected_range": "মধুমতী সিস্টেমের সবচেয়ে ভাটির অংশ — নড়াইলের চেয়ে কিছুটা কম (বিল-অঞ্চলে flow ছড়িয়ে যাওয়ায়)", "source": "নড়াইল/মাগুরা profile থেকে reuse ও সমন্বয়", "confidence": "moderate"},
            "cn": {"old_value": 76, "reviewed_estimate": 88, "reasoning": "বিল-জলাভূমি অঞ্চল — উচ্চ CN যুক্তিসঙ্গত", "confidence": "moderate"},
            "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "গড়াই সিস্টেমের অন্য জেলার সাথে সঙ্গতিপূর্ণ ইতিমধ্যে"},
        },
        "flood_type": "Riverine",
        "flood_type_note": "বিল-জলাভূমি অঞ্চলের কারণে drainage-congestion characteristic থাকতে পারে (নাটোরের চলন বিলের মতো, কিশোরগঞ্জের হাওরের মতো)।",
        "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "বিল-অঞ্চল drainage-congestion — নাটোর/কিশোরগঞ্জের মতো slow-drainage dynamics বিবেচনায় নেওয়া উচিত।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "কুষ্টিয়া/মাগুরা/নড়াইলের একই গড়াই-মধুমতী সিস্টেমের শেষ প্রান্ত — এই চার জেলা একসাথে সম্পূর্ণ নদীর যাত্রাপথ তৈরি করে।",
}