# ============================================================
# FloodAI — data/district_profiles/shariatpur.py
#
# জেলা-বাই-জেলা framework-এর ৫ম জেলা — এটা দিয়ে CONFLUENCE_DISTRICTS-এর
# ৫টা জেলাই (রাজবাড়ী, মানিকগঞ্জ, মুন্সিগঞ্জ, ফরিদপুর, শরীয়তপুর) সম্পূর্ণ হলো।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

SHARIATPUR_PROFILE = {
    "district": "শরীয়তপুর",
    "district_lat": 23.24,
    "district_lon": 90.35,

    "station_count": 1,

    "stations": [
        {
            "name": "Sureshswar",
            "ffwc_id": "SW95",
            "is_primary": True,

            "river": "পদ্মা (Padma)",
            "upazila": "Naria",
            "union": "Kedarpur",

            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "রাজবাড়ী→মানিকগঞ্জ→মুন্সিগঞ্জ হয়ে পদ্মা এখানে (Sureshswar/Naria) "
                    "আসছে, চাঁদপুরে মেঘনার সাথে মেশার ঠিক আগে — confluence chain-এর "
                    "সবচেয়ে ভাটির (downstream-most) জেলা।"
                ),
                "flow_behavior": "একই mega_trunk আচরণ, তবে এই reach-এ river bank খুবই সক্রিয় ও অস্থির (নিচে erosion দ্রষ্টব্য)",
                "upstream_reference": "Malda, IN",
                "lag_time_hours": 44,
            },

            "danger_level_m": 4.00,  # ✅ FFWC verify করা (SW95, ২০২৬-০৮-১০)
            "highest_recorded_m": 4.92,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 400,  # danger_level(4.0)*100
                    "corrected_estimate": 75000,  # bankfull (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত)
                    "corrected_range": "একই পদ্মা trunk — রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জের মতো mean ~৩০,০০০, bankfull ~৭৫,০০০ m³/s",
                    "source": "Neill et al. (Padma hydrotechnical features); Wikipedia Padma River — একই source, একই নদী",
                    "cross_check": "✅ river_categories.py mega_trunk রেঞ্জের মধ্যে",
                    "critical_caveat": "একই retrain/override সমস্যা প্রযোজ্য — এখন ৪টা confluence জেলাতেই একই ধরনের fix লাগবে",
                },
                "cn": {"old_value": 77, "reviewed_estimate": 89, "reasoning": "একই পদ্মা floodplain যুক্তি", "confidence": "moderate"},
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "শরীয়তপুর জাতীয় দুর্যোগ ব্যবস্থাপনা পরিকল্পনা (2010-15)-এ "
                        "cyclone+flood+riverbank erosion — তিনটা ঝুঁকিতেই তালিকাভুক্ত। "
                        "১৯৯৬, ২০১২, ২০১৯ সালে বড় বন্যা হয়েছে। ২০১৮ সালে নড়িয়া "
                        "উপজেলায় ভয়াবহ ভাঙনে ৫,০৮১টা পরিবার গৃহহীন হয়, সরকার "
                        "১০৭৭.৫৮ কোটি টাকার প্রতিরক্ষা প্রকল্প অনুমোদন করে। FFWC-র "
                        "২০২১ বার্ষিক রিপোর্ট অনুযায়ী সেই বছর Sureshswar-এ পদ্মা "
                        "টানা ৩৬ দিন danger level-এর উপরে ছিল — ওই বছরের অন্যতম "
                        "দীর্ঘতম। 'মাঝারি' স্পষ্টতই কম।"
                    ),
                    "source": (
                        "National Plan for Disaster Management 2010-15 (DMB); "
                        "FFWC Annual Flood Report 2021; Dhaka Tribune/Prothom Alo/"
                        "ReliefWeb (২০১৮ Naria erosion coverage); ResearchGate "
                        "(Naria riverbank erosion case studies)"
                    ),
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "ক্লাসিক পদ্মা riverine বন্যা + confluence chain-এর সবচেয়ে severe "
                "erosion-আক্রান্ত জেলা — নড়িয়া/জাজিরা উপজেলায় প্রতি বর্ষায় সক্রিয় "
                "নদীভাঙন, শুধু water-level danger না।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "নড়িয়া/জাজিরার সক্রিয় চর ও ভাঙন-এলাকা",
                "50cm_to_1m_above_danger": "শরীয়তপুর সদর, ভেদরগঞ্জের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৯৮/২০১৯ স্কেলে — জেলার বড় অংশ, বিশেষত নড়িয়া উপজেলা",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি (তবে erosion-hotspot নির্দিষ্টভাবে চিহ্নিত করা গেছে, যা অন্য জেলাগুলোর চেয়ে বেশি তথ্য)",
            },
        },
    ],

    "soil_moisture_weight_note": "একই পদ্মা trunk যুক্তি — discharge/water-level trend primary, soil moisture secondary।",

    "confluence_note": (
        "✅ এই জেলা দিয়ে CONFLUENCE_DISTRICTS-এর ৫টা জেলাই (রাজবাড়ী, মানিকগঞ্জ, "
        "মুন্সিগঞ্জ, ফরিদপুর, শরীয়তপুর) সম্পূর্ণ হলো। সারসংক্ষেপ:\n"
        "  - রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জ/শরীয়তপুর — ৪টাই সত্যিকারের পদ্মা/যমুনা "
        "trunk station, reference_discharge ~৩০,০০০-৫০,০০০ m³/s (পুরনো মান "
        "থেকে ৩৫-৯০ গুণ বেশি) — এখানে confluence override যৌক্তিক, শুধু সংখ্যা ভুল ছিল\n"
        "  - ফরিদপুর — ব্যতিক্রম, এই জেলার একমাত্র station (কুমার) পদ্মার সাথে "
        "সংযুক্তই না — confluence override-এর ভৌগোলিক ভিত্তিই দুর্বল এখানে"
    ),
}