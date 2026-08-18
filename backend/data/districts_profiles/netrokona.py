# ============================================================
# FloodAI — data/district_profiles/netrokona.py
#
# ১১তম জেলা। Habiganj-এর মতোই meghalaya/Garo Hills থেকে নেমে আসা
# transboundary নদী এবং হাওর সিস্টেমের জেলা। আগের জেলাগুলোর সাথে হুবহু
# একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ Coordinate যা পাওয়া গেছে (সবগুলো danger_level ঠিক ছিল):
#   1. Bijoypur — ~১৩-১৪ কিমি off
#   2. Durgapur — ~৭ কিমি off
#   3. Kalmakanda — ~৩-৪ কিমি off (নগণ্য)
#   4. Jariajanjail — নির্দিষ্ট BWDB survey coordinate পাওয়া যায়নি,
#      FFWC live upazila/union নিশ্চিত করেছে
#   5. Khaliajuri — ~৭ কিমি off
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NETROKONA_PROFILE = {
    "district": "নেত্রকোণা",
    "district_lat": 24.8802,
    "district_lon": 90.7276,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # stations.py অনুযায়ী ৫টা (Bijoypur, Durgapur — দুটোই Someswari;
    # Kalmakanda — Someswari; Jariajanjail — Kangsha; Khaliajuri — Dhanu)।
    "station_count": 5,

    "stations": [
        {
            "name": "Bijoypur",
            "ffwc_id": "SW262",
            "is_primary": True,

            "river": "সোমেশ্বরী (Someswari)",
            "upazila": "Durgapur",
            "union": "Kullagora",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "মেঘালয়ের Nokrek পাহাড় (Garo Hills) থেকে উৎপন্ন, "
                    "ভারতে 'Simsang' নামে পরিচিত — মেঘালয়ের বৃহত্তম নদী। "
                    "বাংলাদেশে প্রবেশ করে Durgapur উপজেলা দিয়ে (Bijoypur, "
                    "এই station-এর এলাকা কয়লা ও চীনামাটির খনির জন্য "
                    "বিখ্যাত), পরে দক্ষিণে গিয়ে Kangsha নদীতে মেশে।"
                ),
                "flow_behavior": (
                    "flashy পাহাড়ি চরিত্র — মেঘালয়ের ভারী বৃষ্টি (বিশ্বের "
                    "সর্বোচ্চ বৃষ্টিপাতের অঞ্চলগুলোর একটা, Cherrapunji "
                    "এই একই পাহাড়শ্রেণীতে) দ্রুত নেমে আসে। FFWC-র Flash "
                    "Flood Early Warning System-এ Bijoypur আলাদাভাবে "
                    "তালিকাভুক্ত।"
                ),
                "upstream_reference": "Tura/Garo Hills, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 13.20,  # ✅ FFWC verify করা
            "highest_recorded_m": 17.55,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Durgapur/Kullagora) সব "
                "মিলে গেছে ✅। coordinate off ছিল — stations.py "
                "lat=25.05,lon=90.75 বনাম BWDB official lat=25.1720,"
                "lon=90.6593 — প্রায় ১৩-১৪ কিমি উত্তর-পশ্চিমে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1320,
                    "corrected_estimate": 600,
                    "corrected_range": "নির্দিষ্ট measured figure পাওয়া যায়নি, মেঘালয়ের বৃহত্তম নদী হিসেবে river_categories.py-র 'medium' রেঞ্জের উপরের দিকে ধরা যুক্তিসঙ্গত, flash-flood ইভেন্টে অনেক বেশি হতে পারে",
                    "source": "Wikipedia (Someshwari River, Simsang River)",
                    "confidence": "low — নির্দিষ্ট discharge সংখ্যা পাওয়া যায়নি",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "পাহাড়ি-সংলগ্ন floodplain, দ্রুত runoff", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "মেঘালয়ের অত্যন্ত ভারী বৃষ্টিপাতের (বিশ্বের সর্বোচ্চ অঞ্চলগুলোর একটা) সরাসরি downstream, flash-flood আশঙ্কা বেশি। highest_recorded (17.55m) danger_level-এর ৪.৩৫মি উপরে — উল্লেখযোগ্য ব্যবধান।",
                    "source": "Wikipedia; FFWC Flash Flood Early Warning System listing",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "Habiganj-এর Khowai station-এর ঠিক একই যুক্তি — মেঘালয়ের ভারী বৃষ্টি ও পাহাড়ি ঢল দ্রুত নেমে আসে, classic riverine না।",

            "inundation_bands": {
                "0_to_50cm_above_danger": "দুর্গাপুর উপজেলার সীমান্তবর্তী নিম্নাঞ্চল",
                "50cm_to_1m_above_danger": "কলমাকান্দার সংলগ্ন এলাকা",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — সীমান্তবর্তী বিস্তৃত এলাকা প্লাবিত",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি",
            },
        },
        {
            "name": "Durgapur",
            "ffwc_id": "SW263",
            "is_primary": False,

            "river": "সোমেশ্বরী (Someswari)",
            "upazila": "Durgapur",
            "union": None,

            "river_structure": {
                "category": "medium",
                "catchment": "একই সোমেশ্বরী, Bijoypur-এর সামান্য downstream, দুর্গাপুর উপজেলা সদরের কাছে।",
                "flow_behavior": "একই flashy চরিত্র।",
                "upstream_reference": "Tura/Garo Hills, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 12.55,  # ✅ FFWC verify করা
            "highest_recorded_m": None,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": "danger_level, upazila (Durgapur) মিলে গেছে ✅। coordinate off ছিল — stations.py lat=25.05,lon=90.68 বনাম BWDB official lat=25.1139,lon=90.6705 — প্রায় ৭ কিমি উত্তরে সরাতে হবে।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1255,
                    "corrected_estimate": 550,
                    "corrected_range": "Bijoypur-এর কাছাকাছি রেঞ্জ, একই নদীর downstream পয়েন্ট",
                    "source": "Wikipedia (Someshwari River) — Bijoypur-এর সাথে সামঞ্জস্যপূর্ণ",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "একই floodplain", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "Bijoypur-এর মতোই যুক্তি"},
            },

            "flood_type": "Flash Flood (correlated with Bijoypur — একই নদী, কাছাকাছি পয়েন্ট)",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Kalmakanda",
            "ffwc_id": "SW263.1",
            "is_primary": False,

            "river": "সোমেশ্বরী (Someswari)",
            "upazila": "Kalmakanda",
            "union": "Kalmakanda",

            "river_structure": {
                "category": "medium",
                "catchment": "সোমেশ্বরীর একটা শাখা — Kalmakanda উপজেলার দিকে গিয়ে বালিয়া নদীর সাথে মেশে।",
                "flow_behavior": "একই flashy চরিত্র, তবে ছোট শাখা।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 6.55,  # ✅ FFWC verify করা
            "highest_recorded_m": 12.60,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Kalmakanda) মিলে গেছে ✅। "
                "coordinate ভালো — stations.py lat=25.06,lon=90.86 বনাম "
                "BWDB official lat=25.0767,lon=90.8948 — মাত্র ~৩-৪ কিমি "
                "পার্থক্য, নগণ্য। উল্লেখযোগ্য: highest_recorded (12.60m) "
                "danger_level-এর প্রায় দ্বিগুণ (৬.০৫ মিটার বেশি) — এই "
                "প্রজেক্টের সবচেয়ে বড় margin, চরম flashy আচরণের ইঙ্গিত।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 655,
                    "corrected_estimate": 300,
                    "corrected_range": "সোমেশ্বরীর শাখা, Bijoypur/Durgapur-এর চেয়ে ছোট",
                    "source": "Wikipedia (Someshwari River — branch toward Kalmakanda)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "একই floodplain", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "danger_level-এর প্রায় দ্বিগুণ পর্যন্ত জলস্তর ওঠার রেকর্ড আছে — চরম flash-flood ঝুঁকি, ছোট নদী হলেও অবহেলা করা ঠিক না।",
                    "source": "FFWC data (highest_recorded vs danger_level margin)",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "সবচেয়ে চরম flash-flood margin এই জেলায় (highest_recorded প্রায় ডাবল danger_level) — বিশেষ নজর দরকার।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Jariajanjail",
            "ffwc_id": "SW36",
            "is_primary": False,

            "river": "কংস (Kangsha)",
            "upazila": "Durgapur",
            "union": "Kakairgara",

            "river_structure": {
                "category": "medium",
                "catchment": (
                    "মেঘালয়ের Garo Hills থেকে 'Bhogai' নামে উৎপন্ন হয়ে "
                    "Nalitabari (শেরপুর) পার হয়ে নেত্রকোণায় প্রবেশ করে "
                    "'কংস' নাম নেয়। Barhatta, Mohanganj, Dharampasha "
                    "উপজেলা দিয়ে বয়ে গিয়ে Sunamganj-এ সুরমা নদীতে মেশে। "
                    "সোমেশ্বরী এই নদীতেই এসে মেশে।"
                ),
                "flow_behavior": "মেঘালয়/Garo Hills থেকে আসা সব পাহাড়ি ঢলের মূল সংগ্রহকারী নদী — 'সব বন্যার পানি Garo/Meghalaya পাহাড় থেকে আসে' (wetland protection report অনুযায়ী)।",
                "upstream_reference": "Tura/Garo Hills, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 10.55,  # ✅ FFWC verify করা
            "highest_recorded_m": 11.08,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Durgapur/Kakairgara) FFWC "
                "live current-এ মিলে গেছে ✅। BWDB-র official hydrology "
                "survey table-এ এই নির্দিষ্ট SW36 station খুঁজে পাওয়া "
                "যায়নি (তালিকায় SW36.1 Mohanganj, ভিন্ন station, পাওয়া "
                "গেছে) — coordinate independent verify করা যায়নি, "
                "stations.py-র মান (lat=24.98,lon=90.68) FFWC-র upazila "
                "তথ্যের সাথে ভৌগোলিকভাবে সামঞ্জস্যপূর্ণ মনে হচ্ছে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1055,
                    "corrected_estimate": 800,
                    "corrected_range": "সোমেশ্বরী+মূল Bhogai-Kangsha প্রবাহের সমন্বিত অংশ, Bijoypur-এর চেয়ে কিছুটা বেশি হওয়া উচিত (tributary যোগ হওয়ায়)",
                    "source": "Wikipedia (Kangsha River)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "একই floodplain", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": "মেঘালয়ের সব পাহাড়ি ঢলের সংগ্রহ-বিন্দু হওয়ায় সমন্বিত ঝুঁকি বেশি, একাধিক upstream tributary (Someswari সহ)-র প্রভাব এখানে জমা হয়।",
                    "source": "Wetland protection report (Wikipedia-তে উদ্ধৃত)",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "সোমেশ্বরীর মূল receiving নদী — upstream-এর সবগুলো flash-flood station-এর (Bijoypur, Durgapur, Kalmakanda) সম্মিলিত প্রভাব এখানে প্রতিফলিত হয়, correlated signal।",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
        {
            "name": "Khaliajuri",
            "ffwc_id": "SW72",
            "is_primary": False,

            "river": "ধনু (Dhanu)",
            "upazila": "Khaliajuri",
            "union": "Chakua",

            "river_structure": {
                "category": "large_regional",
                "catchment": (
                    "কংস নদীর শাখা, Kishoreganj জেলার দিকে প্রবাহিত হয়ে "
                    "Baulai-Ghoratura নাম নিয়ে হাওর অঞ্চলে বিস্তৃত হয়। "
                    "BWDB-র নিজস্ব ডেটায় 'Tidal' হিসেবে চিহ্নিত — Habiganj-"
                    "এর Markuli-র মতোই জোয়ারের প্রভাব এই অভ্যন্তরীণ "
                    "অঞ্চলেও পৌঁছায়।"
                ),
                "flow_behavior": "হাওর-অধ্যুষিত এলাকা, বর্ষায় বিশাল জলাশয়ে পরিণত হয়, শীতে সংকুচিত।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 6.55,  # ✅ FFWC verify করা
            "highest_recorded_m": 8.96,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": "danger_level, upazila (Khaliajuri) মিলে গেছে ✅। coordinate off ছিল — stations.py lat=24.75,lon=91.10 বনাম BWDB official lat=24.6877,lon=91.1348 — প্রায় ৭ কিমি দক্ষিণ-পূর্বে সরাতে হবে।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 655,
                    "corrected_estimate": 2000,
                    "corrected_range": "উজানের একাধিক নদীর (Kangsha, Someswari, ইত্যাদি) সম্মিলিত হাওর-প্রবাহ, নির্দিষ্ট figure পাওয়া যায়নি",
                    "source": "Wikipedia (Kangsha River — Dhanu/Dhala branches)",
                    "confidence": "low",
                },
                "cn": {"old_value": None, "reviewed_estimate": 86, "reasoning": "হাওর wetland buffer, কম CN যুক্তিসঙ্গত", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি-উচ্চ", "reasoning": "হাওর buffer থাকলেও upstream flash-flood-এর সম্মিলিত প্রভাব এখানে জমা হয়, Habiganj-এর Markuli-র মতোই যুক্তি"},
            },

            "flood_type": "Riverine (হাওর-buffered, upstream flash-flood-এর correlated downstream signal)",
            "flood_type_note": "Habiganj-এর Markuli station-এর ঠিক একই ধরনের ভূমিকা — উজানের flashy tributary-দের প্রভাব হাওরে জমা হয়ে একটা তুলনামূলক ধীরগতির signal তৈরি করে।",
            "inundation_bands": {"status": "⚠️ placeholder — হাওর dynamics-এর কারণে সাধারণ river inundation model কম প্রাসঙ্গিক"},
        },
    ],

    "soil_moisture_weight_note": (
        "সোমেশ্বরী/কংস station-গুলোর (Bijoypur, Durgapur, Kalmakanda, "
        "Jariajanjail) জন্য স্থানীয় rainfall/soil moisture-এর চেয়ে upstream "
        "মেঘালয়ের বৃষ্টির signal অনেক বেশি গুরুত্বপূর্ণ — Habiganj-এর "
        "Khowai-র মতোই যুক্তি, কিন্তু হয়তো আরও flashy (Kalmakanda-র "
        "highest_recorded/danger_level ratio এই প্রজেক্টের সর্বোচ্চ)। "
        "Khaliajuri (ধনু)-এর জন্য হাওর buffer থাকায় soil moisture কম "
        "প্রাসঙ্গিক, upstream tributary trend বেশি গুরুত্বপূর্ণ predictor।"
    ),

    "confluence_note": (
        "নেত্রকোণা Habiganj-এর সুরমা-মেঘনা/হাওর cluster-এর সাথে যুক্ত হলো — "
        "কিন্তু ভিন্ন উপ-অঞ্চল (মেঘালয়ের Garo Hills-fed সোমেশ্বরী-কংস "
        "সিস্টেম, ত্রিপুরা-fed Khowai-র বদলে)। দুইটাই একই বড় প্যাটার্নের "
        "অংশ — ভারতীয় পাহাড় থেকে flashy runoff + হাওর buffer + downstream "
        "সুরমা-মেঘনা। ভবিষ্যতে Sunamganj, Sylhet, Moulvibazar, Kishoreganj "
        "যোগ হলে পুরো উত্তর-পূর্ব হাওর/flash-flood অঞ্চলের একটা সম্পূর্ণ "
        "picture তৈরি হবে।"
    ),

    "cross_district_flags": (
        "⚠️ Kalmakanda station-এর highest_recorded/danger_level ratio "
        "(প্রায় ২x) এই ৯টা জেলার (Habiganj সহ) মধ্যে সবচেয়ে চরম flash-flood "
        "margin — ভবিষ্যতে flash-flood risk-scoring তৈরি করলে এই ratio-টা "
        "একটা useful feature হতে পারে, শুধু danger_level-এর absolute "
        "distance না।"
    ),
}