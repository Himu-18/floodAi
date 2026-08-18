# ============================================================
# FloodAI — data/district_profiles/khulna.py
#
# ১৩তম জেলা। এই প্রথম Coastal & Tidal flood_type-এর জেলা এই প্রজেক্টে —
# সুন্দরবন/দক্ষিণ-পশ্চিম উপকূলীয় অঞ্চল। flood_types/coastal_tidal.py
# module আগে থেকেই আছে কিন্তু এখনো খুব crude (শুধু পূর্ণিমা heuristic,
# real tide/storm-surge API যোগ হয়নি) — এই profile-এর maঝেই সেটা flag
# করা আছে। আগের জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

KHULNA_PROFILE = {
    "district": "খুলনা",
    "district_lat": 22.8456,
    "district_lon": 89.5403,

    "station_count": 1,

    "stations": [
        {
            "name": "Khulna",
            "ffwc_id": "SW241",
            "is_primary": True,

            "river": "রূপসা (Rupsa)",
            "upazila": "Khalishpur Thana",
            "union": "Paurashava",

            "river_structure": {
                "category": "coastal_tidal",  # river_categories.py-তে সরাসরি নেই, নতুন category বিবেচনা করা যেতে পারে
                "catchment": (
                    "ভৈরব নদীর একটা শাখা, খুলনা শহরের দক্ষিণে ভৈরব "
                    "'রূপসা' নাম নেয়, তারপর আরও দক্ষিণে Chalna-র কাছে "
                    "'পশুর' নাম নিয়ে সুন্দরবনে প্রবেশ করে। খুলনা শহর "
                    "রূপসা ও ভৈরব — দুই নদীর তীরে অবস্থিত।"
                ),
                "flow_behavior": (
                    "⚠️ সম্পূর্ণ tidal-dominated — এই প্রজেক্টের প্রথম "
                    "খাঁটি জোয়ার-ভাটা নদী (Madaripur-এর আড়িয়াল খাঁ-ও "
                    "tidal-influenced ছিল, কিন্তু এখানে জোয়ারই প্রধান "
                    "নিয়ন্ত্রক)। দক্ষিণ-পশ্চিম উপকূলীয় অঞ্চলের নদীগুলো "
                    "(Satkhira, Khulna, Jessore) সবই tidal — কিন্তু "
                    "সাম্প্রতিক প্রতিবেদন (Dhaka Tribune, ২০২৪) অনুযায়ী "
                    "৩৭টা নদীর মধ্যে ২০টাতে পানি প্রবাহ প্রায় নেই — "
                    "unplanned সেতু, বাঁধ, পলি ভরাট, শিল্প-দূষণ ও দখলের "
                    "কারণে। রূপসা নিজে এখনো সচল, কিন্তু আশেপাশের অনেক "
                    "নদী মৃতপ্রায়।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 2.60,  # ✅ FFWC verify করা
            "highest_recorded_m": 3.49,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Khalishpur Thana/"
                "Paurashava) সব মিলে গেছে ✅। coordinate ভালো — "
                "stations.py lat=22.83,lon=89.53 বনাম Wikipedia-র Rupsa "
                "উপজেলা কেন্দ্র (খুলনা শহরের অংশ) lat=22.833,lon=89.583 — "
                "সামান্য পার্থক্য, গ্রহণযোগ্য।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 260,
                    "corrected_estimate": None,
                    "corrected_range": (
                        "⚠️ tidal নদীর জন্য 'reference_discharge' concept-টাই "
                        "সমস্যাজনক — একমুখী upstream discharge না, বরং "
                        "প্রতিদিন দুইবার জোয়ার-ভাটায় প্রবাহের দিক বদলায়। "
                        "একটা গবেষণা (South-western Bangladesh flood "
                        "study) SW243 (Rupsa-Pasur, কাছাকাছি station)-কে "
                        "return-period water-level পদ্ধতিতে বিশ্লেষণ "
                        "করেছে, absolute discharge না।"
                    ),
                    "source": "ResearchGate/PubMed (Flood Prediction and Risk Assessment, South-western Bangladesh)",
                    "confidence": "N/A — discharge-based feature এই নদী-ধরনের জন্য উপযুক্ত না",
                    "critical_caveat": (
                        "⚠️ এটা train_model.py-র danger_level*100 বাগের "
                        "চেয়েও গভীর সমস্যা — tidal নদীর জন্য "
                        "'reference_discharge' feature-টাই conceptually "
                        "ভুল। এই ধরনের station-এর জন্য tide-height ও "
                        "storm-surge proxy আলাদা feature হিসেবে দরকার, "
                        "শুধু সংখ্যা ঠিক করলে হবে না — একটা model-level "
                        "redesign প্রয়োজন।"
                    ),
                },
                "cn": {"old_value": None, "reviewed_estimate": None, "reasoning": "⚠️ CN (Curve Number) rainfall-runoff মডেলের জন্য তৈরি, tidal-dominated flood-এর জন্য সরাসরি প্রযোজ্য না।", "confidence": "N/A"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "খুলনা সুন্দরবনের প্রবেশদ্বার এবং cyclone/storm-"
                        "surge-প্রবণ অঞ্চলের অংশ (১৯৬১-২০২০ সময়ে ১৩টা "
                        "ঘূর্ণিঝড় সুন্দরবন অঞ্চলে আঘাত হেনেছে)। নদী-ক্ষয়, "
                        "লবণাক্ততা ও নদী-মৃত্যু একটা দীর্ঘমেয়াদী কাঠামোগত "
                        "ঝুঁকি তৈরি করছে যা danger_level cross হওয়ার "
                        "বাইরেও প্রাসঙ্গিক।"
                    ),
                    "source": "NCBI/PMC (Epidemic Dynamics Post-Cyclone, Sundarbans, ১৩ cyclones ১৯৬১-২০২০)",
                },
            },

            "flood_type": "Coastal & Tidal",
            "flood_type_note": (
                "⚠️ flood_types/coastal_tidal.py module আগে থেকেই আছে, "
                "কিন্তু বর্তমানে খুবই crude — শুধু 'পূর্ণিমা হলে +২০ বোনাস' "
                "এই lunar-phase heuristic, কোনো real tide calculation "
                "না। WorldTides/Stormglass API integrate না হওয়া পর্যন্ত "
                "এই district-এর prediction quality সীমিত থাকবে — এটা "
                "district-profile গবেষণার চেয়ে বড়, একটা আলাদা technical "
                "priority হিসেবে বিবেচনা করা উচিত।"
            ),

            "inundation_bands": {"status": "⚠️ placeholder — tidal/storm-surge dynamics সম্পূর্ণ ভিন্ন মডেল দাবি করে, সাধারণ rainfall-driven inundation band এখানে প্রযোজ্য না"},
        },
    ],

    "soil_moisture_weight_note": (
        "⚠️ Khulna (রূপসা)-র জন্য soil moisture ও rainfall দুটোরই "
        "prognostic value খুব সীমিত — এটা মূলত tide phase (পূর্ণিমা/"
        "অমাবস্যা) ও storm-surge/cyclone event-নির্ভর। বর্তমান crude "
        "lunar heuristic-এর জায়গায় real tide-height API যোগ করাটাই "
        "সবচেয়ে গুরুত্বপূর্ণ next step, soil-moisture weighting আলোচনার "
        "চেয়ে।"
    ),

    "confluence_note": (
        "খুলনা এই প্রজেক্টে প্রথমবার Coastal & Tidal flood_type-এর একটা "
        "জেলা যোগ করলো — সম্পূর্ণ ভিন্ন hydrology (জোয়ার-ভাটা, cyclone/"
        "storm-surge) যা যমুনা-করিডোর বা হাওর-flash-flood অঞ্চল থেকে "
        "মৌলিকভাবে আলাদা। Bagerhat ও Satkhira (এই একই batch-এ) যোগ হলে "
        "পুরো সুন্দরবন/দক্ষিণ-পশ্চিম উপকূলীয় cluster-এর একটা coherent "
        "picture তৈরি হবে।"
    ),

    "cross_district_flags": (
        "কোনো cross-district administrative conflict পাওয়া যায়নি এই "
        "জেলায়। মূল issue technical/conceptual — tidal নদীর জন্য "
        "reference_discharge feature-এর উপযুক্ততা প্রশ্নবিদ্ধ, এটা "
        "Bagerhat ও Satkhira profile-এও একই রকম প্রযোজ্য হবে।"
    ),
}