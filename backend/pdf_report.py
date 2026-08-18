# ============================================================
# FloodAI — pdf_report.py
# PDF Report Generation Logic (Platypus Version)
# ============================================================

import io
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("⚠️ 'reportlab' library is missing! Run: pip install reportlab")
    REPORTLAB_AVAILABLE = False

# ============================================================
# Bengali Font Registration
# ============================================================
# ⚠️ গুরুত্বপূর্ণ: reportlab এর ডিফল্ট font (Helvetica) এ বাংলা অক্ষর নেই।
# সেটা ব্যবহার করলে বাংলা টেক্সটের জায়গা PDF এ ফাঁকা/ভাঙা দেখায় — কোনো
# error ছাড়াই, তাই bug টা ধরা কঠিন। তাই এখানে একটা Unicode বাংলা font
# (Noto Sans Bengali) explicitly register করা হচ্ছে।
#
# এই .ttf ফাইলটা তোমার project folder এ (app.py এর পাশে) রাখতে হবে।
# ডাউনলোড লিংক: https://fonts.google.com/noto/specimen/Noto+Sans+Bengali
# (Google Fonts পেজ থেকে "Download family" করে Regular ওজনের .ttf বের করে নাও)
BENGALI_FONT_NAME = "NotoBengali"
BENGALI_FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NotoSansBengali-Regular.ttf")

_bengali_font_registered = False
if REPORTLAB_AVAILABLE:
    try:
        if os.path.exists(BENGALI_FONT_PATH):
            pdfmetrics.registerFont(TTFont(BENGALI_FONT_NAME, BENGALI_FONT_PATH))
            _bengali_font_registered = True
        else:
            print(f"⚠️ Bengali font পাওয়া যায়নি: {BENGALI_FONT_PATH} — PDF এ বাংলা টেক্সট ফাঁকা দেখাবে!")
    except Exception as e:
        print(f"⚠️ Bengali font register করতে সমস্যা হয়েছে: {e}")


def _font_name():
    """যদি বাংলা font successfully register হয় তবে সেটা, নাহলে fallback Helvetica।"""
    return BENGALI_FONT_NAME if _bengali_font_registered else "Helvetica"


# ============================================================
# Bengali pre-base matra reordering (২০২৬-০৮ যোগ করা হলো)
# ============================================================
# সমস্যা: reportlab কোনো text-shaping (HarfBuzz-এর মতো) করে না — শুধু
# Unicode কোডপয়েন্ট অর্ডারে glyph বসায়। বাংলার pre-base matra (ি, ে, ৈ)
# Unicode-এ consonant-এর *পরে* লেখা হয় (উচ্চারণ-ক্রম অনুযায়ী — "নি" মানে
# ন তারপর ি) কিন্তু visually consonant-এর *আগে* বসে ("নি" দেখতে ি-হুক
# তারপর ন)। শেপিং ছাড়া রেন্ডার করলে তাই "নিরাপদ" হয়ে যায় "নরিাপদ"।
#
# এই ফাংশন pre-base matra-গুলোকে তাদের conjunct cluster-এর (virama দিয়ে
# জোড়া একাধিক ব্যঞ্জনবর্ণ থাকলে পুরো cluster-এর) শুরুতে সরিয়ে আনে, যাতে
# glyph-order-only রেন্ডারার-ও সঠিক visual ক্রম দেখায়। এটা পূর্ণাঙ্গ
# Unicode শেপিং না (জটিল যুক্তাক্ষর/ligature তবু আলাদা আলাদা glyph হিসেবে
# দেখাবে, একসাথে জোড়া লেগে সুন্দর ligature হবে না) — কিন্তু সাধারণ
# শব্দের matra-ক্রম ঠিক করার জন্য যথেষ্ট। সংখ্যা/ইংরেজি টেক্সটে এটা
# কোনো প্রভাব ফেলে না, তাই যেকোনো স্ট্রিং-এ নিরাপদে apply করা যায়।
import unicodedata

_BN_VIRAMA = '\u09CD'
_BN_PREBASE_VOWELS = {'\u09BF', '\u09C7', '\u09C8'}  # ি (I), ে (E), ৈ (AI)


def bn(text):
    """PDF-এ বসানোর আগে যেকোনো টেক্সট (বাংলা/ইংরেজি/সংখ্যা মেশানো) এই
    দিয়ে পাস করাও — pre-base matra সঠিক visual ক্রমে সরিয়ে দেবে,
    বাকি সব অক্ষর অপরিবর্তিত থাকবে।"""
    text = str(text)
    normalized = unicodedata.normalize('NFD', text)  # ো/ৌ কে ে+া / ে+ৗ তে ভাঙে
    result = []
    for ch in normalized:
        if ch in _BN_PREBASE_VOWELS and result:
            p = len(result) - 1
            while p - 1 >= 0 and result[p - 1] == _BN_VIRAMA:
                p -= 2
            if p < 0:
                p = 0
            result.insert(p, ch)
        else:
            result.append(ch)
    return unicodedata.normalize('NFC', ''.join(result))


def generate_flood_report(data):
    """
    FloodAI এর ডেটা নিয়ে Platypus ব্যবহার করে একটি সুন্দর PDF রিপোর্ট তৈরি করবে।
    বাংলা টেক্সট সঠিকভাবে দেখানোর জন্য Noto Sans Bengali font ব্যবহার করা হয়।
    """
    buffer = io.BytesIO()
    font = _font_name()

    # Document Setup (A4 Size)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()

    # ── বাংলা-সাপোর্টেড স্টাইল তৈরি করা (ডিফল্ট styles.Normal Helvetica ব্যবহার করে, যেটাতে বাংলা নেই) ──
    normal_bn = ParagraphStyle(name="NormalBengali", parent=styles["Normal"], fontName=font, fontSize=10, leading=14)
    heading_bn = ParagraphStyle(name="HeadingBengali", parent=styles["Heading2"], fontName=font, fontSize=13)

    elements = []

    # --- 1. Title Section ---
    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=12
    )
    elements.append(Paragraph("<b>FloodAI - Early Warning Report</b>", title_style))
    
    # --- 2. Date & Time ---
    # ⚠️ এই লাইনটা ইচ্ছাকৃতভাবে ইংরেজিতে এবং styles['Normal'] (default Helvetica)
    # ব্যবহার করছে — এই ফাইলের বাকি সব জায়গায় বাংলা লেখা হচ্ছে কারণ
    # NotoSansBengali-Regular.ttf একটা subset ফন্ট যেখানে কোনো ইংরেজি
    # অক্ষর (A-Z, a-z) নেই। NotoBengali font দিয়ে ইংরেজি লিখলে সেটা কোনো
    # error ছাড়াই চুপচাপ ফাঁকা দেখায় (নিচের সবকিছু তাই বাংলায় লেখা হলো)।
    date_str = datetime.now().strftime("%d %B %Y, %H:%M")
    elements.append(Paragraph(f'<font size=10 color="gray">Report Generated: {date_str}</font>', styles['Normal']))
    elements.append(Spacer(1, 20))

    # --- 3. Location & River Details ---
    elements.append(Paragraph(bn("১. অবস্থান ও নদীর তথ্য"), heading_bn))

    table_data_1 = [
        [bn("জেলা:"), bn(data.get('district', 'N/A')), bn("বিপদসীমা:"), bn(f"{data.get('danger_level', 'N/A')} মি")],
        [bn("স্কোরিং নদী:"), bn(data.get('river', 'N/A')), bn("আজকের ডিসচার্জ:"), bn(f"{data.get('discharge_today', 'N/A')} ঘন মি/সে")],
    ]
    t1 = Table(table_data_1, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), font),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 12))

    # ── একাধিক নদী থাকলে (rivers_status) সবগুলোর একটা ছোট breakdown টেবিল ──
    # "Scoring River" (worst-case, উপরে যেটা দিয়ে ML prediction চালানো হয়েছে)
    # আলাদা করে চিহ্নিত। বাকি নদীগুলোর জন্য কোনো ML prediction চালানো হয়নি,
    # তাই শুধু discharge/danger_level অনুপাত (%) দেখানো হচ্ছে — এটাকে যেন
    # ভুলবশত মডেলের প্রেডিকশন মনে না হয়।
    rivers_status = data.get('rivers_status') or []
    if len(rivers_status) > 1:
        elements.append(Paragraph(bn("এই জেলায় নজরদারিতে থাকা নদীসমূহ"), ParagraphStyle(
            name="SubHeadingBengali", parent=styles["Heading3"], fontName=font, fontSize=11)))
        elements.append(Spacer(1, 4))

        river_rows = [[bn("নদী"), bn("ডিসচার্জ (ঘন মি/সে)"), bn("বিপদসীমা (মি)"), bn("অবস্থা")]]
        for r in rivers_status:
            is_scoring = r.get('name') == data.get('scoring_river')
            if is_scoring:
                status = bn(f"{data.get('prediction', {}).get('level', '-')} (স্কোরিং নদী)")
            else:
                dl = r.get('danger_level') or 0
                ratio_pct = round((r.get('discharge_today', 0) / dl) * 100) if dl else 0
                status = bn(f"বিপদসীমার ~{ratio_pct}%")
            river_rows.append([bn(r.get('name', '-')), str(r.get('discharge_today', '-')), str(r.get('danger_level', '-')), status])

        t_rivers = Table(river_rows, colWidths=[1.3*inch, 1.5*inch, 1.5*inch, 2.1*inch])
        t_rivers.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eef7')),
            ('FONTNAME', (0,0), (-1,-1), font),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t_rivers)
        elements.append(Paragraph(
            f"<font size=8 color='gray' name='{font}'>" + bn(
                "দ্রষ্টব্য: শুধু স্কোরিং নদীর অবস্থা ML মডেল থেকে এসেছে। বাকি "
                "নদীগুলোর জন্য আলাদা ML প্রেডিকশন চালানো হয়নি, শুধু discharge/danger_level অনুপাত দেখানো হচ্ছে।"
            ) + "</font>",
            ParagraphStyle(name="NoteBengali", parent=styles["Normal"], fontName=font)))

    elements.append(Spacer(1, 15))

    # --- 4. Weather & Upstream Conditions ---
    elements.append(Paragraph(bn("২. আবহাওয়া ও উজানের অবস্থা"), heading_bn))
    
    weather = data.get('weather', {})
    upstream = data.get('upstream_weather', {})
    
    table_data_2 = [
        [bn("স্থানীয় বৃষ্টি:"), bn(f"{weather.get('rain', 0)} মিমি"), bn("উজানের বৃষ্টি:"), bn(f"{upstream.get('rain', 0)} মিমি")],
        [bn("মাটির আর্দ্রতা:"), bn(f"{data.get('soil_moisture', 'N/A')}"), bn("ল্যাগ টাইম:"), bn(f"{data.get('lag_time', 'N/A')} ঘণ্টা")]
    ]
    t2 = Table(table_data_2, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), font),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 15))

    # --- 5. Risk Assessment (ML Prediction) ---
    elements.append(Paragraph(bn("৩. ঝুঁকি মূল্যায়ন (ML প্রেডিকশন)"), heading_bn))

    pred = data.get('prediction', {})
    level = pred.get('level', 'নিরাপদ')

    # ডাইনামিক কালার লজিক
    if level == "বিপদ":
        level_color = "red"
    elif level in ["সতর্ক", "সাবধান"]:
        level_color = "orange"
    else:
        level_color = "green"

    elements.append(Paragraph(f"<b>{bn('সতর্কতা স্তর:')}</b> <font name='{font}' color='{level_color}'><b>{bn(level)}</b></font>", normal_bn))
    elements.append(Spacer(1, 5))
    
    prob = pred.get('probability', 0)
    elements.append(Paragraph(f"<b>{bn('বন্যার সম্ভাবনা:')}</b> {prob}%", normal_bn))
    elements.append(Spacer(1, 10))

    # Emoji (🚨, ⚠️) ও Noto Sans Bengali তে নেই — সরিয়ে শুধু টেক্সট রাখা হচ্ছে,
    # নাহলে emoji এর জায়গাটাও ফাঁকা/box দেখাবে।
    msg = pred.get('message', 'কোনো নির্দিষ্ট বার্তা নেই।')
    msg_clean = "".join(ch for ch in msg if ord(ch) < 0x1F000 or ch in ("\n",))
    elements.append(Paragraph(f"<i>{bn('অবস্থার বার্তা:')} {bn(msg_clean)}</i>", normal_bn))
    
    # --- Footer ---
    # (এখানেও ইচ্ছাকৃতভাবে English + default font — উপরের ৯২ নং লাইনের কমেন্ট দ্রষ্টব্য)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<font size=9 color='gray'>This is an AI-generated report by FloodAI System. Use for advisory purposes.</font>", styles['Normal']))

    # PDF বিল্ড করা
    doc.build(elements)
    
    # বাফার শুরুতে সেট করা
    buffer.seek(0)
    return buffer