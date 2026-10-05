from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE_PATH = Path("C:/Users/ian83/OneDrive/文件/DSO576_Music_Project/archive/data/full/spotify_full.csv")
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

DECISION_LOG_PATH = OUTPUT_DIR / "cleaning_decision_log.csv"
VALIDATION_SUMMARY_PATH = OUTPUT_DIR / "validation_summary.json"
GROUP_SUMMARY_PATH = OUTPUT_DIR / "genre_decade_summary.csv"
EXPECTED_CASES_PATH = OUTPUT_DIR / "difficult_case_expectations.json"
ACTUAL_CASES_PATH = OUTPUT_DIR / "difficult_case_actual.csv"
SAMPLE_PATH = OUTPUT_DIR / "cleaned_sample.csv"

DECISION_LOG = [
    {
        "rule": "Read the raw CSV without writing to the source file.",
        "reason": "The archive is the source of truth and must remain unchanged.",
        "check": "Compute the SHA-256 hash before and after the run; ensure the source file hash is unchanged.",
    },
    {
        "rule": "Preserve all rows unless a rule explicitly flags a value as invalid.",
        "reason": "The archive has no exact duplicates and no repeated IDs, so the analysis should not remove rows without evidence.",
        "check": "Exact duplicate count = 0 and repeated ID counts = 0 in the raw validation report.",
    },
    {
        "rule": "Trim and normalize text fields to reduce trailing whitespace and empty-string noise.",
        "reason": "String columns such as titles, album names, and genre labels should be treated the same way across rows.",
        "check": "Check that string values are stripped and empty strings are converted to missing values.",
    },
    {
        "rule": "Coerce numeric columns with pandas and mark out-of-range values as missing.",
        "reason": "Spotify popularity must remain on a 0-100 scale, while other numeric fields should be validated against known ranges.",
        "check": "Track popularity range stays within 0-100 and invalid numeric strings become nulls.",
    },
    {
        "rule": "Keep `streams_total` identified as modeled/estimated and do not use it as the headline metric.",
        "reason": "The metadata explicitly defines `streams_total` as estimated and not as the direct popularity score.",
        "check": "`streams_total_estimated` stays True for modeled rows and `track_popularity` remains primary in the grouped summary.",
    },
    {
        "rule": "Validate categorical fields and exclude missing genre keys from group averages.",
        "reason": "Missing `genre_l1` and `decade` values are not valid groups for the analysis, but they are still retained in the dataset.",
        "check": "Grouped averages use only rows with non-missing `genre_l1`, `decade`, and `track_popularity`.",
    },
    {
        "rule": "Flag suspicious values and keep them visible instead of silently coercing them away.",
        "reason": "Some rows have sparse chart or metadata fields by design; they should be documented and preserved.",
        "check": "Missing chart fields, blank album names, and anomaly flags remain visible in the cleaned dataset and the sample selection.",
    },
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_decision_log() -> None:
    pd.DataFrame(DECISION_LOG).to_csv(DECISION_LOG_PATH, index=False)


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = [
        "track_id",
        "spotify_id",
        "title",
        "title_normalized",
        "track_artist",
        "album_id",
        "album_name",
        "release_date",
        "source_dataset",
        "key_name",
        "mode_name",
        "genre_l1",
        "genre_l2",
        "genre_raw",
        "era",
        "emotional_arc",
        "tempo_band",
        "mood_cluster",
        "taste_cluster",
        "anomaly_flags",
        "streams_source",
        "chart_date_first",
    ]
    clean_df = df.copy()
    for column in text_columns:
        if column in clean_df.columns:
            clean_df[column] = clean_df[column].astype("string")
            clean_df[column] = clean_df[column].str.strip()
            clean_df[column] = clean_df[column].replace(r"^\s*$", pd.NA, regex=True)
    return clean_df


def clean_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    boolean_columns = [
        "explicit_flag",
        "has_audio_features",
        "streams_total_estimated",
        "popularity_imputed_aug",
        "is_likely_instrumental",
        "is_likely_live",
        "is_likely_spoken_word",
        "has_anomaly",
        "release_year_precision_aug",
    ]
    clean_df = df.copy()
    for column in boolean_columns:
        if column in clean_df.columns:
            clean_df[column] = clean_df[column].astype("string").str.strip().str.lower()
            clean_df[column] = clean_df[column].replace({"true": True, "false": False, "1": True, "0": False})
            clean_df[column] = clean_df[column].astype("boolean")
    return clean_df


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    numeric_columns = [
        "release_year",
        "duration_ms",
        "energy",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "speechiness",
        "liveness",
        "loudness",
        "tempo",
        "key",
        "mode",
        "time_signature",
        "track_popularity",
        "streams_total",
        "stream_density",
        "chart_peak_position",
        "weeks_on_chart",
        "track_age_days",
        "energy_loudness_ratio",
        "mood_index",
        "acoustic_synthetic_ratio",
        "novelty_score",
        "hit_probability",
        "fp_energy",
        "fp_valence",
        "fp_danceability",
        "fp_acousticness",
        "fp_instrumentalness",
        "fp_speechiness",
        "fp_liveness",
        "mean_energy_by_artist",
        "sonic_evolution_score",
        "genre_breadth",
        "catalog_size",
        "career_start_year",
        "career_end_year",
        "career_span_years",
        "longevity_score",
        "hit_rate",
        "artist_stream_mean_log",
        "artist_stream_median_log",
        "mean_energy_by_decade",
        "mean_valence_by_decade",
        "mean_tempo_by_decade",
        "mean_loudness_by_decade",
        "acousticness_decline_idx",
        "danceability_trend",
        "decade_track_count",
    ]
    for column in numeric_columns:
        if column in clean_df.columns:
            clean_df[column] = pd.to_numeric(clean_df[column], errors="coerce")

    range_checks = {
        "release_year": (1957, 2023),
        "duration_ms": (1, 3_600_000),
        "track_popularity": (0, 100),
        "energy": (0, 1),
        "valence": (0, 1),
        "danceability": (0, 1),
        "acousticness": (0, 1),
        "instrumentalness": (0, 1),
        "speechiness": (0, 1),
        "liveness": (0, 1),
        "track_age_days": (0, 36500),
        "tempo": (0, 300),
        "key": (0, 11),
        "mode": (0, 1),
        "time_signature": (0, 9),
    }
    for column, (lower, upper) in range_checks.items():
        if column in clean_df.columns:
            clean_df[column] = clean_df[column].where(clean_df[column].between(lower, upper), np.nan)
    return clean_df


def summarize_data(df: pd.DataFrame) -> dict:
    missing_counts = df.isna().sum().to_dict()
    validation = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "repeated_track_id": int(df["track_id"].duplicated().sum()) if "track_id" in df.columns else None,
        "repeated_spotify_id": int(df["spotify_id"].duplicated().sum()) if "spotify_id" in df.columns else None,
        "missing_counts": missing_counts,
        "genre_l1_counts": df["genre_l1"].value_counts(dropna=False).head(10).to_dict() if "genre_l1" in df.columns else None,
        "decade_counts": df["decade"].value_counts(dropna=False).head(10).to_dict() if "decade" in df.columns else None,
        "track_popularity_range": {
            "min": float(df["track_popularity"].min()) if "track_popularity" in df.columns else None,
            "max": float(df["track_popularity"].max()) if "track_popularity" in df.columns else None,
            "nulls": int(df["track_popularity"].isna().sum()) if "track_popularity" in df.columns else None,
        },
        "streams_total_range": {
            "min": float(df["streams_total"].min()) if "streams_total" in df.columns else None,
            "max": float(df["streams_total"].max()) if "streams_total" in df.columns else None,
            "nulls": int(df["streams_total"].isna().sum()) if "streams_total" in df.columns else None,
        },
        "modeled_estimated_streams": int(df["streams_total_estimated"].sum()) if "streams_total_estimated" in df.columns else None,
    }
    return validation


def build_group_summary(df: pd.DataFrame) -> pd.DataFrame:
    valid = df.loc[
        df["genre_l1"].notna()
        & df["decade"].notna()
        & df["track_popularity"].notna()
    ].copy()
    grouped = (
        valid.groupby(["genre_l1", "decade"], dropna=False, as_index=False)
        .agg(
            valid_tracks=("track_popularity", "size"),
            avg_track_popularity=("track_popularity", "mean"),
            avg_streams_total=("streams_total", "mean"),
        )
        .sort_values(["genre_l1", "decade"])
    )
    return grouped.reset_index(drop=True)


def select_difficult_cases(df: pd.DataFrame) -> pd.DataFrame:
    candidates = []
    if "album_name" in df.columns:
        candidates.append(df[df["album_name"].isna()].head(1))
    if "chart_peak_position" in df.columns:
        candidates.append(df[df["chart_peak_position"].isna() & df["weeks_on_chart"].isna()].head(1))
    if "has_anomaly" in df.columns:
        candidates.append(df[df["has_anomaly"] == True].head(1))
    if {"genre_l1", "decade", "track_popularity"}.issubset(df.columns):
        high_popularity = df[(df["genre_l1"].notna()) & (df["decade"].notna()) & (df["track_popularity"].between(90, 100))]
        if not high_popularity.empty:
            candidates.append(high_popularity.head(1))
    if {"streams_total_estimated", "streams_total"}.issubset(df.columns):
        estimated = df[(df["streams_total_estimated"] == True) & (df["streams_total"].notna())]
        if not estimated.empty:
            candidates.append(estimated.sort_values("streams_total", ascending=False).head(1))

    sample = pd.concat(candidates, ignore_index=True) if candidates else df.head(1).copy()
    sample = sample.drop_duplicates(subset=["track_id"]).reset_index(drop=True)
    if len(sample) < 5:
        extra = df.loc[~df.index.isin(sample.index)].head(5 - len(sample))
        sample = pd.concat([sample, extra], ignore_index=True).drop_duplicates(subset=["track_id"]).head(5)
    return sample.reset_index(drop=True)


def build_expected_case_requirements() -> dict:
    return {
        "case_1_missing_album_name": {
            "expected": "album_name is missing for the selected record",
            "reason": "A catalog row may legitimately not have album metadata, and this should remain missing rather than being imputed.",
        },
        "case_2_non_charting_track": {
            "expected": "chart_peak_position and weeks_on_chart are missing",
            "reason": "Non-charting tracks are valid and should not be treated as data errors.",
        },
        "case_3_anomaly_flag": {
            "expected": "has_anomaly is True",
            "reason": "The dataset intentionally flags unusual records; they remain part of the raw catalog but should be highlighted.",
        },
        "case_4_high_popularity_track": {
            "expected": "track_popularity is between 90 and 100 and genre_l1/decade are present",
            "reason": "The main metric is Spotify popularity score and should remain valid for the leading genre/decade comparisons.",
        },
        "case_5_estimated_streams": {
            "expected": "streams_total_estimated is True and streams_total is not missing",
            "reason": "The stream count is modeled/estimated and should remain labeled as such rather than treated as direct popularity.",
        },
    }


def validate_expected_cases(df: pd.DataFrame) -> dict:
    expected_requirements = build_expected_case_requirements()
    actual = {}
    actual["case_1_missing_album_name"] = bool(df["album_name"].isna().any()) if "album_name" in df.columns else False
    actual["case_2_non_charting_track"] = bool((df["chart_peak_position"].isna() & df["weeks_on_chart"].isna()).any()) if {"chart_peak_position", "weeks_on_chart"}.issubset(df.columns) else False
    actual["case_3_anomaly_flag"] = bool(df["has_anomaly"].fillna(False).any()) if "has_anomaly" in df.columns else False
    actual["case_4_high_popularity_track"] = bool(((df["track_popularity"].between(90, 100)) & df["genre_l1"].notna() & df["decade"].notna()).any()) if {"track_popularity", "genre_l1", "decade"}.issubset(df.columns) else False
    actual["case_5_estimated_streams"] = bool(((df["streams_total_estimated"] == True) & df["streams_total"].notna()).any()) if {"streams_total_estimated", "streams_total"}.issubset(df.columns) else False
    return {"expected_requirements": expected_requirements, "actual_checks": actual}


def main() -> None:
    source_hash_before = sha256_file(SOURCE_PATH)
    raw_df = pd.read_csv(SOURCE_PATH, low_memory=False)
    print("[1/6] Loaded raw dataset:", raw_df.shape)

    clean_df = clean_text_columns(raw_df)
    clean_df = clean_boolean_columns(clean_df)
    clean_df = clean_numeric_columns(clean_df)
    print("[2/6] Standardized text, boolean, and numeric types.")

    clean_df["streams_total_status"] = np.where(
        clean_df["streams_total_estimated"].fillna(False) == True,
        "modeled_estimated",
        "not_modeled_or_missing",
    )

    validation_summary = summarize_data(clean_df)
    validation_summary["source_sha256_before"] = source_hash_before
    validation_summary["source_sha256_after"] = sha256_file(SOURCE_PATH)
    validation_summary["source_unchanged"] = validation_summary["source_sha256_before"] == validation_summary["source_sha256_after"]
    validation_summary["rows_after_cleaning"] = int(len(clean_df))
    validation_summary["rows_before_cleaning"] = int(len(raw_df))
    validation_summary["rows_preserved"] = validation_summary["rows_after_cleaning"] == validation_summary["rows_before_cleaning"]

    with VALIDATION_SUMMARY_PATH.open("w", encoding="utf-8") as fh:
        json.dump(validations := validation_summary, fh, ensure_ascii=False, indent=2)

    group_summary = build_group_summary(clean_df)
    group_summary.to_csv(GROUP_SUMMARY_PATH, index=False)
    print("[3/6] Saved validation summary and grouped genre/decade averages.")

    save_decision_log()
    print("[4/6] Saved the cleaning decision log.")

    expected_cases = build_expected_case_requirements()
    with EXPECTED_CASES_PATH.open("w", encoding="utf-8") as fh:
        json.dump(expected_cases, fh, ensure_ascii=False, indent=2)

    sample_df = select_difficult_cases(clean_df)
    sample_df.to_csv(SAMPLE_PATH, index=False)
    sample_df.to_csv(ACTUAL_CASES_PATH, index=False)

    expected_checks = validate_expected_cases(sample_df)
    with (OUTPUT_DIR / "difficult_case_actual_checks.json").open("w", encoding="utf-8") as fh:
        json.dump(expected_checks, fh, ensure_ascii=False, indent=2)
    print("[5/6] Saved expected and actual difficult-case checks and cleaned sample.")

    print("[6/6] Summary: rows before =", len(raw_df), "; rows after =", len(clean_df), "; duplicates =", validation_summary["exact_duplicate_rows"]) 
    print("Row preservation check:", validation_summary["rows_preserved"])
    print("Source unchanged check:", validation_summary["source_unchanged"])
    print("Group summary rows:", len(group_summary))
    print("Cleaned sample rows:", len(sample_df))

    return clean_df, group_summary, validations


if __name__ == "__main__":
    main()
