# Spotify Cleaning Transformation Report

Generated: 2026-10-02T04:13:32.309030+00:00

## Source preservation

- Input: `spotify_full.csv`
- Output: `spotify_clean.csv`
- Source SHA-256 before: `dd195436d5943929a1321d111b45b5560ae0ec4a743f187f58f3bf5b82d1e914`
- Source SHA-256 after: `dd195436d5943929a1321d111b45b5560ae0ec4a743f187f58f3bf5b82d1e914`
- Source size before/after: 816973617 / 816973617 bytes
- Source mtime (ns) before/after: 1785341404000000000 / 1785341404000000000
- Result: source file fingerprint is unchanged.

## Transformation summaries

### Baseline

- Row count: 1182354
- Columns changed in this step: None (baseline)
- Exact duplicate rows: 0
- Duplicate `track_id` values: 0
- Duplicate `spotify_id` values: 0

### After datetime conversion

- Row count: 1182354
- Columns changed in this step: `release_date`, `chart_date_first`
- Exact duplicate rows: 0
- Duplicate `track_id` values: 0
- Duplicate `spotify_id` values: 0

### After track_artist strip

- Row count: 1182354
- Columns changed in this step: `track_artist`
- Exact duplicate rows: 0
- Duplicate `track_id` values: 0
- Duplicate `spotify_id` values: 0

## Missing-value counts by stage

| Column | Baseline | After datetime conversion | After track_artist strip | Change from baseline |
|---|---|---|---|---|
| track_id | 0 | 0 | 0 | 0 |
| spotify_id | 0 | 0 | 0 | 0 |
| title | 5 | 5 | 5 | 0 |
| title_normalized | 25888 | 25888 | 25888 | 0 |
| track_artist | 19 | 19 | 19 | 0 |
| album_id | 1156961 | 1156961 | 1156961 | 0 |
| album_name | 1156965 | 1156965 | 1156965 | 0 |
| release_year | 0 | 0 | 0 | 0 |
| release_date | 1159764 | 1159764 | 1159764 | 0 |
| duration_ms | 0 | 0 | 0 | 0 |
| explicit_flag | 0 | 0 | 0 | 0 |
| has_audio_features | 0 | 0 | 0 | 0 |
| source_dataset | 0 | 0 | 0 | 0 |
| energy | 0 | 0 | 0 | 0 |
| valence | 0 | 0 | 0 | 0 |
| danceability | 0 | 0 | 0 | 0 |
| acousticness | 0 | 0 | 0 | 0 |
| instrumentalness | 0 | 0 | 0 | 0 |
| speechiness | 0 | 0 | 0 | 0 |
| liveness | 0 | 0 | 0 | 0 |
| loudness | 0 | 0 | 0 | 0 |
| tempo | 0 | 0 | 0 | 0 |
| key | 0 | 0 | 0 | 0 |
| key_name | 0 | 0 | 0 | 0 |
| mode | 0 | 0 | 0 | 0 |
| mode_name | 0 | 0 | 0 | 0 |
| time_signature | 22590 | 22590 | 22590 | 0 |
| genre_l1 | 0 | 0 | 0 | 0 |
| genre_l2 | 0 | 0 | 0 | 0 |
| genre_raw | 0 | 0 | 0 | 0 |
| track_popularity | 0 | 0 | 0 | 0 |
| streams_total | 0 | 0 | 0 | 0 |
| streams_source | 1172754 | 1172754 | 1172754 | 0 |
| streams_total_estimated | 0 | 0 | 0 | 0 |
| stream_density | 0 | 0 | 0 | 0 |
| chart_peak_position | 1167441 | 1167441 | 1167441 | 0 |
| weeks_on_chart | 1167441 | 1167441 | 1167441 | 0 |
| chart_date_first | 1167441 | 1167441 | 1167441 | 0 |
| popularity_imputed_aug | 0 | 0 | 0 | 0 |
| track_age_days | 0 | 0 | 0 | 0 |
| era | 0 | 0 | 0 | 0 |
| decade | 0 | 0 | 0 | 0 |
| energy_loudness_ratio | 0 | 0 | 0 | 0 |
| mood_index | 0 | 0 | 0 | 0 |
| acoustic_synthetic_ratio | 0 | 0 | 0 | 0 |
| emotional_arc | 0 | 0 | 0 | 0 |
| tempo_band | 0 | 0 | 0 | 0 |
| is_likely_instrumental | 0 | 0 | 0 | 0 |
| is_likely_live | 0 | 0 | 0 | 0 |
| is_likely_spoken_word | 0 | 0 | 0 | 0 |
| loudness_war_index | 0 | 0 | 0 | 0 |
| novelty_score | 0 | 0 | 0 | 0 |
| hit_probability | 3 | 3 | 3 | 0 |
| mood_cluster | 0 | 0 | 0 | 0 |
| taste_cluster | 1180175 | 1180175 | 1180175 | 0 |
| fp_energy | 0 | 0 | 0 | 0 |
| fp_valence | 0 | 0 | 0 | 0 |
| fp_danceability | 0 | 0 | 0 | 0 |
| fp_acousticness | 0 | 0 | 0 | 0 |
| fp_instrumentalness | 0 | 0 | 0 | 0 |
| fp_speechiness | 0 | 0 | 0 | 0 |
| fp_liveness | 0 | 0 | 0 | 0 |
| mean_energy_by_artist | 19 | 19 | 19 | 0 |
| sonic_evolution_score | 19 | 19 | 19 | 0 |
| genre_breadth | 19 | 19 | 19 | 0 |
| catalog_size | 19 | 19 | 19 | 0 |
| career_start_year | 19 | 19 | 19 | 0 |
| career_end_year | 19 | 19 | 19 | 0 |
| career_span_years | 19 | 19 | 19 | 0 |
| longevity_score | 19 | 19 | 19 | 0 |
| hit_rate | 19 | 19 | 19 | 0 |
| artist_stream_mean_log | 0 | 0 | 0 | 0 |
| artist_stream_median_log | 0 | 0 | 0 | 0 |
| mean_energy_by_decade | 0 | 0 | 0 | 0 |
| mean_valence_by_decade | 0 | 0 | 0 | 0 |
| mean_tempo_by_decade | 0 | 0 | 0 | 0 |
| mean_loudness_by_decade | 0 | 0 | 0 | 0 |
| acousticness_decline_idx | 0 | 0 | 0 | 0 |
| danceability_trend | 0 | 0 | 0 | 0 |
| decade_track_count | 0 | 0 | 0 | 0 |
| anomaly_flags | 1160967 | 1160967 | 1160967 | 0 |
| has_anomaly | 0 | 0 | 0 | 0 |
| release_year_precision_aug | 0 | 0 | 0 | 0 |

## Datetime conversion

### `release_date`

- Current type: string/object input; proposed in-memory type: `datetime64[ns]`.
- Non-null source values: 22590
- Successful conversions: 22590
- Failed conversions: 0
- Missing before/after: 1159764 / 1159764

### `chart_date_first`

- Current type: string/object input; proposed in-memory type: `datetime64[ns]`.
- Non-null source values: 14913
- Successful conversions: 14913
- Failed conversions: 0
- Missing before/after: 1167441 / 1167441

## Text transformation

- `track_artist`: `.str.strip()` changed 30 non-null values; only outer whitespace was removed.
- `title`, genre fields, `track_id`, `spotify_id`, existing `title_normalized`, and `anomaly_flags` were asserted unchanged.
- Missing `title_normalized` values were retained; no transliteration or derivation was performed.

## Validated values retained without alteration

- `track_popularity` range: 0.0 to 100.0.
- `duration_ms` range: 2073.0 to 6000495.0; short (<=4 seconds): 7; long (>=100 minutes): 6.
- `release_year` range: 1957 to 2023; 1957 records: 2.
- All core audio features passed the [0, 1] validation and were retained unchanged.
- Missing `anomaly_flags` values were retained unchanged; no text was filled in.
- No rows were removed and no missing numeric values were imputed.

## CSV reload contract

`spotify_clean.csv` stores dates as ISO `YYYY-MM-DD` strings. Reload it with `parse_dates=['release_date', 'chart_date_first']` to restore the validated datetime columns.
