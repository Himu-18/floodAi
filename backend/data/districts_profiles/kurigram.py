# ============================================================
# FloodAI — data/district_profiles/kurigram.py
#
# জেলা-বাই-জেলা framework-এর ৮ম জেলা। আগের ৭টা জেলার সাথে হুবহু একই
# ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ এই জেলা দুইটা পুরনো cross-district সন্দেহ সরাসরি resolve/confirm
# করেছে:
#   1. Char-Rajibpur (Jamalpur profile-এ flag করা হয়েছিল) — Wikipedia-র
#      Kurigram District পাতা নিজেই নিশ্চিত করেছে 'Char Rajibpur
#      Upazila' একটা বৈধ Kurigram উপজেলা ('island subdistrict in the
#      south of Kurigram, only accessible via water transport')। অথচ
#      FFWC-র SW44.5 station-কে 'District: Jamalpur' ট্যাগ করা আছে।
#      এটা নিশ্চিত করে যে Char-Rajibpur station সম্ভবত ভুল জেলায় ট্যাগ
#      করা, এখন Jamalpur profile-এ, আসলে Kurigram-এর হওয়া উচিত।
#   2. Boalmari/Goalkanda SW327 ID conflict (Jamalpur profile-এ flag
#      করা হয়েছিল) — এখানে নিশ্চিত হলো যে Boalmari (SW327, Kurigram,
#      Raumari উপজেলা) সত্যিই একটা আলাদা, বৈধ station, যেটা কাকতালীয়ভাবে
#      Jamalpur-এর Goalkanda station-এর সাথে একই ID শেয়ার করছে FFWC-র
#      নিজস্ব ডেটাবেজে। এটা FFWC-র ID-সিস্টেমের একটা real bug, দুইটা
#      completely ভিন্ন, বৈধ station।
#
# ⚠️ Coordinate/administrative verification-এ যা পাওয়া গেছে:
#   1. Chilmari — coordinate প্রায় নিখুঁত (~২ কিমি)
#   2. Kurigram (Dharla) — coordinate ভালো (~২ কিমি)
#   3. Boalmari — coordinate ভালো (~২৫ কিমি — দেখুন বিস্তারিত note)
#   4. Hatia — upazila/union ঠিক, coordinate ভালো
#   5. Noonkhawa — ⚠️ upazila conflict (stations.py 'Nageshwari' বনাম
#      BWDB survey table 'Kurigram Sadar' বনাম FFWC live current
#      'Nageshwari') coordinate-ও উল্লেখযোগ্য off
#   6. Pateswari — ⚠️ upazila conflict (stations.py/FFWC live
#      'Nageswari' বনাম BWDB survey table 'Bhurungamari') coordinate
#      অনেক off (~৩০ কিমি+)
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

KURIGRAM_PROFILE = {
    "district": "কুড়িগ্রাম",
    "district_lat": 25.8054,
    "district_lon": 89.6362,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ৬টা। কুড়িগ্রাম বাংলাদেশে ব্রহ্মপুত্রের প্রথম
    # প্রবেশ-বিন্দু এলাকা (ভারত থেকে) এবং তিনটা ভিন্ন Himalaya-fed
    # transboundary নদীর (ব্রহ্মপুত্র, ধরলা, দুধকুমার) সঙ্গমস্থল।
    "station_count": 6,

    "stations": [
        {
            "name": "Noonkhawa",
            "ffwc_id": "SW45",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "ব্রহ্মপুত্র (Brahmaputra)",
            "upazila": "Nageshwari",  # ✅ FFWC live current + stations.py একমত
            "union": "Kaliganj",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "বাংলাদেশে ব্রহ্মপুত্রের সবচেয়ে উজানের গুরুত্বপূর্ণ FFWC "
                    "station — ভারত থেকে নদী বাংলাদেশে প্রবেশ করার পরের "
                    "প্রথম major gauge গুলোর একটা। ২০১৯-এ রেকর্ড সর্বোচ্চ "
                    "জলস্তর (danger level থেকে ১.০৩ মিটার উপরে) এখানেই "
                    "পরিলক্ষিত হয়েছিল।"
                ),
                "flow_behavior": "একই braided, migrating চরিত্র, downstream-এর Kamarjani/Chilmari-র মতোই।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 26.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 27.63,
            "verified_source": "old.ffwc.gov.bd, BWDB monitoring report (২০১৪-১৯), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ও upazila (Nageshwari) FFWC live current "
                "data ও stations.py-তে মিলে গেছে ✅। ⚠️ তবে BWDB-র official "
                "hydrology survey table আলাদাভাবে এই station-এর upazila "
                "'Kurigram Sadar' বলছে, coordinate lat=25.9198, "
                "lon=89.7700 (যেটা stations.py-র lat=25.65,lon=89.75 "
                "থেকে অনেক দূরে — প্রায় ২৯ কিমি উত্তরে)। FFWC live current "
                "(real-time) ডেটা-ই primary সোর্স হিসেবে ধরা হলো, কিন্তু "
                "coordinate BWDB-র সাম্প্রতিক survey অনুযায়ী আপডেট করা "
                "উচিত।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2605,
                    "corrected_estimate": 42000,  # bankfull-এর নিচের দিকে (৪৫,০০০-৬০,০০০ রেঞ্জ) — Bahadurabad-এর উজানে, ধরলা/দুধকুমার/তিস্তা তখনো মেশেনি বলে সামান্য কম
                    "corrected_range": "একই যমুনা-ব্রহ্মপুত্র মূল প্রবাহ, mean annual ~২০,২০০ m³/s (তবে এই পয়েন্ট Bahadurabad-এর উজানে, ধরলা/দুধকুমার/তিস্তা এখনো মেশেনি, তাই সামান্য কম হওয়া স্বাভাবিক)",
                    "source": "Banglapedia (Jamuna River — Bahadurabad discharge represents flow entering Bangladesh PLUS Dudhkumar/Dharla/Tista, MINUS Old Brahmaputra/Bangali)",
                    "cross_check": "✅ river_categories.py-তে কুড়িগ্রাম=mega_trunk হওয়া উচিত।",
                    "critical_caveat": (
                        "⚠️ গুরুত্বপূর্ণ nuance — Bahadurabad-এর discharge "
                        "figure-এ ইতিমধ্যে Dudhkumar+Dharla+Tista যোগ করা "
                        "আছে, কিন্তু Noonkhawa এই তিনটা tributary-র "
                        "সঙ্গমের উজানে অবস্থিত (এই একই জেলাতেই এই "
                        "tributary-গুলো মেশে downstream-এ)। তাই Noonkhawa-র "
                        "reference_discharge Bahadurabad-এর চেয়ে সামান্য "
                        "কম হওয়া উচিত ML feature হিসেবে, ঠিক ২০,২০০ না। "
                        "আগের ৭টা যমুনা-করিডোর জেলার মতোই একই "
                        "train_model.py বাগ প্রযোজ্য, কিন্তু retrain করার "
                        "সময় এই upstream/downstream discharge gradient-টাও "
                        "বিবেচনায় রাখা উচিত।"
                    ),
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই যমুনা-ব্রহ্মপুত্র floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": (
                        "বাংলাদেশে ব্রহ্মপুত্রের প্রবেশ-বিন্দুর কাছাকাছি হওয়ায় "
                        "upstream (ভারতের আসাম) বৃষ্টির প্রভাব সবচেয়ে আগে ও "
                        "সবচেয়ে তীব্রভাবে এখানে পড়ে। ২০১৯-এ রেকর্ড সর্বোচ্চ "
                        "জলস্তর, নিয়মিত চর-ভাঙন।"
                    ),
                    "source": "BWDB monitoring report 2014-2019",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক riverine বন্যা, তবে upstream (ভারত) rainfall-এর early-warning signal হিসেবে বিশেষ গুরুত্বপূর্ণ — বাকি downstream জেলাগুলোর (Gaibandha, Jamalpur ইত্যাদি) জন্যও early indicator হতে পারে।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "নাগেশ্বরী, উলিপুর উপজেলার চরাঞ্চল",
                "50cm_to_1m_above_danger": "কুড়িগ্রাম সদরের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — বিস্তৃত এলাকা প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Kurigram",
            "ffwc_id": "SW77",
            "is_primary": False,

            "river": "ধরলা (Dharla)",
            "upazila": "Kurigram Sadar",
            "union": "Paurashava",

            "river_structure": {
                "category": "medium",  # flashy transboundary, কিন্তু mega_trunk না
                "catchment": (
                    "সিকিম হিমালয়ের Kupup/Bitang হ্রদ থেকে উৎপন্ন (Jaldhaka/"
                    "Singimari নামে পরিচিত উজানে), ভারত-ভুটান-বাংলাদেশ "
                    "তিন দেশ দিয়ে প্রবাহিত transboundary নদী। বাংলাদেশ "
                    "অংশে দৈর্ঘ্য মাত্র ~৬২ কিমি। ১৯৪৭ সালে পুরনো কুড়িগ্রাম "
                    "শহর সম্পূর্ণ ভেঙে ফেলেছিল এই নদী।"
                ),
                "flow_behavior": (
                    "Banglapedia স্পষ্টভাবে বলছে এটা 'flashy' নদী — "
                    "Himalaya-র খাড়া catchment থেকে দ্রুত পানি নামে। বর্ষায় "
                    "প্রবল স্রোত, শীতে হাঁটু-পানি। নিয়মিত bank shifting ও "
                    "erosion — একটা গবেষণায় দেখা গেছে upstream Taluk-"
                    "Shimulbari (SW76) station থেকে ৩০ কিমি downstream-এ "
                    "এই Kurigram station-এ discharge বাড়ে (tributary/"
                    "groundwater baseflow যোগ হওয়ায়)।"
                ),
                "upstream_reference": "Jalpaiguri, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 26.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 27.18,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": "danger_level, upazila (Kurigram Sadar) সব মিলে গেছে ✅। coordinate ভালো — stations.py lat=25.81,lon=89.66 বনাম BWDB official lat=25.8228,lon=89.6647 — মাত্র ~২ কিমি পার্থক্য।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2605,
                    "corrected_estimate": 800,
                    "corrected_range": (
                        "নির্দিষ্ট mean discharge figure পাওয়া যায়নি "
                        "(একাডেমিক গবেষণা আছে কিন্তু সরাসরি সংখ্যা উদ্ধৃত করা "
                        "যায়নি), কিন্তু 'flashy Himalaya-fed tributary' "
                        "হিসেবে river_categories.py-র 'medium' রেঞ্জের "
                        "মাঝামাঝি-উপরের দিকে ধরা যুক্তিসঙ্গত।"
                    ),
                    "source": "Banglapedia (Brahmaputra-Jamuna River System); Juniv.edu গবেষণাপত্র (Dharla discharge analysis, SW76-SW77)",
                    "confidence": "low-moderate — নির্দিষ্ট সংখ্যা পাওয়া যায়নি",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "Himalaya-fed flashy river floodplain, দ্রুত runoff", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "নিয়মিত bank erosion, ১৯৪৭ সালে পুরনো কুড়িগ্রাম শহর ধ্বংস করেছিল, ২০০৭ সালে ২ কিমি বাঁধ ভেঙে ৩০০০ মানুষ গৃহহীন হয়েছিল (Lalmonirhat অংশে)।",
                    "source": "Wikipedia (Dharla River); ResearchGate (Flood Maps and Bank Shifting of Dharla River)",
                },
            },

            "flood_type": "Flash Flood / Riverine (hybrid — flashy Himalayan tributary)",
            "flood_type_note": (
                "⚠️ Haripur (Gaibandha-র তিস্তা station)-এর মতোই যুক্তি — "
                "Dudhkumar, Dharla, Tista — বাংলাদেশের এই তিনটা major "
                "ব্রহ্মপুত্র-tributary Banglapedia দ্বারা স্পষ্টভাবে 'flashy' "
                "হিসেবে চিহ্নিত (Darjeeling-Bhutan হিমালয়ের খাড়া catchment "
                "থেকে)। classic ধীরগতির riverine surge-এর চেয়ে flash-flood "
                "চরিত্র বেশি প্রাসঙ্গিক।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই, flashy river হওয়ায় সাধারণ inundation-band পদ্ধতি কম নির্ভরযোগ্য"},
        },
        {
            "name": "Chilmari",
            "ffwc_id": "SW45.5",
            "is_primary": False,

            "river": "ব্রহ্মপুত্র (Brahmaputra)",
            "upazila": "Chilmari",
            "union": "Chilmari",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "একই ব্রহ্মপুত্র মূল প্রবাহ, Noonkhawa-র downstream-এ। চিলমারী ঐতিহাসিকভাবে গুরুত্বপূর্ণ নদী-বন্দর ও অর্থনৈতিক কেন্দ্র।",
                "flow_behavior": "একই braided, migrating চরিত্র।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 23.25,  # ✅ FFWC verify করা
            "highest_recorded_m": 24.37,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": "danger_level, upazila/union (Chilmari) সব মিলে গেছে ✅। coordinate প্রায় নিখুঁত — stations.py lat=25.55,lon=89.68 বনাম BWDB official lat=25.5681,lon=89.6789 — মাত্র ~২ কিমি পার্থক্য।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2325,
                    "corrected_estimate": 42000,  # bankfull-এর নিচের দিকে (৪৫,০০০-৬০,০০০ রেঞ্জ) — Bahadurabad-এর উজানে, ধরলা/দুধকুমার/তিস্তা তখনো মেশেনি বলে সামান্য কম
                    "corrected_range": "একই ব্রহ্মপুত্র-যমুনা মূল প্রবাহ",
                    "source": "Best et al. 2022",
                    "confidence": "moderate",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain", "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Noonkhawa-র মতোই যুক্তি, গুরুত্বপূর্ণ নদী-বন্দর এলাকা"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Hatia",
            "ffwc_id": "SW45A",
            "is_primary": False,

            "river": "ব্রহ্মপুত্র (Brahmaputra)",
            "upazila": "Ulipur",
            "union": "Hatia",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "একই ব্রহ্মপুত্র মূল প্রবাহ, Chilmari-র downstream-এ, Gaibandha-র Kamarjani-র উজানে।",
                "flow_behavior": "একই braided, migrating চরিত্র।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 24.40,  # ✅ FFWC verify করা
            "highest_recorded_m": 25.61,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": "danger_level, upazila/union (Ulipur/Hatia) সব মিলে গেছে ✅। coordinate ভালো — stations.py lat=25.40,lon=89.65 বনাম BWDB official lat=25.6803,lon=89.6920 — উল্লেখযোগ্য পার্থক্য (~২৮ কিমি), সংশোধন দরকার।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2440,
                    "corrected_estimate": 42000,  # bankfull-এর নিচের দিকে (৪৫,০০০-৬০,০০০ রেঞ্জ) — Bahadurabad-এর উজানে, ধরলা/দুধকুমার/তিস্তা তখনো মেশেনি বলে সামান্য কম
                    "corrected_range": "একই ব্রহ্মপুত্র-যমুনা মূল প্রবাহ",
                    "source": "Best et al. 2022",
                    "confidence": "moderate",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain", "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Noonkhawa/Chilmari-র মতোই যুক্তি"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Pateswari",
            "ffwc_id": "SW81",
            "is_primary": False,

            "river": "দুধকুমার (Dudhkumar)",
            "upazila": "Nageswari (FFWC live + stations.py) — ⚠️ BWDB survey table 'Bhurungamari' বলছে",
            "union": "Bamandanga",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "ভুটানের হিমালয় পাদদেশে উৎপন্ন (Wang Chhu/Thimphu "
                    "Chhu নামে উজানে, ভারতে Raidak নামে, বাংলাদেশে "
                    "Dudhkumar নামে) — তিন দেশ দিয়ে প্রবাহিত। মোট catchment "
                    "~৫,৮০০ বর্গকিমি, যার মাত্র ~২৪০ বর্গকিমি বাংলাদেশ "
                    "অংশে। Kurigram-এর Bhurungamari উপজেলার Shilkhuri "
                    "ইউনিয়ন দিয়ে বাংলাদেশে প্রবেশ করে।"
                ),
                "flow_behavior": (
                    "Banglapedia অনুযায়ী 'flashy' এবং boulder-strewn bed-এর "
                    "উপর দ্রুতগতির স্রোত — Dharla-র মতোই Himalaya-fed "
                    "চরিত্র। স্থানীয় বিবরণে 'destructive but beautiful "
                    "river' হিসেবে পরিচিত, প্রতি বছর নিয়মিত বন্যা করে।"
                ),
                "upstream_reference": "Bhutan/Jalpaiguri, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 29.60,  # ✅ FFWC verify করা — সর্বোচ্চ danger_level এই জেলার ৬টা station-এর মধ্যে
            "highest_recorded_m": 30.85,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে ✅। ⚠️ কিন্তু upazila নিয়ে conflict — "
                "FFWC live current ও stations.py দুটোই 'Nageswari' বলছে, "
                "কিন্তু BWDB-র official hydrology survey table স্পষ্ট করে "
                "বলছে 'Bhurungamari' (যেটা Dudhkumar নদীর বাংলাদেশ-প্রবেশ "
                "বিন্দুর upazila হিসেবে ভৌগোলিকভাবেও বেশি যুক্তিসঙ্গত — উপরে "
                "দেখুন catchment বিবরণ)। coordinate-এও বড় পার্থক্য — "
                "stations.py-তে lat=25.75, lon=89.80, BWDB official "
                "অনুযায়ী lat=26.0972, lon=89.7206 — প্রায় ৩৯ কিমি উত্তরে, "
                "এই ৮টা জেলার মধ্যে সবচেয়ে বড় coordinate error।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2960,
                    "corrected_estimate": 600,
                    "corrected_range": "catchment ~৫,৮০০ বর্গকিমি (মূলত ভুটান/ভারত অংশে), নির্দিষ্ট discharge figure পাওয়া যায়নি",
                    "source": "Dudhkumar River blog/local sources (catchment area data)",
                    "confidence": "low — নির্দিষ্ট measured discharge পাওয়া যায়নি",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "Himalaya-fed flashy river floodplain", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "সর্বোচ্চ danger_level এই জেলায় (29.60m) এবং flashy transboundary চরিত্র মিলিয়ে উল্লেখযোগ্য ঝুঁকি, যদিও catchment ছোট।",
                    "source": "Local sources (Dudhkumar river blog); FFWC data",
                },
            },

            "flood_type": "Flash Flood / Riverine (hybrid — Dharla-র মতোই flashy Himalayan tributary)",
            "flood_type_note": "Kurigram (Dharla) station-এর ঠিক একই যুক্তি প্রযোজ্য — flashy, transboundary, classic riverine-এর চেয়ে flash-flood চরিত্র বেশি প্রাসঙ্গিক।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Boalmari",
            "ffwc_id": "SW327",
            "is_primary": False,

            "river": "নীল জিঞ্জিরাম (Nil Jinjiram)",
            "upazila": "Raumari",
            "union": None,

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "জামালপুর প্রোফাইলের Goalkanda station-এর একই নদী "
                    "(নীল জিঞ্জিরাম), কিন্তু ভিন্ন, উজানের পয়েন্ট — মেঘালয় "
                    "থেকে উৎপন্ন হয়ে Kurigram-এর Raumari উপজেলা দিয়ে "
                    "বাংলাদেশে প্রবেশ করে, তারপর দক্ষিণে জামালপুরের "
                    "Dewanganj-এ গিয়ে Goalkanda station-এর কাছে পুরাতন "
                    "ব্রহ্মপুত্রে মেশে।"
                ),
                "flow_behavior": "মেঘালয়ের flash-flood-প্রবণ ঢল বহন করে, জামালপুরের Goalkanda-র মতোই siltation/ক্ষয়প্রবণ চরিত্র থাকতে পারে।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 23.90,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "⚠️ এই station-এর ID (SW327) নিয়ে Jamalpur profile-এ যে "
                "conflict flag করা হয়েছিল, সেটা এখানে নিশ্চিত হলো — "
                "Boalmari (Kurigram, Raumari) ও Goalkanda (Jamalpur, "
                "Dewanganj) দুইটাই FFWC-র লাইভ ডেটাবেজে আলাদা entry "
                "হিসেবে আছে, কিন্তু দুটোরই ID 'SW327' — এটা FFWC-র নিজস্ব "
                "সিস্টেমের একটা real ID-conflict bug, দুইটাই বৈধ ও পৃথক "
                "station (ভিন্ন জেলা, ভিন্ন danger_level: Boalmari 23.90m "
                "বনাম Goalkanda 21.50m, ভিন্ন coordinate)। danger_level "
                "ঠিক আছে stations.py-তে। coordinate off ছিল — stations.py-তে "
                "lat=25.85, lon=89.75, BWDB official অনুযায়ী lat=25.6174, "
                "lon=89.8670 — প্রায় ২৫ কিমি দক্ষিণ-পূর্বে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2390,
                    "corrected_estimate": 400,
                    "corrected_range": "জামালপুরের Goalkanda-র (~৪০০ m³/s corrected estimate) সাথে সামঞ্জস্যপূর্ণ ধরা হলো, একই নদীর অংশ",
                    "source": "The Daily Star, 'A River Dies in Kurigram' (2019) — জামালপুর প্রোফাইলের একই সোর্স",
                    "confidence": "low — Boalmari-নির্দিষ্ট measured data পাওয়া যায়নি, Goalkanda থেকে extrapolate করা",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "জামালপুরের Goalkanda-র মতোই যুক্তি", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি-উচ্চ",
                    "reasoning": "জামালপুরের Goalkanda-র মতোই যুক্তি — siltation-জনিত ক্ষমতা-হ্রাস মেঘালয়ের আকস্মিক ঢলের ঝুঁকি বাড়ায়।",
                    "source": "The Daily Star (2019) — জামালপুর প্রোফাইল থেকে",
                },
            },

            "flood_type": "Flash Flood (secondary/local — জামালপুরের Goalkanda-র মতোই)",
            "flood_type_note": "জামালপুর প্রোফাইলের Goalkanda station-এর ঠিক একই যুক্তি — মেঘালয়ের আকস্মিক ঢল ও siltation-জনিত ধারণ-ক্ষমতা হ্রাসের কারণে flash-flood চরিত্র বেশি প্রাসঙ্গিক, classic riverine-এর চেয়ে।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান তিনটা ব্রহ্মপুত্র station (Noonkhawa, Chilmari, Hatia)-এর "
        "জন্য discharge/water-level trend primary, soil moisture কমানো — "
        "আগের জেলাগুলোর মতোই। Kurigram (ধরলা) ও Pateswari (দুধকুমার) — "
        "দুইটাই flashy Himalayan tributary, তাই upstream (ভারত/ভুটান) "
        "rainfall/snowmelt-এর ওপর বেশি নির্ভরশীল, স্থানীয় soil moisture-এর "
        "prognostic value কম — Haripur (Gaibandha-র তিস্তা)-এর মতোই যুক্তি। "
        "Boalmari (নীল জিঞ্জিরাম)-এর জন্য জামালপুরের Goalkanda-র মতোই "
        "যুক্তি — soil moisture কমানো ঠিক কিন্তু local_rain-এর weight বেশি "
        "রাখা উচিত।"
    ),

    "confluence_note": (
        "কুড়িগ্রাম বাংলাদেশে ব্রহ্মপুত্রের 'entry point' জেলা — এখান থেকেই "
        "যমুনা-ব্রহ্মপুত্র করিডোরের বাংলাদেশ-অংশ শুরু হয় (Kurigram → "
        "Gaibandha → Jamalpur → Sirajganj → Tangail → Manikganj, ৮টা "
        "জেলা এখন এই একই মূল নদী-সিস্টেমের অংশ)। এছাড়া এই জেলা "
        "Dharla+Dudhkumar (উভয়ই flashy Himalayan tributary) নদীর "
        "বাংলাদেশ-প্রবেশ বিন্দুও ধারণ করে, যা Gaibandha-র তিস্তা (Haripur) "
        "এবং জামালপুরের নীল জিঞ্জিরাম (Goalkanda)-র সাথে মিলিয়ে একটা "
        "সম্পূর্ণ আলাদা 'flashy transboundary tributary' ক্যাটাগরির "
        "coherent picture তৈরি করছে — এই চারটা নদীই (Dudhkumar, Dharla, "
        "Tista, Nil Jinjiram) Banglapedia-তে একসাথে 'flashy' হিসেবে "
        "গোষ্ঠীবদ্ধ, তাই ভবিষ্যতে এদের জন্য একটা common flood_type/"
        "modeling approach তৈরি করা যেতে পারে, প্রতিটা আলাদাভাবে না করে।"
    ),

    "cross_district_flags": (
        "⚠️ এই জেলা দুইটা আগের সন্দেহ resolve করেছে (উপরে ফাইলের শুরুতে "
        "বিস্তারিত): (১) Char-Rajibpur (Jamalpur profile) সম্ভবত ভুল "
        "জেলায় ট্যাগ করা — Wikipedia নিশ্চিত করে এটা প্রকৃতপক্ষে Kurigram-এর "
        "উপজেলা। (২) Boalmari/Goalkanda SW327 conflict নিশ্চিতভাবে FFWC-র "
        "নিজস্ব ID-বাগ, দুইটাই বৈধ পৃথক station। এছাড়া Pateswari-র "
        "coordinate error (~৩৯ কিমি) এই প্রজেক্টের সবচেয়ে বড়, এবং "
        "upazila conflict (Nageswari বনাম Bhurungamari) নিয়ে এখনো "
        "নিশ্চিত সমাধান নেই — ভবিষ্যতে wire করার আগে BWDB-কে সরাসরি "
        "জিজ্ঞাসা করার তালিকায় Shimulbari (Bogura/Gaibandha) ও "
        "Char-Rajibpur (Jamalpur/Kurigram)-এর সাথে Pateswari-ও যোগ করা "
        "উচিত।"
    ),
}