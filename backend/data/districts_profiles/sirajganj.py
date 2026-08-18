# ============================================================
# FloodAI — data/district_profiles/sirajganj.py
#
# জেলা-বাই-জেলা framework-এর ৪র্থ জেলা। রাজবাড়ী/মানিকগঞ্জ/জামালপুরের
# সাথে হুবহু একই ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ জামালপুর প্রোফাইলের confluence_note অনুযায়ী এই জেলা যমুনা করিডোরের
# মাঝামাঝি অংশ (Bahadurabad থেকে Aricha-র মাঝে) — এটা যুক্ত হলে
# জামালপুর → সিরাজগঞ্জ → মানিকগঞ্জ পুরো যমুনা করিডোরের discharge picture
# সম্পূর্ণ হবে।
#
# ⚠️ Coordinate verification-এ যা পাওয়া গেছে:
#   1. Kazipur — coordinate ~১৪ কিমি ভুল জায়গায় বসানো ছিল
#   2. Sirajganj Sadar — coordinate মোটামুটি ঠিক ছিল (~২ কিমি off, নগণ্য)
#   3. Baghabari — coordinate ~৯ কিমি off ছিল
#   danger_level তিনটাতেই ঠিক ছিল (14.80 / 12.90 / 9.95)।
#
# ⚠️ BWDB-র official hydrology database-এ সিরাজগঞ্জ জেলায় stations.py-র
# চেয়ে বেশি station registered আছে — Nalkasengati (SW11.5, বাঙালি নদী,
# Raiganj), Ullapara_Rly_Crossing (SW66, করতোয়া সিস্টেম), Nangoora Bridge
# (SW313, Nangoora নদী)। এই ৩টা stations.py-তে নেই — coverage gap, future
# session-এ যোগ করার কথা ভাবা যেতে পারে।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SIRAJGANJ_PROFILE = {
    "district": "সিরাজগঞ্জ",
    "district_lat": 24.4534,
    "district_lon": 89.7010,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ৩টা station — দুইটা মূল যমুনার উপর (Kazipur,
    # Sirajganj Sadar), একটা সম্পূর্ণ ভিন্ন নদী-সিস্টেমের (Baghabari,
    # উত্তর-পশ্চিম বাংলাদেশের সম্মিলিত নিষ্কাশন ব্যবস্থার আউটলেট)।
    "station_count": 3,

    "stations": [
        {
            "name": "Serajganj",
            "ffwc_id": "SW49",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "যমুনা (Jamuna)",
            "upazila": "Sirajganj Sadar",
            "union": "Paurashava",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই যমুনা মূল প্রবাহ, Bahadurabad থেকে ~৯০ কিমি downstream। "
                    "সিরাজগঞ্জ শহর যমুনার ডান তীরে অবস্থিত, ঐতিহাসিকভাবে উত্তরবঙ্গের "
                    "পাটের প্রধান বাণিজ্যকেন্দ্র ছিল (জুট প্রেস, স্টিমার যোগাযোগ)।"
                ),
                "flow_behavior": (
                    "চরম braided ও migrating। যমুনা সেতুর কাছে (উজানে) নদী "
                    "নাটকীয়ভাবে সংকুচিত হয়ে বালুচরে পরিণত হয়েছে (২০২৬ সালের "
                    "একটা রিপোর্ট অনুযায়ী — 'China Bandh'-এর পাশে বিশাল চর "
                    "জেগে উঠেছে, যেখানে একসময় নদী ছিল), অথচ একই সময়ে "
                    "সিরাজগঞ্জ সদর ও কাজীপুরে তীব্র ভাঙন চলছে। এই দুই বিপরীত "
                    "ঘটনা (upstream-এ char জমা, downstream-এ ভাঙন) দেখায় "
                    "channel avulsion কতটা দ্রুত ও অনির্দেশ্য এই stretch-এ।"
                ),
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 12.90,  # ✅ FFWC verify করা
            "highest_recorded_m": 14.70,
            "verified_source": "old.ffwc.gov.bd (stid=23), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে stations.py-তে। coordinate মোটামুটি "
                "সঠিক — stations.py-তে lat=24.45, lon=89.72, BWDB official "
                "hydrology survey অনুযায়ী lat=24.4685, lon=89.7196 — পার্থক্য "
                "মাত্র ~২ কিমি, নগণ্য।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1290,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": (
                        "একই যমুনা মূল প্রবাহ (Bahadurabad-এর মতো), mean annual "
                        "~২০,২০০ m³/s, bankfull ৪৫,০০০-৬০,০০০ m³/s, রেকর্ড পিক "
                        "১,০২,৫০০ m³/s (১৯৯৮)।"
                    ),
                    "source": "Best et al. 2022 (একই নদী, Bahadurabad-এর ~৯০ কিমি downstream)",
                    "cross_check": "✅ river_categories.py-তে সিরাজগঞ্জ=mega_trunk (10,000-200,000 m³/s) — জামালপুরের সাথে সামঞ্জস্যপূর্ণ।",
                    "critical_caveat": (
                        "রাজবাড়ী/মানিকগঞ্জ/জামালপুরের মতোই একই train_model.py "
                        "বাগ প্রযোজ্য — যমুনার সবগুলো reference point (Aricha, "
                        "Bahadurabad, Jagannathganj, Kazipur, Sirajganj) একসাথে "
                        "consistent হতে হবে retrain/override-এর সময়।"
                    ),
                },
                "cn": {
                    "old_value": None,
                    "reviewed_estimate": 89,
                    "reasoning": "একই যমুনা floodplain, একই TR-55 যুক্তি আগের জেলাগুলোর মতো",
                    "confidence": "moderate",
                },
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": (
                        "'Sirajganj Hard Point' (১৯৯৫-৯৯ সালে ৩৩১ কোটি টাকা "
                        "খরচে নির্মিত, শহর রক্ষার জন্য) বারবার (২০০৯, ২০১০, "
                        "২০১১ ও সাম্প্রতিককালেও) ব্যর্থ হয়েছে — thalweg shift ও "
                        "island গঠনের কারণে। শহর-রক্ষা বাঁধেই বারবার ভাঙন ধরেছে "
                        "(জেলখানা এলাকা)। যমুনার গড় ভাঙনের হার বছরে ১০০ মিটার, "
                        "চরম ক্ষেত্রে ১০০০ মিটার পর্যন্ত — এবং এটা 'সবচেয়ে "
                        "ভাঙনপ্রবণ নদী বাংলাদেশে' হিসেবে চিহ্নিত। danger_level "
                        "(12.90m) নিজে কম হলেও, ভাঙন ও infrastructure-ঝুঁকির "
                        "দিক থেকে এটা 'অতি উচ্চ' হওয়া উচিত।"
                    ),
                    "source": (
                        "'Flow Path at Sirajganj Hard Point' (academic paper, "
                        "river training works failure বিশ্লেষণ); The Daily "
                        "Star (embankment erosion রিপোর্ট, একাধিক বছর)"
                    ),
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক riverine বন্যা, তবে erosion risk flood risk-এর চেয়েও বেশি প্রকট এই station-এ।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "সিরাজগঞ্জ সদরের চরাঞ্চল ও নদী-তীরবর্তী নিম্নাঞ্চল (কাওয়াকোলা চর, পূর্ব বাহুকা)",
                "50cm_to_1m_above_danger": "শহর রক্ষা বাঁধের বাইরের এলাকা",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — উল্লাপাড়া, বেলকুচি, শাহজাদপুর পর্যন্ত বিস্তৃত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Kazipur",
            "ffwc_id": "SW49A",
            "is_primary": False,

            "river": "যমুনা (Jamuna)",
            "upazila": "Kazipur",
            "union": "Tekani",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "একই যমুনা মূল প্রবাহ, Sirajganj Sadar-এর সামান্য উজানে।",
                "flow_behavior": "একই braided ও migrating চরিত্র, তবে erosion rate এই জেলার মধ্যে সবচেয়ে বেশি।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 14.80,  # ✅ FFWC verify করা
            "highest_recorded_m": 16.59,
            "verified_source": "old.ffwc.gov.bd (stid=66/21), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️ coordinate ভুল ছিল — stations.py-তে lat=24.60, "
                "lon=89.72, কিন্তু BWDB official অনুযায়ী সঠিক coordinate "
                "lat=24.6698, lon=89.6491 — প্রায় ১৪ কিমি পশ্চিমে সরাতে হবে। "
                "Wikipedia-র Kazipur উপজেলা কেন্দ্র coordinate (24.6417, "
                "89.650)-ও BWDB-র মানের কাছাকাছি, যা এই correction-কে সমর্থন করে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1480,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ, Sirajganj-এর মতোই রেঞ্জ",
                    "source": "Best et al. 2022 (একই নদী)",
                    "confidence": "moderate — extrapolated from Bahadurabad",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই যমুনা floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": (
                        "জেলার মধ্যে সবচেয়ে গুরুতর ও সাম্প্রতিক (২০২৫-২০২৬) "
                        "ভাঙনের ঘটনা এখানেই — Char Girish, Khash Rajbari, "
                        "Chargirish ইউনিয়নে শুধু গত কয়েক সপ্তাহেই ৩০০+ ঘরবাড়ি "
                        "নদীগর্ভে বিলীন, ১৬টা গ্রাম প্রভাবিত (Daily Star, "
                        "সেপ্টেম্বর ২০২৫ ও জুলাই ২০২৬ রিপোর্ট)। স্থানীয়রা "
                        "ক্ষয়প্রবণ ৬টা ইউনিয়ন নিয়ে আলাদা 'যমুনা উপজেলা' গঠনের "
                        "দাবি জানিয়েছে — সমস্যার তীব্রতা বোঝায়। এটা flood "
                        "risk-এর চেয়েও essentially একটা chronic erosion "
                        "crisis, কিন্তু danger_level-based flood model এই "
                        "মাত্রা capture করে না।"
                    ),
                    "source": "The Daily Star (একাধিক রিপোর্ট, ২০২৫-২০২৬), TBS News (জুলাই ২০২৬)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ গুরুত্বপূর্ণ nuance — এই station-এ 'flood' এর চেয়ে "
                "'erosion' মূল সমস্যা। danger_level cross হওয়ার আগেই ভাঙন "
                "শুরু হয়ে যায় rising water level-এর সাথে। বর্তমান FloodAI "
                "মডেল শুধু danger_level-ভিত্তিক হওয়ায় এই erosion-dominant "
                "ঝুঁকি হয়তো underrepresent হচ্ছে।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — erosion dynamics এর কারণে সাধারণ inundation-band পদ্ধতি এখানে কম প্রাসঙ্গিক, আলাদা চিন্তা দরকার"},
        },
        {
            "name": "Baghabari",
            "ffwc_id": "SW151",
            "is_primary": False,

            "river": "হুড়াসাগর (Hurasagar, Karatoya-Atrai-Gur-Gumani-Hurasagar সিস্টেমের আউটলেট)",
            "upazila": "Shahjadpur",
            "union": "Potajia",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "সম্পূর্ণ ভিন্ন চরিত্রের নদী — এটা যমুনার সরাসরি অংশ না, বরং "
                    "উত্তর-পশ্চিম বাংলাদেশের প্রায় পুরো অভ্যন্তরীণ নিষ্কাশন "
                    "ব্যবস্থার (করতোয়া, আত্রাই, বড়াল, গুড়, গুমানী, বাঙালি) "
                    "সম্মিলিত আউটলেট, যা চলনবিল হয়ে হুড়াসাগর নামে যমুনায় "
                    "গিয়ে পড়ে। FFWC-র নিজস্ব annual flood report অনুযায়ী "
                    "হুড়াসাগর 'উত্তর-পশ্চিম বাংলাদেশের অভ্যন্তরীণ নিষ্কাশনের "
                    "আউটলেট' হিসেবে স্পষ্টভাবে চিহ্নিত।"
                ),
                "flow_behavior": (
                    "তিস্তা/ধরলা/দুধকুমারের মতো flashy পাহাড়ি নদী না — বরং ধীর, "
                    "সমতলভূমির নিষ্কাশন-নির্ভর প্রবাহ, চলনবিলের বিশাল জলাভূমি "
                    "(৫০+ নদী/খাল মিলিত) দিয়ে buffered। তবে সাম্প্রতিক খবর "
                    "অনুযায়ী (Rabindra University campus বিতর্ক, ২০২৫) এই "
                    "প্রাকৃতিক নিষ্কাশন পথে বাধা তৈরি হলে আশপাশের এলাকায় "
                    "জলাবদ্ধতা/বন্যা বাড়ার আশঙ্কা বিশেষজ্ঞরা করছেন — অর্থাৎ "
                    "flow capacity এখনই কিছুটা ঝুঁকিতে।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 9.95,  # ✅ FFWC verify করা
            "highest_recorded_m": 11.80,
            "verified_source": "old.ffwc.gov.bd (stid=23/66/21/46), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে stations.py-তে। ⚠️ coordinate off "
                "ছিল — stations.py-তে lat=24.20, lon=89.55, BWDB official "
                "অনুযায়ী সঠিক coordinate lat=24.1312, lon=89.5813 — প্রায় "
                "৯ কিমি দূরে। Wikipedia-র Baghabari গ্রামের coordinate "
                "(24.1361, 89.5856)-ও BWDB-র মানের সাথে ভালোভাবে মেলে, যা "
                "correction-কে সমর্থন করে। FFWC-র ২০১৯ ও ২০২১ সালের annual "
                "flood report-এও 'Atrai at Baghabari' নামে hydrograph "
                "উল্লেখ আছে (২০২১-এ ২১ দিন danger level-এর উপরে ছিল) — "
                "এই station জাতীয় flood-monitoring-এ নিয়মিত track করা হয়।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 995,
                    "corrected_estimate": 1500,
                    "corrected_range": (
                        "নির্দিষ্ট measured discharge figure পাওয়া যায়নি, কিন্তু "
                        "এটা একাধিক মাঝারি নদীর (করতোয়া, আত্রাই, বড়াল, গুড়, "
                        "গুমানী, বাঙালি) সম্মিলিত প্রবাহ হওয়ায় river_categories.py-র "
                        "'medium' রেঞ্জের (20-8000 m³/s) উপরের দিকে ধরা "
                        "যুক্তিসঙ্গত — একক মাঝারি নদীর চেয়ে বেশি, কিন্তু "
                        "mega_trunk-এর ধারেকাছেও না।"
                    ),
                    "source": "Banglapedia (Hurasagar River, Karatoya River); FFWC Annual Flood Report 2019/2021 (hydrograph reference, সংখ্যা উল্লেখ ছাড়া)",
                    "confidence": "low-moderate — combined multi-river outlet হওয়ায় single-river discharge estimate কঠিন, dedicated BWDB gauge data ভালো হবে",
                },
                "cn": {
                    "old_value": None,
                    "reviewed_estimate": 85,
                    "reasoning": "চলনবিল wetland buffer থাকায় সরাসরি floodplain-এর মতো CN নয় — কিছুটা কম রাখা হলো (85) অন্য station-গুলোর তুলনায় (89), কারণ বিলের স্টোরেজ ক্যাপাসিটি রান-অফ কিছুটা শোষণ করে।",
                    "confidence": "low-moderate",
                },
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": (
                        "চলনবিল বাফার থাকায় আকস্মিক flood risk কম, কিন্তু "
                        "২০২১-এ ২১ দিন danger level-এর উপরে ছিল বলে একেবারে "
                        "নগণ্যও না। upstream construction (যেমন প্রস্তাবিত "
                        "Rabindra University campus চলনবিলের নিষ্কাশন-পথে) "
                        "ভবিষ্যতে ঝুঁকি বাড়াতে পারে — এটা একটা emerging risk "
                        "factor, historical data-তে এখনো প্রতিফলিত হয়নি।"
                    ),
                    "source": "FFWC Annual Flood Report 2021; Prothom Alo (Rabindra University চলনবিল বিতর্ক, ২০২৫)",
                },
            },

            "flood_type": "Riverine (drainage-outlet type — ভিন্ন প্রকৃতির)",
            "flood_type_note": (
                "⚠️ এই station-এর flood behavior বাকি দুইটা (যমুনা মূল "
                "প্রবাহ) থেকে fundamentally আলাদা — এটা upstream rainfall "
                "runoff-নির্ভর নিষ্কাশন সমস্যা, glacier/Himalaya-fed trunk "
                "river surge না। district-level flood_type নির্ধারণে "
                "primary station (Sirajganj/Jamuna) দেখে সিদ্ধান্ত নিলে এই "
                "ভিন্নতা হারিয়ে যাবে।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — চলনবিল wetland dynamics-এর কারণে সাধারণ river inundation model এখানে সরাসরি প্রযোজ্য না-ও হতে পারে"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান দুইটা station (Sirajganj Sadar, Kazipur — যমুনা মূল "
        "প্রবাহ)-এর জন্য discharge/water-level trend primary, soil "
        "moisture কমানো যুক্তিসঙ্গত — আগের জেলাগুলোর মতোই। কিন্তু Baghabari "
        "(হুড়াসাগর) সম্পূর্ণ ভিন্ন — এটা upstream rainfall-runoff-নির্ভর "
        "combined drainage outlet, তাই এখানে local_rain ও upstream "
        "catchment rainfall (শুধু জামালপুর/সিরাজগঞ্জের না, বরং দিনাজপুর/"
        "রংপুর/বগুড়া/নাটোর পর্যন্ত বিস্তৃত এলাকার) weight বেশি রাখা উচিত, "
        "soil moisture কমালেও rainfall কমানো ঠিক হবে না — ঠিক মানিকগঞ্জের "
        "Jagir/Taraghat বা জামালপুরের Goalkanda-র মতো যুক্তি।"
    ),

    "confluence_note": (
        "সিরাজগঞ্জ যমুনা করিডোরের মাঝামাঝি বিন্দু — জামালপুর (Bahadurabad, "
        "উজানে, নাম-পরিবর্তন বিন্দু) ও মানিকগঞ্জ (Aricha, downstream, "
        "Padma confluence-এর কাছে) এর মাঝে। এই তিন জেলা মিলিয়ে এখন যমুনার "
        "পুরো বাংলাদেশ-অংশের discharge picture (Bahadurabad → Kazipur/"
        "Sirajganj → Aricha) প্রায় সম্পূর্ণ — বাকি শুধু Tangail (Porabari, "
        "SW50) যোগ করলে করিডোরটা fully continuous হয়ে যাবে।"
    ),

    "cross_district_flags": (
        "⚠️ Kazipur station-এ যে erosion-vs-flood distinction পাওয়া গেছে, "
        "সেটা সম্ভবত যমুনার অন্য erosion-prone জেলাগুলোতেও (Bogura, "
        "Tangail, Gaibandha) প্রাসঙ্গিক — flood_type='Riverine' ট্যাগ "
        "দেওয়ার সময় pure water-level-crossing বনাম bank-erosion-driven "
        "ক্ষতির পার্থক্য মডেলে ধরা পড়ছে কিনা, সেটা বড় আকারে review করার "
        "দরকার হতে পারে।"
    ),
}