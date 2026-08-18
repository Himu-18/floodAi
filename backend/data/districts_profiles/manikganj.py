# ============================================================
# FloodAI — data/district_profiles/manikganj.py
#
# জেলা-বাই-জেলা framework-এর ২য় জেলা। রাজবাড়ীর সাথে হুবহু একই ৭-ধাপ
# পদ্ধতি অনুসরণ করা হয়েছে (দেখুন rajbari.py)।
#
# ⚠️ গুরুত্বপূর্ণ: মানিকগঞ্জ flood_types/riverine.py-র JAMUNA_REFERENCE_DISTRICT —
# রাজবাড়ী (পদ্মা রেফারেন্স) + মানিকগঞ্জ (যমুনা রেফারেন্স) — এই দুইটা একসাথে
# হলেই confluence bug সম্পূর্ণ fix করা সম্ভব হবে।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

MANIKGANJ_PROFILE = {
    "district": "মানিকগঞ্জ",
    "district_lat": 23.86,
    "district_lon": 90.00,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # ৩টা station — রাজবাড়ীর (১টা) চেয়ে বেশি জটিল, কারণ প্রধান trunk নদী
    # (যমুনা) ছাড়াও দুইটা distributary/tributary নদী এই জেলার মধ্য দিয়ে যায়
    "station_count": 3,

    "stations": [
        {
            "name": "Aricha",
            "ffwc_id": "SW50.6",
            "is_primary": True,

            # ── ২. নদী ──
            "river": "যমুনা (Jamuna/Brahmaputra)",
            "upazila": "Shibalaya",
            "union": "Teota",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",
                "catchment": (
                    "ব্রহ্মপুত্রের catchment ~৫,৮০,০০০ বর্গকিমি (তিব্বত+ভারত+বাংলাদেশ), "
                    "বিশ্বের সপ্তম বৃহত্তম নদী discharge-এর দিক থেকে। Aricha পয়েন্টটা "
                    "যমুনা যেখানে পদ্মার সাথে মিশে (Goalondo-র কাছাকাছি) তার ঠিক উজানে — "
                    "রাজবাড়ীর confluence-এর অপর পাশ।"
                ),
                "flow_behavior": (
                    "মহা-trunk নদীর মতোই ধীরগতির/বড় বাফার, কিন্তু যমুনা braided এবং "
                    "অত্যন্ত অস্থির (channel migration, bank erosion) — পদ্মার চেয়েও "
                    "বেশি ভাঙন-প্রবণ।"
                ),
                "upstream_reference": "Malda, IN",  # flood_config.py অনুযায়ী
                "lag_time_hours": 42,
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 8.95,  # ✅ FFWC verify করা (old.ffwc.gov.bd, stid=38)
            "highest_recorded_m": 9.90,
            "verified_source": "old.ffwc.gov.bd (stid=38), যাচাই করা হয়েছে ২০২৬-০৮-১০",
            "verification_note": (
                "flood_config.py-তে danger_level=8.95 আগে থেকেই সঠিক ছিল। "
                "⚠️ তবে একটা academic paper (Flow Characteristics of the Jamuna "
                "River, 1988/1998 flood study) একই Aricha station-এর danger "
                "level 9.14m বলছে — সম্ভবত পুরনো gauge datum বা ঐ সময়ের হিসাব। "
                "এখন FFWC live-এ যা আছে (8.95) সেটাই authoritative হিসেবে ধরা হলো।"
            ),

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 895,        # danger_level(8.95)*100
                    "corrected_estimate": 50000,   # bankfull discharge (mid-estimate)
                    "corrected_range": (
                        "mean annual ~২০,০০০-২১,২০০ m³/s (Bahadurabad গেজ), "
                        "মৌসুমি গড় ~৪০,০০০-৫০,০০০ m³/s, bankfull ~৪৫,০০০-৬০,০০০ m³/s, "
                        "রেকর্ড পিক ১,০২,৫০০ m³/s (১৯৯৮ বন্যা)"
                    ),
                    "source": (
                        "Best et al. 2022 (mean 20,200 m³/s); Banglapedia Jamuna "
                        "River (মৌসুমি গড় ৪০,০০০ cumec, সর্বোচ্চ ৯৮,৬০০ cumec "
                        "১৯৮৮); FAP24 1996/Thorne et al. 1993 (bankfull 45,000-60,000)"
                    ),
                    "cross_check": (
                        "✅ river_categories.py-তে মানিকগঞ্জ=mega_trunk, রেঞ্জ "
                        "(10,000-200,000 m³/s) — আমাদের ৫০,০০০ estimate এই রেঞ্জের "
                        "মধ্যেই পড়ছে। রাজবাড়ীর পদ্মা estimate (৩০,০০০)-ও একই রেঞ্জে "
                        "পড়েছিল — ভালো consistency signal।"
                    ),
                    "critical_caveat": (
                        "রাজবাড়ীর মতোই — train_model.py-র synthetic data একই "
                        "danger_level*100 সূত্র দিয়ে বানানো, তাই শুধু এখানে বদলালে "
                        "ML model-এর inference input distribution training-এর "
                        "সাথে না মিলে ভুল prediction দেবে। রাজবাড়ী+মানিকগঞ্জ দুইটাই "
                        "শেষ হলে একসাথে retrain/override সিদ্ধান্ত নিতে হবে।"
                    ),
                },
                "cn": {
                    "old_value": 77,
                    "reviewed_estimate": 89,
                    "reasoning": "রাজবাড়ীর মতোই যুক্তি — Bangladesh floodplain paddy/silty-clay soil, HSG C/D, poor hydrologic condition অনুযায়ী CN≈৮৮-৯১ (TR-55)।",
                    "confidence": "moderate — literature-based, স্থানীয় soil-survey verify করা ভালো",
                },
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "১৯৮৮ বন্যায় Aricha-তে যমুনা danger level-এর ১৪১-১৪৪ সেমি উপরে "
                        "উঠেছিল, ৪৩ দিন danger level-এর উপরে ছিল; ১৯৯৮-এ ৬৮ দিন। "
                        "২০০০, ২০০৪, ২০২০ সালেও Manikganj Sadar/Ghior/Daulatpur/"
                        "Harirampur উপজেলা প্লাবিত হয়েছে। এছাড়া Jamuna+Padma+Kaliganga+"
                        "Dhaleshwari — চার নদীর ভাঙনে জেলা 'shrinking' (স্থানীয় "
                        "সংবাদ অনুযায়ী)। 'মাঝারি' যথেষ্ট মনে হচ্ছে না।"
                    ),
                    "source": (
                        "Flow Characteristics of the Jamuna River during 1988/1998 "
                        "(Manikganj case study, hilarispublisher.com); Prothom Alo "
                        "(2020 flood report); TBS News (erosion report, 2020)"
                    ),
                },
            },

            "flood_type": "Riverine",
            "flood_type_note": (
                "ক্লাসিক riverine বন্যা, আগস্ট-সেপ্টেম্বর পিক। রাজবাড়ীর confluence "
                "bug-এর 'অপর পাশ' — riverine.py-র JAMUNA_REFERENCE_DISTRICT এই জেলা।"
            ),

            "inundation_bands": {
                "0_to_50cm_above_danger": "শিবালয়/দৌলতপুর উপজেলার নিচু চরাঞ্চল",
                "50cm_to_1m_above_danger": "হরিরামপুর, ঘিওর, মানিকগঞ্জ সদরের নিম্নাঞ্চল",
                "above_1m_danger": "১৯৮৮/৯৮ স্কেলে — ব্যাপক প্লাবন, জেলার বড় অংশ",
                "status": "⚠️ placeholder — real DEM/DFO calibration বাকি (রাজবাড়ীর মতোই সীমাবদ্ধতা)",
            },
        },
        {
            "name": "Jagir",
            "ffwc_id": "SW68.5",
            "is_primary": False,

            "river": "পুরাতন ধলেশ্বরী (Old Dhaleswari)",
            "upazila": "Manikganj Sadar",
            "union": "Jaigir",

            "river_structure": {
                "category": "small_or_tidal (ঐতিহাসিকভাবে বড় ছিল, এখন সংকুচিত)",
                "catchment": (
                    "যমুনার একটা distributary/offtake — কিন্তু গত কয়েক দশকে flow "
                    "নাটকীয়ভাবে কমে গেছে। ১৯৭০-এর দশকে ~৫,০০০ m³/s থেকে ২০০০-এর "
                    "দশকে ~১,০০০ m³/s-এ নেমেছে, প্রস্থ ২ কিমি থেকে কমে ~০.২ কিমি "
                    "হয়ে গেছে (siltation/avulsion-এর কারণে)।"
                ),
                "flow_behavior": "যমুনার তুলনায় অনেক ছোট ও ধীর, কিন্তু স্থানীয়ভাবে গুরুত্বপূর্ণ",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 7.80,  # ✅ FFWC verify করা (stid=39)
            "highest_recorded_m": 9.15,
            "verified_source": "old.ffwc.gov.bd (stid=39), যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 780,
                    "corrected_estimate": 1200,
                    "corrected_range": "১৯৭০-এর দশকে ~৫,০০০ m³/s, ২০০০-এর দশকে কমে ~১,০০০ m³/s",
                    "source": "Timescales of formative discharge... Jamuna River (Wiley, ESP journal 2025) — Dhaleshwari offtake decline data",
                    "note": (
                        "⚠️ এটা river_categories.py-র কোনো category-তে ঠিক বসে না "
                        "(medium আর small_or_tidal-এর মাঝামাঝি) — কারণ নদীটা নিজেই "
                        "সময়ের সাথে category বদলেছে (বড় থেকে ছোট হয়ে গেছে)। "
                        "confidence মাঝারি — dedicated survey ছাড়া exact সংখ্যা কঠিন।"
                    ),
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "reasoning": "একই floodplain, তাই রাজবাড়ী/Aricha-র মতোই CN ধরা যায়", "confidence": "low-moderate"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "যমুনার তুলনায় ছোট নদী হলেও ২০২০ সালে Manikganj Sadar-এ কালীগঙ্গা+ধলেশ্বরী একসাথে বন্যা করেছিল — সম্পূর্ণ অবহেলার মতো না, কিন্তু Aricha/যমুনার চেয়ে কম গুরুত্বপূর্ণ"},
            },

            "flood_type": "Riverine (secondary/local)",
            "inundation_bands": {"status": "⚠️ placeholder — নেই, ছোট নদী হওয়ায় আরো কম তথ্য পাওয়া গেছে"},
        },
        {
            "name": "Taraghat",
            "ffwc_id": "SW137A",
            "is_primary": False,

            "river": "কালীগঙ্গা (Kaliganga)",
            "upazila": "Manikganj Sadar",
            "union": "Dighi",

            "river_structure": {
                "category": "medium (অনুমান — river_categories.py-তে সরাসরি নেই)",
                "catchment": "স্থানীয় আঞ্চলিক নদী, ঢাকা বিভাগের সমতল এলাকা দিয়ে বয়ে চলা",
                "flow_behavior": "ছোট, কিন্তু ২০২০ সালে সত্যিকারের বন্যা করেছে (Nabagram, Jagir, Putail, Bhararia union)",
                "upstream_reference": None,
                "lag_time_hours": None,
            },

            "danger_level_m": 7.95,  # ✅ FFWC verify করা (stid=37)
            "highest_recorded_m": 9.62,
            "verified_source": "old.ffwc.gov.bd (stid=37), যাচাই করা হয়েছে ২০২৬-০৮-১০",

            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 795,
                    "corrected_estimate": 1500,
                    "corrected_range": "নির্দিষ্ট published data পাওয়া যায়নি — river_categories.py-র 'medium' ক্যাটেগরি রেঞ্জ (20-8000 m³/s)-এর মাঝামাঝি ধরা হলো",
                    "source": None,
                    "confidence": "low — এইটা সবচেয়ে দুর্বল অনুমান এই প্রোফাইলে, dedicated BWDB local gauge data দরকার",
                },
                "cn": {"old_value": None, "reviewed_estimate": 89, "confidence": "low-moderate (একই floodplain assumption)"},
                "risk_category": {"old_value": None, "reviewed_estimate": "মাঝারি", "reasoning": "২০২০-এ প্রকৃত বন্যা করেছে কিন্তু যমুনার মতো নিয়মিত/বড় স্কেলে না"},
            },

            "flood_type": "Riverine (secondary/local)",
            "inundation_bands": {"status": "⚠️ placeholder — নেই"},
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "প্রধান station (Aricha/যমুনা)-এর জন্য discharge/water-level trend primary — "
        "রাজবাড়ীর মতোই যুক্তি। তবে দুইটা ছোট secondary station-এ (Jagir, Taraghat) "
        "যেহেতু discharge ডেটা অনেক কম নির্ভরযোগ্য, ওখানে local_rain এর weight "
        "কিছুটা বেশি রাখা যৌক্তিক হতে পারে — soil moisture এর weight কমানো ঠিক, "
        "কিন্তু rainfall কমানো ঠিক না।"
    ),

    "confluence_note": (
        "✅ মানিকগঞ্জ flood_types/riverine.py-এর JAMUNA_REFERENCE_DISTRICT। "
        "রাজবাড়ী (৩০,০০০-৭৫,০০০ m³/s) + মানিকগঞ্জ (৫০,০০০ m³/s corrected) — "
        "দুইটা reference_discharge-ই এখন literature-verified। Confluence override "
        "fix করার জন্য প্রয়োজনীয় দুইটা সংখ্যাই এখন হাতে আছে।"
    ),
}