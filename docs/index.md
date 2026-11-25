# What rft is

Claude can write the code of a research project, launch its experiments and read its papers
faster than you can follow them. Every researcher now answers a question, on purpose or not:
what is the best way to do research with an AI's help, so that it is still your research?

rft (Reasoning Flow Tree) is one answer, built as a plugin for Claude Code. Its position is that
you stay in charge and Claude works where you can see it. Every experiment and every idea
becomes one short note, each note hangs under the one it came from, and you read them as a live
tree in your browser. From there you monitor Claude, steer it, correct it, direct it and limit
it, and it still does real work for you.

![The tree view of the demo project: directions, experiments, references and a theory note, each under the note it came from](images/tree.png)

## How rft answers it

Claude runs the experiments and keeps the notes, so you do not fill in forms. What rft adds is
your hold on that work.

- **You see what it does.** An experiment gets its note before it is launched and its result
  when it is in, and each new idea gets a note under the one it came from. The
  [tree view](using/tree-view.md) follows the notes as they change, so you can read what Claude
  is doing, and why, while it does it.
- **You say where it goes.** The project starts from your question, and what matters most is
  yours to say: a note's [priority](using/kanban.md) is set by you alone, and Claude only
  suggests one. A dropped idea stays in the tree, so the path not taken is on record.
- **You correct it.** Edit a note's text in the page, or select a part of it and leave a comment
  or a suggestion, as in Overleaf. Ask Claude on that thread and it replies there: the note
  changes only when you accept.
- **You set its limits.** Lock a note and Claude can only suggest changes to its text: the
  plugin refuses its edits. Only you mark a note [verified](reference/statuses.md), and only verified
  notes become the snippets that rft's documents are written from. Any other model you bring in
  works under a [grant](using/agents.md) you give it: answer only, read the project, or change
  it.

## The tree

Three months into a project, the code and the results are still there, but the reasons are gone:
why this experiment, what it ruled out, which idea was dropped and why. With an assistant doing
the work this happens sooner, because more is run than anyone remembers the reason for. rft
writes the reasons down as they happen, in four kinds of notes.

| Note | Id | What it holds |
|---|---|---|
| **Direction** | `D03` | An idea, a question or a hypothesis, including the ones you rejected. `D00` is the question the project starts from. |
| **Experiment** | `E07` | Something you ran or computed, and what it found. |
| **Reference** | `R02` | A paper or a method you read: what it claims, where to check it, what it means for the project. |
| **Theory** | `T01` | A definition, method or argument of the project's own. |

Each note has a parent, so the notes form a tree: a question leads to an experiment, its result
to two new ideas, one of them to the next experiment. The tree shows what was tried and also why
a path was not taken.

## What else you get

- **Plain files.** The notes are markdown in a folder of your project (`vault/` by default).
  They work in Obsidian, in git and in any editor, and they are the source of truth.
- **More when you want it.** A kanban and a calendar over the same notes, a queue for
  experiments on your GPUs, result pages per line of research, LaTeX documents and slide decks
  built from verified results, and an inbox for papers to read. Each has a page under *Using rft*.

## Where to go next

1. [Install](start/install.md) the plugin: two commands.
2. Take the [first run on the demo](start/first-run.md): about five minutes, nothing to set up.
3. [Activate it in your project](start/activate.md).

rft was created by Gianni Moretti
([GianniMoretti/rft-plugin](https://github.com/GianniMoretti/rft-plugin)). This guide describes
the version developed at [alex-pv01/rft-plugin](https://github.com/alex-pv01/rft-plugin).
