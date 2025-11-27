import requests
from requests.exceptions import RequestException
import time
import random
from post_ids import MOST_LIKE_AND_VIEWD_POST_IDS, AUTH_ID

# ------------------------------
# CONFIG
# ------------------------------

AUTH_TOKEN = AUTH_ID  # Using AUTH_ID from post_ids.py

BASE_URL = "https://imagine.vyro.ai/v1/assets/{}/favorite"

# Number of top posts to like (max 10)
NUM_TO_LIKE = 45

# ------------------------------
# SCRIPT START
# ------------------------------


def send_favorite_request(asset_id, token):
    """Send POST request to favorite/like a single asset."""
    url = BASE_URL.format(asset_id)

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,gu;q=0.6",
        "authorization": f"Bearer {token}",
        "content-length": "0",
        "dnt": "1",
        "origin": "https://www.imagine.art",
        "priority": "u=1, i",
        "referer": "https://www.imagine.art/",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    }

    payload = {}

    try:
        response = requests.post(url, headers=headers, data=payload)
        return response.status_code, response.text
    except RequestException as e:
        return None, str(e)


def main():
    if not AUTH_TOKEN:
        print(
            "❌ ERROR: AUTH_ID is empty in post_ids.py. Please set your Bearer token."
        )
        return

    if not MOST_LIKE_AND_VIEWD_POST_IDS:
        print("❌ ERROR: MOST_LIKE_AND_VIEWD_POST_IDS is empty.")
        print("💡 Run 'python3 extract_top_posts.py' first to populate top posts.")
        return

    success = 0
    failed = 0

    print("\n❤️  Starting favorite/like script for TOP posts...")
    print(f"📊 Total top posts available: {len(MOST_LIKE_AND_VIEWD_POST_IDS)}")
    print(f"🎯 Number of posts to like: {NUM_TO_LIKE}")
    print("--------------------------------------")

    # Get top N posts to like
    posts_to_like = MOST_LIKE_AND_VIEWD_POST_IDS[:NUM_TO_LIKE]

    for index, asset_id in enumerate(posts_to_like, start=1):
        print(f"\n▶️ {index}. Sending like request for Asset ID: {asset_id}")

        status, result = send_favorite_request(asset_id, AUTH_TOKEN)

        if status == 200:
            print(f"   ✅ SUCCESS (200 OK) - Post liked!")
            success += 1
        elif status == 201:
            print(f"   ✅ SUCCESS (201 Created) - Post liked!")
            success += 1
        else:
            print(f"   ❌ FAILED (Status: {status})")
            print(f"   Response: {result[:200]}")  # print first 200 chars
            failed += 1

        # Random delay between 1-6 seconds
        if index < len(posts_to_like):  # Don't delay after the last request
            delay = random.uniform(1, 6)
            print(f"   ⏳ Waiting {delay:.2f} seconds...")
            # time.sleep(delay)

    print("\n--------------------------------------")
    print("📊 SUMMARY")
    print(f"   ✔ Successful likes : {success}")
    print(f"   ✖ Failed likes     : {failed}")
    print("--------------------------------------\n")


if __name__ == "__main__":
    main()
