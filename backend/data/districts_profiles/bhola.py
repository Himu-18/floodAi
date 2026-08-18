# ============================================================
# FloodAI — data/district_profiles/bhola.py — জেলা #১৫
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BHOLA_PROFILE = {
    "district": "ভোলা",
    "district_lat": 22.49, "district_lon": 90.84,
    "station_count": 1,
    "stations": [{
        "name": "Daulatkhan", "ffwc_id": "SW278", "is_primary": True,
        "river": "নিম্ন মেঘনা (Lower Meghna)", "upazila": "Daulatkhan", "union": "Char Pata",
        "river_structure": {
            "category": "tidal_estuary (নদী-না — মেঘনার মোহনা, প্রতিদিন জোয়ার-ভাটা প্রভাবিত)",
            "catchment": "মেঘনার সর্বশেষ অংশ, বঙ্গোপসাগরে পড়ার ঠিক আগে — দ্বীপ জেলা ভোলা এখানে অবস্থিত",
            "flow_behavior": "নদীর discharge-এর চেয়ে জোয়ার-ভাটা ও ঘূর্ণিঝড়ের storm surge বেশি নির্ধারক",
            "upstream_reference": "Agartala, IN",
            "upstream_reference_caveat": "⚠️ সম্ভবত ভুল — নোয়াখালীর মতোই কপি-পেস্ট সমস্যা, coastal/tidal জেলায় Agartala অপ্রাসঙ্গিক",
            "lag_time_hours": 26,
        },
        "danger_level_m": 2.95, "highest_recorded_m": 4.03,
        "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 295, "corrected_estimate": None, "note": "tidal estuary station — discharge_ratio concept এখানে কম অর্থবহ, tidal-cycle/storm-surge মডেল বেশি উপযুক্ত", "confidence": "low"},
            "cn": {"old_value": 78, "reviewed_estimate": 82, "reasoning": "নিচু delta দ্বীপ, জলাভূমি-প্রবণ", "confidence": "low"},
            "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত)", "reasoning": "Sidr(২০০৭)/Remal(২০২৪)-এ বারবার সরাসরি আঘাতপ্রাপ্ত, সঠিক classification", "source": "Banglapedia (Sidr), TBS (Remal ২০২৪)"},
        },
        "flood_type": "Coastal & Tidal",
        "flood_type_note": "✅ সঠিক — কিন্তু cyclone-storm-surge (নিয়মিত tidal cycle থেকে ভিন্ন, অনেক বড় মাত্রার) আলাদা sub-category হিসেবে থাকা উচিত",
        "inundation_bands": {
            "note": "Sidr(২০০৭)-এ পুরো ভোলা জেলা ৫ মিটার (১৬ ফুট) উঁচু storm surge-এ আক্রান্ত হয়েছিল",
            "status": "⚠️ placeholder — DEM/DFO বাকি",
        },
    }],
    "soil_moisture_weight_note": "Coastal & Tidal জেলায় soil_moisture কম প্রাসঙ্গিক — cyclone track/intensity + tidal phase সবচেয়ে গুরুত্বপূর্ণ predictor, যা বর্তমান ১৪-feature মডেলে নেই।",
    "confluence_note": "ভোলা CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "Sidr/Remal-এর cyclone-context বরিশাল, পটুয়াখালী, বরগুনা, পিরোজপুর, ঝালকাঠির জন্য পুরোপুরি reuse করা যাবে — একই cyclone landfall zone।",
}