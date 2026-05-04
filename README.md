# 🧠 TryHackMe Progress Tracker

> Automatically synced from TryHackMe · Updated by GitHub Actions · Logged to Notion

![Last Sync](https://img.shields.io/badge/last%20sync-auto-brightgreen?style=flat-square)
![Platform](https://img.shields.io/badge/platform-TryHackMe-red?style=flat-square)
![Automation](https://img.shields.io/badge/automation-GitHub%20Actions-blue?style=flat-square)

---

## 📊 Stats

<!-- THM-STATS:START -->
| Metric | Value |
|--------|-------|
| 🏁 Rooms Completed | — |
| 🔥 Current Streak | — |
| 🏆 Rank | — |
| 🌐 Country Rank | — |
<!-- THM-STATS:END -->

---

## ✅ Completed Rooms

<!-- THM-ROOMS:START -->
| Room | Category | Difficulty | Completed |
|------|----------|------------|-----------|
| — | — | — | — |
<!-- THM-ROOMS:END -->

---

## 📝 Writeups

Writeups are stored in the [`/rooms`](./rooms) folder, organized by category.

---

## ⚙️ How It Works

```
TryHackMe API
     │
     ▼
GitHub Actions (runs every hour)
     │
     ├──▶ Updates this README
     │
     └──▶ Syncs to Notion database
```

1. GitHub Actions polls the TryHackMe API on a schedule
2. New completed rooms are added to the table above
3. The same data is pushed to your Notion database automatically

---

## 🔧 Setup

See [SETUP.md](./SETUP.md) for full instructions.
