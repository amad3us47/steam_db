# steam_db

A self-updating SQLite database of Steam games. A scraper walks Steam app IDs, pulls each game's title from its store page, and stores it in `test/games.db`. A daily GitHub Actions job runs the scraper and commits the growing database back to the repo.

## Schema

Table `games` in `test/games.db`:

| Column | Type    | Description               |
| ------ | ------- | ------------------------- |
| `id`   | INTEGER | Steam app ID (primary key)|
| `name` | TEXT    | Game title                |

## Setup

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
cd test
python main.py    # scrape (resumes from the last stored ID)
python read.py    # print all stored games
```

## Automation

`.github/workflows/test.yml` runs daily at midnight UTC (or manually from the Actions tab), scrapes, and commits the updated `games.db`. Each run resumes where the last one stopped, so the database grows over time.

## Notes

- IDs are crawled sequentially; Steam's ID space is sparse, so many are skipped and a full crawl takes many runs.
- Titles are parsed from the store page's `appHubAppName` element — a Steam layout change could break parsing.
- One request per second (intentionally gentle).
- `main.yml` is a legacy workflow referencing a missing `fetch.py`; `test.yml` is the one that actually runs.

## License
