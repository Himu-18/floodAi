# ============================================================
# FloodAI — data/district_profiles/rangpur.py
#
# জেলা-বাই-জেলা framework-এর ৮ম জেলা — তিস্তা নদী সিস্টেম, ভারতের
# গজলডোবা ব্যারাজের কারণে flow-নিয়ন্ত্রিত (dam-affected dynamics)।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

RANGPUR_PROFILE = {
    "district": "রংপুর",
    "district_lat": 25.75,
    "district_lon": 89.25,

    "station_count": 2,

    "stations": [
        {
            "name": "Kaunia",
            "ffwc_id": "SW294",
            "is_primary": True,

            "river": "তিস্তা (Teesta)",
            "upazila": "Kaunia",
            "union": None,

            "river_structure": {
                "category": "large_regional (mega_trunk না — ভারতের গজলডোবা ব্যারাজ প্রায় পুরো flow ডাইভার্ট করে)",
                "catchment": (
                    "তিস্তার মোট দৈর্ঘ্য ৪১৪ কিমি, catchment ~১২,১৫৯ বর্গকিমি — এর "
                    "৮৩% ভারতে, মাত্র ১৭% বাংলাদেশে। গজলডোবা ব্যারাজ (ভারত) থেকে "
                    "Dalia (নীলফামারী) পর্যন্ত আসা পানির প্রায় পুরোটাই ব্যারাজে "
                    "সেচের জন্য ডাইভার্ট হয় — Kaunia পয়েন্টে যা আসে তা মূলত "
                    "Dalia ব্যারাজের release + সামান্য baseflow/groundwater "
                    "regeneration, কোনো ডাইভারশন নেই এই পয়েন্টে।"
                ),
                "flow_behavior": (
                    "⚠️ 'flashy' নদী (steep gradient ১:২০০০) — কিন্তু ভারতের ব্যারাজ "
                    "operation-এর উপর ভীষণভাবে নির্ভরশীল, তাই flood_config.py-তে "
                    "flood_type='Dam-Affected' ধরা সঠিক। ২০২১ সালের extreme flash "
                    "flood-এ গজলডোবা থেকে ৫,৫০০ m³/s surplus discharge ছেড়ে দেওয়ায় "
                    "(সিকিম/দার্জিলিং-এ cloudburst-এর কারণে) তিস্তা অববাহিকা প্লাবিত "
                    "হয়েছিল — এটা normal monsoon rainfall না, upstream gate "
                    "operation-চালিত।"
                ),
                "upstream_reference": "Jalpaiguri, IN",  # ✅ সঠিক — গজলডোবা ব্যারাজ জলপাইগুড়িতেই অবস্থিত
                "upstream_reference_note": "✅ ইতিমধ্যে সঠিক ছিল, গজলডোবা ব্যারাজের সাথে ভৌগোলিকভাবে সামঞ্জস্যপূর্ণ",
                "lag_time_hours": 10,
                "lag_time_note": "✅ flashy নদীর জন্য যুক্তিসঙ্গত কম মান",
            },

            "danger_level_m": 29.31,  # ✅ FFWC verify করা (SW294)
            "highest_recorded_m": None,  # নির্দিষ্ট তথ্য পাওয়া যায়নি
            "verified_source": "flood_config.py-র সাথে মিলেছে; একাধিক ২০২৬ সংবাদ প্রতিবেদনে (Bonikbarta) danger-crossing ঘটনা নিশ্চিত করা গেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 2931,  # danger_level(29.31)*100
                    "corrected_estimate": 4000,
                    "corrected_range": (
                        "১৯৮৫-২০০৬ ঐতিহাসিক তথ্য: সর্বোচ্চ discharge ৮,৫৭৭ m³/s "
                        "(২১ এপ্রিল ২০০৪), সর্বনিম্ন ৫.৪৭ m³/s (১৫ ফেব্রুয়ারি ২০০৫) — "
                        "অত্যন্ত বিশাল রেঞ্জ (dry-season-এ প্রায় শূন্য, কারণ ব্যারাজ "
                        "পানি আটকে রাখে)। ২০২১-এর extreme flood-এ গজলডোবা থেকে "
                        "৫,৫০০ m³/s surplus release হয়েছিল।"
                    ),
                    "source": "Mondal & Islam 2017 (Jàmbá journal, Kaunia/Dalia 1985-2006 data); IWA Hydrology Research (2021 Teesta flash flood evaluation)",
                    "note": (
                        "⚠️ পুরনো buggy সূত্র (২৯৩১) থেকে নতুন অনুমান (৪০০০) — এবার "
                        "ব্যবধান মাত্র ~১.৪ গুণ, পদ্মা/যমুনার (৩৫-৯০ গুণ) তুলনায় অনেক "
                        "কম। এটা সিলেটের প্যাটার্নের সাথে মিলে যাচ্ছে — বড় danger_level "
                        "সংখ্যা (মিটারে) থাকা নদীতে crude সূত্র কম ভুল দেয়।"
                    ),
                    "confidence": "moderate — historical (2004-06) data, dry-season vs monsoon extreme পার্থক্য অনেক বড় হওয়ায় single reference discharge কম অর্থবহ",
                },
                "cn": {"old_value": 80, "reviewed_estimate": 83, "reasoning": "সামান্য বাড়ানো — উত্তরাঞ্চলের বেলে-দোআঁশ মাটি একটু কম CN হওয়ার কথা পদ্মার পলিমাটির চেয়ে, কিন্তু flashy runoff বিবেচনায় সামঞ্জস্য রাখা হলো", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (অপরিবর্তিত)",
                    "reasoning": "ইতিমধ্যে সঠিক — নিয়মিত danger crossing, embankment breach (Bonikbarta রিপোর্ট), ২০২১-এর extreme flash flood সবই 'উচ্চ' নিশ্চিত করে।",
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "⚠️ flood_config.py-তে flood_type='Riverine' লেখা আছে, কিন্তু "
                "লালমনিরহাটের (একই নদী, উজানে) flood_type='Dam-Affected' — "
                "একই নদীর দুই জেলায় দুই ভিন্ন classification। বাস্তবে Kaunia-ও "
                "গজলডোবা/Dalia ব্যারাজের release-এর উপর সমানভাবে নির্ভরশীল "
                "(উপরে দেখুন), তাই রংপুরকেও 'Dam-Affected' বা অন্তত একটা hybrid "
                "classification দেওয়া যুক্তিসঙ্গত হতে পারে।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "কাউনিয়া উপজেলার তিস্তা তীরবর্তী চরাঞ্চল",
                "50cm_to_1m_above_danger": "গঙ্গাচড়া উপজেলার নিম্নাঞ্চল",
                "above_1m_danger": "embankment breach হলে ব্যাপক প্লাবন (Bonikbarta রিপোর্টে বাঁধ ভাঙার উদাহরণ আছে)",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Badarganj",
            "ffwc_id": "SW62",
            "is_primary": False,

            "river": "যমুনেশ্বরী (Jamuneswari)",
            "upazila": "Taraganj",
            "union": None,

            "river_structure": {
                "category": "medium",
                "catchment": "তিস্তার একটা distributary/স্থানীয় শাখা নদী, রংপুরের ভেতর দিয়ে বয়ে যায়",
                "flow_behavior": "তিস্তার চেয়ে ছোট, স্থানীয় গুরুত্বপূর্ণ",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 31.70,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "flood_config.py-র সাথে মিলেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 3170, "corrected_estimate": 1500, "confidence": "low — নির্দিষ্ট data পাওয়া যায়নি, medium category অনুমান"},
                "cn": {"old_value": None, "reviewed_estimate": 83, "confidence": "low"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "তিস্তার তুলনায় কম critical, কিন্তু নির্দিষ্ট ইতিহাস খুঁজে পাওয়া যায়নি"},
            },

            "flood_type": "Riverine",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    "soil_moisture_weight_note": (
        "⚠️ তিস্তা সিস্টেমে discharge_ratio-র চেয়ে barrage gate status/release "
        "info বেশি গুরুত্বপূর্ণ predictor হওয়া উচিত (যা এখন model-এ নেই) — "
        "soil_moisture/rainfall কমানোর চেয়ে বরং 'dam release' একটা নতুন signal "
        "হিসেবে যোগ করা বেশি জরুরি এই নদীতে।"
    ),

    "confluence_note": "রংপুর CONFLUENCE_DISTRICTS-এ নেই — সম্পূর্ণ ভিন্ন নদী সিস্টেম (তিস্তা, ব্যারাজ-নিয়ন্ত্রিত)।",

    "cross_district_note": "এই গবেষণা লালমনিরহাট, নীলফামারী, কুড়িগ্রাম, গাইবান্ধার জন্য reuse করা যাবে — একই তিস্তা সিস্টেম।",
}