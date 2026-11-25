# 🐾 Dobot User Manual
*Quick guide for Harith's persistent AI companion on Ubuntu + Antigravity CLI*

---

## Quick Start

Dobot auto-loads automatically whenever you start a new `agy` session via the global `dobot-memorycore` plugin. Just open `agy` and talk normally — in Malay, English, or Manglish.

To manually wake or reload Dobot mid-session, just type:
```text
Dobot
```

---

## Commands Cheat Sheet

| Command / Phrase | What Dobot Does |
|------------------|-----------------|
| `Dobot` | Instant memory restoration & check-in |
| `save` / `simpan` | Routes and saves context (session memory, daily diary, topic diary, or all) |
| `save diary` / `tulis diary` | Appends today's hangout to `daily-diary/current/YYYY-MM-DD.md` |
| `review diary` | Summarizes recent daily diary entries |
| `save topic` / `remember this under [topic]` | Saves reusable notes to `topic-diary/topics/[topic].md` |
| `review topic [topic]` / `list topics` | Reviews a saved topic or lists all topics |
| `recall [topic]` / `ingat tak ...` / `hari tu ...` | Searches past diaries & topics and recalls naturally (never fabricates) |
| `remind me ...` / `ingatkan aku ...` | Adds a persistent reminder to `main/reminders.md` |
| `check reminders` | Lists all open reminders |
| `update memory` | Updates Harith's learned preferences in `main/main-memory.md` |

---

## Toggle Dobot ON / OFF

Since Dobot runs as an Antigravity CLI global plugin, you can pause or re-enable Dobot anytime (e.g., if you want plain default mode for heavy work):

```bash
# Pause Dobot
agy plugin disable dobot-memorycore

# Bring Dobot back
agy plugin enable dobot-memorycore

# Check plugin status
agy plugin list
```

---

## File Map

### 1. Memory Database (`/home/arixz/Project-AI-MemoryCore/`)
| File / Folder | Purpose |
|---------------|---------|
| `master-memory.md` | Entry point & loading protocol |
| `main/main-memory.md` | Unified identity, Dobot's personality, Harith's profile, Time-Aware rules |
| `main/current-session.md` | Active session RAM (auto-resets at 500 lines, keeps Session Recap) |
| `main/reminders.md` | Persistent cross-session reminders (`Open` & `Completed`) |
| `daily-diary/current/` | Active month's daily diary entries (`YYYY-MM-DD.md`) |
| `daily-diary/archived/` | Auto-archived past months (`YYYY-MM/`) |
| `topic-diary/index.md` | Catalog of all saved topic journals |
| `topic-diary/topics/` | Individual topic files (`[topic].md`) |
| `Feature/` | Extra optional MemoryCore modules you can explore anytime |

### 2. Antigravity CLI Global Plugin (`/home/arixz/.gemini/config/plugins/dobot-memorycore/`)
| File | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `rules/AGENTS.md` | Always-on rule keeping Dobot active from any folder |
| `hooks.json` | Registers the `SessionStart` auto-load hook |
| `scripts/session-start.sh` | Injects live Ubuntu time + Dobot's cat energy mode on session start |
| `skills/save-diary/SKILL.md` | Daily diary logging skill |
| `skills/topic-diary/SKILL.md` | Topic-based journal & save routing skill |
| `skills/echo-recall/SKILL.md` | Diary & topic memory search skill |
| `skills/check-reminders/SKILL.md` | Cross-session reminder skill |

---

## Tweaking Dobot Later

- **Adjust personality, speech quirks, or language rules:** Edit `/home/arixz/Project-AI-MemoryCore/main/main-memory.md` (or just tell Dobot directly in chat — e.g., *"update memory: ..."*).
- **Keep `AGENTS.md` in sync** if you change major identity rules: `/home/arixz/.gemini/config/plugins/dobot-memorycore/rules/AGENTS.md`.
- **Add more features later:** Browse `/home/arixz/Project-AI-MemoryCore/Feature/` (e.g., Interactive Story, Song Creation, Decision Log, Auto-Commit) and ask Dobot to install any module you want.

---

🐾 *Saved for Harith — 2026-11-25*
