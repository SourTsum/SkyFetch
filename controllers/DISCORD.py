import os
import requests
from dotenv import load_dotenv

load_dotenv("data/hidden.env")

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL not found in .env file")

def send_error(message):
    embed = {
        "embeds": [{
            "title": "[GATHER]: Error",
            "description": message,
            "color": 16711680  # Red
        }]
    }

    response = requests.post(WEBHOOK_URL, json=embed)

    if response.status_code != 204:
        print(f"Failed to send error: {response.status_code}, {response.text}")
    else:
        print("[DISCORD]: Successfully sent error to Discord")


def send_gather_start(current_datetime, start_stats):
    embed = {
        "embeds": [{
            "title": "🟢 [GATHER]: Started",
            "color": 3066993,  # Green
            "fields": [
                {
                    "name": "Date",
                    "value": current_datetime,
                    "inline": False
                },
                {
                    "name": "Last Ran",
                    "value": start_stats.get("last_ran", "N/A"),
                    "inline": True
                },
                {
                    "name": "Seconds / Call",
                    "value": str(start_stats.get("seconds_per_call", "N/A")),
                    "inline": True
                }
            ]
        }]
    }

    response = requests.post(WEBHOOK_URL, json=embed)

    if response.status_code != 204:
        print(f"Failed to send gather_stats: {response.status_code}, {response.text}")

def send_gather_img():
    with open("output/SkyFetch.png", "rb") as f:
        files = {
            "file": (os.path.basename("output/SkyFetch.png"), f, "image/png")
        }

        response = requests.post(WEBHOOK_URL, files=files)

        if response.status_code != 200:
            print(f"Failed to upload image: {response.status_code}, {response.text}")
