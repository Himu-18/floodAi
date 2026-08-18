# ============================================================
# FloodAI — data/district_profiles/lakshmipur.py — জেলা #৪২
# ⚠️ কোনো FFWC station নেই — নোয়াখালীর মতোই কেস।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

LAKSHMIPUR_PROFILE = {
    "district": "লক্ষ্মীপুর", "district_lat": 22.74, "district_lon": 90.89,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False — নোয়াখালীর প্রায় অবিকল একই পরিস্থিতি (প্রতিবেশী জেলা, একই মেঘনা মোহনা)।",

    "river_structure": {
        "river": "মেঘনা (Meghna)",
        "category": "tidal_estuary",
        "catchment": "নোয়াখালীর ঠিক পাশে, মেঘনার মোহনার একই এলাকা — রামগতি/কমলনগর উপজেলা নদীভাঙনের জন্য বিশেষভাবে পরিচিত",
        "upstream_reference": "Agartala, IN",
        "upstream_reference_caveat": "❌ ভুল — নোয়াখালীর মতোই একই সমস্যা",
        "lag_time_hours": 22,
    },

    "danger_level_m": {"old_value": 4.0, "verdict": "❌ unverified"},

    "flood_type": "Coastal & Tidal",
    "flood_type_note": "নোয়াখালীর মতোই — cyclone/tidal surge + upstream (মেঘনা/ফেনী) overflow উভয়ই প্রাসঙ্গিক হতে পারে।",

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 400, "corrected_estimate": None, "note": "danger_level unverified, tidal estuary — discharge_ratio কম প্রাসঙ্গিক", "confidence": "none"},
        "cn": {"old_value": 80, "reviewed_estimate": 83, "confidence": "low"},
        "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত)", "reasoning": "রামগতি/কমলনগর উপজেলা মেঘনার নদীভাঙনে বাংলাদেশের সবচেয়ে বেশি ক্ষতিগ্রস্ত এলাকার মধ্যে পড়ে — 'উচ্চ' যথাযথ"},
    },

    "inundation_bands": {"affected_upazilas": "রামগতি, কমলনগর (নদীভাঙনের জন্য বিশেষভাবে পরিচিত)", "status": "⚠️ placeholder — DEM/DFO বাকি"},

    "soil_moisture_weight_note": "নোয়াখালীর একই যুক্তি — rainfall+tidal-surge-ভিত্তিক approach দরকার।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "নোয়াখালী/ফেনীর সাথে একই ২০২৪ বন্যা-প্রভাবিত অঞ্চল, একই coastal-belt approach প্রযোজ্য।",

    "recommended_fix": "নোয়াখালীর মতোই — rainfall+tidal hybrid model দরকার, discharge-ভিত্তিক ১৪-feature মডেল অপর্যাপ্ত।",
}