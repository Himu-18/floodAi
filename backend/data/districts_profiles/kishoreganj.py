# ============================================================
# FloodAI — data/district_profiles/kishoreganj.py
#
# জেলা-বাই-জেলা framework-এর ১১তম জেলা — উজানের মেঘনা, সুরমা-কুশিয়ারা
# (Surma-Kushiyara, Ajmiriganj/Kuliarchar-এ পুনর্মিলিত) + পুরনো ব্রহ্মপুত্রের
# সঙ্গমস্থল, হাওর অঞ্চলের ভিন্ন dynamics সহ।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

KISHOREGANJ_PROFILE = {
    "district": "কিশোরগঞ্জ",
    "district_lat": 24.43,
    "district_lon": 90.78,

    "station_count": 1,

    "stations": [
        {
            "name": "Bhairabbazar",
            "ffwc_id": "SW273",
            "is_primary": True,

            "river": "উজানের মেঘনা (Upper Meghna)",
            "upazila": "Bhairab",
            "union": None,

            "river_structure": {
                "category": "large_regional (confluence point — mega_trunk থেকে ছোট, কিন্তু একক Meghalaya উপনদীর চেয়ে বড়)",
                "catchment": (
                    "🔍 এটা একটা প্রকৃত সঙ্গমস্থল station: সুরমা ও কুশিয়ারা "
                    "(আসামের বরাক থেকে ভাগ হয়ে, সিলেটের হাওর অঞ্চল পার হয়ে) "
                    "আজমিরীগঞ্জ/কুলিয়ারচরের কাছে পুনর্মিলিত হয়ে 'উজানের মেঘনা' নাম "
                    "নেয়, আর ঠিক ভৈরব বাজারেই পুরনো ব্রহ্মপুত্র ডান তীর থেকে এসে "
                    "মেশে। অর্থাৎ এই একটা station-এ দুইটা সম্পূর্ণ ভিন্ন উৎসের "
                    "(মেঘালয়ের হাওর-সিস্টেম + উত্তরের পুরনো ব্রহ্মপুত্র) পানি একসাথে "
                    "চলে আসে।"
                ),
                "flow_behavior": (
                    "mega_trunk (পদ্মা/যমুনা, ৩০,০০০-৫০,০০০ m³/s)-এর চেয়ে অনেক "
                    "ছোট, কিন্তু একক Meghalaya উপনদী (সুরমা ~৮৫০, ভুগাই ~২৫০)-এর "
                    "চেয়ে বড় — কারণ একাধিক সিস্টেমের মিলিত প্রবাহ।"
                ),
                "upstream_reference": "Guwahati, IN",  # flood_config.py-তে যা আছে
                "upstream_reference_caveat": (
                    "⚠️ এখানে upstream_reference-এর সীমাবদ্ধতা কাঠামোগত, ভুল না — "
                    "এই নদীর দুইটা সম্পূর্ণ ভিন্ন উৎস (সুরমা-কুশিয়ারা হয়ে মেঘালয়, "
                    "আর পুরনো ব্রহ্মপুত্র হয়ে আসামের দিক) থাকায় একটামাত্র "
                    "upstream_reference point (Guwahati) কোনোভাবেই পুরো ছবিটা "
                    "ধরতে পারবে না। এইটা single-upstream-point মডেল ডিজাইনের "
                    "একটা কাঠামোগত সীমাবদ্ধতা confluence station-গুলোর জন্য।"
                ),
                "lag_time_hours": 22,
            },

            "danger_level_m": 5.80,  # ✅ FFWC verify করা (SW273) — flood_config.py-র সাথে মিলেছে
            "highest_recorded_m": None,
            "verified_source": (
                "flood_config.py-র সাথে মিলেছে; ২০২২ সালের বন্যায় TBS রিপোর্ট "
                "অনুযায়ী এই station ঠিক ৫.৮০ সেমি danger-এর উপরে উঠেছিল (নিশ্চিত "
                "real crossing event)"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 580,  # danger_level(5.8)*100
                    "corrected_estimate": 4600,
                    "corrected_range": "গড় বার্ষিক discharge ~৪,৬০০ m³/s (Bhairab Bazar gauge-নির্দিষ্ট পরিমাপ) — শুষ্ক মৌসুমে ৫,০০০-১০,০০০ m³/s রেঞ্জেও যেতে পারে (tidal backwater প্রভাবের কারণে জটিল)",
                    "source": "Meghna River hydrology literature (গঙ্গা-ব্রহ্মপুত্র-মেঘনা ডেল্টা গবেষণা, ২০২০ পর্যন্ত data)",
                    "note": "⚠️ পুরনো (৫৮০) → নতুন (৪৬০০) — ~৮ গুণ underestimate, পদ্মা/যমুনার স্কেলের (৩৫-৯০ গুণ) চেয়ে কম কিন্তু এখনো উল্লেখযোগ্য ভুল",
                    "confidence": "moderate-high — নির্দিষ্ট gauge-এর জন্য published figure পাওয়া গেছে (Munshiganj-এর Meghna-Br profile-এও এই সংখ্যা cross-check করে আপডেট করা যেতে পারে)",
                },
                "cn": {"old_value": 81, "reviewed_estimate": 87, "reasoning": "হাওর অঞ্চলের জলাভূমি/নিচু জমি — উচ্চ CN (কম infiltration, প্রায় সবসময় saturated মাটি) যুক্তিসঙ্গত", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
                    "reasoning": "২০২২ সালে ৯ উপজেলার ৬২ ইউনিয়নে ১ লক্ষের বেশি মানুষ পানিবন্দী হয়েছিল, ১২,৭৪৮ পরিবার ক্ষতিগ্রস্ত — 'উচ্চ' সঠিক।",
                    "source": "TBS News (১ লক্ষ মানুষ পানিবন্দী রিপোর্ট, ২০২২)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ শুধু 'Riverine' লেবেল কিশোরগঞ্জের হাওর-নির্দিষ্ট ঝুঁকিকে সম্পূর্ণ "
                "ধরে না। হাওর অঞ্চলে (ইটনা, মিঠামইন, অষ্টগ্রাম) এপ্রিল-মে মাসে "
                "'আগাম বান' (early flash flood, ধান কাটার আগে) হয় — এটা মূল "
                "monsoon riverine বন্যা থেকে আলাদা একটা risk window, upstream "
                "Meghalaya rainfall-চালিত, কিন্তু flood_config-এ আলাদাভাবে ধরা "
                "নেই। ফসল ক্ষতির দিক থেকে এই early flash flood প্রায়ই মূল "
                "বর্ষার বন্যার চেয়েও বেশি গুরুত্বপূর্ণ।"
            ),

            "inundation_bands": {
                "affected_upazilas": "ইটনা, মিঠামইন, অষ্টগ্রাম (হাওর উপজেলা, সবচেয়ে বেশি ক্ষতিগ্রস্ত) + তাড়াইল, নিকলী, করিমগঞ্জ, বাজিতপুর, ভৈরব",
                "0_to_50cm_above_danger": "হাওর অঞ্চলের প্রান্তবর্তী নিচু কৃষিজমি",
                "50cm_to_1m_above_danger": "ইটনা/মিঠামইন/অষ্টগ্রামের বসতি এলাকা",
                "above_1m_danger": "২০২২ স্কেলে — ৯ উপজেলা, ১ লক্ষের বেশি মানুষ পানিবন্দী",
                "status": "⚠️ placeholder — DEM/DFO calibration বাকি, তবে affected upazila তালিকা নির্দিষ্ট",
            },
        },
    ],

    "soil_moisture_weight_note": (
        "হাওর অঞ্চলের বৈশিষ্ট্যের কারণে soil_moisture এখানে অন্য জেলার তুলনায় "
        "একটু ভিন্নভাবে ব্যবহার হওয়া উচিত — মাটি প্রায় স্থায়ীভাবে saturated "
        "(জলাভূমি), তাই soil_moisture কম discriminative signal, upstream_rain "
        "(বিশেষত এপ্রিল-মে সময়ের আগাম বান-এর জন্য) বেশি গুরুত্বপূর্ণ।"
    ),

    "confluence_note": "কিশোরগঞ্জ riverine.py-র CONFLUENCE_DISTRICTS (পদ্মা-যমুনা)-এ নেই, কিন্তু এটা নিজেই একটা ভিন্ন confluence (সুরমা-কুশিয়ারা+পুরনো ব্রহ্মপুত্র) — এই ধরনের 'secondary confluence' district-এর জন্য আলাদা override logic ভবিষ্যতে বিবেচনা করা যেতে পারে।",

    "cross_district_note": "এই গবেষণা নেত্রকোণা, সুনামগঞ্জ (হাওর-সংলগ্ন জেলা) এবং নরসিংদী/ব্রাহ্মণবাড়িয়ার (উজানের মেঘনার ভাটি) জন্য আংশিক reuse করা যাবে।",
}