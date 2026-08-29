# ============================================================
# FloodAI — data/district_profiles/pabna.py — জেলা #৩৮
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

PABNA_PROFILE = {
    "district": "পাবনা", "district_lat": 24.01, "district_lon": 89.23,
    "station_count": 2, "station_count_note": "✅ দুইটা station-ই flood_config.py-তে সঠিকভাবে linked।",

    "stations": [
        {
            "name": "Mathura", "ffwc_id": "SW50.3", "is_primary": True,
            "river": "যমুনা/ব্রহ্মপুত্র (Brahmaputra-Jamuna)", "upazila": "Bera", "union": None,
            "river_structure": {"category": "mega_trunk", "catchment": "যমুনার পশ্চিম তীরের জেলা — মানিকগঞ্জ/সিরাজগঞ্জের একই যমুনা, ভাটির দিকে (পদ্মার সাথে মেশার আগে)", "upstream_reference": "Malda, IN", "upstream_reference_caveat": "⚠️ প্রশ্নসাপেক্ষ — যমুনার জন্য 'Guwahati,IN' (সিরাজগঞ্জ/মানিকগঞ্জের মতো) বেশি সঠিক হতো, 'Malda,IN' পদ্মার জন্য প্রযোজ্য, দুই নদী সিস্টেম গুলিয়ে ফেলা হয়েছে বলে মনে হচ্ছে", "lag_time_hours": 40},
            "danger_level_m": 9.60, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 960, "corrected_estimate": 50000, "corrected_range": "মানিকগঞ্জ/সিরাজগঞ্জের যমুনা রেফারেন্স reuse", "source": "মানিকগঞ্জ profile থেকে reuse", "confidence": "moderate-high"},
                "cn": {"old_value": 75, "reviewed_estimate": 89, "confidence": "moderate"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "mega_trunk যমুনার সরাসরি সংস্পর্শ, সিরাজগঞ্জ/মানিকগঞ্জের সাথে সঙ্গতি রাখতে upgrade"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Hardinge-RB", "ffwc_id": "SW90", "is_primary": False,
            "river": "গঙ্গা (Ganges)", "upazila": "Ishwardi", "union": None,
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "🔍 এটা বাংলাদেশের সবচেয়ে ঐতিহাসিকভাবে গুরুত্বপূর্ণ গঙ্গা "
                    "gauge — Hardinge Bridge, ১৯১৫ সালে নির্মিত, ব্রিটিশ আমল থেকেই "
                    "গঙ্গার প্রধান পরিমাপ কেন্দ্র। Bahadurabad (যমুনার জন্য) এবং "
                    "Hardinge Bridge (গঙ্গার জন্য) — এই দুইটাই GBM ব-দ্বীপের "
                    "সবচেয়ে বেশি ব্যবহৃত রেফারেন্স গেজ, satellite altimetry "
                    "গবেষণাতেও এই দুই পয়েন্টকেই standard হিসেবে ধরা হয়।"
                ),
                "upstream_reference": "Malda, IN", "lag_time_hours": 40,
            },
            "danger_level_m": 13.80, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1380, "corrected_estimate": 75000, "corrected_range": "রাজবাড়ীর গঙ্গা রেফারেন্স — এটা প্রকৃতপক্ষে সবচেয়ে authoritative গঙ্গা gauge, ভবিষ্যতে বাকি সব গঙ্গা-স্টেশনের জন্য এটাকে primary reference source হিসেবে ব্যবহার করা যেতে পারে (⚠️ ২০২৬-০৮-২৮: আগে এখানে stale mean-annual ৩০,০০০ ছিল — রাজবাড়ীর reference bankfull-এ ঠিক করার সময় এই কপি sync হয়নি)", "confidence": "high — সবচেয়ে বেশি cite করা reference gauge"},
                "cn": {"old_value": None, "reviewed_estimate": 88, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "mega_trunk গঙ্গার সবচেয়ে বিখ্যাত gauge পয়েন্ট"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "দুইটাই mega_trunk — discharge primary।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই, কিন্তু পাবনা আসলে যমুনা ও গঙ্গা উভয়েরই সংস্পর্শে (রাজবাড়ী/মানিকগঞ্জের confluence অঞ্চলের কাছাকাছি, প্রায় একটা তৃতীয় confluence-adjacent জেলা)।",
    "cross_district_note": "Hardinge Bridge গেজ ভবিষ্যতে সব গঙ্গা-সংশ্লিষ্ট জেলার (রাজবাড়ী/রাজশাহী/কুষ্টিয়া/চাঁপাইনবাবগঞ্জ) জন্য primary cross-reference source হতে পারে — এটা সবচেয়ে established measurement point।",
}