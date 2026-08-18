# ============================================================
# FloodAI — data/district_profiles/patuakhali.py — জেলা #১৭
# ⚠️ কোনো FFWC station নেই (নোয়াখালী/লালমনিরহাটের মতো)।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

PATUAKHALI_PROFILE = {
    "district": "পটুয়াখালী",
    "district_lat": 22.26, "district_lon": 90.18,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False — স্বীকৃত unverified।",

    "river_structure": {
        "river": "পায়রা (Payra)",
        "category": "tidal_estuary",
        "catchment": "উপকূলীয় নদী, বঙ্গোপসাগরে সরাসরি মিশেছে — পায়রা বন্দর (deep-sea port) এই নদীর মোহনায়",
        "upstream_reference": "Agartala, IN",
        "upstream_reference_caveat": "❌ ভুল — coastal জেলা, Agartala/ত্রিপুরার সাথে সম্পর্কহীন",
        "lag_time_hours": 28,
    },

    "danger_level_m": {
        "old_value": 2.5,
        "verdict": "❌ unverified — কোনো real gauge-এর সাথে যুক্ত না",
    },

    "cyclone_context": {
        "sidr_2007": "পটুয়াখালী শহর সরাসরি ৫ মিটার (১৬ ফুট) উঁচু storm surge-এ আক্রান্ত হয়েছিল, ৩৮৫ জন নিহত হয়েছিল এই জেলায়",
        "remal_2024": "Great Danger Signal 10 জারি করা হয়েছিল, ৮-১২ ফুট উঁচু tidal surge-এর পূর্বাভাস দেওয়া হয়েছিল",
        "source": "CBS News (Sidr death toll by district), TBS/Prothom Alo (Remal ২০২৪ bulletin)",
    },

    "flood_type": "Coastal & Tidal",
    "flood_type_note": "✅ সঠিক দিক, কিন্তু cyclone storm-surge (নিয়মিত tidal cycle-এর চেয়ে ১০-১৬ ফুট বড় মাত্রার ঘটনা) আলাদাভাবে model করা উচিত।",

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 250, "corrected_estimate": None, "note": "danger_level নিজেই unverified, discharge_ratio concept এই তিদাল estuary-তে কম প্রাসঙ্গিক", "confidence": "none"},
        "cn": {"old_value": 77, "reviewed_estimate": 82, "confidence": "low"},
        "risk_category": {
            "old_value": "উচ্চ",
            "reviewed_estimate": "উচ্চ (অপরিবর্তিত)",
            "reasoning": "Sidr-এ ৩৮৫ মৃত্যু (দেশের মধ্যে ২য় সর্বোচ্চ, বরগুনার পরেই) — 'উচ্চ' সঠিক",
        },
    },

    "inundation_bands": {
        "note": "Sidr স্কেলে (৫ মিটার surge) পুরো উপকূলীয় এলাকা প্লাবিত",
        "status": "⚠️ placeholder — DEM/DFO বাকি",
    },

    "soil_moisture_weight_note": "cyclone/tidal-driven — soil_moisture কম প্রাসঙ্গিক, cyclone track/intensity forecast সবচেয়ে গুরুত্বপূর্ণ (মডেলে অনুপস্থিত)।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",

    "recommended_fix": "নোয়াখালীর মতোই — discharge-ভিত্তিক ১৪-feature মডেলের বদলে BMD cyclone bulletin + tidal-cycle ডেটা-ভিত্তিক আলাদা approach দরকার এই coastal belt-এর জন্য।",
}