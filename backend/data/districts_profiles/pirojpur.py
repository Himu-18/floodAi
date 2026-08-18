# ============================================================
# FloodAI — data/district_profiles/pirojpur.py — জেলা #১৯
# ⚠️ কোনো FFWC station নেই।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

PIROJPUR_PROFILE = {
    "district": "পিরোজপুর",
    "district_lat": 22.38, "district_lon": 89.82,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False।",

    "river_structure": {
        "river": "বলেশ্বর (Baleshwar)",
        "category": "tidal_estuary",
        "catchment": "সুন্দরবনের সংলগ্ন উপকূলীয় নদী, বলেশ্বরের ব্যাপক surge-amplification zone (Morelganj পর্যন্ত ৫০ কিমি বিস্তৃত, journal অনুযায়ী)",
        "upstream_reference": "Agartala, IN",
        "upstream_reference_caveat": "❌ ভুল — একই সমস্যা",
        "lag_time_hours": 28,
    },

    "danger_level_m": {"old_value": 3.5, "verdict": "❌ unverified"},

    "cyclone_context": {
        "note": "Journal of Bangladesh Institute of Planners-এর গবেষণা অনুযায়ী বলেশ্বর নদীর মোহনা থেকে Morelganj পর্যন্ত (৫০ কিমি উজানে) উচ্চ storm surge পৌঁছায় — Sidr-এ Patharghata পয়েন্টে surge ৫.৫-৬ মিটার (PWD datum) রেকর্ড হয়েছিল।",
        "source": "Journal of Bangladesh Institute of Planners (storm surge modeling study, Barguna/Bishkhali-Baleshwar)",
    },

    "flood_type": "Coastal & Tidal",
    "flood_type_note": "✅ সঠিক দিক।",

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 350, "corrected_estimate": None, "confidence": "none"},
        "cn": {"old_value": 76, "reviewed_estimate": 81, "confidence": "low"},
        "risk_category": {
            "old_value": "মাঝারি",
            "reviewed_estimate": "উচ্চ",
            "reasoning": "Remal(২০২৪)-এ 'severely affected districts'-এর তালিকায় পিরোজপুর নির্দিষ্টভাবে উল্লেখিত ছিল (TBS রিপোর্ট), Great Danger Signal 10-এর আওতায় ছিল — প্রতিবেশী সব coastal জেলা (ভোলা/পটুয়াখালী/বরগুনা/ঝালকাঠি) 'উচ্চ' থাকলে পিরোজপুরের 'মাঝারি' থাকাটা inconsistent মনে হচ্ছে।",
            "source": "TBS News (Remal ২০২৪ — 'severely affected districts' তালিকা)",
        },
    },

    "inundation_bands": {"status": "⚠️ placeholder — DEM/DFO বাকি"},

    "soil_moisture_weight_note": "cyclone/tidal-driven।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",

    "recommended_fix": "একই coastal-belt approach দরকার।",
}