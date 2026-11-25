# The notes in one folder, the code in others

A session works on the tree of the nearest `.rft/config.json`: in its own folder, else in the
closest folder above it, so the tree is active in every subfolder of the project. When the code
lives apart from the notes, link to the tree instead of starting a second one: a
`.rft/config.json` holding only

```json
{ "tree": "../notes" }
```

makes every session in that folder, or below it, work on the tree in `../notes` (relative to
the folder that holds `.rft/`, or absolute). With the notes in `phd/notes/` and the repositories
under `phd/code/`, one link in `phd/code/.rft/config.json` serves them all: Claude adds and
updates notes in `phd/notes/`, and nothing is written beside the code.

- The nearest config wins: a repository with its own tree below a link keeps its own.
- A link points at the tree's own folder, not at another link; one that leads nowhere leaves
  RFT off and says why, at session start, in the pane and on `/rft`.
- `/rft-init` starts no second tree in a folder that already works on one.
- Claude's own Read and Edit tools ask before touching files outside the session's folder;
  start the session with `--add-dir <the tree's folder>` to let them read notes freely.
- Sessions in different repositories can add notes to the same tree: ids are taken from the
  notes and the config as they are on disk at that moment.
