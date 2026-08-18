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
        rainfall_intensity_data: {"local_6h": float, "upstream_6h": float}
            (মিমি, গত ৬ ঘণ্টার rolling total) অথবা None

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
        elif total_6h > 40: probability = max(probability, 55)
        elif total_6h > 15: probability = max(probability, 35)
        return probability, True, "6h_rolling_intensity"

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