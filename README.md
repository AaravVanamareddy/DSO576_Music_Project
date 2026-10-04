# DSO 576 Music Project

## Project
Spotify Track Promotion Strategy

This project analyzes Spotify track data to support promotion decisions by identifying characteristics associated with stronger historical track performance. The primary performance metric is `track_popularity`, with `streams_total` used as a secondary metric.

## Data Source
- Source: https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset
- Original file: `spotify_full.csv`

The original dataset is kept unchanged and is not included in the GitHub repository because of its size.

## Data Cleaning
The cleaning workflow is contained in `cleaning.ipynb`.

The notebook:
- preserves the original source data
- selects project-relevant columns
- standardizes descriptive text
- converts and validates dates
- checks exact duplicates and repeated track IDs
- checks and handles missing values
- validates numeric ranges and suspicious values
- verifies five individual records
- reconciles starting and final row counts
- creates reproducible cleaned output files

## How to Run

1. Clone the repository and switch to the `aarav-vanamareddy` branch.
2. Place `spotify_full.csv` in the project directory.
3. Install the required dependencies:

   `pip install -r requirements.txt`

4. Open `cleaning.ipynb`.
5. Restart the kernel and run all cells from top to bottom.

## Expected Outputs

Running `cleaning.ipynb` creates:

- `spotify_cleaned_full.csv` - full cleaned analytical dataset (stored locally and not pushed to GitHub because of its size)
- `spotify_cleaned_sample.csv` - 50-row cleaned sample included in GitHub
- `requirements.txt` - Python dependencies required to reproduce the cleaning workflow

The final cleaned dataset contains 1,182,354 rows and 27 columns.

## GitHub Submission

- Branch: `aarav-vanamareddy`
- Branch URL: [ADD AFTER PUBLISHING BRANCH]
- Commit ID: [ADD FINAL COMMIT ID]