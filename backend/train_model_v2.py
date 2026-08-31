# backend/train_model_v2.py
# ============================================================
# FloodAI — Real-Data ML Training, ধাপ ২: প্রকৃত ডেটায় Train + Evaluate
# ============================================================
# আগের train_model.py সম্পূর্ণ সিন্থেটিক (rule-generated) label দিয়ে
# train/evaluate করত — তাই তার "accuracy" বাস্তব predictive power প্রমাণ
# করত না। এই ভার্সন backtest_results.csv (real DFO flood events, ১৯৮৫-২০২১)
# ও negative_samples.csv (একই জেলার real "স্বাভাবিক" দিন) মিলিয়ে একটা
# real dataset বানায়, এবং advisor-এর সতর্কতা অনুযায়ী **সময়-ভিত্তিক
# (temporal) train/test split** ব্যবহার করে (random split না, কারণ
# random split করলে data leakage হতে পারে সময়-নির্ভর ডেটায়)।
#
# ⚠️ চালানোর আগে দরকার:
#   1. py backtest_dfo.py           (backtest_results.csv তৈরি করে)
#   2. py prepare_negative_samples.py  (negative_samples.csv তৈরি করে)
#   3. py train_model_v2.py         (এই script)
#
# ⚠️ সততার সাথে সীমাবদ্ধতা:
# - মোট sample সংখ্যা ছোট (~২০৮টা: ১০৪ positive + ১০৪ negative) — এটা
#   RandomForest-এর জন্য যথেষ্ট না একটা অত্যন্ত নির্ভরযোগ্য মডেল বানাতে,
#   কিন্তু এটাই প্রথম real-data baseline, ভবিষ্যতে backtest_v2.py-র
#   ফলাফল যোগ হলে dataset বড় হবে।
# - Negative sample-গুলো "flood date থেকে ১৮০ দিন দূরে" ধরে অনুমান করা
#   (সরাসরি verified না যে সেই তারিখে সত্যিই কোনো বন্যা ছিল না)।
# - Feature set সীমিত (শুধু rain/discharge/soil-moisture/month) — district
#   profile-এর richer feature (CN, lag_time, flood_type ইত্যাদি) এখনো
#   যোগ করা হয়নি, ভবিষ্যতে Model A/B/C ablation পরীক্ষায় যোগ করা যাবে
#   (advisor-এর point ১১)।

import csv
import pickle
from pathlib import Path
from datetime import datetime

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score

POSITIVE_CSV = Path(__file__).parent / "backtest_results.csv"
NEGATIVE_CSV = Path(__file__).parent / "negative_samples.csv"
MODEL_OUT = Path(__file__).parent / "model" / "flood_model_v2_real_data.pkl"

# advisor-এর সুপারিশ অনুযায়ী: পুরনো বছর দিয়ে train, নতুন বছর দিয়ে test —
# random split না, কারণ time-series ডেটায় random split করলে ভবিষ্যতের
# তথ্য train set-এ leak হয়ে যেতে পারে (data leakage)।
TRAIN_TEST_SPLIT_YEAR = 2015  # ২০১৫-এর আগে train, ২০১৫+ test


def load_dataset():
    rows = []

    if POSITIVE_CSV.exists():
        with open(POSITIVE_CSV, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                rows.append({
                    "date": r["date"],
                    "local_rain_mm": float(r["local_rain_mm"] or 0),
                    "upstream_rain_mm": float(r["upstream_rain_mm"] or 0),
                    "discharge_m3s": float(r["discharge_m3s"] or 0),
                    "soil_moisture": float(r["soil_moisture"] or 0.5),
                    "actual_flood": 1,
                })
    else:
        print(f"⚠️ {POSITIVE_CSV} পাওয়া যায়নি — আগে backtest_dfo.py চালান।")

    if NEGATIVE_CSV.exists():
        with open(NEGATIVE_CSV, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                rows.append({
                    "date": r["date"],
                    "local_rain_mm": float(r["local_rain_mm"] or 0),
                    "upstream_rain_mm": float(r["upstream_rain_mm"] or 0),
                    "discharge_m3s": float(r["discharge_m3s"] or 0),
                    "soil_moisture": float(r["soil_moisture"] or 0.4),
                    "actual_flood": 0,
                })
    else:
        print(f"⚠️ {NEGATIVE_CSV} পাওয়া যায়নি — আগে prepare_negative_samples.py চালান।")

    return rows


def build_features(rows):
    X, y, years = [], [], []
    for r in rows:
        month = datetime.strptime(r["date"], "%Y-%m-%d").month
        is_monsoon = 1 if 6 <= month <= 10 else 0
        X.append([r["local_rain_mm"], r["upstream_rain_mm"], r["discharge_m3s"], r["soil_moisture"], month, is_monsoon])
        y.append(r["actual_flood"])
        years.append(datetime.strptime(r["date"], "%Y-%m-%d").year)
    return np.array(X), np.array(y), np.array(years)


def temporal_split(X, y, years, split_year):
    train_mask = years < split_year
    test_mask = years >= split_year
    return X[train_mask], X[test_mask], y[train_mask], y[test_mask]


def run():
    print("🌊 FloodAI ML Model — Real Data দিয়ে Training (v2) শুরু হচ্ছে...")
    rows = load_dataset()
    if len(rows) < 20:
        print(f"❌ মোট শুধু {len(rows)}টা sample পাওয়া গেছে — training-এর জন্য যথেষ্ট না। "
              f"backtest_dfo.py ও prepare_negative_samples.py দুটোই চালিয়েছেন কিনা নিশ্চিত করুন।")
        return

    print(f"মোট sample: {len(rows)} (positive={sum(1 for r in rows if r['actual_flood']==1)}, "
          f"negative={sum(1 for r in rows if r['actual_flood']==0)})")

    X, y, years = build_features(rows)
    X_train, X_test, y_train, y_test = temporal_split(X, y, years, TRAIN_TEST_SPLIT_YEAR)

    print(f"\nTemporal split: train={len(X_train)} sample ({TRAIN_TEST_SPLIT_YEAR}-এর আগে), "
          f"test={len(X_test)} sample ({TRAIN_TEST_SPLIT_YEAR}+)")

    if len(X_train) < 10 or len(X_test) < 5:
        print("⚠️ train বা test set খুব ছোট — TRAIN_TEST_SPLIT_YEAR পরিবর্তন করে দেখুন, "
              "অথবা আরও sample (backtest_v2.py চালিয়ে) যোগ করুন।")

    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n=== আসল (real, সিন্থেটিক না) Test-Set Metrics ===")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"Recall:    {recall_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"F1-score:  {f1_score(y_test, y_pred, zero_division=0):.3f}")
    print("\nConfusion Matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_test, y_pred))
    print("\nবিস্তারিত রিপোর্ট:")
    print(classification_report(y_test, y_pred, target_names=["No Flood", "Flood"], zero_division=0))

    print("\n⚠️ তুলনা করার কথা মনে রাখবেন: এই সংখ্যাগুলোকে backend/validation/"
          "backtest_v2.py-র danger-level baseline-এর সাথে তুলনা করুন — যদি এই "
          "ML model simple baseline-কেও ভালো না করে, তাহলে জটিলতা বাড়ানোর "
          "সার্থকতা নেই (advisor-এর point ৯)।")

    MODEL_OUT.parent.mkdir(exist_ok=True)
    with open(MODEL_OUT, "wb") as f:
        pickle.dump(model, f)
    print(f"\n✅ Model সেভ হয়েছে: {MODEL_OUT}")
    print("   ⚠️ এটা এখনো production model.py-তে wire করা হয়নি ইচ্ছাকৃতভাবে — "
          "আগে metrics দেখে সিদ্ধান্ত নিন এটা পুরনো rule-based+synthetic-ML "
          "পদ্ধতির চেয়ে সত্যিই ভালো কিনা।")


if __name__ == "__main__":
    run()
