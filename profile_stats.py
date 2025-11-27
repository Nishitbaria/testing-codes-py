#!/usr/bin/env python3
"""
Display most liked and viewed posts from any Imagine.art profile
"""

import requests
import sys


def fetch_user_posts(username, auth_token, limit=3000):
    """Fetch published posts from a specific user profile"""
    url = f"https://imagine.vyro.ai/v1/user/{username}/published?limit={limit}"

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
        return data.get("assets", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return []


def get_top_by_likes(assets, top_n=10):
    """Get top N posts sorted by likes (favorites)"""
    return sorted(assets, key=lambda x: x.get("favorites", 0), reverse=True)[:top_n]


def get_top_by_views(assets, top_n=10):
    """Get top N posts sorted by views"""
    return sorted(assets, key=lambda x: x.get("views", 0), reverse=True)[:top_n]


def display_top_posts(assets, username, top_n=10):
    """Display top posts in two sections: most liked and most viewed"""
    print("\n" + "=" * 100)
    print(f"📊 PROFILE STATS FOR @{username}")
    print("=" * 100)

    if not assets:
        print("❌ No posts found for this user")
        return

    # Display summary
    total_favorites = sum(a.get("favorites", 0) for a in assets)
    total_views = sum(a.get("views", 0) for a in assets)
    total_downloads = sum(a.get("downloads", 0) for a in assets)

    print(f"\n📈 PROFILE SUMMARY")
    print(f"   Total Posts: {len(assets)}")
    print(f"   Total Favorites: {total_favorites:,}")
    print(f"   Total Views: {total_views:,}")
    print(f"   Total Downloads: {total_downloads:,}")

    # Get top posts by likes and views
    top_liked = get_top_by_likes(assets, top_n)
    top_viewed = get_top_by_views(assets, top_n)

    # Display TOP 10 MOST LIKED POSTS
    print("\n" + "=" * 100)
    print(f"❤️  TOP {top_n} MOST LIKED POSTS")
    print("=" * 100)
    print("-" * 100)
    print(f"{'#':<4} {'Title':<50} {'❤️ Likes':<15} {'👁️ Views':<15}")
    print("-" * 100)

    for i, asset in enumerate(top_liked, 1):
        title = asset.get("title", "Untitled")[:48]
        favorites = asset.get("favorites", 0)
        views = asset.get("views", 0)
        uuid = asset.get("uuid", "N/A")

        print(f"{i:<4} {title:<50} {favorites:<15,} {views:<15,}")

    print("-" * 100)

    # Display TOP 10 MOST VIEWED POSTS
    print("\n" + "=" * 100)
    print(f"👁️  TOP {top_n} MOST VIEWED POSTS")
    print("=" * 100)
    print("-" * 100)
    print(f"{'#':<4} {'Title':<50} {'👁️ Views':<15} {'❤️ Likes':<15}")
    print("-" * 100)

    for i, asset in enumerate(top_viewed, 1):
        title = asset.get("title", "Untitled")[:48]
        views = asset.get("views", 0)
        favorites = asset.get("favorites", 0)
        uuid = asset.get("uuid", "N/A")

        print(f"{i:<4} {title:<50} {views:<15,} {favorites:<15,}")

    print("-" * 100)
    print("\n" + "=" * 100 + "\n")


def main():
    # Auth token
    AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJpbnRlZ3JpdHlDaGVjayI6ZmFsc2UsImJhc2VVcmwiOiIiLCJwcm9kdWN0VmFsaWRGb3IiOiJJTUFHSU5FIiwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTc2MzE3OTE1OSwiZXhwIjoxNzYzMjAwNzU5LCJzdWIiOiIyMjIzZmEwOC01MDZmLTQzOTktOTAzZS00ODcwZjUwN2I2OTMiLCJqdGkiOiJjMmU3Y2I0MS02NjE4LTQ1YTgtYWUwNS0zZjhlMDM2OWU5MTMifQ.kCheQA4ePdNQCT5f4v4cpO5ZK1Rc1C3FnbpQOHRG2BU"

    # Always ask for input
    print("\n" + "=" * 60)
    print("📊 IMAGINE.ART PROFILE STATS VIEWER")
    print("=" * 60)
    username = input("\n🔗 Enter profile link or username: ").strip()

    if not username:
        print("❌ No input provided. Exiting...")
        return

    # Extract username from URL if full link provided
    if "imagine.art" in username:
        # Extract username from URL like https://www.imagine.art/@username
        parts = username.split("/")
        for part in parts:
            if part.startswith("@"):
                username = part[1:]  # Remove @
                break
            elif part and not part.startswith("http") and "." not in part:
                username = part

    # Remove @ if user typed it
    username = username.lstrip("@")

    print(f"\n🔍 Fetching posts from @{username}...")

    # Fetch posts
    assets = fetch_user_posts(username, AUTH_TOKEN)

    if not assets:
        print(f"❌ No posts found for @{username}")
        print("💡 Make sure the username is correct and the profile is public")
        return

    # Display stats
    display_top_posts(assets, username, top_n=10)


if __name__ == "__main__":
    main()
