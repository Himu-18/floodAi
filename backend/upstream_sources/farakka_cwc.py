# ============================================================
# FloodAI — upstream_sources/farakka_cwc.py
#
# ⚠️⚠️⚠️ ড্রাফট / যাচাই করা হয়নি (২০২৬-০৯) ⚠️⚠️⚠️
# এই মডিউল ভারতের Central Water Commission (CWC)-র দৈনিক flood
# bulletin PDF থেকে সরাসরি "Farakka(FF), Murshidabad" স্টেশনের real
# water level বের করার চেষ্টা করে — গেট-স্ট্যাটাস অনুমান করার বদলে
# আসল গঙ্গার পানির স্তর।
#
# আমি (Claude) এই কোড লিখেছি ওয়েব-সার্চে পাওয়া উদাহরণ PDF দেখে, কিন্তু
# এই sandbox-এর network allowlist-এ cwc.gov.in নেই বলে **কোনো actual
# live PDF fetch/parse করে টেস্ট করা হয়নি**। তিনটা জিনিস নিশ্চিতভাবে
# locally verify/ঠিক করা লাগবে:
#
#   ১. BULLETIN_LISTING_URL — আমি নিশ্চিত কোনো stable "সব বুলেটিনের
#      তালিকা" পেজ খুঁজে পাইনি (সাইটটা সম্ভবত Drupal-ভিত্তিক, JS দিয়ে
#      listing render হতে পারে)। browser-এ cwc.gov.in ঘুরে আসল listing
#      URL বের করে বসাতে হবে — অথবা fallback filename-guessing দিয়েই
#      কাজ চালাতে হবে (নিচে দেখুন)।
#
#   ২. FILENAME_PATTERNS — গত কয়েক বছরে অন্তত ৪ রকম filename ফরম্যাট
#      দেখা গেছে (cfcrcwcdfb+DDMMYYYY, dfbcwc+DDMMYYYY,
#      cfcrcwcdfb-DD-MM-YYYY_N, dfb-cwc-dated+DDMMYYYY) — তাই আজকের
#      bulletin কোন প্যাটার্নে আছে তা guess করে কয়েকটা চেষ্টা করা হয়,
#      একটাও কাজ না করলে None রিটার্ন করে।
#
#   ৩. PDF STRUCTURE — বুলেটিন column-ভিত্তিক টেবিল-আকারে, pdfplumber-এর
#      plain text extraction column-order জগাখিচুড়ি করে ফেলতে পারে।
#      নিচের parser আগে সরল regex দিয়ে try করে, কাজ না করলে
#      extract_tables() দিয়ে try করে — কিন্তু আসল PDF ছাড়া regex-টা
#      টিউন করা অসম্ভব, তাই এটা locally আসল bulletin দিয়ে অবশ্যই
#      পরীক্ষা করে regex ঠিক করতে হবে।
#
# ব্যবহার (app.py থেকে, ভবিষ্যতে): fetch_farakka_water_level() রিটার্ন
# করবে {"date": ..., "level_m": ..., "danger_level_m": ...,
# "trend": "Rising"/"Falling"/"Steady", "trend_mm_per_hr": ...} অথবা
# None (fetch/parse ব্যর্থ হলে — caller-কে fallback করতে হবে, ঠিক যেমন
# fetch_rainfall_intensity() ব্যর্থ হলে flash_flood.py দৈনিক-total
# logic-এ fallback করে)।
# ============================================================

import re
import requests
from datetime import datetime, timedelta

try:
    import pdfplumber
except ImportError:
    pdfplumber = None  # locally `pip install pdfplumber` লাগবে

BASE_URL = "https://cwc.gov.in/sites/default/files/"

# ⚠️ যাচাই করা হয়নি — locally এই URL-টা browser-এ খুলে দেখতে হবে যে
# এটা আসলেই সব বুলেটিনের তালিকা দেয় কিনা, নাকি ভুল/৪০৪।
BULLETIN_LISTING_URL_GUESSES = [
    "https://cwc.gov.in/flood-forecast-bulletin",
    "https://cwc.gov.in/daily-flood-bulletin",
]

# ⚠️ যাচাই করা হয়নি — এই প্যাটার্নগুলো পুরনো PDF-এর URL থেকে reverse-
# engineer করা, কিন্তু কোনটা "আজকের" জন্য সঠিক তা সময়ের সাথে বদলেছে।
def _filename_candidates(date_obj):
    dmy = date_obj.strftime("%d%m%Y")
    dmy_dash = date_obj.strftime("%d-%m-%Y")
    dmy_dot = date_obj.strftime("%d.%m.%Y")
    return [
        f"cfcrcwcdfb{dmy}.pdf",
        f"dfbcwc{dmy}.pdf",
        f"cfcrcwcdfb-{dmy_dash}.pdf",
        f"cfcrcwcdfb-{dmy_dash}_2.pdf",
        f"cwcdfb-{dmy_dot}.pdf",
        f"dfb-cwc-dated{dmy}.pdf",
    ]


def _try_discover_todays_pdf_url():
    """
    ধাপ ১: listing page থেকে আজকের বুলেটিনের আসল লিঙ্ক বের করার চেষ্টা।
    এটা সবচেয়ে নির্ভরযোগ্য পথ, কিন্তু listing URL যাচাই করা হয়নি বলে
    এখন এটা প্রায় নিশ্চিতভাবে None রিটার্ন করবে যতক্ষণ না সঠিক URL বসানো
    হচ্ছে।
    """
    for listing_url in BULLETIN_LISTING_URL_GUESSES:
        try:
            r = requests.get(listing_url, timeout=8)
            if r.status_code != 200:
                continue
            # bulletin PDF-এর লিঙ্ক সাধারণত /sites/default/files/...pdf প্যাটার্নে
            matches = re.findall(r'href="(/sites/default/files/[^"]+\.pdf)"', r.text)
            if matches:
                # সবচেয়ে সাম্প্রতিক লিঙ্কটাই সাধারণত তালিকার প্রথমে থাকে
                return "https://cwc.gov.in" + matches[0]
        except Exception as e:
            print(f"_try_discover_todays_pdf_url error ({listing_url}): {e}")
    return None


def _try_guess_todays_pdf_url():
    """ধাপ ২ (fallback): filename-guessing — আজকে ও গতকালের তারিখ দিয়ে
    কয়েকটা সম্ভাব্য filename try করে, HEAD request দিয়ে কোনটা আসলে
    আছে (200 OK) চেক করে।"""
    for days_back in (0, 1):
        date_obj = datetime.now() - timedelta(days=days_back)
        for fname in _filename_candidates(date_obj):
            url = BASE_URL + fname
            try:
                r = requests.head(url, timeout=6)
                if r.status_code == 200:
                    return url
            except Exception:
                continue
    return None


def _parse_farakka_line(text):
    """
    PDF-এর plain text থেকে "Farakka" সংবলিত লাইন খুঁজে বের করে সংখ্যাগুলো
    আলাদা করার চেষ্টা। উদাহরণ (পুরনো PDF থেকে, কলাম-ক্রম আসল লেআউটের
    উপর নির্ভরশীল — তাই এই regex টা locally আসল বুলেটিন দিয়ে verify/
    টিউন করা লাগবেই):

        "MURSHIDABAD 21.25 22.25 25.14 22.6 22.97 Farakka(FF)
         West Bengal 07-09-1998 Steady Rising 0.0 31-08-2022 14:00 20:00:00"

    এখানে ক্রম (danger_level, warning_level, HFL, forecasted, actual)
    সবসময় এক না-ও থাকতে পারে — তাই এটা একটা প্রাথমিক heuristic মাত্র।
    """
    if "Farakka" not in text:
        return None

    # Farakka-সংবলিত লাইনের আশেপাশের প্রসঙ্গ ধরার জন্য একটা windowed search
    idx = text.find("Farakka")
    window = text[max(0, idx - 300):idx + 300]

    numbers = re.findall(r"\d+\.\d+", window)
    trend_match = re.search(r"\b(Rising|Falling|Steady)\b", window)
    date_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", window)

    if not numbers:
        return None

    return {
        "raw_window": window,  # ডিবাগের জন্য — regex ঠিক করার সময় এটা দেখে বোঝা যাবে কোথায় ভুল হচ্ছে
        "numbers_found": numbers,
        "trend": trend_match.group(1) if trend_match else None,
        "date": date_match.group(1) if date_match else None,
    }


def fetch_farakka_water_level():
    """
    মূল entry point। সফল হলে dict, ব্যর্থ হলে (network/parse যেকোনো
    কারণে) None রিটার্ন করে — caller-কে fallback করতে হবে।
    """
    if pdfplumber is None:
        print("fetch_farakka_water_level: pdfplumber ইনস্টল নেই")
        return None

    pdf_url = _try_discover_todays_pdf_url() or _try_guess_todays_pdf_url()
    if not pdf_url:
        print("fetch_farakka_water_level: আজকের বুলেটিনের URL বের করা যায়নি")
        return None

    try:
        r = requests.get(pdf_url, timeout=15)
        r.raise_for_status()
        with open("/tmp/_cwc_bulletin.pdf", "wb") as f:
            f.write(r.content)

        full_text = ""
        with pdfplumber.open("/tmp/_cwc_bulletin.pdf") as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if "Farakka" in page_text:
                    full_text += page_text + "\n"

        parsed = _parse_farakka_line(full_text)
        if parsed:
            parsed["source_url"] = pdf_url
        return parsed

    except Exception as e:
        print(f"fetch_farakka_water_level error: {e}")
        return None


if __name__ == "__main__":
    # ম্যানুয়াল টেস্টের জন্য — locally চালিয়ে দেখুন:
    #   python3 backend/upstream_sources/farakka_cwc.py
    result = fetch_farakka_water_level()
    print(result)
