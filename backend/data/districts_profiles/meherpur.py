# ============================================================
# FloodAI — data/district_profiles/meherpur.py — জেলা #৩৩
# ⚠️⚠️ বড় finding: এই জেলার নদী Wikipedia অনুযায়ী 'practically dead'।
# ⚠️ কোনো FFWC station নেই।
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MEHERPUR_PROFILE = {
    "district": "মেহেরপুর", "district_lat": 23.76, "district_lon": 88.63,
    "station_count": 0,
    "station_count_note": "⚠️ stations.py-তে কোনো entry নেই। flood_config.py-তে ffwc_verified: False।",

    "river_structure": {
        "river": "ভৈরব (Bhairab)",
        "category": "small (প্রায় মৃত নদী)",
        "catchment": (
            "🔍🔍 Wikipedia থেকে সরাসরি: 'Its intake from the Jalangi having "
            "silted up, this river has been **practically dead since long**. "
            "The poor climate of Meherpur... is in great measure attributed "
            "to the stagnancy of its water.' — অর্থাৎ এই নদী কার্যত মৃত, "
            "জালাঙ্গী থেকে তার পানির উৎস পলি জমে বন্ধ হয়ে গেছে বহু আগেই। "
            "মেহেরপুরের টেঙ্গামারী সীমান্ত থেকে উৎপন্ন হয়ে মেহেরপুর শহরের পাশ "
            "দিয়ে বয়ে গিয়ে মাথাভাঙায় হারিয়ে যায়। একটা পৃথক (এবং প্রায়ই "
            "বিভ্রান্তিকরভাবে গুলিয়ে ফেলা) 'জালাঙ্গী-ভৈরব' নামের নদীও আছে যেটা "
            "সম্পূর্ণ ভিন্ন এবং সংযুক্ত না — এই দুইটা নাম না গুলিয়ে ফেলা জরুরি।"
        ),
        "flow_behavior": "স্থবির/স্থগিত পানি, প্রায় কোনো flow নেই — flash flood বা riverine বন্যা কোনোটার জন্যই এই নদী প্রাসঙ্গিক প্রেডিক্টর না",
        "upstream_reference": "Malda, IN",
        "lag_time_hours": 46,
    },

    "danger_level_m": {
        "old_value": 7.5,
        "verdict": "❌❌ 'practically dead' নদীর জন্য ৭.৫ মিটার danger_level সংখ্যাটা কীসের ভিত্তিতে এসেছে স্পষ্ট না — যেহেতু নদীটাই প্রায় স্থবির, এই সংখ্যা লালমনিরহাটের মতোই সম্ভবত fabricated/অর্থহীন।",
    },

    "ml_features_verified": {
        "reference_discharge_m3s": {
            "old_buggy_value": 750, "corrected_estimate": None,
            "note": "⚠️⚠️ 'প্রায় মৃত' নদীতে discharge_ratio ধারণাটাই অর্থহীন — এই জেলার বন্যা ঝুঁকি (যদি থাকে) সম্পূর্ণভাবে local rainfall/drainage-নির্ভর হওয়ার কথা, কোনো trunk river dynamics না।",
            "confidence": "none",
        },
        "cn": {"old_value": 72, "reviewed_estimate": 80, "reasoning": "স্থবির জলাভূমি — মাঝারি CN", "confidence": "low"},
        "risk_category": {
            "old_value": "কম",
            "reviewed_estimate": "কম (অপরিবর্তিত — যুক্তিসঙ্গত, তবে ভিন্ন কারণে)",
            "reasoning": "'কম' ঠিকই আছে, কিন্তু এটা 'কম discharge risk' না বরং 'নদীই প্রায় অকার্যকর, তাই river-based flood risk model-ই এখানে খুব একটা প্রযোজ্য না' — flash-flood/waterlogging জেলার মতো fundamentally ভিন্ন ধরনের সীমাবদ্ধতা।",
        },
    },

    "flood_type": "Riverine",
    "flood_type_note": "⚠️⚠️ সম্ভবত সবচেয়ে ভুল flood_type classification এই framework-এ — 'Riverine' বলতে বোঝায় নদী উপচে পড়ে বন্যা করে, কিন্তু এই নদী তো প্রায় মৃত/স্থবির। মেহেরপুরের প্রকৃত বন্যা ঝুঁকি (থাকলে) স্থানীয় জলাবদ্ধতা/rainfall-ভিত্তিক হওয়ার কথা, classic riverine না।",

    "inundation_bands": {"status": "⚠️ placeholder — এমনকি rough band তৈরির ভিত্তিও নেই এই স্থবির নদীর জন্য"},

    "soil_moisture_weight_note": "নদী প্রায় অকার্যকর হওয়ায় local rainfall + drainage/stagnant-water dynamics-ই একমাত্র প্রাসঙ্গিক factor, discharge_ratio সম্পূর্ণ বাদ দেওয়া উচিত।",

    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই।",

    "recommended_fix": "এই জেলার জন্য discharge-ভিত্তিক মডেল সম্পূর্ণ বাদ দিয়ে rainfall+drainage-ভিত্তিক আলাদা approach বিবেচনা করা উচিত — নোয়াখালী/পটুয়াখালীর মতোই একটা category, যদিও কারণ ভিন্ন (ওখানে কোনো নদীই নেই, এখানে নদী আছে কিন্তু কার্যত মৃত)।",
}