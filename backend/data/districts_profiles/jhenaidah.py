# ============================================================
# FloodAI — data/district_profiles/jhenaidah.py — জেলা #২৯
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

JHENAIDAH_PROFILE = {
    "district": "ঝিনাইদহ", "district_lat": 23.54, "district_lon": 89.15,
    "station_count": 0,
    "station_count_note": (
        "⚠️ stations.py-তে কোনো entry নেই, কিন্তু flood_config.py-তে একটা আকর্ষণীয় "
        "আংশিক-কাজ পাওয়া গেছে — 'ffwc_station': 'Jhenaidah Sadar pillar point "
        "(Nabaganga, BWDB BM pillar list — danger_level unverified)', "
        "'ffwc_verified': 'coordinate-only'। মানে কেউ (সম্ভবত আরেকটা session-এ) "
        "BWDB Hydrology-র BM Pillar List থেকে coordinate বের করতে পেরেছিল, কিন্তু "
        "danger_level যাচাই করতে পারেনি — এটা প্রমাণ করে যে BWDB সাইট থেকে সত্যিই "
        "ডেটা বের করা সম্ভব (তুমি আগে যা বলেছিলে), শুধু আমার fetch tool দিয়ে না।"
    ),

    "river_structure": {
        "river": "নবগঙ্গা (Nabaganga)",
        "category": "medium (গড়াইয়ের branch)",
        "catchment": "গড়াই বোরদিয়া পয়েন্টে নবগঙ্গা ও মধুমতীতে ভাগ হয় — মোট দৈর্ঘ্য ২৩০ কিমি (কুষ্টিয়ায় ২৬ কিমি, যশোরে ২০৪ কিমি)",
        "upstream_reference": "Kolkata, IN",
        "lag_time_hours": 32,
    },

    "danger_level_m": {"old_value": 7.0, "verdict": "⚠️ coordinate আছে কিন্তু danger_level এখনো unverified — কোডেই স্বীকৃত"},

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 700, "corrected_estimate": 1500, "corrected_range": "গড়াইয়ের branch হিসেবে, মূল গড়াই (৪,৫০০-৫,০০০)-এর একটা অংশ পাবে — bifurcation-এর কারণে কম", "confidence": "low"},
        "cn": {"old_value": 73, "reviewed_estimate": 87, "confidence": "low-moderate"},
        "risk_category": {"old_value": "কম", "reviewed_estimate": "মাঝারি", "reasoning": "গড়াই সিস্টেমের অংশ হিসেবে মাগুরা/কুষ্টিয়ার সাথে সঙ্গতি রাখতে upgrade"},
    },

    "flood_type": "Riverine",
    "inundation_bands": {"status": "⚠️ placeholder"},

    "soil_moisture_weight_note": "গড়াই সিস্টেমের একই যুক্তি।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "কুষ্টিয়া/মাগুরা/নড়াইলের একই গড়াই-মধুমতী-নবগঙ্গা সিস্টেম।",

    "recommended_fix": "danger_level real BWDB pillar data দিয়ে verify করা দরকার — coordinate কাজটা আংশিক হয়ে আছে, সম্পূর্ণ করা তুলনামূলক সহজ হবে।",
}