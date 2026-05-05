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
| 🏁 Rooms Completed | 3 |
<!-- THM-STATS:END -->

---

## ✅ Completed Rooms

<!-- THM-ROOMS:START -->
| Room | Category | Difficulty | Completed |
|------|----------|------------|-----------|
| [Junior Security Analyst Intro](https://tryhackme.com/room/jrsecanalystintrouxo) | SOC | 🟢 Easy | 2025-05-04 |
| [Security Operations Center (SOC)](https://tryhackme.com/room/securityoperationscenter) | SOC | 🟢 Easy | 2025-05-04 |
| [A Day in the Life of a Security Analyst](https://tryhackme.com/room/adayinthelifeofasecurityanalyst) | SOC | 🟢 Easy | 2025-05-04 |
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
