"""Test environment: env vars must be set BEFORE app/database are imported
(database.DB_PATH and app's SECRET_KEY/rate-limit settings are read at import time)."""
import os
import sys
import tempfile
from pathlib import Path

_TMP = tempfile.mkdtemp(prefix="floodai-test-")
os.environ["FLOODAI_DB_PATH"] = str(Path(_TMP) / "test.db")
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["FLASK_DEBUG"] = "0"
os.environ["SESSION_COOKIE_SECURE"] = "0"
os.environ["TRUSTED_PROXY_HOPS"] = "0"
os.environ["AUTH_RATE_MAX_REQUESTS"] = "8"
os.environ["REPORT_RATE_MAX_REQUESTS"] = "1000"
os.environ.pop("RENDER", None)
os.environ.pop("VALIDATION_COLLECT_SECRET", None)

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest  # noqa: E402


@pytest.fixture()
def app_module():
    import app as app_module
    app_module._auth_hits.clear()
    app_module._chat_hits.clear()
    app_module._report_hits.clear()
    app_module._FETCH_CACHE.clear()
    return app_module


@pytest.fixture()
def client(app_module):
    return app_module.app.test_client()
