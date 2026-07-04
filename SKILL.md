---
name: israeli-restaurants
description: "Search Israeli restaurant availability. Triggers: restaurant reservations, dinner, tables, DOK, Habasta, Shila, Gaijin. Hebrew: איזה מסעדות פנויות, שולחן פנוי, הזמנה למסעדה"
---

# Israeli Restaurants Skill

Search for restaurant availability across OnTopo and Tabit booking platforms.

## Installation

### Prerequisites
- Python >= 3.10 (with [uv](https://docs.astral.sh/uv/getting-started/installation/), none needed — uv provisions Python itself)

### Setup — Option A: with uv (recommended)
```bash
git clone https://github.com/eytanlevit/israeli-restaurants.git
```
That's it. The CLIs declare their dependencies inline (PEP 723); `uv run --script` installs them automatically on first run. (`uv sync` is only needed to run the test suite.)

### Setup — Option B: without uv (plain Python >= 3.10)
```bash
git clone https://github.com/eytanlevit/israeli-restaurants.git
pip install httpx rich curl_cffi requests python-dotenv
```
Then run the CLIs with `python3` instead of `uv run --script`, e.g.:
```bash
python3 $REPO/ontopo-cli --batch -d YYYYMMDD -t HHMM -p PARTY
```

⚠️ **macOS system Python is 3.9.6 — too old.** `ontopo-cli` crashes on it (`X | None` annotations need 3.10+). On a fresh Mac, install uv (Option A) or Python 3.10+ from python.org first.

No API keys or environment variables required. The CLIs handle all API calls directly.

### Add as a Claude Code skill
```bash
claude skill add --from /path/to/israeli-restaurants/SKILL.md
```

## CRITICAL: ALWAYS Use the CLI Tools

**NEVER** search OnTopo/Tabit marketplaces directly or browse their websites.
**ALWAYS** use the CLI commands which search ONLY the user's curated restaurant list in the CSV.

The user does NOT want results from the full marketplaces.
They ONLY want results from their personal favorites list.

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

### Multiple times
```bash
uv run --script $REPO/ontopo-cli --batch -d YYYYMMDD -t 1900 -t 2100 -p 2
# or comma-separated:
uv run --script $REPO/ontopo-cli --batch -d YYYYMMDD -t 1900,2045,2100 -p 2
```

### List all Tabit restaurants
```bash
uv run --script $REPO/tabit-cli --list
```

## Date Verification

**BEFORE running any command:**
1. Check today's date: `date +%Y%m%d`
2. Calculate the requested date in YYYYMMDD format
3. Verify: "Today is [DATE], user requested [DAY], so target date is [YYYYMMDD]"

**Hebrew day references:**
- היום = today
- מחר = tomorrow
- מוצ"ש / מוצש = Saturday night (Motzei Shabbat)
- יום שישי = Friday
- יום שבת = Saturday

**Date format:** YYYYMMDD (e.g., 20260130)

## Time Format
- HHMM (e.g., 1900 for 7pm)

## Defaults
- Party: 2
- Time: 1900
- Date: tomorrow

## Output Formatting (Telegram-friendly, Hebrew)

**ALWAYS respond in Hebrew.** DO NOT use markdown tables.

### Format Structure

1. **Hebrew summary line:**
   `מצאתי X מסעדות פנויות ל[יום] ([תאריך]) ב-[שעה] ל-[מספר]!`

2. **Group by time relevance:**
   - `עם שולחן ב-[שעה] בדיוק:` (exact match)
   - `קרוב ל-[שעה]:` (nearby times)

3. **Simple bullet format with time RANGES:**
   ```
   • Shila - 19:30-20:30
   • Cicchetti - 20:00, 20:45, 21:15
   • Romano - 19:30-20:15, 22:00
   ```
   Use ranges when times are consecutive (19:30, 19:45, 20:00 -> "19:30-20:00")

4. **If 10+ restaurants, group by cuisine:**
   ```
   🍣 יפני:
   • Gaijin Izakaya - 20:00-21:00
   • ASA Izakaya - 19:30, 20:15

   🍝 איטלקי:
   • Cicchetti - 20:00, 20:45
   • Romano - 19:30-20:15
   ```

5. **End with follow-up in Hebrew:**
   `רוצה שאמליץ על אחת מהן או שתבחר ואשלח לינק להזמנה?`

### Cuisine Categories (for grouping)
- יפני: Gaijin Izakaya, ASA Izakaya, Umai
- ים תיכוני/ישראלי: Shila, North Abraxas, Mashya, HaKatan, Port Said, Barbur, Pereh
- איטלקי: Cicchetti, Romano, Cafe Italia, Pronto
- אסייתי: Taizu, Cichukai
- בשרים: OCD, DOK, The Brothers
- טאפאס/בר: Chacoli, Bar 51, Milgo & Milbar
- שף: A (by Yuval Ben Neriah), Night Kitchen, Santi

### Guidelines
- Keep restaurant names in English (CSV doesn't have Hebrew)
- Use Hebrew for everything else (headers, summaries, questions)
- Show time ranges, not every 15-min slot
- Do NOT truncate - show all available restaurants
- List unavailable briefly at end if relevant: `לא פנוי: HaKatan, Mashya`

## Workflow for "איזה מסעדות פנויות"
1. Verify today's date with `date +%Y%m%d`
2. Calculate target date in YYYYMMDD format
3. Run ontopo-cli --batch
4. Run tabit-cli --batch
5. Combine and present results using the Output Formatting rules above

For general queries like "what's available tonight" or "מסעדה הערב", follow the same workflow -- always run BOTH CLIs to get complete coverage.

## Booking Links (VERIFIED formats)

When sharing a booking link with the user, use EXACTLY these formats.
The batch output's "Book" column already uses them.

**OnTopo** (slug = 8-digit ID from the CSV):
```
https://ontopo.com/he/il/page/{slug}
```
Example: https://ontopo.com/he/il/page/69127207 (Shila)
⚠️ Do NOT use `ontopo.com/he/il/r/{slug}` — it redirects to a 404 page.

**Tabit** (orgId = 24-char hex ID from the CSV):
```
https://tabitisrael.co.il/online-reservations/create-reservation?step=search&orgId={orgId}&locale=he-IL
```
Example: https://tabitisrael.co.il/online-reservations/create-reservation?step=search&orgId=64a2cd4dbaaf6d1b2ba2dfdc&locale=he-IL (Rova A)
⚠️ Do NOT use `tabitisrael.co.il/he/rsv/area/{orgId}` or `/rsv/booking/create?orgId=` — both silently redirect to the Tabit homepage.
⚠️ Tabit serves HTTP 200 for ANY path (SPA catch-all), so `curl` status checks cannot validate a Tabit link — only the format above is known to render the restaurant's booking page.

## Notes

- The CSV contains the user's curated list of restaurants
- OnTopo uses 8-digit slugs for restaurant IDs
- Tabit uses longer org IDs
- Both CLIs support `--raw` for JSON output
