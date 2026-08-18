# ============================================================
# FloodAI — data/district_profiles/munshiganj.py
#
# জেলা-বাই-জেলা framework-এর ৩য় জেলা। রাজবাড়ী/মানিকগঞ্জের মতোই ৭-ধাপ
# পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ মুন্সিগঞ্জ flood_types/riverine.py-র CONFLUENCE_DISTRICTS-এর একটা —
# database-এ ঠিক এই জেলাই ১০০.০% "বিপদ"-এ আটকে ছিল (padma_ratio bug)।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MUNSHIGANJ_PROFILE = {
    "district": "মুন্সিগঞ্জ",
    "district_lat": 23.55,
    "district_lon": 90.33,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 3,

    "stations": [
        {
            "name": "Bhagyakul",
            "ffwc_id": "SW93.4",
            "is_primary": True,

            "river": "পদ্মা (Padma)",
            "upazila": "Sreenagar",
            "union": "Baghra",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "রাজবাড়ীর Goalondo থেকে সামান্য ভাটিতে — একই পদ্মা নদী, "
                    "গঙ্গা+যমুনার মিলিত প্রবাহ। danger_level কম (৫.৮৫ vs "
                    "রাজবাড়ীর ৮.২০) কারণ এটা আরো নিচু/সমতল এলাকা (elevation "
                    "drop), discharge magnitude প্রায় একই থাকার কথা।"
                ),
                "flow_behavior": "মেঘনার সাথে মেশার আগে শেষ বড় stretch — পদ্মা এখান থেকে ভাটিতে গিয়ে চাঁদপুরে মেঘনার সাথে মেশে",
                "upstream_reference": "Malda, IN",  # flood_config.py অনুযায়ী রাজবাড়ীর মতোই
                "lag_time_hours": 44,
            },

            "danger_level_m": 5.85,  # ✅ FFWC verify করা (stid)
            "highest_recorded_m": 6.76,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 585,  # danger_level(5.85)*100
                    "corrected_estimate": 75000,  # bankfull (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত)  # রাজবাড়ীর মতোই পদ্মার mean discharge
                    "corrected_range": "mean ~৩০,০০০ m³/s, bankfull ~৭৫,০০০ m³/s (রাজবাড়ীর Goalondo-র সাথে একই নদী, একই estimate পুনঃব্যবহার করা হলো)",
                    "source": "রাজবাড়ী profile-এর Padma source-ই প্রযোজ্য (Neill; Wikipedia Padma River)",
                    "cross_check": "✅ river_categories.py: মুন্সিগঞ্জ=mega_trunk, রেঞ্জ (10,000-200,000 m³/s) — মিলছে",
                    "critical_caveat": "রাজবাড়ী/মানিকগঞ্জের মতোই — model retrain বা rule-override ছাড়া শুধু এই সংখ্যা বসালে chaos হবে",
                },
                "cn": {"old_value": 77, "reviewed_estimate": 89, "reasoning": "একই পদ্মা-পলিমাটি floodplain যুক্তি (রাজবাড়ী/মানিকগঞ্জের মতো)", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "২০২০ বন্যায় মুন্সিগঞ্জের ৪টা উপজেলার (সদর, লৌহজং, "
                        "টঙ্গিবাড়ী, শ্রীনগর) ২৯টা ইউনিয়নের ১৮৯টা গ্রাম প্লাবিত হয়েছিল "
                        "(~৪০,০০০ মানুষ ক্ষতিগ্রস্ত)। এছাড়া Mawa/Shambhu Haldar Kandi "
                        "এলাকায় সাম্প্রতিক বছরগুলোতে তীব্র নদীভাঙনে পুরো বসতবাড়ি "
                        "নদীগর্ভে চলে গেছে (bdnews24, ২০২২)। 'মাঝারি' এই বাস্তবতার "
                        "তুলনায় কম মনে হচ্ছে।"
                    ),
                    "source": "risingbd.com (২০২০ বন্যা রিপোর্ট); bdnews24 (২০২২ erosion রিপোর্ট)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক পদ্মা riverine বন্যা + তীব্র char erosion (Mawa-Sureshwar reach বিশেষভাবে গবেষণায় উল্লেখিত ভাঙন-প্রবণ এলাকা হিসেবে চিহ্নিত)",

            "inundation_bands": {
                "0_to_50cm_above_danger": "শ্রীনগর/লৌহজং-এর চরাঞ্চল",
                "50cm_to_1m_above_danger": "টঙ্গিবাড়ী, মুন্সিগঞ্জ সদরের নিম্নাঞ্চল",
                "above_1m_danger": "২০২০ স্কেলে — ৪ উপজেলার ব্যাপক অংশ (রেফারেন্স: ১৮৯ গ্রাম প্লাবিত হয়েছিল)",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Mawa",
            "ffwc_id": "SW93.5",
            "is_primary": False,

            "river": "পদ্মা (Padma)",
            "upazila": "Lohajang",
            "union": "Medini Mandal",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "Bhagyakul-এর মতোই একই পদ্মা, সামান্য ভাটিতে — পদ্মা সেতুর অবস্থান এই স্টেশনের কাছাকাছি",
                "flow_behavior": "একই পদ্মা trunk flow, তবে এই reach-এ dredging (পদ্মা সেতু প্রকল্পের) erosion বাড়াচ্ছে বলে গবেষণায় উল্লেখ আছে",
                "upstream_reference": "Malda, IN",
                "lag_time_hours": 44,
            },

            "danger_level_m": 5.65,  # ✅ FFWC verify করা
            "highest_recorded_m": 6.41,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "gap_found": (
                "⚠️ এই station stations.py-তে আছে, কিন্তু flood_config.py-র মুন্সিগঞ্জ "
                "entry-র 'rivers' লিস্টে নেই — শুধু Bhagyakul আর Meghna-Br আছে। "
                "Mawa সম্পূর্ণ বাদ পড়ে গেছে, যদিও এটা পদ্মা সেতুর কাছেই এবং একটা "
                "সক্রিয়ভাবে ভাঙন-প্রবণ (dredging-related erosion) পয়েন্ট হিসেবে "
                "গবেষণায় নির্দিষ্টভাবে উল্লেখ করা হয়েছে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 565,
                    "corrected_estimate": 75000,  # bankfull (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত)
                    "corrected_range": "Bhagyakul-এর মতোই একই পদ্মা reach",
                    "confidence": "moderate — একই নদীর দুই পয়েন্ট বলে Bhagyakul-এর estimate পুনঃব্যবহারযোগ্য",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "পদ্মা সেতু dredging-related অতিরিক্ত ভাঙনের কারণে Bhagyakul-এর চেয়েও বেশি নজরদারি দরকার হতে পারে (Aishi et al. 2024 গবেষণা অনুযায়ী Mawa-Sureshwar reach বিশেষভাবে অধ্যয়িত)",
                },
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — Bhagyakul-এর কাছাকাছি ধরে নেওয়া যায়"},
        },
        {
            "name": "Meghna-Br",
            "ffwc_id": "SW275.5",
            "is_primary": False,

            "river": "মেঘনা (Meghna)",
            "upazila": "Gazaria",
            "union": "Tenger Char",

            "river_structure": {
                "category": "large_regional (Upper Meghna, Padma সাথে মেশার আগে)",
                "catchment": (
                    "Surma-Kushiyara-Barak system থেকে আসা Upper Meghna — সিলেট/"
                    "ভারতের মেঘালয়-আসাম পাহাড় থেকে শুরু। Bhairab Bazar-এ যেই flow "
                    "মাপা হয় সেটাই এখানে (Gazaria) পর্যন্ত আসে, চাঁদপুরে গিয়ে পদ্মার "
                    "সাথে মিশে 'Lower Meghna' হয় (সেখানে discharge বহুগুণ বেড়ে যায়)।"
                ),
                "flow_behavior": "পদ্মার তুলনায় ছোট কিন্তু trunk-এর কাছাকাছি স্কেলের নদী, Bhairab Bazar-এর ডেটা দিয়ে আনুমানিক",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 4.55,  # ✅ FFWC verify করা
            "highest_recorded_m": 7.10,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 455,  # danger_level(4.55)*100
                    "corrected_estimate": 15000,
                    "corrected_range": (
                        "Bhairab Bazar-এ mean annual ~৪,৬০০-৬,৫০০ m³/s (Banglapedia); "
                        "flood-frequency return period ২ বছরে ~১০,৭০০ m³/s থেকে "
                        "২০০ বছরে ~২৪,৫০০ m³/s (Gumbel/LP3 বিশ্লেষণ, ১৯৯০-২০২১ ডেটা); "
                        "ঐতিহাসিক রেকর্ড পিক ~১৯,৮০০ m³/s"
                    ),
                    "source": "Banglapedia (Water Resources, River and Drainage System); Characteristics of Flood in Meghna River Basin (২০২৩ গবেষণা, BWDB ডেটা)",
                    "note": "⚠️ Gazaria (এই station) Bhairab Bazar থেকে একটু ভাটিতে, তাই real discharge কিছুটা বেশি হতে পারে — moderate confidence",
                    "critical_caveat": "একই retrain/override সমস্যা প্রযোজ্য",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "Padma-র চেয়ে একটু কম পলিমাটি-নির্ভর হলেও একই floodplain-ধরনের অঞ্চল", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "মূল পদ্মা station দুটোর (Bhagyakul/Mawa) তুলনায় কম গুরুত্বপূর্ণ, কিন্তু danger_level সবচেয়ে কম (৪.৫৫) হওয়ায় দ্রুত crossing সম্ভব"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    "soil_moisture_weight_note": (
        "প্রধান দুই station (Bhagyakul, Mawa) পদ্মা trunk river — discharge/"
        "water-level trend primary থাকা উচিত, soil moisture secondary। "
        "Meghna-Br-এর জন্যও একই যুক্তি প্রযোজ্য।"
    ),

    "confluence_note": (
        "✅ মুন্সিগঞ্জ CONFLUENCE_DISTRICTS-এর একটা, এবং database-এ যাচাই করা "
        "সময়ে ঠিক এই জেলাই padma_ratio bug-এর কারণে ১০০.০% 'বিপদ'-এ আটকে "
        "ছিল। রাজবাড়ী/মানিকগঞ্জের মতো এটাও পদ্মা trunk river হওয়ায় একই "
        "reference_discharge (~৩০,০০০ m³/s) প্রযোজ্য।"
    ),
}