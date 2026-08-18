# ============================================================
# FloodAI — data/district_profiles/lalmonirhat.py
#
# জেলা-বাই-জেলা framework-এর ৯ম জেলা — ⚠️⚠️ সবচেয়ে ব্যতিক্রমী কেস এখন
# পর্যন্ত: এই জেলার নিজস্ব কোনো FFWC station নেই।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

LALMONIRHAT_PROFILE = {
    "district": "লালমনিরহাট",
    "district_lat": 25.92,
    "district_lon": 89.45,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 0,
    "station_count_note": (
        "⚠️⚠️ stations.py-তে district='Lalmonirhat' নামে একটাও entry নেই। "
        "flood_config.py-তে 'ffwc_station': None, 'ffwc_verified': False — "
        "কোডেই স্বীকার করা আছে যে এটা unverified।"
    ),

    # ── ২. আসলে এই জেলার বন্যা তথ্য কোথা থেকে আসে ──
    "real_world_practice": {
        "finding": (
            "🔍 একাধিক ২০২৬ সালের সংবাদ প্রতিবেদন (jagonews24, TBS, Dhaka "
            "Tribune) ঘেঁটে পেয়েছি — 'লালমনিরহাট পানি উন্নয়ন বোর্ড'-এর নিজস্ব "
            "প্রকৌশলী (Sunil Kumar, Executive Engineer) **Dalia পয়েন্টের "
            "(নীলফামারী জেলা, তিস্তা ব্যারাজ) ডেটা দিয়েই** লালমনিরহাটের বন্যা "
            "পরিস্থিতি বর্ণনা করেন। অর্থাৎ বাস্তবে লালমনিরহাটের 'official' "
            "বন্যা তথ্যের উৎস আসলে প্রতিবেশী জেলার (নীলফামারী) station — "
            "এটা কোনো secret বা bug না, বরং স্থানীয় BWDB office-এর প্রতিষ্ঠিত "
            "প্র্যাকটিস।"
        ),
        "source": (
            "jagonews24.com, tbsnews.net, dhakatribune.com — ২০২৬ সালের জুলাই-আগস্ট "
            "মাসের একাধিক প্রতিবেদন ('Teesta nears danger level, flood fears "
            "grow in Lalmonirhat'; 'Teesta flows 13cm above danger level in "
            "Lalmonirhat')"
        ),
        "implication": (
            "⚠️⚠️ flood_config.py-তে লালমনিরহাটের জন্য danger_level=14.5 বসানো "
            "আছে — কিন্তু Dalia-র আসল danger_level হলো ৫২.১৫ মিটার (সম্পূর্ণ "
            "ভিন্ন elevation datum/reference)। ১৪.৫ সংখ্যাটা Dalia-র সাথে "
            "কোনোভাবেই মেলে না — এটা সম্ভবত fabricated/placeholder সংখ্যা, "
            "কোনো real gauge-এর সাথে যুক্ত না। **এটাই এই framework-এ পাওয়া "
            "সবচেয়ে স্পষ্ট 'fake data' উদাহরণ** — ফরিদপুরের ক্ষেত্রে অন্তত "
            "একটা real (যদিও ছোট) নদী ও station ছিল, এখানে কিছুই নেই।"
        ),
    },

    # ── প্রস্তাবিত সমাধান ──
    "recommended_fix": {
        "option_a": (
            "লালমনিরহাটের ffwc_station সরাসরি Dalia (SW291.5R, নীলফামারী)-কে "
            "point করানো, danger_level=52.15 বসানো — বাস্তব প্র্যাকটিসের সাথে "
            "সঙ্গতিপূর্ণ, কিন্তু এটা 'নীলফামারীর ডেটা ধার করা' বলে UI-তে স্পষ্টভাবে "
            "label করা দরকার (misleading না হওয়ার জন্য)।"
        ),
        "option_b": (
            "Kaunia (রংপুর, ভাটিতে) কেও secondary reference হিসেবে ব্যবহার করা "
            "যায়, কারণ লালমনিরহাট ভৌগোলিকভাবে Dalia আর Kaunia-র মাঝামাঝি — "
            "দুইটার average/worse-case নেওয়া একটা বিকল্প।"
        ),
        "recommendation": (
            "Option A বেশি যুক্তিসঙ্গত, কারণ বাস্তবে স্থানীয় কর্তৃপক্ষ এটাই করছে "
            "(Dalia-কে reference ধরা) — model-কেও একই বাস্তবতা অনুসরণ করানো উচিত, "
            "নতুন কিছু আবিষ্কার করার দরকার নেই।"
        ),
    },

    # ── ৩. নদীর স্ট্রাকচার (Dalia/তিস্তা সিস্টেমের প্রেক্ষিতে) ──
    "river_structure": {
        "river": "তিস্তা (Teesta)",
        "category": "large_regional, dam-controlled",
        "note": "রংপুর প্রোফাইলে (Kaunia) বিস্তারিত আলোচনা করা হয়েছে — একই সিস্টেম, লালমনিরহাট এই দুই gauge (Dalia উজানে, Kaunia ভাটিতে)-র মাঝখানে",
        "upstream_reference": "Jalpaiguri, IN",  # flood_config.py-তে যা আছে, ভৌগোলিকভাবে সঠিক
        "lag_time_hours": 8,  # flood_config.py-তে যা আছে — Dalia থেকে সবচেয়ে কাছে হওয়ায় সবচেয়ে কম lag time, যুক্তিসঙ্গত
    },

    # ── ৪. ড্যাঞ্জার লেভেল — সংশোধনের প্রস্তাব ──
    "danger_level_m": {
        "old_value": 14.5,
        "old_value_verdict": "❌❌ সম্ভবত fabricated — কোনো real station/datum-এর সাথে মেলে না",
        "recommended_value": 52.15,
        "recommended_source": "Dalia station (SW291.5R, নীলফামারী) — লালমনিরহাটের নিজস্ব BWDB office যা ব্যবহার করে",
    },

    "flood_type": "Dam-Affected",
    "flood_type_note": (
        "✅ এটা সঠিকভাবে classify করা ছিল — গজলডোবা ব্যারাজ (ভারত) থেকে পানি "
        "ছাড়া/আটকানোর উপর লালমনিরহাটের বন্যা পরিস্থিতি সরাসরি নির্ভরশীল, "
        "সাধারণ rainfall-driven riverine না। ২০২৬-এর সংবাদে বারবার 'authorities "
        "have kept all necessary gates of the Teesta Barrage open' উল্লেখ "
        "এটা নিশ্চিত করে।"
    ),

    "ml_features_verified": {
        "reference_discharge_m3s": {
            "old_buggy_value": 1450,  # danger_level(14.5, ভুল)*100
            "corrected_estimate": 4000,
            "corrected_range": "Dalia/Kaunia-র মতোই (রংপুর প্রোফাইল দ্রষ্টব্য) — ঐতিহাসিক সর্বোচ্চ ৮,৫৭৭ m³/s",
            "note": "danger_level-ই ভুল হওয়ায় পুরনো reference_discharge-ও অর্থহীন — এটা ঠিক করতে হলে আগে danger_level ঠিক করতে হবে",
        },
        "cn": {"old_value": 81, "reviewed_estimate": 83, "confidence": "low-moderate — রংপুরের সাথে সামঞ্জস্যপূর্ণ"},
        "risk_category": {
            "old_value": "উচ্চ",
            "reviewed_estimate": "উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)",
            "reasoning": "যদিও danger_level সংখ্যা ভুল, তবু বাস্তবে লালমনিরহাট নিয়মিত তিস্তার বন্যায় ক্ষতিগ্রস্ত হয় (আদিতমারী, কালীগঞ্জ, হাতীবান্ধা, পাটগ্রাম উপজেলা) — 'উচ্চ' classification নিজেই ঠিক আছে, শুধু underlying সংখ্যা ভুল।",
        },
    },

    "inundation_bands": {
        "affected_upazilas": "আদিতমারী, কালীগঞ্জ, হাতীবান্ধা, পাটগ্রাম, লালমনিরহাট সদর — ২০২৬-এর একাধিক সংবাদে বারবার উল্লেখিত",
        "status": "⚠️ placeholder — DEM/DFO calibration বাকি, তবে affected upazila-র তালিকা অন্তত নির্দিষ্ট করা গেছে",
    },

    "soil_moisture_weight_note": "একই তিস্তা সিস্টেম যুক্তি — dam release/gate status সবচেয়ে গুরুত্বপূর্ণ predictor হওয়া উচিত, যা এখন model-এ ধরাই পড়ে না।",

    "confluence_note": "লালমনিরহাট CONFLUENCE_DISTRICTS-এ নেই।",
}