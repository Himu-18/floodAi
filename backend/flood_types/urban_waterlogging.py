# ============================================================
# FloodAI — flood_types/urban_waterlogging.py
#
# "Urban Waterlogging" flood_type-এর logic — coastal_tidal.py/
# riverine.py-র প্যাটার্ন অনুসরণ করে model.py থেকে আলাদা করা হলো।
#
# গবেষণায় ধরা পড়া gap ১: চট্টগ্রামের জলাবদ্ধতা শুধু drainage-capacity
# আর ভারী বৃষ্টির সমস্যা না — এটা আংশিকভাবে coastal_tidal সমস্যাও।
# চট্টগ্রামের drainage স্বাভাবিকভাবে কর্ণফুলী নদীতে গিয়ে পড়ার কথা,
# কিন্তু জোয়ারের সময় (বিশেষ করে ভরা কটালে) নদীর পানি বেড়ে যাওয়ায়
# শহরের পানি নদীতে নামতেই পারে না ("tide-lock") — ফলে ভরা কটালের
# সময় সাধারণ বৃষ্টিতেও জলাবদ্ধতা অনেক বেশি হয়।
#
# গবেষণায় ধরা পড়া gap ২ (২০২৬-০৮ যোগ করা হলো): ঢাকার জলাবদ্ধতার
# আসল কারণ discharge/river-water-level না — এটা মূলত drainage
# capacity failure। BUET IWFM-এর গবেষণা ও একাধিক সংবাদ অনুযায়ী:
#   - ঢাকার খাল ৬৫টা থেকে কমে ২৬-৪৩টায় নেমে এসেছে (encroachment)
#   - বর্ষায় নদীর পানি বাড়লে sluice gate বন্ধ হয়ে যায় (নদীর পানি
#     উল্টো শহরে ঢোকা ঠেকাতে), ফলে শহরের বৃষ্টির পানি সম্পূর্ণভাবে
#     pumping capacity-নির্ভর হয়ে পড়ে — যেটা অপ্রতুল
# তাই এখন প্রতি জেলার একটা DRAINAGE_CAPACITY_FACTOR (০-১, যত কম তত
# বেশি ক্ষতিগ্রস্ত drainage system) যোগ করা হলো, যেটা কার্যকরভাবে
# "একই বৃষ্টি এই জেলায় কতটা worse feel করবে" adjust করে।
#
# ⚠️ এই ফ্যাক্টরটা literature-based অনুমান, প্রতি বছরের real
# encroachment-survey ডেটা না — ভবিষ্যতে DNCC/DSCC/CDA-র official
# drainage-capacity assessment পাওয়া গেলে আরো নির্ভুল করা যাবে।
#
# গবেষণায় ধরা পড়া gap ৩: rainfall INTENSITY (মিমি/ঘণ্টা) দৈনিক
# cumulative rain-এর চেয়ে বেশি প্রাসঙ্গিক urban drainage-এর জন্য —
# flash_flood.py-র মতো একই rainfall_intensity_data (৬-ঘণ্টার
# rolling total) এখন এখানেও ব্যবহার হয়, পাওয়া গেলে।
#
# ⚠️ এই tide-lock bonus শুধু "জোয়ারভাটা-প্রভাবিত শহুরে এলাকা"-র জন্য
# প্রযোজ্য (এখন শুধু চট্টগ্রাম) — ঢাকা/গাজীপুর/নারায়ণগঞ্জ অভ্যন্তরীণ
# (inland), এদের জন্য এই effect প্রযোজ্য না, তাই আলাদা তালিকায় রাখা।
# ============================================================

TIDAL_INFLUENCED_URBAN_DISTRICTS = ["চট্টগ্রাম"]

# ১.০ = পূর্ণ ঐতিহাসিক drainage capacity, যত কম সংখ্যা তত বেশি
# encroachment/capacity-loss — literature-based অনুমান (২০২৬-০৮)।
DRAINAGE_CAPACITY_FACTOR = {
    "ঢাকা": 0.45,        # সবচেয়ে বেশি খাল-ক্ষতি (৬৫→২৬-৪৩টা), sluice-gate closure সমস্যা সবচেয়ে severe
    "চট্টগ্রাম": 0.55,   # tide-lock + drainage encroachment উভয়ই
    "গাজীপুর": 0.65,     # শিল্পাঞ্চল, moderate encroachment
    "নারায়ণগঞ্জ": 0.65,  # একই ধরনের শিল্পাঞ্চলীয় সমস্যা
}
DEFAULT_DRAINAGE_CAPACITY_FACTOR = 0.8  # তালিকায় না-থাকা urban জেলার জন্য conservative default


def apply_override(
    probability: float,
    district_name: str,
    local_rain: float,
    is_full_moon: bool,
    rainfall_intensity_data: dict | None = None,
) -> tuple[float, bool]:
    """
    Urban Waterlogging জেলার জন্য override।

    Args:
        probability: base scoring থেকে আসা প্রাথমিক probability
        district_name: জেলার নাম (tidal-influenced ও drainage-capacity চেক করতে)
        local_rain: স্থানীয় বৃষ্টিপাত (mm, দৈনিক — rainfall_intensity_data
            না পাওয়া গেলে fallback হিসেবে ব্যবহার হয়)
        is_full_moon: আজ পূর্ণিমা/ভরা কটাল কিনা
        rainfall_intensity_data: {"local_6h": float, ...} অথবা None —
            flash_flood.py-র মতোই ৬-ঘণ্টার rolling rainfall, urban
            drainage-এর জন্যও দৈনিক total-এর চেয়ে বেশি প্রাসঙ্গিক

    Returns:
        (নতুন probability, tide_lock_applied কিনা)
    """
    capacity_factor = DRAINAGE_CAPACITY_FACTOR.get(district_name, DEFAULT_DRAINAGE_CAPACITY_FACTOR)

    # rainfall intensity data থাকলে সেটাই primary signal — ৬ ঘণ্টার rolling
    # rain-কে capacity_factor দিয়ে ভাগ করে "effective rain" বানানো হচ্ছে
    # (কম capacity মানে একই বৃষ্টি বেশি প্রভাব ফেলবে)
    if rainfall_intensity_data:
        local_6h = rainfall_intensity_data.get("local_6h") or (local_rain / 4)  # daily-র মোটামুটি ৬ঘন্টা অংশ
        effective_rain_6h = local_6h / capacity_factor
        urban_score = 10 + (effective_rain_6h * 2)
        if effective_rain_6h > 40:
            probability = max(probability, 90)
        elif effective_rain_6h > 20:
            probability = max(probability, 65)
        else:
            probability = min(probability, urban_score)
    else:
        # ── Fallback: পুরনো দৈনিক-total-ভিত্তিক logic, কিন্তু এখন
        # capacity_factor দিয়ে adjust করা ──
        effective_rain = local_rain / capacity_factor
        urban_score = 10 + (effective_rain * 2)
        if effective_rain > 40:
            probability = max(probability, 85)
        elif effective_rain > 20:
            probability = max(probability, 60)
        else:
            probability = min(probability, urban_score)

    # tide-lock bonus — শুধু tidal-influenced শহরে (চট্টগ্রাম), এবং
    # শুধু ভরা কটালের সময়েই প্রযোজ্য (নাহলে drainage স্বাভাবিকভাবেই চলে)
    tide_lock_applied = False
    if district_name in TIDAL_INFLUENCED_URBAN_DISTRICTS and is_full_moon:
        # সাধারণ বৃষ্টিতেও tide-lock থাকলে ঝুঁকি বাড়ে — কিন্তু coastal_tidal-এর
        # মতো পূর্ণ +20 বোনাস না (এখানে জোয়ার শুধু "modifying factor",
        # মূল driver বৃষ্টিই থেকে যায়) — তাই ছোট, +10 বোনাস
        probability = min(probability + 10, 100)
        tide_lock_applied = True

    return probability, tide_lock_applied


def get_message_fragment(tide_lock_applied: bool) -> str | None:
    """tide_lock_applied হলে message-এ জুড়ে দেওয়ার মতো একটা বাক্য।"""
    if tide_lock_applied:
        return (" 🌊 আজ ভরা কটাল — জোয়ারের কারণে শহরের ড্রেনেজ আউটফল "
                "সাময়িকভাবে বন্ধ থাকতে পারে, তাই স্বাভাবিক বৃষ্টিতেও "
                "জলাবদ্ধতা বেশি হতে পারে।")
    return None