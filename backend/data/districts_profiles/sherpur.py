# ============================================================
# FloodAI — data/district_profiles/sherpur.py
#
# জেলা-বাই-জেলা framework-এর ১০ম জেলা — ভুগাই নদী, Meghalaya-উৎসের
# আরেকটা flash flood সিস্টেম (Bhugai-Kangsha-Someshwari), সিলেটের
# সুরমা-কুশিয়ারার চেয়েও ছোট ও দ্রুতগতির।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SHERPUR_PROFILE = {
    "district": "শেরপুর",
    "district_lat": 25.02,
    "district_lon": 90.02,

    "station_count": 1,

    "stations": [
        {
            "name": "Nakuagaon",
            "ffwc_id": "SW34",
            "is_primary": True,

            "river": "ভুগাই (Bhugai)",
            "upazila": "Nalitabari",
            "union": None,

            "river_structure": {
                "category": "small (narrow, অত্যন্ত flashy — সিলেটের সুরমা/কুশিয়ারার চেয়েও ছোট)",
                "catchment": (
                    "ভুগাই একটা transboundary নদী, মেঘালয়ের দক্ষিণ গারো পাহাড় থেকে "
                    "সরাসরি নেমে আসে। CEGIS-এর নির্বাহী পরিচালক Malik Fida A Khan "
                    "নিজেই বলেছেন এটা 'rather a narrow river' — সুরমা/কুশিয়ারার "
                    "মতো বড় আয়তনের না। ভুগাই-কাংশা-সোমেশ্বরী একটা সংযুক্ত সিস্টেম "
                    "(Sherpur-Mymensingh-Netrokona জুড়ে), সবই Meghalaya-উৎসের।"
                ),
                "flow_behavior": (
                    "⚠️⚠️ চরম flashy — একটা রেকর্ডকৃত ঘটনায় ভুগাই ২৪ ঘণ্টায় ৬৪০ "
                    "সেমি (~২১ ফুট) বৃদ্ধি পেয়েছিল, danger level-এর ২০০ সেমি উপরে "
                    "উঠেছিল। এটা সিলেটের সুরমা/কুশিয়ারার চেয়েও দ্রুত react করে — "
                    "সিলেটে lag_time ১২ ঘণ্টা, এখানে flood_config-এ ২০ ঘণ্টা "
                    "বসানো আছে, যা এই flashy আচরণের সাথে সামঞ্জস্যপূর্ণ না মনে হচ্ছে "
                    "(নিচে দেখুন)।"
                ),
                "upstream_reference": "Guwahati, IN",  # flood_config.py-তে যা আছে
                "upstream_reference_caveat": (
                    "⚠️ সম্ভবত ভৌগোলিকভাবে কিছুটা ভুল — ভুগাইয়ের আসল উৎস মেঘালয়ের "
                    "দক্ষিণ গারো পাহাড় (Tura-র কাছাকাছি), যেটা গুয়াহাটি (আসাম) "
                    "থেকে বেশ দূরে ভিন্ন দিকে। সিলেটের upstream='Shillong,IN' "
                    "(মেঘালয়ের রাজধানী, সঠিক দিক) থেকে তুলনা করলে শেরপুরের জন্য "
                    "'Tura,IN' বা কাছাকাছি কোনো মেঘালয়ের স্থান বেশি সঠিক হতো। "
                    "রংপুর/লালমনিরহাটের upstream='Guwahati,IN' বা 'Jalpaiguri,IN' "
                    "-ও সঠিক কারণ তিস্তা/ব্রহ্মপুত্র সত্যিই আসামের দিক থেকে আসে — "
                    "কিন্তু ভুগাইয়ের ক্ষেত্রে এই একই 'Guwahati,IN' বসানো সম্ভবত "
                    "কপি-পেস্ট ভুল।"
                ),
                "lag_time_hours": 20,
                "lag_time_note": (
                    "⚠️ প্রশ্নসাপেক্ষ — ২৪ ঘণ্টায় ৬৪০ সেমি বৃদ্ধির মতো extreme flashy "
                    "আচরণের সাথে ২০ ঘণ্টা lag time কিছুটা বেশি মনে হচ্ছে। সিলেটের "
                    "সুরমা (১২ ঘণ্টা) থেকেও এটা ছোট/দ্রুততর নদী হওয়ায়, lag_time "
                    "১০-১২ ঘণ্টার কাছাকাছি হওয়া বেশি যুক্তিসঙ্গত মনে হয় — যদিও এটা "
                    "নির্দিষ্ট hydrograph analysis ছাড়া নিশ্চিত করা কঠিন।"
                ),
            },

            "danger_level_m": 21.95,  # ✅ FFWC verify করা (SW34) — flood_config.py-র সাথে মিলেছে
            "highest_recorded_m": None,
            "verified_source": "flood_config.py-র সাথে মিলেছে; New Age (২০২৪ সালের ৬৪০cm/২৪ghr বৃদ্ধির প্রতিবেদন), একাধিক ২০২৬ FFWC bulletin coverage",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2195,  # danger_level(21.95)*100
                    "corrected_estimate": 250,
                    "corrected_range": (
                        "⚠️ নির্দিষ্ট published discharge measurement পাওয়া যায়নি। "
                        "'narrow river' বর্ণনা এবং সিলেটের সারিগোয়াইনের (~৩০০ m³/s "
                        "অনুমান) সাথে তুলনা করে conservative অনুমান — সম্ভবত আরো ছোট।"
                    ),
                    "source": "New Age (CEGIS বিশেষজ্ঞের মন্তব্য 'narrow river')",
                    "confidence": "low — dedicated hydrological survey দরকার",
                    "note": (
                        "⚠️ এখানে উল্টো দিকে একটা সমস্যা — পুরনো buggy সূত্র (২১৯৫) "
                        "নতুন conservative অনুমান (২৫০)-এর চেয়ে ৮ গুণ বেশি! মানে "
                        "ছোট/narrow নদীতে danger_level*100 সূত্র প্রকৃত discharge-কে "
                        "**overestimate** করতে পারে (Padma/Jamuna-তে যেখানে "
                        "underestimate করেছিল)। এটা একটা নতুন প্যাটার্ন — সূত্রের "
                        "ভুল দিক নদীর আকারের উপর নির্ভর করে ভিন্ন হতে পারে।"
                    ),
                },
                "cn": {
                    "old_value": 80,
                    "reviewed_estimate": 87,
                    "reasoning": "খাড়া পাহাড়ি ছোট catchment, অত্যন্ত দ্রুত runoff (২৪ ঘণ্টায় ৬৪০ সেমি বৃদ্ধি) — উচ্চ CN যুক্তিসঙ্গত, সিলেটের সারিগোয়াইনের (৮৫) কাছাকাছি বা তার চেয়ে বেশি",
                    "confidence": "low-moderate",
                },
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
                    "reasoning": "একাধিক রেকর্ডকৃত flash flood ঘটনা (২৪ঘন্টায় ২০০সেমি উপরে ওঠা সহ), নালিতাবাড়ী/ঝিনাইগাতী/শ্রীবরদী উপজেলা বারবার ক্ষতিগ্রস্ত — upgrade দরকার নেই।",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "✅ সঠিকভাবে classify করা ছিল — সীমান্তবর্তী narrow transboundary নদী, extreme rate-of-rise-এর ইতিহাস আছে।",

            "inundation_bands": {
                "affected_upazilas": "নালিতাবাড়ী, ঝিনাইগাতী, শ্রীবরদী — New Age প্রতিবেদনে নির্দিষ্টভাবে উল্লেখিত",
                "0_to_50cm_above_danger": "নালিতাবাড়ীর সীমান্তবর্তী নিচু এলাকা",
                "50cm_to_1m_above_danger": "ঝিনাইগাতী, শ্রীবরদীর কৃষিজমি",
                "above_1m_danger": "২০২৪-এর ঘটনার স্কেলে (danger-এর ২০০সেমি উপরে) — ব্যাপক প্লাবন, গ্রামীণ রাস্তা বিচ্ছিন্ন",
                "status": "⚠️ placeholder — DEM/DFO calibration বাকি, তবে affected upazila-র তালিকা নির্দিষ্ট করা গেছে",
            },
        },
    ],

    "soil_moisture_weight_note": (
        "সিলেট/সারিগোয়াইনের একই যুক্তি — এখানে আরো তীব্রভাবে প্রযোজ্য, কারণ "
        "ভুগাই সুরমার চেয়েও দ্রুত react করে। rainfall (বিশেষত upstream Meghalaya "
        "rainfall) soil_moisture-এর চেয়ে অনেক বেশি গুরুত্বপূর্ণ, discharge_ratio "
        "এত দ্রুত পরিবর্তনশীল অবস্থায় কম কার্যকর predictor।"
    ),

    "confluence_note": "শেরপুর CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": (
        "এই গবেষণা মূলত মৈমনসিংহ ও নেত্রকোণার জন্য reuse করা যাবে — একই "
        "ভুগাই-কাংশা-সোমেশ্বরী সিস্টেম, সংবাদে তিনটা জেলাই সবসময় একসাথে "
        "উল্লেখিত হয়।"
    ),
}