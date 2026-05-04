"""
sync_thm.py - Reads rooms.json and syncs to Notion + README
"""

import os
import re
import json
import requests
from datetime import datetime, timezone

NOTION_TOKEN       = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

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

def load_rooms():
    with open("rooms.json", "r") as f:
        return json.load(f)

def get_existing_notion_rooms():
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
            slug_prop = page.get("properties", {}).get("Slug", {}).get("rich_text", [])
            if slug_prop:
                existing.add(slug_prop[0]["text"]["content"])
        has_more = data.get("has_more", False)
        cursor = data.get("next_cursor")
    return existing

def add_room_to_notion(room):
    difficulty = room.get("difficulty", "easy").lower()
    emoji = DIFFICULTY_EMOJI.get(difficulty, "🟢")
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name":       {"title": [{"text": {"content": room["title"]}}]},
            "Slug":       {"rich_text": [{"text": {"content": room["slug"]}}]},
            "Category":   {"select": {"name": room.get("category", "General")}},
            "Difficulty": {"select": {"name": f"{emoji} {difficulty.capitalize()}"}},
            "Completed":  {"date": {"start": room["completed"]}},
            "URL":        {"url": f"https://tryhackme.com/room/{room['slug']}"},
            "Status":     {"status": {"name": "Done"}},
        },
    }
    r = requests.post("https://api.notion.com/v1/pages", headers=NOTION_HEADERS, json=payload)
    if r.status_code == 200:
        print(f"[Notion] ✅ Added: {room['title']}")
    else:
        print(f"[Notion] ❌ Failed: {room['title']}: {r.text}")

def update_readme(rooms):
    with open("README.md", "r") as f:
        content = f.read()

    total = len(rooms)
    stats_table = f"""| Metric | Value |
|--------|-------|
| 🏁 Rooms Completed | {total} |"""

    content = re.sub(
        r"(<!-- THM-STATS:START -->).*?(<!-- THM-STATS:END -->)",
        f"<!-- THM-STATS:START -->\n{stats_table}\n<!-- THM-STATS:END -->",
        content, flags=re.DOTALL,
    )

    rows = []
    for room in sorted(rooms, key=lambda r: r.get("completed", ""), reverse=True):
        difficulty = room.get("difficulty", "easy").capitalize()
        emoji = DIFFICULTY_EMOJI.get(difficulty.lower(), "🟢")
        rows.append(
            f"| [{room['title']}](https://tryhackme.com/room/{room['slug']}) "
            f"| {room.get('category', '—')} | {emoji} {difficulty} | {room['completed']} |"
        )

    rooms_table = "| Room | Category | Difficulty | Completed |\n|------|----------|------------|-----------|\n"
    rooms_table += "\n".join(rows) if rows else "| — | — | — | — |"

    content = re.sub(
        r"(<!-- THM-ROOMS:START -->).*?(<!-- THM-ROOMS:END -->)",
        f"<!-- THM-ROOMS:START -->\n{rooms_table}\n<!-- THM-ROOMS:END -->",
        content, flags=re.DOTALL,
    )

    with open("README.md", "w") as f:
        f.write(content)
    print(f"[README] ✅ Updated with {total} rooms")

def main():
    print("🚀 Starting sync...\n")
    rooms = load_rooms()
    print(f"[rooms.json] Found {len(rooms)} rooms")

    existing = get_existing_notion_rooms()
    new_rooms = [r for r in rooms if r["slug"] not in existing]
    print(f"[Notion] {len(new_rooms)} new room(s) to add")
    for room in new_rooms:
        add_room_to_notion(room)

    update_readme(rooms)
    print("\n✅ Sync complete!")

if __name__ == "__main__":
    main()
