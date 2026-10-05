# Approved cleaning decisions

## Status and scope

These rules are approved for a later cleaning implementation. They are documented here but have not been applied. The raw source remains unchanged, and no cleaned CSV or cleaning script has been created.

Expected structural result after a future implementation: 1,182,354 rows, all 83 original columns, and four derived columns (`dashboard_eligible`, `duration_over_one_hour`, `invalid_time_signature`, and `streams_status`) for 87 columns total.

## 1. Canonical key

- **Approved rule:** Use `track_id` as the canonical unique key. Retain `spotify_id` as a validation identifier.
- **Reason:** The complete audit found no missing or repeated values for either identifier, and the ID pair is one-to-one in the source.
- **Expected effect:** No row-count change. Both original identifier columns remain available.
- **Validation check:** Confirm `track_id` is nonmissing and unique across 1,182,354 rows. Confirm `spotify_id` is nonmissing and unique, and verify that each `track_id` maps to exactly one `spotify_id` and vice versa.

## 2. Row retention and duplicates

- **Approved rule:** Keep all 1,182,354 rows. Do not remove duplicates.
- **Reason:** The audit found zero exact duplicate groups and zero repeated `track_id`, `spotify_id`, or ID-pair values.
- **Expected effect:** Final row count remains 1,182,354.
- **Validation check:** Reconcile source rows to cleaned rows at 1,182,354 and confirm that the set of canonical keys is unchanged.

## 3. Original-column preservation

- **Approved rule:** Retain all 83 original source columns.
- **Reason:** The cleaned dataset must preserve source information while adding only analysis-control fields.
- **Expected effect:** Every source column remains present with its original name. Four approved derived columns increase the expected total to 87.
- **Validation check:** Compare the ordered source-column list with the cleaned file. Confirm all 83 names are present exactly once and that only the four approved derived names are added.

## 4. Identifier and text types

- **Approved rule:** Convert identifier and text fields to pandas string types.
- **Reason:** String types preserve identifiers, leading zeros, capitalization, punctuation, accents, and missing values without numeric coercion.
- **Expected effect:** Textual values remain text and missing values remain missing rather than becoming the literal strings `nan` or `None`.
- **Validation check:** Confirm approved identifier/text columns use pandas `string` dtype. Compare nonmissing raw values with cleaned values, allowing only the approved artist trim and title control-character removal.

## 5. Nullable numeric, Boolean, and date types

- **Approved rule:** Convert valid integer, float, Boolean, and date fields to appropriate nullable pandas types. Never convert missing values to zero or `False`.
- **Reason:** Nullable types support analysis while preserving the distinction between missing values and valid zero/false values.
- **Expected effect:** Valid values become typed values; missing values remain `pd.NA` or `NaT`. No row is removed because of conversion.
- **Validation check:** Record conversion failures by column and require zero unexplained failures. Confirm missing counts before and after conversion match. For proposed integer fields, verify all nonmissing numeric values are integer-equivalent before casting to `Int64`.

## 6. Artist boundary whitespace

- **Approved rule:** Remove leading and trailing whitespace from the 30 affected `track_artist` values only.
- **Reason:** The supplemental audit found 30 boundary-whitespace cases and no repeated internal whitespace in `track_artist`.
- **Expected effect:** Exactly 30 `track_artist` values change. Meaningful internal spaces, spelling, capitalization, punctuation, and accents remain unchanged.
- **Validation check:** Confirm 30 before/after differences, zero remaining boundary-whitespace values, and no change after applying `strip` a second time. Compare every unaffected artist value byte-for-byte or character-for-character.

## 7. Invalid title control character

- **Approved rule:** Remove the single DEL control character (`U+007F`) from the affected `title`. Preserve all other title characters and internal spaces.
- **Reason:** The audit found one invalid control character in one title and no approved basis for broader title normalization.
- **Expected effect:** Exactly one title changes: the control character is removed, while spelling, capitalization, punctuation, accents, and meaningful spacing remain intact.
- **Validation check:** Confirm one title difference, zero remaining `U+007F` characters in `title`, and equality of the original and cleaned title after deleting only that character from the original.

## 8. Missing title or artist retention

- **Approved rule:** Keep all 20 records missing `title` or `track_artist`. Do not fill or delete them.
- **Reason:** Missingness is known and limited: 5 records lack title, 19 lack artist, 20 are in the union, and 4 lack both.
- **Expected effect:** Missing counts remain 5 for title and 19 for artist after approved text operations. All 20 affected keys remain present.
- **Validation check:** Recompute the missing-title, missing-artist, union, and intersection counts and reconcile them to 5, 19, 20, and 4.

## 9. Dashboard eligibility

- **Approved rule:** Add `dashboard_eligible`. Set it to `False` when `title` or `track_artist` is missing; otherwise set it to `True`.
- **Reason:** Records without a display title or artist should remain traceable in the cleaned dataset but should not enter the dashboard’s standard track comparison.
- **Expected effect:** Expected `False` count is 20 and expected `True` count is 1,182,334, subject to validation after the approved text operations.
- **Validation check:** Confirm the flag is nonmissing Boolean, matches the rule for every row, and does not affect physical row retention. Test all 20 ineligible records individually by key.

## 10. Long-duration retention and flag

- **Approved rule:** Keep all 407 tracks longer than 3,600,000 milliseconds and add `duration_over_one_hour`.
- **Reason:** The audit found plausible long-form music, ambient, sleep, and sound recordings; duration alone is not evidence of an error.
- **Expected effect:** No row removal or duration change. Expected flag counts are 407 `True` and 1,181,947 `False`.
- **Validation check:** Confirm `duration_over_one_hour` equals `duration_ms > 3_600_000` for every row and that exactly 407 rows are `True`.

## 11. Nonpositive time signatures

- **Approved rule:** Keep all 1,228 nonpositive `time_signature` values unchanged and add `invalid_time_signature`.
- **Reason:** These values are unusual, but the record examples include noise, ambient, and ordinary music tracks; there is not enough evidence to correct or delete them.
- **Expected effect:** No source value or row changes. Expected `True` count is 1,228 for nonmissing values less than or equal to zero.
- **Validation check:** Confirm the original `time_signature` values are preserved and the flag is `True` exactly when the typed value is nonmissing and `<= 0`.

## 12. Missing time signatures

- **Approved rule:** Keep the 22,590 missing `time_signature` values as missing.
- **Reason:** Missing is distinct from zero and must not be represented as an invalid observed signature.
- **Expected effect:** Missing count remains 22,590. `invalid_time_signature` is `False` for missing values because the flag identifies observed nonpositive values.
- **Validation check:** Confirm missing-count preservation, confirm no missing value becomes zero, and confirm missing values do not receive a `True` invalid-time-signature flag.

## 13. Stream status

- **Approved rule:** Add `streams_status` with this precedence:
  1. `missing` when `streams_total` is missing.
  2. `unknown_status` when the estimation flag is missing/unrecognized or its combination with `streams_source` is inconsistent.
  3. `direct` when `streams_total_estimated` is `False` and `streams_source` is populated.
  4. `estimated` when `streams_total_estimated` is `True` and `streams_source` is missing.
- **Reason:** The status must distinguish measurement provenance and expose inconsistent combinations rather than silently treating them as direct or estimated.
- **Expected effect:** Based on the audited source, the expected counts are 9,600 `direct`, 1,172,754 `estimated`, 0 `missing`, and 0 `unknown_status`.
- **Validation check:** Cross-tab `streams_status`, `streams_total_estimated`, `streams_source`, and `streams_total`. Confirm every row follows the precedence above and reconcile to the expected counts.

## 14. Stream-value interpretation

- **Approved rule:** Keep direct and estimated streams distinguishable. Never replace missing streams with zero.
- **Reason:** Direct and modeled values have different provenance, and zero is a possible numeric value rather than a missing-value marker.
- **Expected effect:** `streams_total` values remain unchanged; all dashboard summaries can filter or group by `streams_status`.
- **Validation check:** Confirm source and cleaned nonmissing stream values match exactly, missing counts are unchanged, and every stream display or aggregation includes or filters on `streams_status`.

## 15. Unusual values

- **Approved rule:** Keep unusual values unless independent evidence shows they are incorrect.
- **Reason:** The audit thresholds are review signals, not proof of data error.
- **Expected effect:** No winsorization, clipping, replacement, or exclusion based solely on an outlier threshold.
- **Validation check:** Reconcile minimums, maximums, and flagged-value counts for important numeric fields between source and cleaned data, except where an explicitly approved future correction is documented.

## 16. Hit probability

- **Approved rule:** Retain `hit_probability` in the cleaned file for source preservation. Exclude it from dashboard analysis and do not use it for automatic hit prediction.
- **Reason:** It is a modeled field that could encourage unsupported prediction or target leakage, while source preservation requires keeping the original column.
- **Expected effect:** The column and its values remain unchanged but are absent from dashboard metrics, filters, rankings, recommendations, and eligibility logic.
- **Validation check:** Confirm column preservation in the cleaned file and confirm dashboard code/configuration contains no dependency on `hit_probability`.

## 17. No imputation and raw-source protection

- **Approved rule:** Do not impute missing values. Do not modify `data/raw/spotify_full.csv`.
- **Reason:** Source integrity and transparent missingness are required for reproducibility and review.
- **Expected effect:** Missing values remain missing unless a separate future decision is approved. The raw file’s bytes remain unchanged.
- **Validation check:** Compare missing counts by column before and after cleaning, compute the raw file’s SHA-256 before and after the process, and require it to remain `DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914`.

## Implementation gate

Implementation has not started. Before accepting a future cleaned dataset, complete the five manual record checks, run all validation checks above, reconcile the expected 1,182,354 rows and 87 columns, and document any unexpected result for review.
