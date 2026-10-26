# Change Requests — Spotify Track Promotion Strategy

## Claims

| Member | Feature | Number |
| Arman |Exclude Estimated Streams toggle| Median Streams|
| Yolanda | Track Profile / Add to Shortlist | Top 20% Group Count |
| Elena | Genre Filter / Cohort Update | Median Popularity |

## Findings

### CR-001 — Track Profile Error

**Auditor:** Yolanda  
**Status:** Change requested

**Expected:** Track profiles should display correctly and allow users to add tracks to the Promotion Shortlist.

**Actual:** The Overview tab raises `KeyError: 'canonical_track_id'` after Top Tracks Preview. The error persists after rerunning.

**Evidence:** Tested with the 50-row sample under default filters. Traceback identifies `app.py`, lines 181 and 85.

**Requested change:** Preserve `canonical_track_id` when passing track records to `show_profile()` and retest the shortlist workflow.

### CHECK-001 — Top 20% Group Count

**Auditor:** Yolanda  
**Status:** Passed for tested sample

**Expected:** `ceil(0.20 × N)` tracks selected by popularity descending, breaking ties with canonical track ID.

**Actual:** Cohort N = 50, Top N = 10, cutoff popularity = 44.0.

**Evidence:** Independent results from `verify_module9.py` match the dashboard.

**Requested change:** None for the tested calculation. Full-data and other-filter validation remain untested.


### CHECK-002 – Median Streams

**Auditor:** Arman
**Status:** Passed for tested sample 

**Expected:** Median streams should be the median of streams_total across all 50 cohort tracks when the toggle is off, and across only 2 non estimated tracks when the toggle is on.

**Actual:** toggle off median is 3,283,769 and toggle on is 658,720, 810

**Evidence:** the 50-row sample, all genres, years 2001–2023, success metric = Streams. 
Toggle off: df["streams_total"].median()
Toggle on: df[df["streams_total_estimated"] == False]["streams_total"].median()
It returned the same numbers and passed

**Requested change:** No change is needed for the tested calculation. Although, keep in mind that I did not test other genres or date ranges 

### CR-002 – Exclude Estimated Streams Toggle

**Auditor:** Arman
**Status:** Change requested

**Expected:** Streaming numbers should change, becasuse excluding estimates is about streams data, so it shouldn’t change the cohort or median popularity. Once estimates are excluded, the label should say the streams are actual or real, not “includes estimates.” The app warns you when only a few tracks remain.

**Actual:** The whole cohort dropped from 50 to 2 tracks, and median popularity jumped from 27.5 to 99. The label still said “includes estimates.” No warning appeared.

**Evidence:** Settings: 50-row sample, all genres, 2001–2023, success metric = Streams (includes estimates).
The test: screenshot with the toggle off, then tick it and screenshot again. tracks 50 → 2, median popularity 27.5 → 99.0, median streams 3,283,769 → 658,720,810.
REVEALED  48 estimated and only 2 real, Flowers and Blinding Lights. These are the 2 that remain 

**Requested change:** Have a warning icon when the numbers drop to a certain amount. When toggle is on, change the label to something like "actual streams." Also, only the streams numbers should change, so the toggle shouldn’t remove tracks from the other metrics.
