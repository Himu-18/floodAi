# ============================================================
# FloodAI — flood_types/flash_flood.py
#
# "Flash Flood" (হাওর অঞ্চল, পার্বত্য চট্টগ্রাম) flood_type-এর logic।
#
# গবেষণা অনুযায়ী: ২০২২ সালের সিলেট-সুনামগঞ্জ বন্যার আসল ট্রিগার ছিল
# উজানে (Cherrapunji, Meghalaya) স্বল্প সময়ে প্রবল বৃষ্টি — সিলেট শহরেই
# ৩ ঘণ্টায় ২২০মিমি বা ৬ ঘণ্টায় ১৮৬মিমি রেকর্ড হয়েছিল। মানে key predictor
# হলো short-duration rainfall intensity (কয়েক ঘণ্টায় কত বৃষ্টি), দৈনিক
# যোগফল বা এক ঘণ্টার snapshot না।
#
# ⚠️ এই মডিউল একটা "৬-ঘণ্টার rolling rainfall" ব্যবহার করে (local +
# upstream দুটোই), যেটা app.py-র fetch_rainfall_intensity() থেকে আসে।
# যদি এই ডেটা fetch করা না যায় (API fail/উপরের শহরের coordinate না
# পাওয়া গেলে), পুরনো দৈনিক-total-ভিত্তিক logic-এ fallback করে, যাতে
# পুরোপুরি ভেঙে না পড়ে।
#
# ⚠️ mainstem_36h (২০২৬-০৯ যোগ করা): শুধু সিলেট/সুনামগঞ্জের জন্য,
# বরাক নদীর mainstem (Silchar, আসাম) থেকে আসা ধীর/sustained inflow
# ধরার একটা দ্বিতীয় signal — ৬-ঘণ্টার fast hill-runoff signal থেকে
# আলাদা mechanism (lag ~৩৬ ঘণ্টা)। এখানে এটাকে HARD override না করে
# একটা ছোট additive bonus (সর্বোচ্চ +১৫) হিসেবে রাখা হয়েছে, কারণ এর
# থ্রেশহোল্ড এখনো backtest দিয়ে calibrate করা হয়নি — শুধু rainfall
# rate থেকে আনুপাতিকভাবে বসানো একটা প্রাথমিক অনুমান। পরের ধাপে
# backtest_v2.py দিয়ে ২০২২/২০১০-এর real event-এর সাথে মিলিয়ে এই
# সংখ্যাগুলো ঠিক করা দরকার।
# ============================================================

def apply_override(
    probability: float,
    local_rain: float,
    upstream_rain: float,
    rainfall_intensity_data: dict | None
) -> tuple[float, bool, str]:
    """
    Flash Flood জেলার জন্য override।

    Args:
        probability: base scoring থেকে আসা প্রাথমিক probability
        local_rain, upstream_rain: fallback-এর জন্য (পুরনো দৈনিক ডেটা)
        rainfall_intensity_data: {"local_6h": float, "upstream_6h": float,
            "mainstem_36h": float (optional, শুধু সিলেট/সুনামগঞ্জে)}
            (মিমি) অথবা None

    Returns:
        (নতুন probability, intensity_data_used কিনা, ব্যবহৃত পদ্ধতির নাম)
    """
    if rainfall_intensity_data:
        local_6h = rainfall_intensity_data.get("local_6h") or 0
        upstream_6h = rainfall_intensity_data.get("upstream_6h") or 0
        total_6h = local_6h + upstream_6h

        # থ্রেশহোল্ড গবেষণার real trigger figure (৬ ঘণ্টায় ~১৮৬মিমি = extreme)
        # অনুযায়ী calibrate করা, দৈনিক-total থ্রেশহোল্ডের থেকে ভিন্ন স্কেলে
        if total_6h > 150: probability = max(probability, 95)
        elif total_6h > 80: probability = max(probability, 75)
        elif total_6h > 65: probability = max(probability, 55)
        elif total_6h > 15: probability = max(probability, 35)

        method = "6h_rolling_intensity"

        # ── বরাক-mainstem bonus (provisional, uncalibrated থ্রেশহোল্ড) ──
        if "mainstem_36h" in rainfall_intensity_data:
            mainstem_36h = rainfall_intensity_data.get("mainstem_36h") or 0
            # ৬h স্কেলের সাথে সামঞ্জস্যপূর্ণ mm/ঘণ্টা রেট থেকে ৩৬h-এ স্কেল করা
            # (provisional — backtest-এ verify করা হয়নি)
            if mainstem_36h > 450: probability = min(100, probability + 15)
            elif mainstem_36h > 240: probability = min(100, probability + 8)
            elif mainstem_36h > 90: probability = min(100, probability + 3)
            method = "6h_rolling_intensity+mainstem_36h_provisional"

        return probability, True, method

    # ── Fallback: পুরনো দৈনিক-total-ভিত্তিক logic (API fail করলে) ──
    total_rain = local_rain + upstream_rain
    if total_rain > 60: probability = max(probability, 95)
    elif total_rain > 30: probability = max(probability, 75)
    elif total_rain > 15: probability = max(probability, 55)
    elif total_rain > 5: probability = max(probability, 35)
    return probability, False, "daily_total_fallback"


def get_message_fragment(intensity_data_used: bool, method: str) -> str | None:
    if intensity_data_used:
        return None  # আলাদা করে কিছু বলার দরকার নেই, normal message-ই যথেষ্ট
    return " (⚠️ ৬-ঘণ্টার rainfall intensity ডেটা পাওয়া যায়নি, দৈনিক আনুমানিক হিসাব ব্যবহার হয়েছে)"