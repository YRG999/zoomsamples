import requests
import os
from dotenv import load_dotenv

# Enter access token
load_dotenv()
access_token = os.getenv("ZOOM_ACCESSTOKEN")

# Set up the base URL for API requests
base_url = "https://api.zoom.us/v2"

# Set up the headers with the access token
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Define a function to get a list of all meetings
def get_meetings():
    url = f"{base_url}/users/me/meetings"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        meetings = response.json()["meetings"]
        return meetings
    else:
        return None

# Define a function to get a list of all participants in a meeting
def get_participants(meeting_id):
    url = f"{base_url}/report/meetings/{meeting_id}/participants"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        participants = response.json()["participants"]
        return participants
    else:
        return None

# Get a list of all meetings
meetings = get_meetings()

# For each meeting, get a list of all participants and print their names
for meeting in meetings:
    participants = get_participants(meeting["id"])
    if participants is not None:
        print(f"Participants in {meeting['topic']} ({meeting['id']}):")
        for participant in participants:
            print(participant["name"])
    else:
        print(f"Unable to retrieve participants for {meeting['topic']} ({meeting['id']})")
