# football_stats.py
# Scrapes CBS Sports NFL player touchdowns leaders (Regular season) and prints top 20.
# Source: https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/
#
# Usage: python football_stats.py
# Dependencies: requests, beautifulsoup4
# Note: Requires internet access when you run it locally.

import requests
from bs4 import BeautifulSoup

URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/"

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.text

def parse_touchdowns(html: str):
    soup = BeautifulSoup(html, "html.parser")
    # CBS generally renders a table for stats with tbody rows.
    # We'll search for the first table that contains 'TD' and 'Player' headers.
    tables = soup.find_all("table")
    target = None
    for tbl in tables:
        headers = [th.get_text(strip=True).upper() for th in tbl.find_all("th")]
        if not headers:
            continue
        if "PLAYER" in headers and "TD" in headers:
            target = tbl
            break
    if target is None and tables:
        target = tables[0]
    if target is None:
        raise RuntimeError("Could not locate stats table on the page.")

    rows = []
    for tr in target.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 5:
            continue
        # Heuristic extraction:
        # Usually the first cell is Rank, second contains player (and team/pos),
        # and a later cell contains TD total. We'll map flexibly.
        texts = [td.get_text(" ", strip=True) for td in tds]
        # Find a numeric touchdowns column
        td_val = None
        # try last cells first
        for candidate in reversed(texts):
            if candidate.isdigit():
                td_val = int(candidate)
                break
        # player/pos/team usually in the 1st or 2nd data cell
        player_cell = tds[1] if len(tds) > 1 else None
        player_name = ""
        position = ""
        team = ""
        if player_cell:
            # Player name is often in an <a>, team & pos appear as small tags or spans
            a = player_cell.find("a")
            if a:
                player_name = a.get_text(strip=True)
            else:
                player_name = player_cell.get_text(" ", strip=True)
            # Try to parse team/pos tokens like "KC · RB" or "KC RB"
            tail = player_cell.get_text(" ", strip=True)
            # Attempt to find tokens after name
            if player_name and tail.startswith(player_name):
                tail = tail[len(player_name):].strip(" -·|, ")
            parts = [p for p in tail.replace("·", " ").replace("|", " ").split() if p]
            # Look for a typical 2-3 letter team code and a 1-2 letter position near it
            # Not perfect, but good enough for assignment scraping.
            for p in parts:
                if len(p) in (2,3) and p.isupper():
                    team = team or p
                if len(p) in (1,2,3) and p.upper() in {"QB","RB","WR","TE","FB","KR","PR","DB","LB","DL","OL"}:
                    position = position or p.upper()
        if player_name and td_val is not None:
            rows.append((player_name, position, team, td_val))
        if len(rows) >= 20:
            break
    return rows

def main():
    html = fetch_html(URL)
    leaders = parse_touchdowns(html)
    print("Top 20 NFL Players by Total Touchdowns (CBS Sports, Regular Season)")
    print("{:<2}  {:<25} {:<3} {:<2} {:>3}".format("#", "Player", "Pos", "Tm", "TD"))
    for i, (name, pos, tm, td) in enumerate(leaders, start=1):
        print("{:<2}  {:<25} {:<3} {:<2} {:>3}".format(i, name, pos or "-", tm or "-", td))
    if not leaders:
        print("No results parsed. The page structure may have changed.")

if __name__ == "__main__":
    main()
