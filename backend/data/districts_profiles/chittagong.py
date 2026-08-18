# ============================================================
# FloodAI — data/district_profiles/chittagong.py — জেলা #২৬
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

CHITTAGONG_PROFILE = {
    "district": "চট্টগ্রাম",
    "district_lat": 22.22, "district_lon": 91.78,
    "station_count": 4,
    "station_count_note": "✅ চারটা station-ই flood_config.py-তে সঠিকভাবে linked, কোনো gap নেই — ফেনীর মতো transboundary hill-river ক্লাস্টার।",

    "stations": [
        {
            "name": "Chittagong", "ffwc_id": "SW152.2", "is_primary": True,
            "river": "কর্ণফুলী (Karnaphuli)", "upazila": "Double Mooring", "union": None,
            "river_structure": {
                "category": "urban_tidal_port_river (বন্দর-নদী, দেশের ব্যস্ততম বন্দর এখানেই)",
                "catchment": "পার্বত্য চট্টগ্রাম (কাপ্তাই বাঁধ-নিয়ন্ত্রিত) থেকে আসা প্রধান নদী, শহরের মধ্য দিয়ে বঙ্গোপসাগরে পতিত",
                "flow_behavior": "কাপ্তাই বাঁধ দ্বারা আংশিক নিয়ন্ত্রিত + জোয়ার-ভাটা + urban drainage — তিনটা factor-এর মিশ্রণ, শুধু 'Urban Waterlogging' লেবেল এটা ধরে না",
                "upstream_reference": "Agartala, IN",
                "upstream_reference_note": "✅ এখানে যুক্তিসঙ্গত — সাঙ্গু/হালদা/ফেনী (secondary rivers) সত্যিই ত্রিপুরার পাহাড় থেকে আসে, নোয়াখালীর মতো ভুল-কপি না",
                "lag_time_hours": 20,
            },
            "danger_level_m": 4.15, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 415, "corrected_estimate": None, "note": "কাপ্তাই বাঁধ-নিয়ন্ত্রিত + tidal + urban — একটামাত্র discharge_ratio number এই ত্রিমুখী dynamics ধরতে পারবে না, dam-release+tidal-phase+drainage-capacity তিনটাই দরকার", "confidence": "none"},
                "cn": {"old_value": 95, "reviewed_estimate": 95, "reasoning": "✅ ঢাকা মেট্রোর মতোই সঠিক — ঘনবসতিপূর্ণ urban core", "confidence": "high"},
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "২০২৪ আগস্ট বন্যায় চট্টগ্রাম সরাসরি ক্ষতিগ্রস্ত ছিল (১১ জেলার তালিকায়), বহদ্দারহাট/মুরাদপুর/চকবাজার প্রতি বর্ষায় জলাবদ্ধ হয় — 'মাঝারি' কম মনে হচ্ছে দেশের ২য় বৃহত্তম শহরের জন্য",
                    "source": "Wikipedia (August 2024 floods — Chattogram অন্তর্ভুক্ত)",
                },
            },
            "flood_type": "Urban Waterlogging",
            "flood_type_note": "⚠️ Dhaka-র মতো শুধু drainage-capacity সমস্যা না — এখানে কাপ্তাই বাঁধ (Dam-Affected) + জোয়ার-ভাটা (Coastal & Tidal) + urban drainage — তিনটা flood_type-এর মিশ্রণ, একটামাত্র category দিয়ে সম্পূর্ণ চিত্র ধরা যাচ্ছে না।",
            "inundation_bands": {"affected_areas": "বহদ্দারহাট, মুরাদপুর, চকবাজার, হালিশহর (flood_config.py-তে নির্দিষ্টভাবে উল্লেখিত)", "status": "⚠️ placeholder"},
        },
        {
            "name": "Dohazari", "ffwc_id": "SW248", "is_primary": False,
            "river": "সাঙ্গু (Sangu)", "upazila": "Chandanaish", "union": None,
            "river_structure": {"category": "medium (পার্বত্য চট্টগ্রাম/মিয়ানমার সীমান্তের কাছাকাছি উৎস)", "catchment": "চন্দনাইশ/সাতকানিয়া এলাকা", "upstream_reference": "Agartala, IN", "upstream_reference_caveat": "⚠️ সম্ভবত ভুল — সাঙ্গুর উৎস মিয়ানমার সীমান্তের কাছে (আরাকান পাহাড়), ত্রিপুরা/আগরতলা না। কর্ণফুলীর জন্য Agartala যুক্তিসঙ্গত হলেও সাঙ্গুর জন্য একটা ভিন্ন upstream point (হয়তো Bandarban-এর কাছাকাছি) বেশি সঠিক হতো।", "lag_time_hours": 20},
            "danger_level_m": 6.55, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 655, "corrected_estimate": 500, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "পার্বত্য এলাকা, flash-flood-প্রবণ"}},
            "flood_type": "Flash Flood (Urban Waterlogging না — এই secondary station গ্রামীণ/পার্বত্য এলাকায়)",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Narayanhat", "ffwc_id": "SW117", "is_primary": False,
            "river": "হালদা (Halda)", "upazila": "Fatikchhari", "union": None,
            "river_structure": {"category": "medium (দেশের একমাত্র প্রাকৃতিক কার্প মাছের প্রজনন নদী হিসেবে বিখ্যাত)", "catchment": "ফটিকছড়ি, ত্রিপুরার পাহাড়ের কাছাকাছি", "upstream_reference": "Agartala, IN", "upstream_reference_note": "✅ যুক্তিসঙ্গত — হালদার উৎস সত্যিই ত্রিপুরা সীমান্তের কাছে", "lag_time_hours": 20},
            "danger_level_m": 14.80, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1480, "corrected_estimate": 600, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "২০২৪-এ ১১০cm উপরে ওঠার রেকর্ড (Prothom Alo/bdnews24 আগস্ট ২০২৪ কভারেজ)"}},
            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Ramgarh", "ffwc_id": "SW84", "is_primary": False,
            "river": "ফেনী (Feni)", "upazila": "Fatikchhari", "union": None,
            "river_structure": {"category": "medium (ফেনী জেলার মুহুরীর থেকে ভিন্ন — এটা 'ফেনী নদী' নামের ভিন্ন নদী, ফেনী জেলার সাথে গুলিয়ে ফেলা যাবে না)", "catchment": "রামগড় সীমান্ত এলাকা, ত্রিপুরার কাছাকাছি", "upstream_reference": "Agartala, IN", "upstream_reference_note": "✅ যুক্তিসঙ্গত", "lag_time_hours": 20},
            "danger_level_m": 16.90, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 1690, "corrected_estimate": 600, "confidence": "low"}, "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "২০২৪-এ ২১০cm উপরে ওঠার রেকর্ড — এই framework-এ danger level-এর সবচেয়ে বেশি crossing margin (bdnews24)"}},
            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "মিশ্র জেলা — primary (urban Karnaphuli) এ drainage-capacity+dam+tidal, ৩টা secondary (Sangu/Halda/Feni) এ rainfall-driven flash-flood dynamics প্রাধান্য পাওয়া উচিত।",

    "confluence_note": "চট্টগ্রাম CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "কর্ণফুলী কাপ্তাই বাঁধের জন্য রাঙ্গামাটির সাথে সংযুক্ত (ভবিষ্যতে profile করার সময় প্রাসঙ্গিক)। Sangu/Halda/Feni-এর জন্য বান্দরবান/খাগড়াছড়ির সাথেও ভৌগোলিক সংযোগ আছে।",
}