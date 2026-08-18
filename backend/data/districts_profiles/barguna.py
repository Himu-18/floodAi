# ============================================================
# FloodAI — data/district_profiles/barguna.py — জেলা #১৮
# ⚠️ কোনো FFWC station নেই।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BARGUNA_PROFILE = {
    "district": "বরগুনা",
    "district_lat": 22.06, "district_lon": 89.97,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False।",

    "river_structure": {
        "river": "বিষখালী (Bishkhali) + বলেশ্বর (Baleshwar)",
        "category": "tidal_estuary",
        "catchment": "দুইটা নদীর মোহনার মাঝখানে অবস্থিত জেলা — Patharghata উপজেলা বিশেষভাবে ঝুঁকিপূর্ণ",
        "upstream_reference": "Agartala, IN",
        "upstream_reference_caveat": "❌ ভুল — একই সমস্যা",
        "lag_time_hours": 30,
    },

    "danger_level_m": {"old_value": 2.5, "verdict": "❌ unverified"},

    "cyclone_context": {
        "sidr_2007": (
            "⚠️⚠️ বরগুনা ছিল Sidr(২০০৭)-এর সবচেয়ে বেশি ক্ষতিগ্রস্ত জেলা — "
            "৪৭৪ জন নিহত (দেশের মধ্যে সর্বোচ্চ), Sharankhola-এর কাছাকাছি "
            "এলাকায় প্রায় সবকিছু ধ্বংস হয়ে গিয়েছিল। ৫ মিটার (১৬ ফুট) storm surge।"
        ),
        "remal_2024": (
            "Patharghata উপজেলায় বিষখালী ও বলেশ্বরী নদী danger level-এর ৫০ সেমি "
            "উপরে উঠেছিল, বাঁধ দুর্বল হয়ে পড়েছিল (BWDB নির্বাহী প্রকৌশলী Md "
            "Rakib নিশ্চিত করেছেন), ৮০০টা geo-bag প্রস্তুত রাখা হয়েছিল জরুরি "
            "মেরামতের জন্য।"
        ),
        "source": "CBS News (Sidr মৃত্যুর তথ্য), TBS (Remal, BWDB প্রকৌশলীর বিবৃতি)",
    },

    "flood_type": "Coastal & Tidal",
    "flood_type_note": "✅ সঠিক দিক — বরগুনা এই framework-এ সবচেয়ে ঐতিহাসিকভাবে cyclone-বিধ্বস্ত জেলা (Sidr-এ সর্বোচ্চ মৃত্যু)।",

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 250, "corrected_estimate": None, "confidence": "none"},
        "cn": {"old_value": 77, "reviewed_estimate": 82, "confidence": "low"},
        "risk_category": {
            "old_value": "উচ্চ",
            "reviewed_estimate": "উচ্চ (অপরিবর্তিত — যদিও যুক্তি দেওয়া যায় 'অতি উচ্চ'-এ upgrade করার, ফেনীর মতো)",
            "reasoning": (
                "Sidr-এ ৪৭৪ মৃত্যু (দেশের সর্বোচ্চ, ফেনীর ২০২৪-এর ২৮ মৃত্যুর "
                "চেয়েও অনেক বেশি) — ঐতিহাসিক ভিত্তিতে এটা 'অতি উচ্চ' প্রাপ্য "
                "হতে পারে, ফেনীর মতোই। তবে ঘন ঘন না, একটামাত্র extreme cyclone "
                "event-এর ভিত্তিতে upgrade করা উচিত কিনা সেটা বিবেচনার বিষয়, "
                "তাই এখানে 'উচ্চ' অপরিবর্তিত রাখা হলো conservative choice হিসেবে।"
            ),
            "source": "CBS News (Sidr death toll — Barguna 474, Patuakhali 385)",
        },
    },

    "inundation_bands": {
        "note": "Sidr-এ Sharankhola/Patharghata এলাকায় প্রায় সম্পূর্ণ ধ্বংসের রেকর্ড",
        "status": "⚠️ placeholder — DEM/DFO বাকি",
    },

    "soil_moisture_weight_note": "cyclone/tidal-driven — soil_moisture কম প্রাসঙ্গিক।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",

    "recommended_fix": "নোয়াখালী/পটুয়াখালীর মতো — rainfall+tidal-surge/cyclone-bulletin-ভিত্তিক আলাদা approach দরকার।",
}