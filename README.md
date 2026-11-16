# DSO 576 - Spotify Track Promotion Strategy

A Streamlit decision-support MVP for a music-label marketing manager. It helps a
manager compare **historical tracks already in the supplied dataset** with a
consistent genre, release-year, and success-metric cohort, then save a
human-reviewed promotion shortlist. It is descriptive only: it does not predict
hits, prove causation, or allocate promotional spend.

## Submission links

- **Live dashboard:** https://yolanda-music-dashboard.streamlit.app/
- **Demo video:** https://drive.google.com/file/d/1W5PeeBKKWW3WI8V9swcGCDq1XPC96A48/view?usp=drivesdk
- **Team repository:** https://github.com/AaravVanamareddy/DSO576_Music_Project

## Intended user and decision

The intended user is a music-label marketing manager preparing a promotion
review. They can set a broad-genre and inclusive release-year cohort, select
Popularity or Streams as the descriptive success metric, compare the Top group
with other historical tracks, inspect a dataset track or artist, and export a
manually selected shortlist for further review.

Candidate eligibility is deliberately limited to tracks already in the loaded
canonical dataset. Unreleased tracks or tracks outside that dataset cannot be
searched, uploaded, or compared in this MVP.

## Run locally

1. Use Python 3.10+ and install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Start the application:

   ```bash
   streamlit run app.py
   ```

3. Open the local URL printed by Streamlit. To run the included independent
   calculation check, use `python verify_module9.py`.

## Data scope and limitations

- Source: Kaggle Spotify Music Features Dataset, as described in
  `BUILD_SPEC (1).md`.
- The public deployment intentionally uses `spotify_cleaned_sample.csv`, a
  50-row smoke-test sample. Its results are suitable for demonstrating the
  workflow, **not** for full-population conclusions.
- If `spotify_cleaned_full.csv` is placed beside `app.py`, the application
  automatically prefers it. The full data file is not included in this
  repository/deployment.
- Release year, popularity, audio attributes, and streams can be missing; KPI
  captions show valid counts for each metric. Some stream totals are estimated.
  When Streams is selected, the optional exclusion control removes estimated
  stream records from that streams comparison cohort.
- The app has no Spotify API connection, audio playback, predictive model,
  causal inference, persistent multiuser shortlist, or promotion-budget
  recommendation. A shortlist is stored only for the active Streamlit session.

## Deployment

The publicly accessible Streamlit deployment is served from the personal
hosting fork `yolandaL597/DSO576_Music_Project`, branch `main`, with `app.py`
as its entry point. The team repository above remains the required code
submission link.


## Known limitation
The "Exclude estimated streams" toggle keeps only tracks with real stream
counts. In the current data that is 2 of 50 tracks, so metrics with the toggle
on are based on a very small sample. See CR-002 in change-requests.md.

## Opening the app
The app is hosted on Streamlit Community Cloud's free tier, so it sleeps
when idle. If you see "Your app is waking up," wait a few seconds and it
will load.