# ============================================================
# FloodAI — data/district_profiles/mymensingh.py — জেলা #২২
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MYMENSINGH_PROFILE = {
    "district": "ময়মনসিংহ",
    "district_lat": 24.95, "district_lon": 90.67,
    "station_count": 1,
    "stations": [{
        "name": "Mymensingh", "ffwc_id": "SW228.5", "is_primary": True,
        "river": "পুরাতন ব্রহ্মপুত্র (Old Brahmaputra)", "upazila": "Gauripur", "union": None,
        "river_structure": {
            "category": "medium (ঐতিহাসিকভাবে mega_trunk ছিল, এখন distributary)",
            "catchment": (
                "🔍 মানিকগঞ্জের 'পুরাতন ধলেশ্বরী'-র মতোই একটা ঐতিহাসিক avulsion "
                "কেস, কিন্তু অনেক বড় স্কেলে — Banglapedia অনুযায়ী মূল ব্রহ্মপুত্র "
                "১৭৮৭ সালের আগে এই পথেই (জামালপুর-ময়মনসিংহ হয়ে) প্রবাহিত হতো। "
                "১৭৮৭ সালের প্রবল বন্যা ও তিস্তার ব্রহ্মপুত্রে মিশে যাওয়ার পর নদী "
                "পশ্চিমে সরে যায় (আজকের যমুনা), আর এই পুরনো চ্যানেলটা ধীরে ধীরে "
                "ক্ষীণ হয়ে পড়ে (East India Company-র রেকর্ড অনুযায়ী ১৮৪৫ সালের "
                "মধ্যেই flow কমে যাওয়া নিয়ে তারা চিন্তিত ছিল)।"
            ),
            "flow_behavior": "এখন মূল যমুনার তুলনায় অনেক ছোট, স্থানীয়ভাবে গুরুত্বপূর্ণ কিন্তু trunk river dynamics নেই",
            "upstream_reference": "Guwahati, IN",
            "upstream_reference_note": "⚠️ আংশিক প্রশ্নসাপেক্ষ — এই নদী এখন মূল ব্রহ্মপুত্র/যমুনা থেকে বিচ্ছিন্ন (অনেকটা ফরিদপুরের কুমারের মতো, যদিও এতটা চরম না), তাই সরাসরি Guwahati upstream rainfall কতটা প্রাসঙ্গিক তা স্পষ্ট না। local_rain বেশি গুরুত্বপূর্ণ হতে পারে।",
            "lag_time_hours": 20,
        },
        "danger_level_m": 12.05, "highest_recorded_m": None,
        "verified_source": "flood_config.py-র সাথে মিলেছে; ReliefWeb/ScienceDirect (২০২২ flash flood-এ ময়মনসিংহ ৯ ক্ষতিগ্রস্ত জেলার একটা হিসেবে নিশ্চিত)",
        "ml_features_verified": {
            "reference_discharge_m3s": {
                "old_buggy_value": 1205,
                "corrected_estimate": 1500,
                "corrected_range": "⚠️ নির্দিষ্ট আধুনিক discharge measurement পাওয়া যায়নি — মানিকগঞ্জের 'পুরাতন ধলেশ্বরী' (১৯৭০-এ ৫,০০০ থেকে এখন ~১,০০০ m³/s কমার) প্যাটার্নের সাথে তুলনীয় ধরে conservative অনুমান",
                "source": "Banglapedia (Old Brahmaputra River, avulsion history); Wiley/ScienceDirect (avulsion papers — শুধু ঐতিহাসিক context, আধুনিক discharge না)",
                "confidence": "low — dedicated modern gauge measurement দরকার",
                "note": "⚠️ পুরনো বাগযুক্ত সূত্র (১২০৫) আর নতুন অনুমান (১৫০০) কাছাকাছি — কিশোরগঞ্জ/সুনামগঞ্জের মতো মাঝারি-স্কেল নদীতে crude সূত্র তুলনামূলক কম ভুল দেয়, এই প্যাটার্নটা এখন বেশ কয়েকবার নিশ্চিত হলো।",
            },
            "cn": {"old_value": 80, "reviewed_estimate": 85, "reasoning": "প্লাবনভূমি কৃষিজমি, avulsion-পরবর্তী পলিমাটি — মাঝারি-উচ্চ CN যুক্তিসঙ্গত", "confidence": "low-moderate"},
            "risk_category": {
                "old_value": "উচ্চ",
                "reviewed_estimate": "উচ্চ (অপরিবর্তিত)",
                "reasoning": "২০২২-এর flash flood-এ ৯টা ক্ষতিগ্রস্ত জেলার একটা ছিল (৭.২ মিলিয়ন মানুষ প্রভাবিত অঞ্চলব্যাপী) — 'উচ্চ' যথাযথ, উজানের সিলেট/সুনামগঞ্জের ('অতি উচ্চ') তুলনায় একটু কম গুরুতর হওয়াটাও ভৌগোলিকভাবে যুক্তিসঙ্গত (ময়মনসিংহ হাওর কেন্দ্র থেকে দূরে)।",
                "source": "ReliefWeb/ScienceDirect (২০২২ flash flood impact analysis)",
            },
        },
        "flood_type": "Riverine",
        "flood_type_note": "✅ যুক্তিসঙ্গত — যদিও ঐতিহাসিক avulsion context বিবেচনায় এটা একটা 'reduced trunk river' নদী, খাঁটি ছোট local নদী না।",
        "inundation_bands": {"status": "⚠️ placeholder — DEM/DFO বাকি"},
    }],

    "soil_moisture_weight_note": "মাঝারি-স্কেল distributary নদী — discharge_ratio এবং local_rain দুটোই মোটামুটি সমান গুরুত্বপূর্ণ, পুরনো mega_trunk অনুমান প্রযোজ্য না।",

    "confluence_note": "ময়মনসিংহ CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "শেরপুর/নেত্রকোণার (ভুগাই-কাংশা-সোমেশ্বরী সিস্টেম) সাথে ভৌগোলিকভাবে পাশাপাশি, কিন্তু নদী সিস্টেম আলাদা (ময়মনসিংহ পুরাতন ব্রহ্মপুত্রের, ওগুলো মেঘালয়ের সরাসরি উপনদী) — 2022-এর flash flood-এ একসাথে প্রভাবিত হলেও hydrology ভিন্ন।",
}