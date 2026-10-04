# DSO576 Music Project: Data Cleaning (Arman Hovsepian)

**Project:** Track Promotion Strategy
**Branch:** `arman-hovsepian`
**Branch URL:** https://github.com/AaravVanamareddy/DSO576_Music_Project/tree/arman-hovsepian
**Commit ID:** [added after first push]

## Data source
- Kaggle: Spotify Music Features Dataset (amith1707)
  https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset
- File used: `data/full/spotify_full.csv` (817 MB, 1,182,354 rows, 83 columns; 20 columns used)
- Downloaded: October 4, 2026
- The original data is **not** in this repo (too large for GitHub) and is never modified.

## Setup
1. Download and unzip the Kaggle dataset. Place the `archive/` folder **next to** this repo folder, so the parent folder contains both `archive/` (the Kaggle download, unchanged) and `DSO576_Music_Project/` (this repo).
2. Use Python 3.14 and install dependencies: `pip install -r requirements.txt`

## How to run
- **Script:** from the repo root, run `python src/clean_data.py`
- **Notebook:** open `notebooks/cleaning.ipynb`, click Restart, then Run All

Both read the original CSV, apply the same cleaning rules, and print the same final check.

## Expected output
- `data/sample/cleaned_sample.csv`: 50 cleaned rows, including difficult cases (`source_row` = row position in the original file)
- Final check printed: rows 1,182,354 | columns 22 | possible_duplicate 29,248 | unusual_duration 4,407 | missing genre 18,090

## Cleaning rules
1. Strip leading/trailing spaces from `track_artist` (30 values changed)
2. Convert genre "Unknown" to missing in `genre_l1` and `genre_l2` (18,090 rows)
3. Flag tracks sharing the same title and artist as `possible_duplicate` (matched on the actual title, because `title_normalized` drops non-Latin characters); no rows removed
4. Flag tracks under 30 seconds or over 20 minutes as `unusual_duration`; no rows removed

## Files
- `notebooks/cleaning.ipynb`: full cleaning process with checks and evidence
- `src/clean_data.py`: the same cleaning rules as a runnable script
- `data/sample/cleaned_sample.csv`: 50-row cleaned sample
- `requirements.txt`: dependencies