# ============================================================
# FloodAI — data/district_profiles/noakhali.py
#
# জেলা-বাই-জেলা framework-এর ১৪তম জেলা।
#
# ২০২৬-০৮-১৫ আপডেট: আগে এই প্রোফাইল দাবি করেছিল "একটাও FFWC station নেই"।
# এটা ভুল ছিল — BWDB-র hydrology ডাটাবেসে (hydrology.bwdb.gov.bd)
# Noakhali জেলার ভেতরেই আসলে ৩টা station registered আছে:
#   - SW182 (Companiganj, Little Feni Dakatia) — danger_level 4.15m
#     ইউজার নিজে verify করে দিয়েছেন, এখন যোগ করা হলো।
#   - SW222 (Noakhali Sadar, Noakhali Khal) — coordinate/ID পাওয়া গেছে
#     কিন্তু danger_level এখনো unverified, তাই যোগ করা হয়নি।
#   - SW321 (Hatiya, Hatiya river) — একই অবস্থা।
# আসল কারণ: এই ৩টা station BWDB-র historical/manual hydrology ডাটাবেসে
# আছে, কিন্তু FFWC-র active daily bulletin (old.ffwc.gov.bd, ~৯০টা
# forecasting station)-এর তালিকায় নেই। তাই "FFWC bulletin-এ কোনো তথ্য
# নেই" (bdnews24, ২০২৪) কথাটা ঠিক, কিন্তু "কোনো station নেই" কথাটা ভুল
# ছিল।
#
# এখন stations list-সহ properly wire করা হলো, যাতে
# district_profiles_loader.py এটা সঠিকভাবে পড়তে পারে।
# ============================================================

NOAKHALI_PROFILE = {
    "district": "নোয়াখালী",
    "district_lat": 22.87,
    "district_lon": 91.10,

    "station_count": 1,
    "station_count_note": (
        "SW182 (Companiganj, Little Feni Dakatia) verified ও যোগ করা হয়েছে। "
        "আরও ২টা (SW222 Noakhali Khal, SW321 Hatiya) coordinate/ID-সহ পাওয়া "
        "গেছে কিন্তু danger_level এখনো unverified।"
    ),

    "stations": [
        {
            "name": "Companiganj",
            "ffwc_id": "SW182",
            "is_primary": True,

            "river": "ছোট ফেনী / Little Feni Dakatia",
            "upazila": "Companiganj",
            "lat": 22.7694,
            "lon": 91.3492,

            "river_structure": {
                "category": "small_or_tidal",
                "catchment": (
                    "মূলত ফেনী/মুহুরী নদীর একটা শাখা, ত্রিপুরার পাহাড় থেকে নেমে "
                    "Bay of Bengal-এ মিশেছে। BWDB-র classification অনুযায়ী "
                    "'Tidal' ধরনের station — শুধু upstream discharge না, "
                    "জোয়ার-ভাটার প্রভাবও এখানে সরাসরি কাজ করে।"
                ),
            },

            "danger_level_m": 4.15,

            "flood_type_note": (
                "⚠️ আংশিক সঠিক হিসেবে 'Coastal & Tidal' লেবেল করা আছে, কিন্তু "
                "২০২৪-এর প্রকৃত ঘটনা দেখায় এটা তিনটা কারণের মিশ্রণ ছিল: "
                "(১) সরাসরি extreme rainfall (১,০২০mm/মাস, ২০ বছরের সর্বোচ্চ), "
                "(২) Bay of Bengal থেকে tidal surge, এবং (৩) ফেনী/মুহুরী নদীর "
                "উজানের পানি নেমে আসা। শুধু 'Coastal & Tidal' লেবেল তৃতীয় "
                "কারণটা (upstream overflow) ধরে না — hybrid flood_type হওয়া "
                "উচিত। SW182 (Little Feni Dakatia) এখন সরাসরি এই উজানের "
                "প্রভাবটা measure করে, তাই আংশিকভাবে এই gap পূরণ হলো।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 350,
                    "corrected_estimate": None,
                    "note": (
                        "danger_level এখন verified (4.15m) হলেও এটা BWDB-র "
                        "'Tidal' শ্রেণির station — discharge_ratio concept "
                        "সাধারণ riverine নদীর মতো এখানে সরাসরি প্রযোজ্য না, "
                        "তাই reference_discharge_m3s ইচ্ছাকৃতভাবে None রাখা "
                        "হলো; rainfall+tidal-ভিত্তিক আলাদা approach এই "
                        "জেলার জন্য বেশি অর্থবহ।"
                    ),
                    "confidence": "danger_level: high (verified) — discharge_ratio: not applicable (tidal)",
                },
                "cn": {"old_value": 79, "reviewed_estimate": 85, "reasoning": "উপকূলীয় নিচু জলাভূমি/কৃষিজমি, প্রায়ই জলমগ্ন — উচ্চ CN যুক্তিসঙ্গত", "confidence": "low"},
                "risk_category": {
                    "old_value": "উচ্চ",
                    "reviewed_estimate": "উচ্চ (অপরিবর্তিত — বাস্তবতার সাথে মিলে যায়)",
                    "reasoning": "২০২৪-এ ১০ লক্ষের বেশি মানুষ পানিবন্দী, ২০ বছরের সর্বোচ্চ বৃষ্টিপাত — 'উচ্চ' সঠিক।",
                    "source": "The Daily Star (২০২৪ কভারেজ)",
                },
            },
        },
    ],

    "unverified_stations_found": [
        {"name": "Noakhali", "ffwc_id": "SW222", "river": "Noakhali Khal", "upazila": "Noakhali Sadar", "lat": 22.8450, "lon": 91.1017, "note": "danger_level এখনো verify করা হয়নি"},
        {"name": "Hatiya", "ffwc_id": "SW321", "river": "Hatiya", "upazila": "Hatiya", "lat": 22.2485, "lon": 91.1403, "note": "danger_level এখনো verify করা হয়নি"},
    ],

    "real_world_practice": {
        "finding": (
            "নোয়াখালীর ২০২৪ বন্যার সরকারি/স্থানীয় রিপোর্টিং মূলত rainfall "
            "measurement আর স্থানীয় BWDB কর্মকর্তাদের পর্যবেক্ষণ থেকে আসে। "
            "Noakhali-র BWDB নির্বাহী প্রকৌশলী Munshi Amir Faisal নিজেই "
            "বলেছেন — এক মাসে ১,০২০ মিমি বৃষ্টিপাত হয়েছে (গত ২০ বছরের "
            "সর্বোচ্চ, বার্ষিক গড়ের অর্ধেকেরও বেশি এক মাসেই)।"
        ),
        "source": "The Daily Star (Munshi Amir Faisal, WDB executive engineer, Noakhali)",
    },

    "upstream_reference_issue": {
        "old_value": "Agartala, IN",
        "verdict": "❌ সম্ভবত ভুল/copy-paste — ফেনী জেলার upstream reference ভুলবশত এখানে কপি হয়ে থাকতে পারে",
        "recommendation": "coastal/tidal জেলার জন্য 'upstream' concept কম প্রাসঙ্গিক — Bay of Bengal tidal-cycle ডেটা বেশি অর্থবহ হবে।",
    },

    "inundation_bands": {
        "affected_upazilas": "কোম্পানীগঞ্জ, হাতিয়া (সম্পূর্ণ প্লাবিত), সুবর্ণচর, সোনাইমুড়ী, নোয়াখালী সদর, কবিরহাট (BDRCS SitRep অনুযায়ী)",
        "status": "⚠️ placeholder — DEM/DFO calibration বাকি",
    },

    "soil_moisture_weight_note": "coastal/tidal + rainfall-driven জেলা — rainfall+tidal-surge data সবচেয়ে গুরুত্বপূর্ণ predictor হওয়া উচিত।",

    "confluence_note": "নোয়াখালী CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "একই 'BWDB-তে station আছে কিন্তু FFWC bulletin-এ নেই' প্যাটার্ন লক্ষ্মীপুর, ভোলা, পটুয়াখালী, বরগুনা, পিরোজপুর, ঝালকাঠি — এই উপকূলীয় জেলাগুলোতেও থাকতে পারে, চেক করা দরকার।",
}