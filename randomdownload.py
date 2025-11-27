# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Random Download Script
Downloads random posts from POST_IDS array
"""

import requests
from requests.exceptions import RequestException
import time
import random
from post_ids import POST_IDS, AUTH_ID

# ------------------------------
# CONFIG
# ------------------------------

AUTH_TOKEN = AUTH_ID  # Using AUTH_ID from post_ids.py
NUM_DOWNLOADS = 150  # Number of random posts to download

BASE_URL = "https://imagine.vyro.ai/v1/assets/{}/stats"

# ------------------------------
# SCRIPT START
# ------------------------------


def send_download_request(asset_id, token):
    """Send PUT request to increment download count for a single asset."""
    url = BASE_URL.format(asset_id)

    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123",
    }

    body = (
        "------WebKitFormBoundaryABC123\r\n"
        'Content-Disposition: form-data; name="downloaded"\r\n\r\n'
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
        print("[ERROR] AUTH_TOKEN is empty. Please update AUTH_ID in post_ids.py")
        return

    if len(POST_IDS) < NUM_DOWNLOADS:
        print(
            f"[WARNING] Only {len(POST_IDS)} posts available, downloading all of them"
        )
        num_to_download = len(POST_IDS)
    else:
        num_to_download = NUM_DOWNLOADS

    # Select random posts
    random_posts = random.sample(POST_IDS, num_to_download)

    success = 0
    failed = 0

    print("\n[START] Starting random download script...")
    print(
        f"[INFO] Downloading {num_to_download} random posts from {len(POST_IDS)} total posts"
    )
    print("--------------------------------------")

    for index, asset_id in enumerate(random_posts, start=1):
        print(f"\n[{index}/{num_to_download}] Downloading Asset ID: {asset_id}")

        status, result = send_download_request(asset_id, AUTH_TOKEN)

        if status == 200:
            print(f"   [SUCCESS] (200 OK)")
            success += 1
        else:
            print(f"   [FAILED] (Status: {status})")
            print(f"   Response: {result[:200]}")  # print first 200 chars
            failed += 1

        # Random delay between 5-10 seconds
        if index < num_to_download:  # Don't delay after the last request
            delay = random.uniform(2, 5)
            print(f"   [WAIT] {delay:.2f} seconds...")
            time.sleep(delay)

    print("\n--------------------------------------")
    print("[SUMMARY]")
    print(f"   Successful downloads : {success}")
    print(f"   Failed downloads     : {failed}")
    print("--------------------------------------\n")


if __name__ == "__main__":
    main()
