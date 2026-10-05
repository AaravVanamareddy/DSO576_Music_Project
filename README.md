# DSO576 Music Project

This repository documents a reproducible cleaning workflow for the Spotify archive dataset used in the DSO 576 project. The raw source remains unchanged, and the cleaning pipeline is implemented in a dedicated script so the original archive can always be re-used from the same source of truth.

## Source and version information

- Source archive: `C:/Users/ian83/OneDrive/文件/DSO576_Music_Project/archive/data/full/spotify_full.csv`
- Source metadata version: 1.0.0
- Verified row count: 1,182,354
- Verified column count: 83
- Verified duplicate status: 0 exact duplicates, 0 repeated `track_id`, 0 repeated `spotify_id`
- Primary analysis metric: `track_popularity`
- Secondary metric: `streams_total` only as a supplemental metric and clearly labeled as modeled/estimated
- Business question supported by the data: how Spotify track popularity differs across `genre_l1` and `decade`
- Branch name: `ian-yu`
- Branch URL: https://github.com/AaravVanamareddy/DSO576_Music_Project/tree/ian-yu
- Submitted code commit ID: `e75a85375249f5fb864522c332d3d84ef71ac363`
- Note: This commit ID is the submitted code version and must remain associated with the submitted implementation even after later documentation updates.

## Project files

- [plan.md](plan.md) – verified plan for the cleaning workflow and data-quality decisions
- [spotify_cleaning.py](spotify_cleaning.py) – main cleaning and validation script
- [requirements.txt](requirements.txt) – Python dependencies
- [outputs](outputs) – generated validation reports, grouped summary, sample output, and decision log
- [notebooks/spotify_cleaning_analysis.ipynb](notebooks/spotify_cleaning_analysis.ipynb) – notebook companion for analysis and difficult-case review

## Cleaning decisions implemented

The cleaning workflow follows the approved plan:

- Primary grouping uses `genre_l1`
- Primary metric is `track_popularity`
- `streams_total` is kept only as a secondary metric and flagged as modeled/estimated
- All rows are preserved unless a value is invalid under a documented range or transform rule
- String columns are stripped and empty strings are converted to missing values
- Numeric fields are coerced to numeric and invalid values are set to missing
- Missing `genre_l1` or `decade` values are excluded from grouped averages rather than being silently imputed
- Missing chart fields and album metadata are retained because they are legitimate sparse patterns in the archive dataset

## Run instructions

1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the cleaning script from the repository root:
   `python spotify_cleaning.py`
3. Review the outputs in the `outputs` directory:
   - `validation_summary.json`
   - `genre_decade_summary.csv`
   - `cleaning_decision_log.csv`
   - `cleaned_sample.csv`
   - `difficult_case_expectations.json`
   - `difficult_case_actual.csv`

## Expected outputs

The script reproduces the following artifacts from the original archive file without modifying the source:

- Full-dataset validation summary with row counts, duplicates, missing counts, and range checks
- Grouped average track popularity by `genre_l1` and `decade` with valid record counts
- Decision log matching the approved cleaning rules and their validation checks
- Five-row difficult-case sample capturing missing album names, non-charting records, anomaly flags, high-popularity tracks, and modeled stream estimates

## Important limitations

- The raw archive is treated as read-only and is never edited or overwritten.
- The analysis is intentionally descriptive rather than predictive.
- `streams_total` is not treated as a direct popularity measure because the metadata explicitly flags it as modeled/estimated.
- The script checks and reports values; it does not silently fabricate or hide missingness.
- The repository is kept on the current branch and is not pushed yet.

## Reproducibility

The script validates the original data before and after the cleaning workflow and confirms that the source file is unchanged. Running it repeatedly from the same archive file should produce identical outputs for the same version of the source dataset.
