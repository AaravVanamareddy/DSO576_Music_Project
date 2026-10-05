# Spotify source data audit

## Scope and method

This report records observed results from a read-only pandas audit of the complete source CSV. No row or value was modified, filtered, deduplicated, or cleaned. No cleaned dataset was created. Recommendations and approval items are separated from observations.

## 1. Source controls

| Control | Observed result |
| --- | --- |
| Parsed data rows (header excluded) | 1,182,354 |
| Columns | 83 |
| File size (bytes) | 816,973,617 |
| File size (MiB) | 779.13 |
| SHA-256 | DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914 |

Observed: row count match with metadata = True; column count match = True.

## 2. Actual columns and metadata comparison

Actual columns in file order:

track_id, spotify_id, title, title_normalized, track_artist, album_id, album_name, release_year, release_date, duration_ms, explicit_flag, has_audio_features, source_dataset, energy, valence, danceability, acousticness, instrumentalness, speechiness, liveness, loudness, tempo, key, key_name, mode, mode_name, time_signature, genre_l1, genre_l2, genre_raw, track_popularity, streams_total, streams_source, streams_total_estimated, stream_density, chart_peak_position, weeks_on_chart, chart_date_first, popularity_imputed_aug, track_age_days, era, decade, energy_loudness_ratio, mood_index, acoustic_synthetic_ratio, emotional_arc, tempo_band, is_likely_instrumental, is_likely_live, is_likely_spoken_word, loudness_war_index, novelty_score, hit_probability, mood_cluster, taste_cluster, fp_energy, fp_valence, fp_danceability, fp_acousticness, fp_instrumentalness, fp_speechiness, fp_liveness, mean_energy_by_artist, sonic_evolution_score, genre_breadth, catalog_size, career_start_year, career_end_year, career_span_years, longevity_score, hit_rate, artist_stream_mean_log, artist_stream_median_log, mean_energy_by_decade, mean_valence_by_decade, mean_tempo_by_decade, mean_loudness_by_decade, acousticness_decline_idx, danceability_trend, decade_track_count, anomaly_flags, has_anomaly, release_year_precision_aug

| Comparison | Observed result |
| --- | --- |
| Metadata column count | 83 |
| Actual columns absent from metadata columns list | None |
| Metadata columns absent from source | None |
| Order matches metadata columns list | True |
| Actual columns without detailed metadata schema entry | title_normalized, album_id, album_name, release_date, explicit_flag, has_audio_features, source_dataset, mode_name, time_signature, streams_source, chart_date_first |

## 3. Release-year range

| Measure | Observed result |
| --- | --- |
| Minimum valid numeric release year | 1,957 |
| Maximum valid numeric release year | 2,023 |
| Failed conversions | 0 |
| Outside documented 1957-2023 | 0 |

Observed resolution: the source range begins in 1,957, not a value inferred from documentation, and ends in 2,023.

## 4. Stream-estimation column

Observed: the real column name is streams_total_estimated. Present in source = True.

| Raw value | Count |
| --- | --- |
| True | 1,172,754 |
| False | 9,600 |

## 5. Data types and proposed conversions

| Column | Observed representation | Proposed type | Valid/nonmissing | Failed | Decision |
| --- | --- | --- | --- | --- | --- |
| track_id | CSV text; audited as pandas string | string identifier | 1,182,354 | 0 | Approval required |
| spotify_id | CSV text; audited as pandas string | string identifier | 1,182,354 | 0 | Approval required |
| title | CSV text; audited as pandas string | string | 1,182,349 | 0 | Approval required |
| track_artist | CSV text; audited as pandas string | string | 1,182,335 | 0 | Approval required |
| album_id | CSV text; audited as pandas string | string identifier | 25,393 | 0 | Approval required |
| album_name | CSV text; audited as pandas string | string | 25,389 | 0 | Approval required |
| release_year | CSV text; audited as pandas string | nullable integer | 1,182,354 | 0 | Approval required |
| release_date | CSV text; audited as pandas string | nullable date | 22,590 | 0 | Approval required |
| release_year_precision_aug | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |
| duration_ms | CSV text; audited as pandas string | nullable integer | 1,182,354 | 0 | Approval required |
| explicit_flag | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |
| has_audio_features | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |
| source_dataset | CSV text; audited as pandas string | categorical string | 1,182,354 | 0 | Approval required |
| energy | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| valence | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| danceability | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| acousticness | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| instrumentalness | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| speechiness | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| liveness | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| loudness | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| tempo | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| key | CSV text; audited as pandas string | nullable integer | 1,182,354 | 0 | Approval required |
| key_name | CSV text; audited as pandas string | categorical string | 1,182,354 | 0 | Approval required |
| mode | CSV text; audited as pandas string | nullable integer | 1,182,354 | 0 | Approval required |
| mode_name | CSV text; audited as pandas string | categorical string | 1,182,354 | 0 | Approval required |
| time_signature | CSV text; audited as pandas string | nullable integer | 1,159,764 | 0 | Approval required |
| genre_l1 | CSV text; audited as pandas string | categorical string | 1,182,354 | 0 | Approval required |
| genre_l2 | CSV text; audited as pandas string | categorical string | 1,182,354 | 0 | Approval required |
| genre_raw | CSV text; audited as pandas string | string | 1,182,354 | 0 | Approval required |
| track_popularity | CSV text; audited as pandas string | nullable integer | 1,182,354 | 0 | Approval required |
| popularity_imputed_aug | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |
| streams_total | CSV text; audited as pandas string | nullable float | 1,182,354 | 0 | Approval required |
| streams_source | CSV text; audited as pandas string | categorical string | 9,600 | 0 | Approval required |
| streams_total_estimated | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |
| anomaly_flags | CSV text; audited as pandas string | string | 21,387 | 0 | Approval required |
| has_anomaly | CSV text; audited as pandas string | nullable Boolean | 1,182,354 | 0 | Approval required |

Recommendation, not implemented: use nullable pandas types and never coerce missing values to zero or False. All conversions require approval.

## 6. Failed conversions

| Column | Failed conversion count | Representative failed raw values |
| --- | --- | --- |
| release_year | 0 | None |
| duration_ms | 0 | None |
| energy | 0 | None |
| valence | 0 | None |
| danceability | 0 | None |
| acousticness | 0 | None |
| instrumentalness | 0 | None |
| speechiness | 0 | None |
| liveness | 0 | None |
| loudness | 0 | None |
| tempo | 0 | None |
| key | 0 | None |
| mode | 0 | None |
| time_signature | 0 | None |
| track_popularity | 0 | None |
| streams_total | 0 | None |
| release_date | 0 | None |
| explicit_flag | 0 | None |
| has_audio_features | 0 | None |
| streams_total_estimated | 0 | None |
| popularity_imputed_aug | 0 | None |
| has_anomaly | 0 | None |
| release_year_precision_aug | 0 | None |

Observed: blanks are counted as missing, not as failed conversions.

## 7. Exact duplicates

| Measure | Observed result |
| --- | --- |
| Exact duplicate groups | 0 |
| Rows involved | 0 |
| Duplicate rows beyond first occurrence | 0 |

Method: two independent pandas row hashes were retained across chunks and covered every actual column. No duplicate was removed.

Decision requiring approval: whether exact duplicates may be removed remains unresolved.

## 8. Repeated identifiers

| Key | Repeated distinct keys | Rows involved | Excess rows | Examples |
| --- | --- | --- | --- | --- |
| track_id | 0 | 0 | 0 | None |
| spotify_id | 0 | 0 | 0 | None |
| (track_id, spotify_id) | 0 | 0 | 0 | None |

Observed: repeated IDs are separate from exact duplicates and may have different non-key values.

Decision requiring approval: canonical key and repeated-ID handling remain unresolved.

## 9. Missing values

| Column | Missing count | Missing percent | Whitespace-only subset |
| --- | --- | --- | --- |
| track_id | 0 | 0.0000% | 0 |
| spotify_id | 0 | 0.0000% | 0 |
| title | 5 | 0.0004% | 0 |
| title_normalized | 25,888 | 2.1895% | 0 |
| track_artist | 19 | 0.0016% | 0 |
| album_id | 1,156,961 | 97.8523% | 0 |
| album_name | 1,156,965 | 97.8527% | 0 |
| release_year | 0 | 0.0000% | 0 |
| release_date | 1,159,764 | 98.0894% | 0 |
| duration_ms | 0 | 0.0000% | 0 |
| explicit_flag | 0 | 0.0000% | 0 |
| has_audio_features | 0 | 0.0000% | 0 |
| source_dataset | 0 | 0.0000% | 0 |
| energy | 0 | 0.0000% | 0 |
| valence | 0 | 0.0000% | 0 |
| danceability | 0 | 0.0000% | 0 |
| acousticness | 0 | 0.0000% | 0 |
| instrumentalness | 0 | 0.0000% | 0 |
| speechiness | 0 | 0.0000% | 0 |
| liveness | 0 | 0.0000% | 0 |
| loudness | 0 | 0.0000% | 0 |
| tempo | 0 | 0.0000% | 0 |
| key | 0 | 0.0000% | 0 |
| key_name | 0 | 0.0000% | 0 |
| mode | 0 | 0.0000% | 0 |
| mode_name | 0 | 0.0000% | 0 |
| time_signature | 22,590 | 1.9106% | 0 |
| genre_l1 | 0 | 0.0000% | 0 |
| genre_l2 | 0 | 0.0000% | 0 |
| genre_raw | 0 | 0.0000% | 0 |
| track_popularity | 0 | 0.0000% | 0 |
| streams_total | 0 | 0.0000% | 0 |
| streams_source | 1,172,754 | 99.1881% | 0 |
| streams_total_estimated | 0 | 0.0000% | 0 |
| stream_density | 0 | 0.0000% | 0 |
| chart_peak_position | 1,167,441 | 98.7387% | 0 |
| weeks_on_chart | 1,167,441 | 98.7387% | 0 |
| chart_date_first | 1,167,441 | 98.7387% | 0 |
| popularity_imputed_aug | 0 | 0.0000% | 0 |
| track_age_days | 0 | 0.0000% | 0 |
| era | 0 | 0.0000% | 0 |
| decade | 0 | 0.0000% | 0 |
| energy_loudness_ratio | 0 | 0.0000% | 0 |
| mood_index | 0 | 0.0000% | 0 |
| acoustic_synthetic_ratio | 0 | 0.0000% | 0 |
| emotional_arc | 0 | 0.0000% | 0 |
| tempo_band | 0 | 0.0000% | 0 |
| is_likely_instrumental | 0 | 0.0000% | 0 |
| is_likely_live | 0 | 0.0000% | 0 |
| is_likely_spoken_word | 0 | 0.0000% | 0 |
| loudness_war_index | 0 | 0.0000% | 0 |
| novelty_score | 0 | 0.0000% | 0 |
| hit_probability | 3 | 0.0003% | 0 |
| mood_cluster | 0 | 0.0000% | 0 |
| taste_cluster | 1,180,175 | 99.8157% | 0 |
| fp_energy | 0 | 0.0000% | 0 |
| fp_valence | 0 | 0.0000% | 0 |
| fp_danceability | 0 | 0.0000% | 0 |
| fp_acousticness | 0 | 0.0000% | 0 |
| fp_instrumentalness | 0 | 0.0000% | 0 |
| fp_speechiness | 0 | 0.0000% | 0 |
| fp_liveness | 0 | 0.0000% | 0 |
| mean_energy_by_artist | 19 | 0.0016% | 0 |
| sonic_evolution_score | 19 | 0.0016% | 0 |
| genre_breadth | 19 | 0.0016% | 0 |
| catalog_size | 19 | 0.0016% | 0 |
| career_start_year | 19 | 0.0016% | 0 |
| career_end_year | 19 | 0.0016% | 0 |
| career_span_years | 19 | 0.0016% | 0 |
| longevity_score | 19 | 0.0016% | 0 |
| hit_rate | 19 | 0.0016% | 0 |
| artist_stream_mean_log | 0 | 0.0000% | 0 |
| artist_stream_median_log | 0 | 0.0000% | 0 |
| mean_energy_by_decade | 0 | 0.0000% | 0 |
| mean_valence_by_decade | 0 | 0.0000% | 0 |
| mean_tempo_by_decade | 0 | 0.0000% | 0 |
| mean_loudness_by_decade | 0 | 0.0000% | 0 |
| acousticness_decline_idx | 0 | 0.0000% | 0 |
| danceability_trend | 0 | 0.0000% | 0 |
| decade_track_count | 0 | 0.0000% | 0 |
| anomaly_flags | 1,160,967 | 98.1912% | 0 |
| has_anomaly | 0 | 0.0000% | 0 |
| release_year_precision_aug | 0 | 0.0000% | 0 |

Method: missing includes empty and whitespace-only fields. Literal text such as NA was not silently reclassified.

Decision requiring approval: no exclusion, fill, or imputation rule has been applied.

## 10. Numeric ranges and suspicious-value counts

| Column | Minimum | Maximum | Valid numeric | Missing | Suspicious flags |
| --- | --- | --- | --- | --- | --- |
| release_year | 1,957 | 2,023 | 1,182,354 | 0 | release_year outside documented 1957-2023=0; release_year outside plausible 1900-2026=0 |
| duration_ms | 2,073 | 6,000,495 | 1,182,354 | 0 | duration_ms nonpositive=0; duration_ms over 1 hour=407 |
| energy | 0 | 1 | 1,182,354 | 0 | energy outside 0-1=0 |
| valence | 0 | 1 | 1,182,354 | 0 | valence outside 0-1=0 |
| danceability | 0 | 0.993 | 1,182,354 | 0 | danceability outside 0-1=0 |
| acousticness | 0 | 0.996 | 1,182,354 | 0 | acousticness outside 0-1=0 |
| instrumentalness | 0 | 1 | 1,182,354 | 0 | instrumentalness outside 0-1=0 |
| speechiness | 0 | 0.971 | 1,182,354 | 0 | speechiness outside 0-1=0 |
| liveness | 0 | 1 | 1,182,354 | 0 | liveness outside 0-1=0 |
| loudness | -58.1 | 0 | 1,182,354 | 0 | loudness above 0 dBFS=0; loudness below -60 dBFS=0 |
| tempo | 40 | 249.993 | 1,182,354 | 0 | tempo nonpositive=0; tempo over 300 BPM=0 |
| key | 0 | 11 | 1,182,354 | 0 | key outside -1 to 11=0 |
| mode | 0 | 1 | 1,182,354 | 0 | mode outside 0-1=0 |
| time_signature | 0 | 5 | 1,159,764 | 22,590 | time_signature nonpositive=1,228; time_signature over 7=0 |
| track_popularity | 0 | 100 | 1,182,354 | 0 | track_popularity outside 0-100=0 |
| streams_total | 44,962 | 1,593,270,737 | 1,182,354 | 0 | streams_total negative=0; streams_total zero=0 |

Observed only: thresholds flag values for review and do not establish that a value is incorrect. Thresholds were documented range 1957-2023; popularity 0-100; negative streams; nonpositive or over-one-hour duration; normalized features outside 0-1; loudness above 0 or below -60 dBFS; tempo nonpositive or above 300 BPM; key outside -1 to 11; mode outside 0-1; and time signature nonpositive or above 7.

Decision requiring approval: validity bounds and any treatment of unusual values remain unresolved.

## 11. Important categorical and Boolean values

### genre_l1

Observed distinct raw values: 18.

| Raw value | Count |
| --- | --- |
| Electronic | 307,754 |
| Rock | 135,807 |
| Pop | 131,828 |
| Metal | 98,541 |
| Latin | 93,274 |
| World | 79,530 |
| Classical | 58,223 |
| Folk | 51,302 |
| R&B | 41,155 |
| Reggae | 37,573 |
| Gospel | 21,621 |
| Hip-Hop | 19,975 |
| Blues | 19,682 |
| Unknown | 18,090 |
| Country | 17,883 |
| Instrumental | 17,266 |
| Soundtrack | 16,907 |
| Jazz | 15,943 |

### genre_l2

Observed distinct raw values: 99.

| Raw value | Count |
| --- | --- |
| Mood Pop | 23,937 |
| Black Metal | 21,852 |
| Gospel | 21,621 |
| Ambient | 21,389 |
| Acoustic | 21,097 |
| Alt-Rock | 20,918 |
| Emo | 20,845 |
| Indian | 20,583 |
| K-Pop | 20,004 |
| New Age | 19,911 |
| Blues | 19,682 |
| Forró | 19,379 |
| Comedy | 19,334 |
| Spanish | 19,158 |
| Chill | 18,906 |
| Dancehall | 18,788 |
| Dub | 18,785 |
| Samba | 18,599 |
| French | 18,519 |
| Classical | 18,259 |
| Unknown | 18,090 |
| Death Metal | 18,038 |
| Deep House | 17,896 |
| Country | 17,883 |
| Sertanejo | 17,566 |
| Gothic Rock | 17,381 |
| Guitar | 17,266 |
| Dance | 17,212 |
| Power Pop | 17,161 |
| Garage | 17,123 |
| Disco | 16,987 |
| Pop Film | 16,907 |
| Hip-Hop | 16,677 |
| German | 16,417 |
| Folk | 16,170 |
| Hardcore | 15,993 |
| Jazz | 15,943 |
| Rock N Roll | 15,891 |
| Cantopop | 15,773 |
| Industrial | 15,245 |
| Minimal Techno | 15,198 |
| Funk | 15,136 |
| Opera | 15,079 |
| Tango | 15,069 |
| Hard Rock | 14,908 |
| Heavy Metal | 14,862 |
| Club | 14,678 |
| Drum and Bass | 14,591 |
| Grindcore | 14,509 |
| Singer-Songwriter | 14,035 |
| Piano | 13,784 |
| Ska | 13,776 |
| Groove | 13,366 |
| Psych-Rock | 12,789 |
| Hardstyle | 12,420 |
| Afrobeat | 12,395 |
| Breakbeat | 12,256 |
| Progressive House | 11,855 |
| Nordic | 11,616 |
| Electro | 11,406 |
| Trip-Hop | 11,285 |
| Indie Pop | 11,106 |
| Show Tunes | 11,101 |
| EDM | 10,671 |
| Trance | 9,592 |
| Party | 9,548 |
| Electronic | 9,369 |
| Soul | 8,974 |
| Techno | 7,898 |
| Punk Rock | 7,086 |
| Metal | 7,020 |
| Pop | 6,801 |
| Romantic | 6,518 |
| Metalcore | 6,267 |
| Punk | 6,197 |
| House | 5,233 |
| Chicago House | 5,170 |
| Dubstep | 4,774 |
| Detroit Techno | 3,920 |
| Rock | 3,319 |
| Gangsta Rap | 1,181 |
| Latin Hip-Hop | 1,140 |
| Neo Soul | 1,140 |
| Southern Hip-Hop | 1,097 |
| Electro House | 1,042 |
| Trap | 1,020 |
| Classic Rock | 1,008 |
| New Jack Swing | 1,001 |
| Tropical | 959 |
| Electropop | 904 |
| Pop EDM | 866 |
| Big Room | 861 |
| Album Rock | 858 |
| Urban Contemporary | 834 |
| Indie Rock | 831 |
| Latin Pop | 829 |
| Dance Pop | 742 |
| R&B | 704 |
| Reggaeton | 575 |

### genre_raw

Observed distinct raw values: 85.

| Raw value | Count |
| --- | --- |
| black-metal | 21,852 |
| gospel | 21,621 |
| ambient | 21,389 |
| acoustic | 21,097 |
| alt-rock | 20,918 |
| emo | 20,845 |
| indian | 20,583 |
| k-pop | 20,004 |
| new-age | 19,911 |
| blues | 19,682 |
| forro | 19,379 |
| comedy | 19,334 |
| spanish | 19,158 |
| chill | 18,906 |
| dancehall | 18,788 |
| dub | 18,785 |
| samba | 18,599 |
| french | 18,519 |
| classical | 18,259 |
| death-metal | 18,038 |
| deep-house | 17,896 |
| country | 17,883 |
| sleep | 17,851 |
| sertanejo | 17,566 |
| salsa | 17,501 |
| goth | 17,381 |
| guitar | 17,266 |
| dance | 17,212 |
| power-pop | 17,161 |
| garage | 17,123 |
| disco | 16,987 |
| pop-film | 16,907 |
| german | 16,417 |
| folk | 16,170 |
| hardcore | 15,993 |
| jazz | 15,943 |
| rock-n-roll | 15,891 |
| cantopop | 15,773 |
| hip-hop | 15,703 |
| industrial | 15,245 |
| minimal-techno | 15,198 |
| funk | 15,136 |
| opera | 15,079 |
| tango | 15,069 |
| heavy-metal | 14,862 |
| edm | 14,706 |
| club | 14,678 |
| drum-and-bass | 14,591 |
| grindcore | 14,509 |
| singer-songwriter | 14,035 |
| hard-rock | 13,800 |
| piano | 13,784 |
| ska | 13,776 |
| groove | 13,366 |
| psych-rock | 12,789 |
| hardstyle | 12,420 |
| afrobeat | 12,395 |
| breakbeat | 12,256 |
| swedish | 11,616 |
| electro | 11,406 |
| trip-hop | 11,285 |
| show-tunes | 11,101 |
| progressive-house | 10,589 |
| indie-pop | 10,022 |
| trance | 9,592 |
| party | 9,548 |
| pop | 9,531 |
| electronic | 9,369 |
| soul | 8,974 |
| techno | 7,898 |
| rock | 7,124 |
| punk-rock | 7,086 |
| metal | 7,020 |
| romance | 6,518 |
| metalcore | 6,267 |
| punk | 6,197 |
| sad | 6,086 |
| house | 5,233 |
| chicago-house | 5,170 |
| dubstep | 4,774 |
| rap | 4,272 |
| detroit-techno | 3,920 |
| r&b | 3,679 |
| latin | 3,503 |
| songwriter | 589 |

### streams_source

Observed distinct raw values: 3.

| Raw value | Count |
| --- | --- |
| <missing> | 1,172,754 |
| arc7_chart_dump | 9,499 |
| arc2_2023_top | 101 |

### source_dataset

Observed distinct raw values: 2.

| Raw value | Count |
| --- | --- |
| arc8_spotify_1m | 1,159,764 |
| tidytuesday_spotify | 22,590 |

### key_name

Observed distinct raw values: 12.

| Raw value | Count |
| --- | --- |
| G | 141,970 |
| C | 132,453 |
| D | 125,689 |
| A | 121,442 |
| C# | 115,493 |
| F | 95,868 |
| B | 93,014 |
| E | 92,741 |
| F# | 77,924 |
| A# | 77,588 |
| G# | 71,813 |
| D# | 36,359 |

### mode_name

Observed distinct raw values: 2.

| Raw value | Count |
| --- | --- |
| major | 748,845 |
| minor | 433,509 |

### era

Observed distinct raw values: 4.

| Raw value | Count |
| --- | --- |
| 2011-2020 | 538,636 |
| 2000-2010 | 493,729 |
| 2021+ | 145,907 |
| <2000 | 4,082 |

### tempo_band

Observed distinct raw values: 5.

| Raw value | Count |
| --- | --- |
| fast | 338,729 |
| slow | 288,895 |
| very_fast | 284,614 |
| medium | 245,452 |
| very_slow | 24,664 |

### emotional_arc

Observed distinct raw values: 4.

| Raw value | Count |
| --- | --- |
| Q1_euphoric | 425,793 |
| Q2_angry | 414,955 |
| Q3_depressed | 253,746 |
| Q4_content | 87,860 |

### explicit_flag

Observed distinct raw values: 2.

| Raw value | Count |
| --- | --- |
| False | 1,181,360 |
| True | 994 |

### has_audio_features

Observed distinct raw values: 1.

| Raw value | Count |
| --- | --- |
| True | 1,182,354 |

### streams_total_estimated

Observed distinct raw values: 2.

| Raw value | Count |
| --- | --- |
| True | 1,172,754 |
| False | 9,600 |

### popularity_imputed_aug

Observed distinct raw values: 1.

| Raw value | Count |
| --- | --- |
| False | 1,182,354 |

### has_anomaly

Observed distinct raw values: 2.

| Raw value | Count |
| --- | --- |
| False | 1,160,967 |
| True | 21,387 |

### release_year_precision_aug

Observed distinct raw values: 1.

| Raw value | Count |
| --- | --- |
| False | 1,182,354 |

Decision requiring approval: no category mapping, spelling normalization, or Boolean coercion has been applied.

## 12. Discrepancies

| Area | Observed discrepancy | Recommendation / approval |
| --- | --- | --- |
| Detailed metadata schema | 11 columns lack schema entries: title_normalized, album_id, album_name, release_date, explicit_flag, has_audio_features, source_dataset, mode_name, time_signature, streams_source, chart_date_first | Documentation update recommended |
| Streams wording | Metadata describes streams_total as estimated, while streams_total_estimated distinguishes modeled and direct values. | Status must remain visible; wording requires approval |
| Source provenance | Root README says Kaggle; source README documents multiple component sources and licenses. | Clarify documentation |

## Outstanding approvals before cleaning

- Analytical types and nullable conversion behavior.
- Canonical key and repeated-ID handling.
- Exact-duplicate handling.
- Missing-value eligibility, exclusions, and any imputation.
- Validity bounds and unusual-value treatment.
- Category normalization or mapping.
- Documentation corrections.
- Dashboard wording that separates direct, estimated, missing, and unknown-status streams.

No recommendation in this report has been implemented.

## Supplemental audit: text and edge cases

### Scope

This section contains observations from a read-only pandas scan of all source rows. Original values are shown without correction. Thresholds and coherence checks are review aids, not cleaning rules.

### 1. Text-formatting observations

| Field | Leading/trailing | Repeated internal | Empty strings | Control characters | Representative original examples |
| --- | --- | --- | --- | --- | --- |
| track_id | 0 | 0 | 0 | 0 | None |
| spotify_id | 0 | 0 | 0 | 0 | None |
| title | 0 | 0 | 5 | 1 | empty: row 800963 ''; row 1067726 ''; row 1068054 '' / control: row 1048156 'Merry Shrovetide \x7f (sung in russian) (Power of Evil)' |
| track_artist | 30 | 0 | 19 | 0 | leading_or_trailing: row 41973 'The Wanderer '; row 56975 'Whitewoods '; row 157968 'Whitewoods ' / empty: row 221694 ''; row 269925 ''; row 352007 '' |
| album_name | 0 | 0 | 1,156,965 | 0 | empty: row 29 ''; row 39 ''; row 40 '' |
| genre_l1 | 0 | 0 | 0 | 0 | None |
| genre_l2 | 0 | 0 | 0 | 0 | None |
| genre_raw | 0 | 0 | 0 | 0 | None |
| streams_source | 0 | 0 | 1,172,754 | 0 | empty: row 9 ''; row 20 ''; row 26 '' |

Observation: counts overlap when one value meets more than one condition. Control characters use ASCII ranges 0x00-0x1F and 0x7F; repeated internal whitespace means two or more spaces/tabs between non-whitespace characters.

Recommendation requiring approval: no trimming, whitespace collapsing, or control-character removal has been applied.

### 2. Missing title and artist

| Measure | Observed count |
| --- | --- |
| Missing title | 5 |
| Missing track_artist | 19 |
| Union missing title or artist | 20 |
| Missing both | 4 |

Representative original records:

| missing_pattern | csv_row | track_id | spotify_id | title | track_artist | genre_l1 | genre_l2 | source_dataset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| missing both | 1067726 | spotify:track:3VKFip3OdAvv4OfNTgFWeQ | 3VKFip3OdAvv4OfNTgFWeQ |  |  | Latin | Reggaeton | tidytuesday_spotify |
| missing both | 1068054 | spotify:track:5TTzhRSWQS4Yu8xTgAuq6D | 5TTzhRSWQS4Yu8xTgAuq6D |  |  | Hip-Hop | Gangsta Rap | tidytuesday_spotify |
| missing both | 1068055 | spotify:track:5cjecvX0CmC9gK0Laf5EMQ | 5cjecvX0CmC9gK0Laf5EMQ |  |  | Hip-Hop | Gangsta Rap | tidytuesday_spotify |
| missing both | 1069583 | spotify:track:69gRFGOWY9OMpFJgFol1u0 | 69gRFGOWY9OMpFJgFol1u0 |  |  | Hip-Hop | Southern Hip-Hop | tidytuesday_spotify |
| missing title | 800963 | spotify:track:2Q5cMgzptSupzvvWtZTyVg | 2Q5cMgzptSupzvvWtZTyVg |  | The Duskfall | World | Nordic | arc8_spotify_1m |
| missing artist | 221694 | spotify:track:1SanRTG8EZRb9U1V4NUSKp | 1SanRTG8EZRb9U1V4NUSKp | The Damp Chill of Life |  | Metal | Black Metal | arc8_spotify_1m |
| missing artist | 269925 | spotify:track:773j5fNWIjO0EWqAiX8Quo | 773j5fNWIjO0EWqAiX8Quo | It's Painless to Let Go |  | Metal | Black Metal | arc8_spotify_1m |
| missing artist | 352007 | spotify:track:7shu4LrpMTsGwa8YotA1My | 7shu4LrpMTsGwa8YotA1My | A World, Dead and Gray |  | Metal | Black Metal | arc8_spotify_1m |
| missing artist | 366280 | spotify:track:7K0hyoMx2UZMf173FSUFnY | 7K0hyoMx2UZMf173FSUFnY | You Did a Good Thing |  | Metal | Black Metal | arc8_spotify_1m |
| missing artist | 381930 | spotify:track:7ItLwpnDJNmnmjlx4hOC96 | 7ItLwpnDJNmnmjlx4hOC96 | A Chance I'd Never Have |  | Metal | Black Metal | arc8_spotify_1m |

Recommendation requiring approval: dashboard eligibility for these records remains undecided.

### 3. Condition counts by source_dataset

| source_dataset | missing_time_signature | nonpositive_time_signature | duration_over_one_hour | missing_title | missing_track_artist |
| --- | --- | --- | --- | --- | --- |
| arc8_spotify_1m | 0 | 1,228 | 407 | 1 | 15 |
| tidytuesday_spotify | 22,590 | 0 | 0 | 4 | 4 |

Observations only: no condition is classified as an error and no row has been excluded.

### 4. Representative duration and time-signature records

Ten original records with duration over one hour:

| csv_row | track_id | title | track_artist | genre_l1 | genre_l2 | source_dataset | duration_ms | time_signature | energy | valence | danceability | acousticness | instrumentalness | speechiness | liveness | loudness | tempo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50698 | spotify:track:1saXdvEAafdRzUphXBzSHg | Ocean Waves for Sleep | Ocean Waves For Sleep | Pop | Mood Pop | arc8_spotify_1m | 4120258 | 3.0 | 0.995 | 1e-05 | 0.0797 | 0.932 | 0.562 | 0.0612 | 0.31 | -17.379 | 84.788 |
| 69922 | spotify:track:32N71aqSB1j5skwhEi2hmL | 1 Hour Rain and Thunder | Sleep Fruits Music | Pop | Mood Pop | arc8_spotify_1m | 3603000 | 4.0 | 1.0 | 1e-05 | 0.116 | 0.266 | 0.692 | 0.0644 | 0.951 | -24.4 | 51.997 |
| 106781 | spotify:track:7x64fIPdLotRezkMZpIk4U | 1 Hour Deep Sleep Music | Sleep Fruits Music | Pop | Mood Pop | arc8_spotify_1m | 3608000 | 4.0 | 0.01 | 0.0374 | 0.151 | 0.942 | 0.854 | 0.0471 | 0.0902 | -35.725 | 136.785 |
| 108487 | spotify:track:0PINNy1r5eEILOuHpnjl5d | Internal Flight (Remastered) | Estas Tonne | Instrumental | Guitar | arc8_spotify_1m | 3876277 | 4.0 | 0.64 | 0.212 | 0.3 | 0.946 | 0.893 | 0.0367 | 0.0783 | -9.266 | 159.624 |
| 112557 | spotify:track:4npxcYHeyapx0jHs5QxdoT | Siva Simiran / Siva Amrithavani / Shambho Tere Jaijaikar | Anuradha Paudwal | Pop | K-Pop | arc8_spotify_1m | 3639107 | 4.0 | 0.671 | 0.625 | 0.448 | 0.774 | 0.0 | 0.0462 | 0.249 | -6.008 | 113.996 |
| 133561 | spotify:track:0m3NuZiabJ4wl4HmXONyIP | Dopesmoker - 2022 Remastered Version | Sleep | Metal | Metal | arc8_spotify_1m | 3809027 | 4.0 | 0.419 | 0.0713 | 0.18 | 0.000127 | 0.7 | 0.0308 | 0.0782 | -13.268 | 95.956 |
| 155451 | spotify:track:2QfFLpSGF1T1pY6tq4kD7Z | Ocean Waves Sounds | Ocean Sounds | Pop | Mood Pop | arc8_spotify_1m | 4120258 | 3.0 | 0.995 | 1e-05 | 0.0797 | 0.932 | 0.562 | 0.0612 | 0.31 | -17.379 | 84.788 |
| 163157 | spotify:track:4GYktiEn51I4lc3k6PlN7p | Let's Just Leave | Neelix | Electronic | Techno | arc8_spotify_1m | 3652446 | 4.0 | 0.719 | 0.211 | 0.719 | 0.0227 | 0.717 | 0.0723 | 0.0431 | -9.544 | 140.033 |
| 163697 | spotify:track:5a71BCXF1ojvHckMzWeZmU | Soothing Rainfall-relaxing Rain Nature Sounds-no Thunder | Deep Sleep Systems | Pop | Mood Pop | arc8_spotify_1m | 3610000 | 4.0 | 1.0 | 1e-05 | 0.0784 | 0.598 | 0.978 | 0.0578 | 0.796 | -20.855 | 83.098 |
| 171083 | spotify:track:10SeyQmuBIVJmbZYYJs07W | dlp 1.1 | William Basinski | Electronic | Ambient | arc8_spotify_1m | 3815787 | 5.0 | 0.0815 | 0.0672 | 0.209 | 0.973 | 0.938 | 0.0408 | 0.105 | -31.702 | 95.205 |

Ten original records with nonpositive time_signature:

| csv_row | track_id | title | track_artist | genre_l1 | genre_l2 | source_dataset | duration_ms | time_signature | energy | valence | danceability | acousticness | instrumentalness | speechiness | liveness | loudness | tempo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 111 | spotify:track:2bRKxuH1o7pTmb1y4GfdEc | Clean White Noise - Loopable with no fade | White Noise Baby Sleep | Pop | Mood Pop | arc8_spotify_1m | 90228 | 0.0 | 0.00342 | 0.0 | 0.0 | 0.791 | 1.0 | 0.0 | 0.111 | -28.46 | 40.0 |
| 3368 | spotify:track:65rkHetZXO6DQmBh3C2YtW | White Noise - 500 hz | Granular | Pop | Mood Pop | arc8_spotify_1m | 147097 | 0.0 | 4.98e-05 | 0.0 | 0.0 | 0.923 | 0.297 | 0.0 | 0.11 | -32.354 | 40.0 |
| 4117 | spotify:track:6H4B9gJD6eQlNoEh8q85pP | White Noise - 145 hz | Granular | Pop | Mood Pop | arc8_spotify_1m | 135484 | 0.0 | 2.03e-05 | 0.0 | 0.0 | 0.944 | 0.869 | 0.0 | 0.112 | -40.449 | 40.0 |
| 7722 | spotify:track:5pGBDKBaR63vuJ4g8ialcU | Deep Sleep Recovery Noise | Water Sound Natural White Noise | Pop | Mood Pop | arc8_spotify_1m | 63000 | 0.0 | 0.032 | 0.0 | 0.0 | 0.916 | 0.202 | 0.0 | 0.103 | -30.704 | 40.0 |
| 8050 | spotify:track:5I21rMWLtCjWQl6QyLn85W | Pure Brown Noise - Loopable with no fade | White Noise for Babies | Pop | Mood Pop | arc8_spotify_1m | 72223 | 0.0 | 0.00125 | 0.0 | 0.0 | 0.908 | 1.0 | 0.0 | 0.111 | -27.592 | 40.0 |
| 9312 | spotify:track:575DZcL4PtBm3qoFdilkq8 | Box Fan Sound | Tmsoft’s White Noise Sleep Sounds | Pop | Mood Pop | arc8_spotify_1m | 589972 | 0.0 | 2.03e-05 | 0.0 | 0.0 | 0.15 | 0.204 | 0.0 | 0.112 | -25.402 | 40.0 |
| 9912 | spotify:track:67iF3DdebmElASIGoebYt1 | Brown Noise - Loopable with No Fade | White Noise Meditation | Pop | Mood Pop | arc8_spotify_1m | 73887 | 0.0 | 2.01e-05 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | -15.776 | 40.0 |
| 12059 | spotify:track:6quMGNh47CpSR5kmZSYSTK | Arrival | The Alchemist | Hip-Hop | Hip-Hop | arc8_spotify_1m | 94967 | 0.0 | 0.802 | 0.0 | 0.0 | 0.00417 | 0.878 | 0.0 | 0.603 | -7.977 | 40.0 |
| 15046 | spotify:track:23fEZLdzHoZlNZZu4E1pSp | Absentee | Cass McCombs | Pop | Pop | arc8_spotify_1m | 168737 | 0.0 | 0.328 | 0.0 | 0.0 | 0.893 | 0.862 | 0.0 | 0.122 | -11.101 | 40.0 |
| 16821 | spotify:track:2qTh0uDCWUZ9G9xZO7RqGd | 11:35 In Miami | YN Jay | Hip-Hop | Hip-Hop | arc8_spotify_1m | 96183 | 0.0 | 0.641 | 0.0 | 0.0 | 0.138 | 0.0 | 0.0 | 0.36 | -6.749 | 40.0 |

Recommendation requiring approval: these records need contextual review before any validity or exclusion rule is chosen.

### 5. streams_total_estimated by streams_source

| streams_total_estimated | <EMPTY> | arc2_2023_top | arc7_chart_dump |
| --- | --- | --- | --- |
| False | 0 | 101 | 9,499 |
| True | 1,172,754 | 0 | 0 |

Observed: no inconsistent combinations were found under these checks: direct/False requires a populated streams_source; estimated/True requires an empty streams_source; the flag must be True or False.

Recommendation requiring approval: approve this coherence definition before it is used as a cleaning validation rule.

### 6. Candidate difficult records for later manual checks

| csv_row | track_id | spotify_id | title | track_artist | album_name | genre_l1 | genre_l2 | genre_raw | source_dataset | duration_ms | time_signature | streams_total | streams_total_estimated | streams_source | difficulty_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1067726 | spotify:track:3VKFip3OdAvv4OfNTgFWeQ | 3VKFip3OdAvv4OfNTgFWeQ |  |  |  | Latin | Reggaeton | latin | tidytuesday_spotify | 252773 |  | 3699500.75 | True |  | missing title and artist |
| 800963 | spotify:track:2Q5cMgzptSupzvvWtZTyVg | 2Q5cMgzptSupzvvWtZTyVg |  | The Duskfall |  | World | Nordic | swedish | arc8_spotify_1m | 281533 | 4.0 | 2032031.1600186033 | True |  | missing title |
| 221694 | spotify:track:1SanRTG8EZRb9U1V4NUSKp | 1SanRTG8EZRb9U1V4NUSKp | The Damp Chill of Life |  |  | Metal | Black Metal | black-metal | arc8_spotify_1m | 630715 | 4.0 | 3699500.75 | True |  | missing artist |
| 41973 | spotify:track:5cXq69EbEhTaWE7lUTOwsK | 5cXq69EbEhTaWE7lUTOwsK | We're All Going Home | The Wanderer  |  | Folk | Singer-Songwriter | singer-songwriter | arc8_spotify_1m | 184746 | 4.0 | 1633113.054692513 | True |  | text-formatting edge case |
| 50698 | spotify:track:1saXdvEAafdRzUphXBzSHg | 1saXdvEAafdRzUphXBzSHg | Ocean Waves for Sleep | Ocean Waves For Sleep |  | Pop | Mood Pop | sleep | arc8_spotify_1m | 4120258 | 3.0 | 1128725.2280942663 | True |  | duration over one hour |
| 111 | spotify:track:2bRKxuH1o7pTmb1y4GfdEc | 2bRKxuH1o7pTmb1y4GfdEc | Clean White Noise - Loopable with no fade | White Noise Baby Sleep |  | Pop | Mood Pop | sleep | arc8_spotify_1m | 90228 | 0.0 | 22941256.975895658 | True |  | nonpositive time signature |
| 2 | spotify:track:0yLdNVWF3Srea0uzk55zFn | 0yLdNVWF3Srea0uzk55zFn | Flowers | Miley Cyrus | Flowers | Pop | Pop | pop | arc8_spotify_1m | 200455 | 4.0 | 1316855716.0 | False | arc2_2023_top | direct stream value with populated source |
| 9 | spotify:track:4nrPB8O7Y7wsOCJdgXkthe | 4nrPB8O7Y7wsOCJdgXkthe | Shakira: Bzrp Music Sessions, Vol. 53 | Bizarrap | Shakira: Bzrp Music Sessions, Vol. 53 | Hip-Hop | Hip-Hop | hip-hop | arc8_spotify_1m | 218289 | 4.0 | 168237697.07436818 | True |  | estimated stream value with empty source |
| 1068054 | spotify:track:5TTzhRSWQS4Yu8xTgAuq6D | 5TTzhRSWQS4Yu8xTgAuq6D |  |  |  | Hip-Hop | Gangsta Rap | rap | tidytuesday_spotify | 206465 |  | 3699500.75 | True |  | missing title and artist |
| 269925 | spotify:track:773j5fNWIjO0EWqAiX8Quo | 773j5fNWIjO0EWqAiX8Quo | It's Painless to Let Go |  |  | Metal | Black Metal | black-metal | arc8_spotify_1m | 356752 | 4.0 | 3699500.75 | True |  | missing artist |

Only original values and the selection reason are shown. No expected or cleaned result has been defined.

### Supplemental recommendations and approvals

- Approve or reject each proposed text-standardization operation separately.
- Approve eligibility treatment for missing title or artist.
- Approve whether source-specific patterns change any rule.
- Review long-duration and nonpositive-time-signature examples before setting bounds.
- Approve the stream flag/source coherence definition.
- Select five records from the ten candidates before expected outcomes are written.

No rule in this supplemental section has been applied.

