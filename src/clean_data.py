"""Clean the Spotify project data (DSO 576, Module 6).

Run from the repo root:
    python src/clean_data.py
"""
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA_PATH = REPO.parent / "archive" / "data" / "full" / "spotify_full.csv"
OUT_PATH = REPO / "data" / "sample" / "cleaned_sample.csv"

COLS = [
    "track_id", "title", "title_normalized", "track_artist",
    "genre_l1", "genre_l2", "release_year",
    "track_popularity", "streams_total", "streams_total_estimated", "streams_source",
    "danceability", "energy", "valence", "acousticness",
    "instrumentalness", "loudness", "tempo", "duration_ms", "explicit_flag",
]


def main():
    raw = pd.read_csv(DATA_PATH, usecols=COLS, low_memory=False)
    df = raw.copy()

    # Rule 1 (item 5): remove leading/trailing spaces from artist names
    df["track_artist"] = df["track_artist"].str.strip()

    # Rule 2 (item 7): "Unknown" genre is a placeholder, so treat it as missing
    for c in ["genre_l1", "genre_l2"]:
        df[c] = df[c].mask(df[c] == "Unknown")

    # Rule 3 (item 6): flag same title + artist, matching on the real title
    key = pd.DataFrame({
        "title": df["title"].str.strip().str.lower(),
        "artist": df["track_artist"],
    })
    has_both = key["title"].notna() & key["artist"].notna()
    df["possible_duplicate"] = has_both & key.duplicated(keep=False)

    # Rule 4 (item 8): flag tracks under 30 seconds or over 20 minutes
    df["unusual_duration"] = (df["duration_ms"] < 30_000) | (df["duration_ms"] > 20 * 60 * 1000)

    # Sample of 50 rows, including the difficult cases from item 12
    artist_idx = raw.index[raw["track_artist"].notna() & (raw["track_artist"] != raw["track_artist"].str.strip())][0]
    unknown_idx = raw.index[raw["genre_l1"] == "Unknown"][0]
    sample_ids = [artist_idx, unknown_idx, 4943, 792254, 1035552, 871130]
    sample_ids += list(df.index[df["title"].isna()][:2])
    sample_ids += list(df.index[df["track_artist"].isna()][:2])
    sample_ids += list(df[df["possible_duplicate"]].sample(5, random_state=1).index)
    sample_ids += list(df[df["unusual_duration"]].sample(5, random_state=1).index)
    sample_ids += list(df[df["genre_l1"].isna()].sample(5, random_state=1).index)
    sample_ids = list(dict.fromkeys(sample_ids))
    sample_ids += list(df.drop(index=sample_ids).sample(50 - len(sample_ids), random_state=1).index)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.loc[sample_ids].reset_index(names="source_row").to_csv(OUT_PATH, index=False)

    print("Sample rows saved:", len(sample_ids))
    print("Final check -> rows:", len(df), "| columns:", df.shape[1],
          "| possible_duplicate:", df["possible_duplicate"].sum(),
          "| unusual_duration:", df["unusual_duration"].sum(),
          "| missing genre:", df["genre_l1"].isna().sum())


if __name__ == "__main__":
    main()