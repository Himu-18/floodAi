# ============================================================
# FloodAI — data/district_profiles/comilla.py
#
# জেলা-বাই-জেলা framework-এর ১২তম জেলা — গোমতী নদী, ত্রিপুরার ডুম্বুর
# বাঁধ প্রসঙ্গে ২০২৪-এর আলোচিত বন্যা (ভারত-বাংলাদেশ বিতর্ক সহ)।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

COMILLA_PROFILE = {
    "district": "কুমিল্লা",
    "district_lat": 23.46,
    "district_lon": 91.18,

    "station_count": 2,

    "stations": [
        {
            "name": "Comilla",
            "ffwc_id": "SW110",
            "is_primary": True,

            "river": "গোমতী (Gumti)",
            "upazila": "Comilla Sadar",
            "union": "Panchthubi",

            "river_structure": {
                "category": "medium/large_regional",
                "catchment": (
                    "গোমতী ত্রিপুরার (ভারত) পাহাড় থেকে উৎপন্ন, ডুম্বুর জলাধার "
                    "(বাঁধ) হয়ে বাংলাদেশ সীমান্তের ১২০ কিমি উজানে থেকে আসে। "
                    "⚠️ গুরুত্বপূর্ণ তথ্য: বাংলাদেশি পানি বিশেষজ্ঞ M. Inamul Haque "
                    "(Institute of Water and Environment) অনুযায়ী ডুম্বুর বাঁধ "
                    "গোমতীর মোট catchment-এর মাত্র ~২০% নিয়ন্ত্রণ করে — বাকি ৮০% "
                    "অনিয়ন্ত্রিত বৃষ্টিপাত-নির্ভর।"
                ),
                "flow_behavior": "মাঝারি আকারের transboundary নদী, বাঁধ + বৃষ্টি উভয়ের সম্মিলিত প্রভাবে flash-flood-প্রবণ",
                "upstream_reference": "Agartala, IN",  # ✅ যুক্তিসঙ্গত — ত্রিপুরার রাজধানী, ভৌগোলিকভাবে কাছাকাছি
                "lag_time_hours": 16,
            },

            "danger_level_m": 11.30,  # ✅ FFWC verify করা — flood_config.py-র সাথে মিলেছে
            "highest_recorded_m": 12.50,
            "verified_source": (
                "Scroll.in/Wikipedia (আগস্ট ২০২৪ বন্যার বিস্তারিত কভারেজ) — "
                "২৩ আগস্ট ২০২৪-এ ১২.৫০ মিটারে পৌঁছেছিল, যা BWDB-র ১৯৮৮-২০২৪ (৩৭ "
                "বছরের) তথ্য বিশ্লেষণ অনুযায়ী **সর্বোচ্চ রেকর্ড** — আগে কখনো এত "
                "উপরে ওঠেনি।"
            ),

            "political_context_note": (
                "⚠️ এই নদীতে ২০২৪ সালের আগস্টে একটা রাজনৈতিকভাবে বিতর্কিত ঘটনা "
                "ঘটেছিল — কুমিল্লা, ফেনী, নোয়াখালী সহ ১১ জেলায় ভয়াবহ বন্যা হয়, "
                "যাতে ৫৮ লক্ষ মানুষ ক্ষতিগ্রস্ত হয়। বাংলাদেশের কিছু গণমাধ্যম দাবি "
                "করেছিল ভারতের ডুম্বুর বাঁধের গেট হঠাৎ খুলে দেওয়ার কারণে এটা "
                "হয়েছে; ভারতের পররাষ্ট্র মন্ত্রণালয় এই দাবি অস্বীকার করে বলেছিল "
                "এটা মূলত catchment এলাকায় (ত্রিপুরাতেও) অতিভারী বৃষ্টিপাতের ফল, "
                "বাঁধের কোনো ভূমিকা নেই। ত্রিপুরার একজন কর্মকর্তা বলেছেন গত ৫০ "
                "বছর ধরে ডুম্বুর বাঁধ 'স্বয়ংক্রিয়ভাবে' খোলে (কোনো manual gate "
                "operation ছাড়াই)। এই বিষয়ে ভিন্ন ভিন্ন সূত্র ভিন্ন ভিন্ন দাবি "
                "করছে — এই profile কোনো পক্ষ নিচ্ছে না, শুধু তথ্যটা নথিভুক্ত "
                "রাখছে কারণ এটা flood_type='Dam-Affected' classification-এর "
                "প্রাসঙ্গিক প্রেক্ষাপট।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 1130,  # danger_level(11.3)*100
                    "corrected_estimate": 1500,
                    "corrected_range": (
                        "⚠️ নির্দিষ্ট mean/bankfull discharge পাওয়া যায়নি। ডুম্বুর "
                        "বাঁধের spillway capacity ৪৮১.৩৮ cumecs (m³/s) জানা গেছে "
                        "(SANDRP রিপোর্ট) — কিন্তু এটা শুধু বাঁধের ২০% catchment-এর "
                        "ক্ষমতা, মোট নদীর flood discharge এর চেয়ে অনেক বেশি হওয়ার "
                        "কথা (২০২৪-এর রেকর্ড বন্যা বিবেচনায়)।"
                    ),
                    "source": "SANDRP (Dumbur dam spillway capacity); Scroll.in (২০২৪ বন্যার বিস্তারিত)",
                    "confidence": "low — সরাসরি নদীর discharge measurement পাওয়া যায়নি, শুধু বাঁধের capacity থেকে আনুমানিক bound",
                },
                "cn": {"old_value": 79, "reviewed_estimate": 84, "reasoning": "পাহাড়ি উৎস + নিচে সমতল কৃষিজমি — মিশ্র characteristic, moderate-high CN যুক্তিসঙ্গত", "confidence": "low-moderate"},
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "২০২৪ সালে ৩৭ বছরের রেকর্ড ভেঙে সর্বোচ্চ জলস্তর, ১১ জেলা "
                        "জুড়ে ৫৮ লক্ষ মানুষ ক্ষতিগ্রস্ত, শত শত মৃত্যু — 'মাঝারি' "
                        "কোনোভাবেই যথেষ্ট না।"
                    ),
                    "source": "Wikipedia (August 2024 Bangladesh floods), Scroll.in",
                },
            },

            "flood_type": "Dam-Affected",
            "flood_type_note": (
                "⚠️ নুয়ান্সড — 'Dam-Affected' লেবেল আংশিক সত্য (ডুম্বুর বাঁধ আছে, "
                "flow-এ প্রভাব ফেলে), কিন্তু বাংলাদেশি বিশেষজ্ঞের মতে বাঁধ মাত্র "
                "২০% catchment নিয়ন্ত্রণ করে — বাকি ৮০% pure rainfall-driven। "
                "তাই এটা 'Dam-Affected' আর 'Riverine/Flash-Flood'-এর মিশ্রণ, "
                "শুধু dam-driven ধরে নেওয়া ভুল ব্যাখ্যা দিতে পারে।"
            ),

            "inundation_bands": {
                "affected_areas": "কুমিল্লা সদর, দেবিদ্বার, মুরাদনগর, দাউদকান্দি (২০২৪ বন্যায় সব ক্ষতিগ্রস্ত)",
                "status": "⚠️ placeholder — DEM/DFO calibration বাকি, তবে ২০২৪ বন্যার scale একটা বাস্তব রেফারেন্স পয়েন্ট দেয়",
            },
        },
        {
            "name": "Debidwar",
            "ffwc_id": "SW114",
            "is_primary": False,

            "river": "গোমতী (Gumti)",
            "upazila": "Debidwar",
            "union": None,

            "river_structure": {"category": "medium/large_regional", "catchment": "Comilla station-এর একটু ভাটিতে, একই গোমতী", "flow_behavior": "Comilla-র মতোই", "upstream_reference": "Agartala, IN", "lag_time_hours": 16},

            "danger_level_m": 8.05,  # ✅ FFWC verify করা
            "highest_recorded_m": 8.58,  # 2024 flood: "53cm above danger" per Wikipedia
            "verified_source": "Wikipedia (August 2024 Bangladesh floods) — ২০২৪ বন্যায় ৮.৫৮ মিটারে পৌঁছেছিল, danger-এর ৫৩cm উপরে",

            "gap_found": "⚠️ এই station stations.py-তে আছে কিন্তু flood_config.py-র কুমিল্লার rivers লিস্টে নেই (শুধু Comilla/SW110 আছে) — মুন্সিগঞ্জের Mawa-র মতো একই প্যাটার্নের গ্যাপ।",

            "ml_features_verified": {
                "reference_discharge_m3s": {"old_buggy_value": 805, "corrected_estimate": 1000, "confidence": "low — Comilla station-এর অনুরূপ ধরা হয়েছে"},
                "cn": {"old_value": None, "reviewed_estimate": 84, "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "উচ্চ", "reasoning": "২০২৪ বন্যায় সরাসরি প্রভাবিত হয়েছিল, Comilla station-এর অনুরূপ ঝুঁকি"},
            },

            "flood_type": "Dam-Affected",
            "inundation_bands": {"status": "⚠️ placeholder — Comilla station-এর অনুরূপ ধরা যায়"},
        },
    ],

    "soil_moisture_weight_note": "মিশ্র নদী (dam + rainfall উভয়) — soil_moisture কমানোর স্পষ্ট যুক্তি নেই, বরং dam-release তথ্য (এখন model-এ নেই) এবং local+upstream rainfall দুটোই সমান গুরুত্বপূর্ণ রাখা উচিত।",

    "confluence_note": "কুমিল্লা riverine.py-র CONFLUENCE_DISTRICTS-এ নেই।",

    "cross_district_note": "এই গবেষণা ব্রাহ্মণবাড়িয়ার জন্য আংশিক reuse করা যাবে (একই গোমতী/তিতাস অববাহিকা অঞ্চল)।",
}