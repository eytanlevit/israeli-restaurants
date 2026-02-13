---
name: israeli-restaurants
description: "Search Israeli restaurant availability. Triggers: restaurant reservations, dinner, tables, DOK, Habasta, Shila, Gaijin. Hebrew: איזה מסעדות פנויות, שולחן פנוי, הזמנה למסעדה"
---

# Israeli Restaurants Skill

Search for restaurant availability using OnTopo and Tabit.

## CRITICAL: Use the CLIs

Located at: `~/projects/israeli-restaurants/`

## Commands

### Search all restaurants (batch mode)
```bash
# OnTopo restaurants
uv run --script ~/projects/israeli-restaurants/ontopo-cli --batch -d YYYYMMDD -t HHMM -p PARTY

# Tabit restaurants
uv run --script ~/projects/israeli-restaurants/tabit-cli --batch -d YYYYMMDD -t HHMM -p PARTY

# For comprehensive search, run BOTH commands
```

### Search specific restaurant by name
```bash
# If you know the provider:
uv run --script ~/projects/israeli-restaurants/ontopo-cli -r "name_or_slug" -d YYYYMMDD -t HHMM -p PARTY
uv run --script ~/projects/israeli-restaurants/tabit-cli -r "name_or_org_id" -d YYYYMMDD -t HHMM -p PARTY
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
