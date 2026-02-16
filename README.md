# Israeli Restaurant Availability Checker

Personal CLI tools to check restaurant reservation availability across OnTopo and Tabit — the two main booking platforms in Israel.

Designed for low-volume, personal convenience use — quickly scan which restaurants have open tables on a given evening, instead of manually checking dozens of restaurant pages one by one.

## Disclaimer & Legal Notice

**This project is not affiliated with, endorsed by, or associated with OnTopo, Tabit, or any restaurant listed here.** OnTopo and Tabit are trademarks of their respective owners, used here solely for identification purposes.

This tool makes standard HTTP requests to publicly accessible endpoints to check availability. It does **not** bypass authentication, CAPTCHAs, rate limits, or any other technical access controls.

- It does **not** book, hold, or reserve tables — it only checks publicly visible availability
- It does **not** scrape, store, or redistribute restaurant data at scale
- It includes rate limiting (configurable `--delay`) to avoid placing unnecessary load on any service
- The platforms' terms of service may prohibit automated access — **users are responsible for ensuring their use of this tool complies with all applicable terms of service and local laws**
- If a service blocks automated access, stop using the tool against that service

If you are a representative of OnTopo or Tabit and have concerns, please [open an issue](https://github.com/eytanlevit/israeli-restaurants/issues) or reach out directly — I'm happy to accommodate any requests.

**THE AUTHOR ASSUMES NO LIABILITY FOR ANY USE OR MISUSE OF THIS SOFTWARE. USE AT YOUR OWN RISK.**

## How It Works

Both CLIs act as lightweight clients that check availability for a given date, time, and party size — the same information you'd enter on each platform's website. No accounts, logins, or personal data are involved.

## Setup

### Prerequisites
- Python >= 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Install
```bash
git clone https://github.com/eytanlevit/israeli-restaurants.git
cd israeli-restaurants
uv sync
```

No API keys required for basic usage.

## Usage

### Check a specific restaurant
```bash
# OnTopo restaurant (by name or slug)
uv run --script ontopo-cli -r "Shila" -d 20260220 -t 2000 -p 2

# Tabit restaurant (by name or org ID)
uv run --script tabit-cli -r "DOK" -d 20260220 -t 2000 -p 2
```

### Batch check all restaurants
```bash
uv run --script ontopo-cli --batch -d 20260220 -t 1900 -p 2
uv run --script tabit-cli --batch -d 20260220 -t 1900 -p 2
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-d` / `--date` | Date in YYYYMMDD format | Tomorrow |
| `-t` / `--time` | Time in HHMM format (repeatable) | 1900 |
| `-p` / `--people` | Party size | 2 |
| `-r` / `--restaurant` | Restaurant name or platform ID | — |
| `-b` / `--batch` | Check all restaurants from CSV | — |
| `--delay` | Seconds between API calls | 0.3 |
| `--raw` | Output raw JSON | — |

### Multiple times
```bash
uv run --script ontopo-cli --batch -d 20260220 -t 1900 -t 2100
# or comma-separated
uv run --script ontopo-cli --batch -d 20260220 -t 1900,2030,2100
```

## Restaurant List

Restaurants are managed in `restaurants.csv`. Each entry has a name, booking provider (`ontopo` or `tabit`), the platform's ID, and city. Feel free to add your own favorites.

## Claude Code Integration

This repo includes a `SKILL.md` for use as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code), so you can ask Claude to check restaurant availability in natural language:

```
claude skill add --from /path/to/israeli-restaurants/SKILL.md
```

Then just ask: *"Any tables at Shila this Friday for 4?"*

## Rate Limiting & Responsible Use

Both CLIs include built-in delays between requests (default: 300ms). In batch mode with parallel workers, please be mindful of the load you're generating. The defaults are conservative and designed to be respectful of the platforms' infrastructure.

## License

MIT — see [LICENSE](LICENSE).

This license applies to the code in this repository only. It does not grant any rights to the trademarks, APIs, or services of OnTopo, Tabit, or any third party.
