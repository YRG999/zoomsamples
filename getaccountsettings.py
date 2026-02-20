# getaccountsettings.py

# --- NEED TO TEST ---

from access_request import access_token, client_id, client_secret, refresh_token, refresh_access_token
import requests
import os
from credentials import get_credentials
from dotenv import set_key

# Load environment variables path
env_path = os.path.join(os.path.dirname(__file__), '.env')

account_id = get_credentials('ACCOUNT_ID')

# Ask user if ACCOUNT_ID is missing
if not account_id:
    account_id = input("Please enter your Zoom Account ID: ").strip()
    if account_id:
        # Save ACCOUNT_ID to .env file for future use
        set_key(env_path, 'ACCOUNT_ID', account_id)
        print(f"ACCOUNT_ID saved to {env_path}.")


# -- Get Account Settings --
def get_account_settings(account_id, option=None, custom_query_fields=None):
    """Fetch Zoom account settings for the given account_id."""
    global access_token, refresh_token
    endpoint = f"https://api.zoom.us/v2/accounts/{account_id}/settings"
    params = {}
    if option:
        params["option"] = option
    if custom_query_fields:
        params["custom_query_fields"] = custom_query_fields

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
    except requests.RequestException as exc:
        print(f"Network error while retrieving account settings: {exc}")
        return None

    if response.status_code == 401:
        print("Access token expired. Refreshing token...")
        refreshed_tokens = refresh_access_token(client_id, client_secret, refresh_token)
        if not refreshed_tokens:
            print("Failed to refresh access token.")
            return None
        access_token = refreshed_tokens["access_token"]
        refresh_token = refreshed_tokens["refresh_token"]
        return get_account_settings(account_id, option, custom_query_fields)

    if not response.ok:
        print(f"Failed to retrieve account settings: {response.status_code} - {response.text}")
        return None

    settings = response.json()
    print(f"Account settings for {account_id}: {settings}")
    return settings