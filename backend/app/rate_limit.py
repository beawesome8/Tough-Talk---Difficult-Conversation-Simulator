"""Simple in-memory per-IP rate limit and a global daily call budget.
No new dependency: fixed-window counters are plenty for a one-day demo."""
import os
import time
from collections import defaultdict
from datetime import datetime, timezone

RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "20"))
DAILY_BUDGET_CALLS = int(os.environ.get("DAILY_BUDGET_CALLS", "500"))

_ip_hits: dict[str, list[float]] = defaultdict(list)
_daily_count = 0
_daily_count_date: str | None = None


def check_rate_limit(ip: str) -> bool:
    now = time.time()
    hits = [t for t in _ip_hits[ip] if now - t < 60]
    _ip_hits[ip] = hits
    if len(hits) >= RATE_LIMIT_PER_MINUTE:
        return False
    hits.append(now)
    return True


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def check_daily_budget() -> bool:
    global _daily_count, _daily_count_date
    if _daily_count_date != _today():
        _daily_count_date = _today()
        _daily_count = 0
    return _daily_count < DAILY_BUDGET_CALLS


def record_call() -> None:
    global _daily_count, _daily_count_date
    if _daily_count_date != _today():
        _daily_count_date = _today()
        _daily_count = 0
    _daily_count += 1
