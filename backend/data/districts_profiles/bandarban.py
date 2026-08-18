# ============================================================
# FloodAI — data/district_profiles/bandarban.py
#
# ১৬তম জেলা। চট্টগ্রাম পার্বত্য অঞ্চলের একমাত্র জেলা যেখানে stations.py-তে
# real FFWC station আছে (Rangamati ও Khagrachhari-তে নেই — দেখুন
# rangamati.py/khagrachhari.py-র বিস্তারিত ব্যাখ্যা)। আগের জেলাগুলোর
# সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

BANDARBAN_PROFILE = {
    "district": "বান্দরবান",
    "district_lat": 22.1953,
    "district_lon": 92.2184,

    "station_count": 2,

    "stations": [
        {
            "name": "Bandarban",
            "ffwc_id": "SW247",
            "is_primary": True,

            "river": "সাঙ্গু (Sangu)",
            "upazila": "Bandarban Sadar",
            "union": "Kuhalong",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "মিজোরাম (ভারত)-এর পাহাড় থেকে উৎপন্ন, বান্দরবান "
                    "জেলার মধ্য দিয়ে বয়ে চট্টগ্রামের Dohazari, "
                    "Chandanaish হয়ে বঙ্গোপসাগরে পড়ে। Banglapedia-তে "
                    "স্পষ্টভাবে 'flashy' নদী হিসেবে চিহ্নিত।"
                ),
                "flow_behavior": (
                    "⚠️ চরম flashy — জুলাই ২০২৬-এ এই station-এ ২৪ ঘণ্টায় "
                    "৩৪৮ সেমি জলস্তর বৃদ্ধি রেকর্ড হয়েছে, danger level-এর "
                    "১৯০ সেমি উপরে উঠেছিল। highest_recorded (20.34m) "
                    "danger_level-এর (14.80m) প্রায় ৫.৫ মিটার উপরে — এই "
                    "প্রজেক্টের সবচেয়ে বড় absolute margin।"
                ),
                "upstream_reference": "Mizoram, IN",
                "lag_time_hours": 5,  # flood_config.py অনুযায়ী
            },

            "danger_level_m": 14.80,  # ✅ FFWC verify করা
            "highest_recorded_m": 20.34,
            "verified_source": "old.ffwc.gov.bd, Daily Star/bdnews24/Dhaka Tribune (জুলাই ২০২৬ বন্যা প্রতিবেদন), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Bandarban Sadar/Kuhalong) "
                "সব মিলে গেছে ✅ — flood_config.py-তে আগে থেকেই "
                "'ffwc_verified: True' চিহ্নিত ছিল, এবার independent "
                "verification-এও নিশ্চিত হলো। coordinate ভালো — "
                "stations.py lat=22.20,lon=92.20 বনাম Wikipedia-র "
                "Bandarban Sadar কেন্দ্র lat=22.233,lon=92.192 — সামান্য "
                "পার্থক্য, গ্রহণযোগ্য।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1480,
                    "corrected_estimate": 600,
                    "corrected_range": (
                        "নির্দিষ্ট measured mean discharge পাওয়া যায়নি, "
                        "কিন্তু চরম flash-flood আচরণ (২৪ ঘণ্টায় ৩৪৮ সেমি "
                        "বৃদ্ধি) বিবেচনায় river_categories.py-র 'medium' "
                        "রেঞ্জের উপরের দিকে ধরা হলো peak flow-এর জন্য।"
                    ),
                    "source": "Banglapedia (Chittagong Region River System); FFWC bulletin (জুলাই ২০২৬)",
                    "confidence": "low — normal-flow figure পাওয়া যায়নি, flash-flood event থেকে qualitative অনুমান",
                },
                "cn": {"old_value": 88, "reviewed_estimate": 87, "reasoning": "flood_config.py-র বিদ্যমান মান (৮৮) মোটামুটি যুক্তিসঙ্গত — পাহাড়ি, দ্রুত-runoff floodplain", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "অতি উচ্চ",
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": (
                        "flood_config.py-র বিদ্যমান 'অতি উচ্চ' রেটিং সম্পূর্ণ "
                        "সমর্থিত — এই প্রজেক্টের সবচেয়ে বড় margin "
                        "(highest_recorded - danger_level = ৫.৫৪ মিটার) "
                        "এবং সাম্প্রতিক (২০২৬) একাধিক চরম ঘটনা।"
                    ),
                    "source": "FFWC bulletins (জুলাই ২০২৬, একাধিকবার danger level ছাড়িয়েছে)",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "flood_config.py-র বিদ্যমান 'Flash Flood' ট্যাগ সম্পূর্ণ সঠিক ও সুপ্রতিষ্ঠিত — মিজোরামের পাহাড়ি ঢল দ্রুত নেমে আসে।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "বান্দরবান সদর, রুমা, রোয়াংছড়ি উপজেলার নদী-তীরবর্তী নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "লামা, আলীকদমের সংলগ্ন এলাকা",
                "above_1m_danger": "২০২৬-এর মতো চরম ইভেন্টে — বান্দরবান শহরের নিচু অংশ সম্পূর্ণ প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Lama",
            "ffwc_id": "SW203",
            "is_primary": False,

            "river": "মাতামুহুরী (Matamuhuri)",
            "upazila": "Lama",
            "union": None,

            "river_structure": {
                "category": "medium",
                "catchment": "একই মিজোরাম পাহাড় থেকে উৎপন্ন, বান্দরবানের দক্ষিণ দিয়ে Cox's Bazar-এর Chiringa হয়ে বঙ্গোপসাগরে পড়ে।",
                "flow_behavior": "একই flashy চরিত্র, Sangu-র মতোই — জুলাই ২০২৬-এ ১৭৩ সেমি/দিন বৃদ্ধির রেকর্ড।",
                "upstream_reference": "Mizoram, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 11.80,  # ✅ FFWC verify করা
            "highest_recorded_m": 14.92,
            "verified_source": "old.ffwc.gov.bd, FFWC bulletins (জুলাই ২০২৬), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila (Lama) মিলে গেছে ✅। coordinate "
                "ভালো — stations.py lat=21.82,lon=92.22 বনাম Wikipedia-র "
                "Lama শহর কেন্দ্র lat=21.7775,lon=92.195 — প্রায় ৫-৬ কিমি "
                "পার্থক্য, গ্রহণযোগ্য।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1180,
                    "corrected_estimate": 400,
                    "corrected_range": "Sangu-র কাছাকাছি রেঞ্জ, সামান্য ছোট নদী",
                    "source": "Banglapedia; FFWC bulletin (জুলাই ২০২৬)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "একই পাহাড়ি floodplain", "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Sangu-র মতোই flashy, তবে margin (৩.১২ মি) সামান্য কম"},
            },

            "flood_type": "Flash Flood (correlated with Sangu — একই বৃষ্টি-ইভেন্টে একসাথে ওঠে)",
            "flood_type_note": "সাম্প্রতিক FFWC bulletin-এ Sangu (Bandarban) ও Matamuhuri (Lama) বারবার একসাথে danger level cross করতে দেখা গেছে — correlated signal।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    "soil_moisture_weight_note": (
        "উভয় station-এর জন্য মিজোরামের upstream rainfall-ই প্রধান "
        "predictor, স্থানীয় soil moisture-এর ভূমিকা সীমিত — Habiganj-এর "
        "Khowai বা Netrokona-র Someswari-র মতোই যুক্তি, সম্ভবত আরও বেশি "
        "flashy (২৪ ঘণ্টায় ৩৪৮ সেমি বৃদ্ধির রেকর্ড এই প্রজেক্টের সর্বোচ্চ)।"
    ),

    "confluence_note": (
        "বান্দরবান চট্টগ্রাম পার্বত্য অঞ্চলের flashy-hill-river cluster-এর "
        "একটা সুপ্রতিষ্ঠিত সদস্য (flood_config.py-তে আগে থেকেই "
        "ffwc_verified: True ছিল)। কিন্তু Rangamati ও Khagrachhari — "
        "এই একই cluster-এর অন্য দুই জেলা — সম্পূর্ণ ভিন্ন পরিস্থিতিতে "
        "আছে (কোনো real station নেই, দেখুন rangamati.py/"
        "khagrachhari.py)।"
    ),

    "cross_district_flags": (
        "কোনো নতুন conflict পাওয়া যায়নি — এটা flood_config.py-র "
        "ইতিমধ্যে-verified তথ্যকে independent সোর্স দিয়ে re-confirm "
        "করেছে মাত্র।"
    ),
}