"""
FloodAI — ffwc_scraper.py

old.ffwc.gov.bd (BWDB Flood Forecasting & Warning Centre)-এর হোমপেজ থেকে
প্রতিটা station-এর real-time water level (mMSL) এবং danger_level বের করে।

⚠️ গুরুত্বপূর্ণ সীমাবদ্ধতা (ব্যবহারের আগে পড়ে নাও):
- এটা official API না — scraping। robots.txt এই সাইটকে ব্লক করে না,
  কিন্তু কোনো official permission/SLA নেই। সাইটের HTML structure
  বদলে গেলে এই scraper ভেঙে যেতে পারে — production-এ পুরোপুরি
  নির্ভর করার আগে BWDB-কে (api.support@bwdb.gov.bd) সরাসরি
  যোগাযোগ করে official access নেওয়া ভালো।
- সাইটটা নিজেই বলছে "Beta version! Information may vary with actual" —
  তাই এই ডেটাকে চূড়ান্ত সত্য হিসেবে না ধরে, একটা ভালো reference
  হিসেবে ব্যবহার করা উচিত।
- ভদ্রভাবে ব্যবহার করা জরুরি — বারবার/দ্রুত repeated request না করে
  (scheduler.py-তে ৩০ মিনিট/১ ঘণ্টা পরপর কল করাই যথেষ্ট, প্রতি
  page-load-এ না)।
- HTML structure অনুমান করে লেখা (bs4 দিয়ে flattened text থেকে regex
  parse) — যদি সাইট বদলে যায় এবং parse ভেঙে যায়, নিচের
  `parse_ffwc_stations()` ফাংশনের regex pattern-টা আবার চেক/আপডেট
  করতে হবে।

ব্যবহার:
    from ffwc_scrapper import fetch_ffwc_live_data
    data = fetch_ffwc_live_data()
    # data = {"SW42": {"name": "Dhaka", "river": "Buriganga", "water_level": 3.00,
    #                    "danger_level": 5.55, "district": "Dhaka", ...}, ...}
"""

import re
import time
import requests
from bs4 import BeautifulSoup

FFWC_URL = "http://old.ffwc.gov.bd/"

# সরকারি সাইট, ভদ্র হেডার দেওয়া ভালো — default python-requests UA
# অনেক সময় সরকারি সাইট ব্লক করে দেয়
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0 Safari/537.36 FloodAI-research-project"
}

# প্রতিটা station block-এর জন্য pattern। flattened text-এ এরকম আসে:
# Station Name: Dhaka
# Station ID: SW42
# River Name: Buriganga
# Division: Dhaka
# District: Dhaka
# Upazilla: Keraniganj
# Union: Subhadya
# Water Level: 3.00 mMSL
# (Recorded At: 27-Jul-2026 15:00)
# Highest Water Level: 6.69 mMSL
# Danger Level: 5.55 mMSL
STATION_BLOCK_RE = re.compile(
    r"Station Name:\s*(?P<name>[^\n]+?)\s*"
    r"Station ID:\s*(?P<id>\S+)\s*"
    r"River Name:\s*(?P<river>[^\n]+?)\s*"
    r"Division:\s*(?P<division>[^\n]+?)\s*"
    r"District:\s*(?P<district>[^\n]+?)\s*"
    r"Upazilla:\s*(?P<upazila>[^\n]*?)\s*"
    r"Union:\s*(?P<union>[^\n]*?)\s*"
    r"Water Level:\s*(?P<water_level>[\d.]+)\s*mMSL\s*"
    r"\(Recorded At:\s*(?P<recorded_at>[^)]+)\)\s*"
    r"Highest Water Level:\s*(?P<highest>[\d.]*)\s*mMSL\s*"
    r"Danger Level:\s*(?P<danger_level>[\d.]+)\s*mMSL",
    re.MULTILINE
)


def fetch_ffwc_live_data(timeout=15):
    """
    old.ffwc.gov.bd থেকে সব station-এর real-time water level নিয়ে আসে।

    Returns: dict, key = station_id (যেমন "SW42"), value = {
        "name": str, "river": str, "district": str, "upazila": str,
        "water_level": float (mMSL), "danger_level": float (mMSL),
        "recorded_at": str
    }

    কোনো কারণে fetch/parse fail করলে খালি dict {} রিটার্ন করবে —
    caller-এর উচিত এই ক্ষেত্রে পুরনো/cached ডেটায় fallback করা,
    পুরো app crash না করানো।
    """
    try:
        res = requests.get(FFWC_URL, headers=HEADERS, timeout=timeout)
        res.raise_for_status()
    except Exception as e:
        print(f"[ffwc_scraper] সাইট থেকে ডেটা আনতে ব্যর্থ: {e}")
        return {}

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        # flatten করা হচ্ছে যাতে HTML tag-এর সঠিক গঠন না জানলেও
        # regex দিয়ে টেক্সট প্যাটার্ন ধরা যায়
        flat_text = soup.get_text(separator="\n")
    except Exception as e:
        print(f"[ffwc_scraper] HTML parse করতে ব্যর্থ: {e}")
        return {}

    result = {}
    for m in STATION_BLOCK_RE.finditer(flat_text):
        try:
            station_id = m.group("id").strip()
            result[station_id] = {
                "name": m.group("name").strip(),
                "river": m.group("river").strip(),
                "district": m.group("district").strip(),
                "upazila": m.group("upazila").strip(),
                "water_level": float(m.group("water_level")),
                "danger_level": float(m.group("danger_level")),
                "recorded_at": m.group("recorded_at").strip(),
            }
        except (ValueError, AttributeError):
            # কোনো একটা station block malformed হলে সেটা স্কিপ করে
            # বাকিগুলো processing চালিয়ে যাওয়া হচ্ছে
            continue

    if not result:
        print("[ffwc_scraper] ⚠️ কোনো station পার্স হয়নি — সাইটের HTML "
              "structure বদলে গেছে কিনা চেক করা দরকার (regex pattern আপডেট লাগতে পারে)")

    return result


if __name__ == "__main__":
    # সরাসরি এই ফাইল রান করলে (python ffwc_scraper.py) টেস্ট হিসেবে
    # কতগুলো station পার্স হলো আর প্রথম কয়েকটা দেখাবে
    data = fetch_ffwc_live_data()
    print(f"মোট {len(data)} টা station পার্স হয়েছে\n")
    for i, (sid, info) in enumerate(data.items()):
        if i >= 5:
            print("...")
            break
        print(sid, "->", info)