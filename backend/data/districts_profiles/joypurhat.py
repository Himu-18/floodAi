# ============================================================
# FloodAI — data/district_profiles/joypurhat.py — জেলা #৩৯
# ঝিনাইদহের মতোই আংশিক BWDB coordinate-কাজ পাওয়া গেছে।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

JOYPURHAT_PROFILE = {
    "district": "জয়পুরহাট", "district_lat": 25.10, "district_lon": 89.02,
    "station_count": 0,
    "station_count_note": (
        "⚠️ stations.py-তে কোনো entry নেই। কিন্তু ঝিনাইদহের মতোই flood_config.py-তে "
        "'ffwc_station': 'Akkelpur pillar point (Tulshiganga, BWDB BM pillar list "
        "— danger_level unverified)', 'ffwc_verified': 'coordinate-only' — মানে "
        "এখানেও কেউ আগে BWDB থেকে coordinate বের করেছিল কিন্তু danger_level verify "
        "করতে পারেনি। এই একই প্যাটার্ন এখন ২টা জেলায় (ঝিনাইদহ, জয়পুরহাট) পাওয়া "
        "গেলো — সম্ভবত আরো কিছু 'zero-station' জেলাতেও এই আংশিক কাজ থাকতে পারে, "
        "চেক করা উচিত।"
    ),

    "river_structure": {
        "river": "তুলসীগঙ্গা (Tulshiganga)",
        "category": "medium",
        "catchment": "বরেন্দ্র অঞ্চলের স্থানীয় নদী, আক্কেলপুর উপজেলার মধ্য দিয়ে প্রবাহিত",
        "upstream_reference": "Malda, IN",
        "lag_time_hours": 20,
    },

    "danger_level_m": {"old_value": 8.5, "verdict": "⚠️ coordinate আছে কিন্তু danger_level unverified — ঝিনাইদহের মতোই আংশিক কাজ"},

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 850, "corrected_estimate": 500, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, ছোট বরেন্দ্র-অঞ্চল নদী হিসেবে conservative অনুমান", "confidence": "low"},
        "cn": {"old_value": 76, "reviewed_estimate": 82, "reasoning": "বরেন্দ্র অঞ্চল তুলনামূলক শুষ্ক/উঁচু ভূমি, অন্যান্য জেলার প্লাবনভূমির চেয়ে কম CN যুক্তিসঙ্গত", "confidence": "low"},
        "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "নির্দিষ্ট তথ্যের অভাবে conservative রাখা হলো"},
    },

    "flood_type": "Riverine",
    "inundation_bands": {"status": "⚠️ placeholder"},

    "soil_moisture_weight_note": "বরেন্দ্র অঞ্চল — অন্যান্য প্লাবনভূমি জেলার চেয়ে ভিন্ন soil/drainage characteristic থাকতে পারে, আরো গবেষণা দরকার।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "নওগাঁর সাথে ভৌগোলিকভাবে কাছাকাছি, একই বরেন্দ্র অঞ্চল।",

    "recommended_fix": "ঝিনাইদহের মতোই — danger_level verify করা প্রয়োজন। BWDB coordinate কাজটা কীভাবে করা হয়েছিল সেটা reproduce করতে পারলে বাকি 'zero-station' জেলাগুলোতেও একই পদ্ধতি প্রয়োগ করা যেতে পারে।",
}