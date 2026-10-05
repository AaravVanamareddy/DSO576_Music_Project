# Cleaning validation report

## Outcome

The approved cleaning rules were applied with pandas. No row or original column was removed. The raw source remained unchanged.

| Control | Expected | Actual | Status |
| --- | --- | --- | --- |
| Raw SHA-256 before | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | PASS |
| Raw SHA-256 after | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | PASS |
| Starting rows | 1,182,354 | 1,182,354 | PASS |
| Final rows | 1,182,354 | 1,182,354 | PASS |
| Original columns retained | 83 | 83 | PASS |
| Final columns | 87 | 87 | PASS |
| Cleaned-file SHA-256 | Recorded | EA931D18C19C5FCBB3DB571411EB7FBC3628D289B8444BB40BB5D56A75A7229B | PASS |

## Duplicate and identifier checks

| Check | Actual | Status |
| --- | --- | --- |
| Exact duplicate rows beyond first | 0 | PASS |
| Repeated track_id values | 0 | PASS |
| Repeated spotify_id values | 0 | PASS |
| Repeated ID pairs | 0 | PASS |

## Missing values before and after

| Original column | Before | After | Difference |
| --- | --- | --- | --- |
| track_id | 0 | 0 | 0 |
| spotify_id | 0 | 0 | 0 |
| title | 5 | 5 | 0 |
| title_normalized | 25,888 | 25,888 | 0 |
| track_artist | 19 | 19 | 0 |
| album_id | 1,156,961 | 1,156,961 | 0 |
| album_name | 1,156,965 | 1,156,965 | 0 |
| release_year | 0 | 0 | 0 |
| release_date | 1,159,764 | 1,159,764 | 0 |
| duration_ms | 0 | 0 | 0 |
| explicit_flag | 0 | 0 | 0 |
| has_audio_features | 0 | 0 | 0 |
| source_dataset | 0 | 0 | 0 |
| energy | 0 | 0 | 0 |
| valence | 0 | 0 | 0 |
| danceability | 0 | 0 | 0 |
| acousticness | 0 | 0 | 0 |
| instrumentalness | 0 | 0 | 0 |
| speechiness | 0 | 0 | 0 |
| liveness | 0 | 0 | 0 |
| loudness | 0 | 0 | 0 |
| tempo | 0 | 0 | 0 |
| key | 0 | 0 | 0 |
| key_name | 0 | 0 | 0 |
| mode | 0 | 0 | 0 |
| mode_name | 0 | 0 | 0 |
| time_signature | 22,590 | 22,590 | 0 |
| genre_l1 | 0 | 0 | 0 |
| genre_l2 | 0 | 0 | 0 |
| genre_raw | 0 | 0 | 0 |
| track_popularity | 0 | 0 | 0 |
| streams_total | 0 | 0 | 0 |
| streams_source | 1,172,754 | 1,172,754 | 0 |
| streams_total_estimated | 0 | 0 | 0 |
| stream_density | 0 | 0 | 0 |
| chart_peak_position | 1,167,441 | 1,167,441 | 0 |
| weeks_on_chart | 1,167,441 | 1,167,441 | 0 |
| chart_date_first | 1,167,441 | 1,167,441 | 0 |
| popularity_imputed_aug | 0 | 0 | 0 |
| track_age_days | 0 | 0 | 0 |
| era | 0 | 0 | 0 |
| decade | 0 | 0 | 0 |
| energy_loudness_ratio | 0 | 0 | 0 |
| mood_index | 0 | 0 | 0 |
| acoustic_synthetic_ratio | 0 | 0 | 0 |
| emotional_arc | 0 | 0 | 0 |
| tempo_band | 0 | 0 | 0 |
| is_likely_instrumental | 0 | 0 | 0 |
| is_likely_live | 0 | 0 | 0 |
| is_likely_spoken_word | 0 | 0 | 0 |
| loudness_war_index | 0 | 0 | 0 |
| novelty_score | 0 | 0 | 0 |
| hit_probability | 3 | 3 | 0 |
| mood_cluster | 0 | 0 | 0 |
| taste_cluster | 1,180,175 | 1,180,175 | 0 |
| fp_energy | 0 | 0 | 0 |
| fp_valence | 0 | 0 | 0 |
| fp_danceability | 0 | 0 | 0 |
| fp_acousticness | 0 | 0 | 0 |
| fp_instrumentalness | 0 | 0 | 0 |
| fp_speechiness | 0 | 0 | 0 |
| fp_liveness | 0 | 0 | 0 |
| mean_energy_by_artist | 19 | 19 | 0 |
| sonic_evolution_score | 19 | 19 | 0 |
| genre_breadth | 19 | 19 | 0 |
| catalog_size | 19 | 19 | 0 |
| career_start_year | 19 | 19 | 0 |
| career_end_year | 19 | 19 | 0 |
| career_span_years | 19 | 19 | 0 |
| longevity_score | 19 | 19 | 0 |
| hit_rate | 19 | 19 | 0 |
| artist_stream_mean_log | 0 | 0 | 0 |
| artist_stream_median_log | 0 | 0 | 0 |
| mean_energy_by_decade | 0 | 0 | 0 |
| mean_valence_by_decade | 0 | 0 | 0 |
| mean_tempo_by_decade | 0 | 0 | 0 |
| mean_loudness_by_decade | 0 | 0 | 0 |
| acousticness_decline_idx | 0 | 0 | 0 |
| danceability_trend | 0 | 0 | 0 |
| decade_track_count | 0 | 0 | 0 |
| anomaly_flags | 1,160,967 | 1,160,967 | 0 |
| has_anomaly | 0 | 0 | 0 |
| release_year_precision_aug | 0 | 0 | 0 |

## Rule results

| rule | check | metric | expected | actual | status |
| --- | --- | --- | --- | --- | --- |
| 1 | canonical track_id | repeated track_id values | 0 | 0 | PASS |
| 1 | spotify_id validation | repeated spotify_id values | 0 | 0 | PASS |
| 1 | ID-pair validation | repeated ID pairs | 0 | 0 | PASS |
| 2 | retain all rows | final rows | 1182354 | 1182354 | PASS |
| 2 | exact duplicates | duplicate rows beyond first | 0 | 0 | PASS |
| 3 | retain original columns | original columns retained | 83 | 83 | PASS |
| 4 | string typing | original text columns preserved | all | all | PASS |
| 5 | nullable conversions | total conversion failures | 0 | 0 | PASS |
| 6 | trim track_artist | values changed | 30 | 30 | PASS |
| 7 | remove title DEL | values changed | 1 | 1 | PASS |
| 8 | retain missing title/artist | union count | 20 | 20 | PASS |
| 9 | dashboard eligibility | False count | 20 | 20 | PASS |
| 10 | long duration flag | True count | 407 | 407 | PASS |
| 11 | invalid time signature flag | True count | 1228 | 1228 | PASS |
| 12 | missing time signature | missing count | 22590 | 22590 | PASS |
| 13 | streams_status direct | count | 9600 | 9600 | PASS |
| 13 | streams_status estimated | count | 1172754 | 1172754 | PASS |
| 13 | streams_status missing | count | 0 | 0 | PASS |
| 13 | streams_status unknown | count | 0 | 0 | PASS |
| 14 | preserve missing streams | missing streams | 0 | 0 | PASS |
| 15 | retain unusual values | rows removed for unusual values | 0 | 0 | PASS |
| 16 | retain hit_probability | column present | True | True | PASS |
| 17 | protect raw source | SHA-256 unchanged | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 | PASS |

## Important numeric ranges

| Column | Minimum | Maximum |
| --- | --- | --- |
| release_year | 1,957 | 2,023 |
| duration_ms | 2,073 | 6,000,495 |
| time_signature | 0 | 5 |
| track_popularity | 0 | 100 |
| streams_total | 44,962 | 1,593,270,737 |
| energy | 0 | 1 |
| valence | 0 | 1 |
| danceability | 0 | 0.993 |
| acousticness | 0 | 0.996 |
| instrumentalness | 0 | 1 |
| speechiness | 0 | 0.971 |
| liveness | 0 | 1 |
| loudness | -58.1 | 0 |
| tempo | 40 | 249.993 |

## streams_status counts

| Status | Count |
| --- | --- |
| direct | 9,600 |
| estimated | 1,172,754 |
| missing | 0 |
| unknown_status | 0 |

## Manual record checks

The current manual_record_checks.md contains 5 Pass and 0 Fail results. Expected Result text is preserved, Actual Result is refreshed from the current outputs, and completed human-reviewed Pass/Fail values are not overwritten on rerun.

Numeric comparisons use an approved absolute tolerance of 1e-12. For the missing-title/artist record, novelty_score serializes as 0.2319888770580291 instead of 0.23198887705802917; the difference is approximately 5.6e-17 and is therefore numerically equivalent.

| Case | track_id | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Artist boundary whitespace | spotify:track:5cXq69EbEhTaWE7lUTOwsK | The row remains in the dataset. track_artist becomes "The Wanderer" after removing the trailing space. All other artist characters and original data values remain unchanged. streams_status is "estimated", and dashboard_eligible is True. | Matched exactly one cleaned row. track_artist='The Wanderer'; title="We're All Going Home"; spotify_id='5cXq69EbEhTaWE7lUTOwsK'; dashboard_eligible=True; streams_status='estimated'. All other original fields remain equivalent after approved type conversion, using 1e-12 tolerance for floating-point values. | Pass |
| Title control character | spotify:track:4o1ZHV2KKDlRhFbL3Cn8Re | The row remains in the dataset. The DEL control character \x7f is removed from the title, and the resulting adjacent spaces are reduced to one space. The cleaned title is "Merry Shrovetide (sung in russian) (Power of Evil)". All other meaningful capitalization, spelling, and punctuation remain unchanged. streams_status is "estimated", and dashboard_eligible is True. | Matched exactly one cleaned row. title='Merry Shrovetide (sung in russian) (Power of Evil)'; the title contains no U+007F and has one space at the removal boundary; track_artist='Ivan Petrov'; dashboard_eligible=True; streams_status='estimated'. | Pass |
| Missing title and artist | spotify:track:3VKFip3OdAvv4OfNTgFWeQ | The row remains in the dataset. title and track_artist remain missing and are not filled with invented values. The identifiers, genre, duration, popularity, streams, and other available fields remain unchanged. dashboard_eligible is False, streams_status is "estimated", and the missing time_signature remains missing. | The row remains in the dataset. title and track_artist remain missing; spotify_id='3VKFip3OdAvv4OfNTgFWeQ'; genre='Latin/Reggaeton/latin'; duration_ms=252773; track_popularity=0; streams_total=3699500.75; time_signature remains missing; dashboard_eligible=False; streams_status='estimated'. novelty_score is 0.2319888770580291 in the cleaned CSV versus original 0.23198887705802917; the absolute serialization difference is 8.33e-17 and is numerically equivalent within the approved 1e-12 tolerance. | Pass |
| Duration over one hour | spotify:track:1saXdvEAafdRzUphXBzSHg | The row remains in the dataset, and duration_ms remains 4,120,258. No shortening, deletion, or replacement is applied because the long duration may be valid for sleep audio. duration_over_one_hour is True, streams_status is "estimated", and dashboard_eligible is True. | Matched exactly one cleaned row. duration_ms=4120258; duration_over_one_hour=True; title='Ocean Waves for Sleep'; track_artist='Ocean Waves For Sleep'; streams_status='estimated'; dashboard_eligible=True. The row was retained without shortening, deletion, or duration replacement. | Pass |
| Nonpositive time signature | spotify:track:2bRKxuH1o7pTmb1y4GfdEc | The row remains in the dataset, and time_signature remains 0. It is not corrected or replaced without supporting evidence. invalid_time_signature is True, duration_over_one_hour is False, streams_status is "estimated", and dashboard_eligible is True. | Matched exactly one cleaned row. time_signature=0; invalid_time_signature=True; duration_over_one_hour=False; title='Clean White Noise - Loopable with no fade'; streams_status='estimated'; dashboard_eligible=True. The row and nonpositive time signature were retained without correction or replacement. | Pass |

## Dashboard limitations

- hit_probability is retained for source preservation but was not used in any derived flag, stream status, sample-selection rule, or validation decision.
- Direct and estimated streams remain distinguishable through streams_status.
- Missing streams are not converted to zero.
- Unusual durations and time signatures remain unchanged and are flagged only.
- Results support historical comparison, not causal promotion claims or automatic hit prediction.
