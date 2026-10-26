"""Independent, reproducible checks for DSO 576 Module 9.
Run: python verify_module9.py
Uses only pandas and sample CSV; does not import the Streamlit app.
"""
from pathlib import Path
import math
import pandas as pd

path = Path(__file__).resolve().parent / 'spotify_cleaned_sample.csv'
df = pd.read_csv(path, low_memory=False)
df['canonical_track_id'] = df['canonical_track_id'].astype(str)
low, high = 2001, 2023
cohort = df.loc[df['release_year'].between(low, high) & df['track_popularity'].notna()].copy()
ranked = cohort.sort_values(['track_popularity', 'canonical_track_id'], ascending=[False, True], kind='mergesort')
top_count = math.ceil(0.20 * len(ranked))
cutoff = ranked.iloc[top_count-1]['track_popularity'] if top_count else None
print('Cohort N:', len(cohort))
print('Top 20% N:', top_count)
print('Cutoff popularity:', cutoff)
print('Median popularity:', cohort['track_popularity'].median())
assert (len(cohort), top_count, cutoff) == (50, 10, 44.0)

stream_cohort = df.loc[df['release_year'].between(low, high) & df['streams_total'].notna()]
by_popularity = stream_cohort.sort_values(['track_popularity','canonical_track_id'], ascending=[False,True])
by_streams = stream_cohort.sort_values(['streams_total','canonical_track_id'], ascending=[False,True])
print('Explorer current popularity order (first 3):', by_popularity['title'].head(3).tolist())
print('Streams sort expected (first 3):', by_streams['title'].head(3).tolist())
assert by_popularity['canonical_track_id'].head(3).tolist() != by_streams['canonical_track_id'].head(3).tolist()
print('All independent checks passed.')
