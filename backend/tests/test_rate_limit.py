import time

from app import rate_limit


def setup_function():
    rate_limit._ip_hits.clear()
    rate_limit._daily_count = 0
    rate_limit._daily_count_date = None


def test_allows_requests_under_limit():
    for _ in range(rate_limit.RATE_LIMIT_PER_MINUTE):
        assert rate_limit.check_rate_limit("1.2.3.4") is True


def test_blocks_requests_over_limit():
    for _ in range(rate_limit.RATE_LIMIT_PER_MINUTE):
        rate_limit.check_rate_limit("1.2.3.4")
    assert rate_limit.check_rate_limit("1.2.3.4") is False


def test_different_ips_tracked_separately():
    for _ in range(rate_limit.RATE_LIMIT_PER_MINUTE):
        rate_limit.check_rate_limit("1.2.3.4")
    assert rate_limit.check_rate_limit("5.6.7.8") is True


def test_old_hits_expire(monkeypatch):
    for _ in range(rate_limit.RATE_LIMIT_PER_MINUTE):
        rate_limit.check_rate_limit("1.2.3.4")
    future = time.time() + 61
    monkeypatch.setattr(time, "time", lambda: future)
    assert rate_limit.check_rate_limit("1.2.3.4") is True


def test_daily_budget_blocks_once_exceeded():
    for _ in range(rate_limit.DAILY_BUDGET_CALLS):
        assert rate_limit.check_daily_budget() is True
        rate_limit.record_call()
    assert rate_limit.check_daily_budget() is False
