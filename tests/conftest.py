import os
import re
from datetime import datetime

# Must be set before app.py is imported, since it reads SECRET_KEY at module level.
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
import database.db as db_module
from app import app as flask_app

_LOG_FILE = os.path.join(os.path.dirname(__file__), "test_logs.md")
_http_buffer: list[str] = []   # HTTP calls for the current test
_test_results: list[dict] = [] # accumulates across the session for summary


# ── HTML helpers ──────────────────────────────────────────────────────────────

def _page_title(data: bytes) -> str:
    m = re.search(rb"<title>(.+?)</title>", data)
    return m.group(1).decode("utf-8", errors="replace") if m else "(no title)"


def _inline_errors(data: bytes) -> list[str]:
    hits = re.findall(rb'class="auth-error"[^>]*>\s*([^<]+)', data)
    return [h.decode("utf-8", errors="replace").strip() for h in hits]


# ── Formatting ────────────────────────────────────────────────────────────────

def _format_call_md(method: str, url: str, payload: dict | None, resp) -> str:
    lines = ["```"]
    lines.append(f"{method:4s}  {url}")
    if payload:
        safe = {k: ("●●●●●●●●" if "password" in k.lower() else v)
                for k, v in payload.items()}
        lines.append(f"data  → {safe}")
    lines.append(f"status← {resp.status_code}")
    if resp.data:
        lines.append(f"page  → {_page_title(resp.data)}")
        for err in _inline_errors(resp.data):
            lines.append(f"error → {err}")
    lines.append("```")
    return "\n".join(lines)


def _print_call(method: str, url: str, payload: dict | None, resp) -> None:
    print(f"\n  {'─'*60}")
    print(f"  {method:4s}  {url}")
    if payload:
        safe = {k: ("●●●●●●●●" if "password" in k.lower() else v)
                for k, v in payload.items()}
        print(f"  data  → {safe}")
    print(f"  status← {resp.status_code}")
    if resp.data:
        print(f"  page  → {_page_title(resp.data)}")
        for err in _inline_errors(resp.data):
            print(f"  error → {err}")


# ── Instrumented test client ──────────────────────────────────────────────────

class _InstrumentedClient:
    """Wraps the Flask test client, logging every HTTP call to stdout and buffer."""

    def __init__(self, real_client):
        self._c = real_client

    def get(self, url, **kw):
        resp = self._c.get(url, **kw)
        _print_call("GET", url, None, resp)
        _http_buffer.append(_format_call_md("GET", url, None, resp))
        return resp

    def post(self, url, data=None, **kw):
        resp = self._c.post(url, data=data, **kw)
        _print_call("POST", url, data, resp)
        _http_buffer.append(_format_call_md("POST", url, data, resp))
        return resp

    def __getattr__(self, name):
        return getattr(self._c, name)


# ── Pytest session hooks ──────────────────────────────────────────────────────

def pytest_sessionstart(session):
    """Wipe and recreate test_logs.md at the start of every run."""
    _test_results.clear()
    with open(_LOG_FILE, "w") as f:
        f.write("# Spendly — Test Run Log\n\n")
        f.write(f"**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        f.write("---\n\n")


def pytest_sessionfinish(session, exitstatus):
    """Append the pass/fail summary table after all tests complete."""
    passed = sum(1 for r in _test_results if r["result"] == "PASSED")
    failed = sum(1 for r in _test_results if r["result"] == "FAILED")
    total  = len(_test_results)

    with open(_LOG_FILE, "a") as f:
        f.write("## Summary\n\n")
        f.write("| | Count |\n|---|---|\n")
        f.write(f"| **Total** | {total} |\n")
        f.write(f"| ✅ Passed | {passed} |\n")
        f.write(f"| ❌ Failed | {failed} |\n")


# ── Per-test log hook ─────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach the call-phase report to the test item so fixtures can read it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def _write_test_log(request):
    """Clear the HTTP buffer before each test; write its trace to the log file after."""
    _http_buffer.clear()
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep is None:
        return

    result = "PASSED" if rep.passed else "FAILED"
    emoji  = "✅" if result == "PASSED" else "❌"
    _test_results.append({"node_id": request.node.nodeid, "result": result})

    with open(_LOG_FILE, "a") as f:
        f.write(f"## {emoji} `{request.node.nodeid}`\n\n")
        if _http_buffer:
            f.write("### HTTP Trace\n\n")
            for entry in _http_buffer:
                f.write(entry + "\n\n")
        else:
            f.write("_No HTTP calls made in this test._\n\n")
        f.write("---\n\n")


# ── App / client fixtures ─────────────────────────────────────────────────────

@pytest.fixture()
def app(tmp_path, monkeypatch):
    """Isolated Flask app pointing at a fresh in-process SQLite database."""
    test_db = str(tmp_path / "test_spendly.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_db)
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret-key"})
    with flask_app.app_context():
        db_module.init_db()
    yield flask_app


@pytest.fixture()
def client(app):
    return _InstrumentedClient(app.test_client())


# ── Shared auth helpers ───────────────────────────────────────────────────────

def register(client, name="Alice", email="alice@example.com", password="password123"):
    return client.post(
        "/register",
        data={"name": name, "email": email, "password": password},
        follow_redirects=True,
    )


def login(client, email="alice@example.com", password="password123"):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
