# ============================================================
# FloodAI — data/district_profiles/dhaka.py — জেলা #২৩
# ⚠️⚠️ বড় finding: Urban Waterlogging-এর আসল কারণ drainage capacity,
# discharge_ratio না — নিচে বিস্তারিত।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

DHAKA_PROFILE = {
    "district": "ঢাকা",
    "district_lat": 23.63, "district_lon": 90.48,
    "station_count": 4,

    "critical_mechanism_finding": {
        "issue": "⚠️⚠️ Urban Waterlogging flood_type-এর জন্য discharge_ratio/danger_level ভিত্তিক ML feature ভুল জিনিস মাপছে",
        "evidence": (
            "একাধিক সূত্র (Dhaka Tribune, BSS, গবেষণাপত্র) নিশ্চিত করেছে: বর্ষায় "
            "চারপাশের নদী (বুড়িগঙ্গা/তুরাগ/বালু/শীতলক্ষ্যা)-র পানি বাড়লে "
            "কর্তৃপক্ষ **sluice gate বন্ধ করে দেয়** (নদীর পানি উল্টো শহরে ঢোকা "
            "ঠেকানোর জন্য) — ফলে শহরের নিজস্ব বৃষ্টির পানি সম্পূর্ণভাবে pumping "
            "station-নির্ভর হয়ে পড়ে, যেটার ক্ষমতা অপ্রতুল (মাত্র কয়েকটা pumping "
            "station + ৬৫টা ছোট পাম্প, মোট ক্ষমতা শহরের প্রয়োজনের তুলনায় নগণ্য)। "
            "BUET-এর IWFM অধ্যাপক A.K.M. Saiful Islam সরাসরি বলেছেন মূল কারণ "
            "'unplanned urbanization' — খাল ভরাট (৬৫টা থেকে কমে ২৬-৪৩টা), "
            "encroachment, insufficient drain size — নদীর water level না।"
        ),
        "implication": (
            "মানে ঢাকার জন্য danger_level/discharge_ratio ভিত্তিক risk score "
            "প্রায় ভুল প্রশ্নের উত্তর দিচ্ছে। আসল দরকার: rainfall_intensity "
            "(mm/hour, শুধু দৈনিক total না) vs drainage/pump capacity — এই দুটো "
            "একেবারেই এখন ১৪-feature মডেলে নেই।"
        ),
    },

    "stations": [
        {
            "name": "Dhaka", "ffwc_id": "SW42", "is_primary": True,
            "river": "বুড়িগঙ্গা (Buriganga)", "upazila": "Keraniganj", "union": None,
            "river_structure": {
                "category": "urban_tidal_river (drainage outlet, mega_trunk না)",
                "catchment": "ঢাকা শহরের দক্ষিণ পাশের প্রধান drainage outlet, তীব্র দূষণ ও দখলে সংকুচিত",
                "flow_behavior": "গেট-নিয়ন্ত্রিত — বর্ষায় প্রায়ই বন্ধ থাকে, তাই discharge measurement আসলে শহরের বৃষ্টির প্রকৃত ঝুঁকি প্রতিফলিত নাও করতে পারে",
                "upstream_reference": "Dhaka, BD", "lag_time_hours": 24,
            },
            "danger_level_m": 5.55, "highest_recorded_m": None,
            "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 555, "corrected_estimate": None, "note": "গেট-নিয়ন্ত্রিত urban outlet — discharge_ratio concept প্রায় অপ্রাসঙ্গিক, drainage-capacity feature দরকার", "confidence": "none"},
                "cn": {"old_value": 95, "reviewed_estimate": 95, "reasoning": "✅ ইতিমধ্যে প্রায় সর্বোচ্চ ও সঠিক — সম্পূর্ণ impervious urban surface-এর জন্য এটাই যুক্তিসঙ্গত, এই framework-এ সবচেয়ে ভালো-calibrated CN মান", "confidence": "high"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "উচ্চ", "reasoning": "প্রতি বছর কয়েক ঘণ্টার বৃষ্টিতেই ১৪০+ waterlogging hotspot চিহ্নিত হয় (DNCC/DSCC তথ্য), ১৫,০০০ হেক্টর জলাভূমি হারিয়েছে — জনসংখ্যা ও অর্থনৈতিক গুরুত্ব বিবেচনায় 'মাঝারি' কম মনে হচ্ছে", "source": "Dhaka Tribune (waterlogging hotspot ও wetland loss রিপোর্ট, ২০২৬)"},
            },
            "flood_type": "Urban Waterlogging",
            "inundation_bands": {"affected_areas": "উত্তরা, মিরপুর, ধানমন্ডি, বাড্ডা, মোহাম্মদপুর, বনশ্রী, নিউ বাজার — একাধিক সূত্রে নির্দিষ্ট", "status": "⚠️ placeholder — DEM বাকি, কিন্তু hotspot তালিকা সুনির্দিষ্ট"},
        },
        {"name": "Demra", "ffwc_id": "SW7.5", "is_primary": False, "river": "বালু (Balu)", "upazila": "Demra Thana", "union": None,
         "river_structure": {"category": "urban_tidal_river", "catchment": "শহরের পূর্ব পাশের drainage outlet", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
         "danger_level_m": 5.30, "verified_source": "flood_config.py-র সাথে মিলেছে",
         "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 530, "corrected_estimate": None, "confidence": "none"}, "cn": {"old_value": None, "reviewed_estimate": 95, "confidence": "high"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Dhaka primary station-এর অনুরূপ"}},
         "flood_type": "Urban Waterlogging", "inundation_bands": {"status": "⚠️ placeholder"}},
        {"name": "Mirpur", "ffwc_id": "SW302", "is_primary": False, "river": "তুরাগ (Turag)", "upazila": "Mirpur Thana", "union": None,
         "river_structure": {"category": "urban_tidal_river", "catchment": "শহরের পশ্চিম/উত্তর পাশের drainage outlet, উত্তরা এলাকা বিশেষভাবে প্রভাবিত", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
         "danger_level_m": 5.50, "verified_source": "flood_config.py-র সাথে মিলেছে",
         "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 550, "corrected_estimate": None, "confidence": "none"}, "cn": {"old_value": None, "reviewed_estimate": 95, "confidence": "high"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "উত্তরা এলাকার সাম্প্রতিক জলাভূমি-ধ্বংসের সাথে সরাসরি সম্পর্কিত (Dhaka Tribune)"}},
         "flood_type": "Urban Waterlogging", "inundation_bands": {"status": "⚠️ placeholder — তবে উত্তরা/দিয়াবাড়ি নির্দিষ্টভাবে চিহ্নিত"}},
        {"name": "Hariharpara", "ffwc_id": "SW43", "is_primary": False, "river": "বুড়িগঙ্গা (Buriganga)", "upazila": "Keraniganj", "union": None,
         "river_structure": {"category": "urban_tidal_river", "catchment": "Dhaka(SW42)-র একই বুড়িগঙ্গা, ভিন্ন gauge point", "upstream_reference": "Dhaka, BD", "lag_time_hours": 24},
         "danger_level_m": 5.35, "verified_source": "flood_config.py-র সাথে মিলেছে",
         "gap_found": "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র ঢাকার rivers লিস্টে নেই (শুধু বুড়িগঙ্গা/Dhaka, বালু/Demra, তুরাগ/Mirpur আছে) — মুন্সিগঞ্জের Mawa-প্যাটার্নের পুনরাবৃত্তি।",
         "ml_features_verified": {"reference_discharge_m3s": {"old_buggy_value": 535, "corrected_estimate": None, "confidence": "none"}, "cn": {"old_value": None, "reviewed_estimate": 95, "confidence": "high"}, "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Dhaka primary station-এর একই বুড়িগঙ্গা reach"}},
         "flood_type": "Urban Waterlogging", "inundation_bands": {"status": "⚠️ placeholder"}},
    ],

    "soil_moisture_weight_note": "⚠️ সম্পূর্ণ ভিন্ন প্রেক্ষাপট — impervious urban surface-এ soil_moisture প্রায় অপ্রাসঙ্গিক (মাটি নেই)। প্রকৃত দরকার: rainfall_intensity (mm/ঘণ্টা) + drainage/pump capacity + sluice gate status — এই তিনটাই বর্তমান মডেলে অনুপস্থিত।",

    "confluence_note": "ঢাকা CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "গাজীপুর, নারায়ণগঞ্জ, চট্টগ্রাম — সবগুলোই একই drainage-capacity সমস্যায় ভোগে, একই hybrid rainfall-intensity+drainage মডেল দরকার।",
}