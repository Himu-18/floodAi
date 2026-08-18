# ============================================================
# FloodAI — flood_types/riverine.py
#
# "Riverine" flood_type-এর logic — coastal_tidal.py-র প্যাটার্ন
# অনুসরণ করে model.py থেকে আলাদা করা হলো।
#
# আসল কার্যকারণ (গবেষণা অনুযায়ী): ১৯৮৮-এর ভয়াবহ বন্যার মূল কারণ ছিল
# গঙ্গা, ব্রহ্মপুত্র (যমুনা) আর মেঘনা — এই প্রধান নদীগুলোর flood peak
# প্রায় একই সময়ে synchronize হয়ে যাওয়া, যার ফলে drainage capacity
# একসাথে সব জায়গায় কমে যায়। শুধু একটা নদীর discharge বেশি হওয়ার
# চেয়ে এই "একাধিক নদীর peak একসাথে আসা" ঘটনাটাই riverine flood-এর
# সবচেয়ে গুরুত্বপূর্ণ predictor বলে চিহ্নিত।
#
# আমরা পুরো GBM ব্যবস্থার সব নদী track করছি না (সেটা অনেক বড় কাজ),
# শুধু পদ্মা+যমুনার সঙ্গমস্থলের কাছের জেলাগুলোর জন্য এই "দুই নদী
# একসাথে উঁচু কিনা" চেক করা হচ্ছে, কারণ এই দুটোই আমাদের ডেটাসেটে
# সবচেয়ে বড়/সবচেয়ে ভালো-ক্যালিব্রেটেড নদী (mega_trunk category)।
#
# ⚠️ সীমাবদ্ধতা: এটা শুধু ২টা নদী (পদ্মা+যমুনা) দেখছে, মেঘনা বাদ —
# ভবিষ্যতে চাঁদপুর/বরিশাল/ভোলার জন্য মেঘনাকেও একইভাবে যোগ করা যায়।
# এখনো এটা geometry/measurement-verified না, category-range-calibrated
# discharge-এর উপর ভিত্তি করে বানানো।
#
# 🔧 আপডেট (backtest_dfo.py দিয়ে DFO archive validation-এর পর):
# real discharge পাওয়া গেলে Riverine logic ঐতিহাসিক বন্যায় ~৮৫%
# সঠিক ছিল, কিন্তু discharge fetch ব্যর্থ হলে (０ আসলে) hit-rate
# ~১৩%-এ নেমে যেত — কারণ বাকি ৪টা flood_type-এর মতো Riverine-এর
# কোনো rain-based fallback ছিল না। এখন একটা হালকা rain-based floor
# যোগ করা হলো, discharge যাই বলুক (সত্যিই কম, নাকি fetch ব্যর্থ —
# দুটো আলাদা করার উপায় নেই), শুধু data-gap-এর বিরুদ্ধে একটা safety net।
# ============================================================

CONFLUENCE_DISTRICTS = ["রাজবাড়ী", "মানিকগঞ্জ", "মুন্সিগঞ্জ", "ফরিদপুর", "শরীয়তপুর"]
# ⚠️ ২৭ জুলাই ২০২৬: আগে PADMA_REFERENCE_DISTRICT="রাজবাড়ী" (Goalondo) আর
# JAMUNA_REFERENCE_DISTRICT="মানিকগঞ্জ" (Aricha) ছিল — কিন্তু এই দুই জায়গা
# আসলে পদ্মা-যমুনার সঙ্গমস্থলেই (মাত্র ~1.5 কিমি দূরত্ব, Open-Meteo-র ৫কিমি
# grid resolution-এর মধ্যে কার্যত একই grid cell)। ফলে দুটো "আলাদা" ratio
# আসলে একই combined-flow সংখ্যাকে দুইবার ভিন্ন danger_level দিয়ে ভাগ করছিল —
# তাই synchronized_peak প্রায় সবসময় true হয়ে যাচ্ছিল (মুন্সিগঞ্জে ১০০%
# দেখানোর মূল কারণ)। এখন সঙ্গমস্থলের আগের (upstream, খাঁটি) বিন্দু
# ব্যবহার করা হচ্ছে যাতে দুটো সত্যিই স্বাধীন নদী-পরিমাপ হয়।
PADMA_REFERENCE_DISTRICT = "রাজশাহী"    # সঙ্গমস্থলের অনেক পশ্চিমে, খাঁটি গঙ্গা/পদ্মা
JAMUNA_REFERENCE_DISTRICT = "সিরাজগঞ্জ"  # সঙ্গমস্থলের অনেক উত্তরে, খাঁটি যমুনা


def apply_override(
    probability: float,
    confluence_data: dict | None,
    local_rain: float = 0,
    upstream_rain: float = 0
) -> tuple[float, bool, bool]:
    """
    Riverine জেলার জন্য base probability-তে override বসায়।

    Args:
        probability: base scoring থেকে আসা প্রাথমিক probability (0-100)
        confluence_data: {"padma_ratio": float, "jamuna_ratio": float} অথবা None
        local_rain, upstream_rain: rain-based floor-এর জন্য (মিমি)

    Returns:
        (নতুন probability, synchronized_peak কিনা, rain_floor_applied কিনা)
    """
    synchronized_peak = False
    if confluence_data:
        padma_ratio = confluence_data.get("padma_ratio")
        jamuna_ratio = confluence_data.get("jamuna_ratio")
        if padma_ratio is not None and jamuna_ratio is not None:
            if padma_ratio > 1.0 and jamuna_ratio > 1.0:
                probability = min(probability + 15, 100)
                synchronized_peak = True
            elif padma_ratio > 0.8 and jamuna_ratio > 0.8:
                probability = max(probability, 60)

    # ── Rain-based floor (data-gap safety net) ──
    combined_rain = (local_rain or 0) + (upstream_rain or 0)
    rain_floor_applied = False
    if combined_rain > 60 and probability < 50:
        probability = 50
        rain_floor_applied = True
    elif combined_rain > 30 and probability < 35:
        probability = 35
        rain_floor_applied = True

    return probability, synchronized_peak, rain_floor_applied


def get_message_fragment(synchronized_peak: bool, rain_floor_applied: bool = False) -> str | None:
    """synchronized_peak বা rain_floor_applied হলে message-এ জুড়ে দেওয়ার মতো বাক্য।"""
    if synchronized_peak:
        return (" 🌊 পদ্মা ও যমুনা — দুটো প্রধান নদীরই পানি একসাথে "
                "বিপদসীমার বেশি, যা বন্যার ঝুঁকি উল্লেখযোগ্যভাবে বাড়িয়ে দেয়।")
    if rain_floor_applied:
        return (" ⚠️ নদীর discharge ডেটা অনুপস্থিত/অনিশ্চিত, কিন্তু বৃষ্টির "
                "পরিমাণ উল্লেখযোগ্য — সতর্কতা হিসেবে ন্যূনতম ঝুঁকি ধরা হয়েছে।")
    return None