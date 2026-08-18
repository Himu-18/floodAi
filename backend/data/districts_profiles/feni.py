# ============================================================
# FloodAI — data/district_profiles/feni.py
#
# জেলা-বাই-জেলা framework-এর ১৩তম জেলা — মুহুরী নদী।
#
# ⚠️⚠️ বড় finding: flood_type='Dam-Affected' সম্ভবত ভুল classification —
# নিচে বিস্তারিত।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

FENI_PROFILE = {
    "district": "ফেনী",
    "district_lat": 23.02,
    "district_lon": 91.40,

    "station_count": 1,

    "stations": [
        {
            "name": "Parshuram",
            "ffwc_id": "SW212",
            "is_primary": True,

            "river": "মুহুরী (Muhuri)",
            "upazila": "Parshuram",
            "union": None,

            "river_structure": {
                "category": "small/medium (narrow, অত্যন্ত flashy — কুমিল্লার গোমতীর চেয়েও দ্রুত)",
                "catchment": (
                    "মুহুরী ত্রিপুরার পাহাড় থেকে সরাসরি নেমে আসা একটা transboundary "
                    "নদী, কাহুয়া ও সিলোনিয়া নদীর সাথে মিলিতভাবে একটা পৃথক "
                    "catchment গঠন করে যা সরাসরি বঙ্গোপসাগরে পড়ে (গোমতীর সাথে "
                    "যুক্ত না)।"
                ),
                "flow_behavior": (
                    "⚠️⚠️ অত্যন্ত flashy — ২০২৪-এর বন্যায় মুহুরী মাত্র ১৫ ঘণ্টায় "
                    "৬৯২ সেমি (৬.৯২ মিটার!) বৃদ্ধি পেয়েছিল, danger level-এর "
                    "১৫০ সেমি পর্যন্ত উপরে উঠেছিল। ফেনী আবহাওয়া অফিসে ২৪ ঘণ্টায় "
                    "৪৪০ মিমি বৃষ্টিপাত রেকর্ড হয়েছিল (২০২৪-এর সর্বোচ্চ)।"
                ),
                "upstream_reference": "Agartala, IN",
                "lag_time_hours": 6,
                "lag_time_note": "✅ ইতিমধ্যে সঠিকভাবে সবচেয়ে কম বসানো ছিল (এই framework-এ এখন পর্যন্ত সবচেয়ে কম lag_time) — বাস্তবতার সাথে মিলে যাচ্ছে",
            },

            "danger_level_m": 12.55,  # ✅ FFWC verify করা (SW212) — flood_config.py-র সাথে মিলেছে
            "highest_recorded_m": None,
            "verified_source": "একাধিক ২০২৪ সংবাদ প্রতিবেদন (Financial Express, bdnews24, Prothom Alo, BSS) — danger-এর ১৩৭-১৫০cm উপরে ওঠার তথ্য নিশ্চিত করা গেছে",

            "critical_finding": {
                "issue": "⚠️⚠️ flood_type='Dam-Affected' সম্ভবত ভুল classification",
                "evidence": (
                    "Prothom Alo-র একজন বিশেষজ্ঞের মতামত প্রবন্ধ স্পষ্টভাবে বলছে: "
                    "'ডুম্বুর বাঁধ থেকে পানি মুহুরী নদীর catchment-এ পৌঁছাতে হলে "
                    "প্রায় ২০ কিমি পাহাড়ি এলাকা পার হতে হবে' — অর্থাৎ মুহুরী-কাহুয়া "
                    "নদী ব্যবস্থা গোমতী/ডুম্বুর বাঁধের catchment থেকে **সম্পূর্ণ "
                    "আলাদা**। ২০২৪-এর ভয়াবহ বন্যা (BWDB প্রকৌশলীদের বিবৃতি "
                    "অনুযায়ী) হয়েছিল ভারী বৃষ্টিপাত + মুহুরী/কাহুয়া/সিলোনিয়া "
                    "নদীর ১৭টা পয়েন্টে **বাঁধ (embankment) ভাঙন**-এর কারণে — এটা "
                    "কোনো upstream ব্যারাজ/dam gate operation-চালিত ঘটনা না।"
                ),
                "distinction": (
                    "এখানে দুইটা ভিন্ন জিনিস গুলিয়ে ফেলা হয়েছে বলে মনে হচ্ছে: "
                    "(১) 'dam' = ভারতের ডুম্বুরের মতো upstream জলাধার-নিয়ন্ত্রণ "
                    "কাঠামো (Comilla/লালমনিরহাটে প্রাসঙ্গিক), আর (২) 'embankment/"
                    "flood-control dam' = বাংলাদেশের নিজস্ব নদীতীর বাঁধ যেটা "
                    "বন্যা ঠেকানোর জন্য বানানো, কিন্তু ভেঙে গেলে উল্টো বন্যা "
                    "worse করে। ইংরেজি সংবাদে দুটোই মাঝে মাঝে 'dam' শব্দ দিয়ে "
                    "বর্ণনা করা হয় (bdnews24-এর 'Muhuri dam breached' যেখানে "
                    "আসলে flood-control embankment বোঝানো হয়েছে), যা "
                    "flood_config.py-তে ভুল classification-এর কারণ হয়ে থাকতে পারে।"
                ),
                "recommendation": "flood_type='Flash Flood' বেশি সঠিক হবে (extreme rate-of-rise + rainfall-driven + embankment-breach-driven, কোনো real upstream dam-release-চালিত ঘটনা প্রমাণিত হয়নি)।",
            },

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1255,  # danger_level(12.55)*100
                    "corrected_estimate": 300,
                    "corrected_range": "⚠️ নির্দিষ্ট published discharge measurement পাওয়া যায়নি — 'narrow' transboundary নদী, শেরপুরের ভুগাইয়ের (~২৫০ m³/s) কাছাকাছি স্কেল ধরা হয়েছে",
                    "source": None,
                    "confidence": "low",
                    "note": "⚠️ শেরপুরের প্যাটার্নের পুনরাবৃত্তি — ছোট flashy নদীতে crude সূত্র (১২৫৫) সম্ভবত overestimate করছে বাস্তব discharge-এর (~৩০০) তুলনায়",
                },
                "cn": {"old_value": 86, "reviewed_estimate": 87, "reasoning": "ইতিমধ্যে উচ্চ মান বসানো ছিল (৮৬) — flashy পাহাড়ি catchment-এর জন্য যুক্তিসঙ্গত, সামান্য সমন্বয়", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "অতি উচ্চ",
                    "reviewed_estimate": "অতি উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
                    "reasoning": "এই framework-এ প্রথম 'অতি উচ্চ' tier জেলা — ২০২৪-এ ফেনীতে সর্বোচ্চ মৃত্যু (২৮ জন) হয়েছিল ১১ জেলার মধ্যে, সম্পূর্ণ সঠিক classification, upgrade/downgrade কোনোটাই দরকার নেই।",
                    "source": "Wikipedia (August 2024 Bangladesh floods, death toll by district)",
                },
            },

            "flood_type": "Dam-Affected",
            "flood_type_note": "⚠️⚠️ উপরে critical_finding দ্রষ্টব্য — সম্ভবত ভুল, 'Flash Flood' হওয়া উচিত",

            "inundation_bands": {
                "affected_upazilas": "পরশুরাম, ফুলগাজি, ছাগলনাইয়া — একাধিক সংবাদে নির্দিষ্টভাবে বারবার উল্লেখিত",
                "0_to_50cm_above_danger": "পরশুরাম/ফুলগাজির সীমান্তবর্তী নিচু এলাকা",
                "50cm_to_1m_above_danger": "ফুলগাজি বাজার ও আশেপাশের গ্রাম",
                "above_1m_danger": "২০২৪ স্কেলে (১৩৭-১৫০cm উপরে) — ২৫,০০০ পরিবার ক্ষতিগ্রস্ত, ব্যাপক embankment ভাঙন",
                "status": "⚠️ placeholder — DEM/DFO calibration বাকি, তবে ২০২৪ বন্যার বিস্তারিত upazila/village তালিকা পাওয়া গেছে",
            },
        },
    ],

    "soil_moisture_weight_note": "সিলেট/শেরপুরের একই যুক্তি — অত্যন্ত flashy নদীতে rainfall (৪৪০মিমি/২৪ঘন্টা-র মতো extreme event) সবচেয়ে গুরুত্বপূর্ণ predictor, soil_moisture/discharge_ratio কম কার্যকর এত দ্রুত পরিবর্তনশীল অবস্থায়।",

    "confluence_note": "ফেনী riverine.py-র CONFLUENCE_DISTRICTS-এ নেই, এবং গোমতী/ডুম্বুর বাঁধ সিস্টেমের সাথেও সরাসরি সম্পর্কিত না (উপরে critical_finding দ্রষ্টব্য)।",

    "cross_district_note": "এই গবেষণা নোয়াখালী/লক্ষ্মীপুরের জন্য প্রাসঙ্গিক হতে পারে — ২০২৪ বন্যায় ফেনীর উজানের পানি নোয়াখালীতে গিয়ে পরিস্থিতি আরো খারাপ করেছিল (Wikipedia অনুযায়ী)।",
}