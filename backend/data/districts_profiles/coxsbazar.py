# ============================================================
# FloodAI — data/district_profiles/coxsbazar.py — জেলা #৪৩
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

COXSBAZAR_PROFILE = {
    "district": "কক্সবাজার", "district_lat": 21.68, "district_lon": 91.92,
    "station_count": 1,
    "stations": [{
        "name": "Chiringa", "ffwc_id": "SW204", "is_primary": True,
        "river": "মাতামুহুরী (Matamuhuri)", "upazila": "Chakaria", "union": None,
        "river_structure": {
            "category": "small (পার্বত্য চট্টগ্রাম/মিয়ানমার সীমান্তের কাছাকাছি উৎস, ফেনী নদীর মতোই narrow ও flashy)",
            "catchment": "বান্দরবানের পাহাড় থেকে সরাসরি নেমে আসা, চকরিয়া হয়ে সাগরে পতিত",
            "upstream_reference": "Agartala, IN",
            "upstream_reference_caveat": "⚠️ সম্ভবত ভুল — মাতামুহুরীর উৎস বান্দরবানের পাহাড়ে (মিয়ানমার সীমান্তের কাছাকাছি), ত্রিপুরা/আগরতলা থেকে অনেক দূরে দক্ষিণে। শেরপুরের ভুগাইয়ের মতোই copy-paste সমস্যা মনে হচ্ছে।",
            "lag_time_hours": 8,
            "lag_time_note": "✅ ইতিমধ্যে খুবই কম বসানো ছিল (ফেনীর ৬ ঘণ্টার পরেই ২য় সবচেয়ে কম) — flashy hill-river-এর জন্য যুক্তিসঙ্গত",
        },
        "danger_level_m": 5.80, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 580, "corrected_estimate": 300, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, ফেনী/শেরপুরের ছোট flashy নদীর প্যাটার্নের সাথে তুলনীয় ধরা হয়েছে", "confidence": "low"},
            "cn": {"old_value": 85, "reviewed_estimate": 87, "reasoning": "ইতিমধ্যে উচ্চ ও প্রায় সঠিক ছিল", "confidence": "moderate"},
            "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত)", "reasoning": "চকরিয়া উপজেলা নিয়মিত flash-flood-আক্রান্ত, cyclone-এর ঝুঁকিও যুক্ত (উপকূলীয়) — 'উচ্চ' যথাযথ"},
        },
        "flood_type": "Flash Flood",
        "flood_type_note": "✅ সঠিক শ্রেণীবিভাগ — তবে কক্সবাজার cyclone-ঝুঁকিতেও (Coastal & Tidal) আছে, একটামাত্র flood_type জেলার সম্পূর্ণ চিত্র দেয় না।",
        "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "ফেনী/শেরপুরের একই যুক্তি — rainfall সবচেয়ে গুরুত্বপূর্ণ predictor।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "বান্দরবানের সাথে ভৌগোলিকভাবে সংযুক্ত (একই পার্বত্য উৎস)।",
}