# ============================================================
# FloodAI — data/district_profiles/magura.py — জেলা #২৮
# কুষ্টিয়ার গড়াই গবেষণা এখানে reuse করা হয়েছে।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MAGURA_PROFILE = {
    "district": "মাগুরা", "district_lat": 23.30, "district_lon": 89.47,
    "station_count": 1,
    "stations": [{
        "name": "Kamarkhali", "ffwc_id": "SW101B", "is_primary": True,
        "river": "গড়াই (Gorai)", "upazila": "Magura Sadar", "union": None,
        "river_structure": {
            "category": "large_regional", "catchment": "কুষ্টিয়ার Gorai-RB-র একই নদী, একটু ভাটিতে",
            "flow_behavior": "কুষ্টিয়ার মতোই ফারাক্কা-প্রভাবিত চরম মৌসুমি তারতম্য",
            "upstream_reference": "Kolkata, IN",
            "upstream_reference_note": "⚠️ কুষ্টিয়ার 'Malda,IN'-এর চেয়ে ভিন্ন — একই নদীর জন্য দুই জেলায় দুই ভিন্ন upstream reference ব্যবহার হচ্ছে, একটাতে সঙ্গতি আনা উচিত (Malda বেশি সঠিক, কারণ ফারাক্কা ব্যারাজ মালদা জেলাতেই)।",
            "lag_time_hours": 34,
        },
        "danger_level_m": 7.75, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 775, "corrected_estimate": 4500, "corrected_range": "কুষ্টিয়ার Gorai-RB-র থেকে সামান্য কম (ভাটিতে কিছুটা distributary loss)", "source": "কুষ্টিয়া profile থেকে reuse", "confidence": "moderate"},
            "cn": {"old_value": 74, "reviewed_estimate": 87, "confidence": "moderate"},
            "risk_category": {"old_value": "কম", "reviewed_estimate": "মাঝারি", "reasoning": "কুষ্টিয়ার সাথে সঙ্গতি রাখতে upgrade করা হলো — একই নদীর দুই জেলায় ভিন্ন risk tier (কম বনাম মাঝারি) যুক্তিসঙ্গত মনে হচ্ছে না"},
        },
        "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "কুষ্টিয়ার একই যুক্তি।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "কুষ্টিয়া/নড়াইলের সাথে একই গড়াই-মধুমতী সিস্টেম।",
}