# train_model.py

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from datetime import datetime

print("🌊 FloodAI ML Model Training শুরু হচ্ছে...")

# ─────────────────────────────────
# Step 1: Synthetic Data Generate
# ─────────────────────────────────

np.random.seed(42)
n_samples = 8000

# ⚠️ RIVER-AWARE TRAINING DATA (আগে এখানে সব sample একই generic discharge
# distribution থেকে আসত, যেন সব নদী একরকম — ছোট নদী ফেনী (danger_level 5.5m)
# আর বড় নদী যমুনা (danger_level 19.5m) কে একইভাবে treat করা হতো।
#
# এখন backend/app.py এর ৬৪ জেলার আসল danger_level distribution থেকে bootstrap
# sample করে প্রতিটা sample এর জন্য একটা "simulated river" বানানো হচ্ছে, তারপর
# discharge কে সেই নদীর নিজস্ব reference_discharge (= danger_level * 100, ঠিক
# model.py এর get_reference_discharge() এর মতোই সূত্র) এর সাপেক্ষে জেনারেট করা
# হচ্ছে। এতে ML model rule engine এর সাথে একই scientific assumption শেয়ার করে।
REAL_DANGER_LEVELS = [
    2.5, 2.5, 2.5, 3.0, 3.0, 3.5, 3.5, 3.5, 3.5, 4.0, 4.0, 4.0,
    4.5, 5.0, 5.0, 5.5, 5.5, 5.5, 5.5, 6.0, 6.0, 7.0, 7.0, 7.0, 7.5, 7.5, 7.5,
    7.5, 7.5, 7.8, 8.0, 8.0, 8.2, 8.5, 8.5, 8.5, 8.5, 9.0, 9.0, 9.5, 9.5, 10.0,
    10.0, 10.5, 10.5, 11.0, 11.0, 11.0, 11.5, 12.0, 12.0, 13.0, 13.5, 14.0, 14.0,
    14.5, 14.5, 14.5, 15.5, 17.5, 18.5, 18.5, 19.5, 19.5,
]

data = []

for _ in range(n_samples):
    month = np.random.randint(1, 13)
    is_monsoon = 1 if 6 <= month <= 10 else 0

    # এই sample টার জন্য একটা নদী simulate করা (আসল distribution থেকে)
    danger_level = float(np.random.choice(REAL_DANGER_LEVELS))
    reference_discharge = danger_level * 100  # get_reference_discharge() এর সূত্রের সাথে অভিন্ন

    # Discharge — reference_discharge এর অনুপাতে (gamma distribution, মৌসুমে বেশি)
    ratio_shape, ratio_scale = (2.2, 0.42) if is_monsoon else (1.4, 0.18)
    discharge_ratio_val = float(np.random.gamma(ratio_shape, ratio_scale))
    discharge = max(reference_discharge * discharge_ratio_val, 50)

    # Upstream rain
    upstream_rain = np.random.exponential(
        10 if is_monsoon else 2
    )

    # Local rain
    local_rain = np.random.exponential(
        7 if is_monsoon else 1.5
    )

    # Previous 5 day rain
    prev_5day = np.random.exponential(
        35 if is_monsoon else 8
    )

    # Soil moisture
    soil_moisture = min(
        0.3 + (prev_5day / 150) + np.random.normal(0, 0.1), 1.0
    )
    soil_moisture = max(soil_moisture, 0.1)

    # CN value
    cn = np.random.uniform(70, 92)

    # Lag time
    lag_time = np.random.choice([8, 10, 12, 15, 18, 22, 24, 36, 48])

    # Risk category
    risk_cat = np.random.choice(
        [0, 1, 2, 3],
        p=[0.1, 0.3, 0.4, 0.2]
    )  # 0=কম, 1=মাঝারি, 2=উচ্চ, 3=অতি উচ্চ

    # Discharge change
    discharge_prev = discharge * np.random.uniform(0.7, 1.2)
    discharge_change = discharge - discharge_prev

    # Runoff
    S = (25400 / cn) - 254
    Ia = 0.2 * S
    if local_rain > Ia:
        runoff = ((local_rain - Ia) ** 2) / (local_rain + 0.8 * S)
    else:
        runoff = 0

    # ─── Flood Logic (rule engine এর reference_discharge ratio বাকেটের সাথে
    # সামঞ্জস্যপূর্ণ — আগে absolute discharge (>18000/>22000) ব্যবহার হতো, যেটা
    # ছোট নদীতে কখনো ট্রিগার হতোই না। এখন discharge_ratio_val (নদীর নিজস্ব
    # danger_level এর সাপেক্ষে) দিয়ে ট্রিগার হচ্ছে, তাই ছোট নদীও নিজের স্কেলে
    # flood label পায়) ───
    flood = 0

    # Rule 1: উচ্চ ratio + upstream rain
    if discharge_ratio_val > 1.5 and upstream_rain > 15:
        flood = 1
    # Rule 2: খুব উচ্চ ratio (নিজের danger_level এর দেড়গুণের বেশি)
    elif discharge_ratio_val > 1.3:
        flood = 1
    # Rule 3: Monsoon + saturated soil + upstream rain
    elif is_monsoon and soil_moisture > 0.75 and upstream_rain > 8:
        flood = np.random.choice([0, 1], p=[0.25, 0.75])
    # Rule 4: High risk district + monsoon + rain
    elif risk_cat >= 2 and is_monsoon and upstream_rain > 5:
        flood = np.random.choice([0, 1], p=[0.5, 0.5])
    # Rule 5: Moderate conditions (ratio-ভিত্তিক)
    elif discharge_ratio_val > 0.8 and prev_5day > 50:
        flood = np.random.choice([0, 1], p=[0.4, 0.6])

    # Add noise
    if np.random.random() < 0.04:
        flood = 1 - flood

    data.append({
        # Features
        'discharge': discharge,
        'discharge_prev': discharge_prev,
        'discharge_change': discharge_change,
        'upstream_rain': upstream_rain,
        'local_rain': local_rain,
        'prev_5day_rain': prev_5day,
        'soil_moisture': soil_moisture,
        'cn': cn,
        'lag_time': lag_time,
        'risk_category': risk_cat,
        'month': month,
        'is_monsoon': is_monsoon,
        'runoff': runoff,
        'discharge_ratio': discharge / reference_discharge,  # আগে discharge/20000 (fixed) ছিল
        'soil_upstream_interaction': soil_moisture * upstream_rain,

        # Target
        'flood': flood,
    })

df = pd.DataFrame(data)
print(f"✅ Data generated: {len(df)} samples")
print(f"   Flood cases: {df['flood'].sum()} ({df['flood'].mean()*100:.1f}%)")

# ─────────────────────────────────
# Step 2: Features & Target
# ─────────────────────────────────

FEATURES = [
    'discharge', 'discharge_change', 'discharge_ratio',
    'upstream_rain', 'local_rain', 'prev_5day_rain',
    'soil_moisture', 'cn', 'lag_time', 'risk_category',
    'month', 'is_monsoon', 'runoff',
    'soil_upstream_interaction',
]

X = df[FEATURES]
y = df['flood']

# ─────────────────────────────────
# Step 3: Split & Scale
# ─────────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ─────────────────────────────────
# Step 4: Train Model
# ─────────────────────────────────

print("\n🤖 Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1,
)
rf_model.fit(X_train_scaled, y_train)

print("🤖 Training Gradient Boosting...")
gb_model = GradientBoostingClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
)
gb_model.fit(X_train_scaled, y_train)

# ─────────────────────────────────
# Step 5: Evaluate
# ─────────────────────────────────

print("\n=== Random Forest Results ===")
rf_pred = rf_model.predict(X_test_scaled)
rf_prob = rf_model.predict_proba(X_test_scaled)[:, 1]
print(classification_report(y_test, rf_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, rf_prob):.3f}")

print("\n=== Gradient Boosting Results ===")
gb_pred = gb_model.predict(X_test_scaled)
gb_prob = gb_model.predict_proba(X_test_scaled)[:, 1]
print(classification_report(y_test, gb_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, gb_prob):.3f}")

# Best model select
rf_auc = roc_auc_score(y_test, rf_prob)
gb_auc = roc_auc_score(y_test, gb_prob)
best_model = rf_model if rf_auc >= gb_auc else gb_model
print(f"\n✅ Best model: {'Random Forest' if rf_auc >= gb_auc else 'Gradient Boosting'}")

# Cross validation
cv_scores = cross_val_score(
    best_model, X_train_scaled, y_train,
    cv=5, scoring='roc_auc'
)
print(f"Cross-val AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Feature importance
importance_df = pd.DataFrame({
    'feature': FEATURES,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop Features:")
print(importance_df.head(8).to_string())

# ─────────────────────────────────
# Step 6: Save
# ─────────────────────────────────
# ⚠️ model.py এর load_ml_model() ফাংশন 'model/flood_model.pkl' path থেকে
# load করে (একটা 'model/' subfolder এর ভিতর থেকে) — তাই এখানে ঠিক সেই
# subfolder এ সেভ করা হচ্ছে, নাহলে train করার পরও app.py silently
# rule-based fallback এ চলে যাবে, কোনো error না দেখিয়েই।
import os
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, 'flood_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)

with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

with open(os.path.join(MODEL_DIR, 'features.pkl'), 'wb') as f:
    pickle.dump(FEATURES, f)

print("\n✅ Model saved!")
print(f"   {MODEL_DIR}/flood_model.pkl")
print(f"   {MODEL_DIR}/scaler.pkl")
print(f"   {MODEL_DIR}/features.pkl")
print("\n⚠️ মনে রাখবে: app.py যেখান থেকে চলে, ঠিক তার পাশেই 'model/' ফোল্ডারটা রাখতে হবে,")
print("   নাহলে model.py এর load_ml_model() এই ফাইল খুঁজে পাবে না।")