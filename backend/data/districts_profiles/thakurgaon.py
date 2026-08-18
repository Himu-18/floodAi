# ============================================================
# FloodAI — data/district_profiles/thakurgaon.py
#
# ১৯তম জেলা। উত্তরাঞ্চলের সবচেয়ে উঁচু-elevation cluster-এর একটা —
# danger_level ৪৯.৯৫ মিটার (তুলনা করুন যমুনা-করিডোরের ১১-২৬ মিটারের
# সাথে) — কারণ এই এলাকা হিমালয়ের পাদদেশের অনেক কাছে, mean sea level
# থেকে বেশি উচ্চতায়। আগের জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

THAKURGAON_PROFILE = {
    "district": "ঠাকুরগাঁও",
    "district_lat": 26.0336,
    "district_lon": 88.4616,

    "station_count": 1,

    "stations": [
        {
            "name": "Thakurgaon",
            "ffwc_id": "SW285",
            "is_primary": True,

            "river": "টাঙ্গন (Tangon)",
            "upazila": "Thakurgaon Sadar",
            "union": "Nargun",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "পশ্চিমবঙ্গ (ভারত)-এর পাহাড় থেকে উৎপন্ন, ঠাকুরগাঁও "
                    "সদর, পীরগঞ্জ (ঠাকুরগাঁও), দিনাজপুরের বোচাগঞ্জ/বিরল "
                    "হয়ে আবার ভারতে (দক্ষিণ দিনাজপুর জেলা, পশ্চিমবঙ্গ) "
                    "প্রবেশ করে — অর্থাৎ এই নদী দুইবার সীমান্ত পার হয় "
                    "(ভারত→বাংলাদেশ→ভারত)। Boda শহরের কাছে একটা বাঁধও "
                    "আছে টাঙ্গন নদীর ওপর।"
                ),
                "flow_behavior": "উত্তরাঞ্চলের অন্যান্য নদীর মতোই flashy আচরণ, উজানের (ভারত) বৃষ্টির ওপর সরাসরি নির্ভরশীল।",
                "upstream_reference": "West Bengal, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 49.95,  # ✅ FFWC verify করা
            "highest_recorded_m": 50.87,
            "verified_source": "old.ffwc.gov.bd, FFWC Annual Flood Report (একাধিক বছর, নিয়মিত hydrograph tracked), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Thakurgaon Sadar/Nargun) "
                "সব মিলে গেছে ✅। coordinate প্রায় নিখুঁত — stations.py "
                "lat=26.03,lon=88.47 বনাম Wikipedia-র Thakurgaon Sadar "
                "কেন্দ্র lat=26.0208,lon=88.4667 — মাত্র সামান্য পার্থক্য। "
                "উল্লেখযোগ্য: FFWC-র Annual Flood Report-এ 'Tangon at "
                "Thakurgaon' নিয়মিতভাবে (২০১৭, ২০১৯, ২০২১ সহ প্রতি বছর) "
                "hydrograph comparison-এ থাকে — এটা একটা সুপ্রতিষ্ঠিত, "
                "দীর্ঘদিনের official forecasting point।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 4995,
                    "corrected_estimate": 300,
                    "corrected_range": "নির্দিষ্ট measured figure পাওয়া যায়নি, ছোট-মাঝারি transboundary নদী হিসেবে river_categories.py-র 'medium' রেঞ্জের নিচের-মাঝামাঝি অনুমান",
                    "source": "Wikipedia (Tangon River)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 85, "reasoning": "উত্তরাঞ্চলের সমতল কৃষিভূমি, তুলনামূলক ভালো drainage", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": "danger_level margin (০.৯২ মি) তুলনামূলক ছোট, এই batch-এর অন্য নদীগুলোর (Teesta, Karatoa) চেয়ে কম চরম আচরণ historical data-তে দেখা যাচ্ছে।",
                    "source": "FFWC bulletin data",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": "উত্তরাঞ্চলের ছোট transboundary নদী, classic riverine — Habiganj/Netrokona-র মতো অতটা চরম flashy না মনে হচ্ছে বর্তমান ডেটায়।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "ঠাকুরগাঁও সদর, পীরগঞ্জ উপজেলার নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "রাণীশংকৈল, বালিয়াডাঙ্গীর সংলগ্ন এলাকা",
                "above_1m_danger": "স্পষ্ট রেকর্ড পাওয়া যায়নি",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
    ],

    "soil_moisture_weight_note": (
        "উজানের (পশ্চিমবঙ্গ) rainfall trend গুরুত্বপূর্ণ predictor, "
        "কিন্তু danger_level margin ছোট হওয়ায় (এই batch-এ তুলনামূলক "
        "সবচেয়ে কম চরম) স্থানীয় soil moisture/rainfall-এরও কিছুটা "
        "prognostic value থাকতে পারে — Bandarban/Netrokona-র মতো "
        "সম্পূর্ণ upstream-নির্ভর না।"
    ),

    "confluence_note": (
        "ঠাকুরগাঁও উত্তরাঞ্চলের উচ্চ-elevation, transboundary নদী "
        "cluster-এর একটা সদস্য — Nilphamari (তিস্তা), Panchagarh "
        "(করতোয়া), Dinajpur (পুনর্ভবা/আত্রাই) এই একই batch-এর বাকি "
        "৩টা জেলার সাথে মিলে একটা coherent উত্তরাঞ্চল picture তৈরি করছে। "
        "টাঙ্গন নদী নিজে ভারত-বাংলাদেশ-ভারত — দুইবার সীমান্ত পার হওয়ার "
        "কারণে একটা আকর্ষণীয় ভূগোলিক বৈশিষ্ট্য বহন করে।"
    ),

    "cross_district_flags": "কোনো নতুন conflict পাওয়া যায়নি — এটা এই batch-এর সবচেয়ে 'ক্লিন' প্রোফাইল।",
}