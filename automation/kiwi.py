"""Shared connection helpers for the Kiwi TCMS RPC API (tcms-api 15.0).

Credentials come from environment variables (see .env.example). If none are
set, tcms-api falls back to its own ~/.tcms.conf file.
"""

import configparser
import os
import pathlib
import sys

CONFIG_PATH = pathlib.Path.home() / ".tcms.conf"

# The demo fixture. Keep these in sync with seed/seed_demo.py and the README.
PRODUCT = "Solinal Demo Shop"
VERSION = "1.2"
BUILD = "build-45"
PLAN = "Regression - Authentication 1.2"


def connect():
    """Return the RPC proxy, e.g. rpc.Product.filter({})."""
    if os.environ.get("TCMS_INSECURE_SSL"):
        # The Kiwi container ships a self-signed certificate for localhost.
        # Only ever acceptable against your own local demo instance.
        import ssl  # noqa: PLC0415

        ssl._create_default_https_context = ssl._create_unverified_context  # noqa: SLF001

    from tcms_api import TCMS  # noqa: PLC0415 - keep the import cost inside the call

    url = os.environ.get("TCMS_API_URL")
    username = os.environ.get("TCMS_USERNAME")
    password = os.environ.get("TCMS_PASSWORD")

    if url and username and password:
        return TCMS(url, username, password).exec

    if not CONFIG_PATH.exists():
        sys.exit(
            "No credentials. Export the variables from .env.example:\n"
            "  export TCMS_API_URL=http://localhost:8080/xml-rpc/\n"
            "  export TCMS_USERNAME=admin\n"
            "  export TCMS_PASSWORD=your-password"
        )
    return TCMS().exec


def current_username() -> str:
    if os.environ.get("TCMS_USERNAME"):
        return os.environ["TCMS_USERNAME"]
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)
    return parser["tcms"]["username"]


def first(rows, what: str):
    """Return the first row of an RPC filter() result or fail loudly."""
    if not rows:
        sys.exit(f"Kiwi TCMS returned no {what}. Is the instance initialised?")
    return rows[0]


def get_or_create(rpc, entity: str, lookup: dict, create: dict, label: str):
    """Idempotent create: the seed script can be re-run without duplicating data."""
    existing = getattr(rpc, entity).filter(lookup)
    if existing:
        print(f"  = {label} already exists (id={existing[0]['id']})")
        return existing[0]
    created = getattr(rpc, entity).create(create)
    print(f"  + created {label} (id={created['id']})")
    return created
