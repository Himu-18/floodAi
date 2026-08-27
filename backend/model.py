# ============================================================
# FloodAI — model.py
# ML Flood Prediction Model & Category Logic
# ============================================================

# ============================================================
# FloodAI — model.py
# ML Flood Prediction Model & Category Logic
# ============================================================

import pickle
import numpy as np
from pathlib import Path
from datetime import datetime

from flood_types import coastal_tidal
from flood_types import riverine
from flood_types import flash_flood
from flood_types import urban_waterlogging
from flood_types import dam_affected

# ⚠️ আগে 'model/flood_model.pkl' একটা relative path ছিল — root থেকে backend
# চালালে এই path খুঁজে পেত না (কারণ Python CWD-ভিত্তিক relative path resolve
# করে), শুধু backend/ ফোল্ডার থেকে চালালেই পাওয়া যেত। এখন model.py-র নিজস্ব
# অবস্থান থেকে absolute path বানানো হচ্ছে (app.py-র .env আর database.py-র
# DB_PATH-এ যে একই BASE_DIR pattern ব্যবহার হয়েছে, এটাও ঠিক সেটাই), যাতে
# কোথা থেকে চালাও তাতে কিছু আসে যায় না — সবসময় backend/model/ ব্যবহার হবে।
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

# ── Module-level model cache ──
# আগে load_ml_model() প্রতিটা predict_flood() কলে (মানে প্রতিটা /api/flood
# request-এ) নতুন করে ৩টা pickle ফাইল ডিস্ক থেকে load করত — অহেতুক I/O,
# request latency বাড়ায়। এখন module import হওয়ার সময় একবারই load হবে,
# তারপর সব request একই in-memory object পুনরায় ব্যবহার করবে।
_ML_MODEL_CACHE = {"loaded": False, "model": None, "scaler": None, "features": None}


def load_ml_model():
    """Trained model load করো (module-level cache, প্রথমবারের পর disk touch করে না)"""
    if _ML_MODEL_CACHE["loaded"]:
        return _ML_MODEL_CACHE["model"], _ML_MODEL_CACHE["scaler"], _ML_MODEL_CACHE["features"]

    try:
        with open(MODEL_DIR / 'flood_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(MODEL_DIR / 'scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open(MODEL_DIR / 'features.pkl', 'rb') as f:
            features = pickle.load(f)
        _ML_MODEL_CACHE.update(loaded=True, model=model, scaler=scaler, features=features)
        print(f"✅ ML model cache-এ লোড হয়েছে ({MODEL_DIR})")
    except Exception as e:
        # Development mode error handling — model ফাইল না থাকলে rule-based
        # fallback-এ চলে যাবে। এই ব্যর্থতাও cache করা হচ্ছে (loaded=True,
        # সব None) যাতে প্রতি request-এ বারবার একই ব্যর্থ disk read না হয়।
        print(f"⚠️ ML model লোড ব্যর্থ, rule-based fallback ব্যবহার হবে: {e}")
        _ML_MODEL_CACHE.update(loaded=True, model=None, scaler=None, features=None)

    return _ML_MODEL_CACHE["model"], _ML_MODEL_CACHE["scaler"], _ML_MODEL_CACHE["features"]


def get_reference_discharge(danger_level, district_name=None):
    """
    ⚠️ এটা একটা APPROXIMATION, real rating curve (stage-discharge relationship) না।

    আদর্শভাবে discharge (m3/s, প্রবাহের হার) আর danger_level (মিটার, পানির উচ্চতা)
    সরাসরি তুলনা করা যায় না — এই দুটো ভিন্ন physical quantity, আর এদের মধ্যে সম্পর্ক
    প্রতিটা নদীর প্রতিটা gauge station এর নিজস্ব rating curve (Q = a(H-h0)^b) দিয়ে
    নির্ধারিত হয়, যেটা বছরের পর বছরের real measurement থেকে বের করতে হয়।

    ── জেলা-বাই-জেলা verification (২০২৬-০৮) ──
    district_profiles/ ফোল্ডারে এখন প্রতিটা জেলার real hydrology literature
    (academic paper, FFWC bulletin, BWDB report) থেকে verified reference
    discharge আছে। district_name দেওয়া থাকলে সেটা আগে চেক করা হয় — পাওয়া গেলে
    এই verified সংখ্যা ব্যবহার হয়, না পাওয়া গেলে (এখনো verify না-হওয়া জেলা)
    পুরনো danger_level*100 approximation-এ fallback করে। এভাবে যে জেলাগুলো
    এখনো profile করা হয়নি, সেগুলোতে কোনো regression হয় না।

    ভবিষ্যতে বাকি জেলাগুলোও profile হয়ে গেলে, শুধু district_profiles/ ফোল্ডারে
    নতুন ফাইল যোগ করলেই এই ফাংশন স্বয়ংক্রিয়ভাবে সেটা ব্যবহার করবে — কোড বদলাতে হবে না।
    """
    if not danger_level or danger_level <= 0:
        return None

    if district_name:
        try:
            from data import district_profiles_loader as _dpl
            correction = _dpl.get_correction_by_danger_level(district_name, danger_level)
            if correction and correction.get("reference_discharge_m3s"):
                return correction["reference_discharge_m3s"]
        except Exception as e:
            print(f"⚠️ district_profiles_loader থেকে reference_discharge আনতে ব্যর্থ ({district_name}): {e}")

    return danger_level * 100


def get_reference_discharge_correction_info(danger_level, district_name=None):
    """
    get_reference_discharge()-এর মতোই, কিন্তু শুধু সংখ্যা না — পুরো correction info
    (is_large_divergence সহ) ফেরত দেয়, যাতে caller বুঝতে পারে ML feature হিসেবে
    ব্যবহার করা নিরাপদ কিনা।
    """
    if not danger_level or danger_level <= 0 or not district_name:
        return None
    try:
        from data import district_profiles_loader as _dpl
        return _dpl.get_correction_by_danger_level(district_name, danger_level)
    except Exception as e:
        print(f"⚠️ district_profiles_loader correction info আনতে ব্যর্থ ({district_name}): {e}")
        return None


def predict_flood(
    discharge,
    upstream_rain,
    local_rain,
    soil_moisture,
    lag_time,
    cn,
    risk_category,
    month=None,
    district_name=None,
    flood_type=None,
    vulnerable_areas=None,
    recent_reports=0,
    is_full_moon=False,
    danger_level=None,
    confluence_data=None,
    rainfall_intensity_data=None,
    upstream_rain_history=None,
    cyclone_signal=0,
    tide_ratio=None
):
    if month is None:
        month = datetime.now().month
    if vulnerable_areas is None:
        vulnerable_areas = []
    if recent_reports is None:
        recent_reports = 0

    is_monsoon = 1 if 6 <= month <= 10 else 0
    risk_map = {"অতি উচ্চ": 3, "উচ্চ": 2, "মাঝারি": 1, "কম": 0}
    risk_num = risk_map.get(risk_category, 1)

    # Runoff calculate
    S = (25400 / cn) - 254
    Ia = 0.2 * S
    runoff = max(0, ((local_rain - Ia) ** 2) / (local_rain + 0.8 * S)) if local_rain > Ia else 0

    # discharge কে নদীর নিজস্ব danger_level এর সাপেক্ষে reference করা হচ্ছে —
    # এই একই reference_discharge এখন ML feature আর rule-based fallback দুই
    # জায়গাতেই ব্যবহার হবে, যাতে দুটো logic একই scientific assumption শেয়ার করে।
    reference_discharge = get_reference_discharge(danger_level, district_name)

    # ⚠️ জেলা-বাই-জেলা verification-এ কিছু জেলায় (বিশেষত পদ্মা/যমুনার মতো
    # mega_trunk নদী) দেখা গেছে verified reference_discharge পুরনো
    # danger_level*100 approximation থেকে ৩ গুণের বেশি আলাদা। ML model
    # train হয়েছিল পুরনো approximation-ভিত্তিক synthetic data দিয়ে, তাই
    # এত বড় scale-এ হঠাৎ input বদলে দিলে model ভুল বুঝতে পারে (retrain
    # ছাড়া)। তাই এই ধরনের জেলায় ML স্কিপ করে rule-based fallback ব্যবহার
    # করা হচ্ছে — এটা কম risky, কারণ rule-based logic সরাসরি এই corrected
    # সংখ্যা দিয়েই কাজ করে, কোনো training-time assumption বহন করে না।
    correction_info = get_reference_discharge_correction_info(danger_level, district_name)
    # ⚠️ FIX (২০২৬-০৮): তাইডাল (Coastal & Tidal) নদীর জন্য discharge_ratio
    # feature-টা ML model-এর কাছেও সমানভাবে অর্থহীন (জোয়ার-ভাটায় প্রবাহ
    # দিনে দুইবার দিক বদলায়) — তাই is_large_divergence-এর মতো এখানেও ML
    # স্কিপ করে rule-based fallback-এ পাঠানো হচ্ছে, যেখানে discharge_score
    # আলাদাভাবে বাদ দেওয়া হয়েছে তাইডাল জেলার জন্য (নিচে দেখুন)।
    skip_ml_large_divergence = bool(correction_info and correction_info.get("is_large_divergence")) or flood_type == "Coastal & Tidal"

    # ── ML Model Load ──
    model, scaler, features = load_ml_model()
    
    ml_used = False
    probability = 0

    if model and scaler and not skip_ml_large_divergence:
        # train_model.py (retrained, river-aware ভার্সন) এর discharge_ratio feature
        # ঠিক এই একই সূত্র (discharge / reference_discharge) দিয়ে তৈরি হয়েছে —
        # danger_level পাওয়া না গেলে পুরনো fixed /20000 fallback ব্যবহার হবে।
        discharge_ratio_feature = (discharge / reference_discharge) if reference_discharge else (discharge / 20000)
        X = np.array([[
            discharge,
            0,                          # discharge_change (fallback 0)
            discharge_ratio_feature,    # discharge_ratio — এখন danger_level-ভিত্তিক
            upstream_rain,
            local_rain,
            local_rain * 3,             # prev_5day estimate
            soil_moisture,
            cn,
            lag_time,
            risk_num,
            month,
            is_monsoon,
            runoff,
            soil_moisture * upstream_rain,
        ]])
        try:
            X_scaled = scaler.transform(X)
            probability = round(model.predict_proba(X_scaled)[0][1] * 100, 1)
            ml_used = True
        except Exception as e:
            # আগে এখানে bare `except: pass` ছিল — ML prediction fail করলে
            # সম্পূর্ণ silent থেকে rule-based fallback-এ চলে যেত, কিন্তু কেন
            # fail করলো (feature shape mismatch, scaler ভার্সন মিসম্যাচ
            # ইত্যাদি) সেটা log-এ দেখার উপায় ছিল না। এখন log হবে, fallback
            # আচরণ (ml_used=False থেকে যাওয়া) অপরিবর্তিত।
            print(f"⚠️ ML prediction ব্যর্থ, rule-based fallback ব্যবহার হবে: {e}")

    # score_breakdown এ দেখানোর জন্য প্রতিটা component আলাদাভাবে ট্র্যাক করা হচ্ছে,
    # যাতে breakdown আসল স্কোরিং এর সাথে সবসময় sync থাকে (আগে এখানে একটা আলাদা
    # ফেক ফর্মুলা ছিল যেটা প্রকৃত score এর সাথে মিলত না)।
    discharge_score = upstream_score = local_score = soil_score = 0
    season_score = base_risk_score = lag_score = cn_score = 0

    # ── Rule-based Fallback (If ML fails or not used) ──
    if not ml_used:
        score = 0

        # discharge কে নদীর নিজস্ব danger_level এর সাপেক্ষে স্কোর করা হচ্ছে,
        # আগে যেভাবে সব নদীতে একই fixed threshold (20000/15000/...) বসানো ছিল
        # সেটা ছোট নদী (যেমন ফেনী, danger_level 5.5m) আর বড় নদী (যেমন যমুনা,
        # danger_level 19.5m) কে একইভাবে treat করত, যেটা বাস্তবসম্মত না।
        # (reference_discharge উপরে একবার হিসাব করা হয়েছে, এখানে আবার করার দরকার নেই)
        # ⚠️ FIX (২০২৬-০৮): জোয়ার-ভাটা নিয়ন্ত্রিত নদীতে (Coastal & Tidal
        # flood_type) discharge-ratio concept-টাই অর্থহীন — প্রবাহ দিনে
        # দুইবার দিক বদলায় জোয়ারের কারণে, কোনো একমুখী upstream discharge
        # হিসেবে এটাকে danger_level-এর সাথে তুলনা করা যায় না (খুলনার profile
        # ফাইলেই এটা আগে থেকে flag করা ছিল)। তাই এই flood_type-এ discharge_score
        # স্কিপ করা হচ্ছে — বৃষ্টি/soil-moisture/মৌসুম component ও
        # coastal_tidal.py-র পূর্ণিমা/cyclone override-ই score চালাবে।
        if flood_type == "Coastal & Tidal":
            discharge_score = 0
        elif reference_discharge:
            discharge_ratio_vs_danger = discharge / reference_discharge
            if discharge_ratio_vs_danger > 1.5: discharge_score = 30
            elif discharge_ratio_vs_danger > 1.0: discharge_score = 22
            elif discharge_ratio_vs_danger > 0.7: discharge_score = 15
            elif discharge_ratio_vs_danger > 0.4: discharge_score = 8
            else: discharge_score = 3
        else:
            # danger_level পাওয়া না গেলে (backward-compatible fallback),
            # আগের fixed threshold ব্যবহার করা হচ্ছে যাতে crash না হয়।
            if discharge > 20000: discharge_score = 30
            elif discharge > 15000: discharge_score = 22
            elif discharge > 10000: discharge_score = 15
            elif discharge > 5000: discharge_score = 8
            else: discharge_score = 3
        score += discharge_score

        if upstream_rain > 20: upstream_score = 25
        elif upstream_rain > 10: upstream_score = 18
        elif upstream_rain > 5: upstream_score = 10
        elif upstream_rain > 0: upstream_score = 5
        score += upstream_score

        if local_rain > 50: local_score = 15
        elif local_rain > 20: local_score = 10
        elif local_rain > 5: local_score = 5
        score += local_score

        if soil_moisture > 0.8: soil_score = 15
        elif soil_moisture > 0.6: soil_score = 10
        elif soil_moisture > 0.4: soil_score = 5
        score += soil_score

        if 6 <= month <= 9: season_score = 10
        elif month in [5, 10]: season_score = 5
        score += season_score

        base_risk_score = risk_num * 3
        score += base_risk_score

        if lag_time <= 10: lag_score = 5
        elif lag_time <= 20: lag_score = 2
        score += lag_score

        cn_score = max(0, (cn - 70) // 5)
        score += cn_score

        probability = min(score, 100)

    # =========================================================
    # 🌟 SPECIFIC FLOOD TYPE LOGIC OVERRIDES 
    # =========================================================
    
    # 1. Flash Flood (পাহাড়ি ঢল)
    # — flood_types/flash_flood.py তে সরানো হলো: এখন সম্ভব হলে ৬-ঘণ্টার
    # rolling rainfall intensity ব্যবহার করে (দৈনিক total-এর বদলে),
    # কারণ গবেষণা বলছে flash flood-এর real trigger হলো short-duration
    # intensity (সিলেটে ৬ ঘণ্টায় ১৮৬মিমি-এর মতো), দৈনিক যোগফল না।
    intensity_used = False
    intensity_method = "not_applicable"
    if flood_type == "Flash Flood":
        probability, intensity_used, intensity_method = flash_flood.apply_override(
            probability, local_rain, upstream_rain, rainfall_intensity_data
        )

    # 2. Urban Waterlogging (শহুরে জলাবদ্ধতা)
    # — flood_types/urban_waterlogging.py তে সরানো হলো: এখন চট্টগ্রামের
    # মতো tidal-influenced শহরে ভরা কটালের সময় drainage tide-lock bonus
    # যোগ হয় (is_full_moon এমনিতেই calculate হচ্ছিল, নতুন call লাগেনি)।
    tide_lock_applied = False
    if flood_type == "Urban Waterlogging":
        probability, tide_lock_applied = urban_waterlogging.apply_override(
            probability, district_name, local_rain, is_full_moon, rainfall_intensity_data
        )

    # 3. Coastal & Tidal (উপকূলীয় ও জোয়ার)
    # — এই flood_type-এর সম্পূর্ণ logic এখন flood_types/coastal_tidal.py তে,
    # কারণ tide-API (WorldTides/Stormglass) integrate হলে এটাই সবচেয়ে বড়
    # হতে যাচ্ছে। moon_bonus_applied নিচে message আর score_breakdown এ
    # আবার ব্যবহার হয়, যাতে is_full_moon চেক দুইবার লিখতে না হয়।
    moon_bonus_applied = False
    if flood_type == "Coastal & Tidal":
        probability, moon_bonus_applied = coastal_tidal.apply_override(
            probability, local_rain, is_full_moon, cyclone_signal, tide_ratio
        )

    # 4. Dam-Affected (ড্যাম/ব্যারাজ প্রভাবিত)
    # — flood_types/dam_affected.py তে সরানো হলো: DFO archive বিশ্লেষণে
    # পাওয়া গেছে এই category-র বন্যা গড়ে ৩৪ দিন স্থায়ী হয় (বাকিদের
    # ৮-১৩ দিনের তুলনায়) — তাই শুধু আজকের upstream_rain না, টানা কত
    # দিন ধরে upstream-এ বৃষ্টি চলছে (sustained_days) সেটাও বিবেচনা করা হয়।
    sustained_days = 0
    if flood_type == "Dam-Affected":
        probability, sustained_days = dam_affected.apply_override(
            probability, upstream_rain, upstream_rain_history
        )

    # 5. Riverine (নদী বিধৌত / ক্লাসিক বন্যা)
    # — flood_types/riverine.py তে সরানো হলো: পদ্মা+যমুনার সঙ্গমস্থলের কাছের
    # ৫টা জেলার জন্য "দুই প্রধান নদীর peak synchronization" চেক করা হয়।
    # confluence_data app.py থেকে আসে (শুধু ঐ ৫ জেলার জন্য পাঠানো হবে,
    # বাকিদের জন্য None থাকবে এবং কোনো override হবে না)।
    synchronized_peak = False
    rain_floor_applied = False
    if flood_type == "Riverine":
        probability, synchronized_peak, rain_floor_applied = riverine.apply_override(
            probability, confluence_data, local_rain, upstream_rain
        )

    # =========================================================
    # 🌟 COMMUNITY REPORT OVERRIDE
    # =========================================================
    reports_note = None
    if recent_reports >= 5:
        probability = max(probability, 85)
        reports_note = f"{recent_reports}টি সাম্প্রতিক কমিউনিটি রিপোর্ট নিশ্চিত করছে পরিস্থিতি গুরুতর"
    elif recent_reports >= 3:
        probability = max(probability, 65)
        reports_note = f"{recent_reports}টি সাম্প্রতিক কমিউনিটি রিপোর্ট পাওয়া গেছে"
    elif recent_reports >= 1:
        probability = min(probability + (recent_reports * 5), 100)
        reports_note = f"{recent_reports}টি কমিউনিটি রিপোর্ট পর্যবেক্ষণে রাখা হয়েছে"

    probability = round(probability, 1)

    # ── Warning Level & Messages ──
    if probability >= 70:
        level = "বিপদ"
        color = "red"
        message = "🚨 বন্যার আশঙ্কা অনেক বেশি! এখনই পরিবার নিয়ে নিরাপদ জায়গায় যান।"
        action = ["পরিবার নিয়ে উঁচু জায়গায় যান", "মূল্যবান জিনিস উঁচুতে রাখুন", "জরুরি নম্বরে যোগাযোগ করুন: 999", "নিকটস্থ আশ্রয়কেন্দ্রে যান"]
    elif probability >= 50:
        level = "সতর্ক"
        color = "orange"
        message = f"⚠️ {lag_time} ঘণ্টার মধ্যে পানি বাড়তে পারে। সতর্ক থাকুন।"
        action = ["শুকনো খাবার ও পানি মজুত করুন", "ফোন চার্জ রাখুন", "আবহাওয়ার আপডেট রাখুন", "জরুরি জিনিস প্রস্তুত রাখুন"]
    elif probability >= 30:
        level = "সাবধান"
        color = "yellow"
        message = "⚠️ বন্যার সম্ভাবনা আছে। নজর রাখুন।"
        action = ["আবহাওয়ার দিকে নজর রাখুন", "জরুরি জিনিস প্রস্তুত রাখুন", "পরিবারকে সতর্ক করুন"]
    else:
        level = "নিরাপদ"
        color = "green"
        message = "✅ এলাকা এখন নিরাপদ। তবে আবহাওয়া পর্যবেক্ষণ করুন।"
        action = ["নিয়মিত আপডেট দেখুন", "আবহাওয়ার দিকে নজর রাখুন"]

    # ── Text Formatting ──
    if vulnerable_areas and probability >= 50:
        areas_text = ", ".join(vulnerable_areas[:5])
        message += f" বিশেষভাবে ঝুঁকিপূর্ণ এলাকা: {areas_text}।"

    if reports_note:
        message += f" ({reports_note}।)"
        
    moon_message = coastal_tidal.get_message_fragment(moon_bonus_applied, cyclone_signal, tide_ratio)
    if moon_message:
        message += moon_message

    tide_lock_message = urban_waterlogging.get_message_fragment(tide_lock_applied)
    if tide_lock_message:
        message += tide_lock_message

    dam_message = dam_affected.get_message_fragment(sustained_days)
    if dam_message:
        message += dam_message

    riverine_message = riverine.get_message_fragment(synchronized_peak, rain_floor_applied)
    if riverine_message:
        message += riverine_message

    flash_flood_message = flash_flood.get_message_fragment(intensity_used, intensity_method)
    if flash_flood_message:
        message += flash_flood_message

    return {
        "probability": probability,
        "level": level,
        "color": color,
        "message": message,
        "action": action,
        "ml_model_used": ml_used,
        "ml_skipped_reason": "verified_discharge_diverges_from_training_assumption" if skip_ml_large_divergence else None,
        "flood_type": flood_type,
        "vulnerable_areas": vulnerable_areas,
        "recent_reports": recent_reports,
        "score_breakdown": {
            "discharge": f"{discharge_score}/30",
            "upstream_rain": f"{upstream_score}/25",
            "local_rain": f"{local_score}/15",
            "soil_moisture": f"{soil_score}/15",
            "season": f"{season_score}/10",
            "base_risk": f"{base_risk_score}/9",
            "lag_time": f"{lag_score}/5",
            "curve_number": f"{cn_score}/6",
            "moon_effect": f"{'20' if moon_bonus_applied else '0'}/20",
            "confluence_effect": f"{'15' if synchronized_peak else '0'}/15",
            "tide_lock_effect": f"{'10' if tide_lock_applied else '0'}/10",
            "sustained_upstream_rain_days": sustained_days,
            "note": "ML model ব্যবহৃত হলে এই breakdown প্রযোজ্য নয়" if ml_used else "Rule-based fallback breakdown",
        },
        "input_summary": {
            "discharge_m3s": round(discharge),
            "upstream_rain_mm": upstream_rain,
            "local_rain_mm": local_rain,
            "soil_moisture": soil_moisture,
            "lag_time_hours": lag_time,
            "curve_number": cn,
            "runoff_mm": round(runoff, 2),
            "month": month,
            "is_monsoon": bool(is_monsoon),
            "is_full_moon": is_full_moon,
            "danger_level_m": danger_level,
            "reference_discharge_m3s": reference_discharge,
            "confluence_data": confluence_data,
            "rainfall_intensity_data": rainfall_intensity_data,
            "rainfall_intensity_method": intensity_method,
            "upstream_rain_history": upstream_rain_history,
        }
    }