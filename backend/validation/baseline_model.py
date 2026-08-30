# validation/baseline_model.py
# ============================================================
# FloodAI Validation — Baseline Model
# ============================================================
# advisor-এর সবচেয়ে গুরুত্বপূর্ণ experiment: FloodAI বনাম একটা সাধারণ
# "water level >= danger level হলেই flood" বেসলাইন। এটা ইচ্ছাকৃতভাবে
# অতি-সরল রাখা হয়েছে — কোনো rainfall, upstream data, ML কিছুই ব্যবহার
# করে না। যদি FloodAI এই সরল বেসলাইনকেও হারাতে না পারে, তাহলে সব
# জটিলতা (rule-based scoring + ML) আসলে কোনো real value যোগ করছে না।

def baseline_predict(water_level_m: float, danger_level_m: float) -> bool:
    """
    সবচেয়ে সরল সম্ভাব্য বন্যা-পূর্বাভাস: water level যদি এই মুহূর্তেই
    danger level-এর সমান বা বেশি হয়, তাহলে "flood" বলা।
    এটার কোনো lead-time নেই (শুধু বর্তমান অবস্থা দেখে, ভবিষ্যদ্বাণী করে না)
    — তাই বাস্তব ব্যবহারিক মূল্য কম, কিন্তু comparison baseline হিসেবে
    গুরুত্বপূর্ণ, কারণ FloodAI-র advantage (advance warning) কতটা বাস্তব
    সেটা প্রমাণ করার জন্য এই ন্যূনতম ভিত্তি দরকার।
    """
    if water_level_m is None or danger_level_m is None:
        return False
    return water_level_m >= danger_level_m


def baseline_predict_with_trend(water_level_series_m: list, danger_level_m: float, lookback_days: int = 3) -> bool:
    """
    একটু উন্নত বেসলাইন (ঐচ্ছিক) — গত কয়েকদিনের water-level trend দেখে
    সরল linear extrapolation দিয়ে আগামীকাল danger level cross করবে
    কিনা অনুমান করে। এটা এখনো কোনো rainfall/upstream data ব্যবহার করে
    না, শুধু নিজের গত কয়দিনের প্রবণতা দেখে — FloodAI-র rainfall+upstream
    ব্যবহার করার advantage measure করার জন্য এটা একটা মাঝামাঝি ধাপ।
    """
    if not water_level_series_m or len(water_level_series_m) < 2 or danger_level_m is None:
        return baseline_predict(water_level_series_m[-1] if water_level_series_m else None, danger_level_m)

    recent = water_level_series_m[-lookback_days:]
    daily_rise = (recent[-1] - recent[0]) / max(len(recent) - 1, 1)
    projected_tomorrow = recent[-1] + daily_rise
    return projected_tomorrow >= danger_level_m


if __name__ == "__main__":
    # ছোট self-test
    print("বর্তমান স্তর ১৫মি, danger ১৪মি ->", baseline_predict(15.0, 14.0))   # True
    print("বর্তমান স্তর ১২মি, danger ১৪মি ->", baseline_predict(12.0, 14.0))   # False
    print("trend-based (ক্রমবর্ধমান):", baseline_predict_with_trend([12.0, 12.8, 13.6], 14.0))  # True
