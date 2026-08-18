# ============================================================
# FloodAI — data/district_profiles/brahmanbaria.py — জেলা #৪০
# ⚠️ flood_type='Dam-Affected' সম্ভবত ভুল — নিচে বিস্তারিত।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BRAHMANBARIA_PROFILE = {
    "district": "ব্রাহ্মণবাড়িয়া", "district_lat": 23.96, "district_lon": 91.11,
    "station_count": 1,
    "stations": [{
        "name": "B. Baria", "ffwc_id": "SW3A", "is_primary": True,
        "river": "তিতাস (Titas)", "upazila": "B. Baria Sadar", "union": None,
        "river_structure": {
            "category": "medium (মেঘনার একটা অস্বাভাবিক লুপ-আকৃতির distributary)",
            "catchment": (
                "🔍 তিতাস আসলে মেঘনা থেকেই বের হয়ে (চাতলপাড়ের কাছে, ব্রাহ্মণবাড়িয়া) "
                "প্রায় ২৪০ কিমি ঘুরে আবার নবীনগর উপজেলার কাছে মেঘনাতেই ফিরে মেশে — "
                "একটা loop-আকৃতির distributary, উজানে কোনো dam/ব্যারাজ নেই।"
            ),
            "upstream_reference": "Agartala, IN", "lag_time_hours": 14,
        },
        "danger_level_m": 5.05, "verified_source": "flood_config.py-র সাথে মিলেছে",

        "critical_finding": {
            "issue": "⚠️⚠️ flood_type='Dam-Affected' সম্ভবত ভুল classification",
            "evidence": "একাধিক সূত্র (Banglapedia, Wikipedia, স্থানীয় সরকারি ওয়েবসাইট) তিতাস নদীকে মেঘনার একটা loop-distributary হিসেবে বর্ণনা করেছে — কোথাও কোনো dam/ব্যারাজের উল্লেখ নেই। এটা কুমিল্লার গোমতী (ডুম্বুর বাঁধ) থেকে সম্পূর্ণ ভিন্ন — তিতাসের flooding মূলত মেঘনার backwater effect ও স্থানীয় বৃষ্টির কারণে, কোনো upstream ব্যারাজ-গেট অপারেশনের কারণে না।",
            "recommendation": "flood_type='Riverine' (মেঘনা-backwater-প্রভাবিত) বেশি সঠিক হবে — ফেনীর মতোই এখানে সম্ভবত ভুল category লাগানো হয়েছে।",
        },

        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 505, "corrected_estimate": 1500, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, মেঘনার loop-distributary হিসেবে conservative অনুমান", "confidence": "low"},
            "cn": {"old_value": 81, "reviewed_estimate": 85, "confidence": "low-moderate"},
            "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত)", "reasoning": "উপন্যাস 'তিতাস একটি নদীর নাম'-এর মাধ্যমে বিখ্যাত, নিয়মিত বন্যাপ্রবণ এলাকা হিসেবে পরিচিত, upgrade/downgrade-এর প্রয়োজন নেই"},
        },

        "flood_type": "Dam-Affected",
        "flood_type_note": "⚠️⚠️ উপরে critical_finding দ্রষ্টব্য — সম্ভবত ভুল, 'Riverine' হওয়া উচিত",

        "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "মেঘনার backwater-প্রভাবিত distributary — discharge_ratio-র চেয়ে মেঘনার নিজস্ব water level (কিশোরগঞ্জ/নরসিংদীর মতো) বেশি প্রাসঙ্গিক predictor হতে পারে।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই, কিন্তু মেঘনার সাথে backwater-সংযুক্ত।",
    "cross_district_note": "কুমিল্লার গোমতীর সাথে ভৌগোলিকভাবে কাছাকাছি কিন্তু hydrology সম্পূর্ণ ভিন্ন (dam vs no-dam)।",
}