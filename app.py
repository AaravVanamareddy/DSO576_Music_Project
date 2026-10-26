"""Spotify Track Promotion Strategy — Streamlit MVP.

Run: streamlit run app.py
Place spotify_cleaned_full.csv (preferred) or spotify_cleaned_sample.csv beside app.py.
All comparisons are descriptive; no hit prediction or automated recommendations.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
PRIMARY = ["danceability", "energy", "valence", "acousticness", "instrumentalness"]
AUDIO = PRIMARY + ["speechiness", "liveness"]
SCATTER_FEATURES = AUDIO + ["tempo", "loudness", "duration_ms"]
REQUIRED = ["canonical_track_id", "title", "track_artist", "genre_l1", "genre_l2", "release_year", "track_popularity", "streams_total", "streams_total_estimated"] + SCATTER_FEATURES

st.set_page_config(page_title="Spotify Track Promotion Strategy", page_icon="🎵", layout="wide")

@st.cache_data(show_spinner="Loading music data...")
def load_tracks(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    ids = df["canonical_track_id"]
    if ids.isna().any() or ids.astype(str).str.strip().eq("").any() or ids.duplicated().any():
        raise ValueError("canonical_track_id must be unique and nonmissing")
    df["canonical_track_id"] = ids.astype(str)
    for c in ["release_year", "track_popularity", "streams_total"] + SCATTER_FEATURES:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["streams_total_estimated"] = df["streams_total_estimated"].astype("string").str.lower().isin(["true", "1", "yes"])
    return df

def filter_cohort(df, genre, low, high, metric, exclude_estimated):
    cohort = df[df["release_year"].between(low, high) & df[metric].notna()]
    if genre != "All genres":
        cohort = cohort[cohort["genre_l1"] == genre]
    if metric == "streams_total" and exclude_estimated:
        cohort = cohort[~cohort["streams_total_estimated"]]
    return cohort.copy()

def split_success_groups(cohort, metric, fraction):
    ranked = cohort.sort_values([metric, "canonical_track_id"], ascending=[False, True], kind="mergesort")
    n_top = math.ceil(len(ranked) * fraction)
    top, other = ranked.iloc[:n_top].copy(), ranked.iloc[n_top:].copy()
    cutoff = top.iloc[-1][metric] if n_top else None
    return ranked, top, other, cutoff

def fmt_num(x, digits=0):
    return "N/A" if pd.isna(x) else f"{x:,.{digits}f}"

def feature_means(top, other):
    rows = []
    for f in PRIMARY:
        rows.extend([
            {"Feature": f, "Group": "Top", "Mean": top[f].mean(), "Valid N": int(top[f].count())},
            {"Feature": f, "Group": "Other", "Mean": other[f].mean(), "Valid N": int(other[f].count())},
        ])
    return pd.DataFrame(rows)

def info_table(tracks):
    cols = ["canonical_track_id", "title", "track_artist", "genre_l1", "release_year", "track_popularity", "streams_total", "streams_total_estimated"]
    return tracks[cols].rename(columns={"canonical_track_id":"ID", "title":"Track", "track_artist":"Artist", "genre_l1":"Genre", "release_year":"Year", "track_popularity":"Popularity", "streams_total":"Streams", "streams_total_estimated":"Estimated streams"})

def add_shortlist(track_id):
    if track_id not in st.session_state.shortlist:
        st.session_state.shortlist.append(track_id)

def show_profile(row, top, is_in_cohort):
    st.subheader(f"{row['title']} — {row['track_artist']}")
    st.caption("Inside current comparison cohort" if is_in_cohort else "Outside current comparison cohort — compared against current Top group only")
    st.write(f"**Genre:** {row['genre_l1']}  ·  **Year:** {fmt_num(row['release_year'])}  ·  **Popularity:** {fmt_num(row['track_popularity'])}  ·  **Streams:** {fmt_num(row['streams_total'])}" + (" (estimated)" if row["streams_total_estimated"] else ""))
    rows = []
    for f in PRIMARY:
        mean = top[f].mean()
        value = row[f]
        rows.append({"Feature": f, "Track": value, "Top mean": mean, "Difference (track − top mean)": value - mean if pd.notna(value) and pd.notna(mean) else np.nan, "Top valid N": int(top[f].count())})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.button("Add to shortlist", key="add_" + str(row["canonical_track_id"]), on_click=add_shortlist, args=(str(row["canonical_track_id"]),))

available = [ROOT / "spotify_cleaned_full.csv", ROOT / "spotify_cleaned_sample.csv"]
found = next((p for p in available if p.is_file()), None)
if found is None:
    st.error("No data file found. Put spotify_cleaned_full.csv (preferred) or spotify_cleaned_sample.csv in the same folder as app.py.")
    st.stop()
try:
    data = load_tracks(str(found))
except Exception as exc:
    st.error(f"Data validation failed: {exc}")
    st.stop()

if "shortlist" not in st.session_state:
    st.session_state.shortlist = []

st.title("🎵 Spotify Track Promotion Strategy")
st.write("Explore historical track characteristics to identify candidates for **human promotional review**—not to predict hits or allocate budgets.")
if "sample" in found.name.lower():
    st.warning("DEMO: Using the 50-row smoke-test sample. Rankings, distributions, and artist patterns are **not validated against the full dataset**.")
else:
    st.caption(f"Source: {found.name} · {len(data):,} canonical tracks")

valid_years = data["release_year"].dropna()
if valid_years.empty:
    st.error("No valid release years. Cannot create a year-filtered comparison cohort.")
    st.stop()
y_min, y_max = int(valid_years.min()), int(valid_years.max())
with st.sidebar:
    st.header("Global comparison cohort")
    genres = sorted(data["genre_l1"].dropna().astype(str).unique().tolist())
    genre = st.selectbox("Broad genre", ["All genres"] + genres)
    yrange = st.slider("Release years (inclusive)", min_value=y_min, max_value=y_max, value=(y_min, y_max))
    metric_label = st.selectbox("Success metric", ["Popularity (0–100)", "Streams (includes estimates)"])
    metric = "track_popularity" if metric_label.startswith("Popularity") else "streams_total"
    fraction = st.selectbox("Top group share", [0.10, 0.20, 0.30], index=1, format_func=lambda x: f"Top {x:.0%}")
    exclude_est = st.checkbox("Exclude estimated streams", disabled=metric != "streams_total")
    if metric != "streams_total":
        exclude_est = False
    unknown_years = int(data["release_year"].isna().sum())
    st.caption(f"Unknown release years excluded: {unknown_years:,}")

cohort = filter_cohort(data, genre, yrange[0], yrange[1], metric, exclude_est)
ranked, top, other, cutoff = split_success_groups(cohort, metric, fraction)
with st.sidebar:
    st.write(f"**Cohort:** {len(cohort):,} tracks  ·  **Metric:** {metric_label}")
    if metric == "streams_total" and len(cohort):
        st.caption(f"Estimated streams records in cohort: {cohort['streams_total_estimated'].mean():.1%}")

if cohort.empty:
    st.info("No tracks match the current filters. Widen the release years or change genre/metric.")
    st.stop()

tab_overview, tab_explorer, tab_artist, tab_shortlist = st.tabs(["Overview", "Track Explorer", "Artist View", "Promotion Shortlist"])
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cohort tracks", f"{len(cohort):,}")
    c2.metric(f"Top {fraction:.0%} tracks", f"{len(top):,}")
    c3.metric("Median popularity", fmt_num(cohort["track_popularity"].median(), 1))
    c4.metric("Median streams", fmt_num(cohort["streams_total"].median()))
    st.caption(f"Top cutoff (last selected {metric_label}): {fmt_num(cutoff, 1 if metric == 'track_popularity' else 0)} · Popularity valid N={cohort['track_popularity'].count():,} · Streams valid N={cohort['streams_total'].count():,}. Streams may include estimates unless excluded when selected as the metric.")
    st.subheader("Audio feature comparison: Top vs Other")
    means = feature_means(top, other)
    st.plotly_chart(px.bar(means, x="Feature", y="Mean", color="Group", barmode="group", hover_data=["Valid N"], range_y=[0, 1], title="Means of 0–1 audio features"), use_container_width=True)
    st.dataframe(means, hide_index=True, use_container_width=True)
    st.subheader("Feature vs selected success metric")
    feature = st.selectbox("Audio feature", SCATTER_FEATURES)
    eligible = cohort[["canonical_track_id", feature, metric]].dropna()
    sample = eligible.sample(n=min(5000, len(eligible)), random_state=576) if len(eligible) > 5000 else eligible
    units = {"tempo": "BPM", "loudness": "dB", "duration_ms": "milliseconds"}
    label = f"{feature} ({units[feature]})" if feature in units else f"{feature} (0–1)"
    if len(sample):
        fig = px.scatter(sample, x=feature, y=metric, opacity=0.55, labels={feature: label, metric: metric_label}, title=f"Displayed {len(sample):,} of {len(eligible):,} valid track pairs")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid track pairs for this feature and metric.")
    st.subheader("Typical Top-group profile")
    st.plotly_chart(px.bar(means[means["Group"] == "Top"], x="Mean", y="Feature", orientation="h", range_x=[0, 1], hover_data=["Valid N"]), use_container_width=True)
    st.subheader("Top tracks preview")
    st.dataframe(info_table(ranked.head(10)), hide_index=True, use_container_width=True)

with tab_explorer:
    st.subheader("Find a track")
    query = st.text_input("Search track title or artist (full dataset)", key="query")
    hits = data
    if query.strip():
        hits = hits[data["title"].fillna("").str.contains(query.strip(), case=False, regex=False) | data["track_artist"].fillna("").str.contains(query.strip(), case=False, regex=False)]
    hits = hits.sort_values(["track_popularity", "canonical_track_id"], ascending=[False, True], na_position="last")
    st.caption(f"{len(hits):,} matches · showing up to 100 sorted by popularity. Search spans all tracks, including outside cohort.")
    st.dataframe(info_table(hits.head(100)), hide_index=True, use_container_width=True)
    if len(hits):
        choices = hits.head(500)
        ids = choices["canonical_track_id"].tolist()
        labels = dict(zip(choices["canonical_track_id"], choices["title"].fillna("Untitled") + " — " + choices["track_artist"].fillna("Unknown") + " [" + choices["canonical_track_id"] + "]"))
        selected = st.selectbox("Inspect track", ids, format_func=lambda x: labels[x])
        row = data.set_index("canonical_track_id").loc[selected]
        show_profile(row, top, selected in set(cohort["canonical_track_id"]))

with tab_artist:
    artists = sorted(data["track_artist"].dropna().astype(str).unique().tolist())
    term = st.text_input("Search artist", key="artist_query")
    matching_artists = [a for a in artists if term.casefold() in a.casefold()]
    if not matching_artists:
        st.info("No matching artists in the dataset.")
    else:
        artist = st.selectbox("Select artist", matching_artists)
        songs = ranked[ranked["track_artist"] == artist]
        ca, cb = st.columns(2)
        ca.metric("Artist cohort tracks", len(songs))
        cb.metric("Artist median popularity", fmt_num(songs["track_popularity"].median(), 1))
        if songs.empty:
            st.info("This artist has no tracks in the current comparison cohort.")
        else:
            st.dataframe(info_table(songs.head(100)), hide_index=True, use_container_width=True)
            profile_rows = []
            for f in PRIMARY:
                profile_rows.extend([{"Feature": f, "Group": "Artist", "Mean": songs[f].mean(), "Valid N": int(songs[f].count())}, {"Feature": f, "Group": "Cohort Top", "Mean": top[f].mean(), "Valid N": int(top[f].count())}])
            st.plotly_chart(px.bar(pd.DataFrame(profile_rows), x="Feature", y="Mean", color="Group", barmode="group", range_y=[0, 1], hover_data=["Valid N"]), use_container_width=True)
            a_ids = songs["canonical_track_id"].tolist()
            a_choice = st.selectbox("Inspect artist track", a_ids, format_func=lambda x: f"{data.set_index('canonical_track_id').loc[x, 'title']} [{x}]")
            show_profile(data.set_index("canonical_track_id").loc[a_choice], top, True)

with tab_shortlist:
    st.subheader("Manually selected promotion candidates")
    ids = list(dict.fromkeys(st.session_state.shortlist))
    if not ids:
        st.info("No tracks selected yet. Add tracks in Track Explorer or Artist View.")
    else:
        selected = data[data["canonical_track_id"].isin(ids)].copy()
        selected["In current cohort"] = selected["canonical_track_id"].isin(set(cohort["canonical_track_id"]))
        selected = selected.set_index("canonical_track_id").loc[ids].reset_index()
        display_cols = ["canonical_track_id", "title", "track_artist", "genre_l1", "release_year", "track_popularity", "streams_total", "streams_total_estimated"] + PRIMARY + ["In current cohort"]
        st.dataframe(selected[display_cols], hide_index=True, use_container_width=True)
        st.caption("Comparison benchmark: current cohort Top group means (not an automatic recommendation).")
        st.dataframe(means[means["Group"] == "Top"], hide_index=True, use_container_width=True)
        remove_id = st.selectbox("Remove a track", ids, format_func=lambda x: f"{data.set_index('canonical_track_id').loc[x, 'title']} [{x}]")
        if st.button("Remove selected track"):
            st.session_state.shortlist.remove(remove_id)
            st.rerun()
        if st.checkbox("Confirm clear all selections") and st.button("Clear shortlist"):
            st.session_state.shortlist = []
            st.rerun()
        exported = selected[display_cols].copy()
        exported["filter_genre"] = genre
        exported["filter_year_min"] = yrange[0]
        exported["filter_year_max"] = yrange[1]
        exported["filter_success_metric"] = metric
        exported["filter_top_group_share"] = fraction
        exported["filter_exclude_estimated_streams"] = exclude_est
        st.download_button("Download shortlist CSV", exported.to_csv(index=False).encode("utf-8-sig"), file_name="promotion_shortlist.csv", mime="text/csv")

st.divider()
st.caption("Historical descriptive comparison only. Popularity is not a probability; streams may be estimated. No causal effects, hit predictions, or promotional budget recommendations are implied. Selection is stored only in the current Streamlit session.")
