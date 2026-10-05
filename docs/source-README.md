# SPOTIFY MUSIC FFEATURES DATASET

> Technical overview and specifications of dataset contents and design

---

---

### Dataset Overview:

| Component      | Detail                                                                      |
| -------------- | --------------------------------------------------------------------------- |
| **Type**       | Tabular / Recommendation / Regression / Classification                      |
| **Rows**       | 1,182,354                                                                   |
| **Columns**    | 83 (full) · 38 (features file, with 3 exclusive enrichments)                |
| **Year range** | 1957–2023 (recency-weighted, streaming-era concentrated)                    |
| **Genres**     | 17 L1 genre categories · 99 L2 subgenres · raw Spotify genre tags preserved |
| **Artists**    | ~69,400 unique artists                                                      |
| **Albums**     | ~19,900 unique albums                                                       |
| **Eras**       | Pre-2000, 2000–2010, 2011–2020, 2021+                                       |

### Dataset Description:

A large-scale Spotify music dataset covering over 1.18 million tracks across six decades of recorded music. It combines raw Spotify audio features (energy, valence, danceability, acousticness, instrumentalness, speechiness, liveness, loudness, tempo) with engineered mood, affect, and sonic identity signals, artist-level streaming and career metrics, decade-level trend aggregations, and popularity and chart performance data. The dataset is designed for recommendation systems, hit prediction, genre classification, mood modeling, and longitudinal analysis of how musical taste and audio characteristics have evolved across eras.

---

### Audio Feature Modeling:

| Feature              | Description                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------- |
| **energy**           | Perceptual intensity and activity, 0–1 (mean: 0.641)                                         |
| **valence**          | Musical positiveness; high = euphoric, low = sad/tense (mean: 0.457)                         |
| **danceability**     | Suitability for dancing based on rhythm, tempo stability, and beat strength (mean: 0.540)    |
| **acousticness**     | Confidence that a track is acoustic, 0–1 (mean: 0.319)                                       |
| **instrumentalness** | Predicts absence of vocals; values >0.5 classified as likely instrumental                    |
| **speechiness**      | Detects spoken-word content; high values indicate podcasts, comedy, or audiobooks            |
| **liveness**         | Detects presence of a live audience; values >0.8 strongly suggest a live recording           |
| **loudness**         | Overall track loudness in dBFS; used to compute loudness war index and energy-loudness ratio |
| **tempo**            | Estimated beats per minute (mean: 121.4 BPM); binned into five tempo bands                   |
| **key / mode**       | Pitch class (C–B) and modality (major 63%, minor 37%)                                        |

### Genre Taxonomy:

| Level         | Coverage                                                                                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **L1 genres** | Blues, Classical, Country, Electronic, Folk, Gospel, Hip-Hop, Instrumental, Jazz, Latin, Metal, Pop, R&B, Reggae, Rock, Soundtrack, World                  |
| **L2 genres** | 99 subgenres including Ambient, Alt-Rock, Black Metal, K-Pop, Forró, Dancehall, Samba, Emo, New Age, Acoustic, Comedy, Chill, Mood Pop, Indian, and others |
| **genre_raw** | Original Spotify tag strings retained verbatim for fine-grained genre modeling                                                                             |

### Mood and Affect Modeling:

| Component                    | Values / Behaviour                                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| **emotional_arc**            | Valence × energy quadrant: Q1_euphoric, Q2_angry, Q3_depressed, Q4_content                      |
| **mood_cluster**             | KMeans-derived labels: happy\_energetic, angry\_intense, melancholic, sad\_slow, calm\_positive |
| **tempo_band**               | Five bins: very\_slow, slow, medium, fast, very\_fast (based on BPM distribution)               |
| **mood_index**               | Continuous composite of valence and energy                                                      |
| **acoustic_synthetic_ratio** | Acousticness relative to energy; separates organic from produced sound                          |
| **energy_loudness_ratio**    | Normalised loudness relative to energy; captures loudness-war dynamics                          |
| **is_likely_instrumental**   | Binary flag derived from instrumentalness threshold                                             |
| **is_likely_live**           | Binary flag derived from liveness threshold                                                     |
| **is_likely_spoken_word**    | Binary flag derived from speechiness threshold; correlates with podcast/audiobook anomaly type  |

### Artist-Level Feature Modeling:

| Feature                                 | Description                                                                |
| --------------------------------------- | -------------------------------------------------------------------------- |
| **catalog_size**                        | Total number of tracks in the dataset attributed to the artist             |
| **career_span_years**                   | Years between earliest and latest release in the artist's catalog          |
| **career_start_year / career_end_year** | Temporal bounds of the artist's recorded output in this dataset            |
| **longevity_score**                     | Composite of career span, catalog size, and continued chart presence       |
| **hit_rate**                            | Proportion of the artist's tracks above the high-popularity threshold      |
| **mean_energy_by_artist**               | Artist's characteristic energy level averaged across their catalog         |
| **sonic_evolution_score**               | Measures how much the artist's audio profile has shifted over their career |
| **genre_breadth**                       | Number of distinct L2 subgenres represented in the artist's catalog        |
| **artist_stream_mean_log**              | Log-transformed mean streams across artist tracks (full file)              |
| **artist_stream_median_log**            | Log-transformed median streams across artist tracks (full file)            |

### Decade-Level Trend Modeling:

| Feature                      | Description                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------- |
| **mean_energy_by_decade**    | Average energy of all tracks released in the same decade                      |
| **mean_valence_by_decade**   | Average valence of all tracks released in the same decade                     |
| **mean_tempo_by_decade**     | Average tempo (BPM) of all tracks released in the same decade                 |
| **mean_loudness_by_decade**  | Average loudness of all tracks released in the same decade                    |
| **acousticness_decline_idx** | Measures the documented decline in acoustic recording across decades          |
| **danceability_trend**       | Directional trend in danceability from the artist's earliest to latest decade |
| **decade_track_count**       | Number of tracks in this dataset from the same decade                         |

### Popularity and Streaming Signals:

| Feature                     | Description                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------- |
| **track_popularity**        | Spotify popularity score 0–100 (mean: 18.7, median: 15.0); ~4,878 tracks score ≥70      |
| **streams_total**           | Estimated total streams; median 3.38M, max 1.59B                                        |
| **streams_total_estimated** | Binary flag indicating whether streams_total is modelled or directly sourced            |
| **stream_density**          | Streams normalised by track age in days                                                 |
| **chart_peak_position**     | Highest chart position achieved; present for ~14,900 charting tracks                    |
| **weeks_on_chart**          | Total weeks the track appeared on tracked charts                                        |
| **hit_probability**         | Continuous composite score estimating hit likelihood from audio and popularity features |
| **novelty_score**           | How sonically distinct the track is relative to its genre's typical profile             |

### Feature Engineering:

| Group                 | Features                                                                                                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Audio dimensions**  | energy, valence, danceability, acousticness, instrumentalness, speechiness, liveness, loudness, tempo, key, mode                                                                           |
| **Affect & mood**     | emotional_arc, mood_cluster, mood_index, tempo_band, acoustic_synthetic_ratio, energy_loudness_ratio                                                                                       |
| **Sonic fingerprint** | fp\_energy, fp\_valence, fp\_danceability, fp\_acousticness, fp\_instrumentalness, fp\_speechiness, fp\_liveness                                                                           |
| **Binary flags**      | is\_likely\_instrumental, is\_likely\_live, is\_likely\_spoken\_word, explicit\_flag, has\_audio\_features                                                                                 |
| **Temporal**          | release_year, release_date, decade, era, track_age_days                                                                                                                                    |
| **Genre encoding**    | genre_l1, genre_l2, genre_raw (three-level taxonomy)                                                                                                                                       |
| **Popularity**        | track_popularity, streams_total, stream_density, hit_probability, novelty_score, chart_peak_position, weeks_on_chart                                                                       |
| **Artist-level**      | mean\_energy\_by\_artist, sonic\_evolution\_score, genre\_breadth, catalog\_size, career\_span\_years, longevity\_score, hit\_rate, artist\_stream\_mean\_log, artist\_stream\_median\_log |
| **Decade-level**      | mean\_energy/valence/tempo/loudness\_by\_decade, acousticness\_decline\_idx, danceability\_trend, decade\_track\_count                                                                     |
| **Anomaly**           | anomaly\_flags (LIKELY\_PODCAST\_OR\_AUDIOBOOK, LIKELY\_CLIPPED, EXTREME\_DURATION, LIKELY\_SILENT\_TRACK, GENRE\_AUDIO\_MISMATCH), has\_anomaly                                           |

### Features File Exclusive Columns:

The `spotify_features.csv` (1,182,354 rows, 38 columns) contains three columns not present in the full file:

| Column                        | Description                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **artist_followers**          | Raw (non-log-transformed) follower count; useful for absolute audience-size modeling                         |
| **sonic_fingerprint**         | Composite string encoding the seven fp\_ dimensions as a single vector representation of sonic identity      |
| **genre_fragmentation_index** | Measures how spread an artist's catalog is across genre categories; directly useful for genre-fluid analysis |

### ML Targets:

| Target                     | Task                                                                    |
| -------------------------- | ----------------------------------------------------------------------- |
| **track_popularity**       | Regression — predict Spotify popularity score (0–100)                   |
| **streams_total**          | Regression — predict total estimated stream count                       |
| **hit_probability**        | Regression — predict composite hit likelihood score                     |
| **chart_peak_position**    | Regression — predict highest chart position for a track                 |
| **mood_cluster**           | Multiclass classification — assign mood archetype (5 classes)           |
| **emotional_arc**          | Multiclass classification — predict valence-energy quadrant (4 classes) |
| **genre_l1**               | Multiclass classification — predict primary genre (17 classes)          |
| **is_likely_instrumental** | Binary classification — instrumental detection                          |
| **has_anomaly**            | Binary classification — audio quality / content anomaly flag            |

---

### Dataset Implementation Notes:

| Component              | Detail                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| **Audio features**     | 7 Spotify API dimensions retained verbatim; engineered features layered on top              |
| **Streaming signals**  | streams_total estimated where direct counts unavailable; flag provided                      |
| **Genre resolution**   | Three-level taxonomy: L1 broad → L2 subgenre → raw Spotify tag                              |
| **Anomaly detection**  | 5 flag types; ~21,400 tracks flagged (~1.8% of dataset)                                     |
| **Artist aggregation** | Artist-level stats computed across all tracks in-dataset; not globally                      |
| **Decade trends**      | Computed as within-decade population statistics, not rolling windows                        |
| **Split strategy**     | Random 80/10/10 partitioning across all tracks                                              |
| **Leakage control**    | Artist-level and decade-level aggregates use only information available at time of modeling |

---

### Dataset Directory:

```text
.
├── data/
│   ├── features/
│   │   ├── spotify_albums.csv
│   │   ├── spotify_artists.csv
│   │   ├── spotify_artist_features.csv
│   │   ├── spotify_audio_features.csv
│   │   ├── spotify_decade_trends.csv
│   │   ├── spotify_features.csv
│   │   ├── spotify_genre_tags.csv
│   │   ├── spotify_playlist_cooccurrence.csv
│   │   ├── spotify_popularity_metrics.csv
│   │   └── taste_cluster_report.csv
│   │
│   ├── full/
│   │   └── spotify_full.csv.gz
│   │
│   ├── splits/
│   │   ├── spotify_train.csv.gz
│   │   ├── spotify_val.csv.gz
│   │   └── spotify_test.csv.gz
│   │
│   └── subsets/
│       ├── spotify_high_popularity.csv
│       ├── spotify_instrumental_acoustic.csv
│       ├── spotify_pre2000.csv
│       └── spotify_streaming_era.csv
│
├── LICENSE.txt
│
├── metadata/
│   └── metadata.json
│
├── notebooks/
│   └── demo.ipynb
│
└── README.md
```

---

### Subsets:

**Splits**: Train 80% / Validation 10% / Test 10%

**Featured:**

- High-popularity subset (tracks with popularity ≥ 70)

- Instrumental and acoustic subset

- Pre-2000 catalog subset

- Streaming-era subset (2011+)

---

### Possible applications:

- Music recommendation systems
- Hit song prediction and popularity modeling
- Genre and mood classification
- Audio fingerprint similarity search
- Longitudinal analysis of musical evolution across decades
- Artist career trajectory and longevity modeling
- Streaming count estimation and stream density modeling
- Anomaly and content-type detection (podcasts, live recordings, silent tracks)
- Genre-fluid artist analysis using fragmentation index
- Chart entry and peak position prediction

---

### Sources:

| Source                                           | License                                             | URL                                                                                      |
| ------------------------------------------------ | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| TidyTuesday 2020-01-21 Spotify Data              | Database Contents License (DbCL) v1.0               | https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21            |
| 30000 Spotify Songs *(duplicate of TidyTuesday)* | Database Contents License (DbCL) v1.0               | https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs                      |
| Spotify Dataset                                  | MIT                                                 | https://www.kaggle.com/datasets/ambaliyagati/spotify-dataset-for-playing-around-with-sql |
| 60000 Spotify Songs                              | Database Contents License (DbCL) v1.0               | https://www.kaggle.com/datasets/joebeachcapital/57651-spotify-songs                      |
| Spotify 1Million Tracks                          | Open Data Commons Open Database License (ODbL) v1.0 | https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks                    |

---

### License

Released under the Open Data Commons Open Database License (ODbL) v1.0. 

* **Dataset Rights:** Covered under [ODbL v1.0](LICENSE.txt). Any derivative databases created from this work must also be shared under ODbL v1.0.
* **Dataset Contents:** Individual contents and data entries are made available under the **Database Contents License (DbCL) v1.0**.