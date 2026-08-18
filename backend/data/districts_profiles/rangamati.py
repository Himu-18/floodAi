# ============================================================
# FloodAI — data/district_profiles/rangamati.py
#
# ১৭তম জেলা, এবং এই প্রজেক্টের প্রথম জেলা যেখানে ৭-ধাপ পদ্ধতির ১ম ধাপেই
# ("এই জেলায় কতগুলো FFWC station আছে") উত্তর হলো শূন্য। এটা একটা
# গবেষণা-সীমাবদ্ধতা না, বরং একটা real, উল্লেখযোগ্য gap — সততার সাথে
# document করা হলো, কোনো ভুয়া station data বানানো হয়নি।
#
# ⚠️ মূল finding: রাঙ্গামাটিতে Kaptai বাঁধ থাকা সত্ত্বেও (বাংলাদেশের
# একমাত্র জলবিদ্যুৎ কেন্দ্র, ১১,০০০ বর্গকিমি catchment), FFWC-র public
# monitoring network-এ কর্ণফুলী নদীর একমাত্র station ("Chittagong",
# SW152.2) আছে Chittagong জেলায় — বাঁধের অনেক downstream-এ, প্রায় ৬৫
# কিমি দূরে। রাঙ্গামাটি জেলার ভেতরে (Kaptai Lake-এর ওপরে বা নিচে) কোনো
# public water-level station নেই।
#
# flood_config.py-তে রাঙ্গামাটির entry আগে থেকেই আছে কিন্তু
# 'ffwc_station: None, ffwc_verified: False' — এটা honest ছিল,
# placeholder guess হিসেবেই চিহ্নিত। এবং flood_type='Flash Flood' —
# যেটা প্রশ্নবিদ্ধ, কারণ এই জেলার সবচেয়ে বড় hydrological feature আসলে
# Kaptai বাঁধ, classic flash-flood rain-runoff না।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

RANGAMATI_PROFILE = {
    "district": "রাঙ্গামাটি",
    "district_lat": 22.6533,
    "district_lon": 92.1730,

    # ── ১. এই জেলায় কতগুলো FFWC station আছে ──
    "station_count": 0,
    "station_count_note": (
        "⚠️ stations.py-তে রাঙ্গামাটির কোনো entry নেই, এবং BWDB-র "
        "official hydrology survey database-এও এই জেলার ভেতরে কোনো "
        "water-level forecasting station পাওয়া যায়নি (rainfall gauge "
        "থাকতে পারে, কিন্তু flood forecasting-এর জন্য প্রাসঙ্গিক "
        "water-level station না)। কর্ণফুলী নদীর একমাত্র FFWC station "
        "('Chittagong', SW152.2, Double Mooring) Kaptai বাঁধ থেকে ~৬৫ "
        "কিমি downstream, Chittagong জেলায় — সরাসরি রাঙ্গামাটির "
        "প্রতিনিধিত্ব করে না।"
    ),

    "stations": [],  # ইচ্ছাকৃতভাবে খালি — কোনো ভুয়া/অনুমানভিত্তিক station বানানো হয়নি

    # ── বিকল্প data source যা আছে (station না, কিন্তু প্রাসঙ্গিক) ──
    "alternative_data_sources": [
        {
            "name": "Kaptai Lake water level / reservoir elevation",
            "type": "reservoir_monitoring (BWDB/PDB internal, public API-তে সহজলভ্য না)",
            "relevance": (
                "Kaptai বাঁধের normal elevation ৩৩ মিটার MSL, spillway "
                "capacity ১৬,০০০ m³/s (১৬টা গেট)। Kaptai Lake-এর জলস্তর "
                "রাঙ্গামাটি শহর ও আশেপাশের char/দ্বীপ এলাকার বন্যা/"
                "জলমগ্নতার সবচেয়ে সরাসরি নির্ধারক — কিন্তু এই ডেটা FFWC-র "
                "সাধারণ public API-তে নেই, PDB (Power Development Board) "
                "বা BWDB-র সাথে সরাসরি যোগাযোগ করে পেতে হতে পারে।"
            ),
            "action_needed": "PDB/BWDB-কে সরাসরি email করে Kaptai reservoir-এর real-time/historical elevation ডেটা কীভাবে পাওয়া যায় জিজ্ঞাসা করা যেতে পারে।",
        },
        {
            "name": "Chittagong (SW152.2, Karnaphuli) — downstream proxy",
            "type": "FFWC verified station, কিন্তু ভিন্ন জেলায়",
            "relevance": (
                "যদিও এটা রাঙ্গামাটির ভেতরে না, কর্ণফুলীর এই downstream "
                "station-এর data দিয়ে পরোক্ষভাবে বাঁধ-নিঃসরণ ও উজানের "
                "প্রবাহের একটা সংকেত পাওয়া যেতে পারে — সরাসরি রাঙ্গামাটির "
                "risk হিসেবে না, বরং একটা weak correlated indicator "
                "হিসেবে বিবেচনা করা যেতে পারে ভবিষ্যতে।"
            ),
            "action_needed": None,
        },
    ],

    # ── river structure (station-independent বর্ণনা) ──
    "river_context": {
        "primary_river": "কর্ণফুলী (Karnaphuli)",
        "structure_note": (
            "মিজোরাম (ভারত)-এর Lushai পাহাড় থেকে উৎপন্ন, রাঙ্গামাটির "
            "মধ্য দিয়ে বয়ে Kaptai-তে বাঁধ পার হয়ে Chittagong-এর কাছে "
            "বঙ্গোপসাগরে পড়ে। catchment ~১১,০০০ বর্গকিমি। Kasalong "
            "নদী (Mizoram-এর ছোট স্রোতধারা মিলে Baghaichhari-তে তৈরি, "
            "flashy, ৬৫ কিমি) ও ইছামতি (Kawkhali-র কাছে ছোট উপনদী, "
            "৩০ কিমি, flashy) — দুইটাই কর্ণফুলী/Kaptai Lake-এ গিয়ে মেশে, "
            "উভয়ই BWDB-র মতে 'flashy' চরিত্রের।"
        ),
        "dam_context": (
            "⚠️ Kaptai বাঁধ (১৯৬২ নির্মিত) বাংলাদেশের একমাত্র জলবিদ্যুৎ "
            "কেন্দ্র, উচ্চতা ৪৫.৭ মি, দৈর্ঘ্য ৬৭০.৬ মি, জলাধার ধারণক্ষমতা "
            "৬,৪৭৭ মিলিয়ন ঘনমিটার। নির্মাণকালে জেলার ৪০% আবাদি জমি "
            "ডুবে গিয়েছিল, ১ লক্ষ মানুষ বাস্তুচ্যুত হয়েছিল (Chakma "
            "রাজার প্রাসাদ সহ)। Banglapedia অনুযায়ী এই জলাধার "
            "'downstream এলাকার (Chittagong শহর) জন্য একটা গুরুত্বপূর্ণ "
            "flood-management installation' হিসেবেও কাজ করে — অর্থাৎ "
            "রাঙ্গামাটির নিজের বন্যা-ঝুঁকি এবং downstream Chittagong-এর "
            "সুরক্ষা, দুইটাই একই বাঁধের ওপর নির্ভরশীল, কখনো কখনো "
            "পরস্পরবিরোধী স্বার্থে (বাঁধ ভরে গেলে গেট খুলতে হয়, যা "
            "downstream-এ আকস্মিক নিঃসরণ বন্যা তৈরি করতে পারে — ২০১৭ "
            "সালে ঠিক এটাই ঘটেছিল যখন রাঙ্গামাটিতে ভয়াবহ ভূমিধস ও "
            "বন্যা একসাথে হয়েছিল)।"
        ),
    },

    "flood_type_assessment": {
        "current_flood_config_value": "Flash Flood",
        "reviewed_recommendation": "Dam-Affected",
        "reasoning": (
            "⚠️ এটা এই প্রোফাইলের সবচেয়ে গুরুত্বপূর্ণ finding। "
            "flood_types/dam_affected.py module আগে থেকেই আছে এবং DFO "
            "archive বিশ্লেষণ করে specifically তৈরি হয়েছে (৩৪ দিন গড় "
            "স্থায়িত্ব, সর্বোচ্চ ১২১ দিন — বাকি flood_type-এর ৮-১৩ দিনের "
            "চেয়ে অনেক বেশি)। রাঙ্গামাটি বাংলাদেশের একমাত্র জেলা যেখানে "
            "একটা বড়, নিয়ন্ত্রিত জলাধার (Kaptai Lake) সরাসরি জেলার "
            "প্রধান শহরকেই ঘিরে আছে — dam_affected.py module যে ধরনের "
            "sustained, দীর্ঘস্থায়ী বন্যার কথা বলছে, সেটার সবচেয়ে "
            "স্বাভাবিক প্রার্থী এই জেলা। অথচ flood_config.py-তে এখনো "
            "'Flash Flood' ট্যাগ করা আছে, যা dam_affected.py module-টাকে "
            "কার্যত অব্যবহৃত রাখছে (অন্য কোনো জেলা 'Dam-Affected' ট্যাগ "
            "পেয়েছে কিনা, সেটা আলাদাভাবে যাচাই করা দরকার)।"
        ),
        "caveat": (
            "তবে এই recommendation নিশ্চিত না — Kasalong ও ইছামতির মতো "
            "ছোট, flashy উপনদীগুলোও Rangamati Sadar-এর বাইরের উপজেলায় "
            "(Baghaichhari, Kawkhali ইত্যাদি) সরাসরি rain-driven "
            "flash-flood করতে পারে, যেখানে বাঁধের প্রভাব কম। সম্ভবত "
            "রাঙ্গামাটি জেলার ভেতরেই দুই ধরনের sub-region আছে — Kaptai "
            "Lake-সংলগ্ন এলাকা (Dam-Affected) ও দূরবর্তী উপজেলা "
            "(Flash Flood) — কিন্তু district-level একটামাত্র flood_type "
            "ট্যাগ এই nuance ধরতে পারছে না।"
        ),
    },

    "cross_district_flags": (
        "⚠️⚠️ এটা এখন পর্যন্ত এই প্রজেক্টের সবচেয়ে বড় structural finding — "
        "একটা পুরো জেলায় (৬৪ জেলার মধ্যে একটা) কোনো real-time water-level "
        "monitoring station নেই, অথচ সেখানে বাংলাদেশের সবচেয়ে বড় বাঁধ ও "
        "জলাধার আছে। এটা district-profile-এর 'coordinate ঠিক করা'-র "
        "চেয়ে অনেক বড় একটা গবেষণা/policy প্রশ্ন — সম্ভাব্য next step: "
        "(১) PDB/BWDB-কে সরাসরি জিজ্ঞাসা করা Kaptai reservoir-এর ডেটা "
        "সহজলভ্য কিনা, (২) flood_config.py-র flood_type 'Flash Flood' "
        "থেকে 'Dam-Affected'-এ পরিবর্তনের সম্ভাবনা যাচাই করা, (৩) "
        "Khagrachhari-তেও (একই batch) একই সমস্যা আছে কিনা — সেটা আলাদা "
        "ফাইলে দেখুন।"
    ),
}