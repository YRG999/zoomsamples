# access_request.py
# --- NEED TO TEST ---
# Usage: OAuth 2.0 token management for Zoom API

import requests
import base64
import os
import urllib.parse
from credentials import get_credentials
from dotenv import set_key

# Load environment variables path
env_path = os.path.join(os.path.dirname(__file__), '.env')

client_id = get_credentials('CLIENT_ID')
client_secret = get_credentials('CLIENT_SECRET')
redirect_uri = get_credentials('REDIRECT_URI')
access_token = get_credentials('ACCESS_TOKEN')
refresh_token = get_credentials('REFRESH_TOKEN')


# --- Utility: Encode client credentials ---
def get_basic_auth_header(client_id, client_secret):
    # Validate that client_id and client_secret do not contain problematic characters
    for value, name in [(client_id, "client_id"), (client_secret, "client_secret")]:
        if any(c in value for c in [":", "\x00", "\n", "\r"]):
            raise ValueError(f"{name} contains invalid character (colon, null byte, newline, or carriage return)")
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")
    return {"Authorization": f"Basic {encoded_credentials}"}


# -- Step 1: Generate Authorization URL ---
def generate_authorization_url(client_id, redirect_uri, scope="user:read"):
    authorization_endpoint = "https://zoom.us/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        # "scope": scope  # Zoom does not require scope parameter in authorization URL
    }
    auth_url = f"{authorization_endpoint}?{urllib.parse.urlencode(params)}"
    return auth_url


# -- Step 2: Exchange Authorization Code for Tokens ---
def exchange_code_for_tokens(client_id, client_secret, redirect_uri, authorization_code):
    token_endpoint = "https://zoom.us/oauth/token"
    headers = get_basic_auth_header(client_id, client_secret)
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    response = None
    try:
        response = requests.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
    except requests.HTTPError as exc:
        error_message = (
            f"Failed to exchange authorization code: {response.status_code} - {response.text}"
            if response is not None
            else "Failed to exchange authorization code: no response received."
        )
        raise requests.HTTPError(error_message) from exc
    except requests.RequestException as exc:
        raise requests.RequestException(f"Network error during token exchange: {exc}") from exc
    print("Authorization code exchanged successfully.")
    tokens = response.json()
    
    # Save tokens to .env file
    set_key(env_path, "ACCESS_TOKEN", tokens["access_token"])
    set_key(env_path, "REFRESH_TOKEN", tokens["refresh_token"])
    
    return tokens


# -- Step 3: Refresh Access Token ---
def refresh_access_token(client_id, client_secret, refresh_token):
    token_endpoint = "https://zoom.us/oauth/token"
    headers = get_basic_auth_header(client_id, client_secret)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = None
    try:
        response = requests.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
    except requests.HTTPError as exc:
        error_message = (
            f"Failed to refresh access token: {response.status_code} - {response.text}"
            if response is not None
            else "Failed to refresh access token: no response received."
        )
        raise requests.HTTPError(error_message) from exc
    except requests.RequestException as exc:
        raise requests.RequestException(f"Network error during token refresh: {exc}") from exc
    print("Access token refreshed successfully.")
    tokens = response.json()
    
    # Update tokens in .env file
    set_key(env_path, "ACCESS_TOKEN", tokens["access_token"])
    set_key(env_path, "REFRESH_TOKEN", tokens["refresh_token"])
    
    return tokens

# --- Main workflow ---
if __name__ == "__main__":
    from request_handler import get_user_info

    if not access_token or not refresh_token:
        print("No access or refresh token found. Please authorize the application first.")
        auth_url = generate_authorization_url(client_id, redirect_uri)
        print("Go to the following URL to authorize the application:")
        print(auth_url)

        authorization_code = input("Enter the authorization code from the URL: ")
        tokens = exchange_code_for_tokens(client_id, client_secret, redirect_uri, authorization_code)
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

    user_info = get_user_info()
    print("\nUser data:", user_info)
