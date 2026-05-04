# 🔧 Setup Guide

Follow these steps to get the full automation running.

---

## Step 1 — Create the GitHub Repo

1. Create a new **public** repo on GitHub (e.g. `thm-tracker`)
2. Push all these files into it

---

## Step 2 — Create the Notion Database

1. Open Notion and create a new **full-page database**
2. Name it: `TryHackMe Rooms`
3. Add these exact columns:

| Column Name | Type |
|-------------|------|
| Name | Title |
| Slug | Text |
| Category | Select |
| Difficulty | Select |
| Completed | Date |
| URL | URL |
| Status | Status |

4. Copy your **Database ID** from the URL:
   ```
   https://notion.so/your-workspace/THIS-PART-IS-THE-ID?v=...
   ```

---

## Step 3 — Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New Integration**
3. Name it: `THM Tracker`
4. Copy the **Internal Integration Token**
5. Go to your Notion database → click `...` → **Add connections** → select `THM Tracker`

---

## Step 4 — Add GitHub Secrets

In your GitHub repo go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Value |
|-------------|-------|
| `THM_USERNAME` | Your TryHackMe username (e.g. `MartyDickerson`) |
| `NOTION_TOKEN` | Your Notion integration token |
| `NOTION_DATABASE_ID` | Your Notion database ID from Step 2 |

---

## Step 5 — Run It

- The workflow runs **automatically every hour**
- You can also trigger it manually: **Actions tab → Sync TryHackMe Progress → Run workflow**

---

## How a new room gets logged

```
You complete a room on TryHackMe
         │
         ▼
GitHub Actions wakes up (next hour)
         │
         ├──▶ Fetches your completed rooms from TryHackMe API
         │
         ├──▶ Adds any new rooms to your Notion database
         │
         └──▶ Updates README.md with latest stats & room list
```
