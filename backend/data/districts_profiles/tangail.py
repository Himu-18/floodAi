# ============================================================
# FloodAI — data/district_profiles/tangail.py
#
# জেলা-বাই-জেলা framework-এর ৫ম জেলা। রাজবাড়ী/মানিকগঞ্জ/জামালপুর/
# সিরাজগঞ্জের সাথে হুবহু একই ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ সবচেয়ে গুরুত্বপূর্ণ finding এই জেলায়: Nayarhat (SW14.5, Bangshi)
# স্টেশনটা stations.py ও FFWC live site দুটোতেই "Tangail" জেলার নামে
# আছে, কিন্তু BWDB-র official hydrology survey database এবং একটা
# independent academic paper (Jahangirnagar University) দুটোই স্পষ্ট
# করে বলছে এই gauge-টা আসলে **Dhaka জেলার Savar উপজেলায়** অবস্থিত —
# বাংশী নদী Tangail (Mirzapur) থেকে বেরিয়ে Dhaka (Savar)-এ প্রবেশ করার
# পরের বিন্দুতে। হিমুর সিদ্ধান্ত অনুযায়ী এটা এই profile-এ রাখা হয়েছে,
# কিন্তু "boundary/downstream station" হিসেবে স্পষ্ট caveat সহ — কারণ
# এটা মূলত Tangail-এর upstream flow-এর প্রতিফলন বহন করে, কিন্তু গেজ
# পয়েন্ট নিজে ভৌগোলিকভাবে জেলার বাইরে।
#
# ⚠️ Coordinate verification-এ যা পাওয়া গেছে:
#   1. Porabari — upazila নিয়ে conflict (FFWC/stations.py: "Nagarpur",
#      BWDB official + Wikipedia Porabari Union: "Tangail Sadar")।
#      coordinate ~৩০ কিমি off ছিল stations.py-তে।
#   2. Nayarhat — উপরে বর্ণিত জেলা-নিজেই ভুল থাকার সমস্যা। coordinate-ও
#      অনেক দূরে (stations.py: 24.13,90.13 বনাম BWDB Savar coordinate
#      23.9057,90.2310)।
#   danger_level দুটোতেই ঠিক ছিল (11.80 / 6.85)।
#
# ⚠️ flood_config.py-তে টাঙ্গাইলের জন্য একটা তৃতীয় manual-override
# coordinate পাওয়া গেছে (24.3925, 89.7737, "Bangabandhu/Jamuna Bridge,
# Bhuapur") — grid-search মেগা-ট্রাঙ্ক রেঞ্জে কিছু না পাওয়ায় আগেই
# ম্যানুয়ালি বসানো হয়েছিল। কাকতালীয়ভাবে এটা BWDB-র সঠিক Porabari
# coordinate (24.3011, 89.7970)-এর কাছাকাছি পড়ে গেছে — অর্থাৎ আগের
# manual fix-টা প্রায় সঠিক দিকেই ছিল।
#
# ⚠️ BWDB official database-এ টাঙ্গাইল জেলায় stations.py-র চেয়ে অনেক
# বেশি station registered আছে — Bhuiyanpur (SW343.5, Futikjani),
# Nolsafa (SW342, Futikjani), Jukerchar (SW134, Jhenai), Madhupur
# (SW12, Bangshi), Mirzapur_Bangshi (SW14, Bangshi), Kawaljani (SW13,
# Bangshi), Jugini (SW186, Lohajang), Elashin (SW68A, Dhaleswari)।
# stations.py-তে এর একটাও নেই — বড় coverage gap।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

TANGAIL_PROFILE = {
    "district": "টাঙ্গাইল",
    "district_lat": 24.2513,
    "district_lon": 89.9167,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ২টা — একটা যমুনার উপর (Porabari), একটা
    # বাংশী নদীর উপর (Nayarhat, যদিও ভৌগোলিকভাবে এটা সীমান্ত-পার Dhaka-তে)
    "station_count": 2,

    "stations": [
        {
            "name": "Porabari",
            "ffwc_id": "SW50",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "যমুনা (Jamuna)",
            "upazila": "Tangail Sadar",  # ⚠️ দেখুন verification_note — FFWC/stations.py "Nagarpur" বলছে
            "union": "Porabari",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই যমুনা মূল প্রবাহ, Sirajganj Sadar-এর প্রায় ৩৫ কিমি "
                    "downstream। টাঙ্গাইল জেলার পশ্চিম সীমানা পুরোটাই যমুনা "
                    "দিয়ে ঘেরা (বর্ষায় ৪ মাইলেরও বেশি চওড়া)। Bangabandhu "
                    "Bridge (যমুনা সেতু) এই stretch-এই অবস্থিত, ভূঞাপুর "
                    "উপজেলায়।"
                ),
                "flow_behavior": "একই braided ও migrating চরিত্র, বাকি যমুনা-corridor জেলাগুলোর মতোই।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": 24,  # flood_config.py অনুযায়ী
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 11.80,  # ✅ FFWC verify করা
            "highest_recorded_m": 18.55,
            "verified_source": "old.ffwc.gov.bd (stid=23/66/21), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। ⚠️ কিন্তু উপজেলা নিয়ে conflict — "
                "FFWC live site ও stations.py দুটোতেই 'Upazilla: Nagarpur, "
                "Union: Bhara' লেখা, কিন্তু BWDB-র official hydrology survey "
                "database স্পষ্ট করে বলছে 'Upazila: Tangail Sadar', "
                "coordinate lat=24.3011, lon=89.7970। এটা Wikipedia-র "
                "'Porabari Union' পাতার তথ্যের (Tangail Sadar Upazila, "
                "coordinate 24.227, 89.867)-এর সাথেও সামঞ্জস্যপূর্ণ — "
                "স্টেশনের নাম 'Porabari' নিজেই Tangail Sadar-এর একটা "
                "ইউনিয়নের নাম। stations.py-র বর্তমান coordinate (24.03, "
                "89.87) BWDB-র মান থেকে প্রায় ৩০ কিমি দক্ষিণে ভুল জায়গায় "
                "বসানো ছিল। উল্লেখ্য, flood_config.py-তে আগে থেকেই একটা "
                "manual-override coordinate (24.3925, 89.7737, "
                "'Bangabandhu Bridge, Bhuapur') আছে, যেটা BWDB-র সঠিক "
                "মানের বেশ কাছাকাছি — অর্থাৎ সেই আগের manual fix মোটামুটি "
                "সঠিক দিকেই ছিল, যদিও ভিন্ন উপজেলার (Bhuapur না, আসলে "
                "Tangail Sadar) নাম দেওয়া ছিল।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1180,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ, mean annual ~২০,২০০ m³/s, bankfull ৪৫,০০০-৬০,০০০ m³/s",
                    "source": "Best et al. 2022 (একই নদী, Sirajganj-এর ~৩৫ কিমি downstream)",
                    "cross_check": "✅ river_categories.py-তে টাঙ্গাইল=mega_trunk — সামঞ্জস্যপূর্ণ।",
                    "critical_caveat": "আগের ৪টা জেলার (রাজবাড়ী/মানিকগঞ্জ/জামালপুর/সিরাজগঞ্জ) মতোই একই train_model.py বাগ প্রযোজ্য।",
                },
                "cn": {
                    "old_value": 78,
                    "reviewed_estimate": 89,
                    "reasoning": "একই যমুনা floodplain, একই TR-55 যুক্তি আগের জেলাগুলোর মতো — flood_config.py-র বর্তমান মান (৭৮) অন্য জেলাগুলোর সাথে সামঞ্জস্যপূর্ণ না।",
                    "confidence": "moderate",
                },
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "Bangabandhu Bridge (যমুনা সেতু) এই stretch-এই — জাতীয় "
                        "গুরুত্বপূর্ণ অবকাঠামো ও ঘনবসতিপূর্ণ এলাকা। যমুনার "
                        "অন্যান্য corridor জেলাগুলোর (Sirajganj 'অতি উচ্চ', "
                        "Manikganj/Jamalpur 'উচ্চ') তুলনায় flood_config.py-র "
                        "বর্তমান 'মাঝারি' রেটিং কম মনে হচ্ছে — 'উচ্চ' বেশি "
                        "সামঞ্জস্যপূর্ণ, যদিও Kazipur/Sirajganj-এর মতো তীব্র "
                        "chronic erosion crisis-এর প্রমাণ এই station-এ এখনো "
                        "পাওয়া যায়নি।"
                    ),
                    "source": "Wikipedia (Bhuapur Upazila, Bangabandhu Bridge); অন্য যমুনা-corridor জেলার সাথে cross-comparison",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক riverine বন্যা, বাকি যমুনা-corridor জেলাগুলোর মতোই।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "নাগরপুর, টাঙ্গাইল সদরের চরাঞ্চল",
                "50cm_to_1m_above_danger": "ভূঞাপুর, দেলদুয়ারের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — বিস্তৃত এলাকা প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Nayarhat",
            "ffwc_id": "SW14.5",
            "is_primary": False,

            "river": "বাংশী (Bangshi)",
            "upazila": "Mirzapur (FFWC/stations.py অনুযায়ী) — ⚠️ দেখুন verification_note",
            "union": "Ajgana (FFWC অনুযায়ী)",

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "বাংশী নদী পুরাতন ব্রহ্মপুত্রের একটা শাখা হিসেবে জামালপুরে "
                    "উৎপন্ন হয়ে মধুপুর ট্রাক্ট (শাল বন এলাকা) ঘেঁষে টাঙ্গাইল "
                    "জেলার মাঝ বরাবর বয়ে যায়, তারপর Dhaka জেলার Savar-এ "
                    "ধলেশ্বরীতে গিয়ে মেশে। মোট দৈর্ঘ্য ~২৩৮ কিমি। তুরাগ, "
                    "বুড়িগঙ্গা, কালীগঙ্গা, কর্ণতলী, টঙ্গী — এই সবগুলো "
                    "বাংশীরই distributary।"
                ),
                "flow_behavior": (
                    "বর্ষা ছাড়া প্রায় অচল/non-navigable। দূষণে (DEPZ শিল্প "
                    "বর্জ্য) মারাত্মকভাবে ক্ষতিগ্রস্ত — 'once a lifeline, now "
                    "dying' হিসেবে বর্ণিত হয়েছে সাম্প্রতিক প্রতিবেদনে।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 6.85,  # ✅ FFWC verify করা
            "highest_recorded_m": 9.18,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️⚠️ সবচেয়ে গুরুত্বপূর্ণ finding এই পুরো ৫-জেলা "
                "প্রজেক্টে — FFWC live site ও stations.py দুটোই বলছে এই "
                "station 'District: Tangail, Upazilla: Mirzapur', কিন্তু "
                "BWDB-র official hydrology survey database স্পষ্ট করে বলছে "
                "'District: Dhaka, Upazila: Savar' (coordinate lat=23.9057, "
                "lon=90.2310)। এটা শুধু stations.py-র ভুল না — একটা "
                "independent academic paper-ও (Jahangirnagar University, "
                "Dept. of Environmental Sciences, Savar, Dhaka) নিশ্চিত "
                "করেছে যে 'Nayarhat Bridge' station Savar, Dhaka-তে "
                "অবস্থিত (DEPZ শিল্প-বর্জ্য নিয়ে করা গবেষণায়)। ভূগোলগতভাবেও "
                "এটা সামঞ্জস্যপূর্ণ — বাংশী নদী Tangail-এর Mirzapur দিয়ে "
                "বয়ে গিয়ে Dhaka-র Savar-এ প্রবেশ করে, আর Nayarhat gauge "
                "সেই সীমানা-পারের বিন্দুতে। হিমুর সিদ্ধান্ত অনুযায়ী এটা "
                "এখানে রাখা হলো (upstream Tangail flow-এর signal বহন করে "
                "বলে), কিন্তু এটা কঠোরভাবে 'boundary/downstream' station "
                "হিসেবে treat করা উচিত, খাঁটি Tangail-internal station না।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 685,
                    "corrected_estimate": 300,
                    "corrected_range": (
                        "নির্দিষ্ট প্রকাশিত mean discharge figure পাওয়া "
                        "যায়নি (২০০১-২০১২ সময়কালের flow-duration-curve "
                        "গবেষণা আছে কিন্তু mean discharge সংখ্যা সরাসরি "
                        "উদ্ধৃত করা যায়নি)। নদীর আকার (২৩৮ কিমি দৈর্ঘ্য, "
                        "dry-season-এ প্রায় অচল) বিবেচনায় river_categories.py-র "
                        "'small_or_tidal' রেঞ্জের মাঝামাঝি ধরা হলো।"
                    ),
                    "source": "Flow Characteristics of Bangshi River (ResearchGate, environmental flow assessment study, ২০০১-১২ ডেটা)",
                    "confidence": "low — নির্দিষ্ট discharge সংখ্যা পাওয়া যায়নি, নদীর সাধারণ বিবরণ থেকে অনুমান",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "সমতল floodplain, একই TR-55 যুক্তি", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "নিম্ন-মাঝারি",
                    "reasoning": (
                        "danger_level (6.85m) সবচেয়ে কম এই পুরো ৫-জেলা "
                        "প্রজেক্টে দেখা সবগুলো station-এর মধ্যে, আর নদীটা "
                        "dry-season-এ প্রায় অচল — flood risk তুলনামূলক কম। "
                        "কিন্তু দূষণ/পরিবেশগত ঝুঁকি আলাদা একটা বিষয়, যেটা "
                        "flood risk model-এর scope-এর বাইরে।"
                    ),
                    "source": "Bangshi River Wikipedia; ResearchGate flow study",
                },
            },

            "flood_type": "Riverine (boundary/downstream station — সীমিত প্রাসঙ্গিকতা)",
            "flood_type_note": (
                "⚠️ যেহেতু গেজ পয়েন্টটা সম্ভবত Tangail-এর বাইরে (Dhaka/"
                "Savar), এই station-এর danger_level crossing সরাসরি "
                "Tangail-এর কোনো এলাকা প্লাবিত হওয়া বোঝায় না — বরং টাঙ্গাইল "
                "থেকে বেরিয়ে যাওয়া পানির পরিমাণের একটা proxy signal। "
                "district-level flood alert-এ এটা কীভাবে ব্যবহার করা হবে, "
                "সেটা স্পষ্ট করে সিদ্ধান্ত নেওয়া দরকার — হয় downstream-impact "
                "indicator হিসেবে, নয়তো Tangail-এর সীমার বাইরে থাকা অংশ "
                "হিসেবে বাদ।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — station-টা জেলার বাইরে হওয়ায় Tangail-এর জন্য সরাসরি inundation-band তৈরি করা প্রাসঙ্গিক না"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান station (Porabari/যমুনা)-এর জন্য discharge/water-level "
        "trend primary, soil moisture কমানো — আগের জেলাগুলোর মতোই। "
        "Nayarhat (বাংশী)-এর জন্য যেহেতু এটা essentially একটা "
        "downstream-boundary indicator, স্থানীয় soil moisture বা rainfall "
        "কোনোটারই সরাসরি weight বেশি রাখার justification নেই — বরং এটা "
        "upstream (Tangail-এর ভেতরের) rainfall-এর delayed/aggregated "
        "reflection হিসেবে ব্যবহার করা যুক্তিসঙ্গত।"
    ),

    "confluence_note": (
        "টাঙ্গাইল যোগ হওয়ায় এখন যমুনা করিডোরের পুরো বাংলাদেশ-অংশ "
        "continuous — Bahadurabad (জামালপুর, নাম-পরিবর্তন বিন্দু) → "
        "Kazipur/Sirajganj (সিরাজগঞ্জ) → Porabari (টাঙ্গাইল) → Aricha "
        "(মানিকগঞ্জ, Padma confluence)। ৫টা জেলা মিলিয়ে যমুনার discharge "
        "picture এখন সম্পূর্ণ। এই ৫টা জেলার সবকটাতেই train_model.py-র "
        "একই reference_discharge বাগ আছে — এটাই এখন retrain/override "
        "সিদ্ধান্তের সবচেয়ে গুরুত্বপূর্ণ candidate হওয়া উচিত, কারণ পাঁচটা "
        "জেলা একসাথে সবচেয়ে বড় coherent correction-block তৈরি করছে।"
    ),

    "cross_district_flags": (
        "⚠️ Nayarhat-এর finding সবচেয়ে গুরুত্বপূর্ণ systemic flag এখন "
        "পর্যন্ত — stations.py-তে district-assignment ভুল থাকতে পারে শুধু "
        "coordinate-এ না, বরং পুরো district ফিল্ডেই। এটা অন্য জেলা-সীমান্ত "
        "নদীর station-গুলোতেও (যেমন Dhaleswari, Kaliganga, বা অন্য "
        "distributary নদীর গেজ) থাকতে পারে — future district profile-এ "
        "শুধু coordinate না, পুরো district/upazila assignment-ই BWDB "
        "official সোর্স দিয়ে cross-check করা উচিত, FFWC live site-কে "
        "একা বিশ্বাস না করে।"
    ),
}