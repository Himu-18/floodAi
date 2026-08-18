# ============================================================
# FloodAI — flood_types/dam_affected.py
#
# "Dam-Affected" flood_type-এর logic — coastal_tidal/riverine/
# flash_flood/urban_waterlogging-এর প্যাটার্ন অনুসরণ করে model.py
# থেকে আলাদা করা হলো।
#
# ⚠️ DFO (Dartmouth Flood Observatory) archive বিশ্লেষণ করে পাওয়া
# finding (২০২৬-০৮-০২ তারিখের বিশ্লেষণ, ৯টা genuinely rain-কারণে
# হওয়া ঘটনা, storm/cyclone/surge-কারণে হওয়া ২টা outlier বাদ দিয়ে):
# Dam-Affected জেলার বন্যা গড়ে ~৩৪ দিন স্থায়ী হয় (সর্বোচ্চ ১২১ দিন!)
# — এটা বাকি সব flood_type (৮-১৩ দিন গড়) এর চেয়ে অনেক বেশি দীর্ঘস্থায়ী।
# ৮/৯টা ঘটনাই জুন-জুলাইতে শুরু হয়েছে (peak monsoon)।
#
# এই finding থেকে বোঝা যায়: আসল ঝুঁকির signal শুধু "আজকের" upstream
# rain না, বরং "কতদিন ধরে টানা" upstream-এ বৃষ্টি হচ্ছে (sustained/
# persistent rain) — এটাই দীর্ঘস্থায়ী, বাঁধ-চালিত বন্যার প্যাটার্ন।
#
# ⚠️ সীমাবদ্ধতা: এখনো real dam-release event/announcement data নেই
# (fundamental limitation, আগেও আলোচনা হয়েছে) — এই persistence
# heuristic upstream rain-কেই proxy হিসেবে ব্যবহার করছে, dam gate
# কবে খুলবে সেটা সরাসরি জানে না। আর মাত্র ৯টা ঘটনার ভিত্তিতে থ্রেশহোল্ড
# বসানো হয়েছে (ছোট sample size), ভবিষ্যতে আরও ডেটা দিয়ে refine করা উচিত।
# ============================================================

SUSTAINED_RAIN_THRESHOLD_MM = 20  # এই মানের বেশি upstream rain হলে সেই দিনটা "সক্রিয়" ধরা হচ্ছে


def apply_override(
    probability: float,
    upstream_rain: float,
    upstream_rain_history: list | None = None
) -> tuple[float, int]:
    """
    Dam-Affected জেলার জন্য override।

    Args:
        probability: base scoring থেকে আসা প্রাথমিক probability
        upstream_rain: আজকের upstream rain (mm) — fallback-এর জন্য
        upstream_rain_history: গত কয়েক দিনের upstream_rain মান, সবচেয়ে
            সাম্প্রতিক দিন প্রথমে (যেমন [আজ, গতকাল, পরশু, ...]) —
            app.py-র database থেকে আসবে। None হলে পুরনো single-day
            logic-এ fallback করবে।

    Returns:
        (নতুন probability, sustained_days) — sustained_days = টানা
        কতদিন ধরে upstream-এ উল্লেখযোগ্য বৃষ্টি হচ্ছে (message-এ ব্যবহারের জন্য)
    """
    sustained_days = 0

    if upstream_rain_history:
        for val in upstream_rain_history:
            if val is not None and val > SUSTAINED_RAIN_THRESHOLD_MM:
                sustained_days += 1
            else:
                break  # ধারাবাহিকতা ভেঙে গেলে গোনা বন্ধ

        # DFO history অনুযায়ী থ্রেশহোল্ড (৯টা ঘটনার ছোট sample-ভিত্তিক,
        # ভবিষ্যতে আরও ডেটা দিয়ে refine করা উচিত)
        if sustained_days >= 5:
            probability = min(probability + 25, 100)
        elif sustained_days >= 3:
            probability = min(probability + 15, 100)
        elif upstream_rain > 50:
            probability = min(probability + 20, 100)
        elif upstream_rain > 30:
            probability = min(probability + 10, 100)
        return probability, sustained_days

    # ── Fallback: history পাওয়া না গেলে পুরনো single-day logic ──
    if upstream_rain > 50:
        probability = min(probability + 20, 100)
    elif upstream_rain > 30:
        probability = min(probability + 10, 100)
    return probability, sustained_days


def get_message_fragment(sustained_days: int) -> str | None:
    if sustained_days >= 5:
        return (f" 🌧️ উজানে টানা {sustained_days}+ দিন ধরে ভারী বৃষ্টি চলছে — "
                "ঐতিহাসিকভাবে এই ধরনের দীর্ঘস্থায়ী উজানের বৃষ্টি বাংলাদেশে "
                "সপ্তাহ-মাসব্যাপী দীর্ঘস্থায়ী বন্যার সাথে যুক্ত থেকেছে।")
    return None