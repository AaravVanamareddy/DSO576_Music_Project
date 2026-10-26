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
