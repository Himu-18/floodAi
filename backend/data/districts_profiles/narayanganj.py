# ============================================================
# FloodAI — data/district_profiles/narayanganj.py — জেলা #২৫
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NARAYANGANJ_PROFILE = {
    "district": "নারায়ণগঞ্জ",
    "district_lat": 23.58, "district_lon": 90.45,
    "station_count": 3,
    "station_count_note": "✅ তিনটা station-ই flood_config.py-তে সঠিকভাবে linked, কোনো gap নেই।",

    "stations": [
        {
            "name": "Narayanganj", "ffwc_id": "SW180", "is_primary": True,
            "river": "শীতলক্ষ্যা/লাখ্যা (Sitalakhya/Lakhya)", "upazila": "Narayanganj Sadar", "union": None,
            "river_structure": {
                "category": "urban_industrial_river (mega_trunk না, কিন্তু বড় শিল্পাঞ্চলীয় নদী)",
                "catchment": "ঢাকার পূর্ব-দক্ষিণে শিল্প-বন্দর শহর নারায়ণগঞ্জের প্রধান নদী",
                "note": "⚠️ flood_config.py-তে river name 'শীতলক্ষ্যা' লেখা, কিন্তু ffwc_station field-এ 'নদী Lakhya' লেখা — এই দুই নাম বাংলাদেশে প্রায়ই একই নদীর জন্য ব্যবহৃত হয় (বা কাছাকাছি সংযুক্ত), তবে টেকনিক্যালি Lakhya ও শীতলক্ষ্যা ভিন্ন named reach হতে পারে — নিশ্চিত করা দরকার এটা একই নদীর কথা বলছে কিনা।",
                "upstream_reference": "Dhaka, BD", "lag_time_hours": 24,
            },
            "danger_level_m": 5.05, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 505, "corrected_estimate": None, "note": "শিল্প-দূষিত urban river — drainage-capacity+pollution উভয়ই বিবেচ্য, শুধু discharge_ratio না", "confidence": "none"},
                "cn": {"old_value": 95, "reviewed_estimate": 95, "reasoning": "✅ ঢাকা মেট্রোর অন্যান্য জেলার মতোই সঠিক", "confidence": "high"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "ফতুল্লা/চাষাড়া/সিদ্ধিরগঞ্জ ঘনবসতিপূর্ণ শিল্পাঞ্চল — ঢাকা মেট্রোর অন্য জেলাগুলোর সাথে সঙ্গতি রাখতে upgrade করা হলো"},
            },
            "flood_type": "Urban Waterlogging",
            "inundation_bands": {"affected_areas": "ফতুল্লা, চাষাড়া, সিদ্ধিরগঞ্জ (flood_config.py-তে নির্দিষ্টভাবে উল্লেখিত)", "status": "⚠️ placeholder"},
        },
        {
            "name": "Bayderbazar", "ffwc_id": "SW275", "is_primary": False,
            "river": "মেঘনা (Meghna)", "upazila": "Araihazar", "union": None,
            "river_structure": {"category": "large_regional", "catchment": "নারায়ণগঞ্জের পূর্ব প্রান্তে মেঘনার সংস্পর্শ — এটা আসলে ঢাকা মেট্রোর ছোট urban river-এর চেয়ে ভিন্ন, বড় trunk-এর কাছাকাছি নদী", "upstream_reference": "Dhaka, BD", "upstream_reference_caveat": "⚠️ প্রশ্নসাপেক্ষ — মেঘনা নদীর জন্য 'Dhaka,BD' upstream reference অস্বাভাবিক, কিশোরগঞ্জের মতো Meghalaya/Assam-সংযুক্ত reference বেশি যুক্তিসঙ্গত হতে পারে", "lag_time_hours": 24},
            "danger_level_m": 4.70, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 470, "corrected_estimate": 4600, "corrected_range": "কিশোরগঞ্জের Bhairab Bazar থেকে reuse করা মেঘনার সংখ্যা — এটা ছোট urban khal না, real মেঘনা", "confidence": "moderate — কিশোরগঞ্জ profile থেকে cross-reference"}, "cn": {"old_value": None, "reviewed_estimate": 87, "confidence": "moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "মেঘনার সরাসরি সংস্পর্শ, কিশোরগঞ্জের অনুরূপ ঝুঁকি"}},
            "flood_type": "Riverine",
            "flood_type_note": "⚠️ এই secondary station-টা আসলে 'Urban Waterlogging' না, বরং সত্যিকারের Riverine (মেঘনা) — flood_config.py-তে পুরো জেলার flood_type='Urban Waterlogging' ধরে নেওয়া হলেও, Araihazar উপজেলা (Bayderbazar) আসলে ভিন্ন ধরনের ঝুঁকিতে আছে।",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Rekabi-Bazar", "ffwc_id": "SW71A", "is_primary": False,
            "river": "ধলেশ্বরী (Dhaleswari)", "upazila": "Narayanganj Sadar", "union": None,
            "river_structure": {"category": "medium (মুন্সিগঞ্জ/মানিকগঞ্জের ধলেশ্বরীর একই নদীর ভিন্ন অংশ)", "catchment": "শহরের দক্ষিণ প্রান্তের নদী", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
            "danger_level_m": 4.75, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 475, "corrected_estimate": 1200, "corrected_range": "মানিকগঞ্জের 'পুরাতন ধলেশ্বরী' (Jagir station)-এর সাথে তুলনীয়", "confidence": "low-moderate"}, "cn": {"old_value": None, "reviewed_estimate": 90, "confidence": "low-moderate"}, "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "urban core-এর চেয়ে কম critical, কিন্তু নদীভাঙন-প্রবণ"}},
            "flood_type": "Riverine (secondary — Urban Waterlogging না)",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],

    "soil_moisture_weight_note": "মিশ্র জেলা — primary station (urban) এ drainage-capacity, secondary stations (Bayderbazar/Rekabi-Bazar) এ discharge-ratio প্রাসঙ্গিক। এই জেলাটা এই framework-এ প্রথম উদাহরণ যেখানে একই জেলার ভেতরে দুই সম্পূর্ণ ভিন্ন flood dynamics (urban + riverine) মিশে আছে।",

    "confluence_note": "নারায়ণগঞ্জ CONFLUENCE_DISTRICTS-এ নেই, কিন্তু Bayderbazar station-এর মাধ্যমে মেঘনার সাথে যুক্ত।",

    "cross_district_note": "ঢাকা/গাজীপুরের urban dynamics + কিশোরগঞ্জ/মুন্সিগঞ্জের riverine dynamics — দুটোই এই একটা জেলায় প্রাসঙ্গিক।",
}