# What rft is

Claude can write the code of a research project, launch its experiments and read its papers
faster than you can follow them. Every researcher now answers a question, on purpose or not:
what is the best way to do research with an AI's help, so that it is still your research?

rft (Reasoning Flow Tree) is one answer, built as a plugin for Claude Code. Its position is that
the work can be handed over and the reasoning cannot. The research stays yours as long as you
know what was tried, what it found and why, so Claude writes that down as it works. Every
experiment and every idea becomes one short note, each note hangs under the one it came from,
and you read the result as a live tree in your browser.

![The tree view of the demo project: directions, experiments, references and a theory note, each under the note it came from](images/tree.png)

## How rft answers it

1. **Claude does the work and keeps the record.** It adds an experiment's note before launching
    it, records the result when it is in, and adds a direction for each new idea. You do not fill
    in forms.
2. **You read and steer.** The tree in a browser follows the notes as they change: click a note
    to read it, filter by tag or status, group the notes into lines of research. At any point you
    can see where the project stands and say where it goes next.
3. **Only you verify.** A note is verified when you have checked what it claims. Claude can
    suggest it and cannot do it. Only verified notes become snippets, the pieces of LaTeX that
    rft's documents are written from.

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
