# ============================================================
# FloodAI — data/district_profiles/chuadanga.py — জেলা #৩২
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

CHUADANGA_PROFILE = {
    "district": "চুয়াডাঙ্গা", "district_lat": 23.64, "district_lon": 88.84,
    "station_count": 2, "station_count_note": "✅ দুইটা station-ই flood_config.py-তে সঠিকভাবে linked।",

    "stations": [
        {
            "name": "Chuadanga", "ffwc_id": "SW207", "is_primary": True,
            "river": "মাথাভাঙা (Mathabhanga)", "upazila": "Chuadanga Sadar", "union": None,
            "river_structure": {
                "category": "medium (transboundary, পদ্মার একটা distributary)",
                "catchment": (
                    "🔍 Grokipedia: মাথাভাঙা পদ্মা থেকে বিচ্ছিন্ন হয় (জালাঙ্গীর "
                    "বিভাজন পয়েন্টের ১৬ কিমি ভাটিতে), ১২৪ কিমি পশ্চিমে প্রবাহিত হয়ে "
                    "বাংলাদেশ-ভারত সীমান্তের অংশ গঠন করে (দৌলতপুর উপজেলা/নদীয়া "
                    "জেলার সীমান্তে), তারপর ভারতে ঢুকে চূর্ণী ও ইছামতিতে বিভক্ত হয়।"
                ),
                "flow_behavior": "সীমান্ত নদী, ফারাক্কার প্রভাবেও কমেছে কিন্তু গড়াইয়ের মতো এতটা নাটকীয় না",
                "upstream_reference": "Malda, IN", "lag_time_hours": 44,
            },
            "danger_level_m": 11.60, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1160, "corrected_estimate": 800, "corrected_range": "⚠️ নির্দিষ্ট measurement পাওয়া যায়নি, মাঝারি-স্কেল transboundary distributary হিসেবে অনুমান", "confidence": "low"},
                "cn": {"old_value": 73, "reviewed_estimate": 85, "confidence": "low-moderate"},
                "risk_category": {"old_value": "কম", "reviewed_estimate": "কম (অপরিবর্তিত)", "reasoning": "নির্দিষ্ট বড় বন্যার ইতিহাস খুঁজে পাওয়া যায়নি, upgrade করার justification নেই"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Hatboalia", "ffwc_id": "SW206", "is_primary": False,
            "river": "মাথাভাঙা (Mathabhanga)", "upazila": "Alamdanga", "union": None,
            "river_structure": {
                "category": "medium",
                "catchment": "🔍 Wikipedia: মাথাভাঙা ঠিক Hatboalia গ্রামের কাছেই একটা শাখায় বিভক্ত হয়, যেটাকে 'কুমার' (Kumar) বা 'Pangasi' নামে ডাকা হয় — অর্থাৎ ফরিদপুরের কুমার নদীর **প্রকৃত উৎস এই পয়েন্টেই**! এটা এই framework-এ একটা গুরুত্বপূর্ণ geographic connection আবিষ্কার।",
                "upstream_reference": "Malda, IN", "lag_time_hours": 44,
            },
            "danger_level_m": 14.05, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "gap_found": "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র চুয়াডাঙ্গার rivers লিস্টে নেই (শুধু Chuadanga/SW207 আছে)।",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1405, "corrected_estimate": 700, "confidence": "low"},
                "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "কম", "reasoning": "Chuadanga primary station-এর অনুরূপ"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "মাঝারি-স্কেল transboundary নদী — discharge_ratio এবং local_rain উভয়ই মোটামুটি সমান গুরুত্বপূর্ণ।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",
    "cross_district_note": "🔍 Hatboalia পয়েন্টেই ফরিদপুরের কুমার নদীর জন্ম — চুয়াডাঙ্গা ও ফরিদপুরের profile একসাথে পড়লে কুমারের সম্পূর্ণ উৎস-থেকে-বিচ্ছিন্নতার গল্প বোঝা যায়। মেহেরপুরের ভৈরবও একই মাথাভাঙা সিস্টেমের অংশ।",
}