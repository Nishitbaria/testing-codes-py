#!/usr/bin/env python3
"""
Extract top 20 most liked and viewed post IDs and update MOST_LIKE_AND_VIEWD_POST_IDS in post_ids.py
"""

import re
import requests


def fetch_published_assets(auth_token):
    """Fetch all published assets from the API"""
    url = "https://imagine.vyro.ai/v1/user/nishitbariya/published?limit=3000"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,gu;q=0.6",
        "authorization": f"Bearer {auth_token}",
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
        response.raise_for_status()
        data = response.json()

        assets = data.get("assets", [])
        return assets
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return []


def get_top_liked_and_viewed(assets, top_n=20):
    """Get top N assets by likes (favorites) only"""
    # Sort by favorites (likes) only - descending
    sorted_assets = sorted(assets, key=lambda x: x.get("favorites", 0), reverse=True)

    # Get top N
    top_assets = sorted_assets[:top_n]

    # Extract UUIDs
    top_uuids = [asset["uuid"] for asset in top_assets if "uuid" in asset]

    return top_uuids, top_assets


def update_most_liked_viewed_ids(top_uuids, post_ids_file="post_ids.py"):
    """Update MOST_LIKE_AND_VIEWD_POST_IDS array in post_ids.py"""
    try:
        with open(post_ids_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Create the new MOST_LIKE_AND_VIEWD_POST_IDS array string
        most_liked_str = "MOST_LIKE_AND_VIEWD_POST_IDS = [\n"
        for uuid in top_uuids:
            most_liked_str += f'    "{uuid}",\n'
        most_liked_str += "]"

        # Replace the old MOST_LIKE_AND_VIEWD_POST_IDS array with the new one
        pattern = r"MOST_LIKE_AND_VIEWD_POST_IDS\s*=\s*\[[\s\S]*?\]"
        new_content = re.sub(pattern, most_liked_str, content)

        # Write back to post_ids.py
        with open(post_ids_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        return len(top_uuids)
    except Exception as e:
        print(f"❌ Error updating post_ids.py: {e}")
        return 0


def main():
    # Auth token
    AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJpbnRlZ3JpdHlDaGVjayI6ZmFsc2UsImJhc2VVcmwiOiIiLCJwcm9kdWN0VmFsaWRGb3IiOiJJTUFHSU5FIiwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTc2MzA0MTQ1MiwiZXhwIjoxNzYzMDYzMDUyLCJzdWIiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJqdGkiOiJmOWQyMzJkYi00Yzk2LTRkZDAtOGE2MS02OWNlZWNiZTgxZjAifQ.1uHmG1pPlbUXhZbLF8701stXU5djGb2hhn-f6Dk22TA"

    print("🌐 Fetching published assets from API...")

    # Fetch assets
    assets = fetch_published_assets(AUTH_TOKEN)

    if not assets:
        print("❌ No assets found from API")
        return

    print(f"✅ Found {len(assets)} total assets")

    # Get top 50 by likes only
    print(f"\n📊 Analyzing most liked posts (favorites only)...")
    top_uuids, top_assets = get_top_liked_and_viewed(assets, top_n=50)

    print(f"✅ Found top {len(top_uuids)} most liked posts")

    # Display top posts
    print(f"\n🏆 TOP 50 MOST LIKED POSTS:")
    print("-" * 80)
    for i, asset in enumerate(top_assets, 1):
        title = asset.get("title", "Untitled")
        favorites = asset.get("favorites", 0)
        views = asset.get("views", 0)
        uuid = asset.get("uuid", "N/A")

        print(
            f"{i:2d}. {title[:40]:<40} | ❤️  Likes: {favorites:4d} | 👁️  Views: {views:5d}"
        )
        print(f"    UUID: {uuid}")
        print("-" * 80)

    # Update post_ids.py
    print(f"\n📝 Updating MOST_LIKE_AND_VIEWD_POST_IDS in post_ids.py...")
    count = update_most_liked_viewed_ids(top_uuids, "post_ids.py")

    print(
        f"✅ Successfully updated! Added {count} top post IDs to MOST_LIKE_AND_VIEWD_POST_IDS"
    )


if __name__ == "__main__":
    main()
