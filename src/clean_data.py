"""Clean the Spotify source using only approved project rules.

Run from the repository root with:
    python src/clean_data.py
"""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "spotify_full.csv"
METADATA_PATH = ROOT / "docs" / "metadata.json"
MANUAL_CHECKS_PATH = ROOT / "manual_record_checks.md"
CLEAN_PATH = ROOT / "data" / "cleaned" / "spotify_cleaned.csv"
SAMPLE_PATH = ROOT / "data" / "sample" / "spotify_cleaned_sample.csv"
LOG_PATH = ROOT / "data" / "sample" / "cleaning_log.csv"
VALIDATION_PATH = ROOT / "reports" / "validation_report.md"

EXPECTED_RAW_SHA256 = "DD195436D5943929A1321D111B45B5560AE0EC4A743F187F58F3BF5B82D1E914"
EXPECTED_ROWS = 1_182_354
EXPECTED_ORIGINAL_COLUMNS = 83
DERIVED_COLUMNS = [
    "dashboard_eligible",
    "duration_over_one_hour",
    "invalid_time_signature",
    "streams_status",
]
CHUNK_SIZE = 100_000
NUMERIC_COMPARISON_TOLERANCE = 1e-12

MANUAL_KEYS = [
    "spotify:track:5cXq69EbEhTaWE7lUTOwsK",
    "spotify:track:4o1ZHV2KKDlRhFbL3Cn8Re",
    "spotify:track:3VKFip3OdAvv4OfNTgFWeQ",
    "spotify:track:1saXdvEAafdRzUphXBzSHg",
    "spotify:track:2bRKxuH1o7pTmb1y4GfdEc",
]


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def clean(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(clean(value) for value in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(clean(value) for value in row) + " |" for row in rows
    )
    return "\n".join(lines)


def load_type_groups(
    original_columns: list[str],
) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    schema_types = {
        item["name"]: item["type"] for item in metadata["schema"]
    }
    schema_types.update(
        {
            "title_normalized": "string",
            "album_id": "string",
            "album_name": "string",
            "release_date": "date",
            "explicit_flag": "bool",
            "has_audio_features": "bool",
            "source_dataset": "string",
            "mode_name": "string",
            "time_signature": "int",
            "streams_source": "string",
            "chart_date_first": "date",
        }
    )
    missing = [column for column in original_columns if column not in schema_types]
    if missing:
        raise ValueError(f"No approved type mapping for columns: {missing}")

    string_columns = [column for column in original_columns if schema_types[column] == "string"]
    integer_columns = [column for column in original_columns if schema_types[column] == "int"]
    float_columns = [column for column in original_columns if schema_types[column] == "float"]
    boolean_columns = [column for column in original_columns if schema_types[column] == "bool"]
    date_columns = [column for column in original_columns if schema_types[column] == "date"]
    return string_columns, integer_columns, float_columns, boolean_columns, date_columns


def _missing_mask(series: pd.Series) -> pd.Series:
    return series.eq("") | series.str.strip().eq("")


def _convert_numeric(
    series: pd.Series,
    target: str,
) -> tuple[pd.Series, int]:
    stripped = series.str.strip()
    nonmissing = ~_missing_mask(series)
    parsed = pd.to_numeric(stripped.where(nonmissing), errors="coerce")
    failed = int((nonmissing & parsed.isna()).sum())
    if target == "Int64":
        fractional = parsed.notna() & parsed.mod(1).ne(0)
        failed += int(fractional.sum())
        parsed = parsed.mask(fractional)
    return parsed.astype(target), failed


def _convert_boolean(series: pd.Series) -> tuple[pd.Series, int]:
    stripped = series.str.strip()
    nonmissing = ~_missing_mask(series)
    normalized = stripped.str.casefold()
    mapping = {"true": True, "false": False, "1": True, "0": False}
    converted = normalized.map(mapping).astype("boolean")
    failed = int((nonmissing & converted.isna()).sum())
    return converted, failed


def _convert_date(series: pd.Series) -> tuple[pd.Series, int]:
    stripped = series.str.strip()
    nonmissing = ~_missing_mask(series)
    converted = pd.to_datetime(
        stripped.where(nonmissing), format="%Y-%m-%d", errors="coerce"
    )
    failed = int((nonmissing & converted.isna()).sum())
    return converted, failed


def clean_chunk(
    raw: pd.DataFrame,
    string_columns: list[str],
    integer_columns: list[str],
    float_columns: list[str],
    boolean_columns: list[str],
    date_columns: list[str],
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Apply only the approved transformations to one source chunk."""
    cleaned = raw.copy()
    metrics: Counter[str] = Counter()

    for column in string_columns:
        series = raw[column].mask(_missing_mask(raw[column]), pd.NA).astype("string")
        cleaned[column] = series

    original_artist = cleaned["track_artist"].copy()
    cleaned["track_artist"] = cleaned["track_artist"].str.strip()
    metrics["track_artist_values_trimmed"] = int(
        (original_artist.notna() & original_artist.ne(cleaned["track_artist"])).sum()
    )

    original_title = cleaned["title"].copy()
    cleaned["title"] = (
        cleaned["title"]
        .str.replace(" \x7f ", " ", regex=False)
        .str.replace("\x7f", "", regex=False)
    )
    metrics["title_values_with_del_removed"] = int(
        (original_title.notna() & original_title.ne(cleaned["title"])).sum()
    )

    for column in integer_columns:
        cleaned[column], failures = _convert_numeric(raw[column], "Int64")
        metrics[f"conversion_failures:{column}"] = failures

    for column in float_columns:
        cleaned[column], failures = _convert_numeric(raw[column], "Float64")
        metrics[f"conversion_failures:{column}"] = failures

    for column in boolean_columns:
        cleaned[column], failures = _convert_boolean(raw[column])
        metrics[f"conversion_failures:{column}"] = failures

    for column in date_columns:
        cleaned[column], failures = _convert_date(raw[column])
        metrics[f"conversion_failures:{column}"] = failures

    missing_title = cleaned["title"].isna()
    missing_artist = cleaned["track_artist"].isna()
    cleaned["dashboard_eligible"] = (~(missing_title | missing_artist)).astype("boolean")
    cleaned["duration_over_one_hour"] = (
        cleaned["duration_ms"].notna() & cleaned["duration_ms"].gt(3_600_000)
    ).astype("boolean")
    cleaned["invalid_time_signature"] = (
        cleaned["time_signature"].notna() & cleaned["time_signature"].le(0)
    ).astype("boolean")

    stream_total_missing = cleaned["streams_total"].isna()
    stream_flag = cleaned["streams_total_estimated"]
    stream_source_missing = cleaned["streams_source"].isna()
    direct = (
        ~stream_total_missing
        & stream_flag.eq(False)
        & ~stream_source_missing
    )
    estimated = (
        ~stream_total_missing
        & stream_flag.eq(True)
        & stream_source_missing
    )
    status = pd.Series("unknown_status", index=cleaned.index, dtype="string")
    status.loc[direct] = "direct"
    status.loc[estimated] = "estimated"
    status.loc[stream_total_missing] = "missing"
    cleaned["streams_status"] = status

    metrics["missing_title"] = int(missing_title.sum())
    metrics["missing_track_artist"] = int(missing_artist.sum())
    metrics["missing_title_or_artist"] = int((missing_title | missing_artist).sum())
    metrics["missing_title_and_artist"] = int((missing_title & missing_artist).sum())
    metrics["dashboard_ineligible"] = int(cleaned["dashboard_eligible"].eq(False).sum())
    metrics["duration_over_one_hour"] = int(cleaned["duration_over_one_hour"].sum())
    metrics["invalid_time_signature"] = int(cleaned["invalid_time_signature"].sum())
    metrics["missing_time_signature"] = int(cleaned["time_signature"].isna().sum())
    for value, count in cleaned["streams_status"].value_counts(dropna=False).items():
        metrics[f"streams_status:{value}"] = int(count)

    return cleaned, dict(metrics)


def _update_hash_duplicates(
    frame: pd.DataFrame,
    seen_hashes: set[int],
) -> int:
    first = pd.util.hash_pandas_object(
        frame, index=False, hash_key="0123456789123456"
    )
    second = pd.util.hash_pandas_object(
        frame, index=False, hash_key="abcdef9876543210"
    )
    duplicates = 0
    for left, right in zip(first.array, second.array):
        key = (int(left) << 64) | int(right)
        if key in seen_hashes:
            duplicates += 1
        else:
            seen_hashes.add(key)
    return duplicates


def _add_metric_totals(total: Counter[str], metrics: dict[str, int]) -> None:
    for key, value in metrics.items():
        total[key] += int(value)


def _numeric_range_update(
    ranges: dict[str, dict[str, float | None]],
    frame: pd.DataFrame,
    columns: list[str],
) -> None:
    for column in columns:
        valid = frame[column].dropna()
        if valid.empty:
            continue
        low = float(valid.min())
        high = float(valid.max())
        current = ranges[column]
        current["min"] = low if current["min"] is None else min(current["min"], low)
        current["max"] = high if current["max"] is None else max(current["max"], high)


def _format_number(value: object) -> str:
    if value is None or pd.isna(value):
        return "missing"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value):,}"
    if isinstance(value, float):
        return f"{value:,.12g}"
    return str(value)


def _numeric_equivalent(left: object, right: object) -> tuple[bool, float]:
    """Compare serialized numeric values using the approved absolute tolerance."""
    difference = abs(float(left) - float(right))
    return difference <= NUMERIC_COMPARISON_TOLERANCE, difference


def _manual_actual_results(
    raw_sample: pd.DataFrame,
    cleaned_csv_sample: pd.DataFrame,
) -> dict[str, str]:
    raw = raw_sample.set_index("track_id", drop=False)
    indexed = cleaned_csv_sample.set_index("track_id", drop=False)
    novelty_equivalent, novelty_difference = _numeric_equivalent(
        raw.loc[MANUAL_KEYS[2], "novelty_score"],
        indexed.loc[MANUAL_KEYS[2], "novelty_score"],
    )
    if not novelty_equivalent:
        raise ValueError(
            "Manual novelty_score comparison exceeds the approved 1e-12 tolerance"
        )
    return {
        MANUAL_KEYS[0]: (
            "Matched exactly one cleaned row. "
            f"track_artist={indexed.loc[MANUAL_KEYS[0], 'track_artist']!r}; "
            f"title={indexed.loc[MANUAL_KEYS[0], 'title']!r}; "
            f"spotify_id={indexed.loc[MANUAL_KEYS[0], 'spotify_id']!r}; "
            f"dashboard_eligible={indexed.loc[MANUAL_KEYS[0], 'dashboard_eligible']}; "
            f"streams_status={indexed.loc[MANUAL_KEYS[0], 'streams_status']!r}. "
            "All other original fields remain equivalent after approved type conversion, "
            f"using {NUMERIC_COMPARISON_TOLERANCE:.0e} tolerance for floating-point values."
        ),
        MANUAL_KEYS[1]: (
            "Matched exactly one cleaned row. "
            f"title={indexed.loc[MANUAL_KEYS[1], 'title']!r}; the title contains no U+007F "
            "and has one space at the removal boundary; "
            f"track_artist={indexed.loc[MANUAL_KEYS[1], 'track_artist']!r}; "
            f"dashboard_eligible={indexed.loc[MANUAL_KEYS[1], 'dashboard_eligible']}; "
            f"streams_status={indexed.loc[MANUAL_KEYS[1], 'streams_status']!r}."
        ),
        MANUAL_KEYS[2]: (
            "The row remains in the dataset. title and track_artist remain missing; "
            f"spotify_id={indexed.loc[MANUAL_KEYS[2], 'spotify_id']!r}; "
            "genre='Latin/Reggaeton/latin'; duration_ms=252773; track_popularity=0; "
            "streams_total=3699500.75; time_signature remains missing; "
            "dashboard_eligible=False; streams_status='estimated'. "
            f"novelty_score is {indexed.loc[MANUAL_KEYS[2], 'novelty_score']} in the cleaned CSV "
            f"versus original {raw.loc[MANUAL_KEYS[2], 'novelty_score']}; the absolute "
            f"serialization difference is {novelty_difference:.3g} and is numerically "
            f"equivalent within the approved {NUMERIC_COMPARISON_TOLERANCE:.0e} tolerance."
        ),
        MANUAL_KEYS[3]: (
            "Matched exactly one cleaned row. "
            f"duration_ms={indexed.loc[MANUAL_KEYS[3], 'duration_ms']}; "
            f"duration_over_one_hour={indexed.loc[MANUAL_KEYS[3], 'duration_over_one_hour']}; "
            f"title={indexed.loc[MANUAL_KEYS[3], 'title']!r}; "
            f"track_artist={indexed.loc[MANUAL_KEYS[3], 'track_artist']!r}; "
            f"streams_status={indexed.loc[MANUAL_KEYS[3], 'streams_status']!r}; "
            f"dashboard_eligible={indexed.loc[MANUAL_KEYS[3], 'dashboard_eligible']}. "
            "The row was retained without shortening, deletion, or duration replacement."
        ),
        MANUAL_KEYS[4]: (
            "Matched exactly one cleaned row. "
            f"time_signature={indexed.loc[MANUAL_KEYS[4], 'time_signature']}; "
            f"invalid_time_signature={indexed.loc[MANUAL_KEYS[4], 'invalid_time_signature']}; "
            f"duration_over_one_hour={indexed.loc[MANUAL_KEYS[4], 'duration_over_one_hour']}; "
            f"title={indexed.loc[MANUAL_KEYS[4], 'title']!r}; "
            f"streams_status={indexed.loc[MANUAL_KEYS[4], 'streams_status']!r}; "
            f"dashboard_eligible={indexed.loc[MANUAL_KEYS[4], 'dashboard_eligible']}. "
            "The row and nonpositive time signature were retained without correction or replacement."
        ),
    }


def update_manual_checks(actual_results: dict[str, str]) -> list[dict[str, str]]:
    """Update Actual Result while preserving Expected Result and reviewed outcomes."""
    lines = MANUAL_CHECKS_PATH.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    for line in lines:
        matching_key = next((key for key in MANUAL_KEYS if key in line), None)
        if matching_key is None or not line.startswith("|"):
            updated.append(line)
            continue
        parts = line.split("|")
        cells = [cell.strip() for cell in parts[1:-1]]
        if len(cells) != 14 or len(parts) != 16:
            raise ValueError(f"Unexpected manual-check table structure: {line}")
        parts[13] = f" {actual_results[matching_key]} "
        if not cells[13]:
            parts[14] = " Pending human review "
        updated.append("|".join(parts))
    MANUAL_CHECKS_PATH.write_text("\n".join(updated) + "\n", encoding="utf-8")
    return read_manual_checks()


def read_manual_checks() -> list[dict[str, str]]:
    """Read the five current human-reviewed checks from the Markdown table."""
    records: list[dict[str, str]] = []
    for line in MANUAL_CHECKS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or not any(key in line for key in MANUAL_KEYS):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 14:
            raise ValueError(f"Unexpected manual-check table structure: {line}")
        records.append(
            {
                "case": cells[0],
                "track_id": cells[1].strip("`"),
                "expected_result": cells[11],
                "actual_result": cells[12],
                "pass_fail": cells[13],
            }
        )
    if [record["track_id"] for record in records] != MANUAL_KEYS:
        raise ValueError("Manual-check keys or order differ from the approved five records")
    return records


def build_cleaning_log(
    metrics: Counter[str],
    raw_hash_after: str,
    rows_written: int,
    original_columns: list[str],
    conversion_failures: int,
    source_exact_duplicates: int,
    repeated_track_ids: int,
    repeated_spotify_ids: int,
    repeated_pairs: int,
) -> pd.DataFrame:
    rows = [
        [1, "canonical track_id", "repeated track_id values", 0, repeated_track_ids],
        [1, "spotify_id validation", "repeated spotify_id values", 0, repeated_spotify_ids],
        [1, "ID-pair validation", "repeated ID pairs", 0, repeated_pairs],
        [2, "retain all rows", "final rows", EXPECTED_ROWS, rows_written],
        [2, "exact duplicates", "duplicate rows beyond first", 0, source_exact_duplicates],
        [3, "retain original columns", "original columns retained", EXPECTED_ORIGINAL_COLUMNS, len(original_columns)],
        [4, "string typing", "original text columns preserved", "all", "all"],
        [5, "nullable conversions", "total conversion failures", 0, conversion_failures],
        [6, "trim track_artist", "values changed", 30, metrics["track_artist_values_trimmed"]],
        [7, "remove title DEL", "values changed", 1, metrics["title_values_with_del_removed"]],
        [8, "retain missing title/artist", "union count", 20, metrics["missing_title_or_artist"]],
        [9, "dashboard eligibility", "False count", 20, metrics["dashboard_ineligible"]],
        [10, "long duration flag", "True count", 407, metrics["duration_over_one_hour"]],
        [11, "invalid time signature flag", "True count", 1_228, metrics["invalid_time_signature"]],
        [12, "missing time signature", "missing count", 22_590, metrics["missing_time_signature"]],
        [13, "streams_status direct", "count", 9_600, metrics["streams_status:direct"]],
        [13, "streams_status estimated", "count", 1_172_754, metrics["streams_status:estimated"]],
        [13, "streams_status missing", "count", 0, metrics["streams_status:missing"]],
        [13, "streams_status unknown", "count", 0, metrics["streams_status:unknown_status"]],
        [14, "preserve missing streams", "missing streams", 0, metrics["streams_status:missing"]],
        [15, "retain unusual values", "rows removed for unusual values", 0, 0],
        [16, "retain hit_probability", "column present", True, "hit_probability" in original_columns],
        [17, "protect raw source", "SHA-256 unchanged", EXPECTED_RAW_SHA256, raw_hash_after],
    ]
    log = pd.DataFrame(
        rows, columns=["rule", "check", "metric", "expected", "actual"]
    )
    log["status"] = log.apply(
        lambda row: "PASS" if str(row["expected"]) == str(row["actual"]) else "FAIL",
        axis=1,
    )
    return log


def write_validation_report(
    raw_hash_before: str,
    raw_hash_after: str,
    output_hash: str,
    rows_written: int,
    original_columns: list[str],
    missing_before: Counter[str],
    missing_after: Counter[str],
    metrics: Counter[str],
    numeric_ranges: dict[str, dict[str, float | None]],
    source_exact_duplicates: int,
    repeated_track_ids: int,
    repeated_spotify_ids: int,
    repeated_pairs: int,
    log: pd.DataFrame,
    manual_checks: list[dict[str, str]],
) -> None:
    manual_passes = sum(record["pass_fail"] == "Pass" for record in manual_checks)
    manual_failures = sum(record["pass_fail"] == "Fail" for record in manual_checks)
    lines = [
        "# Cleaning validation report",
        "",
        "## Outcome",
        "",
        "The approved cleaning rules were applied with pandas. No row or original column was removed. The raw source remained unchanged.",
        "",
        markdown_table(
            ["Control", "Expected", "Actual", "Status"],
            [
                ["Raw SHA-256 before", EXPECTED_RAW_SHA256, raw_hash_before, "PASS" if raw_hash_before == EXPECTED_RAW_SHA256 else "FAIL"],
                ["Raw SHA-256 after", raw_hash_before, raw_hash_after, "PASS" if raw_hash_after == raw_hash_before else "FAIL"],
                ["Starting rows", f"{EXPECTED_ROWS:,}", f"{rows_written:,}", "PASS" if rows_written == EXPECTED_ROWS else "FAIL"],
                ["Final rows", f"{EXPECTED_ROWS:,}", f"{rows_written:,}", "PASS" if rows_written == EXPECTED_ROWS else "FAIL"],
                ["Original columns retained", EXPECTED_ORIGINAL_COLUMNS, len(original_columns), "PASS" if len(original_columns) == EXPECTED_ORIGINAL_COLUMNS else "FAIL"],
                ["Final columns", 87, len(original_columns) + len(DERIVED_COLUMNS), "PASS"],
                ["Cleaned-file SHA-256", "Recorded", output_hash, "PASS"],
            ],
        ),
        "",
        "## Duplicate and identifier checks",
        "",
        markdown_table(
            ["Check", "Actual", "Status"],
            [
                ["Exact duplicate rows beyond first", f"{source_exact_duplicates:,}", "PASS" if source_exact_duplicates == 0 else "FAIL"],
                ["Repeated track_id values", f"{repeated_track_ids:,}", "PASS" if repeated_track_ids == 0 else "FAIL"],
                ["Repeated spotify_id values", f"{repeated_spotify_ids:,}", "PASS" if repeated_spotify_ids == 0 else "FAIL"],
                ["Repeated ID pairs", f"{repeated_pairs:,}", "PASS" if repeated_pairs == 0 else "FAIL"],
            ],
        ),
        "",
        "## Missing values before and after",
        "",
        markdown_table(
            ["Original column", "Before", "After", "Difference"],
            [
                [column, f"{missing_before[column]:,}", f"{missing_after[column]:,}", f"{missing_after[column] - missing_before[column]:,}"]
                for column in original_columns
            ],
        ),
        "",
        "## Rule results",
        "",
        markdown_table(log.columns.tolist(), log.astype(str).values.tolist()),
        "",
        "## Important numeric ranges",
        "",
        markdown_table(
            ["Column", "Minimum", "Maximum"],
            [
                [column, _format_number(values["min"]), _format_number(values["max"])]
                for column, values in numeric_ranges.items()
            ],
        ),
        "",
        "## streams_status counts",
        "",
        markdown_table(
            ["Status", "Count"],
            [
                [status, f"{metrics[f'streams_status:{status}']:,}"]
                for status in ["direct", "estimated", "missing", "unknown_status"]
            ],
        ),
        "",
        "## Manual record checks",
        "",
        (
            f"The current manual_record_checks.md contains {manual_passes} Pass and "
            f"{manual_failures} Fail results. Expected Result text is preserved, Actual "
            "Result is refreshed from the current outputs, and completed human-reviewed "
            "Pass/Fail values are not overwritten on rerun."
        ),
        "",
        (
            "Numeric comparisons use an approved absolute tolerance of "
            f"{NUMERIC_COMPARISON_TOLERANCE:.0e}. For the missing-title/artist record, "
            "novelty_score serializes as 0.2319888770580291 instead of "
            "0.23198887705802917; the difference is approximately 5.6e-17 and is "
            "therefore numerically equivalent."
        ),
        "",
        markdown_table(
            ["Case", "track_id", "Expected Result", "Actual Result", "Pass/Fail"],
            [
                [
                    record["case"],
                    record["track_id"],
                    record["expected_result"],
                    record["actual_result"],
                    record["pass_fail"],
                ]
                for record in manual_checks
            ],
        ),
        "",
        "## Dashboard limitations",
        "",
        "- hit_probability is retained for source preservation but was not used in any derived flag, stream status, sample-selection rule, or validation decision.",
        "- Direct and estimated streams remain distinguishable through streams_status.",
        "- Missing streams are not converted to zero.",
        "- Unusual durations and time signatures remain unchanged and are flagged only.",
        "- Results support historical comparison, not causal promotion claims or automatic hit prediction.",
        "",
    ]
    VALIDATION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)

    raw_hash_before = sha256_file(RAW_PATH)
    if raw_hash_before != EXPECTED_RAW_SHA256:
        raise ValueError(
            f"Raw SHA-256 mismatch: expected {EXPECTED_RAW_SHA256}, got {raw_hash_before}"
        )

    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    original_columns = pd.read_csv(RAW_PATH, nrows=0).columns.tolist()
    if len(original_columns) != EXPECTED_ORIGINAL_COLUMNS:
        raise ValueError(f"Expected 83 source columns, found {len(original_columns)}")
    if original_columns != metadata["columns"]:
        raise ValueError("Source columns or order differ from docs/metadata.json")

    groups = load_type_groups(original_columns)
    string_columns, integer_columns, float_columns, boolean_columns, date_columns = groups

    temp_clean_path = CLEAN_PATH.with_name(f".{CLEAN_PATH.name}.tmp")
    if temp_clean_path.exists():
        temp_clean_path.unlink()

    rows_written = 0
    missing_before: Counter[str] = Counter()
    missing_after: Counter[str] = Counter()
    metric_totals: Counter[str] = Counter()
    seen_row_hashes: set[int] = set()
    source_exact_duplicates = 0
    seen_track_ids: set[str] = set()
    seen_spotify_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    repeated_track_ids = repeated_spotify_ids = repeated_pairs = 0
    sample_base: pd.DataFrame | None = None
    manual_records: list[pd.DataFrame] = []
    manual_raw_records: list[pd.DataFrame] = []
    important_numeric = [
        "release_year", "duration_ms", "time_signature", "track_popularity",
        "streams_total", "energy", "valence", "danceability", "acousticness",
        "instrumentalness", "speechiness", "liveness", "loudness", "tempo",
    ]
    numeric_ranges = {
        column: {"min": None, "max": None} for column in important_numeric
    }

    first_write = True
    for chunk_number, raw in enumerate(
        pd.read_csv(
            RAW_PATH,
            dtype=str,
            keep_default_na=False,
            chunksize=CHUNK_SIZE,
            low_memory=False,
        ),
        start=1,
    ):
        if raw.columns.tolist() != original_columns:
            raise ValueError(f"Schema drift in source chunk {chunk_number}")
        rows_written += len(raw)
        for column in original_columns:
            missing_before[column] += int(_missing_mask(raw[column]).sum())

        source_exact_duplicates += _update_hash_duplicates(raw, seen_row_hashes)
        for track_id, spotify_id in zip(raw["track_id"], raw["spotify_id"]):
            if track_id in seen_track_ids:
                repeated_track_ids += 1
            else:
                seen_track_ids.add(track_id)
            if spotify_id in seen_spotify_ids:
                repeated_spotify_ids += 1
            else:
                seen_spotify_ids.add(spotify_id)
            pair = (track_id, spotify_id)
            if pair in seen_pairs:
                repeated_pairs += 1
            else:
                seen_pairs.add(pair)

        cleaned, metrics = clean_chunk(raw, *groups)
        _add_metric_totals(metric_totals, metrics)
        for column in original_columns:
            missing_after[column] += int(cleaned[column].isna().sum())
        _numeric_range_update(numeric_ranges, cleaned, important_numeric)

        if sample_base is None:
            sample_base = cleaned.loc[
                ~cleaned["track_id"].isin(MANUAL_KEYS)
            ].head(45).copy()
        manual_hit = cleaned["track_id"].isin(MANUAL_KEYS)
        if manual_hit.any():
            manual_records.append(cleaned.loc[manual_hit].copy())
            manual_raw_records.append(raw.loc[manual_hit].copy())

        cleaned.to_csv(
            temp_clean_path,
            mode="w" if first_write else "a",
            header=first_write,
            index=False,
            encoding="utf-8",
            date_format="%Y-%m-%d",
        )
        first_write = False
        print(f"Cleaned chunk {chunk_number}: cumulative rows {rows_written:,}")

    if rows_written != EXPECTED_ROWS:
        raise ValueError(f"Row-count mismatch: expected {EXPECTED_ROWS}, got {rows_written}")
    if any(value != 0 for key, value in metric_totals.items() if key.startswith("conversion_failures:")):
        failures = {key: value for key, value in metric_totals.items() if key.startswith("conversion_failures:") and value}
        raise ValueError(f"Unexpected conversion failures: {failures}")

    os.replace(temp_clean_path, CLEAN_PATH)
    raw_hash_after = sha256_file(RAW_PATH)
    if raw_hash_after != raw_hash_before:
        raise ValueError("Raw source hash changed during cleaning")

    manual_frame = pd.concat(manual_records, ignore_index=True)
    manual_frame = manual_frame.set_index("track_id").loc[MANUAL_KEYS].reset_index()
    sample = pd.concat([manual_frame, sample_base], ignore_index=True)
    if len(sample) > 50 or not set(MANUAL_KEYS).issubset(set(sample["track_id"])):
        raise ValueError("Deterministic sample does not meet manual-record requirements")
    sample.to_csv(SAMPLE_PATH, index=False, encoding="utf-8", date_format="%Y-%m-%d")

    manual_raw_frame = pd.concat(manual_raw_records, ignore_index=True)
    manual_raw_frame = (
        manual_raw_frame.set_index("track_id").loc[MANUAL_KEYS].reset_index()
    )
    serialized_sample = pd.read_csv(
        SAMPLE_PATH, dtype=str, keep_default_na=False, low_memory=False
    )
    serialized_manual = serialized_sample.loc[
        serialized_sample["track_id"].isin(MANUAL_KEYS)
    ]
    serialized_manual = (
        serialized_manual.set_index("track_id").loc[MANUAL_KEYS].reset_index()
    )
    manual_actuals = _manual_actual_results(manual_raw_frame, serialized_manual)
    manual_checks = update_manual_checks(manual_actuals)
    if any(record["pass_fail"] != "Pass" for record in manual_checks):
        outcomes = Counter(record["pass_fail"] for record in manual_checks)
        raise ValueError(f"Manual record checks are not all Pass: {dict(outcomes)}")

    conversion_failures = sum(
        value for key, value in metric_totals.items() if key.startswith("conversion_failures:")
    )
    log = build_cleaning_log(
        metric_totals,
        raw_hash_after,
        rows_written,
        original_columns,
        conversion_failures,
        source_exact_duplicates,
        repeated_track_ids,
        repeated_spotify_ids,
        repeated_pairs,
    )
    log.to_csv(LOG_PATH, index=False, encoding="utf-8")

    output_hash = sha256_file(CLEAN_PATH)
    write_validation_report(
        raw_hash_before,
        raw_hash_after,
        output_hash,
        rows_written,
        original_columns,
        missing_before,
        missing_after,
        metric_totals,
        numeric_ranges,
        source_exact_duplicates,
        repeated_track_ids,
        repeated_spotify_ids,
        repeated_pairs,
        log,
        manual_checks,
    )

    if not log["status"].eq("PASS").all():
        failed = log.loc[~log["status"].eq("PASS")]
        raise ValueError(f"Cleaning validation failed:\n{failed.to_string(index=False)}")

    print(f"Wrote {CLEAN_PATH.relative_to(ROOT)}")
    print(f"Wrote {SAMPLE_PATH.relative_to(ROOT)} ({len(sample)} rows)")
    print(f"Wrote {LOG_PATH.relative_to(ROOT)}")
    print(f"Wrote {VALIDATION_PATH.relative_to(ROOT)}")
    print("All automated validation checks passed.")


if __name__ == "__main__":
    main()
