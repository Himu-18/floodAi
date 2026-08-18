# ============================================================
# FloodAI — data/district_profiles/sunamganj.py — জেলা #২১
# সিলেটের সুরমা-কুশিয়ারা গবেষণা এখানে reuse করা হয়েছে।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SUNAMGANJ_PROFILE = {
    "district": "সুনামগঞ্জ",
    "district_lat": 24.97, "district_lon": 91.20,
    "station_count": 4,
    "station_count_note": "✅ সিলেটের বিপরীতে — এই জেলার ৪টা station-ই flood_config.py-র rivers লিস্টে সঠিকভাবে আছে, কোনো gap নেই।",

    "stations": [
        {
            "name": "Sunamganj", "ffwc_id": "SW269", "is_primary": True,
            "river": "সুরমা (Surma)", "upazila": "Sunamganj Sadar", "union": None,
            "river_structure": {"category": "large_regional", "catchment": "সিলেটের একই সুরমা, একটু ভাটিতে — হাওর অঞ্চলের কেন্দ্র", "flow_behavior": "সিলেটের মতোই flashy, কিন্তু হাওর-নির্দিষ্ট slow-drainage সমস্যাও যুক্ত", "upstream_reference": "Shillong, IN", "lag_time_hours": 10},
            "danger_level_m": 7.80, "highest_recorded_m": None,
            "verified_source": "flood_config.py-র সাথে মিলেছে; bdnews24 (Golghor point-এ ৫০সেমি বৃদ্ধির তথ্য, ২০২৬)",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 780, "corrected_estimate": 850, "corrected_range": "সিলেটের সুরমা-র একই (Banglapedia)", "confidence": "moderate"},
                "cn": {"old_value": 87, "reviewed_estimate": 87, "reasoning": "ইতিমধ্যে উচ্চ ও যুক্তিসঙ্গত মান বসানো ছিল — এই framework-এ প্রথম জেলা যেখানে CN আগে থেকেই ঠিক", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "অতি উচ্চ",
                    "reviewed_estimate": "অতি উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
                    "reasoning": "২০২২-এর বন্যা '১২২ বছরের মধ্যে সবচেয়ে খারাপ' হিসেবে বর্ণিত হয়েছে (Dhaka Stream/গবেষণাপত্র) — সুনামগঞ্জ সিলেটের সাথে সবচেয়ে বেশি ক্ষতিগ্রস্ত হয়েছিল, ৬৬০,৩৪৭ মানুষ গৃহহীন। ফেনী/সুনামগঞ্জ/সিলেট — এই framework-এ এখন ৩টা 'অতি উচ্চ' জেলা।",
                    "source": "Dhaka Stream (Surma-Kushiyara project article, ২০২৬); bdnews24 (২০২৪ কভারেজ)",
                },
            },
            "flood_type": "Flash Flood",
            "inundation_bands": {
                "affected_note": "হাওর অঞ্চলের কারণে পানি নামতে দেরি হয় — Golghor/হাওর এলাকা সবচেয়ে বেশি ঝুঁকিপূর্ণ, ২০২৬-এও (danger-এর নিচে থাকা সত্ত্বেও) কৃষি ক্ষতির রিপোর্ট এসেছে",
                "status": "⚠️ placeholder — DEM/DFO বাকি",
            },
        },
        {
            "name": "Derai", "ffwc_id": "SW269.5", "is_primary": False,
            "river": "সুরমা পুরাতন প্রবাহ (Surma Old Course)", "upazila": "Derai", "union": None,
            "river_structure": {"category": "medium (সুরমার পুরনো/ছোট শাখা)", "catchment": "সুরমার একটা distributary", "flow_behavior": "মূল সুরমার চেয়ে ছোট", "upstream_reference": "Shillong, IN", "lag_time_hours": 10},
            "danger_level_m": 6.55, "highest_recorded_m": None, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 655, "corrected_estimate": 300, "confidence": "low — সুরমার তুলনায় ছোট distributary"},
                "cn": {"old_value": None, "reviewed_estimate": 86, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "মূল সুরমার তুলনায় সামান্য কম critical"},
            },
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Lourergorh", "ffwc_id": "SW131.5", "is_primary": False,
            "river": "যাদুকাটা (Jadukata)", "upazila": "Tahirpur", "union": None,
            "river_structure": {"category": "small (মেঘালয়ের সরাসরি উপনদী)", "catchment": "তাহিরপুর সীমান্তবর্তী, মেঘালয় থেকে সরাসরি নেমে আসা", "flow_behavior": "শেরপুরের ভুগাইয়ের মতোই অত্যন্ত flashy", "upstream_reference": "Shillong, IN", "lag_time_hours": 10},
            "danger_level_m": 8.05, "highest_recorded_m": None, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 805, "corrected_estimate": 250, "confidence": "low — শেরপুরের ভুগাই প্যাটার্নের সাথে সাদৃশ্যপূর্ণ ধরা হয়েছে"},
                "cn": {"old_value": None, "reviewed_estimate": 87, "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "অতি উচ্চ", "reasoning": "তাহিরপুর/আনোয়ারপুর এলাকা UN রিপোর্টে ২০২২-এর সবচেয়ে বেশি ক্ষতিগ্রস্ত এলাকা হিসেবে নির্দিষ্টভাবে উল্লেখিত"},
            },
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder — তবে তাহিরপুর/আনোয়ারপুর নির্দিষ্টভাবে চিহ্নিত ঝুঁকিপূর্ণ এলাকা"},
        },
        {
            "name": "Muslimpur", "ffwc_id": "SW333", "is_primary": False,
            "river": "ঝালুখালী (Jhalukhali)", "upazila": "Sunamganj Sadar", "union": None,
            "river_structure": {"category": "small/medium", "catchment": "স্থানীয় হাওর-সংযুক্ত চ্যানেল", "flow_behavior": "হাওর dynamics-প্রভাবিত", "upstream_reference": "Shillong, IN", "lag_time_hours": 10},
            "danger_level_m": 7.80, "highest_recorded_m": None, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 780, "corrected_estimate": 400, "confidence": "low"},
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "হাওর-সংযুক্ত, প্রায় স্থায়ী জলাভূমি — সবচেয়ে বেশি CN এই জেলায়", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "সদর উপজেলার কাছে, হাওর drainage-সংশ্লিষ্ট ঝুঁকি"},
            },
            "flood_type": "Flash Flood", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "সিলেটের একই যুক্তি + হাওর-নির্দিষ্ট বিবেচনা — পানি নামতে দেরি হওয়ায় (drainage congestion) soil_moisture এখানে আসলে একটু বেশি প্রাসঙ্গিক হতে পারে অন্য flash-flood জেলার তুলনায়, কারণ হাওরে পানি জমে থাকার প্রবণতা।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই। তবে এই জেলার নিজস্ব একটা multi-river (সুরমা+পুরাতন সুরমা+যাদুকাটা+ঝালুখালী) সমস্যা আছে, যেটা এই framework-এ সবচেয়ে ভালোভাবে-linked জেলা (৪/৪ station covered)।",

    "cross_district_note": "সিলেটের সাথে প্রায় সম্পূর্ণ গবেষণা ভাগাভাগি করা গেছে — উভয় জেলার profile একসাথে পড়লে সুরমা-কুশিয়ারা সিস্টেমের সম্পূর্ণ ছবি পাওয়া যাবে।",
}