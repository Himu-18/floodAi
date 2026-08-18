# ============================================================
# FloodAI — data/district_profiles/khagrachhari.py
#
# ১৮তম জেলা। Rangamati-র মতোই — stations.py-তে কোনো entry নেই, এবং
# ব্যাপক অনুসন্ধানেও FFWC-র public network-এ খাগড়াছড়ির ভেতরে কোনো
# water-level station পাওয়া যায়নি (Chengi/Maini নদীর জন্য)। সততার সাথে
# document করা হলো, কোনো ভুয়া station data বানানো হয়নি।
#
# ⚠️ FFWC-র Wikipedia পাতা অনুযায়ী সারা দেশে মোট ১০৯টা water-level
# monitoring station ও ৬১টা forecasting station আছে — একটা finite,
# সীমিত network, এবং খাগড়াছড়ি স্পষ্টতই এর বাইরে।
#
# ⚠️ এখনো model.py/app.py এর সাথে wire করা হয়নি।
# ============================================================

KHAGRACHHARI_PROFILE = {
    "district": "খাগড়াছড়ি",
    "district_lat": 23.1193,
    "district_lon": 91.9847,

    "station_count": 0,
    "station_count_note": (
        "⚠️ stations.py-তে খাগড়াছড়ির কোনো entry নেই। BWDB-র official "
        "hydrology survey database ও FFWC live site — কোনোটাতেই "
        "খাগড়াছড়ি জেলার ভেতরে (Chengi, Maini নদীর ওপর) কোনো "
        "water-level forecasting station খুঁজে পাওয়া যায়নি। জেলা সদর "
        "নিজেই Chengi নদীর তীরে অবস্থিত (জেলার নামকরণও এই নদী থেকে), "
        "কিন্তু সেখানে কোনো FFWC public monitoring station নেই।"
    ),

    "stations": [],  # ইচ্ছাকৃতভাবে খালি — Rangamati-র মতোই কোনো ভুয়া station বানানো হয়নি

    "alternative_data_sources": [
        {
            "name": "FFWC Real-time API (ffwc.bwdb.gov.bd)",
            "type": "সরকারি API, সম্প্রতি চালু হয়েছে বলে মনে হচ্ছে",
            "relevance": (
                "একটা নতুন, dedicated API (data_load endpoint সহ) পাওয়া "
                "গেছে যেটা 'various river points across Bangladesh'-এর "
                "real-time ও historical data দেয় বলে দাবি করছে। এটা "
                "old.ffwc.gov.bd-এর চেয়ে বেশি comprehensive হতে পারে — "
                "খাগড়াছড়ি/রাঙ্গামাটির জন্য কোনো hidden/undocumented "
                "station থাকলে এই API-তে থাকতে পারে। সরাসরি explore "
                "করে দেখা উচিত ভবিষ্যতে।"
            ),
            "action_needed": "ffwc.bwdb.gov.bd/data_load/ API explore করে দেখা যে খাগড়াছড়ি/রাঙ্গামাটির কোনো station সেখানে আছে কিনা যেটা stations.py/old.ffwc.gov.bd-এ মিস হয়ে গেছে।",
        },
    ],

    "river_context": {
        "primary_river": "চেঙ্গী (Chengi)",
        "structure_note": (
            "খাগড়াছড়ির Batnatali পাহাড় থেকে উৎপন্ন, দক্ষিণে বয়ে "
            "Madhunaghat (চট্টগ্রাম)-এর কাছে কর্ণফুলীতে মেশে। "
            "Banglapedia স্পষ্টভাবে 'flashy' নদী হিসেবে চিহ্নিত করেছে, "
            "দৈর্ঘ্য ৮৮ কিমি। ⚠️ উল্লেখযোগ্য — BWDB-র এই নদীতে ১৩টা "
            "hydrometric station আছে (১৯৫৯ সাল থেকে ডেটা), কিন্তু এই "
            "স্টেশনগুলো সম্ভবত মূলত hydrometric/research-purpose "
            "(flow measurement), FFWC-র public flood-forecasting "
            "network-এর অংশ না — এটা একটা গুরুত্বপূর্ণ পার্থক্য যা "
            "আরও অনুসন্ধান দাবি করে (BWDB hydrometric station ≠ FFWC "
            "forecasting station, দুইটা ভিন্ন ডেটাবেজ/উদ্দেশ্য হতে পারে)। "
            "Maini নদীও জেলার একটা গুরুত্বপূর্ণ নদী, কর্ণফুলী/Kaptai "
            "Lake-এ গিয়ে মেশে।"
        ),
        "dam_context": (
            "খাগড়াছড়ি সরাসরি Kaptai বাঁধের ওপর অবস্থিত না (সেটা "
            "রাঙ্গামাটিতে), কিন্তু জেলার দক্ষিণ অংশ Kaptai Lake-এর "
            "catchment-এর অংশ হতে পারে — এটা নিশ্চিত করার জন্য আরও "
            "geographic analysis দরকার।"
        ),
    },

    "flood_type_assessment": {
        "current_flood_config_value": "Flash Flood",
        "reviewed_recommendation": "Flash Flood (বহাল রাখা যুক্তিসঙ্গত)",
        "reasoning": (
            "Rangamati-র বিপরীতে, খাগড়াছড়ির প্রধান নদী (চেঙ্গী) সরাসরি "
            "কোনো বাঁধ-নিয়ন্ত্রিত না, এবং Banglapedia নিজেই এটাকে "
            "'flashy' বলছে। ত্রিপুরা (ভারত) সীমান্তের কাছাকাছি হওয়ায় "
            "(flood_config.py-তে upstream='Agartala, IN' আগে থেকেই "
            "আছে) Habiganj-এর Khowai-র মতো ধরনের flash-flood ঝুঁকিই "
            "বেশি প্রাসঙ্গিক মনে হচ্ছে, বর্তমান 'Flash Flood' ট্যাগ "
            "ঠিকই আছে।"
        ),
        "caveat": "কিন্তু কোনো real station data ছাড়া এই assessment পুরোপুরি নিশ্চিত করা কঠিন — এটা geographic/qualitative reasoning-ভিত্তিক, quantitative verification না।",
    },

    "cross_district_flags": (
        "⚠️ Rangamati-র মতোই একই ধরনের 'zero station' সমস্যা, কিন্তু "
        "কারণ ভিন্ন হতে পারে — Rangamati-তে বাঁধ থাকা সত্ত্বেও ডেটা নেই "
        "(institutional/political কারণ থাকতে পারে, PDB-BWDB সমন্বয়ের "
        "অভাব), খাগড়াছড়িতে হয়তো নিছক দুর্গম পার্বত্য এলাকা হওয়ায় "
        "station বসানোই হয়নি। এই দুইটা জেলা মিলিয়ে একটা বড় প্রশ্ন "
        "তুলছে — পার্বত্য চট্টগ্রামের ৩ জেলার মধ্যে ২টাতেই (৬৪ জেলার "
        "১/৩২ অংশ) কোনো flood-forecasting coverage নেই, যেটা এই "
        "এলাকার জনসংখ্যার তুলনায় অসামঞ্জস্যপূর্ণভাবে বড় একটা blind "
        "spot — বিশেষত ২০১৭ সালের রাঙ্গামাটি ভূমিধস-বন্যা বিপর্যয়ের "
        "মতো ঘটনার পরেও।"
    ),
}