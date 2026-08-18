# ============================================================
# FloodAI — data/district_profiles/bogura.py
#
# জেলা-বাই-জেলা framework-এর ৬ষ্ঠ জেলা। আগের ৫টা জেলার সাথে হুবহু
# একই ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ Coordinate/administrative verification-এ যা পাওয়া গেছে:
#   1. Sariakandi — coordinate মোটামুটি ঠিক ছিল (~১১ কিমি off)
#   2. Bogra (Karatoa) — upazila নিয়ে ছোট conflict (BWDB-র দুইটা
#      ভিন্ন ডেটাসেটে ভিন্ন উত্তর — দেখুন verification_note), কিন্তু
#      FFWC live current data stations.py-র সাথে মেলে
#   3. Shimulbari — ⚠️ Tangail-এর Nayarhat-এর মতোই একটা সম্ভাব্য
#      cross-district সমস্যা পাওয়া গেছে। BWDB-র নিজস্ব BM pillar
#      (benchmark) ডেটার ভেতরেই দ্বন্দ্ব আছে — structured fields বলছে
#      District: Bogura, কিন্তু pillar-এর free-text বিবরণে লেখা "PS:
#      Gobindaganj, Gaibandha"। Gobindaganj upazila বাস্তবে Gaibandha
#      জেলারই অংশ, Bogura-র না — তাই এই station সম্ভবত জেলা-সীমান্তে বা
#      ভুল জেলায় ট্যাগ করা।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BOGURA_PROFILE = {
    "district": "বগুড়া",
    "district_lat": 24.8465,
    "district_lon": 89.3773,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ৩টা — একটা যমুনার উপর (Sariakandi), একটা
    # প্রায়-মৃত করতোয়ার উপর (Bogra), একটা বাঙালি নদীর উপর (Shimulbari,
    # যদিও এই শেষেরটার জেলা-অবস্থান নিয়ে প্রশ্ন আছে)।
    "station_count": 3,

    "stations": [
        {
            "name": "Sariakandi",
            "ffwc_id": "SW15J",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "যমুনা (Jamuna)",
            "upazila": "Sariakandi",
            "union": "Sariakandi",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই যমুনা মূল প্রবাহ, বগুড়া জেলার পূর্ব সীমানা এই "
                    "নদী দিয়েই নির্ধারিত (সারিয়াকান্দি জেলার পূর্বতম "
                    "উপজেলা)। এলাকার প্রায় ৪০% জমি জল/চর — মহাস্থানগড়ের "
                    "(প্রাচীন পুণ্ড্রনগর) কাছাকাছি এলাকা।"
                ),
                "flow_behavior": "একই braided, migrating চরিত্র, বাকি যমুনা-corridor জেলাগুলোর মতোই।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 16.25,  # ✅ FFWC verify করা
            "highest_recorded_m": 18.59,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। coordinate মোটামুটি সঠিক — "
                "stations.py-তে lat=24.75, lon=89.55, BWDB official "
                "hydrology survey ও BM pillar ডেটা দুটোই lat≈24.84-24.85, "
                "lon≈89.58 বলছে — প্রায় ১১ কিমি উত্তর-পূর্বে সরাতে হবে, "
                "আগের জেলাগুলোর তুলনায় ছোট correction।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1625,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ, mean annual ~২০,২০০ m³/s, bankfull ৪৫,০০০-৬০,০০০ m³/s",
                    "source": "Best et al. 2022 (একই নদী, Bahadurabad-Sirajganj stretch-এর মাঝামাঝি)",
                    "cross_check": "✅ river_categories.py-তে বগুড়া=mega_trunk হওয়া উচিত (আগের যমুনা-জেলাগুলোর সাথে সামঞ্জস্যপূর্ণ)।",
                    "critical_caveat": "আগের ৫টা যমুনা-করিডোর জেলার মতোই একই train_model.py বাগ প্রযোজ্য।",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই যমুনা floodplain, একই TR-55 যুক্তি", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "সারিয়াকান্দি ঐতিহাসিকভাবে যমুনার char-erosion-প্রবণ এলাকা, নিয়মিত বন্যা-কবলিত — বাকি যমুনা-corridor জেলাগুলোর সাথে সামঞ্জস্যপূর্ণ 'উচ্চ' রেটিং।",
                    "source": "Sariakandi Upazila Wikipedia (৪০% জমি জল/চর)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক riverine বন্যা, বাকি যমুনা-corridor জেলাগুলোর মতোই।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "সারিয়াকান্দি উপজেলার চরাঞ্চল",
                "50cm_to_1m_above_danger": "ধুনট, সোনাতলার নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — বিস্তৃত এলাকা প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Bogra",
            "ffwc_id": "SW65",
            "is_primary": False,

            "river": "করতোয়া (Karatoa)",
            "upazila": "Shajahanpur",  # ✅ FFWC live current + stations.py দুটোই একমত
            "union": "Sultanganj",

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "ঐতিহাসিকভাবে করতোয়া ছিল উত্তরবঙ্গের সবচেয়ে গুরুত্বপূর্ণ "
                    "ও পবিত্র নদী (মহাভারত-এ উল্লেখিত, প্রাচীন পুণ্ড্রবর্ধনের "
                    "সীমানা নির্ধারক) — কিন্তু এখন 'বগুড়া-করতোয়া' অংশ একটা "
                    "সংকুচিত, প্রায়-মৃত নদী। Brahmaputra Right Bank "
                    "Embankment নির্মাণের পর discharge দ্রুত কমে গেছে।"
                ),
                "flow_behavior": (
                    "সর্বোচ্চ discharge মাত্র ~৩,০০০ cusec (~৮৫ m³/s)-এর "
                    "নিচে — river_categories.py-র 'small_or_tidal' রেঞ্জের "
                    "একেবারে নিচের দিকে। বগুড়া শহর পার হয়ে বাঙালি নদীর "
                    "সাথে মিশে ফুলঝোর নাম নেয়, তারপর হুড়াসাগরে গিয়ে পড়ে "
                    "(অর্থাৎ সিরাজগঞ্জের Baghabari station-এর একই সিস্টেমের "
                    "উজানের অংশ — Bogura-Sirajganj hydrological link)।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 15.85,  # ✅ FFWC verify করা
            "highest_recorded_m": 16.61,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ও upazila (Shajahanpur) দুটোই FFWC live "
                "current data-তে stations.py-র সাথে মিলে যাচ্ছে ✅। ⚠️ "
                "তবে একটা ছোট অসঙ্গতি — BWDB-র নিজের official hydrology "
                "survey database (water_level_data_available_print.php) "
                "আলাদাভাবে এই একই station (SW65)-এর upazila 'Bogura Sadar' "
                "বলছে, coordinate lat=24.8459, lon=89.3792। FFWC live "
                "current + stations.py বলছে 'Shajahanpur'। যেহেতু দুই "
                "উপজেলাই ভৌগোলিকভাবে পাশাপাশি (বগুড়া শহরের চারপাশে), এবং "
                "FFWC-র real-time current data-ই বেশি নির্ভরযোগ্য মনে "
                "হচ্ছে (কারণ এটা সাম্প্রতিকতম), stations.py-র upazila অপরিবর্তিত "
                "রাখা হলো, তবে coordinate BWDB-র survey মান অনুযায়ী "
                "আপডেট করার পরামর্শ (stations.py-র lat=24.80,lon=89.42 "
                "থেকে lat=24.8459,lon=89.3792 — প্রায় ৭ কিমি পার্থক্য)।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1585,
                    "corrected_estimate": 70,
                    "corrected_range": "সর্বোচ্চ ~৩,০০০ cusec (~৮৫ m³/s)-এর নিচে, ক্রমহ্রাসমান — river_categories.py-র small_or_tidal রেঞ্জের একেবারে নিচের দিকে",
                    "source": "Banglapedia (Karatoya River, Brahmaputra-Jamuna River System)",
                    "confidence": "moderate — historical max discharge উদ্ধৃত করা আছে, কিন্তু বর্তমান average আলাদা হতে পারে",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "উত্তরবঙ্গের floodplain, তবে নদী নিজেই সংকুচিত হওয়ায় সরাসরি overflow ঝুঁকি কম, বেশি waterlogging-প্রবণ", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "নিম্ন-মাঝারি",
                    "reasoning": (
                        "নদী নিজেই প্রায় মৃত হয়ে যাওয়ায় classic riverine "
                        "flood risk কম, কিন্তু বগুড়া শহরের ঘনবসতির কারণে "
                        "সামান্য water rise-ও urban drainage সমস্যা তৈরি করতে "
                        "পারে — এটা বেশি waterlogging character-এর ঝুঁকি, "
                        "trunk-river surge-এর না।"
                    ),
                    "source": "Banglapedia (discharge decline history)",
                },
            },

            "flood_type": "Urban Waterlogging (নদী সংকুচিত হওয়ায় classic riverine-এর চেয়ে বেশি প্রাসঙ্গিক)",
            "flood_type_note": (
                "⚠️ গুরুত্বপূর্ণ nuance — মানিকগঞ্জের Jagir/পুরাতন "
                "ধলেশ্বরীর মতোই, করতোয়া এখানে ঐতিহাসিকভাবে বড় নদী ছিল "
                "কিন্তু এখন সংকুচিত। বগুড়া শহর (জেলা সদর, ঘনবসতিপূর্ণ) এই "
                "station-এর কাছেই — সংকুচিত channel capacity urban "
                "drainage-এর সাথে interact করে waterlogging ঝুঁকি তৈরি "
                "করতে পারে, শুধু classic riverine ঝুঁকি না।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই, শহুরে drainage-নির্ভর ঝুঁকি হওয়ায় সাধারণ river inundation model কম প্রাসঙ্গিক"},
        },
        {
            "name": "Shimulbari",
            "ffwc_id": "SW10",
            "is_primary": False,

            "river": "বাঙালি (Bangali)",
            "upazila": "Gobindaganj (FFWC/stations.py অনুযায়ী) — ⚠️ দেখুন verification_note",
            "union": "Salmara (FFWC অনুযায়ী)",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "বাঙালি নদী উৎপত্তি Gaibandha-তে ঘাঘট নামে, তারপর "
                    "দুই ভাগে বিভক্ত হয়ে একটা অংশ পশ্চিমে গিয়ে করতোয়ায় "
                    "(Sherpur, বগুড়া) মেশে, আরেকটা অংশ দক্ষিণে গিয়ে "
                    "বগুড়াতেই আরও দুই ভাগে বিভক্ত হয়ে যমুনা ও করতোয়ায় "
                    "মেশে। সাম্প্রতিক গবেষণা অনুযায়ী তিস্তার flow কমে "
                    "যাওয়ায় যমুনা এখন বাঙালি নদীর মূল water source "
                    "হয়ে উঠছে বলে কিছু বিশেষজ্ঞ (River Research "
                    "Institute-এর সাবেক নির্বাহী পরিচালক সহ) মনে করছেন।"
                ),
                "flow_behavior": (
                    "flow ৪০০ থেকে ২১,০০০ cusec (~১১-৫৯৪ m³/s) পর্যন্ত "
                    "ওঠানামা করে — করতোয়ার চেয়ে যথেষ্ট বড়, কিন্তু "
                    "mega_trunk যমুনার ধারেকাছেও না।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 17.75,  # ✅ FFWC verify করা
            "highest_recorded_m": 18.37,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। ⚠️ কিন্তু একটা গুরুত্বপূর্ণ "
                "cross-district সন্দেহ পাওয়া গেছে, Tangail-এর Nayarhat-এর "
                "মতোই ধরনের। BWDB-র নিজস্ব BM pillar (benchmark) ডেটার "
                "ভেতরেই দ্বন্দ্ব — structured fields বলছে 'District: "
                "Bogura, Upazila: Sonatola', কিন্তু pillar-এর free-text "
                "অবস্থান-বিবরণে লেখা 'S/E corner of Toslima House, Vill: "
                "Uzirerpara, PS: Gobindaganj, Gaibandha'। Gobindaganj "
                "upazila বাস্তবে Gaibandha জেলারই অংশ, Bogura-র না। FFWC "
                "live current data অবশ্য 'District: Bogra, Upazilla: "
                "Gobindaganj' বলছে — যেটা নিজেই স্ববিরোধী, কারণ Gobindaganj "
                "নামে Bogura-র কোনো উপজেলা নেই (এটা Gaibandha-র উপজেলা)। "
                "এই তিনটা সোর্স (FFWC live, BWDB survey table, BWDB "
                "pillar note) একে অপরের সাথে সামঞ্জস্যপূর্ণ না — চূড়ান্ত "
                "সিদ্ধান্তের জন্য আরও verification দরকার (সম্ভবত সরাসরি "
                "BWDB-কে email করে জিজ্ঞেস করা)। আপাতত stations.py-র "
                "বর্তমান জেলা-assignment (Bogura) অপরিবর্তিত রাখা হলো, "
                "কিন্তু এটা নিশ্চিত না।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1775,
                    "corrected_estimate": 300,
                    "corrected_range": "৪০০-২১,০০০ cusec (~১১-৫৯৪ m³/s), মৌসুমভেদে বিরাট তারতম্য",
                    "source": "Wikipedia (Bangali River)",
                    "confidence": "moderate — measured range পাওয়া গেছে, কিন্তু এই নির্দিষ্ট station-এর (upstream-most, Gobindaganj/Sonatola stretch) specific data না",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "উত্তরবঙ্গের floodplain, একই TR-55 যুক্তি", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": "যমুনার তুলনায় ছোট নদী, কিন্তু flow range-এর ঊর্ধ্বসীমা (২১,০০০ cusec) যথেষ্ট উল্লেখযোগ্য — সম্পূর্ণ নগণ্য না।",
                    "source": "Wikipedia (Bangali River)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ জেলা-assignment নিজেই অনিশ্চিত (উপরে দেখুন) — এই "
                "station Bogura-র বদলে Gaibandha-র হতে পারে। যদি তাই হয়, "
                "তাহলে এটা এই profile থেকে সরিয়ে Gaibandha-র future "
                "profile-এ যোগ করা উচিত।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান station (Sariakandi/যমুনা)-এর জন্য discharge/water-level "
        "trend primary, soil moisture কমানো — আগের জেলাগুলোর মতোই। Bogra "
        "(করতোয়া)-এর জন্য যেহেতু নদী প্রায় মৃত এবং শহুরে drainage ফ্যাক্টর "
        "প্রাসঙ্গিক, local_rain-এর weight তুলনামূলক বেশি রাখা উচিত — ঠিক "
        "মানিকগঞ্জের Jagir বা জামালপুরের Jamalpur (Old Brahmaputra) "
        "station-এর মতো যুক্তি। Shimulbari (বাঙালি)-এর জন্য জেলা-assignment "
        "নিজেই অনিশ্চিত থাকায় এই মুহূর্তে weight নির্ধারণ স্থগিত রাখা "
        "ভালো, verification সম্পূর্ণ হওয়া পর্যন্ত।"
    ),

    "confluence_note": (
        "বগুড়া যমুনা-করিডোরে (Jamalpur → Sirajganj → Tangail → Manikganj) "
        "একটা নতুন সংযোগ যোগ করেছে — Sariakandi আসলে Sirajganj-এর "
        "Kazipur-এর উজানে (আরও উত্তরে)। এছাড়া করতোয়া-বাঙালি-হুড়াসাগর "
        "সিস্টেমের একটা নতুন উজানের বিন্দুও যোগ হলো — Bogra (করতোয়া) ও "
        "Sirajganj-এর Baghabari (হুড়াসাগর) একই নদী-সিস্টেমের দুই প্রান্ত। "
        "এই দুইটা connection ভবিষ্যতে করতোয়া-আত্রাই-হুড়াসাগর সিস্টেমের "
        "একটা coherent multi-district picture তৈরিতে সাহায্য করবে।"
    ),

    "cross_district_flags": (
        "⚠️ Shimulbari-র জেলা-দ্বন্দ্ব Tangail-এর Nayarhat-এর প্যাটার্নই "
        "আবার দেখাচ্ছে — কিন্তু এবার BWDB-র নিজের ডেটার ভেতরেই (survey "
        "table বনাম BM pillar note) দ্বন্দ্ব, শুধু FFWC live বনাম BWDB "
        "survey না। এটা নিশ্চিত করছে যে district-boundary-এর কাছাকাছি "
        "station-গুলোতে multiple official সোর্সও নিজেদের মধ্যে একমত না "
        "হতে পারে — ভবিষ্যতে যেকোনো জেলা-সীমান্ত-ঘেঁষা station পেলে অন্তত "
        "৩টা independent সোর্স (FFWC live, BWDB survey table, BWDB BM "
        "pillar) মিলিয়ে দেখা উচিত, একটাতেই থেমে না গিয়ে।"
    ),
}