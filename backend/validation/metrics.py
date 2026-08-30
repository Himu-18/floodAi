# validation/metrics.py
# ============================================================
# FloodAI Validation — Metrics Module
# ============================================================
# শুধু "accuracy" না, advisor-এর সুপারিশ অনুযায়ী confusion matrix,
# precision/recall/F1, false-alarm-rate, miss-rate, এবং lead-time
# হিসাব করার জন্য reusable ফাংশন। কারণ accuracy একা বিভ্রান্তিকর হতে
# পারে (যদি বেশিরভাগ দিন "No Flood" হয়, তাহলে সবসময় "No Flood" বললেও
# উচ্চ accuracy আসবে, কিন্তু model আসলে flood ধরতেই পারছে না)।

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PredictionRecord:
    """একটা single prediction-vs-actual তুলনার রেকর্ড।"""
    station: str
    date: str
    predicted_flood: bool          # model কি flood বলেছিল
    actual_flood: bool             # বাস্তবে flood হয়েছিল কিনা (danger level cross করেছিল কিনা)
    predicted_at: Optional[str] = None   # prediction কবে করা হয়েছিল (lead-time হিসাবের জন্য)
    actual_flood_start: Optional[str] = None  # বাস্তব বন্যা কবে শুরু হয়েছিল


def confusion_matrix(records: List[PredictionRecord]) -> dict:
    """TP/FP/FN/TN গণনা করে।"""
    tp = sum(1 for r in records if r.predicted_flood and r.actual_flood)
    fp = sum(1 for r in records if r.predicted_flood and not r.actual_flood)
    fn = sum(1 for r in records if not r.predicted_flood and r.actual_flood)
    tn = sum(1 for r in records if not r.predicted_flood and not r.actual_flood)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "total": len(records)}


def compute_metrics(records: List[PredictionRecord]) -> dict:
    """
    Precision, Recall, F1, False Alarm Rate (FAR), Miss Rate — advisor-এর
    বলা সব মূল মেট্রিক একসাথে।
    """
    cm = confusion_matrix(records)
    tp, fp, fn, tn = cm["TP"], cm["FP"], cm["FN"], cm["TN"]

    precision = tp / (tp + fp) if (tp + fp) > 0 else None
    recall = tp / (tp + fn) if (tp + fn) > 0 else None  # = Detection Rate
    f1 = (2 * precision * recall / (precision + recall)
          if precision is not None and recall is not None and (precision + recall) > 0 else None)
    far = fp / (tp + fp) if (tp + fp) > 0 else None       # False Alarm Rate
    miss_rate = fn / (tp + fn) if (tp + fn) > 0 else None  # যত % প্রকৃত বন্যা মিস হয়েছে
    accuracy = (tp + tn) / cm["total"] if cm["total"] > 0 else None

    return {
        "confusion_matrix": cm,
        "accuracy": round(accuracy, 4) if accuracy is not None else None,
        "precision": round(precision, 4) if precision is not None else None,
        "recall": round(recall, 4) if recall is not None else None,
        "f1_score": round(f1, 4) if f1 is not None else None,
        "false_alarm_rate": round(far, 4) if far is not None else None,
        "miss_rate": round(miss_rate, 4) if miss_rate is not None else None,
    }


def compute_lead_time_hours(predicted_at: str, actual_flood_start: str) -> Optional[float]:
    """
    prediction কবে দেওয়া হয়েছিল বনাম বাস্তবে বন্যা কবে শুরু হয়েছিল —
    এই দুইয়ের ব্যবধান (ঘণ্টায়) হিসাব করে। ধনাত্মক মানে prediction আগে
    এসেছে (ভালো), ঋণাত্মক মানে দেরিতে এসেছে (খারাপ)।
    """
    from datetime import datetime
    try:
        p = datetime.fromisoformat(predicted_at)
        a = datetime.fromisoformat(actual_flood_start)
        return round((a - p).total_seconds() / 3600, 1)
    except Exception:
        return None


def lead_time_summary(lead_times_hours: List[float], threshold_hours: float = 24) -> dict:
    """
    advisor-এর উদাহরণের মতো: "FloodAI ৮২% ঘটনায় ≥২৪ ঘণ্টা আগাম সতর্কতা দিয়েছে"
    — এই ধরনের সারাংশ তৈরি করে।
    """
    valid = [lt for lt in lead_times_hours if lt is not None]
    if not valid:
        return {"count": 0, "avg_lead_time_hours": None, f"pct_with_ge_{int(threshold_hours)}h_lead": None}
    successful = [lt for lt in valid if lt >= threshold_hours]
    return {
        "count": len(valid),
        "avg_lead_time_hours": round(sum(valid) / len(valid), 1),
        f"pct_with_ge_{int(threshold_hours)}h_lead": round(100 * len(successful) / len(valid), 1),
    }


def compare_models(baseline_records: List[PredictionRecord], floodai_records: List[PredictionRecord]) -> dict:
    """
    advisor-এর সবচেয়ে গুরুত্বপূর্ণ experiment: FloodAI বনাম simple
    danger-level-threshold baseline — পাশাপাশি metrics দেখিয়ে scientifically
    বলা যাবে FloodAI আদৌ value add করছে কিনা।
    """
    return {
        "danger_level_baseline": compute_metrics(baseline_records),
        "floodai": compute_metrics(floodai_records),
    }


if __name__ == "__main__":
    # ছোট self-test — বাস্তব ডেটা ছাড়াই মেট্রিক ফাংশনগুলো ঠিকমতো কাজ করছে কিনা যাচাই
    sample = [
        PredictionRecord("Bahadurabad", "1998-07-15", True, True),
        PredictionRecord("Bahadurabad", "1998-07-16", True, False),
        PredictionRecord("Bahadurabad", "1998-07-17", False, True),
        PredictionRecord("Bahadurabad", "1998-07-18", False, False),
    ]
    print(compute_metrics(sample))
