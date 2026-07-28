#!/usr/bin/env python3
"""Create the demo fixture inside a fresh Kiwi TCMS instance.

Creates: Product -> Version -> Build -> Test Plan -> Test Cases -> Test Run.
Safe to re-run: everything is looked up before it is created.

    python seed/seed_demo.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from automation.kiwi import (  # noqa: E402
    BUILD,
    PLAN,
    PRODUCT,
    VERSION,
    connect,
    current_username,
    first,
    get_or_create,
)

CASES = [
    {
        "summary": "Login with valid credentials returns a session token",
        "priority": "P1",
        "script": "test_login_with_valid_credentials_returns_token",
        "text": (
            "**Preconditions:** an active user with a password younger than 90 days.\n\n"
            "1. Submit the username and the correct password.\n"
            "**Expected:** a session token is returned and the failed-attempt "
            "counter is reset to zero."
        ),
    },
    {
        "summary": "Login with a wrong password is rejected",
        "priority": "P1",
        "script": "test_login_with_wrong_password_is_rejected",
        "text": (
            "**Preconditions:** an active user.\n\n"
            "1. Submit the username with an incorrect password.\n"
            "**Expected:** authentication fails with 'invalid credentials' and the "
            "failed-attempt counter increases by one."
        ),
    },
    {
        "summary": "Account is locked after 3 consecutive failed attempts",
        "priority": "P1",
        "script": "test_login_is_blocked_after_max_failed_attempts",
        "text": (
            "**Preconditions:** a user with 3 recorded failed attempts.\n\n"
            "1. Submit the username with the correct password.\n"
            "**Expected:** authentication fails with 'account is locked'."
        ),
    },
    {
        "summary": "A disabled account cannot log in",
        "priority": "P2",
        "script": "test_login_with_disabled_account_is_rejected",
        "text": (
            "**Preconditions:** a user whose account has been deactivated.\n\n"
            "1. Submit valid credentials.\n"
            "**Expected:** authentication fails with 'account is disabled'."
        ),
    },
    {
        "summary": "Login with an expired password is rejected",
        "priority": "P1",
        "script": "test_login_with_expired_password_is_rejected",
        "text": (
            "**Preconditions:** an active user whose password is older than the "
            "90-day maximum age.\n\n"
            "1. Submit valid credentials.\n"
            "**Expected:** authentication fails with 'password expired' and the "
            "user is redirected to the password change screen."
        ),
    },
    {
        "summary": "Password reset email is delivered within 2 minutes",
        "priority": "P2",
        "script": "",  # manual case: shows manual and automated coverage side by side
        "text": (
            "**Preconditions:** a registered user with a verified email address.\n\n"
            "1. Request a password reset from the login screen.\n"
            "2. Check the inbox of the registered address.\n"
            "**Expected:** a reset email with a single-use link arrives within 2 minutes."
        ),
    },
]


def main() -> None:
    rpc = connect()
    print("Connected to Kiwi TCMS")

    # A fresh Kiwi instance has no classifications, so create ours.
    classification = get_or_create(
        rpc,
        "Classification",
        {"name": "Web"},
        {"name": "Web"},
        "classification 'Web'",
    )
    product = get_or_create(
        rpc,
        "Product",
        {"name": PRODUCT},
        {
            "name": PRODUCT,
            "description": "Demo web shop used for the test management demo",
            "classification": classification["id"],
        },
        f"product '{PRODUCT}'",
    )

    version = get_or_create(
        rpc,
        "Version",
        {"product": product["id"], "value": VERSION},
        {"product": product["id"], "value": VERSION},
        f"version {VERSION}",
    )

    build = get_or_create(
        rpc,
        "Build",
        {"version": version["id"], "name": BUILD},
        {"version": version["id"], "name": BUILD},
        f"build {BUILD}",
    )

    plan_type = first(rpc.PlanType.filter({"name": "Regression"}), "plan types")
    plan = get_or_create(
        rpc,
        "TestPlan",
        {"name": PLAN},
        {
            "name": PLAN,
            "product": product["id"],
            "product_version": version["id"],
            "type": plan_type["id"],
            "is_active": True,
            "text": (
                "Scope: authentication and session rules of the demo shop.\n"
                "Exit criteria: every P1 case PASSED on the release build, "
                "no open blocker defects."
            ),
        },
        f"test plan '{PLAN}'",
    )

    category = first(rpc.Category.filter({"product": product["id"]}), "categories")
    confirmed = first(
        rpc.TestCaseStatus.filter({"name": "CONFIRMED"}), "case statuses"
    )
    priorities = {p["value"]: p["id"] for p in rpc.Priority.filter({})}

    for spec in CASES:
        existing = rpc.TestCase.filter({"summary": spec["summary"]})
        if existing:
            print(f"  = case '{spec['summary'][:40]}...' already exists")
            case = existing[0]
        else:
            case = rpc.TestCase.create(
                {
                    "summary": spec["summary"],
                    "product": product["id"],
                    "category": category["id"],
                    "priority": priorities[spec["priority"]],
                    "case_status": confirmed["id"],
                    "is_automated": bool(spec["script"]),
                    "script": spec["script"],
                    "text": spec["text"],
                }
            )
            print(f"  + created case '{spec['summary'][:40]}...'")
        rpc.TestPlan.add_case(plan["id"], case["id"])

    manager = first(
        rpc.User.filter({"username": current_username()}), "users"
    )
    runs = rpc.TestRun.filter({"summary": f"Manual regression - {BUILD}"})
    if runs:
        print("  = test run already exists")
    else:
        run = rpc.TestRun.create(
            {
                "summary": f"Manual regression - {BUILD}",
                "plan": plan["id"],
                "build": build["id"],
                "manager": manager["id"],
                "default_tester": manager["id"],
            }
        )
        for case in rpc.TestCase.filter({"plan": plan["id"]}):
            rpc.TestRun.add_case(run["id"], case["id"])
        print(f"  + created test run (id={run['id']}) with all executions IDLE")

    print("\nDone. Open https://localhost:8443 and go to Testing -> Test Runs.")


if __name__ == "__main__":
    main()
