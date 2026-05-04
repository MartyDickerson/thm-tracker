"""
sync_thm.py
-----------
Fetches completed TryHackMe rooms and syncs them to:
  1. This repo's README.md
  2. A Notion database
"""

import os
import re
import json
import requests
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────

THM_USERNAME      = os.environ["THM_USERNAME"]
NOTION_TOKEN      = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

THM_PROFILE_URL   = f"https://tryhackme.com/api/user/rank/{THM_USERNAME}"
THM_ROOMS_URL     = f"https://tryhackme.com/api/v2/hacktivities?username={THM_USERNAME}&limit=100&type=completed"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

DIFFICULTY_EMOJI = {
    "easy":   "🟢",
    "medium": "🟡",
    "hard":   "🔴",
    "insane": "⚫",
}

# ── TryHackMe ─────────────────────────────────────────────────────────────────

def fetch_thm_profile():
    """Fetch rank/streak data from TryHackMe public API."""
    try:
        r = requests.get(THM_PROFILE_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[THM] Could not fetch profile: {e}")
        return {}


def fetch_completed_rooms():
    """Fetch list of completed rooms from TryHackMe public API."""
    try:
        r = requests.get(THM_ROOMS_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("data", {}).get("items", [])
    except Exception as e:
        print(f"[THM] Could not fetch rooms: {e}")
        return []


# ── Notion ────────────────────────────────────────────────────────────────────

def get_existing_notion_rooms():
    """Return set of room slugs already in the Notion database."""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    existing = set()
    has_more = True
    cursor = None

    while has_more:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor

        r = requests.post(url, headers=NOTION_HEADERS, json=payload)
        data = r.json()

        for page in data.get("results", []):
            props = page.get("properties", {})
            slug_prop = props.get("Slug", {}).get("rich_text", [])
            if slug_prop:
                existing.add(slug_prop[0]["text"]["content"])

        has_more = data.get("has_more", False)
        cursor = data.get("next_cursor")

    return existing


def add_room_to_notion(room: dict):
    """Create a new page in the Notion database for a completed room."""
    difficulty = room.get("difficulty", "unknown").lower()
    emoji = DIFFICULTY_EMOJI.get(difficulty, "⚪")
    completed_date = room.get("completedDate", "")

    # Parse ISO date if present
    try:
        dt = datetime.fromisoformat(completed_date.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": room.get("title", "Unknown Room")}}]
            },
            "Slug": {
                "rich_text": [{"text": {"content": room.get("code", "")}}]
            },
            "Category": {
                "select": {"name": room.get("categories", ["Uncategorized"])[0] if room.get("categories") else "Uncategorized"}
            },
            "Difficulty": {
                "select": {"name": f"{emoji} {difficulty.capitalize()}"}
            },
            "Completed": {
                "date": {"start": date_str}
            },
            "URL": {
                "url": f"https://tryhackme.com/room/{room.get('code', '')}"
            },
            "Status": {
                "status": {"name": "Done"}
            },
        },
    }

    r = requests.post(
        "https://api.notion.com/v1/pages",
        headers=NOTION_HEADERS,
        json=payload,
    )

    if r.status_code == 200:
        print(f"[Notion] ✅ Added: {room.get('title')}")
    else:
        print(f"[Notion] ❌ Failed to add {room.get('title')}: {r.text}")


# ── README ────────────────────────────────────────────────────────────────────

def update_readme(rooms: list, profile: dict):
    """Inject updated stats and room table into README.md."""
    with open("README.md", "r") as f:
        content = f.read()

    # ── Stats block ──
    rank        = profile.get("userRank", "—")
    country_rank = profile.get("countryRank", "—")
    streak      = profile.get("streak", {}).get("currentStreak", "—")
    total       = len(rooms)

    stats_table = f"""| Metric | Value |
|--------|-------|
| 🏁 Rooms Completed | {total} |
| 🔥 Current Streak | {streak} days |
| 🏆 Rank | #{rank} |
| 🌐 Country Rank | #{country_rank} |"""

    content = re.sub(
        r"(<!-- THM-STATS:START -->).*?(<!-- THM-STATS:END -->)",
        f"<!-- THM-STATS:START -->\n{stats_table}\n<!-- THM-STATS:END -->",
        content,
        flags=re.DOTALL,
    )

    # ── Rooms table ──
    rows = []
    for room in sorted(rooms, key=lambda r: r.get("completedDate", ""), reverse=True):
        title      = room.get("title", "Unknown")
        slug       = room.get("code", "")
        category   = (room.get("categories") or ["—"])[0]
        difficulty = room.get("difficulty", "—").capitalize()
        emoji      = DIFFICULTY_EMOJI.get(difficulty.lower(), "⚪")

        try:
            dt = datetime.fromisoformat(room.get("completedDate", "").replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            date_str = "—"

        rows.append(
            f"| [{title}](https://tryhackme.com/room/{slug}) | {category} | {emoji} {difficulty} | {date_str} |"
        )

    rooms_table = "| Room | Category | Difficulty | Completed |\n|------|----------|------------|-----------|\n"
    rooms_table += "\n".join(rows) if rows else "| — | — | — | — |"

    content = re.sub(
        r"(<!-- THM-ROOMS:START -->).*?(<!-- THM-ROOMS:END -->)",
        f"<!-- THM-ROOMS:START -->\n{rooms_table}\n<!-- THM-ROOMS:END -->",
        content,
        flags=re.DOTALL,
    )

    with open("README.md", "w") as f:
        f.write(content)

    print(f"[README] ✅ Updated with {total} rooms")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("🚀 Starting TryHackMe sync...\n")

    profile = fetch_thm_profile()
    rooms   = fetch_completed_rooms()

    print(f"[THM] Found {len(rooms)} completed rooms")

    # Sync new rooms to Notion
    existing = get_existing_notion_rooms()
    new_rooms = [r for r in rooms if r.get("code") not in existing]

    print(f"[Notion] {len(new_rooms)} new room(s) to add")
    for room in new_rooms:
        add_room_to_notion(room)

    # Update README
    update_readme(rooms, profile)

    print("\n✅ Sync complete!")


if __name__ == "__main__":
    main()
