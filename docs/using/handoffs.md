# Handoffs: carrying on in a new session

Every request of a session carries the whole session, and a session resumed after an hour is
read whole again: a session of 400k tokens pays for 400k tokens with each step, a new one starts
from the rules and the tree. What makes a long session hard to leave is what it holds that the
notes do not. A handoff is that, written down:

- **`/rft-handoff [a note for the next session]`** asks Claude for one: it first brings the tree
  up to date (results and statuses of what the session touched, new ideas as directions, the
  digests of the concepts that changed), then calls `rft_handoff` with three short texts, 2,000
  characters in all: what was done (by note id), what to do first (what is running, where its
  output goes, what to check in it), and what neither a note nor a commit holds. The plugin adds
  what it can check by itself: the repositories with uncommitted or untracked files, among the
  session's folder, the tree's and the concepts' code. Claude also writes one unasked when you
  say you stop with work under way.
- **The next session in that folder** (a new one, or the same one after `/clear`) gets the
  handoff in its rules, in full, and works from it. The notes stay the record: where a note and
  the handoff differ, the note holds. A session after that one gets a single line pointing at
  it, for a week; a handoff left in another folder shows as one line until a session there
  takes it up.
- **`/rft-handoff show`** prints this folder's handoff and **`/rft-handoff clear`** removes it,
  both without a model turn.
- **A session grown large** is told so once when it passes 200k tokens and once at 400k, with
  the two commands that end it cheaply (`/rft-handoff`, then `/clear`).

A handoff is one file per session folder in `vault/.handoff/`, kept out of git by its own
`.gitignore`: it is the state of this machine, like the queue's. The handoff tool and its rule
are in the prompt only once the vault holds one.
