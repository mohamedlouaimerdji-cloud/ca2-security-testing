#!/usr/bin/env python3
"""
Access control test harness (horizontal and vertical privilege checks).

This is the project's primary automation artefact (brief requirement 3): it
takes two low-privilege user sessions (and optionally the admin session
obtained via the F1 bypass) and checks whether one account can read or
modify another account's resources, or reach admin-only endpoints.

This script performs read-only GET checks by default. Any check that would
modify data is marked `mutates: True` in CHECKS and is skipped unless
--allow-mutate is passed explicitly, to avoid damaging the single shared
database used across this project's testing.

Usage:
    python scripts/access_control_test.py \
        --base-url http://127.0.0.1:3000 \
        --token-a <user_a_jwt> --user-a-id 2 \
        --token-b <user_b_jwt> --user-b-id 3 \
        [--admin-token <admin_jwt>]
"""
import argparse
import json
import sys

import requests

CHECKS = []


def check(name, mutates=False):
    def decorator(fn):
        CHECKS.append({"name": name, "fn": fn, "mutates": mutates})
        return fn
    return decorator


@check("horizontal_basket_read")
def horizontal_basket_read(base_url, token_a, user_a_id, token_b, user_b_id, admin_token, allow_mutate):
    """Can user A read user B's basket by guessing/incrementing the ID?"""
    headers_a = {"Authorization": f"Bearer {token_a}"}
    results = []
    # Try a small window of basket IDs around user A's own, looking for
    # another user's basket content returned without ownership checks.
    for basket_id in range(1, 6):
        resp = requests.get(f"{base_url}/rest/basket/{basket_id}", headers=headers_a, timeout=10)
        results.append({"basket_id": basket_id, "status": resp.status_code})
    leaked = [r for r in results if r["status"] == 200]
    return {
        "pass": len(leaked) <= 1,  # only the caller's own basket should return 200
        "detail": results,
    }


@check("vertical_admin_endpoint")
def vertical_admin_endpoint(base_url, token_a, user_a_id, token_b, user_b_id, admin_token, allow_mutate):
    """Can a non-admin user reach an admin-only endpoint (e.g. /api/Users)?"""
    headers_a = {"Authorization": f"Bearer {token_a}"}
    resp = requests.get(f"{base_url}/api/Users", headers=headers_a, timeout=10)
    return {
        "pass": resp.status_code in (401, 403),
        "detail": {"status": resp.status_code},
    }


@check("horizontal_profile_read")
def horizontal_profile_read(base_url, token_a, user_a_id, token_b, user_b_id, admin_token, allow_mutate):
    """Can user A read user B's profile/order data directly by ID?"""
    headers_a = {"Authorization": f"Bearer {token_a}"}
    resp = requests.get(f"{base_url}/rest/user/{user_b_id}", headers=headers_a, timeout=10)
    return {
        "pass": resp.status_code in (401, 403, 404),
        "detail": {"status": resp.status_code},
    }


def run(base_url, token_a, user_a_id, token_b, user_b_id, admin_token, allow_mutate):
    report = {"base_url": base_url, "results": []}
    for c in CHECKS:
        if c["mutates"] and not allow_mutate:
            report["results"].append({"name": c["name"], "status": "SKIPPED (mutating, not allowed)"})
            continue
        try:
            outcome = c["fn"](base_url, token_a, user_a_id, token_b, user_b_id, admin_token, allow_mutate)
            status = "PASS" if outcome["pass"] else "FAIL"
            report["results"].append({"name": c["name"], "status": status, "detail": outcome["detail"]})
        except requests.RequestException as exc:
            report["results"].append({"name": c["name"], "status": "ERROR", "detail": str(exc)})
    report["overall"] = "PASS" if all(r["status"] == "PASS" for r in report["results"] if r["status"] != "SKIPPED") else "FAIL"
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3000")
    parser.add_argument("--token-a", required=True)
    parser.add_argument("--user-a-id", required=True)
    parser.add_argument("--token-b", required=True)
    parser.add_argument("--user-b-id", required=True)
    parser.add_argument("--admin-token", default=None)
    parser.add_argument("--allow-mutate", action="store_true")
    args = parser.parse_args()

    report = run(
        args.base_url, args.token_a, args.user_a_id, args.token_b, args.user_b_id,
        args.admin_token, args.allow_mutate,
    )
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["overall"] == "PASS" else 1)
