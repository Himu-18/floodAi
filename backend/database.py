# database.py

import sqlite3
import os
from pathlib import Path
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ⚠️ আগে DB_PATH = "floodai.db" ছিল — relative path, যেটা তুমি কোন ফোল্ডার থেকে
# app.py চালাচ্ছ তার উপর নির্ভর করত (root থেকে চালালে root-এ DB বানাত, backend
# থেকে চালালে backend-এ)। এখন app.py-র মতোই script-এর নিজের অবস্থান থেকে
# absolute path বানানো হচ্ছে, যাতে কোথা থেকে চালাও তাতে কিছু আসে যায় না —
# সবসময় backend/floodai.db-ই ব্যবহার হবে।
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "floodai.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS flood_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            discharge REAL,
            soil_moisture REAL,
            local_rain REAL DEFAULT 0,
            upstream_rain REAL DEFAULT 0,
            risk_score REAL,
            warning_level TEXT
        );

        CREATE TABLE IF NOT EXISTS community_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            description TEXT,
            lat REAL,
            lon REAL
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            district TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready!")

def save_reading(district, discharge, soil_moisture,
                 local_rain, upstream_rain, risk_score, warning_level):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO flood_readings
            (district, discharge, soil_moisture, local_rain,
             upstream_rain, risk_score, warning_level)
            VALUES (?,?,?,?,?,?,?)
        """, (district, discharge, soil_moisture,
              local_rain, upstream_rain, risk_score, warning_level))
        conn.commit()
    except Exception as e:
        print(f"DB Error (save_reading): {e}")
    finally:
        conn.close()

def save_community_report(district, status, description, lat, lon):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO community_reports
            (district, status, description, lat, lon)
            VALUES (?,?,?,?,?)
        """, (district, status, description, lat, lon))
        conn.commit()
    except Exception as e:
        print(f"DB Error (save_community_report): {e}")
    finally:
        conn.close()

def get_history(district, limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM flood_readings
            WHERE district = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (district, limit))
        return [dict(r) for r in cursor.fetchall()]
    except Exception as e:
        print(f"DB Error (get_history): {e}")
        return []
    finally:
        conn.close()

# ── মানচিত্রের জন্য: প্রতিটা জেলার সবচেয়ে সাম্প্রতিক reading একবারে আনা ──
def get_latest_readings():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT fr.district, fr.timestamp, fr.risk_score, fr.warning_level,
                   -- ⚠️ FIX (২০২৬-০৮): আগে শুধু সবচেয়ে সাম্প্রতিক reading আনা হতো,
                   -- কিন্তু কতটা পুরনো তা যাচাই করা হতো না — scheduler অনেকক্ষণ
                   -- বন্ধ থাকলে (Render free-tier spin-down ইত্যাদি) দিনের-পর-দিন
                   -- পুরনো "বিপদ" reading ম্যাপে "live" হিসেবে দেখানোর ঝুঁকি ছিল।
                   -- এখন ৬ ঘণ্টার বেশি পুরনো হলে is_stale=1 flag যোগ হচ্ছে, frontend
                   -- এটা দেখে চাইলে আলাদাভাবে (ধূসর/"পুরনো ডেটা") দেখাতে পারবে।
                   (julianday('now') - julianday(fr.timestamp)) * 24 > 6 AS is_stale
            FROM flood_readings fr
            INNER JOIN (
                SELECT district, MAX(timestamp) AS max_ts
                FROM flood_readings
                GROUP BY district
            ) latest
            ON fr.district = latest.district AND fr.timestamp = latest.max_ts
        """)
        return [dict(r) for r in cursor.fetchall()]
    except Exception as e:
        print(f"DB Error (get_latest_readings): {e}")
        return []
    finally:
        conn.close()

def get_community_reports(district, limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM community_reports
            WHERE district = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (district, limit))
        return [dict(r) for r in cursor.fetchall()]
    except Exception as e:
        print(f"DB Error (get_community_reports): {e}")
        return []
    finally:
        conn.close()

def register_user(name, email, password, district, phone):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed_pw = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (name, email, password, district, phone)
            VALUES (?,?,?,?,?)
        """, (name, email, hashed_pw, district, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"DB Error (register_user): {e}")
        return False
    finally:
        conn.close()

def get_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row and check_password_hash(row["password"], password):
            return dict(row)
        return None
    except Exception as e:
        print(f"DB Error (get_user): {e}")
        return None
    finally:
        conn.close()