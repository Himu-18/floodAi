# ============================================================
# FloodAI — data/district_profiles/jessore.py — জেলা #৩১
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

JESSORE_PROFILE = {
    "district": "যশোর", "district_lat": 22.90, "district_lon": 89.05,
    "station_count": 1,
    "stations": [{
        "name": "Jhikargacha", "ffwc_id": "SW162", "is_primary": True,
        "river": "কোবাদক (Kobadak/Kapotaksha)", "upazila": "Jhikargachha", "union": None,
        "river_structure": {
            "category": "medium (মাথাভাঙ্গা সিস্টেমের branch, ভৈরবের সাথে যুক্ত)",
            "catchment": (
                "🔍 কোবাদক (কপোতাক্ষ) আসলে মাথাভাঙ্গা নদী থেকে উৎপন্ন, ভৈরবের একটা "
                "শাখা হিসেবে কাজ করে (Wikipedia: 'Bhairab River has two main "
                "branches, the Khulna-Ichamati and the Kobadak')। এই একই নদী "
                "সিস্টেমের নামেই 'Ganges-Kobadak (G-K) irrigation project' — যেটা "
                "ফরিদপুরের কুমার নদীকে বিচ্ছিন্ন করে দিয়েছিল (আগে profile করা) — "
                "মানে যশোরের কোবাদকও একই প্রজেক্টের প্রভাবে থাকার সম্ভাবনা আছে।"
            ),
            "upstream_reference": "Kolkata, IN", "lag_time_hours": 30,
        },
        "danger_level_m": 4.65, "verified_source": "flood_config.py-র সাথে মিলেছে",
        "ml_features_verified": {
            "reference_discharge_m3s": {"old_buggy_value": 465, "corrected_estimate": 400, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি — G-K project-প্রভাবিত ছোট নদী, ফরিদপুরের কুমারের (৮০০) কাছাকাছি বা তার চেয়ে ছোট ধরা হয়েছে", "source": "ফরিদপুরের কুমার profile-এর যুক্তি reuse করা", "confidence": "low"},
            "cn": {"old_value": 75, "reviewed_estimate": 84, "confidence": "low-moderate"},
            "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "ফরিদপুরের কুমারের মতোই ছোট/আংশিক-বিচ্ছিন্ন নদী, বড় upgrade/downgrade-এর justification নেই"},
        },
        "flood_type": "Riverine",
        "flood_type_note": "⚠️ ফরিদপুরের কুমারের মতোই — G-K project-প্রভাবিত হওয়ায় pure trunk-river riverine dynamics এখানে পুরোপুরি প্রযোজ্য নাও হতে পারে, local_rain বেশি গুরুত্বপূর্ণ হতে পারে",
        "inundation_bands": {"status": "⚠️ placeholder"},
    }],
    "soil_moisture_weight_note": "ফরিদপুরের কুমারের একই যুক্তি — G-K project-প্রভাবিত নদীতে local rainfall বেশি প্রাসঙ্গিক discharge_ratio-র চেয়ে।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "ফরিদপুরের কুমার + মেহেরপুর/চুয়াডাঙ্গার ভৈরব/মাথাভাঙ্গা — সবই একই G-K project-প্রভাবিত delta distributary network-এর অংশ।",
}