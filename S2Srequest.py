import requests
import os
from dotenv import load_dotenv

# Enter access token. Can also be used for Video SDK JWT Token
load_dotenv()
access_token = os.getenv("ZOOM_ACCESSTOKEN")

# Set up the API endpoint to query (this gets your user info)
endpoint = "https://api.zoom.us/v2/users/me"

# Get Video SDK settings
# endpoint = "https://api.zoom.us/v2/accounts/me/settings"

# Set up the headers with the access token
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {access_token}"
}

# Send a GET request to the endpoint with the headers
response = requests.get(endpoint, headers=headers)

# Check the response status code
if response.status_code == 200:
    # The request was successful, so print out the user data
    user_data = response.json()
    print(f"User data: {user_data}")
else:
    # The request was not successful, so print out an error message
    print(f"Error: {response.status_code} - {response.text}")
