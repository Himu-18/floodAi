# ============================================================
# FloodAI — data/district_profiles/madaripur.py
#
# জেলা-বাই-জেলা framework-এর ১০ম জেলা। প্রথমবার Ganges-Padma ব-দ্বীপ
# অঞ্চলের tidal-influenced distributary নদীর একটা জেলা যুক্ত হলো।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MADARIPUR_PROFILE = {
    "district": "মাদারীপুর",
    "district_lat": 23.1642,
    "district_lon": 90.1897,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # শুধু ১টা station — এই প্রজেক্টের সবচেয়ে ছোট জেলা-প্রোফাইল এখন
    # পর্যন্ত। (উল্লেখ্য, stations.py-তে 'Haridaspur'/SW198 নামের একটা
    # station river='Madaripur BR' লেখা থাকলেও সেটা আসলে Gopalganj
    # জেলার station — নদীর নামে 'Madaripur' শব্দ থাকলেও জেলা ভিন্ন)
    "station_count": 1,

    "stations": [
        {
            "name": "Madaripur",
            "ffwc_id": "SW5",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "আড়িয়াল খাঁ (Arial Khan)",
            "upazila": "Madaripur Sadar",
            "union": "Paurashava",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "large_regional",  # river_categories.py-তে সরাসরি নেই, Padma-distributary হিসেবে অনুমান
                "catchment": (
                    "পদ্মার একটা major distributary — Rajbari জেলার "
                    "Goalanda-র প্রায় ৫১.৫ কিমি দক্ষিণ-পূর্বে পদ্মা থেকে "
                    "বিচ্ছিন্ন হয়ে Faridpur ও Madaripur জেলা দিয়ে বয়ে "
                    "Barisal-এর Tentulia নদীতে গিয়ে মেশে। মাদারীপুর শহর "
                    "এই নদীর ডান তীরে অবস্থিত। মোট দৈর্ঘ্য ১৫৫-১৬৩ কিমি, "
                    "basin area ১,৪৩৮ বর্গকিমি। BWDB এটাকে দক্ষিণ-পশ্চিম "
                    "অঞ্চলের 'River No. 2' হিসেবে চিহ্নিত করেছে।"
                ),
                "flow_behavior": (
                    "সারা বছর নৌ-চলাচল উপযোগী, জোয়ার-ভাটার প্রভাবযুক্ত "
                    "(মাদারীপুরে normal tidal range ০.৩২ মিটার)। "
                    "জুলাই-আগস্টে discharge সর্বোচ্চ ~৪,০০০ m³/s পর্যন্ত "
                    "পৌঁছায়, পানির গভীরতা ১২ মিটার পর্যন্ত হতে পারে। "
                    "মার্চ-এপ্রিলে flow কম থাকে। meander চরিত্রের এবং "
                    "erosion-প্রবণ — মাদারীপুর শহর নিজেই ভাঙনের হুমকিতে "
                    "আছে, BWDB ইতিমধ্যে groyne নির্মাণ করেছে শহর রক্ষায়।"
                ),
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 3.75,  # ✅ FFWC verify করা
            "highest_recorded_m": 5.37,
            "verified_source": "old.ffwc.gov.bd, Banglapedia, Wikipedia, যাচাই করা হয়েছে ২০২৬-০৮-১১",
            "verification_note": "danger_level, upazila/union (Madaripur Sadar/Paurashava) সব মিলে গেছে ✅। coordinate যাচাই করার জন্য BWDB-র official hydrology survey table-এ সরাসরি এই station খুঁজে পাওয়া যায়নি (Kushtia/Gopalganj-এর কাছাকাছি অন্য entries পাওয়া গেছে কিন্তু এই নির্দিষ্ট SW5 না) — stations.py-র coordinate (lat=23.16, lon=90.19) মাদারীপুর শহরের সাধারণ অবস্থানের সাথে সামঞ্জস্যপূর্ণ মনে হচ্ছে, কিন্তু independent survey দিয়ে confirm করা যায়নি।",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 375,
                    "corrected_estimate": 4000,
                    "corrected_range": "জুলাই-আগস্টে সর্বোচ্চ ~৪,০০০ m³/s (measured figure, Wikipedia)",
                    "source": "Wikipedia (Arial Khan River) — measured discharge figure পাওয়া গেছে, এই প্রজেক্টের কিছু জেলার তুলনায় বেশি নির্ভরযোগ্য",
                    "cross_check": "river_categories.py-তে সরাসরি এই category নেই — ৪,০০০ m³/s 'medium' (20-8000)-এর উপরের দিকে এবং 'large_regional'-এর নিচের দিকে পড়ে, একটা নতুন সীমানাবর্তী category বিবেচনা করা যেতে পারে।",
                    "critical_caveat": "train_model.py-র একই danger_level*100 বাগ প্রযোজ্য, কিন্তু এখানে বিশেষভাবে গুরুত্বপূর্ণ — corrected_estimate (৪,০০০) পুরনো buggy value (৩৭৫)-এর প্রায় ১১ গুণ, তাই retrain করলে এই station-এর প্রভাব উল্লেখযোগ্যভাবে বদলাবে।",
                },
                "cn": {"old_value": None, "reviewed_estimate": 82, "reasoning": "ব-দ্বীপ/tidal floodplain, উচ্চ পানি-ধারণ ক্ষমতাসম্পন্ন মাটি — অন্যান্য জেলার (৮৮-৮৯) তুলনায় সামান্য কম CN যুক্তিসঙ্গত কারণ tidal drainage flexibility বেশি", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": None,
                    "reviewed_estimate": "মাঝারি",
                    "reasoning": "danger_level (3.75m) এই পুরো প্রজেক্টের মধ্যে সবচেয়ে কম — tidal buffer ও deltaic flatness বন্যার তীব্রতা কমায়, কিন্তু bank erosion (মাদারীপুর শহর নিজেই হুমকিতে) একটা আলাদা, উল্লেখযোগ্য ঝুঁকি যা danger_level দিয়ে captured হয় না।",
                    "source": "Banglapedia (Arial Khan River — town erosion, groyne construction)",
                },
            },

            "flood_type": "Riverine (tidal-influenced, deltaic — এই প্রজেক্টের প্রথম pure tidal-delta station)",
            "flood_type_note": (
                "⚠️ এই প্রজেক্টের প্রথম pure ব-দ্বীপ/tidal station — বাকি "
                "সবগুলো জেলা হয় mega_trunk যমুনা-ব্রহ্মপুত্র, নয়তো flashy "
                "পাহাড়ি transboundary নদী ছিল। এখানে flood risk-এর প্রকৃতি "
                "সম্পূর্ণ ভিন্ন — জোয়ার-ভাটা, ধীর deltaic drainage, এবং "
                "danger_level cross হওয়ার চেয়ে bank erosion বেশি বাস্তব "
                "ঝুঁকি। flood_type ট্যাগে এই tidal/deltaic character আলাদা "
                "করে চিহ্নিত করা উচিত।"
            ),
            "inundation_bands": {"status": "⚠️ placeholder — নেই, tidal/deltaic dynamics-এর কারণে সাধারণ rainfall-driven inundation model এখানে কম প্রাসঙ্গিক, tidal-surge-aware model দরকার"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "⚠️ Madaripur (আড়িয়াল খাঁ)-এর জন্য এই প্রজেক্টের সবচেয়ে ভিন্ন "
        "যুক্তি প্রযোজ্য — এটা tidal-influenced deltaic distributary, "
        "তাই flood risk মূলত (১) পদ্মার upstream discharge, এবং (২) "
        "জোয়ার-ভাটার phase-এর ওপর নির্ভরশীল, স্থানীয় soil moisture বা "
        "এমনকি স্থানীয় rainfall-এর prognostic value দুটোই তুলনামূলক কম। "
        "soil moisture কমানো ঠিক আছে, কিন্তু rainfall-এর জায়গায় বরং "
        "upstream Padma discharge trend ও tidal calendar/phase একটা "
        "নতুন feature হিসেবে যোগ করার কথা ভাবা যেতে পারে।"
    ),

    "confluence_note": (
        "মাদারীপুর প্রথমবার Ganges-Padma ব-দ্বীপের একটা distributary "
        "নদী এই প্রজেক্টে যুক্ত করলো — Rajbari (পদ্মা মূল প্রবাহ) থেকে "
        "সরাসরি branch করা আড়িয়াল খাঁ। ভবিষ্যতে Faridpur (যেখান দিয়ে "
        "এই নদী প্রথমে যায়) বা Barisal/Shariatpur (যেখানে এটা Tentulia-য় "
        "মেশে) যোগ হলে পুরো আড়িয়াল খাঁ করিডোর সম্পূর্ণ হবে — এটাও একটা "
        "সম্ভাব্য ভবিষ্যৎ multi-district thread, যমুনা করিডোরের মতোই।"
    ),

    "cross_district_flags": (
        "⚠️ ছোট একটা naming-confusion flag — stations.py-তে "
        "'Haridaspur' (SW198) নামের একটা station-এর river field-এ "
        "'Madaripur BR' (সম্ভবত Madaripur Beel Route) লেখা আছে, কিন্তু "
        "সেই station-এর district আসলে Gopalganj (Gopalganj Sadar "
        "উপজেলা)। এটা কোনো ভুল না — শুধু নদীর নামে 'Madaripur' শব্দ "
        "থাকা আর জেলার নাম 'Madaripur' হওয়া দুইটা আলাদা জিনিস — কিন্তু "
        "ভবিষ্যতে কেউ কোড quickly scan করলে বিভ্রান্ত হতে পারে, তাই এখানে "
        "স্পষ্ট করে নোট রাখা হলো।"
    ),
}