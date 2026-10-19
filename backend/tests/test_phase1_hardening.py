import sqlite3

import pytest

import database
import model as model_module
from model import predict_flood

KURIGRAM = "কুড়িগ্রাম"

# ── নিচের inputs-এ নদী/আবহাওয়া নিরাপদ বা ঝুঁকিপূর্ণ — দুই ধরনের baseline ──
LOW = dict(
    discharge=100, upstream_rain=0, local_rain=0, soil_moisture=0.3, lag_time=48,
    cn=70, risk_category="কম", month=2, flood_type="Riverine", danger_level=10,
)
HIGH = dict(
    discharge=3000, upstream_rain=30, local_rain=60, soil_moisture=0.9, lag_time=6,
    cn=90, risk_category="অতি উচ্চ", month=8, flood_type="Riverine", danger_level=10,
)


# ── ffwc_id collision (কুড়িগ্রাম: ধরলা SW77 বনাম ব্রহ্মপুত্র SW45, দুটোই 26.05m) ──
def test_ffwc_id_selects_correct_river_reference():
    kw = dict(
        discharge=1000, upstream_rain=0, local_rain=0, soil_moisture=0.5, lag_time=24,
        cn=80, risk_category="উচ্চ", month=8, district_name=KURIGRAM,
        flood_type="Riverine", danger_level=26.05,
    )
    dharla = predict_flood(ffwc_id="SW77", **kw)["input_summary"]["reference_discharge_m3s"]
    brahmaputra = predict_flood(ffwc_id="SW45", **kw)["input_summary"]["reference_discharge_m3s"]
    assert dharla == 800
    assert brahmaputra == 42000


# ── Community report: একাই "বিপদ" বানাতে পারবে না ──
# (এই দুই টেস্টে ML বন্ধ রাখা হয়েছে, যাতে ফলাফল নির্ধারিত rule-based score-এর উপর
# দাঁড়ায়, pickle-এর আচরণের উপর না — ML-এর আচরণ আলাদা টেস্টে নিচে)
@pytest.fixture()
def rule_based(monkeypatch):
    monkeypatch.setattr(model_module, "load_ml_model", lambda: (None, None, None))


def test_reports_cannot_force_danger_when_hydrology_is_safe(rule_based):
    assert predict_flood(**LOW)["probability"] < 30  # sanity: baseline সত্যিই নিরাপদ
    result = predict_flood(recent_reports=10, **LOW)
    assert result["probability"] <= 49
    assert result["level"] != "বিপদ"
    assert result["reports_capped_uncorroborated"] is True


def test_reports_still_escalate_when_hydrology_agrees(rule_based):
    assert predict_flood(**HIGH)["probability"] >= 30  # sanity
    result = predict_flood(recent_reports=5, **HIGH)
    assert result["probability"] >= 85
    assert result["reports_capped_uncorroborated"] is False


# ── জানা সমস্যা: ML মডেল শুকনো মৌসুমে/কম প্রবাহেও ঝুঁকি বেশি দেখায় ──
# (Phase 3-এ real data দিয়ে retrain করলে এই টেস্ট pass করবে — তখন xfail মার্কটা তুলে দাও;
# strict=True থাকায় হঠাৎ pass করলে suite ব্যর্থ হয়ে মনে করিয়ে দেবে)
@pytest.mark.xfail(strict=True, reason="ML model: ফেব্রুয়ারি, ০ বৃষ্টি, নদীর প্রবাহ বিপদসীমার ~১০% — তবু ~৩১% সম্ভাবনা দেয়")
def test_ml_model_is_calibrated_for_dry_low_flow_scenario():
    assert predict_flood(**LOW)["probability"] < 30


# ── একই reporter-এর একাধিক report একবারই গোনা হয় ──
def test_active_report_count_dedupes_by_reporter(app_module):
    d = "ঢাকা"
    for _ in range(6):
        database.save_community_report(d, "emergency", "x", 0, 0, reporter_hash="same-client")
    assert app_module.get_active_report_count(d) == 1
    for i in range(3):
        database.save_community_report(d, "emergency", "x", 0, 0, reporter_hash=f"other-{i}")
    assert app_module.get_active_report_count(d) == 4


def test_reports_endpoint_hides_reporter_hash(client):
    r = client.post("/api/report", json={"district": "সিলেট", "status": "rising", "description": "test"})
    assert r.status_code == 200
    rows = client.get("/api/reports/সিলেট").get_json()
    assert rows and all("reporter_hash" not in row for row in rows)


# ── Rate limit: X-Forwarded-For spoof দিয়ে এড়ানো যায় না ──
def test_spoofed_forwarded_for_does_not_bypass_auth_rate_limit(client):
    statuses = []
    for i in range(12):
        resp = client.post(
            "/api/login",
            json={"email": "nobody@example.com", "password": "wrong-password"},
            headers={"X-Forwarded-For": f"10.0.0.{i}"},
        )
        statuses.append(resp.status_code)
    assert 429 in statuses, statuses


# ── Validation log: secret, limit clamp ──
def test_validation_log_requires_secret_and_clamps_limit(client, monkeypatch):
    monkeypatch.setenv("VALIDATION_COLLECT_SECRET", "s3cret")
    assert client.get("/api/validation/log").status_code == 403
    assert client.get("/api/validation/log", headers={"X-Internal-Secret": "wrong"}).status_code == 403
    ok = client.get("/api/validation/log?limit=abc", headers={"X-Internal-Secret": "s3cret"})
    assert ok.status_code == 200
    ok = client.get("/api/validation/log?limit=99999999", headers={"X-Internal-Secret": "s3cret"})
    assert ok.status_code == 200


# ── Forecast: river fetch ব্যর্থ হলে false-safe না, স্পষ্ট 503 ──
def test_forecast_returns_503_when_river_data_unavailable(client, app_module, monkeypatch):
    monkeypatch.setattr(
        app_module, "fetch_river",
        lambda lat, lon: {"today": 0, "discharge_change_pct": 0.0, "forecast": [], "dates": [], "ok": False},
    )
    resp = client.get(f"/api/flood/{KURIGRAM}/forecast")
    assert resp.status_code == 503
    assert resp.get_json()["data_unavailable"] is True


# ── Cache: সফল response cache হয়, ব্যর্থ হয় না ──
def test_ttl_cache_only_stores_successful_responses(app_module):
    calls = {"n": 0}

    @app_module._ttl_cached("t", lambda: 60)
    def flaky(x):
        calls["n"] += 1
        return {"ok": calls["n"] >= 2, "n": calls["n"]}

    assert flaky(1)["ok"] is False   # ব্যর্থ — cache হয়নি
    assert flaky(1)["ok"] is True    # আবার call হলো, সফল — cache হলো
    assert flaky(1)["ok"] is True    # cache hit
    assert calls["n"] == 2


# ── Persistent DB path ও পুরনো DB migration ──
def test_db_path_comes_from_env():
    assert database.DB_PATH.name == "test.db"
    assert "floodai-test-" in str(database.DB_PATH)


def test_init_db_migrates_old_community_reports_table(tmp_path, monkeypatch):
    old = tmp_path / "old.db"
    conn = sqlite3.connect(old)
    conn.execute(
        "CREATE TABLE community_reports (id INTEGER PRIMARY KEY AUTOINCREMENT, district TEXT NOT NULL,"
        " timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT, description TEXT, lat REAL, lon REAL)"
    )
    conn.commit()
    conn.close()
    monkeypatch.setattr(database, "DB_PATH", old)
    database.init_db()
    database.init_db()  # idempotent
    cols = [r[1] for r in sqlite3.connect(old).execute("PRAGMA table_info(community_reports)")]
    assert "reporter_hash" in cols


# ── Outage: সব live API ব্যর্থ হলে প্রধান স্তর "নিরাপদ" হতে পারবে না ──
def test_outage_never_reports_safe(client, app_module, monkeypatch):
    monkeypatch.setattr(
        app_module, "fetch_river",
        lambda lat, lon: {"today": 0, "discharge_change_pct": 0.0, "forecast": [], "dates": [], "ok": False},
    )
    monkeypatch.setattr(app_module, "fetch_weather", lambda lat, lon: {"temp": None, "humidity": None, "rain": 0, "wind": None, "desc": "", "ok": False})
    monkeypatch.setattr(app_module, "fetch_upstream", lambda city: {"city": "x", "rain": 0, "humidity": None, "temp": None, "ok": False})
    monkeypatch.setattr(app_module, "fetch_soil_moisture_status", lambda lat, lon: {"value": 0.5, "ok": True})
    j = client.get(f"/api/flood/{KURIGRAM}").get_json()
    assert j["data_unavailable"] is True
    assert j["data_quality"] == "degraded"
    assert j["warning_level"] != "নিরাপদ"
    assert j["prediction"]["data_incomplete"] is True
    # সংখ্যা বানানো হয় না: স্তর floor হয়েছে, কিন্তু probability আসল হিসাব করা মান (৫০ বসানো নয়)
    assert j["prediction"]["safety_floor_applied"] is True
    assert j["flood_probability"] < 50


# ── Partial outage: শুধু একটি *অ-active* নদী ব্যর্থ হলেও "নিরাপদ" নয় ──
def _ok_river(discharge):
    return {"today": discharge, "discharge_change_pct": 0.0, "forecast": [discharge] * 7, "dates": ["d"] * 7, "ok": True}


def test_failed_secondary_river_is_not_silently_ignored(client, app_module, monkeypatch):
    rivers = app_module.DISTRICTS[KURIGRAM]["rivers"]
    primary = (rivers[0]["lat"], rivers[0]["lon"])
    failing = next((r for r in rivers if (r["lat"], r["lon"]) != primary), None)
    assert failing is not None  # কুড়িগ্রামে অন্তত একটি আলাদা-coordinate নদী থাকার কথা

    def fake_river(lat, lon):
        if (lat, lon) == (failing["lat"], failing["lon"]):
            return {"today": 0, "discharge_change_pct": 0.0, "forecast": [], "dates": [], "ok": False}
        return _ok_river(10)

    monkeypatch.setattr(app_module, "fetch_river", fake_river)
    monkeypatch.setattr(app_module, "fetch_weather", lambda lat, lon: {"temp": 30, "humidity": 80, "rain": 0, "wind": 1, "desc": "", "ok": True})
    monkeypatch.setattr(app_module, "fetch_upstream", lambda city: {"city": "x", "rain": 0, "humidity": 50, "temp": 30, "ok": True})
    monkeypatch.setattr(app_module, "fetch_soil_moisture_status", lambda lat, lon: {"value": 0.3, "ok": True})
    j = client.get(f"/api/flood/{KURIGRAM}").get_json()
    assert j["data_unavailable"] is True
    assert any(src.startswith("river:") for src in j["failed_sources"])
    assert j["warning_level"] != "নিরাপদ"


def test_soil_only_failure_is_partial_not_unavailable(client, app_module, monkeypatch):
    monkeypatch.setattr(app_module, "fetch_river", lambda lat, lon: _ok_river(10))
    monkeypatch.setattr(app_module, "fetch_weather", lambda lat, lon: {"temp": 30, "humidity": 80, "rain": 0, "wind": 1, "desc": "", "ok": True})
    monkeypatch.setattr(app_module, "fetch_upstream", lambda city: {"city": "x", "rain": 0, "humidity": 50, "temp": 30, "ok": True})
    monkeypatch.setattr(app_module, "fetch_soil_moisture_status", lambda lat, lon: {"value": 0.5, "ok": False})
    j = client.get(f"/api/flood/{KURIGRAM}").get_json()
    assert j["data_unavailable"] is False
    assert j["data_quality"] == "partial"
    assert j["failed_sources"] == ["soil_moisture"]


# ── Report dedupe: ৫০-row সীমায় ধরা পড়ে না ──
def test_distinct_reporters_counted_beyond_50_rows(app_module):
    d = "রংপুর"
    for i in range(3):
        database.save_community_report(d, "emergency", "x", 0, 0, reporter_hash=f"early-{i}")
    for _ in range(60):  # একজন ৬০টা report দিয়ে বাকিদের ৫০-এর বাইরে ঠেলে দিল
        database.save_community_report(d, "emergency", "x", 0, 0, reporter_hash="spammer")
    assert app_module.get_active_report_count(d) == 4


# ── Proxy hops: ভুল env value app ভাঙে না ──
@pytest.mark.parametrize("raw,default,expected", [("2", 1, 2), ("abc", 1, 1), ("-1", 0, 0), ("99", 1, 1), (" 3 ", 0, 3)])
def test_proxy_hops_parsing(app_module, raw, default, expected):
    assert app_module._parse_proxy_hops(raw, default) == expected
