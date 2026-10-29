#!/usr/bin/env python3
"""
Confirms CA1 findings F2 (insecure session token storage) and M3 (CSRF via
missing SameSite) by inspecting the actual Set-Cookie / auth header
behaviour on login, rather than relying on config review alone.

Usage:
    python scripts/check_cookie_flags.py --base-url http://localhost:3000 \
        --email victim@juice-sh.op --password changeme
"""
import argparse
import json
import sys

import requests


def get_set_cookie_headers(resp: requests.Response) -> list:
    """Return every Set-Cookie header (requests merges duplicates, so use raw)."""
    headers = []
    if resp.raw is not None and hasattr(resp.raw.headers, "getlist"):
        headers = resp.raw.headers.getlist("Set-Cookie")
    if not headers and "Set-Cookie" in resp.headers:
        headers = [resp.headers["Set-Cookie"]]
    return headers


def check_cookie_flags(base_url: str, email: str, password: str, timeout: float = 10.0) -> dict:
    url = f"{base_url.rstrip('/')}/rest/user/login"
    try:
        resp = requests.post(url, json={"email": email, "password": password}, timeout=timeout)
    except requests.RequestException as exc:
        return {"check": "F2_M3_cookie_flags", "status": "ERROR", "detail": str(exc)}

    # A failed login says nothing about cookie/token handling, so don't report
    # it as a finding.
    if resp.status_code != 200:
        return {
            "check": "F2_M3_cookie_flags",
            "status": "ERROR (login failed)",
            "http_status": resp.status_code,
            "detail": "Login rejected; cookie/token results would be meaningless. "
                      "Check the email/password and that the account is registered.",
        }

    set_cookie_headers = get_set_cookie_headers(resp)

    flags = {"HttpOnly": False, "Secure": False, "SameSite": None}
    for header in set_cookie_headers:
        lower = header.lower()
        if "httponly" in lower:
            flags["HttpOnly"] = True
        if "secure" in lower:
            flags["Secure"] = True
        if "samesite=strict" in lower:
            flags["SameSite"] = "Strict"
        elif "samesite=lax" in lower:
            flags["SameSite"] = "Lax"
        elif "samesite=none" in lower:
            flags["SameSite"] = "None"

    # Juice Shop returns the JWT in the response body rather than a cookie by
    # default; note that explicitly rather than silently treating it as safe.
    uses_body_token = False
    try:
        body = resp.json()
        uses_body_token = bool(body.get("authentication", {}).get("token")) and not set_cookie_headers
    except (ValueError, AttributeError):
        pass

    vulnerable = (not flags["HttpOnly"]) or (not flags["Secure"]) or (flags["SameSite"] in (None, "None"))
    status = "FAIL (missing protective flags)" if (vulnerable or uses_body_token) else "PASS"

    return {
        "check": "F2_M3_cookie_flags",
        "status": status,
        "http_status": resp.status_code,
        "set_cookie_headers_seen": set_cookie_headers,
        "flags": flags,
        "token_returned_in_body_not_cookie": uses_body_token,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3000")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    result = check_cookie_flags(args.base_url, args.email, args.password)
    print(json.dumps(result, indent=2))

    if result["status"] == "PASS":
        sys.exit(0)
    elif result["status"].startswith("ERROR"):
        sys.exit(2)  # distinguish a broken test from a genuine finding
    else:
        sys.exit(1)