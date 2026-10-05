# Track Promotion Strategy Data Cleaning

This repository contains my individual DSO 576 Module 6 data-cleaning work for the Track Promotion Strategy project. The project supports music-label marketing managers who want to compare tracks within the same genre and release period and examine which audio characteristics are associated with higher historical Spotify popularity. `track_popularity` is the primary metric. `streams_total` is a secondary metric and must be interpreted together with `streams_status`.

## Submission Information

- Student: Zhouyan Yuan
- Personal branch: Hazel-Yuan
- Team repository: <https://github.com/AaravVanamareddy/DSO576_Music_Project>


## Data Source and Version

- Dataset: Spotify Music Features Dataset
- Provider: Kaggle
- Source URL: <https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset>
- Source file: `data/raw/spotify_full.csv`
- Download date/version used: October 4, 2026
- Source dimensions: 1,182,354 rows and 83 columns
- Source file size: 816,973,617 bytes (779.13 MiB)
- Source SHA-256: `DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914`

The raw CSV is the authoritative source and must remain unchanged. The cleaning script reads it from `data/raw/` and writes all derived files to separate locations. The large raw and cleaned CSV files may be excluded from Git according to the repository's data-storage rules.

## Cleaning Summary

The approved workflow preserves all 1,182,354 source rows and all 83 original columns. Four transparent fields are added:

- `dashboard_eligible`
- `duration_over_one_hour`
- `invalid_time_signature`
- `streams_status`

The cleaning rules:

- preserve `track_id` and `spotify_id` as text identifiers;
- retain all rows because the full audit found no exact duplicates or repeated identifiers;
- convert applicable fields to nullable pandas types;
- trim boundary whitespace from 30 `track_artist` values;
- remove the single U+007F DEL control character from one title;
- retain missing title and artist values without imputation and mark the 20 affected rows as dashboard-ineligible;
- retain and flag 407 durations longer than one hour;
- retain and flag 1,228 nonpositive time signatures;
- retain 22,590 missing time signatures without imputation;
- distinguish 9,600 direct stream values from 1,172,754 estimated values; and
- retain `hit_probability` for source preservation but exclude it from dashboard decision logic.

No source row was dropped, no missing value was filled, and no unusual numeric value was automatically corrected.

## Repository Files

```text
.
├── data/
│   ├── raw/
│   │   └── spotify_full.csv
│   ├── cleaned/
│   │   └── spotify_cleaned.csv
│   └── sample/
│       ├── spotify_cleaned_sample.csv
│       └── cleaning_log.csv
├── notebooks/
│   └── data_cleaning.ipynb
├── reports/
│   └── validation_report.md
├── src/
│   └── clean_data.py
├── audit_report.md
├── manual_record_checks.md
├── plan.md
├── requirements.txt
└── README.md
```

If the notebook directory in the repository is named `notebook/` rather than `notebooks/`, use the existing directory name and do not create a duplicate folder.

## Environment Setup

Python 3.13 was used for this project. A project-specific virtual environment is recommended.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run Instructions

1. Place the unchanged source CSV at:

   ```text
   data/raw/spotify_full.csv
   ```

2. Activate the project virtual environment.

3. From the repository root, run the complete cleaning pipeline:

   ```bash
   python src/clean_data.py
   ```

4. Confirm that the terminal finishes without an exception and that every row in the cleaning log has `PASS` status.

5. Open `notebooks/data_cleaning.ipynb` in VS Code, select the project kernel, and choose **Restart Kernel and Run All Cells**.

The notebook uses `RUN_FULL_PIPELINE = False` by default so that it can review the existing sample and reports quickly without loading or rewriting the full dataset. The complete rebuild is performed with `python src/clean_data.py`. Change the notebook switch to `True` only when an intentional full rerun is required.

## Expected Output Files

After a successful full run, the following files should exist:

| Output | Purpose |
| --- | --- |
| `data/cleaned/spotify_cleaned.csv` | Complete cleaned dataset with 1,182,354 rows and 87 columns |
| `data/sample/spotify_cleaned_sample.csv` | Up to 50 cleaned rows, including the five difficult manual-check cases |
| `data/sample/cleaning_log.csv` | Machine-readable rule checks with expected values, actual values, and PASS status |
| `reports/validation_report.md` | Full reconciliation, duplicate, missing-value, range, stream-status, and hash results |
| `manual_record_checks.md` | Five original, expected, and actual record comparisons with Pass/Fail decisions |
| `notebooks/data_cleaning.ipynb` | Readable audit, decision, result, and validation walkthrough |

The validated full output contains 1,182,354 rows and 87 columns. All 83 original columns are retained, all automated cleaning controls pass, all five manual record checks pass, and the raw source hash remains unchanged.

## Validation Checks

The submitted results were checked using:

- row counts before and after cleaning;
- original and final column counts;
- exact duplicate and repeated-identifier counts;
- missing-value counts before and after cleaning;
- numeric ranges and suspicious-value flags;
- direct versus estimated stream counts;
- the raw-file SHA-256 before and after cleaning;
- five manually reviewed difficult records; and
- comparison of the cleaned outputs with approved expected results.

One apparent manual-check failure was reviewed rather than accepted automatically. A `novelty_score` value differed only because of CSV floating-point serialization: `0.23198887705802917` versus `0.2319888770580291`. The absolute difference was approximately `8.33e-17`, below the approved `1e-12` tolerance, so the semantic value was unchanged and the record correctly passed.

## Limitations

- The analysis is descriptive and does not establish that an audio feature causes popularity.
- Most stream counts are estimated rather than directly observed.
- Twenty records lack a title or artist and are retained but excluded from dashboard display.
- Unusual durations and invalid or missing time signatures are flagged rather than externally corrected.
- `hit_probability` is a modeled field and is not used for dashboard eligibility or automated promotion decisions.
- Marketing spend, playlist placement, promotion exposure, radio play, and listener demographics are not included in the dataset.

