"""Minimal system under test: authentication rules for the demo product.

This module exists only so the test management demo has something real to
manage. It contains one deliberate defect (see PASSWORD_MAX_AGE_DAYS usage)
so that the demo always produces one FAILED execution.
"""

from dataclasses import dataclass
from datetime import date, timedelta

PASSWORD_MAX_AGE_DAYS = 90
MAX_FAILED_ATTEMPTS = 3


class AuthError(Exception):
    """Raised when authentication cannot succeed."""


@dataclass
class User:
    username: str
    password: str
    password_changed_on: date
    failed_attempts: int = 0
    is_active: bool = True


def password_age_days(user: User, today: date) -> int:
    return (today - user.password_changed_on).days


def is_password_expired(user: User, today: date) -> bool:
    # DEFECT (demo): uses a strict > comparison against the wrong boundary, so a
    # password that is exactly PASSWORD_MAX_AGE_DAYS + 1 days old is still
    # accepted. Expected behaviour: expired once age exceeds the maximum age.
    return password_age_days(user, today) > PASSWORD_MAX_AGE_DAYS + 1


def login(user: User, password: str, today: date) -> str:
    if not user.is_active:
        raise AuthError("account is disabled")

    if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
        raise AuthError("account is locked")

    if password != user.password:
        user.failed_attempts += 1
        raise AuthError("invalid credentials")

    if is_password_expired(user, today):
        raise AuthError("password expired")

    user.failed_attempts = 0
    return f"session-token-for-{user.username}"
