# Change Requests — Spotify Track Promotion Strategy

## Claims

| Member | Feature | Number |
| --- | --- | --- |
| Arman |Exclude Estimated Streams toggle| Median Streams|
| Yolanda | Track Profile / Add to Shortlist | Top 20% Group Count |
| Elena | Genre Filter / Cohort Update | Median Popularity |
| Ian Yu | Audio Feature Comparison | Top Group Mean Energy |
| Hazel | Data Source Integrity / Estimated-Stream Disclosure | Estimated-stream share in cohort |

## Findings

### CR-001 — Track Profile Error

**Auditor:** Yolanda  
**Status:** Change requested

**Expected:** Track profiles should display correctly and allow users to add tracks to the Promotion Shortlist.

**Actual:** The Overview tab raises `KeyError: 'canonical_track_id'` after Top Tracks Preview. The error persists after rerunning.

**Evidence:** Tested with the 50-row sample under default filters. Traceback identifies `app.py`, lines 181 and 85.

**Requested change:** Preserve `canonical_track_id` when passing track records to `show_profile()` and retest the shortlist workflow.

### CHECK-001 — Top 20% Group Count

**Auditor:** Yolanda  
**Status:** Passed for tested sample

**Expected:** `ceil(0.20 × N)` tracks selected by popularity descending, breaking ties with canonical track ID.

**Actual:** Cohort N = 50, Top N = 10, cutoff popularity = 44.0.

**Evidence:** Independent results from `verify_module9.py` match the dashboard.

**Requested change:** None for the tested calculation. Full-data and other-filter validation remain untested.

### CHECK-002 – Median Streams

**Auditor:** Arman
**Status:** Passed for tested sample 

**Expected:** Median streams should be the median of streams_total across all 50 cohort tracks when the toggle is off, and across only 2 non estimated tracks when the toggle is on.

**Actual:** toggle off median is 3,283,769 and toggle on is 658,720, 810

**Evidence:** the 50-row sample, all genres, years 2001–2023, success metric = Streams. 
Toggle off: df["streams_total"].median()
Toggle on: df[df["streams_total_estimated"] == False]["streams_total"].median()
It returned the same numbers and passed

**Requested change:** No change is needed for the tested calculation. Although, keep in mind that I did not test other genres or date ranges 

### CR-002 – Exclude Estimated Streams Toggle

**Auditor:** Arman
**Status:** Change requested

**Expected:** Streaming numbers should change, becasuse excluding estimates is about streams data, so it shouldn’t change the cohort or median popularity. Once estimates are excluded, the label should say the streams are actual or real, not “includes estimates.” The app warns you when only a few tracks remain.

**Actual:** The whole cohort dropped from 50 to 2 tracks, and median popularity jumped from 27.5 to 99. The label still said “includes estimates.” No warning appeared.

**Evidence:** Settings: 50-row sample, all genres, 2001–2023, success metric = Streams (includes estimates).
The test: screenshot with the toggle off, then tick it and screenshot again. tracks 50 → 2, median popularity 27.5 → 99.0, median streams 3,283,769 → 658,720,810.
REVEALED  48 estimated and only 2 real, Flowers and Blinding Lights. These are the 2 that remain 

**Requested change:** Have a warning icon when the numbers drop to a certain amount. When toggle is on, change the label to something like "actual streams." Also, only the streams numbers should change, so the toggle shouldn’t remove tracks from the other metrics.

### CHECK-003 — Audio Feature Comparison / Top Group Mean Energy

**Auditor:** Ian Yu
**Status:** Passed for tested sample

**Expected:** With All genres, release years 2001–2023, Popularity, and Top 20%, the audio feature comparison should show the mean Energy for the Top and Other groups, with valid counts. Energy is on a 0–1 scale.

**Actual:** The app showed Top mean Energy = 0.7207 (Valid N = 10) and Other mean Energy = 0.592 (Valid N = 40).

**Evidence:** I opened Overview using the settings above and inspected the Audio Feature Comparison chart and table. The sample cohort contained 50 tracks, split into 10 Top tracks and 40 Other tracks. An independent pandas calculation from `spotify_cleaned_sample.csv` returned Top mean = 0.720700 and Other mean = 0.591969, which rounds to the displayed values.

**Requested change:** None for the tested sample. The full dataset and other filter settings remain untested.

### CHECK-004 — Genre Filter / Cohort Update and Median Popularity

**Auditor:** Elena Wei
**Status:** Passed for tested sample

**Expected:** Selecting a broad genre should restrict the cohort to that genre and recalculate the cohort-dependent results. Median popularity should equal the median of the nonmissing `track_popularity` values in the filtered cohort.

**Actual:** With release years 2001–2023 and Popularity selected, changing Broad genre from All genres to Pop reduced the cohort from 50 to 5 tracks and the Top 20% group from 10 to 1 track. All five preview records were Pop. The dashboard displayed median popularity of 29.0.

**Evidence:** The five Pop popularity values were 100, 98, 29, 18, and 0. Manually sorting them as 0, 18, 29, 98, and 100 gives a median of 29, matching the dashboard. The filtering logic in `filter_cohort()` uses `genre_l1`, the inclusive release-year range, and nonmissing values for the selected metric.

**Requested change:** None for the tested Genre Filter and Median Popularity claims. Other genres, release-year ranges, and the full dataset remain untested.

### CHECK-005 — Data Source Integrity / Estimated-Stream Disclosure

**Auditor:** Hazel Yuan
**Status:** Passed for tested sample

**Expected:** The deployed `spotify_cleaned_sample.csv` should satisfy the Module 6 cleaning rules the app relies on: `canonical_track_id` unique and nonmissing, no missing values in required display and metric fields, no boundary whitespace in `title` or `track_artist`, and release years inside the slider range. With All genres, 2001–2023, and any success metric, the caption "Estimated streams records in cohort" should equal the share of cohort rows where `streams_total_estimated` is True.

**Actual:** 50 rows × 27 columns. `canonical_track_id` has 0 duplicates and 0 missing values. `title`, `track_artist`, `genre_l1`, `release_year`, `track_popularity`, and `streams_total` each have 0 missing values. Boundary whitespace: 0 titles, 0 artists. Release years range from 2001 to 2023. `streams_total_estimated`: 48 True, 2 False, so the expected caption is 96.0%. The dashboard displayed 96.0%.

**Evidence:** Independent pandas check on `spotify_cleaned_sample.csv` without importing the app:
`df["canonical_track_id"].duplicated().sum()` → 0;
`(df["track_artist"] != df["track_artist"].str.strip()).sum()` → 0;
`df["streams_total_estimated"].value_counts()` → True 48, False 2.
Note: `canonical_track_id` equals `spotify_id` (the bare 22-character ID), not `track_id` (the `spotify:track:` URI). This works, but it is not documented in the README or BUILD_SPEC.

**Requested change:** None for the tested calculation. Document in the README that `canonical_track_id` = `spotify_id`.

### CR-003 — Deployed Sample Does Not Represent Full-Data Edge Cases

**Auditor:** Hazel Yuan
**Status:** Change requested

**Expected:** The smoke-test sample should include the edge cases found in the full-data audit (Module 6, `Hazel-Yuan` branch), so the app's handling of them is tested before the full file is used: records missing title or artist (20 in full data), durations over one hour (407), nonpositive time signatures (1,228), and a realistic direct vs. estimated stream mix (9,600 direct of 1,182,354, about 0.8%).

**Actual:** The sample contains 0 records missing title or artist, 0 durations over one hour, and 0 nonpositive time signatures. Direct streams make up 4% of the sample (2 of 50), and both direct tracks are the two most popular tracks in it (Flowers = 100, Blinding Lights = 98). This explains why CR-002's toggle sends median popularity from 27.5 to 99. The app also does not read a `dashboard_eligible` flag, so with the full file the 20 records without a title or artist would enter rankings, and the track selector would label them "nan".

**Evidence:** `spotify_cleaned_sample.csv` checks: `(df["duration_ms"] > 3_600_000).sum()` → 0; `(df["time_signature"] <= 0).sum()` → 0; `df[["title","track_artist"]].isna().any(axis=1).sum()` → 0. Full-data counts come from `Hazel-Yuan:reports/validation_report.md` and `data/sample/cleaning_log.csv`. In `app.py`, `filter_cohort()` filters only on year, metric, genre, and the estimate toggle.

**Requested change:** (1) Add a few edge-case rows to the sample (for example the five records in `Hazel-Yuan:manual_record_checks.md`) and rerun CHECK-001 to CHECK-005. (2) In `filter_cohort()`, exclude rows where `title` or `track_artist` is missing (or `dashboard_eligible` is False) before ranking, and show the excluded count in a caption. (3) State in the README that sample-based KPIs cannot be generalized to the full dataset.
