# ============================================================
# FloodAI — data/district_profiles/faridpur.py
#
# জেলা-বাই-জেলা framework-এর ৪র্থ জেলা।
#
# ⚠️⚠️ সবচেয়ে গুরুত্বপূর্ণ finding এই জেলায়: ফরিদপুর CONFLUENCE_DISTRICTS
# তালিকায় আছে (riverine.py), কিন্তু এই জেলার একমাত্র monitored FFWC
# station আসলে পদ্মা/গঙ্গার সাথে সরাসরি সংযুক্তই না — নিচে বিস্তারিত।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

FARIDPUR_PROFILE = {
    "district": "ফরিদপুর",
    "district_lat": 23.60,
    "district_lon": 89.83,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 1,

    "stations": [
        {
            "name": "Faridpur",
            "ffwc_id": "SW168",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "কুমার (Kumar)",
            "upazila": "Faridpur Sadar",
            "union": "Aliabad",

            # ── ৩. নদীর স্ট্রাকচার — ⚠️ এখানেই সবচেয়ে বড় finding ──
            "river_structure": {
                "category": "small (disconnected distributary — mega_trunk বা large_regional না)",
                "catchment": (
                    "⚠️⚠️ Banglapedia অনুযায়ী: 'The origin of the Kumar has been "
                    "disconnected from the Nabaganga after commissioning of the "
                    "Ganges-Kobadak (G-K) irrigation project. As a result, the "
                    "Kumar is now turned into a narrow channel. The only source "
                    "of the river is excess water from the G-K project and "
                    "local rainwater.' — মানে কুমার নদী এখন আর সরাসরি গঙ্গা/পদ্মার "
                    "trunk flow-এর অংশ না, এটা মূলত সেচ প্রকল্পের উদ্বৃত্ত পানি ও "
                    "স্থানীয় বৃষ্টিনির্ভর একটা সংকীর্ণ চ্যানেল (মোট দৈর্ঘ্য ~১৪৪ কিমি)।"
                ),
                "flow_behavior": (
                    "ছোট, ধীর, rainfall/irrigation-excess নির্ভর — পদ্মার মতো "
                    "trunk river discharge dynamics এখানে প্রযোজ্য না।"
                ),
                "upstream_reference": "Malda, IN",  # flood_config.py-তে যা আছে — কিন্তু নিচে caveat দেখুন
                "upstream_reference_caveat": (
                    "⚠️ flood_config.py-তে upstream='Malda,IN' বসানো আছে (রাজবাড়ীর "
                    "মতোই), কিন্তু কুমার যেহেতু এখন Ganges/Padma-র সাথে সরাসরি "
                    "সংযুক্ত না, Malda-র upstream rain data এই নদীর জন্য কতটা "
                    "প্রাসঙ্গিক সেটা প্রশ্নসাপেক্ষ। local_rain-ই সম্ভবত এখানে "
                    "upstream_rain-এর চেয়ে বেশি গুরুত্বপূর্ণ predictor।"
                ),
                "lag_time_hours": 46,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 7.05,  # ✅ FFWC verify করা (SW168, ২০২৬-০৮-১০)
            "highest_recorded_m": 8.70,
            "verified_source": "old.ffwc.gov.bd (stid=23/21), যাচাই করা হয়েছে ২০২৬-০৮-১০ — flood_config.py-র সাথে মিলেছে",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 705,  # danger_level(7.05)*100
                    "corrected_estimate": 800,
                    "corrected_range": (
                        "⚠️ নির্দিষ্ট published discharge measurement পাওয়া যায়নি — "
                        "কুমার এত ছোট ও disconnected যে এটা প্রায় কোনো major "
                        "hydrology paper-এ আলাদাভাবে পরিমাপ করা হয়নি। river_categories.py-র "
                        "'small' ক্যাটেগরি ধরে conservative অনুমান।"
                    ),
                    "source": "Banglapedia (Kumar River entry) — শুধু qualitative বর্ণনা, quantitative discharge নেই",
                    "confidence": "low — এই প্রোফাইলে সবচেয়ে দুর্বল সংখ্যা, কারণ real data খুঁজে পাওয়া যায়নি",
                    "note": (
                        "যেহেতু পুরনো buggy সূত্র (danger_level*100=705) আর নতুন অনুমান "
                        "(৮০০) কাছাকাছি সংখ্যা — এই ছোট/disconnected নদীর ক্ষেত্রে crude "
                        "সূত্রটা accidentally খুব বেশি ভুল না-ও হতে পারে। এটা রাজবাড়ী/"
                        "মানিকগঞ্জ/মুন্সিগঞ্জের (mega_trunk, ৩০-১০০ গুণ ভুল) থেকে "
                        "সম্পূর্ণ আলাদা ধরনের keস — ছোট নদীতে বাগ কম মারাত্মক।"
                    ),
                },
                "cn": {
                    "old_value": 77,
                    "reviewed_estimate": 82,
                    "reasoning": (
                        "irrigation project excess water + local rainfall নির্ভর "
                        "channel — বড় পদ্মা floodplain-এর চেয়ে soil/land-use ভিন্ন "
                        "হতে পারে, তাই ৮৯ (পদ্মা floodplain) না বসিয়ে একটু কম "
                        "রক্ষণশীল মান রাখা হলো। এটাও literature-confirmed না, শুধু "
                        "যুক্তিসঙ্গত অনুমান।"
                    ),
                    "confidence": "low",
                },
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "মাঝারি (অপরিবর্তিত)",
                    "reasoning": (
                        "রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জের মতো ঐতিহাসিক বড় বন্যার তথ্য "
                        "কুমার নদী নিয়ে খুঁজে পাওয়া যায়নি (কারণ এটা ছোট, স্থানীয় "
                        "নদী) — তাই upgrade করার মতো justification নেই, 'মাঝারি'ই "
                        "রাখা হলো।"
                    ),
                    "source": None,
                },
            },

            "flood_type": "Riverine (small/local — কিন্তু প্রকৃতিতে rain/irrigation-excess নির্ভর, classic trunk-river riverine না)",
            "flood_type_note": (
                "⚠️ এটা রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জের মতো 'classic mega-trunk "
                "riverine' না — বরং ছোট নদীর local flooding-এর কাছাকাছি প্যাটার্ন। "
                "flood_config.py-তে 'Riverine' লেখা আছে, কারিগরিভাবে ভুল না হলেও "
                "misleading — কারণ এটা বোঝায় Ganges/Padma trunk-এর behavior, যা "
                "আসলে প্রযোজ্য না।"
            ),

            "inundation_bands": {
                "status": "⚠️ placeholder নেই — এমনকি rough band তৈরির মতো তথ্যও খুঁজে পাওয়া যায়নি এই ছোট নদীর জন্য",
            },
        },
    ],

    # ── ৭. Soil moisture-এর priority ──
    "soil_moisture_weight_note": (
        "⚠️ এখানে উল্টো যুক্তি — রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জে যেখানে "
        "discharge/water-level primary হওয়া উচিত বলেছি, ফরিদপুরের কুমার নদীতে "
        "যেহেতু flow-ই মূলত local rainfall+irrigation-excess নির্ভর, তাই "
        "local_rain আর soil_moisture-এর গুরুত্ব হয়তো *কমানো ঠিক হবে না* — "
        "বরং discharge_ratio (যেটা trunk-river assumption-এর উপর বানানো) এই "
        "স্টেশনের জন্য কম অর্থবহ হতে পারে।"
    ),

    "confluence_note": (
        "⚠️⚠️ এইটাই সবচেয়ে বড় সমস্যা — ফরিদপুর riverine.py-র CONFLUENCE_DISTRICTS "
        "তালিকায় আছে, মানে রাজবাড়ী(পদ্মা)+মানিকগঞ্জ(যমুনা)-এর ratio >1 হলে এই "
        "জেলাতেও +15/100 boost প্রযোজ্য হয়। কিন্তু ফরিদপুরের একমাত্র monitored "
        "station (কুমার) বাস্তবে পদ্মা/যমুনার সাথে সংযুক্তই না (Ganges-Kobadak "
        "প্রজেক্টের পর বিচ্ছিন্ন)! মানে ফরিদপুরের কুমার নদী পুরোপুরি স্বাভাবিক/শুকনো "
        "থাকলেও, শুধু রাজবাড়ী-মানিকগঞ্জে পদ্মা-যমুনা একসাথে বেশি থাকলেই ফরিদপুরকে "
        "'বিপদ' দেখানো হতে পারে — এটা রাজবাড়ী/মানিকগঞ্জ/মুন্সিগঞ্জে যে bug পেয়েছি "
        "তার চেয়েও বেশি গুরুতর, কারণ এখানে ভৌগোলিক যুক্তিটাই দুর্বল (ফরিদপুর সদর "
        "শহর পদ্মার তীরে না, কুমার নদীর তীরে)।"
    ),
}