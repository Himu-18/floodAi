# ============================================================
# FloodAI — data/district_profiles/chandpur.py — জেলা #৪১
# 🔍 সবচেয়ে গুরুত্বপূর্ণ confluence point — পদ্মা+যমুনা+মেঘনার সম্পূর্ণ
# মিলিত প্রবাহ এখানেই।
# ✅ (২০২৬-০৮) এখন wired — get_reference_discharge(danger_level, district_name)
# সাধারণ single-river fallback পথেই এই profile খুঁজে পায় ও ব্যবহার করে।
# ============================================================

CHANDPUR_PROFILE = {
    "district": "চাঁদপুর", "district_lat": 23.23, "district_lon": 90.65,
    "station_count": 1,
    "stations": [{
        "name": "Chandpur", "ffwc_id": "SW277", "is_primary": True,
        "river": "নিম্ন মেঘনা (Lower Meghna)", "upazila": "Chandpur Sadar", "union": None,
        "river_structure": {
            "category": "mega_trunk (দেশের একক বৃহত্তম combined discharge পয়েন্ট)",
            "catchment": (
                "🔍🔍 এটা বাংলাদেশের হাইড্রোলজিক্যালি সবচেয়ে গুরুত্বপূর্ণ পয়েন্ট — "
                "পদ্মা (গঙ্গা+যমুনার মিলিত প্রবাহ) এখানে এসে উজানের মেঘনা (সুরমা+"
                "কুশিয়ারা)-র সাথে মেশে, 'নিম্ন মেঘনা' নাম নিয়ে। বিশ্বের তৃতীয় "
                "সর্বোচ্চ পানি নিষ্কাশনকারী নদী-সঙ্গম এটা (sediment discharge-এ "
                "সর্বোচ্চ)। পদ্মা+যমুনা মিলিতভাবে ৮৫% flow দেয়, মেঘনা (উজানের) "
                "বাকি ১৫% দেয়।"
            ),
            "flow_behavior": "Tidal reach — জোয়ার-ভাটার প্রভাবও আছে ঊর্ধ্বমুখী discharge-এর সাথে মিশে",
            "upstream_reference": "Agartala, IN",
            "upstream_reference_caveat": "⚠️ ভুল — এই পয়েন্টের প্রধান discharge আসে গঙ্গা/যমুনা (Malda/Guwahati) থেকে, ত্রিপুরা/আগরতলা থেকে না। উজানের মেঘনার অংশটুকুই শুধু হিমালয়-মেঘালয় (Shillong) থেকে আসে।",
            "lag_time_hours": 24,
        },
        "danger_level_m": 3.55, "highest_recorded_m": None,
        "verified_source": "flood_config.py-র সাথে মিলেছে; Wikipedia (Meghna River — Chandpur গড় discharge তথ্য)",
        "ml_features_verified": {
            "reference_discharge_m3s": {
                "old_buggy_value": 355, "corrected_estimate": 95000,
                "corrected_range": "৯০,০০০-১,০০,০০০ m³/s অনুমান — সরাসরি published bankfull figure নিম্ন মেঘনা/চাঁদপুরের জন্য পাওয়া যায়নি, তাই পদ্মার bankfull:mean ratio (~২.৫x, Best et al./ResearchGate অনুযায়ী পদ্মার গড় ~৩০,০০০ বনাম bankfull ~৭৬,০০০) একই অনুপাতে চাঁদপুরের গড় (৪০,৫৩২.৯ m³/s, Wikipedia/Banglapedia) -এ প্রয়োগ করে estimate করা",
                "source": "Wikipedia/Banglapedia (mean discharge) + Padma bankfull:mean ratio extrapolation (এই framework-এ যমুনা/পদ্মাতেও একই পদ্ধতি ব্যবহৃত হয়েছে)",
                "confidence": "moderate — mean discharge সরাসরি measured/verified, কিন্তু bankfull সংখ্যাটা extrapolated, চাঁদপুর-নির্দিষ্ট bankfull measurement না",
                "note": "⚠️⚠️ আগে এখানে ভুলবশত mean annual discharge (৪০,৫০০) বসানো ছিল danger-level-equivalent threshold হিসেবে — কিন্তু mean annual মানে বছরের প্রায় অর্ধেক সময়ই প্রবাহ তার চেয়ে বেশি থাকে (বিশেষত বর্ষাকালে), তাই এটা প্রায় সবসময়ই 'উচ্চ ঝুঁকি' দেখাচ্ছিল even স্বাভাবিক মৌসুমি প্রবাহেও। bankfull ব্যবহার করাই সঠিক পদ্ধতি, যেমনটা যমুনা/পদ্মার জন্য আগেই করা হয়েছিল।",
            },
            "cn": {"old_value": 80, "reviewed_estimate": 88, "confidence": "moderate"},
            "risk_category": {"old_value": "উচ্চ", "reviewed_estimate": "উচ্চ (অপরিবর্তিত — ইতিমধ্যে সঠিক)", "reasoning": "দেশের সবচেয়ে গুরুত্বপূর্ণ hydrological node, নিয়মিত নদীভাঙনের শিকার (Chandpur hard-point erosion-control প্রকল্প)"},
        },
        "flood_type": "Riverine",
        "flood_type_note": "⚠️ Barisal-এর মতোই সমস্যা — এটা tidal reach-ও বটে (জোয়ার-ভাটা প্রভাবিত), শুধু 'Riverine' সম্পূর্ণ চিত্র দেয় না।",
        "inundation_bands": {"status": "⚠️ placeholder — DEM/DFO বাকি"},
    }],
    "soil_moisture_weight_note": "mega_trunk confluence — discharge সবচেয়ে বড় predictor, কিন্তু tidal phase-ও গুরুত্বপূর্ণ (এখন model-এ নেই)।",
    "confluence_note": "⚠️ এটা riverine.py-র CONFLUENCE_DISTRICTS তালিকায় নেই, কিন্তু ভৌগোলিকভাবে এটাই *সবচেয়ে গুরুত্বপূর্ণ* confluence point — পদ্মা+মেঘনার মিলনস্থল। মূল confluence-bug fix করার সময় এই জেলাকেও তালিকায় যোগ করা বিবেচনা করা উচিত।",
    "cross_district_note": "কিশোরগঞ্জের Bhairab Bazar (উজানের মেঘনার জন্ম) ও রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জ/শরীয়তপুরের (পদ্মা trunk) সাথে সরাসরি hydrologically সংযুক্ত — এই সবগুলোর পানিই শেষমেশ চাঁদপুর দিয়ে বয়ে যায়।",
}