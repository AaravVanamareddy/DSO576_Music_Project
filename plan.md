# Spotify Track Promotion Data-Cleaning Plan

## Scope and guardrails

This document is a plan only. No cleaning rule has been applied. `data/raw/spotify_full.csv` remains the authoritative, unchanged source. The project documentation describes an expected 1,182,354 rows and 83 columns covering 1957–2023; those figures will be treated as source expectations to verify, not as final cleaning results.

The future analytical dataset is intended for historical comparison of tracks within a selected genre and release period. It will not support causal claims or automatic hit prediction. `track_popularity` is the primary success metric. `streams_total` is secondary and must always be paired with its estimated/direct/missing status.

## 1. Project vision, business question, and main metric

**What Codex will inspect**

- The stated dashboard audience and decision: music-label marketing managers comparing tracks within the same genre and release period.
- The definitions and provenance of `track_popularity`, `streams_total`, `streams_total_estimated`, `streams_source`, and `popularity_imputed_aug` in the source documentation.
- Whether popularity is a current snapshot, a release-time measure, or measured as of a documented date.

**Evidence or output**

- A short analysis charter defining the dashboard population, comparison dimensions, primary and secondary metrics, and permitted interpretations.
- A metric-definition table that records units, source, missing-value meaning, estimation/imputation status, and known time basis.

**Proposed rule**

- Use `track_popularity` as the primary metric and label it as a Spotify popularity score from 0 to 100.
- Display `streams_total` only with a categorical status derived from its value and `streams_total_estimated`: `direct`, `estimated`, `missing`, or `unknown status` if the flag is invalid.
- Keep imputed popularity distinguishable from observed popularity.
- Describe all comparisons as historical/descriptive associations. Exclude `hit_probability` from the promotion dashboard because it is a modeled field and would encourage automatic hit-prediction claims.

**Decision requiring approval**

- Approve whether tracks with imputed popularity may appear by default or must be excluded by the dashboard’s default filter.
- Approve the exact dashboard wording for the time basis of popularity if the source does not provide a reliable snapshot date.

## 2. Row meaning and possible unique key

**What Codex will inspect**

- Whether each parsed row represents one Spotify track record, rather than an artist, album, chart observation, or track-source observation.
- Uniqueness, missingness, and one-to-one consistency of `track_id` and `spotify_id`.
- Whether a single ID appears with conflicting titles, artists, albums, genres, release years, popularity values, or source datasets.

**Evidence or output**

- A grain statement describing what one row represents.
- A key-profile table for `track_id`, `spotify_id`, and the pair (`track_id`, `spotify_id`): nonmissing count, distinct count, duplicate-row count, and conflict count.
- Examples of any ID conflicts, without resolving them during the audit.

**Proposed rule**

- Treat `track_id` as the leading candidate key and `spotify_id` as its validation counterpart.
- Do not assume either field is unique until profiling proves it.
- Preserve identifiers as text. Never convert them to numeric values, case-fold them, or remove leading zeros.

**Decision requiring approval**

- Approve the final canonical key after the key profile is reviewed.
- If repeated IDs exist, approve whether the future analytical grain should be one row per source record or one resolved row per Spotify track.

## 3. Preservation of the original source

**What Codex will inspect**

- The source path, file size, modification timestamp, encoding, delimiter, header, and a cryptographic hash.
- Repository ignore rules and the intended location for future derived data and audit artifacts.

**Evidence or output**

- A source manifest containing the path, byte size, timestamp, encoding, expected schema, and SHA-256 hash.
- A before-and-after hash comparison proving that the raw file did not change.

**Proposed rule**

- Open `data/raw/spotify_full.csv` read-only and never overwrite it.
- Write any future cleaned dataset to a separate derived-data path using a temporary file followed by an atomic rename only after validation passes.
- Keep cleaning logic, configuration, and audit logs separate from the raw data.

**Decision requiring approval**

- Approve the future derived-data path and filename.
- Approve whether large derived files should be tracked in Git, Git LFS, or excluded and rebuilt locally.

## 4. Columns, data types, conversions, and failed conversions

**What Codex will inspect**

- All source column names, unexpected columns, missing expected columns, duplicate headers, and column order.
- Parsed types and raw string patterns for identifiers, dates, booleans, integers, and decimal values.
- Conversion success and failure for the proposed dashboard fields: identifiers, title, artist, album, genre, release fields, popularity, streams, explicit status, duration, audio features, anomaly flags, and source provenance.

**Evidence or output**

- A schema comparison against `docs/metadata.json`.
- A conversion report by column with total values, blanks, successful conversions, failed conversions, and representative failed raw values.
- A proposed data dictionary with source type, target type, units, nullable status, and any renamed display field.

**Proposed rule**

- Keep identifiers and categorical fields as strings.
- Parse `release_year`, `duration_ms`, `track_popularity`, and `time_signature` as integers when valid.
- Parse `release_date` only when it is a valid date with known precision; retain `release_year_precision_aug` to distinguish inferred years.
- Parse `streams_total` and audio features as numeric values using locale-invariant decimal rules.
- Standardize valid booleans to one representation while retaining failed conversions as missing plus an audit flag; never silently coerce an unrecognized value to `false` or zero.

**Decision requiring approval**

- Approve proposed output types and field names.
- Approve whether raw values that fail conversion should remain in dedicated audit columns in the future cleaned file or only in a separate exception report.

## 5. Text standardization while preserving meaningful differences and leading zeros

**What Codex will inspect**

- Leading/trailing whitespace, repeated internal whitespace, control characters, encoding problems, Unicode variants, and visually similar category labels.
- Case and punctuation differences in titles, artist names, albums, genres, IDs, and source labels.
- Values that may contain meaningful leading zeros.

**Evidence or output**

- Per-column counts of values affected by each proposed text operation.
- Before/after examples for every proposed standardization.
- A category-collision report showing when multiple original values would map to the same standardized value.

**Proposed rule**

- Preserve `track_id`, `spotify_id`, titles, artist names, album names, and raw genre labels exactly except for clearly nonmeaningful boundary whitespace or invalid control characters approved after review.
- Do not title-case, lowercase, strip punctuation, remove accents, or collapse internal whitespace in names and titles without an explicit mapping decision.
- Use separate normalized helper fields only when matching requires them; never replace the display value with the normalized value.
- Preserve leading zeros in every identifier-like field.

**Decision requiring approval**

- Approve each text normalization operation and any category mapping table after collision examples are reviewed.
- Approve whether Unicode normalization is allowed for matching-only helper fields.

## 6. Exact duplicates and repeated IDs

**What Codex will inspect**

- Exact duplicate rows across all 83 source columns.
- Repeated `track_id` values, repeated `spotify_id` values, and repeated ID pairs, regardless of whether the rest of the row matches.
- Conflicting values within repeated-ID groups and the source dataset attached to each occurrence.

**Evidence or output**

- One exact-duplicate report based on a full-row comparison or stable row hash.
- A separate repeated-ID report with occurrence counts, differing columns, and representative groups.
- Counts that do not combine these two issues.

**Proposed rule**

- Keep exact duplicates and repeated IDs as separate audit categories.
- Do not remove exact duplicates or select a winning repeated-ID record until the evidence is reviewed.
- If de-duplication is later approved, preserve source-row lineage and document a deterministic precedence rule.

**Decision requiring approval**

- Approve whether exact duplicates should be removed from the future analytical dataset.
- Approve the treatment of repeated IDs: retain all, aggregate, or select one record using an agreed precedence rule.

## 7. Missing values and possible handling rules

**What Codex will inspect**

- True blanks, whitespace-only values, textual null markers, and parser-generated nulls in every column.
- Missingness by genre, release period, source dataset, estimated-stream status, and audio-feature availability.
- Co-missingness among critical fields such as key, title, artist, genre, release year, popularity, streams, and audio features.

**Evidence or output**

- A missingness table with counts and percentages for every field.
- A missingness-by-group report for the dashboard’s main comparison dimensions.
- A list of records missing candidate key or primary-metric fields.

**Proposed rule**

- Do not fill missing IDs, titles, artist names, genres, popularity scores, streams, or audio features during initial cleaning.
- Represent missing streams as missing, not zero, and assign `streams_status = missing`.
- Retain records with missing optional audio features and expose `has_audio_features` for filtering.
- Define dashboard eligibility separately from physical row retention so that an unusable record can remain traceable without entering a comparison.

**Decision requiring approval**

- Approve which fields are required for dashboard eligibility.
- Approve whether ineligible records remain in the cleaned dataset with an eligibility flag or are written only to an exception dataset.
- Approve any future imputation; none is proposed by default.

## 8. Invalid, impossible, and unusual values

**What Codex will inspect**

- Domain validity: popularity outside 0–100; negative streams or duration; audio features outside 0–1; invalid dates or years; invalid booleans; impossible key/mode/time-signature combinations; and nonfinite numeric values.
- Consistency: `release_date` versus `release_year`, `has_audio_features` versus populated feature columns, and streams versus estimated flag and source.
- Unusual but potentially valid values such as extreme duration, tempo, loudness, instrumentalness, speechiness, or source-provided anomaly flags.
- Release years outside the documented 1957–2023 range, treating them as suspicious until verified.

**Evidence or output**

- Separate reports for invalid/impossible values and statistically unusual values.
- Distribution summaries and selected examples by genre and release period.
- A rule register that records whether each finding is retained, corrected, excluded from analysis, or left unresolved.

**Proposed rule**

- Flag suspicious values before deciding how to handle them.
- Never replace an extreme value merely because it is an outlier.
- Treat source anomaly fields as review signals, not automatic exclusion rules.
- Require explicit provenance before correcting a value; otherwise preserve the original and mark it for review.

**Decision requiring approval**

- Approve hard validity bounds, unusual-value thresholds, and the action for each flagged condition.
- Approve whether anomaly-flagged tracks are included by default in the dashboard.

## 9. Table merges and merge verification

**What Codex will inspect**

- Whether the requested cleaning can be completed from the single denormalized source file.
- Whether documentation or future dashboard requirements introduce external lookup tables, genre mappings, or period mappings.
- Candidate join keys, key uniqueness on both sides, unmatched keys, and many-to-many risks for any proposed merge.

**Evidence or output**

- A merge inventory stating either `no merges used` or documenting every join’s left table, right table, key, cardinality, pre/post row counts, match rate, and unmatched examples.
- A many-to-many expansion check and a reconciliation of values before and after each join.

**Proposed rule**

- Use no table merge for the initial cleaning unless a reviewed mapping table is necessary.
- If a mapping is approved, validate key uniqueness before joining and stop on an unintended many-to-many join or unexplained row multiplication.

**Decision requiring approval**

- Approve any external mapping table and its ownership/version.
- Approve how unmatched keys are labeled; no silent dropping is allowed.

## 10. Starting and final row counts and important totals

**What Codex will inspect**

- Parsed starting row count versus the documented source expectation.
- Counts at every proposed stage: parse failures, exact duplicates, repeated IDs, missing critical fields, invalid values, unusual values, dashboard-eligible rows, and retained rows.
- Key distributions and secondary-metric coverage by genre and release period.

**Evidence or output**

- A reconciliation table in which starting rows equal retained rows plus mutually exclusive exclusions, if exclusions are approved.
- Separate nonexclusive diagnostic counts for flags such as repeated IDs, unusual values, and missing optional fields.
- Before/after counts by genre, release period, stream status, popularity status, and source dataset.

**Proposed rule**

- Every row-count change must have a named, mutually exclusive reason and a traceable list of affected source rows.
- Do not use total streams as a single reconciliation control unless direct and estimated values are reported separately.
- Reconcile popularity coverage and distribution, not only row count, because popularity is the primary metric.

**Decision requiring approval**

- Approve the final list of permitted exclusions and the tolerance for numeric reconciliation, if any.
- Approve which totals and distributions constitute release-blocking controls.

## 11. Calculations, missing values, denominators, and missing group keys

**What Codex will inspect**

- Every derived field proposed for the dashboard, including release-period labels, duration units, status labels, group statistics, and percentages.
- The treatment of blanks and zeros in each calculation.
- Denominators for genre/period means, medians, proportions, and coverage rates.
- Records with missing genre or release-period keys.

**Evidence or output**

- A calculation specification showing formula, input fields, units, missing-value behavior, denominator, and expected edge cases.
- Independent spot calculations and group-level reconciliation for selected genres and periods.
- Numerator and denominator counts displayed beside percentages and averages in validation outputs.

**Proposed rule**

- Exclude missing metric values from metric denominators and always report the nonmissing count; never treat missing as zero.
- Keep zero popularity or zero streams as valid numeric values when source semantics support them.
- Put missing genre or release-period keys in an explicit `Missing/Unknown` audit group rather than silently dropping them.
- Compare tracks within a selected genre and release period without implying causation. Do not calculate or expose an automatic hit score.
- Keep direct and estimated streams separate in summaries unless a combined figure is explicitly labeled and approved.

**Decision requiring approval**

- Approve release-period boundaries and labels.
- Approve the dashboard’s default aggregation functions and minimum group-size rule.
- Approve whether direct and estimated streams may ever be combined in one summary.

## 12. Five individual record checks

**What Codex will inspect**

- Five deterministic records selected after profiling to cover distinct edge cases:
  1. A complete record with observed popularity and direct streams.
  2. A record with estimated streams.
  3. A record with missing full release date or an inferred release year.
  4. A record with missing audio features or an anomaly flag.
  5. A record from an exact-duplicate or repeated-ID group, if one exists; otherwise a record containing quoting, punctuation, Unicode, or leading-zero risk.

**Evidence or output**

- A record-check table with the following fields for each selected record:

| Check | Source locator/key | Original values | Expected result under approved rules | Actual result | Pass/fail | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | To be selected | To be captured verbatim | To be written after approval | To be populated after a future run | Pending | Complete/direct-stream case |
| 2 | To be selected | To be captured verbatim | To be written after approval | To be populated after a future run | Pending | Estimated-stream case |
| 3 | To be selected | To be captured verbatim | To be written after approval | To be populated after a future run | Pending | Release-date precision case |
| 4 | To be selected | To be captured verbatim | To be written after approval | To be populated after a future run | Pending | Missing-feature/anomaly case |
| 5 | To be selected | To be captured verbatim | To be written after approval | To be populated after a future run | Pending | Duplicate/ID/text-preservation case |

**Proposed rule**

- Capture original values directly from the unchanged source, define expected values only from approved rules, and compare them field by field with actual future output.
- Include identifiers, title, artist, genre, release fields, popularity, stream value/status, explicit flag, duration, and representative audio features in every applicable check.

**Decision requiring approval**

- Approve the five selected source records and their expected outcomes before the cleaning run is accepted.

## 13. Reproducibility from unchanged source data

**What Codex will inspect**

- Source hash, configuration, tool/runtime versions, rule version, deterministic ordering, and any external mapping versions.
- Whether two independent future runs from the same source and rules produce identical schemas, row counts, audit results, and output hashes.
- Whether locale, current date, random seeds, or unordered operations can change results.

**Evidence or output**

- A run manifest containing source hash, rule/configuration version, environment versions, timestamps, and output hashes.
- A clean-room rerun comparison showing identical row counts, schema, control totals, and file hash, or documenting any intentional nondeterminism.
- A source hash check after each run proving the raw file remained unchanged.

**Proposed rule**

- Make the future process deterministic, parameterized, and fail-fast on schema drift or source-hash mismatch.
- Pin mappings and release-period definitions to versioned configuration.
- Rebuild all derived outputs from the raw source rather than manually editing cleaned data.

**Decision requiring approval**

- Approve the reproducibility acceptance criteria and the location/retention policy for run manifests and audit logs.

## 14. Unresolved limitations and their effects

**What Codex will inspect**

- Missing snapshot dates and changing Spotify popularity scores.
- Mixed direct and modeled stream counts, unknown stream-estimation methodology, and source-to-source comparability.
- Genre assignment ambiguity, source coverage bias, duplicate-source integration, inferred release years, missing release dates, and missing audio features.
- Engineered fields that could leak target information or encourage prediction claims.
- Whether the dataset represents the label’s catalog, the broader market, or a nonrandom compilation of public sources.

**Evidence or output**

- A limitations register with issue, affected fields/records, likely analytical effect, mitigation, residual risk, and dashboard disclosure text.
- A release decision log distinguishing resolved issues, accepted limitations, and blockers.

**Proposed rule**

- Document limitations beside the affected metrics and filters, not only in technical notes.
- State that results describe this dataset and time snapshot, do not establish causal promotion effects, and do not predict hits automatically.
- Label estimated streams wherever they appear and avoid ranking tracks on mixed stream types without a visible status control.
- Exclude predictive or target-derived engineered fields from the core dashboard unless separately justified and approved.

**Decision requiring approval**

- Approve the residual limitations that are acceptable for dashboard release and the exact disclosure language shown to users.
- Approve any exception that would include predictive fields or combine incomparable stream measures.

## Approval gate before implementation

No cleaning should begin until the project owner approves the following: canonical key and row grain; dashboard eligibility fields; duplicate and repeated-ID handling; type and text rules; missing-value policy; validity bounds and outlier treatment; any mapping or merge; release-period definitions; aggregation and denominator rules; direct/estimated stream treatment; five record-level expected outcomes; reconciliation controls; reproducibility criteria; and release limitations.
