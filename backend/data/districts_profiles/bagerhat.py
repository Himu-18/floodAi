# ============================================================
# FloodAI — data/district_profiles/bagerhat.py
#
# ১৪তম জেলা। খুলনার মতোই Coastal & Tidal flood_type, সুন্দরবন/Mongla
# বন্দর অঞ্চল। আগের জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BAGERHAT_PROFILE = {
    "district": "বাগেরহাট",
    "district_lat": 22.6602,
    "district_lon": 89.7895,

    "station_count": 1,

    "stations": [
        {
            "name": "Mongla",
            "ffwc_id": "SW244",
            "is_primary": True,

            "river": "পশুর (Pasur)",
            "upazila": "Mongla",
            "union": "Paurashava",

            "river_structure": {
                "category": "coastal_tidal",
                "catchment": (
                    "রূপসা/ভৈরব নদীর সরাসরি ধারাবাহিকতা — Chalna-র কাছে "
                    "'পশুর' নাম নেয়, Mongla উপজেলার দক্ষিণে সুন্দরবনে "
                    "প্রবেশ করে। মেঘনার পরে বদ্বীপ অঞ্চলের দ্বিতীয় "
                    "বৃহত্তম নদী (Banglapedia)। গড়াই-মধুমতির সর্বোচ্চ "
                    "প্রবাহ নবগঙ্গা হয়ে এই নদীতেই আসে। খুবই গভীর ও সারা "
                    "বছর নাব্য — বড় সামুদ্রিক জাহাজ সরাসরি Mongla "
                    "সমুদ্রবন্দরে (বাংলাদেশের ২য় বৃহত্তম) প্রবেশ করতে পারে।"
                ),
                "flow_behavior": (
                    "সম্পূর্ণ tidal-dominated, Khulna-র রূপসার মতোই। "
                    "Mongla বন্দর হওয়ায় এখানে জোয়ারের উচ্চতা ও storm-"
                    "surge ঝুঁকি অর্থনৈতিকভাবেও (বন্দর কার্যক্রম) "
                    "গুরুত্বপূর্ণ — শুধু জনবসতির জন্য না।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 1.80,  # ✅ FFWC verify করা
            "highest_recorded_m": 3.33,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Mongla/Paurashava) সব "
                "মিলে গেছে ✅। coordinate প্রায় নিখুঁত — stations.py "
                "lat=22.49,lon=89.60 বনাম Wikipedia-র Mongla উপজেলা "
                "কেন্দ্র lat=22.483,lon=89.6083 — মাত্র সামান্য পার্থক্য, "
                "নগণ্য। উল্লেখযোগ্য: highest_recorded (3.33m) danger_"
                "level-এর প্রায় দ্বিগুণ (১.৫৩ মি বেশি) — বড় storm-surge "
                "ইভেন্টে কতটা ছাড়িয়ে যেতে পারে তার ইঙ্গিত।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 180,
                    "corrected_estimate": None,
                    "corrected_range": "Khulna (রূপসা)-র ঠিক একই যুক্তি — tidal নদী, একমুখী discharge concept অপ্রযোজ্য",
                    "source": "N/A — কাঠামোগত সমস্যা, নির্দিষ্ট সোর্সের অভাব না",
                    "confidence": "N/A",
                    "critical_caveat": "Khulna profile-এ বিস্তারিত আলোচিত একই সমস্যা — tidal reference_discharge redesign প্রয়োজন।",
                },
                "cn": {"old_value": None, "reviewed_estimate": None, "reasoning": "tidal-dominated flood-এর জন্য CN সরাসরি প্রযোজ্য না।", "confidence": "N/A"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "Mongla সমুদ্রবন্দর — জাতীয় অর্থনৈতিক গুরুত্ব, সরাসরি "
                        "সুন্দরবনের কাছে অবস্থিত হওয়ায় cyclone landfall-এর "
                        "প্রথম সারির ঝুঁকিতে থাকে (সিডর ২০০৭, আইলা ২০০৯, "
                        "আম্পান ২০২০ — সবগুলোই এই উপকূলীয় বেল্টের কাছাকাছি "
                        "আঘাত হেনেছে)। highest_recorded/danger_level ratio "
                        "Khulna-র চেয়েও বেশি চরম।"
                    ),
                    "source": "Wikipedia (Port of Mongla); Sundarbans cyclone history (১৯৬১-২০২০, ১৩টা ঘূর্ণিঝড়)",
                },
            },

            "flood_type": "Coastal & Tidal",
            "flood_type_note": "Khulna-র রূপসার ঠিক একই যুক্তি — coastal_tidal.py module-এর crude lunar-heuristic real tide/storm-surge API দিয়ে replace হওয়া দরকার।",

            "inundation_bands": {"status": "⚠️ placeholder — tidal/storm-surge dynamics, Khulna-র মতোই আলাদা মডেল দরকার"},
        },
    ],

    "soil_moisture_weight_note": (
        "Khulna-র রূপসার ঠিক একই যুক্তি — tide phase ও storm-surge/"
        "cyclone event-ই primary driver, soil moisture/rainfall-এর "
        "prognostic value সীমিত।"
    ),

    "confluence_note": (
        "বাগেরহাট Khulna-র রূপসা-পশুর একই নদীর ধারাবাহিকতা — "
        "physically একই নদী-সিস্টেমের দুই বিন্দু (Khulna উজানে, Mongla "
        "downstream-এ, সুন্দরবনের কাছে)। এই দুইটা এবং Satkhira (একই "
        "batch-এ) মিলিয়ে দক্ষিণ-পশ্চিম উপকূলীয় Coastal & Tidal cluster-এর "
        "একটা coherent picture তৈরি হচ্ছে।"
    ),

    "cross_district_flags": (
        "কোনো নতুন cross-district conflict পাওয়া যায়নি। Khulna profile-এ "
        "flag করা tidal-discharge conceptual সমস্যা এখানেও প্রযোজ্য।"
    ),
}