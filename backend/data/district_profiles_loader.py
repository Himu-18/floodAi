# ============================================================
# FloodAI — data/district_profiles_loader.py
#
# সব district_profiles/*.py ফাইল পড়ে একটা lookup table বানায়, যাতে
# model.py আর flood_config.py migration script দুটোই ব্যবহার করতে পারে।
#
# এই ফাইলটা district_profiles/ ফোল্ডারে যত জেলা থাকবে (৪৬ হোক বা ৬৪),
# স্বয়ংক্রিয়ভাবে সবগুলো পড়বে — নতুন প্রোফাইল যোগ হলে কোড বদলাতে হবে না।
# ============================================================

import os
import glob
import importlib.util

_PROFILES_DIR = os.path.join(os.path.dirname(__file__), "districts_profiles")

_CACHE = {"loaded": False, "by_district": {}, "by_station_id": {}}


def _load_module(filepath):
    """একটা .py ফাইল থেকে dynamically module load করে {NAME}_PROFILE dict-টা খুঁজে বের করে।"""
    spec = importlib.util.spec_from_file_location("profile_mod", filepath)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"⚠️ প্রোফাইল লোড ব্যর্থ ({filepath}): {e}")
        return None

    for attr_name in dir(mod):
        if attr_name.endswith("_PROFILE") and not attr_name.startswith("_"):
            return getattr(mod, attr_name)
    return None


def _extract_station_correction(station):
    """একটা station dict থেকে corrected reference_discharge/cn/risk_category বের করে।"""
    ml = station.get("ml_features_verified", {})

    ref = ml.get("reference_discharge_m3s", {})
    corrected_discharge = ref.get("corrected_estimate")
    old_buggy_discharge = ref.get("old_buggy_value")

    cn_info = ml.get("cn", {})
    corrected_cn = cn_info.get("reviewed_estimate")

    risk_info = ml.get("risk_category", {})
    corrected_risk = risk_info.get("reviewed_estimate")
    # "উচ্চ (অপরিবর্তিত)" এর মতো টেক্সট থেকে শুধু আসল risk category শব্দটা বের করা
    if corrected_risk:
        for level in ["অতি উচ্চ", "উচ্চ", "মাঝারি", "কম"]:
            if corrected_risk.startswith(level):
                corrected_risk = level
                break

    # ML feature হিসেবে ব্যবহার করা কতটা নিরাপদ তা বোঝার জন্য divergence মাপা হচ্ছে —
    # পুরনো buggy সূত্র আর নতুন corrected সংখ্যা অনেক বেশি আলাদা হলে (৩ গুণের বেশি),
    # ML model-কে out-of-distribution ইনপুট দেওয়া ঝুঁকিপূর্ণ (retrain ছাড়া)।
    is_large_divergence = False
    if corrected_discharge and old_buggy_discharge and old_buggy_discharge > 0:
        divergence_ratio = max(corrected_discharge, old_buggy_discharge) / min(corrected_discharge, old_buggy_discharge)
        is_large_divergence = divergence_ratio >= 3.0

    return {
        "reference_discharge_m3s": corrected_discharge,
        "old_buggy_value": old_buggy_discharge,
        "is_large_divergence": is_large_divergence,
        "cn": corrected_cn,
        "risk_category": corrected_risk,
        "danger_level_m": station.get("danger_level_m"),
        "flood_type_note": station.get("flood_type_note"),
        "station_name": station.get("name"),
        "ffwc_id": station.get("ffwc_id"),
        "is_primary": station.get("is_primary", False),
        "confidence": ref.get("confidence", "unknown"),
    }


def _load_all():
    if _CACHE["loaded"]:
        return

    by_district = {}
    by_station_id = {}

    for filepath in sorted(glob.glob(os.path.join(_PROFILES_DIR, "*.py"))):
        profile = _load_module(filepath)
        if not profile:
            continue

        district_name = profile.get("district")
        if not district_name:
            continue

        stations = profile.get("stations")
        corrections = []

        if stations:
            # সাধারণ কেস — station list আছে
            for st in stations:
                corr = _extract_station_correction(st)
                corrections.append(corr)
                if corr["ffwc_id"]:
                    by_station_id[corr["ffwc_id"]] = corr
        else:
            # zero-station জেলা — দুই রকম format থাকতে পারে:
            # (ক) 'ml_features_verified' — লালমনিরহাট/নোয়াখালী/মেহেরপুর স্টাইল (numeric correction সহ)
            # (খ) 'flood_type_assessment' — খাগড়াছড়ি/রাঙ্গামাটি স্টাইল (কোনো station-ই নেই,
            #     তাই numeric correction সম্ভব না, শুধু qualitative geographic reasoning)
            ml = profile.get("ml_features_verified", {})
            flood_assessment = profile.get("flood_type_assessment", {})

            if ml:
                ref = ml.get("reference_discharge_m3s", {})
                cn_info = ml.get("cn", {})
                risk_info = ml.get("risk_category", {})
                corrected_risk = risk_info.get("reviewed_estimate")
                if corrected_risk:
                    for level in ["অতি উচ্চ", "উচ্চ", "মাঝারি", "কম"]:
                        if corrected_risk.startswith(level):
                            corrected_risk = level
                            break
                _corrected = ref.get("corrected_estimate")
                _old_buggy = ref.get("old_buggy_value")
                _large_div = False
                if _corrected and _old_buggy and _old_buggy > 0:
                    _dr = max(_corrected, _old_buggy) / min(_corrected, _old_buggy)
                    _large_div = _dr >= 3.0
                corrections.append({
                    "reference_discharge_m3s": _corrected,
                    "old_buggy_value": _old_buggy,
                    "is_large_divergence": _large_div,
                    "cn": cn_info.get("reviewed_estimate"),
                    "risk_category": corrected_risk,
                    "danger_level_m": None,
                    "flood_type_note": profile.get("flood_type_note"),
                    "station_name": None,
                    "ffwc_id": None,
                    "is_primary": True,
                    "confidence": ref.get("confidence", "unknown"),
                    "no_station_warning": profile.get("station_count_note"),
                })
            elif flood_assessment:
                # খাগড়াছড়ি/রাঙ্গামাটি ফরম্যাট — কোনো numeric correction নেই
                # (correct করার মতো কোনো station-ই নেই), কিন্তু flood_type
                # নিয়ে qualitative recommendation থাকতে পারে — সেটা রেকর্ড
                # করে রাখা হচ্ছে যাতে "covered districts" তালিকায় অন্তত
                # তাদের existence (এবং কেন কোনো correction নেই) ধরা পড়ে।
                corrections.append({
                    "reference_discharge_m3s": None,
                    "old_buggy_value": None,
                    "is_large_divergence": False,
                    "cn": None,
                    "risk_category": None,
                    "danger_level_m": None,
                    "flood_type_note": flood_assessment.get("reasoning"),
                    "flood_type_recommendation": flood_assessment.get("reviewed_recommendation"),
                    "station_name": None,
                    "ffwc_id": None,
                    "is_primary": True,
                    "confidence": "no_station_no_correction_possible",
                    "no_station_warning": profile.get("station_count_note"),
                })

        if corrections:
            by_district[district_name] = corrections

    _CACHE["loaded"] = True
    _CACHE["by_district"] = by_district
    _CACHE["by_station_id"] = by_station_id


def get_primary_correction(district_name):
    """একটা জেলার primary station-এর corrected তথ্য দেয় (flood_config.py migration-এর জন্য)।"""
    _load_all()
    corrections = _CACHE["by_district"].get(district_name, [])
    for c in corrections:
        if c.get("is_primary"):
            return c
    return corrections[0] if corrections else None


def get_correction_by_danger_level(district_name, danger_level):
    """
    একটা জেলার নির্দিষ্ট station (danger_level মিলিয়ে) এর corrected reference_discharge
    খুঁজে বের করে — model.py এর get_reference_discharge() এখান থেকে কল করবে।
    danger_level না মিললে primary station-এর তথ্য fallback হিসেবে দেয়।
    """
    _load_all()
    corrections = _CACHE["by_district"].get(district_name, [])
    if not corrections:
        return None

    if danger_level:
        for c in corrections:
            if c.get("danger_level_m") is not None and abs(c["danger_level_m"] - danger_level) < 0.01:
                return c

    # fallback — primary station
    return get_primary_correction(district_name)


def get_correction_by_station_id(ffwc_id):
    _load_all()
    return _CACHE["by_station_id"].get(ffwc_id)


def get_all_districts_covered():
    _load_all()
    return sorted(_CACHE["by_district"].keys())


def reload():
    """cache পরিষ্কার করে — নতুন প্রোফাইল ফাইল যোগ করার পর টেস্ট করতে কাজে লাগবে।"""
    _CACHE["loaded"] = False
    _CACHE["by_district"] = {}
    _CACHE["by_station_id"] = {}
    _load_all()