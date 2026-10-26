# BUILD_SPEC — Spotify Track Promotion Strategy

 
**Project:** Track Promotion Strategy Phase 2
**Status:** Phase 2 build specification for the Phase 3 dashboard MVP  
**Repository:** https://github.com/AaravVanamareddy/DSO576_Music_Project

## 1. Product vision and scope

**User:** A music label marketing manager preparing to prioritize tracks from an artist's upcoming release.

**Decision:** Which candidate tracks merit further promotional consideration based on how their musical characteristics compare with historically successful tracks in a similar genre and release period?

**Value over current practice:** Instead of reviewing separate track lists, audio attributes, and popularity figures manually, the manager can apply a consistent comparison cohort, inspect interpretable historical patterns, examine individual tracks, and export a reasoned shortlist. The dashboard supports human judgment; it does not predict guaranteed hits, infer causation, or recommend a marketing budget.

**Core MVP:** Four connected tabs — **Overview**, **Track Explorer**, **Artist View**, and **Promotion Shortlist**. The Overview preserves the core Phase 1 dashboard concept; the other tabs make its exploration and selection workflows usable without adding a predictive model. Phase 2 produces this specification, reconciled team cleaning workflow, and tested reusable analysis code, not yet a polished UI.

### Use cases (select/input → see → decide)

| ID | User selects/inputs | Dashboard shows | User decides |
|---|---|---|---|
| UC1 | Broad genre, release-year range, success metric, top-group percentage | Cohort size, top-group threshold, feature comparisons, feature-versus-success scatter | Which audio characteristics warrant closer attention |
| UC2 | A track or artist, with search and sorting | Track details, performance, and comparison with a relevant historical cohort | Whether to investigate a particular track further |
| UC3 | Artist and comparison cohort | Artist's tracks, within-artist rankings, and context against the cohort | Which of that artist's tracks to prioritize for review |
| UC4 | Tracks added to a shortlist | Saved selection, side-by-side features and performance, export | Which tracks to propose for promotional review |

Every major dashboard component below supports one or more of these use cases. Avoid unrelated features.

## 2. Canonical data contract and provenance

**Source:** Kaggle *Spotify Music Features Dataset*: https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset. Raw local filename: `spotify_full.csv`. Record the exact download date or Kaggle dataset version in the team README before final Phase 2 submission; the existing documents do not establish it.

**Candidate canonical output:** `spotify_cleaned_full.csv`, produced by `cleaning.ipynb`. The prior individual-cleaning run reported **1,182,354 rows × 27 columns**, zero duplicate canonical IDs, zero missing canonical IDs, and zero missing primary metric.

**Grain:** One row per track, uniquely identified by `canonical_track_id` (prefer `spotify_id`, fallback to `track_id`). Do not aggregate different track IDs into one song or treat repeated artist names as duplicates.

**Required columns:**

| Purpose | Exact columns |
|---|---|
| Identity and labels | `canonical_track_id`, `spotify_id`, `track_id`, `title`, `track_artist` |
| Filtering | `genre_l1`, `genre_l2`, `release_year`, `explicit_flag` |
| Primary and secondary outcomes | `track_popularity`, `streams_total`, `streams_total_estimated`, `streams_source` |
| Audio comparisons | `danceability`, `energy`, `valence`, `acousticness`, `instrumentalness`, `speechiness`, `liveness`, `loudness`, `tempo`, `duration_ms` |
| Optional track details | `release_date`, `key`, `mode`, `time_signature` |

**Data rules:**
- `track_popularity` is the **primary** historical success metric (0–100). `streams_total` is secondary and may be estimated; always identify estimates. Never call estimated streams verified plays.
- `release_year` drives the release-period filter because most `release_date` values are missing. Unknown years do not appear in a year-filtered cohort; display their exclusion count.
- Audio features `danceability`, `energy`, `valence`, `acousticness`, `instrumentalness`, `speechiness`, `liveness` are on 0–1 scales; `tempo` is BPM, `duration_ms` is milliseconds, and `loudness` is in dB. Do **not** plot or average different units on the same unnormalized scale.
- Preserve missing optional fields as missing. Never substitute zero. Exclude missing values from each metric's calculation and show the corresponding valid count.
- Treat artist/genre labels as provided by the canonical cleaning workflow; do not silently invent artist aliases or remap genres.
- No external joins or API calls are required for the MVP. No audio playback or track-upload workflow is required.
- A 50-row sample is suitable for smoke tests, **not** for validating full-data rankings, distributions, or performance.


## 3. Exact analytics and filter semantics

### 3.1 Global comparison cohort

Global controls (persist across tabs):
1. **Broad genre:** `genre_l1`; default **All genres**. Values populated from the actual data, not hard-coded.
2. **Release period:** inclusive minimum and maximum `release_year`; default **all available valid years**. Validate min ≤ max.
3. **Success metric:** `track_popularity` (default) or `streams_total`.
4. **Success group:** **Top 20%** by default; allow **Top 10%, Top 20%, or Top 30%**.

The **comparison cohort** is all canonical tracks matching genre and year filters **and with nonmissing selected success metric**. Genre/year filters apply before defining success. All views use this same cohort unless explicitly labeled as an artist-only or shortlist view. Show cohort count and selected metric next to the filters.

**Top-group definition (deterministic):** Sort the cohort by selected success metric descending, then `canonical_track_id` ascending to break ties. Select the first `ceil(p × N)` tracks, where `p` is 0.10, 0.20, or 0.30 and `N` is cohort size. The remainder is **Other tracks**. This is a top-share-of-records rule, not a percentile-value cutoff; ties at the boundary are resolved by ID, so the top group has exactly the intended count. If N=0, return empty results and a helpful message; if N=1, the top group has one track and Other is empty. Show N, top-group size, and the metric value of the last top-group track. Recalculate after every relevant filter change.

**Estimated streams:** When streams are selected, include both estimated and nonestimated values in rankings by default **but clearly label** the metric `Streams (includes estimates)` and display the percentage of records marked `streams_total_estimated=True`. Provide an optional checkbox **Exclude estimated streams** (default off); when enabled, remove estimated records **before** ranking and aggregating. Apply this option consistently across all tabs and exports. Do not silently switch metric definitions.

### 3.2 Metric definitions

| Metric / output | Question answered | Source and calculation | Relevant filters |
|---|---|---|---|
| Cohort track count | How much history is being compared? | Number of rows after cohort filters and selected-metric validity rules | Genre, year, metric, estimated-stream option |
| Top-group count and cutoff | Which records count as successful? | Deterministic top-share rule above; cutoff is last selected track's metric value | All global controls |
| Median popularity | What is typical historical popularity? | Median of nonmissing `track_popularity`; show valid N | Genre, year; not changed by selected success metric |
| Median streams | What is typical recorded/estimated reach? | Median nonmissing `streams_total`, with estimate disclosure | Genre, year, estimated-stream option |
| Audio feature comparison | How do successful tracks differ? | Arithmetic mean of each selected 0–1 audio feature, separately for Top and Other; show nonmissing N per group/feature | All global controls |
| Feature-versus-success scatter | How does one attribute relate to the chosen outcome? | Individual valid track pairs (feature, success metric); plot or sampled display as defined below | All global controls and feature selector |
| Ranked track list | Which tracks lead this cohort? | Sort by selected success metric descending, ID ascending; include name, artist, genre, year, popularity, streams, estimate flag | All global controls |
| Candidate profile | How does a chosen track compare? | Candidate's raw feature values versus Top-group feature means in current cohort; difference = candidate minus top-group mean | All global controls; candidate selection |
| Artist summary | Which tracks of an artist deserve review? | Artist track count, artist median popularity, ranked artist tracks; compare each track with global cohort top group | Global controls and artist search |
| Shortlist export | Which tracks were chosen? | User-selected IDs plus displayed metadata and comparison context; no automatic recommendations | User selections; current global filters recorded as metadata |

**Missing-value behavior:** All averages/medians ignore missing values **per field**, show `n_valid`, and return unavailable rather than zero if no valid values exist. Never interpret popularity as a probability. Track popularity and streams are not directly comparable units; show one selected success metric at a time.

**Track selection outside cohort:** Search may find a track outside current genre/year filters. Label it **Outside current comparison cohort**; allow viewing its profile against the current cohort without inserting it into rankings or changing cohort statistics. This makes candidate comparison useful for upcoming tracks not represented in the historical slice. If the candidate has missing audio values, show N/A for those features.

## 4. Dashboard UX specification

**App shell:** Clear title, one-sentence decision purpose, source/limitations note, persistent global filters, and four navigation tabs. Display loading, empty, and error states. Use consistent formatting: popularity 0–100; streams with thousands separators or K/M/B abbreviation; audio features to 2 decimals; BPM to 1 decimal; duration as minutes:seconds; estimated values explicitly flagged.

### Tab A — Overview (UC1)

**Starting tab on launch.** Contains:
1. KPI row: cohort track count, top-group count, median popularity, median streams (estimated-value disclosure).
2. **Audio Feature Comparison:** grouped bar chart for Top vs Other means of `danceability`, `energy`, `valence`, `acousticness`, and `instrumentalness` (all on 0–1 scale); tooltip shows valid counts and exact means.
3. **Selected Feature vs Success Metric:** scatter plot with a selector for one of the seven 0–1 audio features, plus `tempo`, `loudness`, or `duration_ms`; axes display correct units. Use the current cohort and metric. Plot no more than **5,000** points using deterministic sampling for rendering only; label displayed N versus full eligible N. **All summary calculations must use the full eligible cohort**, never the plotting sample. Do not display a regression line or causal claim by default.
4. **Typical Top-Group Profile:** horizontal feature bars for the five primary 0–1 audio features and the valid N for each.
5. **Top Tracks Preview:** top 10 ranked tracks with an action to inspect the track in Track Explorer.

### Tab B — Track Explorer (UC2)

- Search by partial `title` or `track_artist` (case-insensitive), with clear matches and stable sorting.
- Paginated or virtualized track table: title, artist, genre, year, popularity, streams, estimated flag, energy, danceability; sort by the chosen success metric or visible columns.
- Selecting a track shows its detail card and an interpretable feature-by-feature comparison against the **current cohort's Top group**. Show differences in raw feature units, not an invented overall score.
- Allow **Add to shortlist** / **Remove from shortlist**. Duplicate adds do not create duplicate entries.
- Track search operates on the full canonical dataset; clearly label whether each result is inside or outside the current cohort.

### Tab C — Artist View (UC3)

- Search/select an artist from existing `track_artist` values (no fuzzy merging of aliases).
- Show artist track count in current cohort, median popularity, and a ranked table of that artist's cohort tracks.
- Show the selected artist's mean 0–1 audio-feature profile alongside the current cohort Top-group means, with valid counts. Show no-data messaging when the artist has no tracks in the cohort.
- Selecting an artist track opens its detail/comparison and offers **Add to shortlist**.
- Artist data must honor global filters; artist selection must **not** redefine the Top group to be only the artist's tracks.

### Tab D — Promotion Shortlist (UC4)

- Show tracks the user explicitly added (not an automatically predicted recommendation list).
- Include track title, artist, genre, year, popularity, streams, estimated flag, and the five primary audio features.
- Support remove, clear (with confirmation), and **Download CSV**. CSV export must contain `canonical_track_id` and current filter context (genre, year range, selected success metric, top-group percentage, estimated-stream exclusion setting). Include comparison-group summary separately in the view; do not imply shortlist entries were automatically selected.
- Keep shortlist in **current browser/app session only**; no account system, shared database, or persistent storage in the MVP. Changing global filters does not delete selected IDs, but out-of-cohort items are clearly flagged.
- Empty shortlist: explain how to add tracks from Explorer or Artist View.

## 5. Architecture and technical choices

**Recommended stack:** Python 3.11+, pandas, NumPy, **Streamlit** for the local dashboard, and Plotly for interactive charts. These are proposed Phase 2 technical decisions; Use local files only; no Spotify API, authentication, hosted database, or paid service is necessary for the MVP.

**Data size and responsiveness:** The full CSV is about 291 MB on disk and over 1.18 million records. Load the canonical dataset **once per app process**, cache the loaded DataFrame, and cache reusable cohort aggregations by filter settings. Never reload the CSV on every widget change. Filter/aggregate on the full data, but limit displayed tables via pagination and scatter points via deterministic downsampling. If full-file loading is too slow or exceeds available memory, use a locally generated **Parquet** analytical copy as an optional performance optimization; it must preserve the canonical CSV values and be reproducibly created, not treated as a new source of truth.

**Separate modules with one responsibility each:**

| Component | Responsibility | Input → output |
|---|---|---|
| `cleaning.ipynb` (existing) | Generate/validate canonical data | Raw CSV → cleaned CSV + sample |
| `data_loader.py` | Read canonical data, check schema, normalize runtime types | File path → validated DataFrame |
| `analysis.py` | Filter cohorts, define Top group, compute summaries, rankings, comparisons | DataFrame + explicit parameters → values/DataFrames |
| `app.py` | Render tabs, controls, tables, charts, session shortlist | Analysis outputs + UI state → dashboard |
| `tests/test_analysis.py` | Verify analysis contracts and edge cases | Small deterministic test fixtures → assertions |

The names above are proposed implementation filenames, not files claimed to exist yet. Analysis functions must not depend on Streamlit session state, print-only outputs, global mutable variables, or plotting objects. Pass filters as arguments; return plain values or DataFrames. Keep display formatting in the UI layer. No hidden cross-tab transformations.

**Error behavior:** Fail clearly if the canonical data file is missing or lacks required columns; display the expected path and generation instructions. Handle empty cohorts, missing metrics, unknown artists, and invalid filter ranges without exceptions or misleading zero-valued charts.

## 6. Reusable backend analysis contracts (Phase 2 implementation)

Implement and test the following capabilities; function names are suggestions, **not code to copy into this specification**:

1. `load_tracks(path)` → validated canonical DataFrame with expected columns and unique, nonmissing IDs.
2. `filter_cohort(df, genre, year_min, year_max, success_metric, exclude_estimated)` → eligible comparison cohort. Estimated exclusion only changes the cohort when the success metric is streams; document this behavior.
3. `split_success_groups(cohort, metric, top_fraction)` → Top and Other DataFrames plus cutoff and counts, using the exact sort/tie rule in §3.1.
4. `summarize_cohort(cohort, top, other, exclude_estimated)` → KPIs and per-metric valid counts.
5. `feature_comparison(top, other, features)` → one row per feature with Top mean, Other mean, and valid counts.
6. `scatter_data(cohort, feature, metric, max_points=5000)` → eligible full N and reproducible render sample; never use sampled data for aggregate statistics.
7. `rank_tracks(cohort, metric, page, page_size)` → deterministic paginated ranking and total count.
8. `compare_track(df, track_id, top, features)` → track metadata, cohort membership flag, Top-group means, and per-feature differences.
9. `artist_summary(cohort, artist, top)` → artist KPIs, ranked artist tracks, feature profile, and valid counts.
10. `shortlist_export(df, selected_ids, filter_context)` → deduplicated export-ready DataFrame with canonical IDs, metadata, and filter-context fields.

**Backend acceptance:** Functions return reusable values/DataFrames; never only print tables. They agree with the global filter, success-group, missing-value, and estimate policies above. Do not build the UI as a substitute for these Phase 2 functions.

## 7. Build order

1. **Schema and data loader:** Confirm actual columns/types against full canonical data and sample. Record data version/download date. Fail fast on schema violations.
2. **Analysis core:** Implement cohort filtering, success-group split, summary metrics, audio comparisons, scatter-data preparation, ranking, candidate comparison, artist summary, and shortlist export as independent reusable functions.
3. **Backend tests:** Verify exact results on small fixtures, then smoke-test full canonical data. Reconcile aggregate counts with filtered data.
4. **Fresh-agent test:** Give a fresh coding agent only the repository and this file; note any questions, guesses, missing instructions, or mismatches; update the spec and code/docs to eliminate them.
5. **Phase 3:** Implement Streamlit shell, Overview, Track Explorer, Artist View, and Promotion Shortlist in that order; connect tested backend functions; perform UI acceptance checks.


## 8. Non-goals and limitations

Not in MVP: predictive hit probabilities, causal inference, optimized promotional spending, Spotify API integration, audio playback, authentication, persistent multiuser shortlists, automated artist-name reconciliation, or new external datasets. This is a historical decision-support dashboard. Marketing spend, playlist placement, audience demographics, and other potential success drivers are unavailable. Some streams are estimated and some optional metadata is missing. Comparisons must be framed as **associations**, not prescriptions or guarantees.

## 9. Source alignment and decisions to confirm

This spec builds on Phase 1 **Track Promotion Strategy** vision and mockup: genre/release-period filters, selectable popularity/streams success metric, Top 20% group, audio comparisons, scatter, ranked tracks, and candidate comparison. The extension to four tabs is a Phase 2 product-design choice intended to organize the same workflows rather than expand into predictive modeling.


