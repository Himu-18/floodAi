# ============================================================
# FloodAI — data/district_profiles/dinajpur.py
#
# ২১তম জেলা। ২টা station — Punarbhaba (ভারত-বাংলাদেশ-ভারত সীমান্ত-
# পারাপার নদী, Thakurgaon-এর টাঙ্গনের মতোই) ও Upper Atrai (আত্রাই-
# বাঙালি-হুড়াসাগর সিস্টেমের উজানের বিন্দু, Sirajganj-এর Baghabari ও
# Bogura-র Bogra station-এর সাথে একই বৃহৎ নদী-নেটওয়ার্কের অংশ)। আগের
# জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

DINAJPUR_PROFILE = {
    "district": "দিনাজপুর",
    "district_lat": 25.6279,
    "district_lon": 88.6332,

    "station_count": 2,

    "stations": [
        {
            "name": "Dinajpur",
            "ffwc_id": "SW236",
            "is_primary": True,

            "river": "পুনর্ভবা (Punarbhaba)",
            "upazila": "Dinajpur Sadar",
            "union": "Chehelgazi",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "দিনাজপুরের ধেপা নদী থেকে উৎপন্ন (Dhepa River-এর "
                    "একটা শাখা হিসেবে শুরু), মোট দৈর্ঘ্য ১৬০ কিমি, "
                    "প্রস্থ ৩-৮ কিমি — Thakurgaon-এর টাঙ্গনের মতোই "
                    "ভারত-বাংলাদেশ সীমান্ত একাধিকবার পার হয়ে শেষে "
                    "নবাবগঞ্জ (রাজশাহী)-এর Gomostapur উপজেলায় "
                    "মহানন্দা নদীতে মিশে, যেটা পরে পদ্মায় গিয়ে পড়ে। "
                    "অর্থাৎ পুনর্ভবা গঙ্গা-পদ্মা সিস্টেমের অংশ, "
                    "ব্রহ্মপুত্র-যমুনা সিস্টেমের না — এই ব্যাচের প্রথম "
                    "নদী যেটা সরাসরি গঙ্গা-অববাহিকার অংশ।"
                ),
                "flow_behavior": "সমতল-ভূমির transboundary নদী, টাঙ্গনের মতোই — চরম flashy না, তুলনামূলক ধীরগতির।",
                "upstream_reference": "West Bengal, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 33.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 34.36,
            "verified_source": "old.ffwc.gov.bd, FFWC Annual Flood Report (নিয়মিত tracked), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Dinajpur Sadar/Chehelgazi) "
                "সব মিলে গেছে ✅। coordinate ভালো — stations.py "
                "lat=25.63,lon=88.64 বনাম BWDB official hydrology survey "
                "lat=25.6156,lon=88.6257 — মাত্র সামান্য পার্থক্য, নগণ্য। "
                "'Punarbhaba at Dinajpur' FFWC-র Annual Flood Report-এ "
                "নিয়মিত tracked (২০১৭, ২০১৯, ২০২১)।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 3305,
                    "corrected_estimate": 200,
                    "corrected_range": "নির্দিষ্ট figure পাওয়া যায়নি, ছোট-মাঝারি সমতল-ভূমির নদী হিসেবে অনুমান",
                    "source": "Wikipedia (Punarbhaba River)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 84, "reasoning": "সমতল কৃষিভূমি, তুলনামূলক ভালো natural drainage", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "danger_level margin (১.৩১ মি) তুলনামূলক ছোট, Thakurgaon-এর মতোই তুলনামূলক শান্ত আচরণ"},
            },

            "flood_type": "Riverine",
            "flood_type_note": "Thakurgaon-এর টাঙ্গনের ঠিক একই যুক্তি — সমতল-ভূমির সীমান্ত-পারাপার নদী, তুলনামূলক কম flashy।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "দিনাজপুর সদর, কাহারোলের নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "বিরল, বোচাগঞ্জের সংলগ্ন এলাকা",
                "above_1m_danger": "স্পষ্ট রেকর্ড পাওয়া যায়নি",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Bhusirbandar",
            "ffwc_id": "SW142.5",
            "is_primary": False,

            "river": "আপার আত্রাই (Upper Atrai)",
            "upazila": "Chirirbandar",
            "union": None,

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "⚠️ গুরুত্বপূর্ণ সংযোগ — এই station আত্রাই-বাঙালি-"
                    "হুড়াসাগর সিস্টেমের সবচেয়ে উজানের বিন্দুগুলোর একটা, "
                    "যেটা আগের প্রোফাইলগুলোতে বারবার এসেছে: Sirajganj-এর "
                    "Baghabari (এই সিস্টেমের সর্ব-দক্ষিণ প্রান্ত, হুড়াসাগর "
                    "নামে যমুনায় মেশে) ও Gaibandha-র Gaibandha (ঘাঘট)। "
                    "এই একই বৃহৎ উত্তরবঙ্গ-drainage-network এখন উজান থেকে "
                    "downstream পর্যন্ত (Dinajpur → Gaibandha → "
                    "Sirajganj) একটা প্রায়-সম্পূর্ণ picture পাচ্ছে।"
                ),
                "flow_behavior": "উজানের অংশ হওয়ায় তুলনামূলক ছোট flow, downstream-এ (Baghabari) গিয়ে অন্যান্য নদীর (করতোয়া, বাঙালি, গুড়, গুমানী) সাথে মিলে বড় হয়।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 39.15,  # ✅ FFWC verify করা
            "highest_recorded_m": 39.43,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila (Chirirbandar, FFWC-তে সামান্য "
                "টাইপো 'Chirirbdndar' দেখা গেছে — বানান-ভুল মাত্র, প্রকৃত "
                "সমস্যা না) মিলে গেছে ✅। ⚠️ একটা ছোট অসঙ্গতি — BWDB-র "
                "official hydrology survey table-এ এই এলাকার station-এর "
                "ID 'SW142.1' (coordinate 25.7700,88.7313) হিসেবে "
                "পাওয়া গেছে, stations.py/FFWC live-এর 'SW142.5' থেকে "
                "ভিন্ন। এটা Jamalpur-এর Goalkanda/SW327-এর মতো সরাসরি "
                "conflict না মনে হচ্ছে — সম্ভবত কাছাকাছি দুইটা ভিন্ন "
                "গেজ পয়েন্ট (একই নদী-সিস্টেমে প্রায়ই একাধিক sub-station "
                "থাকে), কিন্তু নিশ্চিত করার জন্য আরও verification ভালো। "
                "highest_recorded (39.43m) danger_level-এর মাত্র ২৮ "
                "সেমি উপরে — margin খুবই ছোট।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 3915,
                    "corrected_estimate": 500,
                    "corrected_range": "আত্রাই-হুড়াসাগর সিস্টেমের উজানের অংশ, Baghabari (Sirajganj)-এর corrected_estimate (১৫০০)-এর চেয়ে ছোট হওয়া উচিত (উজানে হওয়ায়)",
                    "source": "Sirajganj profile-এর Baghabari/Hurasagar data থেকে সামঞ্জস্য বিচার",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 85, "reasoning": "সমতল কৃষিভূমি, একই TR-55 যুক্তি", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": "danger_level margin খুবই ছোট (০.২৮ মি) — এই সংখ্যাটা যেকোনো ছোট বৃষ্টি-ইভেন্টেও অতিক্রম হতে পারে, তাই ঘন ঘন 'sensitive' signal দিতে পারে যদিও প্রকৃত বিপর্যয় নাও হতে পারে।",
                    "source": "FFWC data (margin analysis)",
                },
            },

            "flood_type": "Riverine (upstream point of the Atrai-Bangali-Hurasagar network)",
            "flood_type_note": "Gaibandha/Sirajganj profile-এর একই বৃহৎ সিস্টেমের অংশ — উজানের এই station-এর trend downstream Baghabari/Gaibandha-র early indicator হতে পারে।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    "soil_moisture_weight_note": (
        "উভয় station-এর জন্য (Punarbhaba, Upper Atrai) উজানের (ভারত) "
        "rainfall trend গুরুত্বপূর্ণ, কিন্তু Thakurgaon-এর মতোই এই দুটোও "
        "তুলনামূলক কম flashy — স্থানীয় soil moisture/rainfall-এর কিছুটা "
        "prognostic value থাকতে পারে।"
    ),

    "confluence_note": (
        "দিনাজপুর দুইটা ভিন্ন নদী-সিস্টেমের সংযোগ স্থাপন করছে এই "
        "প্রজেক্টে: (১) Thakurgaon-এর টাঙ্গনের সাথে (Ganges-অববাহিকা, "
        "সীমান্ত-পারাপার) এবং (২) Sirajganj/Gaibandha-র আত্রাই-বাঙালি-"
        "হুড়াসাগর সিস্টেমের সাথে (Upper Atrai দিয়ে, উজানের সংযোগ)। "
        "এটা এই প্রজেক্টের প্রথম জেলা যেটা দুইটা ভিন্ন major "
        "river-system cluster-কেই একসাথে স্পর্শ করছে।"
    ),

    "cross_district_flags": (
        "⚠️ Bhusirbandar-এর SW142.5 (stations.py/FFWC live) বনাম "
        "SW142.1 (BWDB survey table) ID পার্থক্য — Jamalpur-এর "
        "Goalkanda/SW327-এর মতো definitive conflict কিনা এখনো নিশ্চিত "
        "না, কিন্তু নজরে রাখা উচিত। ভবিষ্যতে wire করার সময় verify করা "
        "প্রয়োজন এটা একই station-এর দুই ID নাকি সত্যিই দুইটা কাছাকাছি "
        "ভিন্ন গেজ পয়েন্ট।"
    ),
}