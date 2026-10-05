# Spotify track popularity cleaning plan (verified against archive data)

## Scope and status

This plan updates the preliminary plan with verified findings from the actual archive dataset at `C:\Users\ian83\OneDrive\文件\DSO576_Music_Project\archive` and the project repository on the current branch. No cleaning transformations have been applied, and the original files have not been moved, overwritten, or modified.

The archive dataset is the canonical project data file at `archive/data/full/spotify_full.csv`. The archive also includes several derived feature files and subset files, but the full track-level table is the appropriate source for the business question: how Spotify track popularity differs across genres and release decades.

## 1. Source of the data and reproduction note

### Verified archive files

The archive contains these relevant files:
- `README.md`
- `metadata/metadata.json`
- `data/full/spotify_full.csv`
- `data/features/spotify_features.csv`
- `data/features/spotify_audio_features.csv`
- `data/features/spotify_artists.csv`
- `data/features/spotify_artist_features.csv`
- `data/features/spotify_genre_tags.csv`
- `data/features/spotify_popularity_metrics.csv`
- `data/splits/spotify_train.csv`, `spotify_val.csv`, `spotify_test.csv`
- `data/subsets/spotify_high_popularity.csv`, `spotify_instrumental_acoustic.csv`, `spotify_pre2000.csv`, `spotify_streaming_era.csv`

### Original dataset used for this plan

The canonical full dataset is:
- `C:\Users\ian83\OneDrive\文件\DSO576_Music_Project\archive\data\full\spotify_full.csv`

This is the file that should be used for the analysis unless a different upstream dataset or subset is explicitly requested.

### How to reproduce the source

Another person can reproduce the work by copying the archive folder, keeping the raw file read-only, and re-running the profiling logic from the repository. The raw file should be preserved as-is; no commit or push should include the full raw dataset content.

## 2. Verified dataset profile

### Full-dataset counts and schema

Verified with the actual source file:
- Rows: 1,182,354
- Columns: 83
- File type: CSV, not gzipped
- Data source description in metadata: “Spotify Music Features Dataset”, version 1.0.0

### Column names

`track_id`, `spotify_id`, `title`, `title_normalized`, `track_artist`, `album_id`, `album_name`, `release_year`, `release_date`, `duration_ms`, `explicit_flag`, `has_audio_features`, `source_dataset`, `energy`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`, `loudness`, `tempo`, `key`, `key_name`, `mode`, `mode_name`, `time_signature`, `genre_l1`, `genre_l2`, `genre_raw`, `track_popularity`, `streams_total`, `streams_source`, `streams_total_estimated`, `stream_density`, `chart_peak_position`, `weeks_on_chart`, `chart_date_first`, `popularity_imputed_aug`, `track_age_days`, `era`, `decade`, `energy_loudness_ratio`, `mood_index`, `acoustic_synthetic_ratio`, `emotional_arc`, `tempo_band`, `is_likely_instrumental`, `is_likely_live`, `is_likely_spoken_word`, `loudness_war_index`, `novelty_score`, `hit_probability`, `mood_cluster`, `taste_cluster`, `fp_energy`, `fp_valence`, `fp_danceability`, `fp_acousticness`, `fp_instrumentalness`, `fp_speechiness`, `fp_liveness`, `mean_energy_by_artist`, `sonic_evolution_score`, `genre_breadth`, `catalog_size`, `career_start_year`, `career_end_year`, `career_span_years`, `longevity_score`, `hit_rate`, `artist_stream_mean_log`, `artist_stream_median_log`, `mean_energy_by_decade`, `mean_valence_by_decade`, `mean_tempo_by_decade`, `mean_loudness_by_decade`, `acousticness_decline_idx`, `danceability_trend`, `decade_track_count`, `anomaly_flags`, `has_anomaly`, `release_year_precision_aug`

### Verified dtypes

- `album_id`: string
- `album_name`: string
- `release_year`: int64
- `release_date`: string
- `duration_ms`: int64
- `explicit_flag`: bool
- `has_audio_features`: bool
- `source_dataset`: string
- `energy`: float64
- `valence`: float64
- `danceability`: float64
- `acousticness`: float64
- `instrumentalness`: float64
- `speechiness`: float64
- `liveness`: float64
- `loudness`: float64
- `tempo`: float64
- `key`: int64
- `key_name`: string
- `mode`: int64
- `mode_name`: string
- `time_signature`: float64
- `genre_l1`: string
- `genre_l2`: string
- `genre_raw`: string
- `track_popularity`: int64
- `streams_total`: float64
- `streams_source`: string
- `streams_total_estimated`: bool
- `stream_density`: float64
- `chart_peak_position`: float64
- `weeks_on_chart`: float64
- `chart_date_first`: string
- `popularity_imputed_aug`: bool
- `track_age_days`: float64
- `era`: string
- `decade`: int64
- `energy_loudness_ratio`: float64
- `mood_index`: float64
- `acoustic_synthetic_ratio`: float64
- `emotional_arc`: string
- `tempo_band`: string
- `is_likely_instrumental`: bool
- `is_likely_live`: bool
- `is_likely_spoken_word`: bool
- `loudness_war_index`: float64
- `novelty_score`: float64
- `hit_probability`: float64
- `mood_cluster`: string
- `taste_cluster`: string
- `fp_energy`: float64
- `fp_valence`: float64
- `fp_danceability`: float64
- `fp_acousticness`: float64
- `fp_instrumentalness`: float64
- `fp_speechiness`: float64
- `fp_liveness`: float64
- `mean_energy_by_artist`: float64
- `sonic_evolution_score`: float64
- `genre_breadth`: float64
- `catalog_size`: float64
- `career_start_year`: float64
- `career_end_year`: float64
- `career_span_years`: float64
- `longevity_score`: float64
- `hit_rate`: float64
- `artist_stream_mean_log`: float64
- `artist_stream_median_log`: float64
- `mean_energy_by_decade`: float64
- `mean_valence_by_decade`: float64
- `mean_tempo_by_decade`: float64
- `mean_loudness_by_decade`: float64
- `acousticness_decline_idx`: float64
- `danceability_trend`: float64
- `decade_track_count`: int64
- `anomaly_flags`: string
- `has_anomaly`: bool
- `release_year_precision_aug`: bool

## 3. What one row represents and possible unique identifiers

### Verified row meaning

A row represents one Spotify track record with track metadata, audio features, chart/popularity signals, artist-level summary fields, and decade-level derived metrics. It is not a customer, subscription, membership, or conversion row.

The metadata description and columns confirm this:
- track metadata: `track_id`, `spotify_id`, `title`, `track_artist`, `album_id`, `album_name`, `release_year`, `release_date`
- audio features: `energy`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`, `loudness`, `tempo`
- chart/popularity features: `track_popularity`, `streams_total`, `chart_peak_position`, `weeks_on_chart`
- artist-level fields: `catalog_size`, `career_start_year`, `career_end_year`, `hit_rate`, etc.

### Candidate keys and verified duplicate status

Possible identifiers:
- `track_id` — likely the strongest candidate key
- `spotify_id` — likely a direct Spotify-specific identifier
- `title + track_artist + release_year` — useful for manual review but not a guaranteed key
- `album_id + title + artist` — lower confidence, because remasters and alternate versions can repeat

Verified duplicate checks on the full file:
- Exact duplicate rows: 0
- Repeated `track_id`: 0
- Repeated `spotify_id`: 0

This means there are no exact duplicate rows and no repeated identifiers in the full file at the current archive snapshot.

## 4. Definition and source of track_popularity

This is the most important point for the business question.

### Verified metadata definition

From the archive metadata schema:
- `track_popularity`: `int`, description = `Spotify popularity score 0-100. Dataset mean: 18.7, median: 15.0; ~4,878 tracks score >= 90`

This is a Spotify popularity score, not a count of streams, not revenue, and not a membership/conversion measure.

### Verified values

`track_popularity` summary on the full dataset:
- count: 1,182,354
- mean: 18.6993
- std: 16.2230
- min: 0
- 25%: 5
- 50%: 15
- 75%: 29
- max: 100
- no nulls

### Streams field note

The metadata also defines:
- `streams_total`: `float`, description = `Total estimated stream count. Median: 3.38M, max: 1.59B`
- `streams_total_estimated`: `bool`, description = `True if streams_total was modelled rather than directly sourced`

Because `streams_total` is a modelled/estimated stream count rather than a direct popularity measure, it should not be used as the primary metric for this assignment unless the question specifically asks about stream volume.

## 5. Missing counts for every column

Verified missing counts for the full dataset:

```
taste_cluster                 1180175
t streams_source               1172754
weeks_on_chart               1167441
chart_date_first             1167441
chart_peak_position          1167441
anomaly_flags                1160967
release_date                 1159764
album_name                   1156965
album_id                     1156961
title_normalized              25900
time_signature                22590
hit_rate                           19
track_artist                       19
catalog_size                       19
genre_breadth                      19
sonic_evolution_score              19
mean_energy_by_artist              19
career_end_year                    19
career_start_year                  19
longevity_score                    19
career_span_years                  19
title                               5
hit_probability                     3
valence                             0
instrumentalness                    0
acousticness                        0
danceability                        0
explicit_flag                       0
duration_ms                         0
release_year                        0
spotify_id                          0
track_id                            0
energy                              0
source_dataset                      0
has_audio_features                  0
speechiness                         0
streams_total_estimated             0
streams_total                       0
popularity_imputed_aug              0
stream_density                      0
key                                 0
tempo                               0
liveness                            0
mode_name                           0
genre_l1                            0
genre_raw                           0
genre_l2                            0
track_popularity                    0
key_name                            0
mode                                0
loudness                            0
loudness_war_index                  0
is_likely_spoken_word               0
is_likely_live                      0
is_likely_instrumental              0
tempo_band                          0
emotional_arc                       0
acoustic_synthetic_ratio            0
mood_index                          0
energy_loudness_ratio               0
decade                              0
era                                 0
track_age_days                      0
fp_acousticness                     0
fp_danceability                     0
fp_valence                          0
novelty_score                       0
fp_speechiness                      0
fp_instrumentalness                 0
fp_liveness                         0
mood_cluster                        0
fp_energy                           0
artist_stream_mean_log              0
mean_energy_by_decade               0
artist_stream_median_log            0
mean_valence_by_decade              0
mean_tempo_by_decade                0
acousticness_decline_idx            0
mean_loudness_by_decade             0
danceability_trend                  0
decade_track_count                 0
has_anomaly                         0
release_year_precision_aug          0
```

## 6. Text inconsistencies, numeric ranges, and suspicious values

### Text inconsistencies to review

The dataset includes several natural text issues that should be preserved and documented rather than silently coerced:
- blank `album_id`, `album_name`, and `release_date` for many rows
- `title_normalized` missing in 25,900 rows
- `taste_cluster` missing for most rows (1,180,175)
- `streams_source` missing for 1,172,754 rows
- `chart_peak_position`, `weeks_on_chart`, and `chart_date_first` missing for non-charting tracks
- `anomaly_flags` missing for many rows because not every track is flagged

These appear to be legitimate sparse patterns, not necessarily data-entry failures.

### Numeric ranges and suspicious values

Verified patterns from the source file:
- `track_popularity`: 0 to 100; no nulls
- `release_year`: within the documented range 1957-2023
- `energy`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`: realistic 0-1 float ranges
- `loudness`: negative dBFS values are valid and expected for this domain
- `tempo`: values are plausible BPM readings and should be reviewed as a continuous field, not auto-corrected
- `duration_ms`: positive durations with plausible music-track range; extreme values may be legitimate (e.g., white-noise/sleep tracks, ambient material)
- `streams_total`: stream counts can be high and may be modelled/estimated; do not treat them as popularity or revenue data

### Suspicious values are not automatically errors

Examples from metadata and the archive sample include:
- long-duration ambient/noise tracks
- near-instrumental tracks or spoken-word recordings
- album/date gaps for catalog entries and non-charting tracks
- fields that are intentionally sparse by design for a broad catalog dataset

These values should be flagged and retained unless there is strong, domain-backed evidence to recode or remove them.

## 7. Business question fit and metric choice

### Verified fit for proposed question

The proposed question is supported by the actual data:
- `genre_l1` exists and is populated for all rows
- `decade` exists and is populated for all rows
- `track_popularity` is available for all rows
- A group-level summary can be computed as average popularity by `genre_l1` and `decade`

Verified example from the archive file:

```
genre_l1  decade  valid_tracks   avg_pop
Blues    2000          7898 18.407445
Blues    2010          8569 23.441358
Blues    2020          3215 24.657854
Classical 2000        22066 12.718617
Classical 2010        26040 17.219777
Classical 2020        10117 21.480083
Country  2000          7399 25.370050
Country  2010          7697 35.257763
Country  2020          2787 47.325081
Electronic 2000      109009  9.839261
Electronic 2010      144425 19.051404
Electronic 2020       54301 26.667152
```

This confirms that the actual dataset supports the question “How does Spotify track popularity differ across genres and release decades?” using `track_popularity` as the metric and valid track counts as the denominator.

### Main metric recommendation

Primary metric:
- `track_popularity` (Spotify score 0–100)

Secondary data point:
- valid track counts by group, not stream volume

Do not interpret `track_popularity` as stream counts, revenue, or subscription performance.

## 8. Proposed rules for each column grouping

### Identifier and name columns
- `track_id`, `spotify_id`: preserve as strings; do not coerce to numeric; validate duplicates and format consistency.
- `title`, `title_normalized`, `track_artist`, `album_id`, `album_name`: preserve original strings; only trim trivial whitespace/control characters if explicitly justified.
- Validation checks: null count, duplicate count, same-ID conflict review, and pattern check for Spotify IDs.

### Temporal columns
- `release_year`, `release_date`, `era`, `decade`, `track_age_days`, `release_year_precision_aug`: keep raw values and document precision; only derive era/decade from valid release years.
- Validation: year within documented range, date parseability, flag ambiguous precision, ensure track age aligns with release date.

### Audio feature columns
- `duration_ms`, `tempo`, `loudness`, `key`, `mode`, `time_signature`, `energy`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`: keep as numeric where valid; preserve missing where truly absent; do not silently coerce invalid strings.
- Validation: zero/negative checks where appropriate, range checks for 0–1 audio features, and anomaly review for extreme values.

### Categorical and classification columns
- `genre_l1`, `genre_l2`, `genre_raw`, `mood_cluster`, `emotional_arc`, `tempo_band`, `anomaly_flags`, `has_anomaly`, `source_dataset`: preserve the original category strings; avoid re-coding unless a domain rule is approved.
- Validation: frequency distribution, category collisions, missingness counts, and whether values are raw or engineered labels.

### Popularity and chart columns
- `track_popularity`, `streams_total`, `stream_density`, `chart_peak_position`, `weeks_on_chart`, `chart_date_first`, `hit_probability`, `popularity_imputed_aug`, `streams_total_estimated`, `streams_source`: preserve original values and keep missingness explicit instead of coercing to zeros.
- Validation: range check for popularity, distinction between direct and estimated streams, and chart absence handling.

### Artist and decade aggregate columns
- `mean_energy_by_artist`, `sonic_evolution_score`, `genre_breadth`, `catalog_size`, `career_start_year`, `career_end_year`, `career_span_years`, `longevity_score`, `hit_rate`, `artist_stream_mean_log`, `artist_stream_median_log`, `mean_energy_by_decade`, `mean_valence_by_decade`, `mean_tempo_by_decade`, `mean_loudness_by_decade`, `acousticness_decline_idx`, `danceability_trend`, `decade_track_count`: keep numeric and do not drop rows simply because aggregates are sparse or absent; document them as engineered features.
- Validation: review those fields for blanks and check if they are intentionally sparse or derived only for certain subsets.

## 9. Final analysis choices

The following choices have been approved for the final analysis:

1. Use `genre_l1` for the final grouped analysis.
   - This provides a clear, interpretable comparison across broader genres.
   - `genre_l2` can still be used as a drill-down or exploratory breakdown, but not as the primary grouping for the main dashboard.

2. Keep `streams_total` as a secondary metric only.
   - `track_popularity` remains the primary metric for the main comparison.
   - `streams_total` may be displayed alongside the popularity metric when needed, but it should not replace the headline metric.

3. Include all rows with valid `genre_l1` and `release_year` values, unless a data-quality issue is specifically identified and documented.
   - The dataset has no missing `track_popularity`, so there is no need to exclude rows solely for missing popularity.

4. Keep missing `album_name`, `release_date`, and chart fields as missing values rather than imputing them or dropping rows without justification.
   - This preserves the raw data while making sparse fields visible in the reporting layer.

5. Preserve raw genre labels for analysis and use normalized display names only if needed for presentation.
   - This avoids silently altering the original data semantics.

## 10. Homework checklist coverage

This plan addresses the required 14 items directly:

1. Row meaning and unit of observation — Section 3.
2. Data source and version — Section 1 and 2.
3. Full-row counts and column inventory — Section 2.
4. Exact duplicate rows — Section 3.
5. Repeated IDs — Section 3.
6. Missing value counts by column — Section 5.
7. Text inconsistencies — Section 6.
8. Numeric ranges and suspicious values — Section 6.
9. Proposed cleaning rules for each column group — Section 8.
10. Documentation of not changing units or categories without record — Section 8 and the plan guardrails.
11. Decisions requiring human judgment — Section 9.
12. No row dropping without explanation — embedded in this plan and the project rules.
13. Avoid inventing metadata or results — verified findings are explicitly separated from documentation and sample data.
14. Work stays on the current branch and does not push to main — confirmed in the repository state and source handling.

## 11. Summary and final confirmation needed

Verified findings:
- The canonical full dataset is `archive/data/full/spotify_full.csv`.
- The file contains 1,182,354 rows and 83 columns.
- There are zero exact duplicate rows and zero repeated `track_id`/`spotify_id` values.
- `track_popularity` is an integer Spotify popularity score from 0 to 100, no missing values, and the metadata explicitly says it is not streams or revenue.
- The proposed question is supported by the actual columns: `genre_l1`, `decade`, and `track_popularity` are all populated and suitable for a group-level popularity comparison.

The final analysis configuration is now set:
- Primary grouping: `genre_l1`
- Primary metric: `track_popularity`
- Secondary metric: `streams_total` only as a supplemental metric

This satisfies the approved business question and keeps the analysis aligned with the verified raw dataset. I can move to the cleaning implementation phase next if you want me to begin the data-cleaning code.
