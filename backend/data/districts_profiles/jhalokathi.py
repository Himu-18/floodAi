# ============================================================
# FloodAI — data/district_profiles/jhalokati.py — জেলা #২০
# ⚠️ কোনো FFWC station নেই।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

JHALOKATI_PROFILE = {
    "district": "ঝালকাঠি",
    "district_lat": 22.44, "district_lon": 90.10,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False।",

    "river_structure": {
        "river": "বিষখালী (Bishkhali)",
        "category": "tidal_estuary",
        "catchment": "বরগুনার একই বিষখালী নদীর একটু উজানে, কিন্তু flood_config.py-তে danger_level ভিন্ন (৩.০ বনাম বরগুনার ২.৫) — একই নদীর ভিন্ন বিন্দুতে ভিন্ন স্তর যুক্তিসঙ্গত হতে পারে (উজান-ভাটার পার্থক্য), কিন্তু যেহেতু দুটোই unverified/no-station, এই পার্থক্যটা প্রকৃত পরিমাপ না বরং অনুমান হতে পারে।",
        "upstream_reference": "Agartala, IN",
        "upstream_reference_caveat": "❌ ভুল — একই সমস্যা",
        "lag_time_hours": 26,
    },

    "danger_level_m": {"old_value": 3.0, "verdict": "❌ unverified — বরগুনার একই নদীর সাথে সংখ্যার পার্থক্য থাকলেও কোনোটাই real gauge-ভিত্তিক না"},

    "cyclone_context": {
        "sidr_2007": "ঝালকাঠি শহর সরাসরি Sidr-এর ৫ মিটার storm surge-এ আক্রান্ত হয়েছিল (Patuakhali/Barguna-র সাথে একইসাথে উল্লেখিত)।",
        "remal_2024": "Great Danger Signal 10-এর আওতায়, 'severely affected districts' তালিকায় ছিল।",
        "source": "Dr. George Pararas-Carayannis (Sidr বিশ্লেষণ), TBS (Remal)",
    },

    "flood_type": "Coastal & Tidal",
    "flood_type_note": "✅ সঠিক দিক।",

    "ml_features_verified": {
        "reference_discharge_m3s": {"old_buggy_value": 300, "corrected_estimate": None, "confidence": "none"},
        "cn": {"old_value": 76, "reviewed_estimate": 81, "confidence": "low"},
        "risk_category": {
            "old_value": "মাঝারি",
            "reviewed_estimate": "উচ্চ",
            "reasoning": "পিরোজপুরের মতোই — Sidr ও Remal দুটোতেই সরাসরি আক্রান্ত, প্রতিবেশী coastal জেলাগুলোর (সব 'উচ্চ') সাথে সঙ্গতি রাখার জন্য upgrade করা হলো।",
            "source": "একই cyclone coverage sources",
        },
    },

    "inundation_bands": {"status": "⚠️ placeholder — DEM/DFO বাকি"},

    "soil_moisture_weight_note": "cyclone/tidal-driven।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",

    "recommended_fix": "একই coastal-belt approach দরকার — এই ৬ জেলা (ভোলা, বরিশাল, পটুয়াখালী, বরগুনা, পিরোজপুর, ঝালকাঠি) একসাথে একটা 'cyclone-coastal cluster' হিসেবে বিবেচনা করা উচিত, আলাদা আলাদা district-level tuning-এর চেয়ে।",
}