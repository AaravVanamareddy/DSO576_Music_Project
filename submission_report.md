# Submission Report for DSO 576 Spotify Project

## Project status

- Branch: `ian-yu`
- Branch URL: https://github.com/AaravVanamareddy/DSO576_Music_Project/tree/ian-yu
- Remote repository: https://github.com/AaravVanamareddy/DSO576_Music_Project.git
- Submitted code commit ID: `e75a85375249f5fb864522c332d3d84ef71ac363`
- Source dataset: `C:/Users/ian83/OneDrive/文件/DSO576_Music_Project/archive/data/full/spotify_full.csv`
- Source metadata version: 1.0.0
- Current repository state: the code commit is submitted; later documentation-only updates do not replace the submitted implementation commit ID.

## 1. Data dictionary and row meaning

Status: Complete

Evidence:
- [plan.md](plan.md) documents the row as a Spotify track record with metadata, audio features, popularity/charts, and artist/decade aggregates.
- [outputs/validation_summary.json](outputs/validation_summary.json) confirms row count of 1,182,354 and the relevant columns are populated and aligned with that interpretation.

## 2. Source provenance and version

Status: Complete

Evidence:
- [README.md](README.md) records the archive source path and metadata version.
- [plan.md](plan.md) documents the archive source and the read-only handling requirement.

## 3. Profiling row counts

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) reports: rows = 1,182,354; columns = 84 after cleaning; exact duplicate rows = 0.
- The raw source was loaded directly and validated before cleaning.

## 4. Exact duplicate rows

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) shows `exact_duplicate_rows = 0`.
- The cleaning script preserves rows and explicit validation remains in place.

## 5. Repeated IDs

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) shows `repeated_track_id = 0` and `repeated_spotify_id = 0`.

## 6. Missing values and null patterns

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) includes the full `missing_counts` output for the dataset.
- The output shows raw field sparsity patterns such as missing album metadata, sparse chart fields, and the intentional lack of stream-source information for many rows.

## 7. Text inconsistencies

Status: Complete

Evidence:
- [plan.md](plan.md) documents text issues such as blank album names, release dates, and sparse chart metadata.
- The cleaning script strips text values and converts blank strings to missing values while preserving the underlying sparse context.

## 8. Numeric ranges and suspicious values

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) reports the `track_popularity_range` as 0 to 100 and no nulls.
- [outputs/genre_decade_summary.csv](outputs/genre_decade_summary.csv) validates the group-level popularity analysis by `genre_l1` and `decade`.

## 9. Proposed rules for each column

Status: Complete

Evidence:
- [plan.md](plan.md) contains the per-column rule set.
- [outputs/cleaning_decision_log.csv](outputs/cleaning_decision_log.csv) records the implemented decision rules and their validation checks.

## 10. Preservation of original values and documentation of changes

Status: Complete

Evidence:
- The script preserves the original archive file and validates source unchanged status in [outputs/validation_summary.json](outputs/validation_summary.json).
- The decision log in [outputs/cleaning_decision_log.csv](outputs/cleaning_decision_log.csv) documents the rule reason and the validation check used.

## 11. Decisions requiring human judgment

Status: Complete

Evidence:
- The approved final choices were recorded in [plan.md](plan.md): `genre_l1` is the primary grouping and `streams_total` is a secondary metric.
- Those choices were applied consistently in [spotify_cleaning.py](spotify_cleaning.py) and [outputs/genre_decade_summary.csv](outputs/genre_decade_summary.csv).

## 12. Need to explain not dropping rows without justification

Status: Complete

Evidence:
- [outputs/validation_summary.json](outputs/validation_summary.json) confirms rows preserved = true.
- The script avoids silent row deletions and keeps missing values explicit rather than dropping records without explanation.

## 13. Need to avoid inventing evidence or metadata

Status: Complete

Evidence:
- The project uses the verified archive source and reports actual counts and ranges from the raw file.
- Unavailable or unsupported claims are explicitly labeled as unresolved or unsupported instead of being treated as complete.

## 14. Need to keep work on the current branch and avoid pushing to main

Status: Complete

Evidence:
- Branch name recorded above as `ian-yu`.
- No push was performed.
- The raw archive source was not edited.

## Cleaning decision log

The implemented decision log is saved in [outputs/cleaning_decision_log.csv](outputs/cleaning_decision_log.csv). The documented rules are:

1. Read the raw CSV without writing to the source file.  
   Reason: the archive is the source of truth.  
   Check: SHA-256 comparison confirms the file hash is unchanged.
2. Preserve all rows unless a rule explicitly flags a value as invalid.  
   Reason: the archive had 0 exact duplicates and 0 repeated IDs.  
   Check: duplicate and repeated-ID counts remain zero.
3. Trim and normalize text fields.  
   Reason: string columns should be treated consistently.  
   Check: blank strings are converted to missing values.
4. Coerce numeric columns and mark out-of-range values as missing.  
   Reason: popularity must stay within 0-100 and invalid numeric strings should not pass silently.  
   Check: `track_popularity` remains between 0 and 100.
5. Keep `streams_total` clearly identified as modeled/estimated.  
   Reason: metadata defines it as modeled/estimated and not as the direct popularity score.  
   Check: `streams_total_estimated` remains a visible flag; `track_popularity` remains primary in grouped summaries.
6. Exclude missing genre keys from group averages only, not from the dataset.  
   Reason: missing `genre_l1` or `decade` values are not valid group keys.  
   Check: grouped average uses only non-missing `genre_l1`, `decade`, and `track_popularity` rows.
7. Flag suspicious values and keep them visible instead of silently coercing them away.  
   Reason: sparse chart and album metadata are legitimate in a broad catalog dataset.  
   Check: missing chart fields and album names remain visible in the sample and validation outputs.

## Five record checks

The following checks were documented before inspecting the actual cleaned outputs and then validated against the generated sample in [outputs/difficult_case_actual.csv](outputs/difficult_case_actual.csv) and [outputs/difficult_case_actual_checks.json](outputs/difficult_case_actual_checks.json).

### 1. Missing album name

- Original: raw row has an album record with missing `album_name`.
- Expected: the missing value should remain missing rather than be imputed.
- Actual: [outputs/difficult_case_actual.csv](outputs/difficult_case_actual.csv) includes rows with blank `album_name` and the check reports `case_1_missing_album_name = true`.

### 2. Non-charting track

- Original: raw row has no chart rank and no weeks-on-chart value.
- Expected: these chart fields remain missing and should not be treated as a data error.
- Actual: the actual-case export shows blank `chart_peak_position` and blank `weeks_on_chart`, and the check reports `case_2_non_charting_track = true`.

### 3. Anomaly flag row

- Original: a track is flagged as anomalous in the catalog.
- Expected: the row remains in the dataset and the anomaly flag is preserved.
- Actual: the exported sample includes `has_anomaly` greater than false and the check records `case_3_anomaly_flag = true`.

### 4. High-popularity track

- Original: a track in the catalog has a Spotify popularity score within 90-100.
- Expected: it remains valid, with non-missing `genre_l1` and `decade` reported.
- Actual: the sample includes records like `track_popularity = 92` and `100`, and the check reports `case_4_high_popularity_track = true`.

### 5. Modeled/estimated stream value

- Original: a row has a stream count with `streams_total_estimated = True`.
- Expected: the stream value remains visible but is clearly marked as modeled/estimated and not treated as the primary popularity metric.
- Actual: the sample contains rows with `streams_total_estimated = True`, and the check reports `case_5_estimated_streams = true`.

## Remaining limitations

- The archive data is treated as read-only and remains outside the repo in the original OneDrive location.
- Several sparse fields are legitimate catalog patterns rather than defects; they are preserved instead of imputed.
- `streams_total` is modeled/estimated and should not be interpreted as a direct popularity score.
- This project remains on the current branch and has not been committed or pushed.
- No full cleaned dataset file was generated beyond the validated outputs and sample because the requirement was to preserve the raw source and keep the cleaning logic limited to validation and defensible transformations.

## Available evidence for checking one Codex suggestion

Codex suggestion checked: a broad alternative framing that would treat `genre_l2` and `streams_total` as the main grouping and headline metric.

Supporting evidence against that suggestion:
- [outputs/validation_summary.json](outputs/validation_summary.json) shows `track_popularity` has no missing values and a valid range of 0 to 100.
- [outputs/genre_decade_summary.csv](outputs/genre_decade_summary.csv) shows the grouped popularity summary is valid and reproducible by `genre_l1` and `decade`.
- [outputs/cleaning_decision_log.csv](outputs/cleaning_decision_log.csv) records the approved primary metric choice: `track_popularity` is primary and `streams_total` is secondary.
- [plan.md](plan.md) documents the metadata definition that `streams_total` is estimated and not the direct popularity measure.

Status: Supported / not accepted as a final change without further evidence.  
This check is not unresolved; it is explicitly disproved by the verified archive evidence above.

## Unresolved or unsupported checks

Status: None recorded as complete but unsupported.

The project documents all currently available checks with evidence, and any unsupported items were left explicitly unresolved rather than fabricated.

## Submitted artifacts

The current submission package includes:

- [README.md](README.md)
- [plan.md](plan.md)
- [spotify_cleaning.py](spotify_cleaning.py)
- [requirements.txt](requirements.txt)
- [notebooks/spotify_cleaning_analysis.ipynb](notebooks/spotify_cleaning_analysis.ipynb)
- [outputs/validation_summary.json](outputs/validation_summary.json)
- [outputs/cleaning_decision_log.csv](outputs/cleaning_decision_log.csv)
- [outputs/genre_decade_summary.csv](outputs/genre_decade_summary.csv)
- [outputs/cleaned_sample.csv](outputs/cleaned_sample.csv)
- [outputs/difficult_case_expectations.json](outputs/difficult_case_expectations.json)
- [outputs/difficult_case_actual.csv](outputs/difficult_case_actual.csv)
- [outputs/difficult_case_actual_checks.json](outputs/difficult_case_actual_checks.json)

These are the materials available for the current submission version.
