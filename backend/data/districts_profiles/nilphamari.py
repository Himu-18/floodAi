# ============================================================
# FloodAI — data/district_profiles/nilphamari.py
#
# ২০তম জেলা। এই প্রজেক্টে তিস্তা নদীর ২য় station (প্রথমটা Gaibandha-র
# Haripur, তিস্তার মোহনার কাছে; এটা Dalia, তিস্তা বাংলাদেশে প্রবেশ করার
# পয়েন্টের কাছাকাছি — তিস্তা ব্যারেজের ঠিক downstream)। আগের জেলাগুলোর
# সাথে হুবহু একই ৭-ধাপ পদ্ধতি।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

NILPHAMARI_PROFILE = {
    "district": "নীলফামারী",
    "district_lat": 25.9315,
    "district_lon": 88.8560,

    "station_count": 1,

    "stations": [
        {
            "name": "Dalia",
            "ffwc_id": "SW291.5R",
            "is_primary": True,

            "river": "তিস্তা (Teesta)",
            "upazila": "Dimla",
            "union": "Khalisa Chapani",

            "river_structure": {
                "category": "medium",  # Gaibandha-র Haripur profile-এও একই ক্যাটেগরি ধরা হয়েছিল
                "catchment": (
                    "সিকিম হিমালয়ের Tso Lhamo হিমবাহ থেকে উৎপন্ন, "
                    "নীলফামারীর Dalia পয়েন্টেই বাংলাদেশ তিস্তা ব্যারেজ "
                    "(Teesta Barrage) অবস্থিত — বাংলাদেশের বৃহত্তম "
                    "সেচ প্রকল্প (Teesta Barrage Irrigation Project)। "
                    "এই station ব্যারেজের ঠিক downstream-এ, তাই এখানকার "
                    "জলস্তর সরাসরি ব্যারেজের গেট-নিয়ন্ত্রণের ওপর "
                    "নির্ভরশীল — Gaibandha-র Haripur (মোহনার কাছে, আরও "
                    "downstream)-এর চেয়ে বাঁধ-প্রভাব এখানে আরও বেশি "
                    "প্রত্যক্ষ।"
                ),
                "flow_behavior": (
                    "⚠️ দ্বিমুখী নিয়ন্ত্রণ — উজানে ভারতের Gajaldoba "
                    "ব্যারেজ (dry season-এ পানি আটকায়) এবং এই স্থানেই "
                    "বাংলাদেশের নিজস্ব তিস্তা ব্যারেজ (সেচের জন্য পানি "
                    "সরায়) — দুইটা বাঁধ/ব্যারেজের মাঝে অবস্থিত এই station। "
                    "danger_level margin (highest_recorded - danger_level "
                    "= মাত্র ০.৭৫ মি) এই batch-এর মধ্যে সবচেয়ে ছোট, যা "
                    "barrage-নিয়ন্ত্রণের tight-band আচরণের ইঙ্গিত দিতে পারে।"
                ),
                "upstream_reference": "Jalpaiguri, IN",
                "lag_time_hours": None,
            },

            "danger_level_m": 52.15,  # ✅ FFWC verify করা
            "highest_recorded_m": 52.90,
            "verified_source": "old.ffwc.gov.bd, FFWC Annual Flood Report (নিয়মিত tracked), যাচাই করা হয়েছে ২০২৬-০৮-১২",
            "verification_note": (
                "danger_level, upazila/union (Dimla/Khalisa Chapani) "
                "সব মিলে গেছে ✅। coordinate ভালো — stations.py "
                "lat=25.92,lon=88.96 বনাম FFWC-র বিভিন্ন সোর্স থেকে "
                "সামঞ্জস্যপূর্ণ। 'Teesta at Dalia' FFWC-র Annual Flood "
                "Report-এ সবসময় সবার প্রথমে (Figure 3.2) উল্লেখ করা হয় — "
                "জাতীয়ভাবে সবচেয়ে গুরুত্বপূর্ণ monitored point-গুলোর একটা। "
                "২০২১-এর report-এ ১৮-২২ অক্টোবরের একটা বিস্তারিত hydrograph "
                "case-study-ও আছে এই station নিয়ে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 5215,
                    "corrected_estimate": None,
                    "corrected_range": (
                        "Gaibandha-র Haripur profile-এ যেমন আলোচিত — "
                        "dry-season vs wet-season discharge-এ বিরাট "
                        "পার্থক্য, এবং এখানে barrage-নিয়ন্ত্রণ আরও প্রত্যক্ষ "
                        "(এই station-ই বাংলাদেশ ব্যারেজের downstream)। "
                        "একটা single reference_discharge সংখ্যা পুরো বছর "
                        "capture করতে পারবে না।"
                    ),
                    "source": "N/A — কাঠামোগত সমস্যা, Gaibandha profile-এর সাথে সামঞ্জস্যপূর্ণ",
                    "confidence": "N/A",
                    "critical_caveat": (
                        "⚠️ Dalia ও Haripur (Gaibandha) — তিস্তার দুইটা "
                        "station একসাথে বিবেচনা করলে ভবিষ্যতে একটা "
                        "dedicated 'barrage-controlled river' model "
                        "তৈরি করা যেতে পারে, যেখানে barrage gate-status "
                        "(যদি পাওয়া যায়) বা অন্তত upstream Gajaldoba "
                        "discharge trend feature হিসেবে যোগ করা যায়।"
                    ),
                },
                "cn": {"old_value": None, "reviewed_estimate": None, "reasoning": "barrage-নিয়ন্ত্রিত flow-এর জন্য rainfall-runoff CN সরাসরি প্রযোজ্য না", "confidence": "N/A"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "যদিও margin ছোট, তিস্তা ব্যারেজ এলাকা জনবহুল ও "
                        "কৃষি-নির্ভর (সেচ প্রকল্প), এবং উজানে বৃষ্টি/হিমবাহ-"
                        "গলন হঠাৎ বৃদ্ধি পেলে ব্যারেজ গেট খোলার কারণে "
                        "downstream-এ আকস্মিক নিঃসরণ বন্যা হতে পারে — "
                        "Rangamati/Kaptai profile-এ আলোচিত একই ধরনের "
                        "dam-release ঝুঁকি এখানেও প্রাসঙ্গিক।"
                    ),
                    "source": "FFWC Annual Flood Report (২০২১ Dalia case study)",
                },
            },

            "flood_type": "Dam-Affected / Riverine (hybrid — Gajaldoba+তিস্তা ব্যারেজ উভয়ের প্রভাব)",
            "flood_type_note": (
                "⚠️ Rangamati-প্রোফাইলে যে dam_affected.py module-এর "
                "কথা বলেছিলাম, Dalia সেই module-এর জন্য Rangamati-র "
                "চেয়েও বেশি সরাসরি প্রার্থী হতে পারে — কারণ এখানে "
                "সরাসরি একটা BWDB-পরিচালিত ব্যারেজ আছে (Kaptai-র মতো "
                "hydropower dam না হলেও, flow-regulation-এর দিক থেকে "
                "একই নীতি প্রযোজ্য) এবং প্রকৃত FFWC station data-ও "
                "বিদ্যমান — যেটা Rangamati-তে নেই। এই station "
                "dam_affected.py module test/calibrate করার জন্য "
                "সবচেয়ে ভালো candidate হতে পারে।"
            ),

            "inundation_bands": {"status": "⚠️ placeholder — barrage-নিয়ন্ত্রিত flow, সাধারণ rainfall-driven model কম প্রাসঙ্গিক"},
        },
    ],

    "soil_moisture_weight_note": (
        "Gaibandha-র Haripur profile-এর ঠিক একই যুক্তি, কিন্তু আরও "
        "জোরালোভাবে — এই station দুইটা বাঁধ/ব্যারেজের (Gajaldoba + "
        "বাংলাদেশ তিস্তা ব্যারেজ) মাঝে থাকায় স্থানীয় rainfall/soil "
        "moisture-এর prognostic value প্রায় শূন্য। gate-operation data "
        "(যদি পাওয়া যায়) সবচেয়ে গুরুত্বপূর্ণ predictor হবে।"
    ),

    "confluence_note": (
        "নীলফামারী (Dalia, ব্যারেজের downstream) ও Gaibandha (Haripur, "
        "মোহনার কাছে) — তিস্তার দুই প্রান্ত এখন এই প্রজেক্টে আছে। এই "
        "দুইটা মিলিয়ে তিস্তার পুরো বাংলাদেশ-যাত্রার একটা upstream-to-"
        "confluence picture তৈরি হচ্ছে, ঠিক যেভাবে যমুনা-করিডোরের জন্য "
        "হয়েছিল।"
    ),

    "cross_district_flags": (
        "কোনো coordinate/administrative conflict পাওয়া যায়নি। মূল "
        "finding হলো flood_type reassessment সুযোগ — dam_affected.py "
        "module-এর জন্য একটা ভালো real-data candidate পাওয়া গেছে।"
    ),
}