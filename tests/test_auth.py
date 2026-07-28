"""Automated regression suite for the demo product.

Each test name matches the `script` field of a Test Case in Kiwi TCMS, which is
how automation/report_results.py maps a JUnit result back to a managed case.
"""

from datetime import date, timedelta

import pytest

from app.auth import (
    MAX_FAILED_ATTEMPTS,
    PASSWORD_MAX_AGE_DAYS,
    AuthError,
    User,
    login,
)

TODAY = date(2026, 6, 1)


def make_user(password_age_days: int = 0, **kwargs) -> User:
    return User(
        username="john.doe",
        password="Correct-Horse-1",
        password_changed_on=TODAY - timedelta(days=password_age_days),
        **kwargs,
    )


def test_login_with_valid_credentials_returns_token():
    user = make_user()
    assert login(user, "Correct-Horse-1", TODAY).startswith("session-token-for-")


def test_login_with_wrong_password_is_rejected():
    user = make_user()
    with pytest.raises(AuthError, match="invalid credentials"):
        login(user, "wrong", TODAY)
    assert user.failed_attempts == 1


def test_login_is_blocked_after_max_failed_attempts():
    user = make_user(failed_attempts=MAX_FAILED_ATTEMPTS)
    with pytest.raises(AuthError, match="locked"):
        login(user, "Correct-Horse-1", TODAY)


def test_login_with_disabled_account_is_rejected():
    user = make_user(is_active=False)
    with pytest.raises(AuthError, match="disabled"):
        login(user, "Correct-Horse-1", TODAY)


def test_login_with_expired_password_is_rejected():
    """Deliberately failing: reveals the off-by-one in is_password_expired."""
    user = make_user(password_age_days=PASSWORD_MAX_AGE_DAYS + 1)
    with pytest.raises(AuthError, match="password expired"):
        login(user, "Correct-Horse-1", TODAY)
