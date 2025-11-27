import requests
from requests.exceptions import RequestException
import time
import random
from post_ids import POST_IDS, AUTH_ID

# ------------------------------
# CONFIG
# ------------------------------

AUTH_TOKEN = AUTH_ID  # Using AUTH_ID from post_ids.py

BASE_URL = "https://imagine.vyro.ai/v1/assets/{}/stats"

# ------------------------------
# SCRIPT START
# ------------------------------


def send_view_request(asset_id, token):
    """Send PUT request to increment view count for a single asset."""
    url = BASE_URL.format(asset_id)

    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123",
    }

    body = (
        "------WebKitFormBoundaryABC123\r\n"
        'Content-Disposition: form-data; name="viewed"\r\n\r\n'
        "true\r\n"
        "------WebKitFormBoundaryABC123--\r\n"
    )

    try:
        response = requests.put(url, headers=headers, data=body)
        return response.status_code, response.text
    except RequestException as e:
        return None, str(e)


def main():
    if not AUTH_TOKEN:
        print("❌ ERROR: AUTH_TOKEN is empty. Please paste your token in the script.")
        return

    success = 0
    failed = 0

    print("\n🚀 Starting view-increment script...")
    print("--------------------------------------")

    for index, asset_id in enumerate(POST_IDS, start=1):
        print(f"\n▶️ {index}. Sending request for Asset ID: {asset_id}")

        status, result = send_view_request(asset_id, AUTH_TOKEN)

        if status == 200:
            print(f"   ✅ SUCCESS (200 OK)")
            success += 1
        else:
            print(f"   ❌ FAILED (Status: {status})")
            print(f"   Response: {result[:200]}")  # print first 200 chars
            failed += 1

        # Random delay between 10-20 seconds
        if index < len(POST_IDS):  # Don't delay after the last request
            delay = random.uniform(4, 5)
            print(f"   ⏳ Waiting {delay:.2f} seconds...")
            time.sleep(delay)

    print("\n--------------------------------------")
    print("📊 SUMMARY")
    print(f"   ✔ Successful requests : {success}")
    print(f"   ✖ Failed requests     : {failed}")
    print("--------------------------------------\n")


if __name__ == "__main__":
    main()
