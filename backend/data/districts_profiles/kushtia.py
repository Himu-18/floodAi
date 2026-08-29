# ============================================================
# FloodAI — data/district_profiles/kushtia.py — জেলা #২৭
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

KUSHTIA_PROFILE = {
    "district": "কুষ্টিয়া", "district_lat": 23.90, "district_lon": 89.12,
    "station_count": 2, "station_count_note": "✅ দুইটা station-ই flood_config.py-তে সঠিকভাবে linked।",
    "stations": [
        {
            "name": "Talbaria", "ffwc_id": "SW91", "is_primary": False,
            "river": "গঙ্গা (Ganges)", "upazila": "Mirpur", "union": None,
            "river_structure": {
                "category": "mega_trunk (real গঙ্গা mainstem, হার্ডিঞ্জ ব্রিজের ১৯ কিমি ভাটিতে, গড়াইয়ের offtake পয়েন্টের কাছেই)",
                "catchment": "রাজবাড়ীর পদ্মার একই গঙ্গা trunk, কিন্তু এখানে গড়াই আলাদা হয়ে যাওয়ার ঠিক আগের পয়েন্ট",
                "upstream_reference": "Malda, IN", "lag_time_hours": 42,
            },
            "danger_level_m": 13.05, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 1305, "corrected_estimate": 75000, "corrected_range": "bankfull — রাজবাড়ীর গঙ্গা/পদ্মা রেফারেন্স reuse, একই trunk river (⚠️ ২০২৬-০৮-২৮: আগে এখানে stale ৩০,০০০ ছিল — রাজবাড়ীর reference mean-annual থেকে bankfull-এ ঠিক করার সময় এই কপি sync হয়নি, ধরা পড়ল basin-by-basin যাচাইয়ে)", "source": "রাজবাড়ী profile (Neill et al., bankfull)", "confidence": "moderate-high"},
                "cn": {"old_value": None, "reviewed_estimate": 88, "confidence": "moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "mega_trunk গঙ্গার সরাসরি সংস্পর্শ"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
        {
            "name": "Gorai-RB", "ffwc_id": "SW99", "is_primary": True,
            "river": "গড়াই (Gorai)", "upazila": "Kumarkhali", "union": None,
            "river_structure": {
                "category": "large_regional (গঙ্গার প্রধান distributary — দক্ষিণ-পশ্চিম বাংলাদেশের একমাত্র মিঠাপানির উৎস)",
                "catchment": (
                    "Banglapedia: গড়াই তালবাড়িয়া থেকে (হার্ডিঞ্জ ব্রিজের ১৯ কিমি ভাটিতে) "
                    "গঙ্গা থেকে বিচ্ছিন্ন হয়। দৈর্ঘ্য ১৯৯ কিমি, catchment ১৫,১৬০ বর্গকিমি। "
                    "⚠️⚠️ ভারতের ফারাক্কা ব্যারাজ (১৯৭৫) চালুর পর শুষ্ক মৌসুমের discharge "
                    "নাটকীয়ভাবে কমে গেছে — ১৯৬০-এর দশকে গড় সর্বনিম্ন ~১১০ m³/s ছিল, এখন "
                    "মাত্র ~১০ m³/s (Gorai Railway Bridge পয়েন্টে) — এক দশকের মধ্যেই "
                    "magnitude-এর একটা order কমে গেছে!"
                ),
                "flow_behavior": "চরম মৌসুমি তারতম্য — শুষ্ক মৌসুমে ০-১৭০ m³/s, বর্ষায় ৪,০০০-৮,৮৮০ m³/s",
                "upstream_reference": "Malda, IN", "lag_time_hours": 42,
            },
            "danger_level_m": 12.30, "verified_source": "flood_config.py-র সাথে মিলেছে",
            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1230, "corrected_estimate": 5000,
                    "corrected_range": "শুষ্ক মৌসুম ০-১৭০ m³/s, বর্ষা ৪,০০০-৮,৮৮০ m³/s — flood risk-এর জন্য বর্ষার সংখ্যাই প্রাসঙ্গিক",
                    "source": "ResearchGate (Farakka impact studies, Gorai Restoration Project reports)",
                    "confidence": "moderate-high — একাধিক academic source থেকে সামঞ্জস্যপূর্ণ সংখ্যা",
                    "note": "⚠️ এই নদীতে ফারাক্কা বাঁধের প্রভাব অত্যন্ত well-documented এবং politically sensitive (ভারত-বাংলাদেশ পানি বণ্টন চুক্তির কেন্দ্রীয় বিষয়) — কোনো একপক্ষের দাবি ছাড়াই শুধু academic measurement তথ্য এখানে রাখা হলো।",
                },
                "cn": {"old_value": 75, "reviewed_estimate": 87, "reasoning": "প্লাবনভূমি কৃষিজমি, TR-55 অনুযায়ী বাড়ানো উচিত", "confidence": "moderate"},
                "risk_category": {"old_value": "মাঝারি", "reviewed_estimate": "মাঝারি (অপরিবর্তিত)", "reasoning": "শুষ্ক মৌসুমে almost dry, বর্ষায় significant flood risk — সিজনাল ভারসাম্যে 'মাঝারি' যুক্তিসঙ্গত"},
            },
            "flood_type": "Riverine", "inundation_bands": {"status": "⚠️ placeholder"},
        },
    ],
    "soil_moisture_weight_note": "Farakka-প্রভাবিত distributary — discharge_ratio-র মৌসুমি ভিন্নতা (শুষ্ক বনাম বর্ষা) অত্যন্ত grNoticeable, একটামাত্র reference_discharge দিয়ে সারা বছর মডেল করা কঠিন।",
    "confluence_note": "CONFLUENCE_DISTRICTS-এ নেই, কিন্তু Talbaria station সরাসরি গঙ্গা trunk-এর সাথে সংযুক্ত হওয়ায় রাজবাড়ীর confluence bug-এর প্যাটার্ন এখানেও প্রাসঙ্গিক।",
    "cross_district_note": "গড়াই/মধুমতী সিস্টেম মাগুরা, নড়াইল, ফরিদপুর, খুলনা, বরিশাল পর্যন্ত বিস্তৃত (৩৭১ কিমি) — নবগঙ্গা (ঝিনাইদহ) বোরদিয়া পয়েন্টে গড়াই থেকে branch করে। কুমার (ফরিদপুর, আগে profile করা) এই একই সিস্টেমের অংশ — কালিগঙ্গা (গড়াইয়ের প্রথম শাখা, শৈলকুপার কাছে) কুমারের সাথে মেশে।",
}