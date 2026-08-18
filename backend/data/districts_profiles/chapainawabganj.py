# ============================================================
# FloodAI — data/district_profiles/chapainawabganj.py — জেলা #৩৫
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

CHAPAINAWABGANJ_PROFILE = {
    "district": "চাঁপাইনবাবগঞ্জ", "district_lat": 24.60, "district_lon": 88.28,
    "station_count": 3, "station_count_note": "✅ তিনটা station-ই flood_config.py-তে সঠিকভাবে linked।",
    "stations": [
        {
            "name": "Pankha", "ffwc_id": "SW88A", "is_primary": True,
            "river": "পদ্মা/গঙ্গা (Ganges/Padma)", "upazila": "Shibganj", "union": None,
            "river_structure": {"category": "mega_trunk", "catchment": "বাংলাদেশের ভূখণ্ডে গঙ্গার সবচেয়ে উজানের পয়েন্ট — ভারত সীমান্তের ঠিক কাছে, danger_level এই framework-এ সবচেয়ে বেশি (২২.০৫)", "upstream_reference": "Malda, IN", "lag_time_hours": 36},
            "danger_level_m": 22.05, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 2205, "corrected_estimate": 75000, "corrected_range": "bankfull — একই গঙ্গা trunk রেফারেন্স (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল), যদিও এত উজানে discharge সামান্য কম হতে পারে (কম উপনদী যুক্ত হয়েছে)", "confidence": "moderate"},
                "cn": {"old_value": 73, "reviewed_estimate": 88, "confidence": "moderate"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "রাজশাহীর সাথে সঙ্গতি রাখতে upgrade"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "C-Nawabganj", "ffwc_id": "SW211.5", "is_primary": False,
            "river": "মহানন্দা (Mohananda)", "upazila": "Nawabganj Sadar", "union": None,
            "river_structure": {"category": "medium (transboundary, ভারতের মালদা থেকে সরাসরি)", "catchment": "ভারতের মালদা জেলা থেকে সরাসরি প্রবাহিত, খুবই নিকটবর্তী উৎস তাই lag time কম হওয়ার কথা", "upstream_reference": "Malda, IN", "upstream_reference_note": "✅ বিশেষভাবে সঠিক এই স্টেশনের জন্য — মহানন্দা আক্ষরিক অর্থেই মালদা থেকে আসে", "lag_time_hours": 36},
            "danger_level_m": 20.55, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 2055, "corrected_estimate": 1500, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "transboundary মাঝারি নদী"}},
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Rohanpur", "ffwc_id": "SW238", "is_primary": False,
            "river": "পুনর্ভবা (Punarvaba)", "upazila": "Gomastapur", "union": None,
            "river_structure": {"category": "medium (transboundary)", "catchment": "ভারত থেকে আসা আরেকটা সীমান্ত নদী, নওগাঁর দিকে প্রবাহিত", "upstream_reference": "Malda, IN", "lag_time_hours": 36},
            "danger_level_m": 21.55, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 2155, "corrected_estimate": 1200, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "C-Nawabganj-এর অনুরূপ"}},
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],
    "soil_moisture_weight_note": "primary station-এ discharge primary; দুই secondary transboundary নদীতে local+upstream rain দুটোই প্রাসঙ্গিক।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "রাজশাহীর সাথে একই গঙ্গা trunk; পুনর্ভবা নওগাঁর দিকেও প্রবাহিত।",
}