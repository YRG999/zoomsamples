import requests
import base64
import os
from dotenv import load_dotenv

# Set up the API credentials
load_dotenv()
client_id = os.getenv("ZOOM_CLIENTID")
client_secret = os.getenv("ZOOM_CLIENTSECRET")
account_id = os.getenv("ZOOM_ACCOUNTID")

# Encode the client ID and secret in base64 format
auth_string = f"{client_id}:{client_secret}"
auth_bytes = auth_string.encode("ascii")
base64_bytes = base64.b64encode(auth_bytes)
base64_string = base64_bytes.decode("ascii")

# Set up the headers for API requests
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {base64_string}"
}

# Set up the data for the token API request
data = {
    "grant_type": "account_credentials",
    "account_id": account_id
}

# Send a POST request to the token API to get an access token
url = "https://zoom.us/oauth/token"
response = requests.post(url, data=data, headers=headers)

# Parse the JSON response and extract the access token
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"Access token: {token}")
else:
    print("Error getting access token")
