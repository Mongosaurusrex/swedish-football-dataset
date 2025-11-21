# swedish-football-dataset

This repository contains a complete, cleaned dataset of match results from the Swedish football league system, covering Allsvenskan, Superettan, Ettan Norra, and Ettan Södra, for the seasons 2011 through 2025.

Data was collected from Transfermarkt’s public matchday pages and cleaned into a uniform format for use in analysis, modelling, and prediction.

The purpose of this dataset is to support statistical analysis, Bayesian rating systems, predictive modelling (win/draw/loss), and general historical queries for Swedish football.

## Contents

```
data/
    raw/
        SE1_2011_2025.csv               # Allsvenskan
        SE2_2011_2025.csv               # Superettan
        SE3N_2011_2025.csv              # Ettan Norra
        SE3S_2011_2025.csv              # Ettan Södra
        swedish_leagues_2011_2025.csv   # Combined master dataset

src/
    scraper/
        transfermarkt_scraper           # The scraper

requirements.txt                        # Minimal Python packages requirements
README.md                               # This file
```

## Dataset structure

| Column | Description |
|----------|----------|
| date    | Match date (parsed YYYY-MM-DD) |
| home_team    | Home team name |
| away_team    | Away team name |
| home_goals | Home team goals |
| away_team    | Away team goals |
| league | Which league the game was played (see below for translation) |
| season | Which season (year) |
| matchday| What matchday it was (number) |
| result    | Match outcome (H, D, A) |

### League translation

| Code | League |
|----------|----------|
| SE1 | Allsvenskan |
| SE2   | Superettan |
| SE3N    | Division 1 Norra |
| SE3S | Division 1 Södra |

## Data cleaning notes

	•	Dates are parsed using dayfirst=True.
	•	Team names have been inspected for duplication or inconsistencies.
	•	A small number of matchday anomalies were manually patched:
	•	SE3N 2025 Day 13
	•	SE2 2011 Day 5
	•	SE1 2011 Day 2
	•	Div 1 leagues have varying team counts across years (14–16), so match totals differ by season.

## Why from 2011?

In order to have a continuous history of football results across all of the league 2011 was selected because it was the furthest common season that all four leagues had 

## License

You must give appropriate credit if you:
	•	use the data
	•	publish analyses
	•	build models
	•	include it in research
	•	redistribute modified or unmodified versions

Attribution example:

Dataset created by Nathan Dygant (2025).
Source: https://github.com/Mongosaurusrex/swedish-football-dataset

Full license text:
https://creativecommons.org/licenses/by/4.0/


