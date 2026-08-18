# ============================================================
# FloodAI — data/district_profiles/habiganj.py
#
# জেলা-বাই-জেলা framework-এর ৯ম জেলা। প্রথমবার Surma-Meghna/হাওর
# বেসিন-এর একটা জেলা এই প্রজেক্টে যুক্ত হলো — এখন পর্যন্ত সব ক'টা জেলা
# ছিল যমুনা-ব্রহ্মপুত্র করিডোরের অংশ।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

HABIGANJ_PROFILE = {
    "district": "হবিগঞ্জ",
    "district_lat": 24.3745,
    "district_lon": 91.4155,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 2,

    "stations": [
        {
            "name": "Habiganj",
            "ffwc_id": "SW159",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "খোয়াই (Khowai)",
            "upazila": "Baniachong (stations.py) — ⚠️ FFWC live current data বলছে upazila 'Habiganj Sadar'-এর কাছাকাছি হওয়া উচিত (নদীটা হবিগঞ্জ শহর ঘেঁষে যায়), FFWC live-এ union 'Umednagar' দেওয়া আছে",
            "union": "Umednagar",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "medium",  # flashy transboundary hill river
                "catchment": (
                    "ত্রিপুরার Atharamura পাহাড় থেকে উৎপন্ন, মোট দৈর্ঘ্য "
                    "১৬৬ কিমি (ত্রিপুরার ২য় দীর্ঘতম নদী)। Balla (হবিগঞ্জ) "
                    "দিয়ে বাংলাদেশে প্রবেশ করে, হবিগঞ্জ শহরের পূর্ব দিক "
                    "ঘেঁষে বয়ে Lakhai উপজেলার Adampur-এ কুশিয়ারার সাথে মেশে।"
                ),
                "flow_behavior": (
                    "সম্পূর্ণ flashy, transboundary পাহাড়ি নদী — ২০২৪ সালের "
                    "বন্যায় ২৪ ঘণ্টায় ৩১৫ সেমি পানি বেড়েছিল, all-time রেকর্ড "
                    "জলস্তর (১০.৯৫মি) স্পর্শ করেছিল ২০২৬-এর এক বন্যায় (আগের "
                    "রেকর্ড ২০১৭ সালে ১০.৯৩মি ছিল)। দূষণ ও দখলে নদীটা চাপে আছে "
                    "হবিগঞ্জ শহরের কাছে।"
                ),
                "upstream_reference": "Tripura, IN",
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 9.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 10.95,  # ২০২৬-এর বন্যায় নতুন রেকর্ড, আগের ১০.৯৩(২০১৭)-কে ছাড়িয়ে
            "verified_source": "old.ffwc.gov.bd, New Age BD (বন্যা রিপোর্ট), যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level ঠিক আছে। coordinate off ছিল — stations.py-তে "
                "lat=24.53, lon=91.30, BWDB official survey অনুযায়ী "
                "lat=24.3681, lon=91.4277 — প্রায় ১৯ কিমি দক্ষিণ-পূর্বে "
                "সরাতে হবে। highest_recorded_m stations.py-তে নেই, "
                "২০২৬-এর সাম্প্রতিক news অনুযায়ী নতুন রেকর্ড (১০.৯৫মি) "
                "আপডেট করা হলো।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 905,
                    "corrected_estimate": 600,
                    "corrected_range": "নির্দিষ্ট measured discharge পাওয়া যায়নি, কিন্তু ২৪ ঘণ্টায় ৩১৫ সেমি জলস্তর বৃদ্ধি অত্যন্ত flashy চরিত্র নির্দেশ করে — river_categories.py-র 'medium' রেঞ্জের উপরের দিকে ধরা হলো",
                    "source": "Banglapedia (Khowai River); New Age BD (২০২৪ বন্যা রিপোর্ট)",
                    "confidence": "low-moderate",
                },
                "cn": {"old_value": None, "reviewed_estimate": 87, "reasoning": "সিলেট বেসিনের floodplain, flashy hill-river হওয়ায় standard floodplain CN আংশিক প্রযোজ্য", "confidence": "low"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "অতি উচ্চ",
                    "reasoning": "২০২৬-এ all-time রেকর্ড জলস্তর স্পর্শ করেছে, ২৪ ঘণ্টায় ৩১৫ সেমি বৃদ্ধি — এই প্রজেক্টের সবচেয়ে flashy নদীগুলোর একটা।",
                    "source": "New Age BD (২০২৪ বন্যা রিপোর্ট); FFWC bulletin",
                },
            },

            "flood_type": "Flash Flood",
            "flood_type_note": "ত্রিপুরার পাহাড় থেকে আসা classic flash flood — Kurigram-এর Dharla/Dudhkumar বা Gaibandha-র তিস্তার মতোই দ্রুত ও predict করা কঠিন, কিন্তু বৃষ্টি-নির্ভর (barrage-নিয়ন্ত্রিত না)।",

            "inundation_bands": {"status": "⚠️ placeholder — নেই, flashy river হওয়ায় সাধারণ inundation-band পদ্ধতি কম নির্ভরযোগ্য"},
        },
        {
            "name": "Markuli",
            "ffwc_id": "SW270",
            "is_primary": False,

            "river": "সুরমা-মেঘনা (Surma-Meghna)",
            "upazila": "Baniachong (stations.py) — FFWC live current-এ 'Banyachong' বানানে, একই",
            "union": "Kulanj",

            "river_structure": {
                "category": "mega_trunk",  # সুরমা-কুশিয়ারা মিলিত হয়ে মেঘনা গঠন করে এই বিন্দুর কাছেই
                "catchment": (
                    "গুরুত্বপূর্ণ hydrological বিন্দু — এই station-এর কাছেই "
                    "সুরমা ও কুশিয়ারা নদী পুনরায় মিলিত হয়ে মেঘনা নাম নেয় "
                    "(Bhairab Bazar-এর দিকে)। সুরমা মেঘালয় পাহাড় থেকে, "
                    "কুশিয়ারা ত্রিপুরা পাহাড় (প্রধানত মনু নদী) থেকে পানি "
                    "বহন করে — দুইটা ভিন্ন transboundary উৎসের মিলনস্থল।"
                ),
                "flow_behavior": "Tidal station (BWDB survey অনুযায়ী) — জোয়ার-ভাটার প্রভাব আছে, সুরমা-কুশিয়ারা হাওর বেসিনের জটিল নিষ্কাশন প্যাটার্নের অংশ।",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 7.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 7.48,
            "verified_source": "old.ffwc.gov.bd, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": (
                "danger_level, upazila/union (Baniachong/Kulanj) সব "
                "মিলে গেছে ✅। coordinate off ছিল — stations.py-তে lat=24.60, "
                "lon=91.20, BWDB official অনুযায়ী lat=24.6952, lon=91.3790 — "
                "প্রায় ১৮ কিমি পূর্বে সরাতে হবে।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 705,
                    "corrected_estimate": 5000,
                    "corrected_range": "সুরমা+কুশিয়ারা মিলিত প্রবাহ হওয়ায় উল্লেখযোগ্য discharge, কিন্তু নির্দিষ্ট সংখ্যা পাওয়া যায়নি — river_categories.py-তে এই নদীর জন্য category না থাকায় আনুমানিক 'large_regional' ধরা যেতে পারে",
                    "source": "Banglapedia (Surma-Meghna River System)",
                    "confidence": "low — নির্দিষ্ট সংখ্যা পাওয়া যায়নি",
                },
                "cn": {"old_value": None, "reviewed_estimate": 85, "reasoning": "হাওর/জলাভূমি এলাকা, প্রচুর natural storage capacity", "confidence": "low"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": "danger_level (7.05m) তুলনামূলক কম, tidal buffer থাকায় flash-flood ধরনের আকস্মিকতা কম Khowai-র চেয়ে, কিন্তু haor বেসিনের deep flooding ঝুঁকি আলাদাভাবে বিবেচনা করা দরকার।",
                    "source": "Banglapedia",
                },
            },

            "flood_type": "Riverine (haor-basin — deep, seasonal flooding চরিত্র)",
            "flood_type_note": (
                "⚠️ হাওর বেসিন এলাকার বৈশিষ্ট্য — সুরমা ও কুশিয়ারার মাঝের "
                "এই এলাকা Banglapedia-তে 'complex basin area comprised of "
                "depressions or haors' হিসেবে বর্ণিত, যা বর্ষাকালে গভীরভাবে "
                "প্লাবিত থাকে দীর্ঘ সময় ধরে — এটা classic riverine (ওঠা-নামা) "
                "বা flash flood (আকস্মিক) কোনোটার সাথেই সম্পূর্ণ মেলে না, "
                "বরং একটা 'seasonal deep flooding/haor' নিজস্ব category "
                "দরকার হতে পারে।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই, হাওর এলাকার জন্য বিশেষ inundation model দরকার"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "Habiganj (খোয়াই)-এর জন্য এটা flashy transboundary নদী — উজানে "
        "(ত্রিপুরা) rainfall-এর ওপর discharge অনেক বেশি নির্ভরশীল, "
        "স্থানীয় soil moisture-এর prognostic value কম, কিন্তু স্থানীয় "
        "rainfall-ও গুরুত্বপূর্ণ কারণ ছোট catchment দ্রুত সাড়া দেয়। "
        "Markuli (সুরমা-মেঘনা)-এর জন্য হাওর বেসিনের বিশাল natural storage "
        "থাকায় soil moisture ও rainfall উভয়ের tactical weight কমিয়ে "
        "upstream cumulative rainfall (কয়েক দিনের collective) এর ওপর "
        "বেশি জোর দেওয়া যুক্তিসঙ্গত।"
    ),

    "confluence_note": (
        "হবিগঞ্জ প্রথমবার Surma-Meghna/হাওর বেসিন এই প্রজেক্টে যুক্ত করেছে। "
        "Markuli station বিশেষভাবে গুরুত্বপূর্ণ কারণ এটাই সুরমা-কুশিয়ারা "
        "সঙ্গমস্থল, যেখানে মেঘনা নদী শুরু হয় — এটা ভবিষ্যতে Sylhet, "
        "Sunamganj, Moulvibazar (কুশিয়ারা/মনু) জেলার সাথে যুক্ত হয়ে একটা "
        "সম্পূর্ণ Surma-Meghna করিডোর তৈরি করতে পারে, ঠিক যেভাবে যমুনা-"
        "ব্রহ্মপুত্র করিডোর তৈরি হয়েছে।"
    ),

    "cross_district_flags": (
        "⚠️ কোনো নতুন cross-district সন্দেহ পাওয়া যায়নি এই জেলায়। তবে "
        "Habiganj station-এর upazila field-এ ছোট একটা অস্পষ্টতা আছে — "
        "stations.py 'Baniachong' বলছে কিন্তু নদীটা মূলত হবিগঞ্জ শহর "
        "(Habiganj Sadar) ঘেঁষে যায় বলে Banglapedia বর্ণনা করেছে। "
        "গুরুত্বপূর্ণ না, কিন্তু ভবিষ্যতে wire করার সময় BWDB survey-র "
        "সাথে ক্রস-চেক করা ভালো।"
    ),
}