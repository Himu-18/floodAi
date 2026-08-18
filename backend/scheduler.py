# ============================================================
# FloodAI — scheduler.py
# ============================================================

import requests
import time
import os
import schedule
from datetime import datetime

BACKEND_URL = f"http://127.0.0.1:{os.getenv('PORT', '5000')}"

# High risk districts — এগুলো বেশি frequently update হবে
HIGH_RISK_DISTRICTS = [
    "কুড়িগ্রাম", "গাইবান্ধা", "সুনামগঞ্জ",
    "জামালপুর", "সিলেট", "নেত্রকোণা",
    "সিরাজগঞ্জ", "কিশোরগঞ্জ", "লালমনিরহাট",
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# সব ৬৪ জেলা — আগে এখানে app.py এর DISTRICTS dict এর সাথে হুবহু মিলিয়ে
# manually একটা duplicate list রাখা হতো, যেটা app.py বদলালে ম্যানুয়ালি
# sync করতে হতো (real bug risk)। এখন data/districts_base.py-ই একমাত্র
# source of truth — সরাসরি সেখান থেকে জেলার তালিকা নেওয়া হচ্ছে, তাই
# app.py-তে জেলা যোগ/বাদ দিলে এখানে আর কিছু করতে হবে না।
from data.districts_base import DISTRICTS_BASE
ALL_DISTRICTS = list(DISTRICTS_BASE.keys())


def get_all_districts():
    """
    আগে এটা backend এর /api/districts endpoint থেকে dynamically জেলার
    তালিকা আনত। কিন্তু scheduler.py চালানোর জন্য app.py আলাদাভাবে
    চালু রাখতেই হয়, তাই dynamic HTTP fetch করে extra জটিলতা বাড়ানোর
    দরকার নেই — data/districts_base.py থেকে সরাসরি তালিকা আনা হচ্ছে।

    এখন app.py আর scheduler.py দুটোই একই data/districts_base.py file
    থেকে জেলার তালিকা নেয়, তাই নতুন জেলা যোগ/বাদ দিলে শুধু ওই একটা
    ফাইলেই পরিবর্তন করলেই দুই জায়গায় automatically sync থাকবে।
    """
    return ALL_DISTRICTS


def collect_district(district):
    try:
        r = requests.get(
            f"{BACKEND_URL}/api/flood/{district}",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            level = data.get("prediction", {}).get("level", "")
            prob = data.get("prediction", {}).get("probability", 0)
            log(f"✅ {district} — {level} ({prob}%)")

            # High risk হলে alert
            if prob >= 70:
                log(f"🚨 HIGH RISK: {district} — {prob}%")

        else:
            log(f"❌ {district} — Error {r.status_code}")

    except Exception as e:
        log(f"❌ {district} — {str(e)}")

    time.sleep(0.5)  # Rate limit

def collect_high_risk():
    """প্রতি ১৫ মিনিটে high risk districts update"""
    log("⏰ High risk districts updating...")
    for district in HIGH_RISK_DISTRICTS:
        collect_district(district)
    log("✅ High risk update done!")

def collect_all():
    """প্রতি ১ ঘণ্টায় সব districts update (হার্ডকোডেড তালিকা)"""
    log("⏰ All districts updating...")
    all_districts = get_all_districts()
    log(f"📋 মোট {len(all_districts)}টি জেলা আপডেট হবে")
    for district in all_districts:
        collect_district(district)
    log("✅ All districts update done!")

def morning_report():
    """সকাল ৬টায় full update"""
    log("🌅 Morning report starting...")
    collect_all()
    log("🌅 Morning report done!")

def evening_report():
    """সন্ধ্যা ৬টায় full update"""
    log("🌆 Evening report starting...")
    collect_all()
    log("🌆 Evening report done!")

def collect_validation():
    """
    দিনে একবার — FFWC station থাকা প্রতিটা জেলার আজকের FloodAI
    prediction আর FFWC live data একসাথে validation_log-এ জমা করে।
    সন্ধ্যার দিকে (evening_report-এর কাছাকাছি) চালানো ভালো, কারণ
    FFWC-র recorded_at সাধারণত দিনের মাঝামাঝি/বিকেলের রিডিং হয়।
    """
    log("📊 Validation log collecting...")
    try:
        r = requests.post(f"{BACKEND_URL}/api/validation/collect", timeout=120)
        if r.status_code == 200:
            data = r.json()
            log(f"✅ Validation log — {data.get('saved')} জেলা saved, {data.get('skipped')} skip")
        else:
            log(f"❌ Validation log — Error {r.status_code}")
    except Exception as e:
        log(f"❌ Validation log — {str(e)}")

def run_scheduler_loop():
    """
    সব cron job register করে অনন্তকাল ধরে চালায়। এটা এখন একটা ফাংশনে
    রাখা হয়েছে যাতে app.py চাইলে এটাকে background thread হিসেবে
    সরাসরি চালাতে পারে (production/Render-এ আলাদা scheduler process
    চালানোর দরকার নেই) — অথবা এই ফাইল সরাসরি `python scheduler.py`
    দিয়ে লোকালেও চালানো যায় (নিচের __main__ ব্লক দেখুন)।
    """
    schedule.every(15).minutes.do(collect_high_risk)
    schedule.every(1).hours.do(collect_all)
    schedule.every().day.at("06:00").do(morning_report)
    schedule.every().day.at("18:00").do(evening_report)
    schedule.every().day.at("17:30").do(collect_validation)

    log("🚀 FloodAI Scheduler started!")
    log("📋 Schedule:")
    log("   → প্রতি ১৫ মিনিট: High risk districts")
    log("   → প্রতি ১ ঘণ্টা: সব districts (হার্ডকোডেড ৬৪ জেলা)")
    log("   → সকাল ৬টা: Morning report")
    log("   → সন্ধ্যা ৬টা: Evening report")
    log("   → বিকাল ৫:৩০: Validation log (FloodAI vs FFWC)")

    # First run
    collect_high_risk()

    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        log("🛑 Scheduler বন্ধ করা হলো (Ctrl+C)")

if __name__ == "__main__":
    run_scheduler_loop()