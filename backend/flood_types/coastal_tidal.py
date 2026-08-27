# ============================================================
# FloodAI — flood_types/coastal_tidal.py
#
# "Coastal & Tidal" flood_type-এর সব logic এখানে। model.py থেকে
# আলাদা করা হলো কারণ এই ফাইলটাই সবচেয়ে দ্রুত বড় হতে যাচ্ছে —
# এখন শুধু "পূর্ণিমা হলে বোনাস" এই crude rule আছে, কিন্তু WorldTides/
# Stormglass API integrate হলে এখানেই astronomical tide height আর
# storm-surge proxy যোগ হবে। বাকি flood_type (Flash Flood,
# Urban Waterlogging, Dam-Affected) এখনো ছোট বলে আপাতত model.py-তেই
# আছে — যেটা বড় হবে সেটাই পরে আলাদা হবে।
#
# ⚠️ এখনকার lunar-phase heuristic (পূর্ণিমা = ভরা কটাল ধরে নিয়ে
# +২০ বোনাস) কোনো real tide calculation না — এটা placeholder,
# WorldTides/Stormglass API যোগ হলে এটা replace হবে real tide
# height দিয়ে।
#
# ── cyclone_signal (২০২৬-০৮ যোগ করা হলো) ──
# জেলা-বাই-জেলা verification-এ (ভোলা/পটুয়াখালী/বরগুনা/পিরোজপুর/ঝালকাঠি)
# পাওয়া গেছে — Sidr(২০০৭)-এ storm surge ছিল ৫ মিটার (~১৬ ফুট), Remal
# (২০২৪)-এ ৮-১২ ফুট — এটা দৈনিক জোয়ার-ভাটার (lunar bonus, +২০) তুলনায়
# ১০-১৬ গুণ বড় মাত্রার ঘটনা। বরগুনায় একাই Sidr-এ ৪৭৪ জন মারা গিয়েছিল —
# দেশের ইতিহাসে সর্বোচ্চ। তাই BMD-র সংকেত সংখ্যা (Local Warning Signal,
# ১-১১) আলাদা parameter হিসেবে যোগ করা হলো।
#
# ⚠️ এখনো কোনো live BMD API integrate করা হয়নি — cyclone_signal
# পাঠানো না হলে (None/0) আগের মতোই আচরণ করবে, কোনো regression নেই।
# ভবিষ্যতে BMD-র bulletin থেকে live signal number টেনে এখানে
# পাস করলেই এই logic সক্রিয় হয়ে যাবে।
# ============================================================
def apply_override(probability: float, local_rain: float, is_full_moon: bool, cyclone_signal: int = 0, tide_ratio: float | None = None) -> tuple[float, bool]:
    """
    Coastal & Tidal জেলার জন্য base probability-তে override বসায়.
    Args:
        probability: base scoring থেকে আসা প্রাথমিক probability (0-100)
        local_rain: স্থানীয় বৃষ্টিপাত (mm)
        is_full_moon: আজ পূর্ণিমা/ভরা কটাল কিনা (tide_ratio না পাওয়া গেলে fallback হিসেবে ব্যবহৃত)
        cyclone_signal: BMD-র Local Warning Signal নম্বর (০ = কোনো সতর্কতা নেই,
            ১-৪ = দূরবর্তী সতর্কতা, ৫-৯ = স্থানীয় বিপদ সংকেত, ১০-১১ = মহাবিপদ
            সংকেত)। এখনো কোনো live source নেই বলে ডিফল্ট ০।
        tide_ratio: WorldTides API থেকে আসা real tide অবস্থান (0=সর্বনিম্ন
            জোয়ার, ১=সর্বোচ্চ জোয়ার)। None হলে (API key না থাকলে বা fetch
            ব্যর্থ হলে) is_full_moon-ভিত্তিক পুরনো crude heuristic ব্যবহৃত হয়।
    Returns:
        (নতুন probability, moon_bonus_applied কিনা) — দ্বিতীয় value
        model.py-র message আর score_breakdown এ ব্যবহার হয়, যাতে
        দুই জায়গায় is_full_moon চেক ডুপ্লিকেট করতে না হয়।
    """
    moon_bonus_applied = False
    if tide_ratio is not None:
        # ✅ (২০২৬-০৮) real tide height দিয়ে granular bonus — sharp cutoff-এর
        # বদলে ধারাবাহিক স্কেল, যেটা lunar heuristic-এর চেয়ে বেশি নির্ভুল।
        if tide_ratio >= 0.9:
            probability = min(probability + 25, 100)
            moon_bonus_applied = True
        elif tide_ratio >= 0.75:
            probability = min(probability + 15, 100)
            moon_bonus_applied = True
        elif tide_ratio >= 0.6:
            probability = min(probability + 8, 100)
            moon_bonus_applied = True
    elif is_full_moon:
        probability = min(probability + 20, 100)  # ভরা কটালের জন্য এক্সট্রা ২০% ঝুঁকি (fallback, real tide data না থাকলে)
        moon_bonus_applied = True
    if local_rain > 30:
        probability = max(probability, 65)
    elif local_rain > 10:
        probability = max(probability, 45)

    # cyclone_signal — Sidr/Remal স্কেলের storm surge, দৈনিক tidal cycle-এর
    # চেয়ে সম্পূর্ণ ভিন্ন মাত্রার বিপদ, তাই lunar bonus-এর চেয়ে অনেক বড় floor
    if cyclone_signal and cyclone_signal >= 10:      # মহাবিপদ সংকেত (Sidr/Remal স্কেল)
        probability = max(probability, 95)
    elif cyclone_signal and cyclone_signal >= 7:      # স্থানীয় বিপদ সংকেত (উচ্চ)
        probability = max(probability, 75)
    elif cyclone_signal and cyclone_signal >= 4:      # দূরবর্তী সতর্কতা
        probability = max(probability, 50)

    return probability, moon_bonus_applied


def get_message_fragment(moon_bonus_applied: bool, cyclone_signal: int = 0, tide_ratio: float | None = None) -> str | None:
    """moon_bonus_applied/cyclone_signal হলে message-এ জুড়ে দেওয়ার মতো বাক্য।"""
    if cyclone_signal and cyclone_signal >= 10:
        return " 🌀 মহাবিপদ সংকেত জারি — Sidr/Remal-স্কেলের ঘূর্ণিঝড়, উপকূলীয় এলাকায় গুরুতর storm surge-এর আশঙ্কা।"
    elif cyclone_signal and cyclone_signal >= 7:
        return f" 🌀 স্থানীয় বিপদ সংকেত ({cyclone_signal} নম্বর) জারি আছে।"
    elif cyclone_signal and cyclone_signal >= 4:
        return f" 🌀 দূরবর্তী সতর্কতা সংকেত ({cyclone_signal} নম্বর) জারি আছে।"
    if moon_bonus_applied and tide_ratio is not None:
        return f" 🌊 এই মুহূর্তে জোয়ার এলাকার সর্বোচ্চ সীমার {round(tide_ratio*100)}%-এ, পানির উচ্চতা স্বাভাবিকের চেয়ে বেশি থাকবে।"
    if moon_bonus_applied:
        return " 🌕 আজ ভরা কটাল (পূর্ণিমা), জোয়ারের উচ্চতা স্বাভাবিকের চেয়ে বেশি থাকবে।"
    return None