"""Independent checks for Aarav's Module 9 audit.
Run: python verify_aarav_module9.py
Requires: pandas, numpy, and spotify_cleaned_sample.csv in this directory or repo root.
This checks data/logic independently; UI behavior must also be tested manually.
"""
from pathlib import Path
import math
import pandas as pd

root = Path(__file__).resolve().parent
file = next((p for p in (root / 'spotify_cleaned_sample.csv', root.parent / 'spotify_cleaned_sample.csv') if p.exists()), None)
if file is None:
    raise SystemExit('Missing spotify_cleaned_sample.csv; put this script in the repository root.')
df = pd.read_csv(file)
for col in ('track_popularity', 'danceability', 'release_year'):
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['canonical_track_id'] = df['canonical_track_id'].astype(str)
cohort = df[df['release_year'].notna() & df['track_popularity'].notna()].copy()
cohort = cohort.sort_values(['track_popularity', 'canonical_track_id'], ascending=[False, True], kind='mergesort')
top = cohort.head(math.ceil(len(cohort) * 0.2))
expected_mean = top['danceability'].sum() / top['danceability'].count() if top['danceability'].count() else float('nan')
print('DATA:', file.name)
print('Cohort N:', len(cohort), 'Top N:', len(top))
print('Top danceability valid N:', top['danceability'].count())
print('Independently calculated top danceability mean:', expected_mean)
print('Pandas mean cross-check:', top['danceability'].mean())
assert (pd.isna(expected_mean) and pd.isna(top['danceability'].mean())) or abs(expected_mean - top['danceability'].mean()) < 1e-12

query = 'a'  # Replace with a real title/artist substring from the data for the final audit
mask = df['title'].fillna('').str.contains(query, case=False, regex=False) | df['track_artist'].fillna('').str.contains(query, case=False, regex=False)
matched = df[mask]
print('Search query:', repr(query), '| matches:', len(matched))
print('First 5 matches:', matched[['title', 'track_artist']].head(5).to_dict('records'))
assert all(query.casefold() in str(row['title']).casefold() or query.casefold() in str(row['track_artist']).casefold() for _, row in matched.iterrows())
print('Independent checks passed. Compare outputs with app UI and record evidence in my-audit.md.')
