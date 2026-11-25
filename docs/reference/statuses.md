# Statuses

`planned` →, `running` …, `done` ✓, `idea` ?, `dropped` ✗, `discussed` · (not pursued),
`moved` ↗, and two a done note goes on to:

- `verified` ✔: you checked what the note claims. Only you verify a note, with **Verify** in its
  drawer; Claude suggests it (`rft_set_status verified` writes `suggested_verified:` with its
  reason, which you accept or dismiss). Verifying locks the note and stamps it (`verified: <date>
  <fingerprint>`) with what it claims: an experiment's Result, a theory note's Statement and
  Explanation, a reference's Source and Key results, a direction's Idea. An experiment with a
  notebook is ready once its run reproduced it; a direction once a note under it is verified.
  Only verified notes become snippets (see Snippets and documents).
- `review` ↺: a verified note whose claim may no longer hold. It goes there by itself, unlocked
  and with a History line, when what it claims changes (an accepted suggestion, an edit), when it
  is superseded, or when its notebook's run differs or fails; Claude sets one there when it finds
  a reason (the session asks you first, as the note is locked), and so can you (**Back to
  review**). Verify it again, or give it another status.

The tree draws a verified note with a ring, dashed in review; the kanban has a column for each.
