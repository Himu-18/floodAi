# ============================================================
# FloodAI — data/district_profiles/jamalpur.py
#
# জেলা-বাই-জেলা framework-এর ৩য় জেলা। রাজবাড়ী/মানিকগঞ্জের সাথে হুবহু
# একই ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ এই জেলার জন্য coordinate verification-এ stations.py-তে বেশ কিছু
# গুরুত্বপূর্ণ ভুল/অসঙ্গতি পাওয়া গেছে — নিচে প্রতিটা station-এ আলাদা করে
# note করা আছে। সংক্ষেপে:
#   1. Jagannathganj — coordinate ~২৩ কিমি ভুল জায়গায় বসানো ছিল
#   2. Goalkanda — FFWC live site নিজেই এই station-কে ভুল ID (SW327)
#      দিয়েছে, যেটা আসলে Kurigram-এর Boalmari station-এর ID। BWDB-র
#      official hydrology survey database অনুযায়ী Goalkanda-র আসল ID
#      হলো SW223। coordinate-ও ~২৮ কিমি off ছিল।
#   3. Char-Rajibpur — FFWC এটাকে "District: Jamalpur" বলছে, কিন্তু
#      বাস্তবে "Char Rajibpur Upazila" নিজেই এখন প্রশাসনিকভাবে Kurigram
#      জেলার অংশ (১৯৮৩ থেকে পৃথক)। exact coordinate BWDB-র official
#      survey database-এও পাওয়া যায়নি — এখনো unverified/approximate।
#   4. flood_config.py-তে বর্তমানে ৪টা river আছে জামালপুরের জন্য, কিন্তু
#      stations.py-তে ৫টা station আছে — Jagannathganj flood_config.py-র
#      rivers list-এ ঢোকানোই হয়নি। এটা wire করার সময় ঠিক করতে হবে।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

JAMALPUR_PROFILE = {
    "district": "জামালপুর",
    "district_lat": 24.9375,
    "district_lon": 89.9376,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # ৫টা station — রাজবাড়ী (১টা), মানিকগঞ্জ (৩টা)-এর চেয়েও জটিল।
    # মূল কারণ: জামালপুর সেই জায়গা যেখানে ব্রহ্মপুত্র "যমুনা" নামে পরিচিত
    # হতে শুরু করে (Bahadurabad-এ, Dewanganj উপজেলা) — অর্থাৎ এই জেলা
    # বাংলাদেশের সবচেয়ে বড় নদীর নাম-পরিবর্তনের বিন্দু।
    "station_count": 5,

    "stations": [
        {
            "name": "Bahadurabad (Bahadurabad_Transit)",
            "ffwc_id": "SW46.9L",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "যমুনা (Jamuna/Brahmaputra)",
            "upazila": "Islampur",
            "union": "Belgachha",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "এইটাই বাংলাদেশের সবচেয়ে গুরুত্বপূর্ণ discharge-measurement "
                    "point — ব্রহ্মপুত্রের পুরো catchment (~৫,৮০,০০০-৬,৫০,০০০ "
                    "বর্গকিমি, তিব্বত+ভারত+ভুটান+বাংলাদেশ) এখানে এসে মেশে। "
                    "Bahadurabad-এর ঠিক উজানেই (Dewanganj উপজেলা) নদীটা "
                    "'ব্রহ্মপুত্র' নাম ছেড়ে 'যমুনা' নাম নেয় — ১৭৮৭ সালের ভূমিকম্প/"
                    "বন্যার পর মূল প্রবাহ এই নতুন পথে সরে যাওয়ার কারণে।"
                ),
                "flow_behavior": (
                    "অত্যন্ত braided, migrating channel। বিশ্বের saদ্যতম বৃহৎ "
                    "braided নদীগুলোর একটা। বছরে water stage-এর তারতম্য ~৬ মিটার।"
                ),
                "upstream_reference": "Guwahati, IN",  # flood_config.py অনুযায়ী
                "lag_time_hours": 20,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 19.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 20.63,
            "verified_source": "old.ffwc.gov.bd (stid=66), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে flood_config.py-তে। কিন্তু ⚠️ coordinate "
                "নিয়ে সমস্যা আছে — stations.py-তে lat=25.14, lon=89.60 আছে, "
                "কিন্তু BWDB-র official hydrology survey database "
                "(water_level_data_available_print.php) অনুযায়ী "
                "Bahadurabad_Transit (SW46.9L)-এর সঠিক coordinate হলো "
                "lat=25.1303, lon=89.7346 — অর্থাৎ lon প্রায় ১৩ কিমি পূর্বে "
                "সরাতে হবে। এছাড়া flood_config.py-র primary river_lat/lon "
                "(25.29, 89.6)-ও stations.py-র সাথে মেলে না — তিন জায়গায় "
                "তিন রকম coordinate (flood_config.py, stations.py, BWDB "
                "official) — এই তিনটার মধ্যে BWDB-র official survey ডেটাই "
                "সবচেয়ে নির্ভরযোগ্য বলে ধরা উচিত। উল্লেখ্য, একটা পুরনো "
                "discontinued gauge (SW47, একই নাম 'Bahadurabad', ১৯৬২-৮৫ "
                "সাল পর্যন্ত সক্রিয় ছিল) lat=25.1106/lon=89.6800-এ ছিল — "
                "stations.py-র coordinate সম্ভবত ভুলবশত এই পুরনো "
                "discontinued gauge-এর কাছাকাছি বসানো হয়েছিল, বর্তমান "
                "সক্রিয় Transit station-এর না।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1905,       # danger_level(19.05)*100
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": (
                        "mean annual ২০,২০০ m³/s (Best et al. 2022, ৩৫-বছর গড় "
                        "maximum discharge ৬৭,৪৩৫ m³/s), bankfull ৪৫,০০০-৬০,০০০ "
                        "m³/s, dry-season minimum ~২,৮৬০ m³/s, রেকর্ড পিক "
                        "১,০২,৫০০ m³/s (১৯৯৮)। Period-ভেদে গড় ২১,৩১৯-২৪,০২৭ "
                        "m³/s (Wikipedia/BWDB compiled)।"
                    ),
                    "source": (
                        "Best et al. 2022 (Jamuna-Brahmaputra River chapter); "
                        "Banglapedia Jamuna River; Aktar 2013 (erosion study, "
                        "৩৫-বছর গড়)"
                    ),
                    "cross_check": (
                        "✅ river_categories.py-তে জামালপুর=mega_trunk (10,000-"
                        "200,000 m³/s রেঞ্জ) — ২০,২০০ estimate এই রেঞ্জের মধ্যেই। "
                        "রাজবাড়ী (৩০,০০০-৭৫,০০০) ও মানিকগঞ্জ (৫০,০০০)-এর সাথে "
                        "তুলনা করলে Bahadurabad-এর mean annual figure কম মনে "
                        "হতে পারে, কিন্তু এটা 'mean annual' vs আগের দুইটার "
                        "'মৌসুমি গড়' — একই metric না, তাই সরাসরি তুলনীয় না। "
                        "bankfull রেঞ্জ (৪৫,০০০-৬০,০০০) তিনটা জেলাতেই প্রায় একই।"
                    ),
                    "critical_caveat": (
                        "রাজবাড়ী+মানিকগঞ্জের মতোই — train_model.py-র synthetic "
                        "data একই danger_level*100 সূত্র দিয়ে বানানো। এই তিনটা "
                        "জেলা (রাজবাড়ী, মানিকগঞ্জ, জামালপুর) একসাথে শেষ হলে "
                        "retrain/override সিদ্ধান্ত নেওয়া দরকার — Jamuna নদীর "
                        "একাধিক reference point (Aricha, Bahadurabad, "
                        "Jagannathganj) একই নদী হলেও আলাদা station, তাই সবগুলোই "
                        "consistent হওয়া উচিত।"
                    ),
                },
                "cn": {
                    "old_value": 81,
                    "reviewed_estimate": 89,
                    "reasoning": (
                        "রাজবাড়ী/মানিকগঞ্জের মতোই যুক্তি — Bangladesh floodplain "
                        "paddy/silty-clay soil, HSG C/D, poor hydrologic "
                        "condition অনুযায়ী CN≈৮৮-৯১ (TR-55)। বর্তমান "
                        "flood_config.py-র মান (৮১) সম্ভবত অন্য কোনো generic "
                        "অনুমান থেকে এসেছে, রাজবাড়ী/মানিকগঞ্জের সাথে সামঞ্জস্যপূর্ণ না।"
                    ),
                    "confidence": "moderate — literature-based, স্থানীয় soil-survey verify করা ভালো",
                },
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (borderline অতি উচ্চ)",
                    "reasoning": (
                        "Bahadurabad হলো বাংলাদেশের জাতীয় flood-forecasting "
                        "ব্যবস্থার সবচেয়ে গুরুত্বপূর্ণ reference gauge — ১৯৮৮ ও "
                        "১৯৯৮ উভয় বন্যাতেই এখানকার রিডিং জাতীয় সিদ্ধান্তের "
                        "ভিত্তি ছিল। Islampur উপজেলা প্রতি বছর কমবেশি প্লাবিত হয়, "
                        "বিশেষ করে চর এলাকাগুলো। 'উচ্চ' যুক্তিসঙ্গত মনে হচ্ছে, "
                        "তবে reference-gauge status ও প্রতি-বছরের নিয়মিত "
                        "প্লাবনের কারণে 'অতি উচ্চ'-ও justify করা যায় — সিদ্ধান্তটা "
                        "তোমার judgment call।"
                    ),
                    "source": (
                        "Best et al. 2022 (Jamuna chapter, Bahadurabad reference "
                        "gauge status); Banglapedia; Old Brahmaputra/Jamuna "
                        "Wikipedia flood history"
                    ),
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "ক্লাসিক riverine বন্যা, জুলাই-সেপ্টেম্বর পিক। এই station জাতীয় "
                "flood-forecasting model-এর backbone — FFWC-র মূল forecast "
                "এখান থেকেই derive হয়।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "ইসলামপুর উপজেলার চরাঞ্চল ও নদী-তীরবর্তী নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "দেওয়ানগঞ্জ, ইসলামপুর সদরের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — জামালপুর জেলার বিস্তীর্ণ অংশ, বিশেষত চর এলাকা সম্পূর্ণ নিমজ্জিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি (রাজবাড়ী/মানিকগঞ্জের মতোই সীমাবদ্ধতা)",
            },
        },
        {
            "name": "Char-Rajibpur",
            "ffwc_id": "SW44.5",
            "is_primary": False,

            "river": "ব্রহ্মপুত্র (Brahmaputra)",
            "upazila": None,  # FFWC নিজেই ফাঁকা রেখেছে
            "union": None,

            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই ব্রহ্মপুত্র নদী, Bahadurabad-এর সামান্য উজানে — "
                    "অর্থাৎ যেখানে নদীটা এখনো 'ব্রহ্মপুত্র' নামে পরিচিত, "
                    "'যমুনা' নাম পাওয়ার আগে। Kurigram-এর Chilmari/Noonkhawa "
                    "station থেকে নেমে আসা একই মূল প্রবাহ।"
                ),
                "flow_behavior": "Bahadurabad-এর মতোই braided ও অস্থির, চর-ভাঙন খুব বেশি এই এলাকায়।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 23.50,  # ✅ FFWC verify করা
            "highest_recorded_m": None,  # FFWC live-এ ফাঁকা ছিল
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️ দুইটা গুরুত্বপূর্ণ সীমাবদ্ধতা: "
                "(১) প্রশাসনিক দ্বন্দ্ব — FFWC এই station-কে 'District: "
                "Jamalpur' বলছে, কিন্তু বাস্তবে 'Char Rajibpur Upazila' নিজেই "
                "এখন প্রশাসনিকভাবে Kurigram জেলার অংশ (১৯৮৩ সাল থেকে পৃথক "
                "উপজেলা, Rangpur বিভাগ) — সম্ভবত FFWC পুরনো administrative "
                "label ব্যবহার করছে অথবা গেজ পয়েন্টটা প্রকৃতপক্ষে জামালপুরের "
                "সীমানার মধ্যেই (upazila বাউন্ডারি ও district বাউন্ডারি এক না)। "
                "(২) coordinate — BWDB-র official hydrology survey "
                "database-এ SW44.5 খুঁজে পাওয়া যায়নি (হয়তো তুলনামূলক নতুন "
                "station, ঐ survey list-এ অন্তর্ভুক্ত হয়নি)। stations.py-র "
                "(lat=25.53, lon=89.72) coordinate তাই এখনো unverified — "
                "Char Rajibpur উপজেলার কেন্দ্রের coordinate (Wikipedia "
                "অনুযায়ী 25.40, 89.69) থেকে কাছাকাছি মনে হলেও, exact gauge "
                "location আলাদাভাবে verify করা দরকার।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2350,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": (
                        "একই ব্রহ্মপুত্র-যমুনা মূল প্রবাহ, তাই Bahadurabad-এর "
                        "সাথে একই রেঞ্জ ধরা যৌক্তিক (mean annual ~২০,২০০, "
                        "bankfull ৪৫,০০০-৬০,০০০ m³/s) — মাঝে কোনো বড় "
                        "tributary confluence নেই যা discharge উল্লেখযোগ্যভাবে বদলে দেবে।"
                    ),
                    "source": "Best et al. 2022 (একই reference, geographic proximity-ভিত্তিক)",
                    "confidence": "moderate — সরাসরি এই station-এর জন্য measured data পাওয়া যায়নি, Bahadurabad থেকে extrapolate করা",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই ব্রহ্মপুত্র-যমুনা floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": (
                        "চর এলাকা — নদীর মাঝখানের নিচু, অস্থায়ী ভূমি। সামান্য "
                        "পানি বাড়লেও দ্রুত ও ব্যাপকভাবে প্লাবিত হয়, এবং প্রতি "
                        "বছর ভাঙনের ঝুঁকিতে থাকে। danger_level (23.50m) নিজেই "
                        "জেলার সব station-এর মধ্যে সর্বোচ্চ — উজানের দিকে হওয়ায় "
                        "bed elevation বেশি।"
                    ),
                },
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — char এলাকা হওয়ায় সম্পূর্ণ ভিন্ন inundation dynamics (frequent shifting), বিশেষ মনোযোগ দরকার"},
        },
        {
            "name": "Goalkanda",
            "ffwc_id": "SW327 (FFWC live site অনুযায়ী) / SW223 (BWDB official survey অনুযায়ী — দেখুন verification_note)",
            "is_primary": False,

            "river": "নীল জিঞ্জিরাম (Nil Jinjiram)",
            "upazila": "Dewanganj",  # BWDB official অনুযায়ী
            "union": None,

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "আসামের মেঘালয় পাহাড় থেকে উৎপন্ন, Kurigram-এর Rowmari "
                    "উপজেলা দিয়ে বাংলাদেশে প্রবেশ করে, তারপর Dewanganj "
                    "(জামালপুর)-এ পুরাতন ব্রহ্মপুত্রের সাথে মিশে। বাংলাদেশ "
                    "অংশে দৈর্ঘ্য মাত্র ৫৫ কিমি, গড় প্রস্থ ১০৭ মিটার, গড় গভীরতা "
                    "৭ মিটার, basin area মাত্র ২৪০ বর্গকিমি — এটা river_categories.py-র "
                    "'medium' রেঞ্জেরও নিচে, 'small_or_tidal' category-তেই বসে।"
                ),
                "flow_behavior": (
                    "'A River Dies in Kurigram' (Daily Star, 2019) অনুযায়ী "
                    "নদীটা siltation ও অবৈধ বালু-উত্তোলনে ভুগছে — depth কমে "
                    "যাওয়ায় মেঘালয়ের flash flood ধারণ করতে পারছে না, ফলে "
                    "unregulated overflow/erosion বাড়ছে।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 21.50,  # ✅ FFWC verify করা (দুই ID-তেই একই মান)
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd + BWDB hydrology official database, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️ গুরুত্বপূর্ণ ID conflict পাওয়া গেছে — FFWC-র live public "
                "site (old.ffwc.gov.bd) Goalkanda-কে ID 'SW327' দিয়েছে, "
                "কিন্তু এই একই ID তাদের নিজের ডেটাতেই Kurigram-এর Boalmari "
                "station-কেও দেওয়া আছে (দুইটা সম্পূর্ণ ভিন্ন station, একই ID — "
                "FFWC-র নিজের ডেটা-এন্ট্রি ভুল)। BWDB-র official hydrology "
                "survey database (water_level_data_available_print.php) "
                "অনুযায়ী Goalkanda-র প্রকৃত station ID হলো 'SW223', অবস্থান "
                "Dewanganj উপজেলা, coordinate lat=25.3652, lon=89.8095। "
                "danger_level (21.50m) দুই সোর্সেই মিলে যাওয়ায় এটা নিশ্চিত যে "
                "এটা একই (জামালপুরের) Goalkanda station, শুধু ID-টাই FFWC "
                "live site-এ ভুল বসানো। stations.py-র বর্তমান coordinate "
                "(lat=25.60, lon=89.90) BWDB-র সঠিক মান থেকে প্রায় ২৮ কিমি দূরে — "
                "ঠিক করা দরকার।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2150,
                    "corrected_estimate": 400,
                    "corrected_range": (
                        "নির্দিষ্ট measured discharge পাওয়া যায়নি, কিন্তু নদীর "
                        "আকার (প্রস্থ ১০৭মি, গভীরতা ৭মি, basin ২৪০ বর্গকিমি) "
                        "থেকে river_categories.py-র 'small_or_tidal' রেঞ্জের "
                        "(2-1000 m³/s) মাঝামাঝি-উপরের দিকে ধরা হলো — মৌসুমে "
                        "flash-flood আকারে বেশি হতে পারে।"
                    ),
                    "source": "The Daily Star, 'A River Dies in Kurigram' (2019) — নদীর geometric তথ্য",
                    "confidence": "low — dedicated BWDB discharge gauge data দরকার, এখানে geometry থেকে অনুমান করা",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "ব্রহ্মপুত্র floodplain-এর অংশ কিন্তু siltation-প্রবণ", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি-উচ্চ",
                    "reasoning": (
                        "ছোট নদী হলেও siltation-এর কারণে ধারণ ক্ষমতা কমে যাওয়ায় "
                        "flash-flood ধরনের আকস্মিক প্লাবনের ঝুঁকি বেড়েছে — এটা "
                        "'ছোট নদী = কম ঝুঁকি' এই সরল ধারণাকে challenge করে। "
                        "Kurigram+জামালপুর দুই জেলার শত শত গ্রাম এতে প্রভাবিত।"
                    ),
                    "source": "The Daily Star (2019)",
                },
            },

            "flood_type": "Flash Flood (secondary/local)",
            "flood_type_note": (
                "⚠️ এইটা লক্ষণীয় — বাকি ৪টা station 'Riverine' হলেও, "
                "siltation-জনিত ধারণ-ক্ষমতা কমে যাওয়া ও মেঘালয়ের আকস্মিক "
                "ঢলের কারণে Goalkanda/Nil Jinjiram-এর flood behavior আসলে "
                "Flash Flood ক্যাটাগরির সাথে বেশি মেলে, classic riverine-এর "
                "চেয়ে। district-level flood_type নির্ধারণের সময় এই nuance "
                "হারিয়ে যাওয়ার ঝুঁকি আছে যদি শুধু primary station (Bahadurabad) "
                "দেখে সিদ্ধান্ত নেওয়া হয়।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Jagannathganj",
            "ffwc_id": "SW48",
            "is_primary": False,

            "river": "যমুনা (Jamuna)",
            "upazila": "Sarishabari",
            "union": "Jagannathganj",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই যমুনা মূল প্রবাহ, Bahadurabad-এর প্রায় ৫০ কিমি "
                    "downstream (দক্ষিণে)। ঐতিহাসিক ফেরিঘাট এলাকা — এক সময় "
                    "রেল-ফেরি যোগাযোগের গুরুত্বপূর্ণ পয়েন্ট ছিল।"
                ),
                "flow_behavior": "Bahadurabad-এর মতোই braided, তবে danger_level কম (13.55m) কারণ bed elevation নিচু এই stretch-এ।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 13.55,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️ এই station-এর coordinate-এ সবচেয়ে বড় ভুলটা পাওয়া গেছে। "
                "stations.py-তে lat=24.83, lon=89.70 আছে, কিন্তু BWDB-র "
                "official hydrology survey database অনুযায়ী সঠিক coordinate "
                "হলো lat=24.6419, lon=89.8046 — প্রায় ২৩ কিমি দূরে ভুল জায়গায় "
                "বসানো ছিল (মূলত জামালপুর সদরের কাছাকাছি একটা বিন্দুতে, যেখানে "
                "আসলে হওয়া উচিত ছিল আরো দক্ষিণে, Sarishabari উপজেলার Jagannathganj "
                "ইউনিয়নে)। এছাড়া এই station flood_config.py-র জামালপুরের "
                "rivers list-এ একেবারেই নেই — stations.py-তে থাকলেও district "
                "profile-এ এখনো যুক্ত হয়নি।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1355,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ, Bahadurabad-এর মতোই রেঞ্জ (mean annual ~২০,২০০, bankfull ৪৫,০০০-৬০,০০০ m³/s)",
                    "source": "Best et al. 2022 (একই নদী, ~৫০ কিমি downstream, কোনো বড় confluence মাঝে নেই)",
                    "confidence": "moderate — Bahadurabad থেকে extrapolate করা, station-specific measured data পাওয়া যায়নি",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই যমুনা floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "Bahadurabad-এর মতোই classic riverine ঝুঁকি, ঐতিহাসিকভাবে গুরুত্বপূর্ণ ফেরি/যোগাযোগ পয়েন্ট হওয়ায় জনবসতিও ঘন",
                },
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Jamalpur",
            "ffwc_id": "SW225",
            "is_primary": False,

            "river": "পুরাতন ব্রহ্মপুত্র (Old Brahmaputra)",
            "upazila": "Jamalpur Sadar",
            "union": "Char Pakshimari",

            "river_structure": {
                "category": "small_or_tidal (ঐতিহাসিকভাবে ছিল mega_trunk — নদীটা নিজেই category বদলেছে)",
                "catchment": (
                    "১৭৮৭ সালের আগে এটাই ছিল ব্রহ্মপুত্রের মূল প্রবাহ — এখন "
                    "যমুনা মূল প্রবাহ বহন করে, আর পুরাতন ব্রহ্মপুত্র একটা "
                    "distributary/offtake হিসেবে টিকে আছে, Bahadurabad-এর "
                    "উজানে branch করে জামালপুর-ময়মনসিংহ-কিশোরগঞ্জ হয়ে "
                    "মেঘনায় গিয়ে মেশে (~২০০ কিমি)।"
                ),
                "flow_behavior": (
                    "নাটকীয়ভাবে সংকুচিত হয়ে গেছে। একটা গবেষণা অনুযায়ী flow "
                    "range বর্ষায় ৫০০-২২০০ m³/s-এর মধ্যে ওঠানামা করে, ক্রমাগত "
                    "কমতির দিকে (sharp decreasing trend)। ময়মনসিংহ অংশে তো "
                    "নদী প্রায় শুকিয়ে যাওয়ার খবরও এসেছে সংবাদমাধ্যমে।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 16.55,  # ✅ FFWC verify করা
            "highest_recorded_m": 17.20,
            "verified_source": "old.ffwc.gov.bd (stid=21), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "coordinate মোটামুটি ঠিকই ছিল — stations.py-তে lat=24.92, "
                "lon=89.94, BWDB official অনুযায়ী lat=24.9224, lon=89.9677 "
                "(পার্থক্য মাত্র ~৩ কিমি, নগণ্য)। danger_level ও union নাম "
                "(Char Pakshimari) দুই সোর্সেই মেলে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1655,
                    "corrected_estimate": 1200,
                    "corrected_range": "বর্ষায় ৫০০-২২০০ m³/s রেঞ্জে ওঠানামা করে, ক্রমহ্রাসমান প্রবণতা",
                    "source": "IEEE conference paper, 'Temporal variation characteristics of flow and water level in the Old Brahmaputra River'",
                    "note": (
                        "⚠️ মানিকগঞ্জের Jagir/পুরাতন ধলেশ্বরীর মতোই — এই নদীও "
                        "সময়ের সাথে ছোট হয়ে গেছে (mega_trunk থেকে small_or_tidal-এ)। "
                        "category নিজেই বদলেছে, তাই river_categories.py-র "
                        "কোনো single category-তে সঠিকভাবে বসে না। moderate "
                        "confidence — measured recent data পাওয়া গেছে, তবে "
                        "site-specific (Jamalpur সদর পয়েন্টে) না, বরং সাধারণ "
                        "trend থেকে।"
                    ),
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain assumption, তবে শহুরে এলাকা (জামালপুর সদর) হওয়ায় drainage/waterlogging factor-ও বিবেচনায় রাখা উচিত", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": (
                        "discharge কমে যাওয়া মানে বন্যার ঝুঁকি কম মনে হতে পারে, "
                        "কিন্তু siltation-জনিত reduced channel capacity আসলে "
                        "waterlogging/local flooding-এর ঝুঁকি বাড়ায় (ঠিক Nil "
                        "Jinjiram-এর মতো যুক্তি) — জামালপুর শহরের ভেতরেই এই "
                        "station, তাই urban drainage ফ্যাক্টরও প্রাসঙ্গিক।"
                    ),
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ শহুরে এলাকা (জামালপুর সদর) হওয়ায় সম্ভবত Urban Waterlogging "
                "উপাদানও আছে খাঁটি Riverine-এর পাশাপাশি — এই জেলার flood_type "
                "নির্ধারণে এই দুই-ধরনের overlap বিবেচনা করা দরকার, যেমনটা "
                "Manikganj-এর secondary station-গুলোতেও দেখা গিয়েছিল।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান station (Bahadurabad/যমুনা)-এর জন্য discharge/water-level "
        "trend primary — রাজবাড়ী/মানিকগঞ্জের মতোই যুক্তি। তবে এই জেলায় "
        "৩টা secondary station (Char-Rajibpur, Goalkanda, Jagannathganj) "
        "একই মূল নদীর (যমুনা/ব্রহ্মপুত্র) অংশ হওয়ায় সেগুলোর জন্য soil moisture "
        "কমানো ও discharge/water-level-কে primary রাখা যুক্তিসঙ্গত। কিন্তু "
        "৫ম station (Jamalpur/পুরাতন ব্রহ্মপুত্র) সম্পূর্ণ ভিন্ন চরিত্রের — "
        "discharge data কম নির্ভরযোগ্য এবং শহুরে drainage factor আছে, তাই "
        "এখানে local_rain-এর weight তুলনামূলক বেশি রাখা উচিত, ঠিক মানিকগঞ্জের "
        "Jagir/Taraghat-এর মতো।"
    ),

    "confluence_note": (
        "জামালপুর হলো বাংলাদেশের সবচেয়ে গুরুত্বপূর্ণ hydrological "
        "transition point — এখানেই ব্রহ্মপুত্র 'যমুনা' নাম নেয় (Bahadurabad-এ)। "
        "রাজবাড়ী+মানিকগঞ্জ (Padma-Jamuna confluence, downstream) এর সাথে "
        "জামালপুর (Brahmaputra-Jamuna name transition, upstream) মিলিয়ে "
        "যমুনা নদীর পুরো বাংলাদেশ-অংশের discharge picture (upstream থেকে "
        "confluence পর্যন্ত) এখন সম্পূর্ণ। আগামী candidate: Sirajganj বা "
        "Tangail (মাঝামাঝি অংশ) হলে পুরো যমুনা করিডোর cover হয়ে যাবে।"
    ),

    "cross_district_flags": (
        "⚠️ এই প্রোফাইল বানাতে গিয়ে যে ৩টা সমস্যা পাওয়া গেছে তার মধ্যে ২টা "
        "আসলে জামালপুরের একার সমস্যা না, বরং FFWC/stations.py-র সিস্টেমেটিক "
        "সমস্যার লক্ষণ: (১) FFWC-র live site-এ station ID duplicate/conflict "
        "থাকতে পারে (Goalkanda বনাম Boalmari), অন্য জেলাতেও এমন থাকার "
        "সম্ভাবনা আছে, যাচাই করা দরকার। (২) upazila-বিভাজনের ফলে তৈরি হওয়া "
        "নতুন জেলা (Char Rajibpur → Kurigram, ১৯৮৩) নিয়ে FFWC-র পুরনো "
        "administrative label থেকে যাওয়া সম্ভব অন্য station-এও।"
    ),
}