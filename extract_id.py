#!/usr/bin/env python3
"""
Fetch UUIDs from API and add new ones to index.py POST_IDS array
"""

import re
import requests


def fetch_uuids_from_api(auth_token):
    """Fetch all UUIDs from the API"""
    url = "https://imagine.vyro.ai/v1/user/nishitbariya/published?limit=5000"

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

        # Extract UUIDs from assets
        assets = data.get("assets", [])
        uuids = []
        seen = {}

        for asset in assets:
            if "uuid" in asset:
                uuid = asset["uuid"]
                if uuid not in seen:
                    seen[uuid] = True
                    uuids.append(uuid)

        return uuids, len(assets)
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return [], 0


def get_existing_post_ids(post_ids_file="post_ids.py"):
    """Extract existing POST_IDS from post_ids.py"""
    try:
        with open(post_ids_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract POST_IDS array
        pattern = r"POST_IDS\s*=\s*\[([\s\S]*?)\]"
        match = re.search(pattern, content)

        if match:
            ids_content = match.group(1)
            # Extract all UUIDs
            uuid_pattern = r'"([a-f0-9\-]+)"'
            existing_ids = re.findall(uuid_pattern, ids_content)
            return set(existing_ids)

        return set()
    except FileNotFoundError:
        print(f"❌ File '{post_ids_file}' not found")
        return set()


def update_post_ids_file_with_new_ids(new_uuids, post_ids_file="post_ids.py"):
    """Add new UUIDs to POST_IDS array in post_ids.py"""
    try:
        with open(post_ids_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Get existing IDs
        existing_ids = get_existing_post_ids(post_ids_file)

        # Combine existing + new (maintaining order)
        all_ids = list(existing_ids) + new_uuids

        # Create the new POST_IDS array string
        post_ids_str = "POST_IDS = [\n"
        for uuid in all_ids:
            post_ids_str += f'    "{uuid}",\n'
        post_ids_str += "]"

        # Replace the old POST_IDS array with the new one
        pattern = r"POST_IDS\s*=\s*\[[\s\S]*?\]"
        new_content = re.sub(pattern, post_ids_str, content)

        # Write back to post_ids.py
        with open(post_ids_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        return len(all_ids)
    except Exception as e:
        print(f"❌ Error updating post_ids.py: {e}")
        return 0


def main():
    # Auth token from index.py
    AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJpbnRlZ3JpdHlDaGVjayI6ZmFsc2UsImJhc2VVcmwiOiIiLCJwcm9kdWN0VmFsaWRGb3IiOiJJTUFHSU5FIiwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTc2MzA0MTQ1MiwiZXhwIjoxNzYzMDYzMDUyLCJzdWIiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJqdGkiOiJmOWQyMzJkYi00Yzk2LTRkZDAtOGE2MS02OWNlZWNiZTgxZjAifQ.1uHmG1pPlbUXhZbLF8701stXU5djGb2hhn-f6Dk22TA"

    print("🌐 Fetching published assets from API...")

    # Fetch UUIDs from API
    api_uuids, total_assets = fetch_uuids_from_api(AUTH_TOKEN)

    if not api_uuids:
        print("❌ No UUIDs found from API")
        return

    print(f"✅ Found {len(api_uuids)} unique UUIDs from {total_assets} assets")

    # Get existing IDs from post_ids.py
    print(f"\n🔍 Checking for new IDs...")
    existing_ids = get_existing_post_ids("post_ids.py")
    print(f"📋 Existing IDs in post_ids.py: {len(existing_ids)}")

    # Find new IDs
    new_ids = [uuid for uuid in api_uuids if uuid not in existing_ids]

    if not new_ids:
        print("✅ No new IDs to add. All IDs are already in post_ids.py!")
        return

    print(f"\n🆕 Found {len(new_ids)} NEW IDs:")
    for i, new_id in enumerate(new_ids, 1):
        print(f"  {i}. {new_id}")

    # Update post_ids.py with new IDs
    print(f"\n📝 Adding new IDs to post_ids.py...")
    total_count = update_post_ids_file_with_new_ids(new_ids, "post_ids.py")

    print(f"✅ Successfully updated! Total IDs in post_ids.py: {total_count}")


if __name__ == "__main__":
    main()
