# ============================================================
# FloodAI — data/district_profiles/gaibandha.py
#
# জেলা-বাই-জেলা framework-এর ৭ম জেলা। আগের ৬টা জেলার সাথে হুবহু একই
# ৭-ধাপ পদ্ধতি অনুসরণ করা হয়েছে।
#
# ⚠️ এই জেলা বগুড়ার Shimulbari station নিয়ে আগের সন্দেহ অনেকটাই সমর্থন
# করে — Chakrahimpur (SW63, Gaibandha-র Gobindaganj উপজেলা) verify
# করতে গিয়ে নিশ্চিত হলো যে 'Gobindaganj' নামের upazila বাস্তবেই
# Gaibandha জেলার অংশ (FFWC live নিজেই এটা এখানে সঠিকভাবে বলছে)। এটা
# Bogura-প্রোফাইলের Shimulbari station-এর সন্দেহকে জোরালো সমর্থন করে —
# ওই station সম্ভবত আসলে Gaibandha-র, Bogura-র না। (চূড়ান্ত সিদ্ধান্তের
# জন্য এখনো BWDB-কে সরাসরি জিজ্ঞাসা করা ভালো, কিন্তু এই finding-টা এখন
# আরও জোরালো প্রমাণ হিসেবে যোগ হলো)।
#
# ⚠️ Coordinate verification-এ যা পাওয়া গেছে (সবগুলো danger_level ঠিক
# ছিল, শুধু coordinate-এ পার্থক্য):
#   1. Chakrahimpur — ~১৭ কিমি off (lon)
#   2. Fulchari — ~১৩ কিমি off
#   3. Gaibandha (Ghagot) — প্রায় নিখুঁত (~১ কিমি off)
#   4. Haripur (Teesta) — ~১৩ কিমি off
#   5. Kamarjani — ~৮-৯ কিমি off
#   6. Saghata — ~১২ কিমি off
#
# ⚠️ BWDB official database-এ Gaibandha-য় stations.py-র চেয়ে একটা বেশি
# station আছে — Mohimaganj Railway Crossing (SW155, Katakhali নদী,
# Gobindaganj উপজেলা)। stations.py-তে নেই, coverage gap।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

GAIBANDHA_PROFILE = {
    "district": "গাইবান্ধা",
    "district_lat": 25.3288,
    "district_lon": 89.5285,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ৬টা — এখন পর্যন্ত এই ৭-জেলা প্রজেক্টের মধ্যে
    # সবচেয়ে বেশি স্টেশন-সমৃদ্ধ জেলা। কারণ গাইবান্ধা তিনটা ভিন্ন
    # নদী-সিস্টেমের সংযোগস্থল — যমুনা/ব্রহ্মপুত্র (mega_trunk), তিস্তা
    # (transboundary major tributary), এবং করতোয়া-বাঙালি-ঘাঘট local
    # drainage system।
    "station_count": 6,

    "stations": [
        {
            "name": "Kamarjani",
            "ffwc_id": "SW46",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "ব্রহ্মপুত্র (Brahmaputra)",
            "upazila": "Fulchhari",  # BWDB official অনুযায়ী; FFWC live-এ ফাঁকা
            "union": None,

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "একই ব্রহ্মপুত্র মূল প্রবাহ, Bahadurabad (জামালপুর, "
                    "নাম-পরিবর্তন বিন্দু)-এর উজানে, Kurigram-এর "
                    "Chilmari/Noonkhawa-র প্রায় ৩০-৪০ কিমি দক্ষিণে। "
                    "গাইবান্ধা জেলা 'যমুনা, তিস্তা ও ব্রহ্মপুত্রের সঙ্গমস্থল' "
                    "হিসেবে পরিচিত।"
                ),
                "flow_behavior": "একই braided, migrating চরিত্র, বাকি ব্রহ্মপুত্র-যমুনা-corridor জেলাগুলোর মতোই।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 21.70,  # ✅ FFWC verify করা
            "highest_recorded_m": None,  # FFWC live-এ ফাঁকা
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। coordinate off ছিল — stations.py-তে "
                "lat=25.38, lon=89.55, BWDB official অনুযায়ী lat=25.4094, "
                "lon=89.6259 — প্রায় ৮-৯ কিমি পূর্বে সরাতে হবে। উল্লেখ্য, "
                "FFWC live ও stations.py দুটোতেই upazila field ফাঁকা — এটা "
                "কোনো ভুল না, উৎসেই ফাঁকা।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2170,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা-ব্রহ্মপুত্র মূল প্রবাহ, mean annual ~২০,২০০ m³/s, bankfull ৪৫,০০০-৬০,০০০ m³/s",
                    "source": "Best et al. 2022 (একই নদী)",
                    "cross_check": "✅ river_categories.py-তে গাইবান্ধা=mega_trunk হওয়া উচিত।",
                    "critical_caveat": "আগের ৬টা যমুনা-করিডোর জেলার মতোই একই train_model.py বাগ প্রযোজ্য।",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই যমুনা-ব্রহ্মপুত্র floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "ফুলছড়ি/সাঘাটা উপজেলার চরাঞ্চল নিয়মিত প্লাবিত হয় — বাকি ব্রহ্মপুত্র-যমুনা-corridor জেলাগুলোর সাথে সামঞ্জস্যপূর্ণ 'উচ্চ' রেটিং।",
                    "source": "BSS News (২০২২, ২০২৪ বন্যা প্রতিবেদন — Sundarganj, Sadar, Fulchhari, Saghata উপজেলার char এলাকা নিয়মিত প্লাবিত)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "ক্লাসিক riverine বন্যা, বাকি যমুনা-ব্রহ্মপুত্র-corridor জেলাগুলোর মতোই।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "ফুলছড়ি, সাঘাটা উপজেলার চরাঞ্চল",
                "50cm_to_1m_above_danger": "গাইবান্ধা সদরের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — বিস্তৃত এলাকা প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Fulchari",
            "ffwc_id": "SW46.9R",
            "is_primary": False,

            "river": "যমুনা (Jamuna)",
            "upazila": "Fulchari",
            "union": "Gazaria",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "একই যমুনা মূল প্রবাহ, Kamarjani-র কাছাকাছি, ব্রহ্মপুত্র-যমুনা নাম-পরিবর্তন অঞ্চলের অংশ।",
                "flow_behavior": "একই braided, migrating চরিত্র।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 19.35,  # ✅ FFWC verify করা
            "highest_recorded_m": 20.69,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ও upazila (Fulchari)/union (Gazaria) সব "
                "মিলে গেছে ✅। coordinate off ছিল — stations.py-তে lat=25.30, "
                "lon=89.65, BWDB official অনুযায়ী lat=25.1871, lon=89.5993 — "
                "প্রায় ১৩ কিমি দক্ষিণ-পশ্চিমে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1935,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ",
                    "source": "Best et al. 2022",
                    "confidence": "moderate",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain", "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Kamarjani-র মতোই যুক্তি, ফুলছড়ি ঘাট এলাকা"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Gaibandha",
            "ffwc_id": "SW97",
            "is_primary": False,

            "river": "ঘাঘট (Ghagot)",
            "upazila": "Gaibandha Sadar",
            "union": None,

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "বাঙালি নদীর উৎস-অংশ — গাইবান্ধা শহরের পূর্ব দিক থেকে "
                    "উৎপন্ন হয়ে দক্ষিণে গিয়ে বাঙালি নাম নেয়, পশ্চিমে গিয়ে "
                    "ঘাঘট নাম নিয়ে শেরপুর (বগুড়া)-তে করতোয়ায় মেশে। "
                    "প্রাচীনকালে গুরুত্বপূর্ণ ছিল।"
                ),
                "flow_behavior": (
                    "ধীরগতির, আগাছায় ভরা 'sluggish stream'। flow মাত্র "
                    "৫০-২,৫০০ cusec (~১.৪-৭১ m³/s) — river_categories.py-র "
                    "'small_or_tidal' রেঞ্জের একেবারে নিচের দিকে, বগুড়ার "
                    "করতোয়ার (~৮৫ m³/s max) চেয়েও ছোট।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 21.25,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": "danger_level ঠিক আছে। coordinate প্রায় নিখুঁত — stations.py lat=25.33,lon=89.55 বনাম BWDB official lat=25.3392,lon=89.5510 — মাত্র ~১ কিমি পার্থক্য, নগণ্য।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2125,
                    "corrected_estimate": 40,
                    "corrected_range": "৫০-২,৫০০ cusec (~১.৪-৭১ m³/s)",
                    "source": "Banglapedia (Brahmaputra-Jamuna River System, Ghaghat River)",
                    "confidence": "moderate — নির্দিষ্ট রেঞ্জ published, কিন্তু বর্তমান average আলাদা হতে পারে",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "শহুরে/আধা-শহুরে floodplain (গাইবান্ধা সদর), drainage factor প্রাসঙ্গিক", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি-উচ্চ",
                    "reasoning": (
                        "নদী ছোট হলেও গাইবান্ধা সদরের ভেতর দিয়ে যাওয়ায় "
                        "urban drainage সমস্যা তৈরি করে। BSS News-এর "
                        "সাম্প্রতিক প্রতিবেদন (২০২২, ২০২৪) অনুযায়ী ব্রহ্মপুত্রের "
                        "সাথে একই সময়ে ঘাঘটও danger level cross করেছে — "
                        "এই দুই নদী একসাথে সমন্বিতভাবে বন্যা তৈরি করে, "
                        "স্বতন্ত্রভাবে না। এটা secondary station হলেও 'কম "
                        "গুরুত্বপূর্ণ' ধরে নেওয়া ঠিক না।"
                    ),
                    "source": "BSS News (২০২২-০৬-২০, ২০২৪-০৬-২০ বন্যা প্রতিবেদন)",
                },
            },

            "flood_type": "Riverine (correlated with Brahmaputra — একসাথে ওঠে)",
            "flood_type_note": (
                "⚠️ গুরুত্বপূর্ণ পর্যবেক্ষণ — সাম্প্রতিক news অনুযায়ী ঘাঘট ও "
                "ব্রহ্মপুত্র প্রায় একই সময়ে danger level cross করে (একই "
                "বৃষ্টি ইভেন্টে backwater effect বা একসাথে upstream rain "
                "থেকে)। এটা secondary station-কে independent না ভেবে "
                "primary-র সাথে correlated signal হিসেবে treat করার পক্ষে "
                "একটা যুক্তি।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Haripur",
            "ffwc_id": "SW294.5",
            "is_primary": False,

            "river": "তিস্তা (Teesta)",
            "upazila": "Sundarganj",
            "union": "Haripur",

            "river_structure": {
                "category": "medium",  # river_categories.py-তে সরাসরি নেই, catchment/discharge অনুযায়ী অনুমান
                "catchment": (
                    "সিকিম হিমালয়ের Tso Lhamo/Pahunri হিমবাহ থেকে উৎপন্ন, "
                    "মোট catchment ~১২,৫৪০-১৬,৭৬০ বর্গকিমি (উৎসের হিসাব-ভেদে), "
                    "যার ৫৭.৮৬% বাংলাদেশ অংশে। এই station-এই (Haripur, "
                    "ফুলছড়ি উপজেলা) তিস্তা ব্রহ্মপুত্র/যমুনায় গিয়ে মেশে — "
                    "তিস্তার একদম শেষ বিন্দু।"
                ),
                "flow_behavior": (
                    "⚠️ ভারত-বাংলাদেশ পানি-বণ্টন বিরোধের কেন্দ্রবিন্দু — "
                    "ভারতের Gajaldoba ব্যারেজ শুষ্ক মৌসুমে (ডিসেম্বর-মার্চ) "
                    "প্রায় সবটুকু পানি আটকে রাখে, ফলে বাংলাদেশ অংশে flow "
                    "নাটকীয়ভাবে কমে যায়। বর্ষায় হিমালয়ের দ্রুত-গলা বরফ ও "
                    "ভারী বৃষ্টির কারণে flashy, আকস্মিক flood-প্রবণ।"
                ),
                "upstream_reference": "Jalpaiguri, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 22.30,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ও upazila/union (Sundarganj/Haripur) সব "
                "মিলে গেছে ✅। coordinate off ছিল — stations.py-তে lat=25.48, "
                "lon=89.53, BWDB official + BM pillar দুটোই lat≈25.52-25.53, "
                "lon≈89.65 বলছে — প্রায় ১২-১৩ কিমি পূর্বে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2230,
                    "corrected_estimate": 500,
                    "corrected_range": (
                        "নির্দিষ্ট mean discharge figure পাওয়া যায়নি, কিন্তু "
                        "তিস্তা বাংলাদেশের ৪র্থ বৃহত্তম transboundary নদী "
                        "(গঙ্গা/ব্রহ্মপুত্র/মেঘনার পর) — river_categories.py-র "
                        "'medium' রেঞ্জের ঊর্ধ্বসীমার কাছাকাছি ধরা যুক্তিসঙ্গত, "
                        "যদিও শুষ্ক মৌসুমে ভারতের barrage diversion-এর কারণে "
                        "এই সংখ্যা অনেক কমে যায়।"
                    ),
                    "source": "Springer (Hydro-Economic Model of Teesta), studyiq.com (Teesta dispute)",
                    "confidence": "low — dry-season vs wet-season discharge-এ বিরাট পার্থক্য থাকায় একটা single reference_discharge সংখ্যা দিয়ে পুরো বছর capture করা কঠিন, dedicated seasonal modeling ভালো হবে",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "উত্তরবঙ্গের floodplain, তবে flashy hill-fed river হওয়ায় সাধারণ floodplain CN পুরোপুরি প্রযোজ্য নাও হতে পারে", "confidence": "low"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "তিস্তা flashy ও আকস্মিক বন্যা-প্রবণ — barrage "
                        "diversion-এর কারণে flow পূর্বাভাস করা কঠিন, উজানে "
                        "হঠাৎ পানি ছাড়া হলে দ্রুত বন্যা হতে পারে। এটা যমুনার "
                        "মতো ধীর, বৃহৎ trunk-river surge না, বরং আরো "
                        "flash-flood ধরনের আচরণ।"
                    ),
                    "source": "Teesta River Dispute literature (multiple sources); river's transboundary/barrage-controlled নেচার",
                },
            },

            "flood_type": "Flash Flood / Riverine (hybrid — barrage-নিয়ন্ত্রিত হওয়ায় predictable riverine না)",
            "flood_type_note": (
                "⚠️ গুরুত্বপূর্ণ nuance — তিস্তার flow ভারতের ব্যারেজ "
                "নিয়ন্ত্রণের অধীনে, তাই এটার behavior classic riverine "
                "(ধীরে ধীরে ওঠা, predictable) থেকে ভিন্ন — উজানে হঠাৎ পানি "
                "ছাড়া বা আটকানো হলে downstream-এ আকস্মিক পরিবর্তন হতে পারে। "
                "flood_type ট্যাগে এই আন্তর্জাতিক/রাজনৈতিক নিয়ন্ত্রণ ফ্যাক্টর "
                "প্রতিফলিত হওয়া উচিত।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই, barrage-নিয়ন্ত্রিত flow হওয়ায় সাধারণ rainfall-based inundation model কম নির্ভরযোগ্য"},
        },
        {
            "name": "Saghata",
            "ffwc_id": "SW46.5",
            "is_primary": False,

            "river": "যমুনা (Jamuna)",
            "upazila": "Saghata",
            "union": None,

            "river_structure": {
                "category": "mega_trunk",
                "catchment": "একই যমুনা মূল প্রবাহ, Fulchari/Kamarjani-র কাছাকাছি, Sirajganj-এর Kazipur-এর উজানে।",
                "flow_behavior": "একই braided, migrating চরিত্র।",
                "upstream_reference": "Guwahati, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 18.50,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। coordinate off ছিল — stations.py-তে "
                "lat=25.20, lon=89.65, BWDB official অনুযায়ী lat=25.1075, "
                "lon=89.5866 — প্রায় ১২ কিমি দক্ষিণ-পশ্চিমে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1850,
                    "corrected_estimate": 45000,  # bankfull (FAP24 1996e; Thorne et al. 1993, via Best et al. 2022) — আগে ভুলবশত mean annual (২০,২০০) বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত
                    "corrected_range": "একই যমুনা মূল প্রবাহ",
                    "source": "Best et al. 2022",
                    "confidence": "moderate",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain", "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Kamarjani/Fulchari-র মতোই যুক্তি"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Chakrahimpur",
            "ffwc_id": "SW63",
            "is_primary": False,

            "river": "করতোয়া (Karatoa)",
            "upazila": "Gobindaganj",
            "union": "Gobindaganj Psa",

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "করতোয়ার 'Rangpur-Karatoya' অংশ — Bogura-র 'Bogra-Karatoya' "
                    "অংশ (আগের জেলার Bogra/SW65 station)-এর থেকে ভিন্ন "
                    "সেগমেন্ট। এই দুইটা অংশ Shibganj উপজেলার (বগুড়া) একটা "
                    "শুকনো portion দিয়ে পৃথক হয়ে আছে। Rangpur-Karatoya "
                    "অংশে পানি খুবই কম, শেষে বাঙালি নদীতে গিয়ে মেশে।"
                ),
                "flow_behavior": "Bogra-Karatoya-র চেয়েও কম পানি বহন করে ('carries very little water' — Banglapedia-র ভাষ্যে)।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 19.70,  # ✅ FFWC verify করা
            "highest_recorded_m": 20.95,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ও upazila (Gobindaganj) সব মিলে গেছে ✅ — "
                "এবং এটাই নিশ্চিত করে যে 'Gobindaganj' সত্যিই একটা বৈধ "
                "গাইবান্ধা উপজেলা (Bogura-র Shimulbari station-এর জেলা-দ্বন্দ্ব "
                "প্রসঙ্গে এটা গুরুত্বপূর্ণ প্রমাণ — দেখুন এই ফাইলের উপরের "
                "মন্তব্য)। coordinate off ছিল — stations.py-তে lat=25.13, "
                "lon=89.53, BWDB official + BM pillar দুটোই lat≈25.147-25.148, "
                "lon≈89.358-89.36 বলছে — প্রায় ১৭ কিমি পশ্চিমে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1970,
                    "corrected_estimate": 50,
                    "corrected_range": "Bogura-Karatoya-র (~৮৫ m³/s max)-এর চেয়েও কম — 'carries very little water' (Banglapedia)",
                    "source": "Banglapedia (Brahmaputra-Jamuna River System)",
                    "confidence": "low — নির্দিষ্ট সংখ্যা পাওয়া যায়নি, তুলনামূলক বিবরণ থেকে অনুমান",
                },
                "cn": {"old_value": None, "reviewed_estimate": 88, "reasoning": "উত্তরবঙ্গের floodplain, নদী সংকুচিত হওয়ায় waterlogging-প্রবণ", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "নিম্ন-মাঝারি",
                    "reasoning": "প্রায়-মৃত ছোট নদী, Bogura-র Bogra/Karatoa station-এর মতোই যুক্তি — waterlogging risk বেশি, classic riverine surge risk কম।",
                    "source": "Banglapedia",
                },
            },

            "flood_type": "Urban Waterlogging (নদী সংকুচিত হওয়ায় Bogura-র Karatoa station-এর মতোই যুক্তি)",
            "flood_type_note": "বগুড়ার Bogra (SW65, Karatoa) station-এর ঠিক একই ধরনের যুক্তি প্রযোজ্য — ঐতিহাসিক বড় নদী, এখন সংকুচিত, waterlogging-প্রবণ।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান তিনটা station (Kamarjani, Fulchari, Saghata — যমুনা/"
        "ব্রহ্মপুত্র মূল প্রবাহ)-এর জন্য discharge/water-level trend "
        "primary, soil moisture কমানো — আগের জেলাগুলোর মতোই। Haripur "
        "(তিস্তা)-এর জন্য জটিল case — barrage-নিয়ন্ত্রিত flow হওয়ায় "
        "স্থানীয় rainfall/soil moisture কোনোটাই flow predict করার জন্য "
        "পর্যাপ্ত না; upstream (ভারতের) barrage release data ideally "
        "দরকার, যা সহজলভ্য না — এই সীমাবদ্ধতা স্পষ্টভাবে নোট রাখা উচিত। "
        "Gaibandha (ঘাঘট) ও Chakrahimpur (করতোয়া) — দুইটাই ছোট, সংকুচিত "
        "নদী, স্থানীয় rainfall/soil moisture-এর weight বেশি রাখা উচিত, "
        "ঠিক Bogura-র Bogra/Karatoa station-এর মতো যুক্তি।"
    ),

    "confluence_note": (
        "গাইবান্ধা তিনটা গুরুত্বপূর্ণ hydrological সংযোগ তৈরি করেছে: "
        "(১) যমুনা-ব্রহ্মপুত্র করিডোর আরও উত্তরে বিস্তৃত হলো (Jamalpur "
        "→ Sirajganj → Tangail → Manikganj চেইনের সাথে এখন Gaibandha "
        "যোগ হলো, Bahadurabad-এর উজানে); (২) তিস্তা নদী প্রথমবারের মতো "
        "এই প্রজেক্টে যোগ হলো — একটা সম্পূর্ণ ভিন্ন transboundary/"
        "barrage-নিয়ন্ত্রিত নদী-চরিত্র; (৩) করতোয়া-বাঙালি-ঘাঘট সিস্টেমের "
        "উজানের প্রান্ত এখন Bogura-র downstream প্রান্তের সাথে যুক্ত হলো, "
        "যা ভবিষ্যতে Sirajganj-এর Baghabari (হুড়াসাগর, একই সিস্টেমের "
        "সর্ব-দক্ষিণ প্রান্ত) পর্যন্ত একটা সম্পূর্ণ multi-district picture "
        "তৈরিতে সাহায্য করবে।"
    ),

    "cross_district_flags": (
        "⚠️ Chakrahimpur station নিশ্চিত করেছে যে 'Gobindaganj' একটা "
        "বৈধ Gaibandha উপজেলা — এটা Bogura-প্রোফাইলের Shimulbari (SW10) "
        "station-এর জেলা-দ্বন্দ্বকে সমর্থন করে এবং সম্ভাবনা বাড়িয়ে দেয় যে "
        "Shimulbari আসলে Gaibandha-র station, Bogura-র ভুলবশত tag করা। "
        "এই দুইটা জেলা প্রোফাইল (Bogura + Gaibandha) একসাথে wire করার "
        "সময় Shimulbari-র চূড়ান্ত জেলা-assignment নিয়ে একটা সিদ্ধান্ত "
        "নেওয়া প্রয়োজন — প্রয়োজনে সরাসরি BWDB-কে email করে নিশ্চিত করা "
        "যেতে পারে (api.support@bwdb.gov.bd, আগে থেকেই suggested)।"
    ),
}