# ============================================================
# FloodAI — data/district_profiles/narsingdi.py — জেলা #৪৪
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NARSINGDI_PROFILE = {
    "district": "নরসিংদী", "district_lat": 23.93, "district_lon": 90.72,
    "station_count": 1,
    "stations": [{
        "name": "Narsingdi", "ffwc_id": "SW274", "is_primary": True,
        "river": "মেঘনা (Meghna)", "upazila": "Narsingdi Sadar", "union": None,
        "river_structure": {
            "category": "mega_trunk", "catchment": "নারায়ণগঞ্জের Bayderbazar (২৩.৭৫,৯০.৭)-র প্রায় একই এলাকা (২৩.৯৩,৯০.৭২) — একই মেঘনা reach, কিশোরগঞ্জের Bhairab Bazar-এর একটু ভাটিতে",
            "upstream_reference": "Agartala, IN",
            "upstream_reference_caveat": "⚠️ প্রশ্নসাপেক্ষ — কিশোরগঞ্জের মতোই এই মেঘনার উৎস মেঘালয়+পুরনো ব্রহ্মপুত্র (Shillong/Guwahati দিক), আগরতলা/ত্রিপুরা না",
            "lag_time_hours": 18,
        },
        "danger_level_m": 5.25, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 525, "corrected_estimate": 4600, "corrected_range": "কিশোরগঞ্জের Bhairab Bazar থেকে reuse (একই মেঘনা reach-এর কাছাকাছি)", "source": "কিশোরগঞ্জ profile থেকে reuse", "confidence": "moderate"},
            "cn": {"old_value": 79, "reviewed_estimate": 87, "confidence": "moderate"},
            "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "mega_trunk মেঘনার সরাসরি সংস্পর্শ, কিশোরগঞ্জ/নারায়ণগঞ্জের সাথে সঙ্গতি রাখতে upgrade"},
        },
        "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "mega_trunk মেঘনা — discharge primary।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই, কিন্তু মেঘনা করিডোরের অংশ (কিশোরগঞ্জ→নরসিংদী→নারায়ণগঞ্জ→চাঁদপুর)।",
    "cross_district_note": "কিশোরগঞ্জ/নারায়ণগঞ্জ/চাঁদপুরের সাথে একই মেঘনা trunk — চারটা জেলা একসাথে দেখলে পুরো মেঘনা করিডোরের discharge profile তৈরি করা সম্ভব।",
}