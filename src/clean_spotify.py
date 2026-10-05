"""Clean the Spotify dataset and create a 50-row sample."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "spotify_full.csv"
OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "spotify_cleaned.csv"
)
SAMPLE_PATH = (
    PROJECT_ROOT / "data" / "sample" / "spotify_cleaned_sample_50.csv"
)

CHUNK_SIZE = 100_000

VALID_SOURCES = {
    "arc8_spotify_1m",
    "tidytuesday_spotify",
}

NUMERIC_COLUMNS = [
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
    "track_popularity",
    "streams_total",
]


def clean_chunk(chunk: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    """Clean one chunk and return it with removal counts."""
    valid_source_mask = chunk["source_dataset"].isin(VALID_SOURCES)
    removed_invalid_source = int((~valid_source_mask).sum())

    cleaned_chunk = chunk.loc[valid_source_mask].copy()

    unnamed_columns = [
        column
        for column in cleaned_chunk.columns
        if column.startswith("Unnamed:")
    ]
    cleaned_chunk = cleaned_chunk.drop(columns=unnamed_columns)

    text_columns = cleaned_chunk.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_chunk[column] = cleaned_chunk[column].map(
            lambda value: (
                value.strip()
                if isinstance(value, str)
                else value
            )
        )

    cleaned_chunk[text_columns] = cleaned_chunk[text_columns].replace(
        "",
        pd.NA,
    )

    cleaned_chunk[NUMERIC_COLUMNS] = cleaned_chunk[
        NUMERIC_COLUMNS
    ].apply(
        pd.to_numeric,
        errors="coerce",
    )

    missing_identifier_mask = (
        cleaned_chunk["spotify_id"].isna()
        | cleaned_chunk["title"].isna()
    )
    removed_missing_identifier = int(
        missing_identifier_mask.sum()
    )

    cleaned_chunk = cleaned_chunk.loc[
        ~missing_identifier_mask
    ].copy()

    return (
        cleaned_chunk,
        removed_invalid_source,
        removed_missing_identifier,
    )


def clean_dataset() -> None:
    """Clean the full dataset and save the outputs."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_PATH}"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    input_rows = 0
    output_rows = 0
    removed_invalid_source = 0
    removed_missing_identifier = 0
    first_chunk = True
    sample_pieces = []

    reader = pd.read_csv(
        INPUT_PATH,
        encoding="utf-8",
        encoding_errors="replace",
        chunksize=CHUNK_SIZE,
        low_memory=False,
    )

    for chunk_number, chunk in enumerate(reader):
        input_rows += len(chunk)

        (
            cleaned_chunk,
            chunk_invalid_source,
            chunk_missing_identifier,
        ) = clean_chunk(chunk)

        removed_invalid_source += chunk_invalid_source
        removed_missing_identifier += chunk_missing_identifier
        output_rows += len(cleaned_chunk)

        cleaned_chunk.to_csv(
            OUTPUT_PATH,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
            encoding="utf-8",
        )
        first_chunk = False

        sample_size = min(5, len(cleaned_chunk))
        sample_pieces.append(
            cleaned_chunk.sample(
                n=sample_size,
                random_state=42 + chunk_number,
            )
        )

        print(
            f"Processed {input_rows:,} input rows; "
            f"kept {output_rows:,} cleaned rows"
        )

    cleaned_sample = (
        pd.concat(sample_pieces, ignore_index=True)
        .sample(n=50, random_state=42)
        .reset_index(drop=True)
    )

    cleaned_sample.to_csv(
        SAMPLE_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nCleaning completed")
    print(f"Input rows: {input_rows:,}")
    print(
        "Removed invalid-source rows:",
        f"{removed_invalid_source:,}",
    )
    print(
        "Removed rows missing spotify_id or title:",
        f"{removed_missing_identifier:,}",
    )
    print(f"Cleaned rows: {output_rows:,}")
    print(f"Cleaned columns: {cleaned_sample.shape[1]}")
    print(f"Cleaned sample shape: {cleaned_sample.shape}")


if __name__ == "__main__":
    clean_dataset()