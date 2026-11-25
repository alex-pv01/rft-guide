# Notes in one folder, code in others

Many projects keep their notes in one place and their code in several repositories. rft handles
that with a link: the code folders point at the tree, and no second tree is started.

## Which tree a session works on

A session works on the tree of the nearest `.rft/config.json`: the one in its own folder, or
else in the closest folder above it. So a tree is active in every subfolder of its project.

## Linking a code folder to the tree

In the folder that holds your code, create `.rft/config.json` with only this:

```json
{ "tree": "../notes" }
```

Every session started in that folder, or below it, now works on the tree in `../notes`. The path
is relative to the folder that holds `.rft/`, or absolute.

For example, with the notes in `phd/notes/` and the repositories under `phd/code/`, one link in
`phd/code/.rft/config.json` serves all the repositories. Claude adds and updates notes in
`phd/notes/`, and nothing is written beside the code.

## Good to know

- **The nearest config wins.** A repository with a tree of its own, below a link, keeps its own.
- **A link points at a tree, not at another link.** A link that leads nowhere leaves rft off,
  and says why at session start, in the pane and on `/rft`.
- **No second tree by accident.** `/rft-init` does not start a tree in a folder that already
  works on one.
- **Let Claude read the notes freely.** Claude's own Read and Edit tools ask before touching
  files outside the session's folder. Start the session with `--add-dir <the tree's folder>`
  to avoid being asked each time.
- **Several repositories, one tree.** Sessions in different repositories can add notes to the
  same tree. Ids are taken from the notes and the config as they are on disk at that moment.
