import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

LEAGUES = ["SE1", "SE2", "SE3N", "SE3S"]

MATCHDAYS = {
    "SE1": 30,
    "SE2": 30,
    "SE3N": 26,
    "SE3S": 26,
}

def build_url(league_code: str, day: int, season: int) -> str:
    tm_year = season - 1
    return (
        f"https://www.transfermarkt.com/allsvenskan/spieltag/"
        f"wettbewerb/{league_code}/saison_id/{tm_year}/spieltag/{day}"
    )

def scrape_matchday(url: str):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    boxes = soup.select("div.large-8.columns > div.box")
    match_boxes = [b for b in boxes if b.select_one("span.matchresult")]

    matches = []
    for match in match_boxes:
        try:
            result_text = match.select_one("span.matchresult").text.strip()
            if ":" not in result_text:
                continue

            date_raw = match.select_one(
                "table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(1) > a:nth-child(2)"
            ).text.strip()

            home_team = match.select_one(
                "table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(1) > a:nth-child(2)"
            )["title"]

            away_team = match.select_one(
                "table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(8) > a:nth-child(1)"
            )["title"]

            hg, ag = result_text.split(":")
            matches.append({
                "date": date_raw,
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": int(hg),
                "away_goals": int(ag)
            })
        except Exception:
            continue

    return matches

def scrape_league(league_code: str, start_year: int, end_year: int):
    all_matches = []

    for season in range(start_year, end_year + 1):
        print(f"Scraping {league_code} {season}")

        for day in range(1, MATCHDAYS[league_code] + 1):
            url = build_url(league_code, day, season)
            day_matches = scrape_matchday(url)

            if not day_matches:
                break

            for m in day_matches:
                m["league"] = league_code
                m["season"] = season
                m["matchday"] = day

                all_matches.append(m)

            print(f"  Day {day}: {len(day_matches)} matches")
            time.sleep(1.0)

    return pd.DataFrame(all_matches)

def main():
    os.makedirs("data", exist_ok=True)
    combined = []

    for league in LEAGUES:
        df = scrape_league(league, 2011, 2025)
        path = f"data/raw/{league}_2011_2025.csv"
        df.to_csv(path, index=False)
        print(f"Saved {path}")
        combined.append(df)

    all_df = pd.concat(combined, ignore_index=True)
    all_df.to_csv("data/raw/swedish_leagues_2011_2025.csv", index=False)
    print("Saved data/swedish_leagues_2011_2025.csv")

if __name__ == "__main__":
    main()
