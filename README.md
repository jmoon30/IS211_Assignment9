John Moon
Prof. Ledon
IS 211 - Software App. Programming II
Oct. 25, 2025

---
## Week 9 Web Scraping Scripts

This archive now includes two runnable scripts:

- `football_stats.py` — Scrapes CBS Sports NFL touchdowns leaders (regular season) and prints the top 20 with position, team, and TDs.  
  Source: https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/

- `apple_stock.py` — Scrapes Yahoo Finance AAPL historical prices and prints `Date` and `Close`.  
  Source: https://finance.yahoo.com/quote/AAPL/history?p=AAPL

### How to run
```bash
pip install -r requirements.txt  # or: pip install requests beautifulsoup4
python football_stats.py
python apple_stock.py
```

> If either site changes its HTML, the scripts include fallbacks and will print a helpful message.
