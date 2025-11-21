import pandas as pd

df = pd.read_csv("data/raw/swedish_leagues_2011_2025.csv")

df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")

TEAM_MAP = {
    "Athletic FC United": "AFC Eskilstuna",
}

df["home_team"] = df["home_team"].replace(TEAM_MAP)
df["away_team"] = df["away_team"].replace(TEAM_MAP)

teams_after = sorted(
    pd.unique(pd.concat([df["home_team"], df["away_team"]], ignore_index=True))
)

df["result"] = df.apply(
    lambda r: (
        "H"
        if r["home_goals"] > r["away_goals"]
        else ("A" if r["home_goals"] < r["away_goals"] else "D")
    ),
    axis=1,
)

df = df.sort_values(["league", "season", "date", "matchday"]).reset_index(drop=True)

out_path = "data/processed/swedish_leagues_2011_2025_clean.csv"
df.to_csv(out_path, index=False)

print("Saved:", out_path)
print("Total rows:", len(df))
