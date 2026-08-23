# ============================================================
# FloodAI — Bangladesh Flood Warning System
# Backend: app.py (100% Complete Version with ALL APIs)
# ============================================================

import os
import time
from pathlib import Path
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import requests
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# .env ফাইল থেকে environment variable লোড করা (WEATHER_API_KEY, GROQ_API_KEY) —
# এটা os.getenv() কল করার আগে চালাতে হবে, নাহলে key None আসবে।
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# index.html, script.js, style.css, assets/ — এগুলো backend/ ফোল্ডারের বাইরে,
# project root-এ থাকে (VS Code explorer-এ backend/-এর ঠিক উপরে)। ngrok দিয়ে
# একটামাত্র link সবাইকে দিতে হলে Flask-কেই এই ফাইলগুলো serve করতে হবে,
# নাহলে "/" এ শুধু API JSON status দেখাবে, ওয়েবসাইট না।
PROJECT_ROOT = BASE_DIR.parent

# Local imports
from model import predict_flood, get_reference_discharge
from flood_types.riverine import CONFLUENCE_DISTRICTS, PADMA_REFERENCE_DISTRICT, JAMUNA_REFERENCE_DISTRICT
try:
    from satellite import get_full_satellite_data
except ImportError:
    pass
try:
    from ffwc_scrapper import fetch_ffwc_live_data
except ImportError:
    fetch_ffwc_live_data = None
try:
    from union_data import get_unions_by_district, get_high_risk_unions, get_union_stats
except ImportError:
    pass
try:
    from data.union_gazetteer import get_all_unions_for_district, get_upazilas_for_district
except ImportError:
    get_all_unions_for_district = None
    get_upazilas_for_district = None
from database import (
    init_db, save_reading, save_community_report,
    get_history, get_community_reports, register_user, get_user,
    get_latest_readings, DB_PATH
)
try:
    from pdf_report import generate_flood_report
except ImportError:
    pass

app = Flask(__name__)

def parse_csv_env(name, default):
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]

CORS_ORIGINS = parse_csv_env(
    "CORS_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500,"
    "http://127.0.0.1:8000,http://localhost:8000,null"
)
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

# ============================================================
# API KEYS
# ============================================================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_RATE_WINDOW_SECONDS = int(os.getenv("CHAT_RATE_WINDOW_SECONDS", "60"))
CHAT_RATE_MAX_REQUESTS = int(os.getenv("CHAT_RATE_MAX_REQUESTS", "20"))
_chat_hits = {}

if not WEATHER_API_KEY or not GROQ_API_KEY:
    print("⚠️ WARNING: WEATHER_API_KEY বা GROQ_API_KEY .env ফাইলে পাওয়া যায়নি! "
          "backend/.env ফাইল ঠিকমতো আছে কিনা চেক করুন।")

# ============================================================
# DISTRICT DATA
# ============================================================
from data.districts_base import DISTRICTS_BASE
from data.flood_config import FLOOD_CONFIG
from data.stations import FFWC_STATIONS
from data.upstream_cities import get_upstream_coords

DISTRICTS = {
    name: {**base, **FLOOD_CONFIG.get(name, {})}
    for name, base in DISTRICTS_BASE.items()
}

# ============================================================
# DATABASE INIT
# ============================================================
init_db()

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_json_body():
    return request.get_json(silent=True) or {}

def to_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def is_chat_rate_limited(client_id):
    if CHAT_RATE_MAX_REQUESTS <= 0:
        return False
    now = time.time()
    cutoff = now - CHAT_RATE_WINDOW_SECONDS
    hits = [t for t in _chat_hits.get(client_id, []) if t >= cutoff]
    if len(hits) >= CHAT_RATE_MAX_REQUESTS:
        _chat_hits[client_id] = hits
        return True
    hits.append(now)
    _chat_hits[client_id] = hits
    return False

def fetch_weather(lat, lon):
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric"},
            timeout=5
        )
        data = r.json()
        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rain": data.get("rain", {}).get("1h", 0),
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"],
            "ok": True,
        }
    except Exception as e:
        print(f"fetch_weather error: {e}")
        return {"temp": None, "humidity": None, "rain": 0, "wind": None, "desc": "", "ok": False}

def fetch_upstream(city):
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
            timeout=5
        )
        data = r.json()
        return {
            "city": city.split(",")[0],
            "rain": data.get("rain", {}).get("1h", 0),
            "humidity": data["main"]["humidity"],
            "temp": data["main"]["temp"],
            "ok": True,
        }
    except Exception as e:
        print(f"fetch_upstream error: {e}")
        return {"city": city.split(",")[0], "rain": 0, "humidity": None, "temp": None, "ok": False}

# ── FFWC live water-level cache ──
# fetch_ffwc_live_data() পুরো old.ffwc.gov.bd হোমপেজ scrape করে, তাই প্রতি
# request-এ কল করা অভদ্র (scraper-এর নিজের docstring-এ ৩০ মিনিট/১ ঘণ্টা
# পরপর কল করার কথা বলা আছে)। তাই এখানে একটা module-level TTL cache রাখা
# হচ্ছে — প্রথম request scrape করবে, তার পরের ৩০ মিনিট সবাই cache থেকে পাবে।
FFWC_LIVE_CACHE_TTL = int(os.getenv("FFWC_LIVE_CACHE_TTL_SECONDS", "1800"))
_ffwc_live_cache = {"data": {}, "fetched_at": 0}

def get_ffwc_live_cached():
    """
    Cache করা FFWC live station data রিটার্ন করে (station_id -> dict)।
    Cache stale বা খালি হলে নতুন করে scrape করে refresh করে।
    scrape ব্যর্থ হলে (fetch_ffwc_live_data None বা {} রিটার্ন করলে) পুরনো
    cache-ই ধরে রাখা হয় (থাকলে) — পুরোপুরি খালি করে দেওয়া হয় না, কারণ
    কিছুক্ষণ আগের real data, কিছুই না থাকার চেয়ে ভালো।
    """
    if fetch_ffwc_live_data is None:
        return {}

    now = time.time()
    is_stale = (now - _ffwc_live_cache["fetched_at"]) > FFWC_LIVE_CACHE_TTL
    if is_stale:
        try:
            fresh = fetch_ffwc_live_data()
        except Exception as e:
            print(f"[ffwc live cache] scrape ব্যর্থ: {e}")
            fresh = {}

        if fresh:
            _ffwc_live_cache["data"] = fresh
            _ffwc_live_cache["fetched_at"] = now
        elif _ffwc_live_cache["fetched_at"] == 0:
            # প্রথমবারই scrape ব্যর্থ হলে খালি dict-ই থাকবে, caller fallback করবে
            _ffwc_live_cache["fetched_at"] = now

    return _ffwc_live_cache["data"]


def fetch_river(lat, lon):
    try:
        r = requests.get(
            "https://flood-api.open-meteo.com/v1/flood",
            params={"latitude": lat, "longitude": lon, "daily": "river_discharge", "forecast_days": 7},
            timeout=5
        )
        data = r.json()
        return {
            "today": data["daily"]["river_discharge"][0],
            "forecast": data["daily"]["river_discharge"],
            "dates": data["daily"]["time"],
            "ok": True,
        }
    except Exception as e:
        print(f"fetch_river error: {e}")
        return {"today": 0, "forecast": [], "dates": [], "ok": False}

def fetch_soil_moisture(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "hourly": "soil_moisture_0_to_1cm",
                "forecast_days": 1,
            },
            timeout=5
        )
        data = r.json()
        values = data["hourly"]["soil_moisture_0_to_1cm"]
        return round(sum(values) / len(values), 3)
    except Exception as e:
        print(f"fetch_soil_moisture error: {e}")
        return 0.5

# ── Flash Flood-এর জন্য: গত ৬ ঘণ্টার rolling rainfall (মিমি)।
# OpenWeatherMap-এর "rain.1h" শুধু গত ১ ঘণ্টার snapshot দেয়, যেখানে
# গবেষণা বলছে flash flood-এর real trigger ৩-৬ ঘণ্টার তীব্রতা —
# তাই Open-Meteo-র hourly + past_hours প্যারামিটার দিয়ে (বিনামূল্যে,
# নতুন কোনো API key লাগে না) গত ৬ ঘণ্টার precipitation যোগ করে
# ফেরত দেওয়া হচ্ছে। ব্যর্থ হলে None (caller fallback করবে)।
def fetch_rainfall_intensity(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "hourly": "precipitation",
                "past_hours": 6,
                "forecast_days": 1,
            },
            timeout=5
        )
        data = r.json()
        values = data["hourly"]["precipitation"]
        # past_hours প্যারামিটার দিলে Open-Meteo array-র শুরুতে সেই past
        # hour-গুলো বসায়, তাই প্রথম ৬টা এন্ট্রিই "গত ৬ ঘণ্টা"
        past_6h = values[:6]
        return round(sum(past_6h), 1)
    except Exception as e:
        print(f"fetch_rainfall_intensity error: {e}")
        return None

def calculate_runoff(rainfall, cn):
    S = (25400 / cn) - 254
    Ia = 0.2 * S
    if rainfall <= Ia:
        return 0
    return round(((rainfall - Ia) ** 2) / (rainfall + 0.8 * S), 2)

def is_full_moon_today():
    known_new_moon = datetime(2024, 1, 11)
    now = datetime.now()
    days_since_new_moon = (now - known_new_moon).days
    moon_age = days_since_new_moon % 29.53
    return 13.5 <= moon_age <= 16.5

def get_color_by_level(level):
    if level == "বিপদ": return "#c0392b"
    if level == "সতর্ক": return "#e67e22"
    if level == "সাবধান": return "#f39c12"
    return "#27ae60"

def get_active_report_count(district_name):
    active_reports = 0
    try:
        reports = get_community_reports(district_name, limit=20)
        for r in reports:
            if r['status'] in ['road', 'house', 'rising', 'emergency']:
                active_reports += 1
    except Exception as e:
        print(f"get_active_report_count error: {e}")
    return active_reports

# ── Riverine confluence check (get_flood ও download_pdf দুই জায়গাতেই
# একই লজিক ব্যবহারের জন্য শেয়ার করা হলো) — শুধু পদ্মা-যমুনার সঙ্গমস্থলের
# কাছের ৫টা জেলার জন্য (flood_types/riverine.py-র CONFLUENCE_DISTRICTS)
# এক্সট্রা ২টা discharge fetch করে "দুই প্রধান নদী একসাথে peak" কিনা
# চেক করে; বাকি সব জেলার জন্য None রিটার্ন করে, কোনো এক্সট্রা call হয় না ──
def get_confluence_data(district_name):
    if district_name not in CONFLUENCE_DISTRICTS:
        return None
    try:
        padma_info = DISTRICTS[PADMA_REFERENCE_DISTRICT]
        jamuna_info = DISTRICTS[JAMUNA_REFERENCE_DISTRICT]

        padma_river = fetch_river(padma_info["river_lat"], padma_info["river_lon"])
        jamuna_river = fetch_river(jamuna_info["river_lat"], jamuna_info["river_lon"])

        # ⚠️ আগে এখানে district_name পাস করা হতো না, তাই এই দুই reference-ই
        # সবসময় crude danger_level*100 approximation ব্যবহার করত (রাজবাড়ীর
        # জন্য ৮২০, মানিকগঞ্জের জন্য ৮৯৫ m³/s) — বাস্তবে পদ্মা/যমুনার real
        # discharge ৩০,০০০-৫০,০০০ m³/s রেঞ্জে, তাই ratio প্রায় সবসময় >১ হয়ে
        # যেত আর confluence override বর্ষাকালে প্রায় সবসময় ট্রিগার হতো। এখন
        # district_name পাস করায় district_profiles/-এর verified সংখ্যা
        # ব্যবহার হবে (রাজবাড়ী→৩০,০০০, মানিকগঞ্জ→৫০,০০০)।
        padma_ref = get_reference_discharge(padma_info.get("danger_level"), PADMA_REFERENCE_DISTRICT)
        jamuna_ref = get_reference_discharge(jamuna_info.get("danger_level"), JAMUNA_REFERENCE_DISTRICT)

        if not padma_ref or not jamuna_ref:
            return None

        return {
            "padma_ratio": float(padma_river.get("today") or 0) / padma_ref,
            "jamuna_ratio": float(jamuna_river.get("today") or 0) / jamuna_ref,
        }
    except Exception as e:
        print(f"get_confluence_data error: {e}")
        return None

# ── Dam-Affected জেলার জন্য গত কয়েক দিনের upstream_rain history —
# database.py-র get_history() ইতিমধ্যেই প্রতিটা reading সেভ রাখে,
# তাই নতুন কোনো টেবিল/API লাগছে না। শুধু Dam-Affected জেলাতেই কল হবে।
# ⚠️ সীমাবদ্ধতা: এটা "গত N বার check করা হয়েছে" তার history, ঠিক
# "গত N ক্যালেন্ডার দিন" না — যদি কোনো জেলা অনিয়মিতভাবে/কম চেক করা হয়
# (scheduler.py নিয়মিত না চালালে), sustained_days-এর হিসাব সঠিক
# ক্যালেন্ডার-দিন প্রতিফলিত নাও করতে পারে।
def get_upstream_rain_history(district_name, info, limit=7):
    if info.get("flood_type") != "Dam-Affected":
        return None
    try:
        history = get_history(district_name, limit=limit)
        if not history:
            return None
        return [row.get("upstream_rain") for row in history]
    except Exception as e:
        print(f"get_upstream_rain_history error: {e}")
        return None

# ── Flash Flood জেলার জন্য ৬-ঘণ্টার rolling rainfall intensity (local +
# upstream) — শুধু flood_type == "Flash Flood" জেলাতেই কল হবে (১০টা
# জেলা), বাকি ৫৪ জেলায় কোনো এক্সট্রা call হয় না। কোনো কারণে upstream
# শহরের coordinate না পাওয়া গেলে বা fetch ব্যর্থ হলে None রিটার্ন করে,
# model.py-র flash_flood.py তখন পুরনো দৈনিক-total logic-এ fallback করবে ──
def get_rainfall_intensity_data(district_name, info, local_lat, local_lon):
    # ⚠️ আগে শুধু "Flash Flood"-এর জন্য প্রযোজ্য ছিল। কিন্তু urban drainage-ও
    # (Urban Waterlogging) দৈনিক total-এর চেয়ে short-duration intensity-র
    # প্রতি বেশি sensitive — একই যুক্তি এখানেও প্রযোজ্য, তাই যোগ করা হলো।
    if info.get("flood_type") not in ("Flash Flood", "Urban Waterlogging"):
        return None
    try:
        local_6h = fetch_rainfall_intensity(local_lat, local_lon)

        upstream_coords = get_upstream_coords(info.get("upstream"))
        upstream_6h = None
        if upstream_coords:
            upstream_6h = fetch_rainfall_intensity(upstream_coords[0], upstream_coords[1])

        if local_6h is None and upstream_6h is None:
            return None

        return {"local_6h": local_6h or 0, "upstream_6h": upstream_6h or 0}
    except Exception as e:
        print(f"get_rainfall_intensity_data error: {e}")
        return None

# ============================================================
# API ROUTES
# ============================================================

@app.route('/')
def home():
    return send_file(PROJECT_ROOT / "index.html")

@app.route('/script.js')
def serve_script():
    return send_file(PROJECT_ROOT / "script.js")

@app.route('/style.css')
def serve_style():
    return send_file(PROJECT_ROOT / "style.css")

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    # ⚠️ FIX (২০২৬-০৮): আগে filename সরাসরি PROJECT_ROOT/"assets"-এর সাথে জোড়া
    # লেগে send_file-এ যেত, কোনো sanitization ছাড়া — ../ দিয়ে path traversal
    # করে assets ফোল্ডারের বাইরের ফাইল (backend source code, DB) পড়ার ঝুঁকি
    # ছিল। send_from_directory নিজে থেকেই traversal প্রতিরোধ করে (safe_join
    # ব্যবহার করে, ফোল্ডারের বাইরে গেলে 404 দেয়)।
    return send_from_directory(str(PROJECT_ROOT / "assets"), filename)

@app.route('/api/status')
def api_status():
    return jsonify({
        "message": "🌊 FloodAI Backend চলছে!",
        "status": "ok",
        "version": "2.0 Complete",
        "districts": len(DISTRICTS)
    })

@app.route('/api/districts')
def get_districts():
    return jsonify(sorted(list(DISTRICTS.keys())))

@app.route('/api/districts/map')
def get_districts_map():
    try:
        latest_rows = get_latest_readings()
    except Exception as e:
        print(f"get_latest_readings error: {e}")
        latest_rows = []
    latest_by_district = {r["district"]: r for r in latest_rows}

    result = []
    for name, d in DISTRICTS.items():
        live = latest_by_district.get(name)
        # stale (৬ ঘণ্টার বেশি পুরনো) reading থাকলে সেটাকে "live" হিসেবে না
        # দেখিয়ে None ধরা হচ্ছে — নাহলে scheduler বন্ধ থাকা অবস্থায় দিনের পর
        # দিন পুরনো "বিপদ" reading ম্যাপে সক্রিয় সতর্কতা হিসেবে দেখাতে থাকতো।
        if live and live.get("is_stale"):
            live = None
        result.append({
            "name": name,
            "lat": d.get("lat"),
            "lon": d.get("lon"),
            "river_lat": d.get("river_lat"),
            "river_lon": d.get("river_lon"),
            "risk": d.get("risk"),
            "river": d.get("river"),
            "danger_level": d.get("danger_level"),
            "ffwc_station": d.get("ffwc_station"),
            "ffwc_verified": d.get("ffwc_verified"),
            "live_warning_level": live["warning_level"] if live else None,
            "live_risk_score": live["risk_score"] if live else None,
            "live_timestamp": live["timestamp"] if live else None
        })
    return jsonify(result)

@app.route('/api/stations/map')
def get_stations_map():
    return jsonify(FFWC_STATIONS)

@app.route('/api/stations/<station_id>/live')
def get_station_live(station_id):
    station = next((s for s in FFWC_STATIONS if s["id"] == station_id), None)
    if not station:
        return jsonify({"error": "Station পাওয়া যায়নি"}), 404

    # Open-Meteo discharge (m3/s) — সবসময় দেখানো হয়, কারণ এটা model-এর
    # নিজের input হিসেবে ব্যবহৃত হচ্ছে (danger_level-ভিত্তিক ratio না, raw discharge)
    try:
        river = fetch_river(station["lat"], station["lon"])
        discharge = float(river.get("today") or 0)
    except Exception as e:
        discharge = 0
        print(f"get_station_live discharge error: {e}")

    # আসল FFWC-scraped water level (mMSL) — এটাই প্রকৃত "live" observed data,
    # discharge modeled/estimated। station_id মিলিয়ে খুঁজে বের করা হচ্ছে।
    live = get_ffwc_live_cached().get(station_id)

    if live:
        return jsonify({
            "station": station["name"],
            "river": station["river"],
            "district": station["district"],
            "danger_level": live.get("danger_level", station["danger_level"]),
            "water_level": live.get("water_level"),
            "recorded_at": live.get("recorded_at"),
            "discharge": discharge,
            "linked_district": station["linked_district"],
            "source": "ffwc_live",
        })

    # scrape না পাওয়া গেলে honest fallback — water_level=None রাখা হচ্ছে,
    # discharge দিয়ে replace করা হচ্ছে না, যাতে caller/frontend real observed
    # water level আর modeled discharge গুলিয়ে না ফেলে।
    return jsonify({
        "station": station["name"],
        "river": station["river"],
        "district": station["district"],
        "danger_level": station["danger_level"],
        "water_level": None,
        "recorded_at": None,
        "discharge": discharge,
        "linked_district": station["linked_district"],
        "source": "estimated_fallback",
    })

# ── Main Flood API ──
@app.route('/api/flood/<district_name>')
def get_flood(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404

    info = DISTRICTS[district_name]

    # ── Multi-river support ──
    # একটা জেলা দিয়ে একাধিক নদী গেলে (info["rivers"], ২০২৬-০৮ থেকে),
    # প্রতিটার discharge আলাদাভাবে fetch করে সবচেয়ে ঝুঁকিপূর্ণটা
    # (discharge/danger_level ratio সবচেয়ে বেশি) worst-case হিসেবে
    # স্কোরিং-এ ব্যবহার করা হয় — নিরাপত্তার দিক থেকে এটাই যুক্তিসঙ্গত,
    # কারণ একটা নদী বিপদসীমা ছাড়ালে বাকি নদী শান্ত থাকলেও জেলার সেই
    # অংশ ঝুঁকিতেই থাকে।
    rivers_list = info.get("rivers") or [{
        "name": info["river"], "lat": info["river_lat"], "lon": info["river_lon"],
        "danger_level": info["danger_level"], "ffwc_station": info.get("ffwc_station"),
        "ffwc_verified": info.get("ffwc_verified"), "is_primary": True,
    }]

    rivers_status = []
    for r in rivers_list:
        r_data = fetch_river(r["lat"], r["lon"])
        r_discharge = float(r_data.get("today") or 0)
        r_danger = r.get("danger_level") or 0
        # ⚠️ FIX (২০২৬-০৮): আগে discharge (m³/s) কে সরাসরি danger_level (মিটার)
        # দিয়ে ভাগ করে ratio বানানো হতো — এই দুটো ভিন্ন unit, ফলে কম danger_level
        # (মিটার)-এর নদী বাস্তব ঝুঁকি কম হলেও artificially বেশি ratio পেয়ে
        # "risk-determining river" হিসেবে ভুলভাবে নির্বাচিত হতো (সুনামগঞ্জে এই
        # কারণেই ছোট branch বারবার মূল নদীকে হারিয়ে যাচ্ছিল)। এখন discharge-কে
        # তার নিজস্ব verified/approximated reference_discharge (m³/s)-এর
        # সাপেক্ষে ভাগ করা হচ্ছে, যেটা একই unit — apples-to-apples তুলনা।
        r_reference_discharge = get_reference_discharge(r_danger, district_name) if r_danger else None
        r_ratio = (r_discharge / r_reference_discharge) if r_reference_discharge else 0
        rivers_status.append({
            "name": r["name"], "discharge_today": round(r_discharge),
            "forecast": r_data["forecast"], "dates": r_data["dates"],
            "danger_level": r_danger, "ratio": round(r_ratio, 3),
            "is_primary": r.get("is_primary", False),
            "ffwc_station": r.get("ffwc_station"), "ffwc_verified": r.get("ffwc_verified"),
            "fetch_ok": r_data.get("ok", False),
        })

    # worst-case: সর্বোচ্চ ratio-র নদীটাই স্কোরিং চালাবে (tie হলে primary জিতবে, কারণ ও লিস্টে প্রথমে থাকে)
    active_river = max(rivers_status, key=lambda x: x["ratio"])

    river = {"today": active_river["discharge_today"], "forecast": active_river["forecast"], "dates": active_river["dates"]}
    soil_moisture = fetch_soil_moisture(info["lat"], info["lon"])

    weather_data = fetch_weather(info["lat"], info["lon"])
    upstream_data = fetch_upstream(info["upstream"])

    discharge = float(active_river["discharge_today"])
    active_danger_level = active_river["danger_level"] or info["danger_level"]
    local_rain = float(weather_data.get("rain", 0) or 0)
    upstream_rain = float(upstream_data.get("rain", 0) or 0)
    soil_moisture = float(soil_moisture or 0)

    runoff = calculate_runoff(local_rain, info.get("cn", 80))

    active_reports = get_active_report_count(district_name)

    full_moon_status = is_full_moon_today()

    confluence_data = get_confluence_data(district_name)
    rainfall_intensity_data = get_rainfall_intensity_data(district_name, info, info["lat"], info["lon"])
    upstream_rain_history = get_upstream_rain_history(district_name, info)

    try:
        prediction = predict_flood(
            discharge=discharge,
            upstream_rain=upstream_rain,
            local_rain=local_rain,
            soil_moisture=soil_moisture,
            lag_time=info.get("lag_time", 24),
            cn=info.get("cn", 80),
            risk_category=info.get("risk", "মাঝারি"),
            district_name=district_name,
            flood_type=info.get("flood_type", "Riverine"),
            vulnerable_areas=info.get("vulnerable_areas", []),
            recent_reports=active_reports,
            is_full_moon=full_moon_status,
            danger_level=active_danger_level,
            confluence_data=confluence_data,
            rainfall_intensity_data=rainfall_intensity_data,
            upstream_rain_history=upstream_rain_history,
            # ⚠️ এখনো কোনো live BMD cyclone API নেই — flood_config.py-তে
            # কোনো জেলার entry-তে ম্যানুয়ালি 'cyclone_signal' key বসালে
            # (যেমন সত্যিকারের ঘূর্ণিঝড় সতর্কতার সময়) সেটা এখানে ব্যবহার
            # হবে, না থাকলে ডিফল্ট ০ (কোনো প্রভাব নেই)।
            cyclone_signal=info.get("cyclone_signal", 0)
        )
    except Exception as e:
        print(f"Prediction Error: {e}")
        prediction = {
            "level": "সতর্ক",
            "probability": 40,
            "message": f"⚠️ {district_name} এর জন্য রিয়েল-টাইম ডেটা বিশ্লেষণ চলছে। সাবধানে থাকুন।",
            "action": ["আবহাওয়ার খবরে নজর রাখুন", "প্রয়োজনীয় প্রস্তুতি নিন"],
            "ml_model_used": False
        }

    risk_score = prediction.get("probability", 0)

    # ⚠️ FIX (২০২৬-০৮): আগে API ব্যর্থ হলেও (river/weather/upstream fetch fail
    # করলে) rain/discharge চুপচাপ ০ ধরে prediction চালিয়ে DB-তে save করা হতো —
    # এতে outage-এর সময় ভুলভাবে "নিরাপদ" reading তৈরি হয়ে আগের সঠিক reading
    # মুছে যাওয়ার ঝুঁকি ছিল (false-safe)। এখন কোনো critical fetch ব্যর্থ হলে
    # DB-তে নতুন করে save করা হয় না — শেষ known-good reading DB-তে থেকে যায়,
    # এবং response-এ data_unavailable flag যোগ হয় যাতে frontend/user বুঝতে
    # পারে এই মুহূর্তের ডেটা সম্পূর্ণ live না।
    data_unavailable = not (active_river.get("fetch_ok") and weather_data.get("ok") and upstream_data.get("ok"))

    if not data_unavailable:
        try:
            save_reading(
                district_name, round(discharge), soil_moisture,
                local_rain, upstream_rain, risk_score, prediction["level"]
            )
        except Exception as e:
            print(f"save_reading error: {e}")
    else:
        print(f"⚠️ {district_name}: একটা বা একাধিক live API ব্যর্থ, এই reading DB-তে save করা হলো না")

    return jsonify({
        "district": district_name,
        "river": active_river["name"],
        "danger_level": active_danger_level,
        "risk_category": info["risk"],
        "flood_type": info.get("flood_type", "Riverine"),
        "data_unavailable": data_unavailable,
        "discharge_today": round(discharge),
        "forecast": river["forecast"],
        "dates": river["dates"],
        "rivers_status": rivers_status,
        "scoring_river": active_river["name"],
        "soil_moisture": soil_moisture,
        "lag_time": info["lag_time"],
        "runoff_mm": runoff,
        "risk_score": risk_score,
        "weather": weather_data,
        "upstream_weather": upstream_data,
        "upstream_warning": f"{info['lag_time']} ঘণ্টা পরে {district_name} তে প্রভাব পড়বে",
        "prediction": prediction,
        "ml_prediction": prediction,
        "flood_probability": prediction.get("probability", 0) if prediction else 0,
        "warning_level": prediction.get("level", "অনির্ণীত") if prediction else "অনির্ণীত",
        "warning_color": get_color_by_level(prediction.get("level", "নিরাপদ")) if prediction else "#808080",
        "lat": info["lat"],
        "lon": info["lon"]
    })

# ── Weather API ──
@app.route('/api/weather/<district_name>')
def get_weather(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404
    info = DISTRICTS[district_name]
    try:
        local = fetch_weather(info["lat"], info["lon"])
        upstream = fetch_upstream(info["upstream"])
        return jsonify({"district": district_name, "local": local, "upstream": upstream})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── River Forecast API ──
@app.route('/api/river/<district_name>')
def get_river(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404
    info = DISTRICTS[district_name]
    river = fetch_river(info["river_lat"], info["river_lon"])
    return jsonify({
        "district": district_name,
        "river": info["river"],
        "danger_level": info["danger_level"],
        "risk": info["risk"],
        "lag_time": info["lag_time"],
        "discharge_today": round(river["today"]),
        "forecast": river["forecast"],
        "dates": river["dates"],
    })

# ── Satellite API ──
@app.route('/api/satellite/<district_name>')
def get_satellite(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404
    info = DISTRICTS[district_name]
    river = fetch_river(info["river_lat"], info["river_lon"])
    soil_moisture = fetch_soil_moisture(info["lat"], info["lon"])
    try:
        sat_data = get_full_satellite_data(
            discharge=river["today"],
            danger_level=info["danger_level"],
            soil_moisture=soil_moisture,
            river_forecast=river.get("forecast", [])
        )
        return jsonify({"district": district_name, **sat_data})
    except Exception as e:
        print(f"Satellite Data Error: {e}")
        return jsonify({"error": str(e)}), 500

# ── Upstream Forecast API ──
@app.route('/api/upstream/forecast/<district_name>')
def upstream_forecast(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404
    if not WEATHER_API_KEY:
        return jsonify({"error": "Weather API key configured নেই"}), 503
    info = DISTRICTS[district_name]
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": info["upstream"], "appid": WEATHER_API_KEY, "units": "metric", "cnt": 56},
            timeout=5
        )
        if r.status_code != 200:
            print(f"OpenWeather forecast error {r.status_code}: {r.text[:200]}")
            return jsonify({"error": "উজানের আবহাওয়ার তথ্য এখন পাওয়া যাচ্ছে না"}), 502
        data = r.json()
        items = data.get("list")
        if not isinstance(items, list):
            print(f"OpenWeather forecast response missing list: {data}")
            return jsonify({"error": "উজানের আবহাওয়ার তথ্য অসম্পূর্ণ"}), 502
        forecast_list = []
        warnings = []
        for item in items[::8][:7]:
            date = item["dt_txt"][:10]
            rain = item.get("rain", {}).get("3h", 0)
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]

            if rain > 15:
                impact = "🚨 বন্যার আশঙ্কা"
                warnings.append(f"{date}: ভারী বৃষ্টি → {info['lag_time']} ঘণ্টা পরে {district_name} তে প্রভাব")
            elif rain > 5:
                impact = "⚠️ সতর্ক থাকুন"
            else:
                impact = "✅ স্বাভাবিক"

            forecast_list.append({"date": date, "rain": round(rain, 1), "temp": round(temp, 1), "humidity": humidity, "impact": impact})

        return jsonify({
            "district": district_name,
            "upstream_city": info["upstream"].split(",")[0],
            "lag_time": info["lag_time"],
            "forecast": forecast_list,
            "warnings": warnings,
        })
    except Exception as e:
        print(f"upstream_forecast error: {e}")
        return jsonify({"error": "উজানের পূর্বাভাস লোড করা যায়নি"}), 502

# ── Unions & High Risk APIs ──
@app.route('/api/unions/<district_name>')
def district_unions(district_name):
    try:
        unions = get_unions_by_district(district_name)
        return jsonify({"district": district_name, "unions": unions, "count": len(unions)})
    except NameError:
        return jsonify({"unions": []})

@app.route('/api/gazetteer/<district_name>')
def district_gazetteer(district_name):
    """
    জেলার সব real ইউনিয়নের নাম (bn/en) + upazila + সরকারি union parishad
    ওয়েবসাইট URL রিটার্ন করে (bangladesh-geocode dataset থেকে, ৪৫৪০টা
    ইউনিয়ন কভার)। এটা flood-risk তথ্য না — শুধু নাম/location resolve,
    dropdown populate, বা community report ফর্মে ব্যবহারের জন্য।
    """
    if get_all_unions_for_district is None:
        return jsonify({"error": "Gazetteer লোড করা যায়নি", "unions": []}), 503
    unions = get_all_unions_for_district(district_name)
    if not unions:
        return jsonify({"district": district_name, "unions": [], "count": 0})
    return jsonify({"district": district_name, "unions": unions, "count": len(unions)})

@app.route('/api/unions/high-risk')
def high_risk_unions():
    try:
        unions = get_high_risk_unions()
        return jsonify({"high_risk_unions": unions, "count": len(unions)})
    except NameError:
        return jsonify({"high_risk_unions": []})

# ── Historical Data API ──
@app.route('/api/history/<district_name>')
def history(district_name):
    try:
        data = get_history(district_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── PDF Generation API ──
@app.route('/api/report/pdf/<district_name>')
def download_pdf(district_name):
    if district_name not in DISTRICTS:
        return jsonify({"error": "জেলা পাওয়া যায়নি"}), 404
    info = DISTRICTS[district_name]
    try:
        river = fetch_river(info["river_lat"], info["river_lon"])
        soil_moisture = fetch_soil_moisture(info["lat"], info["lon"])
        weather_data = fetch_weather(info["lat"], info["lon"])
        upstream_data = fetch_upstream(info["upstream"])
        discharge = river["today"]

        active_reports = get_active_report_count(district_name)
        full_moon_status = is_full_moon_today()
        confluence_data = get_confluence_data(district_name)
        rainfall_intensity_data = get_rainfall_intensity_data(district_name, info, info["lat"], info["lon"])
        upstream_rain_history = get_upstream_rain_history(district_name, info)

        try:
            prediction = predict_flood(
                discharge=discharge,
                upstream_rain=upstream_data.get("rain", 0),
                local_rain=weather_data.get("rain", 0),
                soil_moisture=soil_moisture,
                lag_time=info["lag_time"],
                cn=info.get("cn", 80),
                risk_category=info["risk"],
                district_name=district_name,
                flood_type=info.get("flood_type", "Riverine"),
                vulnerable_areas=info.get("vulnerable_areas", []),
                recent_reports=active_reports,
                is_full_moon=full_moon_status,
                danger_level=info.get("danger_level"),
                confluence_data=confluence_data,
                rainfall_intensity_data=rainfall_intensity_data,
                upstream_rain_history=upstream_rain_history,
                cyclone_signal=info.get("cyclone_signal", 0)
            )
        except Exception as e:
            print(f"Prediction Error (PDF): {e}")
            prediction = {"level": "নিরাপদ", "probability": 0, "message": "ML Error Fallback"}

        data = {
            "district": district_name,
            "river": info["river"],
            "danger_level": info["danger_level"],
            "risk_category": info["risk"],
            "discharge_today": round(discharge),
            "soil_moisture": soil_moisture,
            "lag_time": info["lag_time"],
            "weather": weather_data,
            "upstream_weather": upstream_data,
            "prediction": prediction,
        }

        try:
            pdf_buffer = generate_flood_report(data)
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'floodAi_{district_name}_{datetime.now().strftime("%Y%m%d")}.pdf'
            )
        except NameError:
            return jsonify({"error": "pdf_report module not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Overall System Stats ──
@app.route('/api/stats')
def overall_stats():
    try:
        union_stats = get_union_stats()
    except NameError:
        union_stats = {}
    return jsonify({
        "total_districts": len(DISTRICTS),
        **union_stats,
        "data_sources": [
            "Open-Meteo Flood API",
            "OpenWeatherMap API",
            "Open-Meteo Soil Moisture",
        ]
    })

# ── Active Warnings List ──
@app.route('/api/warnings/active')
def active_warnings():
    conn = None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM flood_readings
            WHERE warning_level != 'নিরাপদ'
              AND timestamp > datetime('now', '-6 hours')
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        rows = [dict(r) for r in cursor.fetchall()]
        return jsonify(rows)
    except Exception as e:
        print(f"Active Warnings DB Error: {e}")
        return jsonify([])
    finally:
        if conn:
            conn.close()

# ── Community Reports ──
@app.route('/api/report', methods=['POST'])
def community_report():
    data = get_json_body()
    district = data.get('district')
    status = data.get('status')
    valid_statuses = {'normal', 'rising', 'road', 'house', 'emergency'}
    if district not in DISTRICTS:
        return jsonify({"error": "Valid district required"}), 400
    if status not in valid_statuses:
        return jsonify({"error": "Valid report status required"}), 400
    save_community_report(
        district, status,
        (data.get('description') or '').strip()[:500],
        to_float(data.get('lat')), to_float(data.get('lon')),
    )
    return jsonify({"message": "✅ Report submitted!"})

@app.route('/api/reports/<district_name>')
def get_reports(district_name):
    data = get_community_reports(district_name)
    return jsonify(data)

# ── Chatbot ──
@app.route('/api/chat', methods=['POST'])
def chat():
    data = get_json_body()
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify({"error": "Message empty"}), 400
    if len(msg) > 1000:
        return jsonify({"error": "Message too long"}), 400
    if not GROQ_API_KEY:
        return jsonify({"error": "Chatbot API key configured নেই"}), 503
    client_id = (request.headers.get("X-Forwarded-For") or request.remote_addr or "local").split(",")[0].strip()
    if is_chat_rate_limited(client_id):
        return jsonify({"error": "Too many chat requests. একটু পরে আবার চেষ্টা করুন।"}), 429

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "তুমি FloodAI এর বন্যা বিশেষজ্ঞ। বাংলাদেশের বন্যা, নদী, আবহাওয়া, দুর্যোগ ব্যবস্থাপনা নিয়ে বাংলায় সহজ ভাষায় সংক্ষিপ্ত উত্তর দাও।"},
                {"role": "user", "content": msg}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"chat error: {e}")
        return jsonify({"error": "Chatbot response তৈরি করা যায়নি"}), 502

# ── User Authentication ──
@app.route('/api/register', methods=['POST'])
def register():
    data = get_json_body()
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    district = data.get('district')
    phone = (data.get('phone') or '').strip()
    if not name or not email or len(password) < 6 or district not in DISTRICTS:
        return jsonify({"error": "Name, valid email, 6+ character password, and district required"}), 400
    success = register_user(
        name, email, password, district, phone,
    )
    if success:
        return jsonify({"message": "✅ Registration successful!"})
    return jsonify({"error": "Email already exists"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = get_json_body()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    user = get_user(email, password)
    if user:
        return jsonify({
            "message": "✅ Login successful!",
            "user": {"name": user["name"], "email": user["email"], "district": user["district"]}
        })
    return jsonify({"error": "Invalid email or password"}), 401


# ============================================================
# BACKGROUND SCHEDULER (শুধু Render-এ, production-এ)
# ============================================================
# Render নিজে থেকেই RENDER=true environment variable সেট করে দেয়।
# লোকালে (VS Code) এই ব্লক চলবে না, তাই লোকাল workflow (আলাদা করে
# `python scheduler.py` চালানো) আগের মতোই কাজ করবে। কিন্তু Render-এ
# gunicorn app.py import করলে এখানেই একটা background thread-এ
# scheduler.py-র সব cron job (১৫ মিনিট/১ ঘণ্টা/সকাল-সন্ধ্যা আপডেট)
# চালু হয়ে যাবে, আলাদা কোনো service/খরচ ছাড়াই।
if os.getenv("RENDER"):
    import threading

    def _start_background_scheduler():
        import time
        time.sleep(5)  # Flask পুরোপুরি bind হওয়ার সময় দেওয়া
        from scheduler import run_scheduler_loop
        try:
            run_scheduler_loop()
        except Exception as e:
            print(f"⚠️ Background scheduler crashed: {e}")

    threading.Thread(target=_start_background_scheduler, daemon=True).start()
    print("🕐 Background scheduler thread started (Render production mode)")

# ============================================================
# RUN SERVER
# ============================================================
if __name__ == '__main__':
    print("🚀 FloodAI Backend Complete Version starting...")
    print("📍 http://localhost:5000")
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", port=5000)