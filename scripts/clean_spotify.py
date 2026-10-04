"""Create an audited, non-destructive cleaned Spotify dataset.

The script intentionally performs only the approved transformations:
1. convert release_date and chart_date_first to datetime;
2. strip outer whitespace from track_artist.

It preserves all rows and leaves the source CSV untouched.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "spotify_full.csv"
DEFAULT_OUTPUT = ROOT / "data" / "spotify_clean.csv"
DEFAULT_REPORT = ROOT / "reports" / "spotify_cleaning_report.md"

DATE_COLUMNS = ("release_date", "chart_date_first")
PRESERVED_COLUMNS = (
    "title",
    "genre_l1",
    "genre_l2",
    "genre_raw",
    "track_id",
    "spotify_id",
    "title_normalized",
    "anomaly_flags",
)
MAIN_ANALYSIS_COLUMNS = (
    "track_popularity",
    "streams_total",
    "genre_l1",
    "genre_l2",
    "release_year",
    "energy",
    "valence",
    "danceability",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "liveness",
)
AUDIO_FEATURE_COLUMNS = (
    "energy",
    "valence",
    "danceability",
    "acousticness",
    "instrumentalness",
    "speechiness",
    "liveness",
)


@dataclass
class Snapshot:
    """Quality checks recorded before and after each approved transformation."""

    label: str
    rows: int
    missing: pd.Series
    exact_duplicate_rows: int
    duplicate_track_ids: int
    duplicate_spotify_ids: int
    changed_columns: tuple[str, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for block in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "sha256": sha256(path),
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def duplicate_counts(frame: pd.DataFrame) -> tuple[int, int, int]:
    """Return extra exact rows and repeated non-null identifier values."""
    exact_rows = int(frame.duplicated().sum())
    track_ids = int(frame.loc[frame["track_id"].notna(), "track_id"].duplicated().sum())
    spotify_ids = int(
        frame.loc[frame["spotify_id"].notna(), "spotify_id"].duplicated().sum()
    )
    return exact_rows, track_ids, spotify_ids


def snapshot(frame: pd.DataFrame, label: str, changed_columns: tuple[str, ...] = ()) -> Snapshot:
    exact_rows, track_ids, spotify_ids = duplicate_counts(frame)
    return Snapshot(
        label=label,
        rows=len(frame),
        missing=frame.isna().sum().astype("int64"),
        exact_duplicate_rows=exact_rows,
        duplicate_track_ids=track_ids,
        duplicate_spotify_ids=spotify_ids,
        changed_columns=changed_columns,
    )


def assert_expected_columns(frame: pd.DataFrame) -> None:
    expected = set(DATE_COLUMNS + PRESERVED_COLUMNS + MAIN_ANALYSIS_COLUMNS + ("track_artist", "duration_ms"))
    absent = sorted(expected.difference(frame.columns))
    if absent:
        raise ValueError(f"Input is missing expected columns: {absent}")


def convert_dates(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    results: dict[str, dict[str, int]] = {}
    for column in DATE_COLUMNS:
        source = frame[column]
        source_non_null = source.notna()
        parsed = pd.to_datetime(source, format="%Y-%m-%d", errors="coerce")
        failures = int((source_non_null & parsed.isna()).sum())
        if failures:
            raise ValueError(f"{column} has {failures} failed non-null datetime conversions")
        if int(parsed.isna().sum()) != int(source.isna().sum()):
            raise AssertionError(f"{column} null count changed during datetime conversion")
        frame[column] = parsed
        results[column] = {
            "source_non_null": int(source_non_null.sum()),
            "converted_non_null": int(parsed.notna().sum()),
            "failed_conversions": failures,
            "missing_before": int(source.isna().sum()),
            "missing_after": int(parsed.isna().sum()),
        }
    return results


def strip_track_artist(frame: pd.DataFrame) -> int:
    before = frame["track_artist"].copy()
    after = before.str.strip()
    changed = before.notna() & after.ne(before)
    changed_count = int(changed.sum())
    if changed_count != 30:
        raise AssertionError(
            f"Expected 30 outer-whitespace track_artist changes; found {changed_count}"
        )
    if not after.loc[changed].eq(before.loc[changed].str.strip()).all():
        raise AssertionError("track_artist changes were not limited to outer whitespace")
    if int(before.isna().sum()) != int(after.isna().sum()):
        raise AssertionError("track_artist null count changed during strip")
    frame["track_artist"] = after
    return changed_count


def assert_preserved_columns(raw: pd.DataFrame, clean: pd.DataFrame) -> None:
    changed = [column for column in PRESERVED_COLUMNS if not raw[column].equals(clean[column])]
    if changed:
        raise AssertionError(f"Unapproved changes found in preserved columns: {changed}")


def validate_approved_invariants(raw: pd.DataFrame, clean: pd.DataFrame) -> dict[str, Any]:
    if len(raw) != len(clean):
        raise AssertionError("A source row was added or removed")

    numeric_columns = raw.select_dtypes(include="number").columns
    numeric_missing_changed = [
        column
        for column in numeric_columns
        if int(raw[column].isna().sum()) != int(clean[column].isna().sum())
    ]
    if numeric_missing_changed:
        raise AssertionError(f"Numeric missingness changed: {numeric_missing_changed}")
    numeric_values_changed = [
        column for column in numeric_columns if not raw[column].equals(clean[column])
    ]
    if numeric_values_changed:
        raise AssertionError(f"Numeric values changed: {numeric_values_changed}")

    main_missing = {column: int(clean[column].isna().sum()) for column in MAIN_ANALYSIS_COLUMNS}
    incomplete_main = {column: count for column, count in main_missing.items() if count != 0}
    if incomplete_main:
        raise AssertionError(f"Main analysis variables unexpectedly contain nulls: {incomplete_main}")

    popularity = clean["track_popularity"]
    if not popularity.between(0, 100).all():
        raise AssertionError("track_popularity contains values outside 0-100")
    invalid_audio = {
        column: int((~clean[column].between(0, 1)).sum())
        for column in AUDIO_FEATURE_COLUMNS
    }
    invalid_audio = {column: count for column, count in invalid_audio.items() if count}
    if invalid_audio:
        raise AssertionError(f"Audio features outside 0-1: {invalid_audio}")

    duration = clean["duration_ms"]
    if not duration.gt(0).all():
        raise AssertionError("duration_ms contains zero or negative values")
    release_year = clean["release_year"]
    if int(release_year.min()) != 1957 or int(release_year.max()) != 2023:
        raise AssertionError("release_year range differs from validated 1957-2023 range")

    return {
        "main_analysis_missing": main_missing,
        "track_popularity_min": float(popularity.min()),
        "track_popularity_max": float(popularity.max()),
        "audio_feature_ranges": {
            column: {"min": float(clean[column].min()), "max": float(clean[column].max())}
            for column in AUDIO_FEATURE_COLUMNS
        },
        "duration_min_ms": float(duration.min()),
        "duration_max_ms": float(duration.max()),
        "short_duration_count_le_4_seconds": int(duration.le(4_000).sum()),
        "long_duration_count_ge_100_minutes": int(duration.ge(6_000_000).sum()),
        "release_year_min": int(release_year.min()),
        "release_year_max": int(release_year.max()),
        "release_year_1957_count": int(release_year.eq(1957).sum()),
    }


def markdown_missing_table(snapshots: list[Snapshot]) -> list[str]:
    header = ["Column"] + [item.label for item in snapshots] + ["Change from baseline"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    baseline = snapshots[0].missing
    for column in baseline.index:
        values = [int(item.missing[column]) for item in snapshots]
        delta = values[-1] - values[0]
        lines.append("| " + " | ".join([column] + [str(value) for value in values] + [str(delta)]) + " |")
    return lines


def render_report(
    input_path: Path,
    output_path: Path,
    source_before: dict[str, Any],
    source_after: dict[str, Any],
    snapshots: list[Snapshot],
    date_results: dict[str, dict[str, int]],
    artist_changes: int,
    validation: dict[str, Any],
) -> str:
    lines = [
        "# Spotify Cleaning Transformation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source preservation",
        "",
        f"- Input: `{input_path.name}`",
        f"- Output: `{output_path.name}`",
        f"- Source SHA-256 before: `{source_before['sha256']}`",
        f"- Source SHA-256 after: `{source_after['sha256']}`",
        f"- Source size before/after: {source_before['size_bytes']} / {source_after['size_bytes']} bytes",
        f"- Source mtime (ns) before/after: {source_before['mtime_ns']} / {source_after['mtime_ns']}",
        "- Result: source file fingerprint is unchanged.",
        "",
        "## Transformation summaries",
        "",
    ]
    for item in snapshots:
        changed = ", ".join(f"`{column}`" for column in item.changed_columns) or "None (baseline)"
        lines.extend(
            [
                f"### {item.label}",
                "",
                f"- Row count: {item.rows}",
                f"- Columns changed in this step: {changed}",
                f"- Exact duplicate rows: {item.exact_duplicate_rows}",
                f"- Duplicate `track_id` values: {item.duplicate_track_ids}",
                f"- Duplicate `spotify_id` values: {item.duplicate_spotify_ids}",
                "",
            ]
        )

    lines.extend(["## Missing-value counts by stage", ""])
    lines.extend(markdown_missing_table(snapshots))
    lines.extend(["", "## Datetime conversion", ""])
    for column, result in date_results.items():
        lines.extend(
            [
                f"### `{column}`",
                "",
                f"- Current type: string/object input; proposed in-memory type: `datetime64[ns]`.",
                f"- Non-null source values: {result['source_non_null']}",
                f"- Successful conversions: {result['converted_non_null']}",
                f"- Failed conversions: {result['failed_conversions']}",
                f"- Missing before/after: {result['missing_before']} / {result['missing_after']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Text transformation",
            "",
            f"- `track_artist`: `.str.strip()` changed {artist_changes} non-null values; only outer whitespace was removed.",
            "- `title`, genre fields, `track_id`, `spotify_id`, existing `title_normalized`, and `anomaly_flags` were asserted unchanged.",
            "- Missing `title_normalized` values were retained; no transliteration or derivation was performed.",
            "",
            "## Validated values retained without alteration",
            "",
            f"- `track_popularity` range: {validation['track_popularity_min']} to {validation['track_popularity_max']}.",
            f"- `duration_ms` range: {validation['duration_min_ms']} to {validation['duration_max_ms']}; short (<=4 seconds): {validation['short_duration_count_le_4_seconds']}; long (>=100 minutes): {validation['long_duration_count_ge_100_minutes']}.",
            f"- `release_year` range: {validation['release_year_min']} to {validation['release_year_max']}; 1957 records: {validation['release_year_1957_count']}.",
            "- All core audio features passed the [0, 1] validation and were retained unchanged.",
            "- Missing `anomaly_flags` values were retained unchanged; no text was filled in.",
            "- No rows were removed and no missing numeric values were imputed.",
            "",
            "## CSV reload contract",
            "",
            "`spotify_clean.csv` stores dates as ISO `YYYY-MM-DD` strings. Reload it with `parse_dates=['release_date', 'chart_date_first']` to restore the validated datetime columns.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_output(frame: pd.DataFrame, output_path: Path, overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing output: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    if temporary_path.exists():
        temporary_path.unlink()
    try:
        frame.to_csv(output_path if overwrite else temporary_path, index=False, date_format="%Y-%m-%d")
        if not overwrite:
            temporary_path.replace(output_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def write_report(report: str, report_path: Path, overwrite: bool) -> None:
    if report_path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing report: {report_path}")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--overwrite", action="store_true", help="Allow replacement of existing outputs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    report_path = args.report.resolve()
    if input_path == output_path:
        raise ValueError("Output path must differ from the source CSV")
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    source_before = source_fingerprint(input_path)
    raw_df = pd.read_csv(input_path, keep_default_na=False, na_values=[""])
    assert_expected_columns(raw_df)
    clean_df = raw_df.copy(deep=True)

    snapshots = [snapshot(clean_df, "Baseline")]
    date_results = convert_dates(clean_df)
    assert_preserved_columns(raw_df, clean_df)
    snapshots.append(snapshot(clean_df, "After datetime conversion", DATE_COLUMNS))

    artist_changes = strip_track_artist(clean_df)
    assert_preserved_columns(raw_df, clean_df)
    snapshots.append(snapshot(clean_df, "After track_artist strip", ("track_artist",)))

    validation = validate_approved_invariants(raw_df, clean_df)
    source_after = source_fingerprint(input_path)
    if source_before != source_after:
        raise AssertionError("Source fingerprint changed; refusing to write output")

    write_output(clean_df, output_path, args.overwrite)
    report = render_report(
        input_path,
        output_path,
        source_before,
        source_after,
        snapshots,
        date_results,
        artist_changes,
        validation,
    )
    write_report(report, report_path, args.overwrite)
    print(f"Cleaned CSV written to: {output_path}")
    print(f"Transformation report written to: {report_path}")


if __name__ == "__main__":
    main()
