# ============================================================
# FloodAI — data/district_profiles/rajshahi.py — জেলা #৩৪
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

RAJSHAHI_PROFILE = {
    "district": "রাজশাহী", "district_lat": 24.37, "district_lon": 88.60,
    "station_count": 1,
    "stations": [{
        "name": "Rajshahi", "ffwc_id": "SW88", "is_primary": True,
        "river": "পদ্মা/গঙ্গা (Ganges/Padma)", "upazila": "Paba", "union": None,
        "river_structure": {
            "category": "mega_trunk", "catchment": "রাজবাড়ীর একই গঙ্গা/পদ্মা, কিন্তু অনেক উজানে (হার্ডিঞ্জ ব্রিজেরও উজানে) — danger_level ১৮.০৫ (রাজবাড়ীর ৮.২-এর চেয়ে অনেক বেশি, উঁচু elevation-এর কারণে)",
            "upstream_reference": "Malda, IN", "lag_time_hours": 48,
        },
        "danger_level_m": 18.05, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 1805, "corrected_estimate": 75000, "corrected_range": "bankfull — রাজবাড়ীর রেফারেন্স reuse (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল, Wikipedia mean ৩৪,৯৩৮ m³/s; danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত)", "source": "রাজবাড়ী profile থেকে reuse", "confidence": "moderate-high"},
            "cn": {"old_value": 72, "reviewed_estimate": 88, "confidence": "moderate"},
            "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "mega_trunk গঙ্গার সরাসরি সংস্পর্শ, রাজবাড়ী/চাঁপাইনবাবগঞ্জের সাথে সঙ্গতি রাখতে upgrade"},
        },
        "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "রাজবাড়ীর একই যুক্তি — mega_trunk-এ discharge primary।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই (পদ্মা-যমুনা মিলনস্থলের অনেক উজানে), কিন্তু রাজবাড়ীর confluence bug-এর reference_discharge সমস্যা এখানেও প্রযোজ্য।",
    "cross_district_note": "চাঁপাইনবাবগঞ্জ (আরো উজানে) ও কুষ্টিয়ার Talbaria-র সাথে একই গঙ্গা trunk।",
}