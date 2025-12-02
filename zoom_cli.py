# !/usr/bin/env python3
# zoom_cli.py
# --- NEED TO TEST ---
# Usage: Command-line interface for Zoom API authorization and requests

import json
import sys

import requests

import access_request
from request_handler import get_user_info, make_request


def _require_credentials():
    missing = [
        name
        for name, value in (
            ("CLIENT_ID", access_request.client_id),
            ("CLIENT_SECRET", access_request.client_secret),
            ("REDIRECT_URI", access_request.redirect_uri),
        )
        if not value
    ]
    if missing:
        print(f"Missing environment values: {', '.join(missing)}.")
        return False
    return True


def authorize():
    if not _require_credentials():
        return
    auth_url = access_request.generate_authorization_url(
        access_request.client_id,
        access_request.redirect_uri,
    )
    print(f"\nVisit:\n{auth_url}\n")
    authorization_code = input("Enter authorization code: ").strip()
    if not authorization_code:
        print("Authorization code required.")
        return
    try:
        tokens = access_request.exchange_code_for_tokens(
            access_request.client_id,
            access_request.client_secret,
            access_request.redirect_uri,
            authorization_code,
        )
    except requests.RequestException as exc:
        print(f"Authorization failed: {exc}")
        return
    access_request.access_token = tokens["access_token"]
    access_request.refresh_token = tokens["refresh_token"]
    print("Authorized successfully.")


def refresh_tokens():
    if not access_request.refresh_token:
        print("No refresh token available. Authorize first.")
        return
    try:
        tokens = access_request.refresh_access_token(
            access_request.client_id,
            access_request.client_secret,
            access_request.refresh_token,
        )
    except requests.RequestException as exc:
        print(f"Token refresh failed: {exc}")
        return
    access_request.access_token = tokens["access_token"]
    access_request.refresh_token = tokens["refresh_token"]
    print("Tokens refreshed.")


def show_user_info():
    try:
        data = get_user_info()
    except requests.RequestException as exc:
        print(f"User info request failed: {exc}")
        return
    print(json.dumps(data, indent=2))


def make_custom_request():
    method = input("HTTP method (default GET): ").strip().upper() or "GET"
    endpoint = input("Endpoint URL: ").strip()
    if not endpoint:
        print("Endpoint is required.")
        return
    raw_params = input("Query params as JSON (blank for none): ").strip()
    params = None
    if raw_params:
        try:
            params = json.loads(raw_params)
            if not isinstance(params, dict):
                raise ValueError
        except ValueError:
            print("Params must be a JSON object.")
            return
    try:
        data = make_request(method=method, endpoint=endpoint, params=params)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return
    print(json.dumps(data, indent=2))


def main():
    actions = {
        "1": authorize,
        "2": show_user_info,
        "3": refresh_tokens,
        "4": make_custom_request,
        "0": lambda: sys.exit(0),
    }
    while True:
        print(
            "\nZoom CLI\n"
            "1. Authorize\n"
            "2. Get current user info\n"
            "3. Refresh tokens\n"
            "4. Custom request\n"
            "0. Exit"
        )
        choice = input("Select option: ").strip()
        action = actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        action()


if __name__ == "__main__":
    main()
