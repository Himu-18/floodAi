# ============================================================
# FloodAI — data/district_profiles/natore.py — জেলা #৩৬
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NATORE_PROFILE = {
    "district": "নাটোর", "district_lat": 24.27, "district_lon": 89.00,
    "station_count": 1,
    "stations": [{
        "name": "Singra", "ffwc_id": "SW147.5", "is_primary": True,
        "river": "গুড় (Gur)", "upazila": "Singra", "union": None,
        "river_structure": {
            "category": "medium (আত্রাই সিস্টেমের সাথে সংযুক্ত স্থানীয় নদী)",
            "catchment": "নওগাঁর আত্রাই নদীর কাছাকাছি এলাকা দিয়ে প্রবাহিত, উত্তরাঞ্চলের নিচু চলন বিল অঞ্চলের অংশ",
            "upstream_reference": "Malda, IN", "lag_time_hours": 28,
        },
        "danger_level_m": 12.20, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 1220, "corrected_estimate": 1000, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, medium category অনুমান", "confidence": "low"},
            "cn": {"old_value": 76, "reviewed_estimate": 88, "reasoning": "চলন বিল অঞ্চলের নিচু জলাভূমি — উচ্চ CN যুক্তিসঙ্গত", "confidence": "low-moderate"},
            "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "নির্দিষ্ট বড় বন্যার ইতিহাস খুঁজে পাওয়া যায়নি"},
        },
        "flood_type": "Riverine",
        "flood_type_note": "চলন বিল (দেশের সবচেয়ে বড় বিল অঞ্চলগুলোর একটা) অঞ্চলের কারণে drainage-congestion characteristic থাকতে পারে, শুধু classic riverine না।",
        "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "চলন বিল অঞ্চলের কারণে drainage congestion বিবেচনায় নেওয়া উচিত।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "নওগাঁর আত্রাই সিস্টেমের সাথে ভৌগোলিকভাবে সংযুক্ত।",
}