# ============================================================
# FloodAI — data/district_profiles/barisal.py — জেলা #১৬
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BARISAL_PROFILE = {
    "district": "বরিশাল",
    "district_lat": 22.72, "district_lon": 90.45,
    "station_count": 1,
    "stations": [{
        "name": "Barisal", "ffwc_id": "SW18", "is_primary": True,
        "river": "কীর্তনখোলা (Kirtonkhola)", "upazila": "Barisal Sadar", "union": "Char Kowa",
        "river_structure": {
            "category": "tidal_river (মেঘনার একটা শাখা, জোয়ার-ভাটা প্রভাবিত কিন্তু ভোলার মতো সরাসরি মোহনা না — একটু ভেতরে)",
            "catchment": "বরিশাল শহর কীর্তনখোলা নদীর তীরে, মেঘনা বদ্বীপের অভ্যন্তরীণ নদী-বন্দর",
            "flow_behavior": "জোয়ার-ভাটা প্রভাবিত, কিন্তু ভোলার Lower Meghna-র চেয়ে কম সরাসরি সাগরের সংস্পর্শে",
            "upstream_reference": "Agartala, IN",
            "upstream_reference_caveat": "⚠️ একই সমস্যা — অপ্রাসঙ্গিক",
            "lag_time_hours": 30,
        },
        "danger_level_m": 2.10, "highest_recorded_m": 2.79,
        "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 210, "corrected_estimate": None, "note": "tidal river — discharge_ratio কম অর্থবহ", "confidence": "low"},
            "cn": {"old_value": 76, "reviewed_estimate": 80, "confidence": "low"},
            "risk_category": {
                "old_value": "মাঝারি",
                "reviewed_estimate": "উচ্চ",
                "reasoning": "Remal(২০২৪)-এ বরিশাল বিভাগে ১০০ কিমি/ঘণ্টার বেশি বাতাসের রেকর্ড হয়েছিল, একাধিক মৃত্যু রিপোর্ট হয়েছিল বরিশালে — 'মাঝারি' কম মনে হচ্ছে অন্য coastal জেলার (সব 'উচ্চ') তুলনায়।",
                "source": "TBS (Remal ২০২৪ কভারেজ — বরিশালে মৃত্যুর তালিকায় উল্লেখ)",
            },
        },
        "flood_type": "Riverine",
        "flood_type_note": "⚠️ ভোলা/অন্য coastal জেলার 'Coastal & Tidal'-এর তুলনায় ভিন্ন classification — বরিশাল শহর একটু ভেতরে হওয়ায় এটা যুক্তিসঙ্গত হতে পারে, কিন্তু Remal-এর মতো বড় cyclone-এ বরিশালও একইভাবে আক্রান্ত হয় (উপরে দেখুন) — তাই pure 'Riverine' না বরং hybrid হওয়া উচিত।",
        "inundation_bands": {"status": "⚠️ placeholder — DEM/DFO বাকি"},
    }],
    "soil_moisture_weight_note": "আংশিক tidal, আংশিক riverine — cyclone season-এ tidal/surge factor প্রাধান্য পাওয়া উচিত।",
    "confluence_note": "বরিশাল CONFLUENCE_DISTRICTS-এ নেই।",
}