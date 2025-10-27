# apple_stock.py
# Prints Apple (AAPL) historical Date and Close using Yahoo Finance's chart API due to 404 conflict.
# Primary source: https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=1mo
# (Still Yahoo Finance; just a stable JSON endpoint instead of scraping HTML.)

import requests
from datetime import datetime, timezone

API_URLS = [
    # 1-month daily candles (enough rows for the assignment display)
    ("https://query1.finance.yahoo.com/v8/finance/chart/AAPL",
     {"interval": "1d", "range": "1mo"}),
    # Fallback: 3 months if 1mo fails for any reason
    ("https://query2.finance.yahoo.com/v8/finance/chart/AAPL",
     {"interval": "1d", "range": "3mo"}),
]

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_chart_json():
    last_err = None
    for url, params in API_URLS:
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            # Basic sanity check
            if "chart" in data and data["chart"].get("result"):
                return data
        except Exception as e:
            last_err = e
    raise last_err

def parse_dates_closes(data):
    result = data["chart"]["result"][0]
    ts = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    out = []
    for t, c in zip(ts, closes):
        if c is None:
            continue  # skip missing
        dt = datetime.fromtimestamp(t, tz=timezone.utc).date().isoformat()
        out.append((dt, c))
    return out

def main():
    data = fetch_chart_json()
    rows = parse_dates_closes(data)
    print("AAPL Historical Prices (Date, Close)")
    for dt, close in rows:
        print(f"{dt}\t{close}")
    if not rows:
        print("No rows parsed—API format may have changed.")

if __name__ == "__main__":
    main()
