# ============================================================
# FloodAI — data/district_profiles/panchagarh.py
#
# ২২তম জেলা, এবং এই batch-এর শেষ জেলা। বাংলাদেশের উত্তরতম জেলা এবং
# এই প্রজেক্টের সর্বোচ্চ danger_level (৭০.৩০ মিটার!)। সবচেয়ে গুরুত্বপূর্ণ
# finding: এই জেলার 'Upper Karatoa' station-ই সেই একই করতোয়া নদীর
# উৎস-বিন্দু যেটা Bogura (SW65, প্রায় মৃত নদী হিসেবে বর্ণিত) ও
# Gaibandha (SW63, Chakrahimpur) profile-এ ইতিমধ্যে documented। আগের
# জেলাগুলোর সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

PANCHAGARH_PROFILE = {
    "district": "পঞ্চগড়",
    "district_lat": 26.3411,
    "district_lon": 88.5541,

    "station_count": 1,

    "stations": [
        {
            "name": "Panchagarh",
            "ffwc_id": "SW140",
            "is_primary": True,

            "river": "আপার করতোয়া (Upper Karatoa)",
            "upazila": "Panchagar Sadar",
            "union": "Panchagarh",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "⚠️⚠️ সবচেয়ে গুরুত্বপূর্ণ finding এই profile-এ — এটাই "
                    "সেই করতোয়া নদীর আসল উৎস-বিন্দু! পশ্চিমবঙ্গ (ভারত, "
                    "জলপাইগুড়ি)-এর পাহাড় থেকে উৎপন্ন হয়ে পঞ্চগড়ে "
                    "বাংলাদেশে প্রবেশ করে, তারপর দক্ষিণে বয়ে গিয়ে "
                    "ধীরে ধীরে ছোট হতে হতে Bogura profile-এ documented "
                    "'প্রায়-মৃত' নদীতে পরিণত হয় (max discharge মাত্র "
                    "~৮৫ m³/s Bogra station-এ), এবং Gaibandha-র "
                    "Chakrahimpur-এ আরও কমে যায় ('carries very little "
                    "water' — Banglapedia)। অর্থাৎ পঞ্চগড় → দিনাজপুর → "
                    "গাইবান্ধা → বগুড়া — এই পুরো করতোয়া নদীর জীবনচক্র "
                    "(উৎস থেকে প্রায়-মৃত্যু) এখন এই প্রজেক্টে দৃশ্যমান।"
                ),
                "flow_behavior": (
                    "উৎসের কাছে হওয়ায় এখানে flow তুলনামূলক শক্তিশালী "
                    "ও পাহাড়ি-চরিত্রের flashy — downstream-এর সংকুচিত "
                    "রূপের থেকে সম্পূর্ণ ভিন্ন। danger_level (70.30m) "
                    "এই প্রজেক্টের সর্বোচ্চ — উচ্চতার কারণে (mean sea "
                    "level-এর datum থেকে), discharge-এর কারণে না।"
                ),
                "upstream_reference": "Jalpaiguri, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 70.30,  # ✅ FFWC verify করা — এই প্রজেক্টের সর্বোচ্চ
            "highest_recorded_m": 72.03,
            "verified_source": "old.ffwc.gov.bd, FFWC Annual Flood Report (নিয়মিত tracked, Figure 3.4 প্রতি বছর), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Panchagar Sadar/Panchagarh) "
                "সব মিলে গেছে ✅। coordinate ভালো — stations.py "
                "lat=26.33,lon=88.56 বনাম Wikipedia-র Panchagarh জেলা "
                "কেন্দ্র lat=26.2,lon=88.34 তুলনায় সামান্য uttar-purbe, "
                "কিন্তু জেলা সদর শহর নিজেই জেলার কেন্দ্র থেকে ভিন্ন "
                "অবস্থানে থাকতে পারে — grহণযোগ্য। 'Upper Karatoa at "
                "Panchagarh' FFWC-র Annual Flood Report-এ নিয়মিত ট্র্যাক "
                "করা একটা established forecasting point।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 7030,
                    "corrected_estimate": 150,
                    "corrected_range": (
                        "নির্দিষ্ট measured figure পাওয়া যায়নি, কিন্তু "
                        "downstream-এর তুলনা থেকে reverse-engineer করা "
                        "যায় — যদি Bogra (অনেক downstream)-এ max ~৮৫ "
                        "m³/s হয়, তাহলে উৎসের কাছে (এখানে) সাধারণ flow "
                        "সম্ভবত বেশি হওয়া উচিত (এখনো কোনো major "
                        "abstraction/siltation হয়নি), কিন্তু নির্দিষ্ট "
                        "সংখ্যা অনুমান।"
                    ),
                    "source": "Bogura profile cross-reference (downstream data থেকে reverse inference)",
                    "confidence": "low — এটা সরাসরি measured না, downstream comparison থেকে অনুমিত",
                },
                "cn": {"old_value": None, "reviewed_estimate": 86, "reasoning": "পাহাড়ি-সংলগ্ন উৎস অঞ্চল, দ্রুত initial runoff", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "উৎসের কাছাকাছি হওয়ায় upstream (ভারত) বৃষ্টির প্রভাব সবচেয়ে দ্রুত পড়ে — Kurigram-এর Noonkhawa-র মতো একই যুক্তি (early-warning-এর দিক থেকে গুরুত্বপূর্ণ)।",
                    "source": "Geographic reasoning (উৎস-বিন্দু হওয়ার কারণে)",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ Bogura profile-এ করতোয়াকে 'Urban Waterlogging'-এর "
                "দিকে ঝুঁকিয়ে দেওয়া হয়েছিল (নদী সংকুচিত হওয়ায়), কিন্তু "
                "এখানে উৎসের কাছে সেই যুক্তি প্রযোজ্য না — এটা এখনো একটা "
                "স্বাভাবিক, সক্রিয় riverine নদী। এটা একই নদীর ভিন্ন "
                "stretch-এ ভিন্ন flood_type হওয়ার একটা স্পষ্ট উদাহরণ — "
                "district-level single flood_type ট্যাগের সীমাবদ্ধতা "
                "আরেকবার প্রমাণিত হলো।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "পঞ্চগড় সদর, তেঁতুলিয়ার সীমান্তবর্তী নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "বোদা, দেবীগঞ্জের সংলগ্ন এলাকা",
                "above_1m_danger": "স্পষ্ট রেকর্ড পাওয়া যায়নি",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
    ],

    "soil_moisture_weight_note": (
        "উজানের (পশ্চিমবঙ্গ/জলপাইগুড়ি) rainfall trend প্রধান predictor — "
        "উৎসের কাছাকাছি হওয়ায় lag time কম হওয়া উচিত, তাই upstream rain "
        "signal দ্রুত reflect হবে। soil moisture-এর ভূমিকা মাঝারি।"
    ),

    "confluence_note": (
        "⚠️ পঞ্চগড় এই batch-এর সবচেয়ে গুরুত্বপূর্ণ connective finding "
        "বহন করছে — করতোয়া নদীর সম্পূর্ণ জীবনচক্র (পঞ্চগড়ে শক্তিশালী "
        "উৎস → Dinajpur/Gaibandha-তে মাঝারি প্রবাহ → Bogura-তে প্রায়-"
        "মৃত) এখন documented। এটা ভবিষ্যতে একটা 'river life-cycle' "
        "visualization বা cross-district feature তৈরির ভালো candidate "
        "হতে পারে — একই নদী কীভাবে upstream থেকে downstream-এ "
        "hydrologically রূপান্তরিত হয় তার একটা concrete উদাহরণ।"
    ),

    "cross_district_flags": (
        "কোনো নতুন administrative conflict নেই। মূল contribution হলো "
        "করতোয়া নদীর multi-district life-cycle picture সম্পূর্ণ করা।"
    ),
}