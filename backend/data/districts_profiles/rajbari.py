# ============================================================
# FloodAI — data/district_profiles/rajbari.py
#
# জেলা-বাই-জেলা, স্টেশন-বাই-স্টেশন framework-এর প্রথম pilot।
# উদ্দেশ্য: এখন model.py-তে যে crude approximation গুলো আছে
# (যেমন get_reference_discharge()-এর danger_level*100 হিসাব),
# সেগুলোকে ধীরে ধীরে real, verified, station-level জ্ঞান দিয়ে
# replace করা।
#
# ⚠️ এই ফাইলটা এখনো model.py/app.py এর সাথে wire করা হয়নি —
# শুধু data হিসেবে বানানো হলো, আগে verify করে নেওয়ার জন্য।
# ============================================================

RAJBARI_PROFILE = {
    "district": "রাজবাড়ী",
    "district_lat": 23.76,
    "district_lon": 89.64,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    # শুধু ১টা official FFWC water-level station — Goalondo।
    # (তুলনায় সিলেট/সুনামগঞ্জের মতো জেলায় ৫-৬টা থাকে)
    "station_count": 1,

    "stations": [
        {
            "name": "Goalondo",
            "ffwc_id": "SW91.9R",

            # ── ২. এই স্টেশনে কোন নদী ইম্প্যাক্ট ফেলে ──
            "river": "পদ্মা (Ganges/Padma)",
            "upazila": "Goalanda",
            "union": "Debagram",

            # ── ৩. নদীর স্ট্রাকচার ──
            "river_structure": {
                "category": "mega_trunk",  # river_categories.py-র সাথে সামঞ্জস্যপূর্ণ
                "catchment": (
                    "গঙ্গা নদীর বিশাল transboundary catchment — হিমালয় থেকে "
                    "ভারতের একাধিক রাজ্য হয়ে আসে। Goalondo point-টা ঐতিহাসিকভাবে "
                    "গঙ্গা ও যমুনার সঙ্গমস্থলের কাছে (এখান থেকেই নদীটা 'পদ্মা' নামে "
                    "পরিচিত হয়ে এগিয়ে যায়)।"
                ),
                "flow_behavior": (
                    "ধীরগতির, বড় বাফার — flash river না। উজানের বৃষ্টি/স্নোমেল্ট "
                    "থেকে পিক আসতে সময় লাগে, তাই পূর্বাভাসের জন্য তুলনামূলক ভালো "
                    "সময় (lead time) পাওয়া যায়।"
                ),
                "upstream_reference": "Malda, IN",
                "lag_time_hours": 44,  # flood_config.py-তে যা আছে, তার সাথে মিল
            },

            # ── ৪. ড্যাঞ্জার লেভেল ──
            "danger_level_m": 8.20,   # ✅ FFWC-র লাইভ পেজ থেকে সরাসরি verify করা (২০২৬-০৮-১০)
            "highest_recorded_m": 9.45,  # FFWC পেজে যা দেখানো হচ্ছে
            "verified_source": "old.ffwc.gov.bd (stid=34), যাচাই করা হয়েছে ২০২৬-০৮-১০",
            "verification_note": (
                "flood_config.py-তে আগে থেকেই danger_level=8.2 বসানো ছিল — "
                "এটা সঠিক, FFWC-র সাথে মিলে যাচ্ছে। কিন্তু highest_recorded_m "
                "কোডে কোথাও নেই, নতুন যোগ করা হলো (ভবিষ্যতে 'কত উপরে গেলে "
                "কতটা অস্বাভাবিক' বোঝার রেফারেন্স হিসেবে কাজে লাগবে)।"
            ),

            # ── ML model-এর ১৪ feature-এর মধ্যে যেগুলো verify করা হলো ──
            "ml_features_verified": {
                "reference_discharge_m3s": {
                    "old_buggy_value": 820,       # = danger_level(8.2) * 100 — সম্পূর্ণ ভুল
                    "corrected_estimate": 75000,  # bankfull (আগে ভুলবশত mean annual ৩০,০০০ বসানো ছিল, danger-level threshold হিসেবে bankfull বেশি যুক্তিসঙ্গত)  # Padma-র real mean annual discharge
                    "corrected_range": "mean ~৩০,০০০ m³/s, bankfull ~৭৫,০০০ m³/s",
                    "source": (
                        "Neill, 'Some hydrotechnical features of Padma River, "
                        "Bangladesh' (mean ~30,000 m³/s, bankfull ~75,000 m³/s, "
                        "100-yr flood ~130,000 m³/s); Wikipedia Padma River "
                        "(1971-2000 average discharge 34,938 m³/s)"
                    ),
                    "note": (
                        "⚠️ এই সংখ্যাটা danger_level(8.2m)-এর প্রায় ৩৭ গুণ বড় — "
                        "পুরনো `danger_level * 100` সূত্র বাস্তব হাইড্রোলজি থেকে "
                        "কয়েকশো গুণ দূরে ছিল। Goalondo সরাসরি গঙ্গা-যমুনা সঙ্গমস্থলে, "
                        "তাই এখানে Padma-র (শুধু গঙ্গার না) combined discharge "
                        "ব্যবহার করা ঠিক হবে।"
                    ),
                    "critical_caveat": (
                        "⚠️⚠️ train_model.py-র synthetic training data-ও একই "
                        "`danger_level*100` সূত্র দিয়ে discharge_ratio জেনারেট "
                        "করেছে (comment: 'রুল ইঞ্জিনের সাথে একই scientific "
                        "assumption শেয়ার করার জন্য')। মানে শুধু model.py-তে "
                        "reference_discharge বদলালে runtime discharge_ratio "
                        "হঠাৎ inference-এর সময় model যা train-এ দেখেছে তার চেয়ে "
                        "অনেক ছোট হয়ে যাবে (কারণ denominator ৩৭ গুণ বড় হলে "
                        "ratio ৩৭ গুণ ছোট হয়) — ML model সেটাকে ভুল বুঝবে। "
                        "তাই শুধু রাজবাড়ীতে এই সংখ্যা বসালেই চলবে না — হয় "
                        "সব জেলার জন্য reference_discharge নতুন করে (per-river "
                        "real data দিয়ে) বসিয়ে model retrain করতে হবে, নয়তো "
                        "আপাতত rule-based override (riverine.py) স্তরেই এই "
                        "সংখ্যা ব্যবহার করে ML prediction-কে override করতে হবে।"
                    ),
                },
                "cn": {
                    "old_value": 76,  # flood_config.py-তে যা ছিল (নির্দিষ্ট source ছাড়া)
                    "reviewed_estimate": 89,
                    "reasoning": (
                        "SCS Curve Number পদ্ধতিতে Bangladesh-এর পলিমাটির প্লাবনভূমি "
                        "(silty clay, ধান চাষ, Hydrologic Soil Group C/D)-এর জন্য "
                        "সাধারণত 'row crop/paddy, poor hydrologic condition' "
                        "ক্যাটেগরিতে CN≈৮৮-৯১ পড়ে (TR-55 স্ট্যান্ডার্ড টেবিল অনুযায়ী)। "
                        "বর্ষায় জমি আগে থেকেই ভেজা/স্যাচুরেটেড থাকায় ৭৬ (যা 'ভালো "
                        "hydrologic condition'-এর কাছাকাছি) কম মনে হচ্ছে।"
                    ),
                    "confidence": "moderate — literature-based estimate, স্থানীয় soil survey data দিয়ে verify করা ভালো হবে",
                },
                "risk_category": {
                    "old_value": "মাঝারি",
                    "reviewed_estimate": "উচ্চ",
                    "reasoning": (
                        "ঐতিহাসিক রেকর্ড অনুযায়ী রাজবাড়ী ১৯৮৮, ১৯৯৮, ২০০৪, ২০২০ — "
                        "একাধিক বড় বন্যায় ক্ষতিগ্রস্ত হয়েছে, এবং এটা গঙ্গা-যমুনা "
                        "সঙ্গমস্থলের ঠিক কাছে হওয়ায় নদীভাঙনও তীব্র (bank erosion "
                        "বছরে ১০০ মিটারের বেশি হতে পারে সক্রিয় char এলাকায়)। "
                        "'মাঝারি' এই ইতিহাসের তুলনায় কম মনে হচ্ছে।"
                    ),
                    "source": "Rajbari District hydrology/flood-history literature (১৯৮৮/১৯৯৮/২০০৪/২০২০ বন্যা, char erosion studies)",
                },
            },

            # ── ৫. কী ধরনের বন্যা হয় ──
            "flood_type": "Riverine",
            "flood_type_note": (
                "ক্লাসিক ধীরগতির riverine বন্যা — সাধারণত আগস্ট-সেপ্টেম্বরে "
                "পিক হয়, যখন গঙ্গা ও যমুনা দুটোরই monsoon flow একসাথে বেশি থাকে। "
                "Flash flood/tidal/dam-release টাইপের সাথে সম্পর্ক নেই। "
                "⚠️ তবে চর/নদীভাঙন এই জেলার একটা বাড়তি বাস্তবতা — danger level "
                "না ছুঁলেও পদ্মার তীরবর্তী চরাঞ্চলে ভাঙন/জলাবদ্ধতা হতে পারে, "
                "এটা water-level model দিয়ে ধরা পড়বে না।"
            ),

            # ── ৬. পানি বাড়লে কতটুকু এলাকা প্লাবিত হয় ──
            # ⚠️ এখনো real rating curve / DEM-ভিত্তিক তথ্য নেই।
            # আপাতত danger-level-exceedance অনুযায়ী rough band — এটা placeholder,
            # future-এ DFO/Sentinel imagery দিয়ে calibrate করা দরকার।
            "inundation_bands": {
                "0_to_50cm_above_danger": "Goalanda/নিম্নাঞ্চল চরের কিছু অংশ, নিচু কৃষিজমি",
                "50cm_to_1m_above_danger": "গোয়ালন্দ উপজেলার আরো বিস্তৃত অংশ, চরাঞ্চলের বসতি",
                "above_1m_danger": "ব্যাপক প্লাবন — রাজবাড়ী সদরের কাছাকাছি এলাকাও ঝুঁকিতে",
                "status": "⚠️ placeholder — real measurement/DEM/DFO archive দিয়ে calibrate করা বাকি",
            },
        },
    ],

    # ── ৭. Soil moisture-এর priority কমানো ──
    "soil_moisture_weight_note": (
        "এই জেলার (Riverine, mega_trunk river) জন্য soil_moisture-কে "
        "primary driver না রেখে discharge/water-level trend-কেই মূল "
        "নির্ধারক করা উচিত — soil moisture শুধু tie-breaker/secondary "
        "signal হিসেবে থাকবে।"
    ),

    "confluence_note": (
        "⚠️ রাজবাড়ী flood_types/riverine.py-এর PADMA_REFERENCE_DISTRICT — "
        "app.py-র get_confluence_data() এই জেলার danger_level ব্যবহার করে "
        "get_reference_discharge() (= danger_level * 100 = 820 m³/s) বানায়, "
        "যেটা পদ্মার real monsoon discharge (৪০,০০০-৮০,০০০ m³/s)-এর তুলনায় "
        "বহু গুণ কম — এটাই confluence bug-এর মূল কারণ। এই profile ব্যবহার করে "
        "fix করার সময় এই reference-discharge হিসাবটাই সবচেয়ে আগে বদলানো দরকার।"
    ),
}