---
name: israeli-restaurants
description: "Search Israeli restaurant availability. Triggers: restaurant reservations, dinner, tables, DOK, Habasta, Shila, Gaijin. Hebrew: איזה מסעדות פנויות, שולחן פנוי, הזמנה למסעדה"
---

# Israeli Restaurants Skill

Search for restaurant availability across OnTopo and Tabit booking platforms.

## Installation

### Prerequisites
- Python >= 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Setup
```bash
git clone https://github.com/eytanlevit/israeli-restaurants.git
cd israeli-restaurants
uv sync
```

No API keys or environment variables required. The CLIs handle all API calls directly.

### Add as a Claude Code skill
```bash
claude skill add --from /path/to/israeli-restaurants/SKILL.md
```

## Commands

Set `REPO` to wherever you cloned the repo (e.g., `~/projects/israeli-restaurants`).

### Search all restaurants (batch mode)
```bash
# OnTopo restaurants
uv run --script $REPO/ontopo-cli --batch -d YYYYMMDD -t HHMM -p PARTY

# Tabit restaurants
uv run --script $REPO/tabit-cli --batch -d YYYYMMDD -t HHMM -p PARTY

# For comprehensive search, run BOTH commands
```

### Search specific restaurant by name
```bash
uv run --script $REPO/ontopo-cli -r "name_or_slug" -d YYYYMMDD -t HHMM -p PARTY
uv run --script $REPO/tabit-cli -r "name_or_org_id" -d YYYYMMDD -t HHMM -p PARTY
```

## Date Format
- YYYYMMDD (e.g., 20260130)
- Parse from: tomorrow, friday, מחר, יום שישי, מוצ"ש

## Time Format
- HHMM (e.g., 1900 for 7pm)

## Defaults
- Party: 2
- Time: 1900
- Date: tomorrow

## Workflow for "איזה מסעדות פנויות"
1. Calculate date in YYYYMMDD format
2. Run ontopo-cli --batch
3. Run tabit-cli --batch
4. Combine and present results
