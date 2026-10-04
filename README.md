# DSO576 Music Project

## Project

Track Promotion Strategy

This project uses Spotify track data to support music promotion decisions by comparing track popularity, stream counts, genre, release period, and musical characteristics.

## Data Source

Source: Kaggle Spotify Music Features Dataset

Original file:
`data/spotify_full.csv`

The source dataset contains 1,182,354 rows and 83 columns.

The original source file is preserved and is not modified during the cleaning process.

## Data Cleaning

The cleaning workflow:

- preserves all source rows;
- converts `release_date` and `chart_date_first` to datetime;
- removes leading and trailing whitespace from `track_artist`;
- preserves missing values when no reliable replacement is available;
- does not automatically generate missing `title_normalized` values;
- preserves unusual but plausible duration and release-year records;
- does not remove rows for duplication because no exact duplicate rows, duplicated `track_id`, or duplicated `spotify_id` values were found.

## Run Instructions

From the project root, run:

```bash
python scripts/clean_spotify.py
```

## Expected Output Files

- `data/spotify_clean.csv` — full cleaned dataset
- `data/spotify_clean_sample.csv` — 50-row cleaned sample
- `spotify_cleaning_report.md` — cleaning and validation report

## Cleaned Sample

The 50-row cleaned sample includes five intentionally selected difficult cases:

- missing `title_normalized`
- missing `release_date`
- missing `anomaly_flags`
- unusually long track duration
- unusually short track duration

The remaining 45 records were randomly selected from the cleaned dataset using `random_state=42`.

## GitHub Submission

Branch name: `yolanda`

Branch URL: [add final branch URL]

Commit ID: [add final commit ID]