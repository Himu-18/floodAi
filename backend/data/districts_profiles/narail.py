# ============================================================
# FloodAI — data/district_profiles/narail.py — জেলা #৩০
# ⚠️ কোনো FFWC station নেই।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NARAIL_PROFILE = {
    "district": "নড়াইল", "district_lat": 22.97, "district_lon": 89.51,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False।",

    "river_structure": {
        "river": "মধুমতী (Madhumati)",
        "category": "large_regional (গড়াইয়ের ভাটির নাম — একই নদী, ভিন্ন নামকরণ)",
        "catchment": "🔍 Banglapedia: গড়াই ও মধুমতী আসলে একই নদী — উজানে 'গড়াই', ভাটিতে 'মধুমতী' নামে পরিচিত। কুষ্টিয়া/মাগুরার গবেষণা সরাসরি প্রযোজ্য।",
        "upstream_reference": "Kolkata, IN",
        "lag_time_hours": 36,
    },

    "danger_level_m": {"old_value": 7.0, "verdict": "❌ unverified — কোনো real gauge-এর সাথে যুক্ত না"},

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 700, "corrected_estimate": 4000, "corrected_range": "মাগুরার গড়াই থেকে সামান্য কম (আরো ভাটিতে, কিন্তু বোরদিয়ার আগে তাই এখনো বেশিরভাগ flow বহন করে)", "source": "কুষ্টিয়া/মাগুরা profile থেকে reuse", "confidence": "moderate — যদিও danger_level নিজেই unverified"},
        "cn": {"old_value": 73, "reviewed_estimate": 87, "confidence": "low-moderate"},
        "risk_category": {"old_value": "কম", "reviewed_estimate": "মাঝারি", "reasoning": "গড়াই সিস্টেমের ধারাবাহিকতা হিসেবে মাগুরার সাথে সঙ্গতি রাখতে upgrade"},
    },

    "flood_type": "Riverine",
    "inundation_bands": {"status": "⚠️ placeholder"},

    "soil_moisture_weight_note": "গড়াই সিস্টেমের একই যুক্তি।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "কুষ্টিয়া/মাগুরা/ঝিনাইদহের একই গড়াই-মধুমতী সিস্টেম — danger_level ঠিক করতে হলে নিকটতম real gauge (Kamarkhali/মাগুরা) থেকে proportionally extrapolate করা যেতে পারে।",

    "recommended_fix": "নিকটতম Kamarkhali (মাগুরা) gauge-কে secondary reference হিসেবে ব্যবহার করা যেতে পারে, নোয়াখালী/লালমনিরহাটের মতো 'ধার করা ডেটা' approach দিয়ে।",
}