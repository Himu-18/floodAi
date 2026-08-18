# ============================================================
# FloodAI — data/district_profiles/sylhet.py
#
# জেলা-বাই-জেলা framework-এর ৭ম জেলা, প্রথম Flash Flood টাইপ জেলা।
# পদ্মা/যমুনার (mega_trunk, ধীরগতি) থেকে সম্পূর্ণ ভিন্ন dynamics —
# সুরমা-কুশিয়ারা অনেক ছোট আয়তনের নদী কিন্তু pahari ঢল-প্রবণ (fast-rise)।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SYLHET_PROFILE = {
    "district": "সিলেট",
    "district_lat": 24.90,
    "district_lon": 91.87,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 5,

    "stations": [
        {
            "name": "Sylhet",
            "ffwc_id": "SW267",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "সুরমা (Surma)",
            "upazila": "Sylhet Sadar",
            "union": "Baraikandi",

            # ── ৩. নদীর স্ট্রাকচার — ⚠️ পদ্মা/যমুনার থেকে সম্পূর্ণ আলাদা ──
            "river_structure": {
                "category": "large_regional (mega_trunk না — অনেক ছোট আয়তন, কিন্তু অতি দ্রুতগতির)",
                "catchment": (
                    "ভারতের আসামের বরাক নদী মেঘালয়ের কাছে দুই শাখায় ভাগ হয় — উত্তর "
                    "শাখা সুরমা, দক্ষিণ শাখা কুশিয়ারা। মেঘালয় মালভূমির অত্যন্ত "
                    "খাড়া ঢাল থেকে বৃষ্টির পানি সরাসরি নেমে আসে — বার্ষিক বৃষ্টিপাত "
                    "৫,০০০ মিমি-র বেশি (বিশ্বের সবচেয়ে বেশি বৃষ্টিপাতের একটা অঞ্চল, "
                    "চেরাপুঞ্জির কাছাকাছি)।"
                ),
                "flow_behavior": (
                    "⚠️ mega_trunk (পদ্মা/যমুনা)-র মতো ধীর/বড়-বাফার না — এখানে "
                    "পাহাড়ি ঢল-প্রবণ, পানি অতি দ্রুত ওঠে এবং নামে। একই কারণে "
                    "flood_config.py-তে flood_type='Flash Flood' আর lag_time মাত্র "
                    "১২ ঘণ্টা (রাজবাড়ীর ৪৪ ঘণ্টার তুলনায় অনেক কম) — এটা সঠিক ধরা "
                    "হয়েছিল।"
                ),
                "upstream_reference": "Shillong, IN",  # ✅ সঠিক — মেঘালয়ের রাজধানী, Malda(পদ্মা)/Guwahati(যমুনা) থেকে আলাদা
                "upstream_reference_note": "✅ সঠিক ছিল — মেঘালয় pahari ঢলের যথাযথ উৎস-প্রতিনিধি",
                "lag_time_hours": 12,
                "lag_time_note": "✅ ইতিমধ্যে সঠিকভাবে কম বসানো ছিল, flash-flood characteristic-এর সাথে সামঞ্জস্যপূর্ণ",
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 10.80,  # ✅ FFWC verify করা (SW267)
            "highest_recorded_m": 12.55,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1080,  # danger_level(10.8)*100
                    "corrected_estimate": 850,
                    "corrected_range": "মৌসুমি গড় ~৩০,০০০ কিউসেক (≈৮৫০ m³/s), ১৯৫০-৫৮ রেকর্ড সর্বোচ্চ ৫৩,০০৮ কিউসেক (≈১,৫০০ m³/s)",
                    "source": "Banglapedia (Surma River entry)",
                    "note": (
                        "⚠️⚠️ এখানে পুরনো buggy সূত্র (১০৮০) আর নতুন verified সংখ্যা "
                        "(৮৫০) আসলে **কাছাকাছি**! মজার ব্যাপার — পদ্মা/যমুনার মতো "
                        "mega_trunk নদীতে crude সূত্র ৩৫-৯০ গুণ ভুল ছিল, কিন্তু "
                        "সুরমার মতো ছোট আয়তনের নদীতে danger_level*100 আসলে অনেকটা "
                        "reasonable magnitude দেয় — কারণ ছোট নদীর discharge/danger-level "
                        "অনুপাত ছোট trunk নদীর কাছাকাছি স্কেলে পড়ে। **এটা একটা "
                        "গুরুত্বপূর্ণ প্যাটার্ন**: confluence bug টা মূলত mega_trunk "
                        "নদীতে (পদ্মা/যমুনা) কেন্দ্রীভূত, flash-flood/ছোট নদীতে ততটা "
                        "মারাত্মক না।"
                    ),
                    "confidence": "moderate — ঐতিহাসিক (১৯৫০-৫৮) data, সাম্প্রতিক পরিমাপ দিয়ে আপডেট করা ভালো হতো",
                },
                "cn": {
                    "old_value": 82,
                    "reviewed_estimate": 84,
                    "reasoning": (
                        "মেঘালয়ের খাড়া পাহাড়ি ঢাল থেকে দ্রুত runoff হওয়া এলাকার "
                        "জন্য CN সাধারণত বেশি হয় (কম infiltration, দ্রুত surface "
                        "runoff) — ৮২ ইতিমধ্যে যুক্তিসঙ্গত মানের কাছাকাছি ছিল, "
                        "সামান্য বাড়ানো হলো।"
                    ),
                    "confidence": "moderate",
                },
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
                    "reasoning": (
                        "২০২২ সালের flash flood-এ ২০ লক্ষের বেশি মানুষ ক্ষতিগ্রস্ত "
                        "হয়েছিল (Surma-Kushiyara অববাহিকা জুড়ে) — 'উচ্চ' যথাযথ, "
                        "upgrade করার দরকার নেই।"
                    ),
                    "source": "BDRCS Flash Flood 2022 SitRep",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": (
                "✅ ইতিমধ্যে সঠিকভাবে classify করা ছিল। সরকার ২০২৬-২০২৮ মেয়াদে "
                "১,২৭৩.৭৭ কোটি টাকার 'Surma-Kushiyara River Basin Development' "
                "প্রকল্প নিয়েছে — ১২১ কিমি dredging + ১৭ কিমি riverbank protection। "
                "এটা ভবিষ্যতে danger_level/discharge relationship বদলে দিতে পারে, "
                "তাই periodic re-verification দরকার হবে।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "গোয়াইনঘাট, কোম্পানীগঞ্জ, জৈন্তাপুরের নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "সিলেট সদর শহরের নিচু এলাকা (সুবিদবাজার, দক্ষিণ সুরমা)",
                "above_1m_danger": "২০২২ স্কেলে — ৩০০+ গ্রাম, সিলেট শহরের বড় অংশ প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি, তবে ২০২২ flood extent থেকে rough calibration সম্ভব",
            },
        },
        {
            "name": "Amalshid",
            "ffwc_id": "SW172",
            "is_primary": False,

            "river": "কুশিয়ারা (Kushiyara)",
            "upazila": "Zakiganj",
            "union": None,

            "river_structure": {
                "category": "large_regional",
                "catchment": "বরাকের দক্ষিণ শাখা, সীমান্তের ঠিক ওপারেই — Bangladesh-এ ঢোকার প্রথম gauge point",
                "flow_behavior": "সুরমার মতোই দ্রুতগতির, তবে erosion-prone সীমান্ত এলাকা (সরকারি প্রকল্পে বিশেষভাবে চিহ্নিত)",
                "upstream_reference": "Shillong, IN",
                "lag_time_hours": 12,
            },

            "danger_level_m": 15.40,  # ✅ FFWC verify করা
            "highest_recorded_m": None,  # নির্দিষ্ট তথ্য পাওয়া যায়নি এই সময়ে
            "verified_source": "old.ffwc.gov.bd, danger_level যাচাই করা হয়েছে ২০২৬-০৮-১০",
            "verification_note": "The Daily Star/TBS-এর একাধিক রিপোর্টে (২০২৫-২০২৬) এই station-এ ৭৫-৯৩cm above danger পর্যন্ত ওঠা-নামার রেকর্ড পাওয়া গেছে — অত্যন্ত volatile station",

            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1540, "corrected_estimate": 900, "confidence": "low-moderate — কুশিয়ারা-নির্দিষ্ট data কম, সুরমার সাথে সমান ধরা হয়েছে"},
                "cn": {"old_value": None, "reviewed_estimate": 84, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "সীমান্ত-সংলগ্ন সবচেয়ে volatile station, সরকারি প্রকল্পে erosion-hotspot হিসেবে বিশেষভাবে চিহ্নিত"},
            },

            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder — Sylhet primary station-এর অনুরূপ ধরা যায়"},
        },
        {
            "name": "Kanaighat",
            "ffwc_id": "SW266",
            "is_primary": False,

            "river": "সুরমা (Surma)",
            "upazila": "Kanaighat",
            "union": None,

            "river_structure": {
                "category": "large_regional",
                "catchment": "সিলেট (SW267)-এর একটু উজানে, একই সুরমা",
                "flow_behavior": "সুরমার একই দ্রুতগতির আচরণ",
                "upstream_reference": "Shillong, IN",
                "lag_time_hours": 12,
            },

            "danger_level_m": 12.75,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, danger_level যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "gap_found": (
                "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র সিলেটের "
                "'rivers' লিস্টে নেই (শুধু সুরমা-প্রধান/Sylhet station, কুশিয়ারা/"
                "Amalshid, আর সারিগোয়াইন/Sarighat আছে — Kanaighat আলাদাভাবে নেই)। "
                "বাস্তবে একাধিক সংবাদ প্রতিবেদনে (Daily Star, TBS, Dhaka Tribune) "
                "Kanaighat point-টাই বারবার danger crossing-এর headline উদাহরণ "
                "হিসেবে আসে — এটা সবচেয়ে গুরুত্বপূর্ণ gap এই জেলায়।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1275, "corrected_estimate": 850, "confidence": "moderate — Sylhet primary-র মতোই ধরা হয়েছে"},
                "cn": {"old_value": None, "reviewed_estimate": 84, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "সংবাদে বারবার প্রথম danger-crossing point হিসেবে উল্লেখিত"},
            },

            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder — Sylhet primary station-এর অনুরূপ"},
        },
        {
            "name": "Sheola",
            "ffwc_id": "SW173",
            "is_primary": False,

            "river": "কুশিয়ারা (Kushiyara)",
            "upazila": "Beani Bazar",
            "union": None,

            "river_structure": {
                "category": "large_regional",
                "catchment": "Amalshid-এর একটু ভাটিতে, একই কুশিয়ারা",
                "flow_behavior": "কুশিয়ারার একই দ্রুতগতির আচরণ",
                "upstream_reference": "Shillong, IN",
                "lag_time_hours": 12,
            },

            "danger_level_m": 13.05,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, danger_level যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "gap_found": "⚠️ Kanaighat-এর মতোই — এই station-ও flood_config.py-র rivers লিস্টে নেই।",

            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1305, "corrected_estimate": 900, "confidence": "low-moderate"},
                "cn": {"old_value": None, "reviewed_estimate": 84, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Amalshid-এর একই কুশিয়ারা reach"},
            },

            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Sarighat",
            "ffwc_id": "SW251",
            "is_primary": False,

            "river": "সারিগোয়াইন (Sarigowain)",
            "upazila": "Gowainghat",
            "union": None,

            "river_structure": {
                "category": "small (সুরমা/কুশিয়ারার উপনদী)",
                "catchment": "মেঘালয় থেকে সরাসরি নেমে আসা ছোট উপনদী, সুরমার একটা শাখা",
                "flow_behavior": "সুরমা-কুশিয়ারার চেয়েও দ্রুত ও ছোট আয়তনের — সবচেয়ে flash-flood-prone",
                "upstream_reference": "Shillong, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 12.35,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, danger_level যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1235,
                    "corrected_estimate": 300,
                    "corrected_range": "⚠️ নির্দিষ্ট published data নেই, সুরমা/কুশিয়ারার চেয়ে অনেক ছোট উপনদী হিসেবে conservative অনুমান",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 85, "confidence": "low — খাড়া পাহাড়ি ছোট catchment, উচ্চ CN যুক্তিসঙ্গত"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "গোয়াইনঘাট ২০২২ flash flood-এ সবচেয়ে বেশি ক্ষতিগ্রস্ত উপজেলাগুলোর একটা ছিল"},
            },

            "flood_type": "Flash Flood",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority ──
    "soil_moisture_weight_note": (
        "⚠️ পদ্মা/যমুনার উল্টো যুক্তি এখানে — flash flood জেলায় soil_moisture "
        "কমানোর দরকার নেই, বরং rainfall (local_rain + upstream_rain, বিশেষত "
        "Shillong/Meghalaya-র তাৎক্ষণিক বৃষ্টি) সবচেয়ে গুরুত্বপূর্ণ predictor "
        "হওয়া উচিত — ১২ ঘণ্টার lag time মানে discharge_ratio-ভিত্তিক ধীর "
        "সংকেতের চেয়ে rainfall-ভিত্তিক দ্রুত সংকেত বেশি কার্যকর হবে।"
    ),

    "confluence_note": "সিলেট CONFLUENCE_DISTRICTS-এ নেই — সম্পূর্ণ ভিন্ন নদী সিস্টেম (Barak/Meghalaya), পদ্মা-যমুনার সাথে কোনো সম্পর্ক নেই।",

    "cross_district_note": (
        "⚠️ এই জেলার গবেষণা সরাসরি সুনামগঞ্জ, মৌলভীবাজার, হবিগঞ্জের জন্য reuse "
        "করা যাবে — একই সুরমা-কুশিয়ারা সিস্টেম, একই উৎস (মেঘালয়/Shillong), "
        "একই Flash Flood dynamics। পরবর্তী জেলা হিসেবে এগুলো efficient হবে।"
    ),
}