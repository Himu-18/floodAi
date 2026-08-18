# ============================================================
# FloodAI — data/district_profiles/satkhira.py
#
# ১৫তম জেলা। Khulna/Bagerhat-এর মতোই Coastal & Tidal cluster, কিন্তু
# এখানে দুইটা station — দুটোই ভারত-সীমান্তবর্তী tidal নদী (Betna,
# ইছামতি)। আগের জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ Coordinate যা পাওয়া গেছে:
#   1. Kalaroa — ⚠️ সবচেয়ে বড় ভুল এই batch-এ, ~২৮ কিমি off
#   2. Shakra — ~১৯-২০ কিমি off
#   danger_level দুটোতেই ঠিক ছিল।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SATKHIRA_PROFILE = {
    "district": "সাতক্ষীরা",
    "district_lat": 22.7185,
    "district_lon": 89.0705,

    "station_count": 2,

    "stations": [
        {
            "name": "Shakra",
            "ffwc_id": "SW128",
            "is_primary": True,

            "river": "ইছামতি (Ichamati, পশ্চিম সীমান্ত)",
            "upazila": "Debhata",
            "union": "Parulia",

            "river_structure": {
                "category": "coastal_tidal",
                "catchment": (
                    "পদ্মার শাখা মাথাভাঙ্গা থেকে উৎপন্ন হয়ে ২০৮ কিমি "
                    "প্রবাহিত হয়ে ভারতের North 24 Parganas ও বাংলাদেশের "
                    "Debhata (সাতক্ষীরা) সীমান্তে Kalindi নদীর সাথে মেশে। "
                    "বাংলাদেশ-ভারত সীমান্ত-নদী — সীমান্তের ঠিক ওপারেই "
                    "ভারত সরকার একটা নতুন জেলার নামই 'Ichamati' রেখেছে "
                    "(২০২২)।"
                ),
                "flow_behavior": (
                    "সম্পূর্ণ tidal — 'Ichamati (Western Border)' নামে "
                    "BWDB-র নিজস্ব ডেটাতেও 'Tidal' চিহ্নিত। সাতক্ষীরা "
                    "জেলা লবণাক্ততা অনুপ্রবেশের (salinity intrusion) "
                    "একটা arxiv গবেষণায় (২০২৬) 'rapid salinization' "
                    "হিসেবে বিশেষভাবে চিহ্নিত হয়েছে — জোয়ারের পানি "
                    "ক্রমশ বেশি লবণাক্ত হচ্ছে, যা কৃষি ও সুপেয় পানির "
                    "ওপর সরাসরি প্রভাব ফেলছে।"
                ),
                "upstream_reference": "West Bengal, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 3.50,  # ✅ FFWC verify করা
            "highest_recorded_m": 3.98,
            "verified_source": "old.ffwc.gov.bd, BWDB official hydrology survey, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Debhata/Parulia) সব মিলে "
                "গেছে ✅। ⚠️ coordinate off ছিল — stations.py lat=22.60,"
                "lon=89.15 বনাম BWDB official lat=22.6173,lon=88.9618 — "
                "প্রায় ১৯-২০ কিমি পশ্চিমে সরাতে হবে। Wikipedia-র Debhata "
                "উপজেলা কেন্দ্র (lat=22.567,lon=88.967)-ও BWDB-র মানের "
                "কাছাকাছি, correction-কে সমর্থন করে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 350,
                    "corrected_estimate": None,
                    "corrected_range": "Khulna/Bagerhat-এর ঠিক একই কাঠামোগত সমস্যা — tidal নদী, একমুখী discharge concept অপ্রযোজ্য",
                    "source": "N/A",
                    "confidence": "N/A",
                    "critical_caveat": "Khulna profile-এ বিস্তারিত আলোচিত একই সমস্যা।",
                },
                "cn": {"old_value": None, "reviewed_estimate": None, "reasoning": "tidal-dominated flood-এর জন্য CN সরাসরি প্রযোজ্য না।", "confidence": "N/A"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "সাতক্ষীরা flood + salinity — দুইটা সমস্যার "
                        "combination-এ ভুগছে (২০২৬ arxiv গবেষণা)। ঘূর্ণিঝড়/"
                        "storm-surge, উপকূলীয় বন্যা, ভারী বৃষ্টি ও তাপপ্রবাহ "
                        "একসাথে জেলার পরিবেশগত চাপ বাড়াচ্ছে — চিংড়ি চাষের "
                        "জন্য বিখ্যাত হলেও সেটাই লবণাক্ততার একটা কারণও।"
                    ),
                    "source": "arXiv (Dynamic Learning Observatory Reveals Rapid Salinization of Satkhira, ২০২৬)",
                },
            },

            "flood_type": "Coastal & Tidal",
            "flood_type_note": (
                "⚠️ এই station-এ flood ও salinity intrusion দুটো সমস্যা "
                "ওভারল্যাপ করে — coastal_tidal.py module শুধু flood "
                "probability নিয়ে কাজ করে, salinity ট্র্যাক করে না। "
                "ভবিষ্যতে এই দুইটা আলাদা কিন্তু সম্পর্কিত সমস্যা একসাথে "
                "মডেল করার কথা ভাবা যেতে পারে, বিশেষত সাতক্ষীরার মতো "
                "জেলায়।"
            ),

            "inundation_bands": {"status": "⚠️ placeholder — tidal dynamics + salinity intrusion, Khulna/Bagerhat-এর চেয়েও জটিল combination"},
        },
        {
            "name": "Kalaroa",
            "ffwc_id": "SW23",
            "is_primary": False,

            "river": "বেতনা (Betna)",
            "upazila": "Kalaroa",
            "union": "Helatala",

            "river_structure": {
                "category": "coastal_tidal",
                "catchment": (
                    "যশোর জেলায় উৎপন্ন হয়ে সাতক্ষীরা ও খুলনা দিয়ে "
                    "প্রবাহিত, খুলনা অংশে 'কালিয়া' নামে পরিচিত, "
                    "কোবাদক নদীর একটা শাখা (দালুয়া) তৈরি করে। সুন্দরবনে "
                    "পৌঁছে নাম বদলে 'আরপাঙ্গাছিয়া' হয়, তারপর আবার "
                    "'মালঞ্চ' নামে বঙ্গোপসাগরে পড়ে — এক নদীর তিনটা "
                    "নাম-পরিবর্তন, বাংলাদেশের ব-দ্বীপ নদীগুলোর একটা "
                    "সাধারণ বৈশিষ্ট্য।"
                ),
                "flow_behavior": "BWDB-র ডেটায় 'Betna-Kholpetua' সিস্টেম নামে 'Tidal' চিহ্নিত।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 3.35,  # ✅ FFWC verify করা
            "highest_recorded_m": 4.74,
            "verified_source": "old.ffwc.gov.bd, BWDB official hydrology survey, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Kalaroa/Helatala) সব "
                "মিলে গেছে ✅। ⚠️ কিন্তু coordinate-এ এই পুরো batch-এর "
                "(Khulna+Bagerhat+Satkhira) মধ্যে সবচেয়ে বড় ভুল — "
                "stations.py lat=22.63,lon=88.98 বনাম BWDB official "
                "lat=22.8880,lon=89.0412 — প্রায় ২৮ কিমি উত্তরে সরাতে "
                "হবে। Wikipedia-র বিবরণও এটা সমর্থন করে — Kalaroa শহর "
                "'সাতক্ষীরার ১৮ কিমি উত্তরে' অবস্থিত বলা আছে, যেটা "
                "stations.py-র coordinate (যেটা প্রায় সাতক্ষীরা শহরের "
                "সমান lat-এ) না, বরং BWDB-র উত্তরের মানকে সমর্থন করে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 335,
                    "corrected_estimate": None,
                    "corrected_range": "একই কাঠামোগত সমস্যা — tidal নদী",
                    "source": "N/A",
                    "confidence": "N/A",
                },
                "cn": {"old_value": None, "reviewed_estimate": None, "reasoning": "tidal flood-এর জন্য প্রযোজ্য না", "confidence": "N/A"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি-উচ্চ",
                    "reasoning": "Shakra/ইছামতির চেয়ে সামান্য কম danger_level margin, কিন্তু একই জেলার salinity/flood combination ঝুঁকি প্রযোজ্য।",
                    "source": "Wikipedia (Betna River)",
                },
            },

            "flood_type": "Coastal & Tidal",
            "flood_type_note": "Shakra station-এর ঠিক একই যুক্তি প্রযোজ্য।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    "soil_moisture_weight_note": (
        "Khulna/Bagerhat-এর ঠিক একই যুক্তি — উভয় station-এর জন্য tide "
        "phase ও storm-surge/cyclone event primary driver, soil "
        "moisture/rainfall-এর ভূমিকা সীমিত। Satkhira-তে অতিরিক্তভাবে "
        "salinity intrusion trend-ও ভবিষ্যতে একটা প্রাসঙ্গিক feature "
        "হতে পারে, যদিও এটা flood risk-এর সরাসরি অংশ না।"
    ),

    "confluence_note": (
        "সাতক্ষীরা দিয়ে Coastal & Tidal cluster (Khulna, Bagerhat, "
        "Satkhira) সম্পূর্ণ হলো এই batch-এ। তিনটা জেলা মিলিয়ে এখন "
        "সুন্দরবন-সংলগ্ন উপকূলীয় অঞ্চলের একটা coherent picture — যদিও "
        "প্রতিটাই tidal reference_discharge-এর একই কাঠামোগত সমস্যায় "
        "ভুগছে, যেটা এই তিনটা প্রোফাইলেই বারবার flag করা হয়েছে।"
    ),

    "cross_district_flags": (
        "⚠️ Kalaroa-র coordinate error (~২৮ কিমি) এই batch-এর সবচেয়ে "
        "বড়। এছাড়া তিনটা জেলা জুড়েই (Khulna, Bagerhat, Satkhira) একটা "
        "common systemic issue উঠে এসেছে — coastal_tidal.py-র crude "
        "lunar-heuristic এবং reference_discharge feature-এর tidal "
        "নদীর জন্য অনুপযুক্ততা। এটা প্রতিটা জেলায় আলাদাভাবে fix করার "
        "চেয়ে একবারে একটা coastal-district-wide technical redesign "
        "হিসেবে সমাধান করা বেশি efficient হবে।"
    ),
}