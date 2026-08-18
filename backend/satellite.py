# ============================================================
# FloodAI — satellite.py
# NDWI Estimator & Water-Trend Analysis
# ============================================================
#
# ⚠️ নোট: প্রকৃত Sentinel-2/MODIS ইমেজারি (Google Earth Engine) এখনো
# integrate করা হয়নি। এই ফাইলটি এখন যা করে তা হলো — discharge ও
# soil moisture এর real API ডেটা থেকে NDWI/AMC অনুমান করা।
# আগে এখানে যে "precipitation_forecast" থাকতো, সেটি সম্পূর্ণ random
# সংখ্যা দিয়ে বানানো ছিল বলে বাদ দেওয়া হয়েছে — real rain forecast
# এর জন্য app.py এর /api/upstream/forecast/<district> route ব্যবহার করো।
# ============================================================


def get_full_satellite_data(discharge, danger_level, soil_moisture, river_forecast=None):
    """
    lat, lon future GEE integration এর জন্য রাখা হয়নি কারণ বর্তমানে
    ব্যবহার হয় না — real satellite imagery যুক্ত হলে এখানে যোগ করা যাবে।

    discharge: আজকের real river discharge (m3/s), app.py এর fetch_river() থেকে
    danger_level: জেলার danger level (DISTRICTS dict থেকে)
    soil_moisture: real soil moisture (0-1), app.py এর fetch_soil_moisture() থেকে
    river_forecast: real ৭ দিনের discharge forecast list (ঐচ্ছিক), fetch_river()["forecast"] থেকে
    """
    # ── NDWI (Normalized Difference Water Index) Estimation ──
    # > 0 মানে পানি/প্লাবিত এলাকা, < 0 মানে স্থলভাগ
    # discharge ও danger_level এর অনুপাত থেকে আনুমানিক করা হচ্ছে,
    # যেহেতু real satellite imagery ছাড়া প্রকৃত NDWI বের করা সম্ভব না।
    base_ndwi = -0.2

    if danger_level > 0:
        ratio = discharge / (danger_level * 100)
        ndwi_val = base_ndwi + (ratio * 0.8)
    else:
        ndwi_val = base_ndwi

    ndwi_val = round(min(max(ndwi_val, -1.0), 1.0), 2)

    status = "স্বাভাবিক শুষ্ক ভূমি"
    color = "#27ae60"

    if ndwi_val > 0.3:
        status = "মারাত্মক প্লাবিত (Severe Flood)"
        color = "#c0392b"
    elif ndwi_val > 0.0:
        status = "আংশিক প্লাবিত (Waterlogging)"
        color = "#e67e22"

    # ── Soil Moisture AMC Level (real data ব্যবহার করা হচ্ছে) ──
    soil = round(float(soil_moisture or 0), 3)
    if soil > 0.8:
        amc = "III"
        amc_label = "(সম্পূর্ণ ভেজা, রানঅফ বেশি)"
    elif soil > 0.5:
        amc = "II"
        amc_label = "(স্বাভাবিক)"
    else:
        amc = "I"
        amc_label = "(শুষ্ক, রানঅফ কম)"

    # ── River Discharge Trend (real ৭-দিনের forecast থেকে, random নয়) ──
    discharge_trend = []
    if river_forecast:
        for i, val in enumerate(river_forecast[:7]):
            try:
                val = float(val or 0)
            except (TypeError, ValueError):
                val = 0
            # ⚠️ আগে এখানে সরাসরি val > danger_level তুলনা হতো, যেটা discharge
            # (m3/s) কে danger_level (মিটার) এর সাথে সরাসরি তুলনা করত — দুইটা
            # ভিন্ন একক, ফলে risk প্রায় সবসময় "উচ্চ" দেখাতো। উপরে NDWI হিসাবে
            # যেভাবে danger_level * 100 কে reference discharge ধরা হয়েছে,
            # এখানেও সেই একই reference ব্যবহার করা হচ্ছে যাতে সামঞ্জস্যপূর্ণ থাকে।
            reference = danger_level * 100
            if reference > 0 and val > reference:
                risk = "উচ্চ"
            elif reference > 0 and val > reference * 0.7:
                risk = "মাঝারি"
            else:
                risk = "কম"
            discharge_trend.append({
                "day_index": i,
                "discharge_m3s": round(val),
                "risk": risk
            })

    return {
        "ndwi": {
            "ndwi": ndwi_val,
            "status": status,
            "color": color
        },
        "soil_moisture": {
            "average": soil,
            "amc": amc,
            "amc_label": amc_label,
            "status": "Saturated" if soil > 0.7 else "Normal"
        },
        "discharge_trend": discharge_trend,
        "data_source_note": "NDWI ও AMC আনুমানিক (real discharge/soil moisture ভিত্তিক); সরাসরি satellite imagery নয়।"
    }