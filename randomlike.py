import requests
from requests.exceptions import RequestException
import time
import random
from post_ids import POST_IDS, AUTH_ID

# ------------------------------
# CONFIG
# ------------------------------

AUTH_TOKEN = AUTH_ID  # Using AUTH_ID from post_ids.py

BASE_URL = "https://imagine.vyro.ai/v1/assets/{}/favorite"

# Number of random posts to like (change this as needed)
NUM_LIKES = 500

# ------------------------------
# SCRIPT START
# ------------------------------


def get_asset_details(asset_id, token):
    """Fetch asset details to get title and other info."""
    url = f"https://imagine.vyro.ai/v1/feed/asset/{asset_id}"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,gu;q=0.6",
        "authorization": f"Bearer {token}",
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

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return (
                data.get("title", "Untitled"),
                data.get("favorites", 0),
                data.get("views", 0),
            )
        return "Unknown", 0, 0
    except RequestException:
        return "Unknown", 0, 0


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

    if not POST_IDS:
        print("❌ ERROR: POST_IDS is empty. Add some asset IDs first.")
        return

    success = 0
    failed = 0

    print("\n❤️  Starting random like/favorite script...")
    print(f"📊 Total available assets: {len(POST_IDS)}")
    print(f"🎯 Number of random posts to like: {NUM_LIKES}")
    print("--------------------------------------")

    # Select random asset IDs
    num_to_select = min(NUM_LIKES, len(POST_IDS))
    random_assets = random.sample(POST_IDS, num_to_select)

    for index, asset_id in enumerate(random_assets, start=1):
        # Fetch asset details first to get title
        title, favorites, views = get_asset_details(asset_id, AUTH_TOKEN)

        print(f"\n▶️  {index}. Liking post: '{title}'")
        print(f"   UUID: {asset_id}")
        print(f"   Stats: ❤️  {favorites} likes | 👁️  {views} views")

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
        if index < num_to_select:  # Don't delay after the last request
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
