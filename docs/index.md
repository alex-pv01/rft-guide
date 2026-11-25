# What rft is

What is the best way to do research now that an AI can help with it, so that it is still your
research? rft's answer: you build a knowledge base of your project, and your agents work from
it.

rft (Reasoning Flow Tree) is a tool for keeping track of a research project: the questions you
ask, the experiments you run, the papers you read and what you conclude from them. Each becomes
one short note under the note it came from. Together the notes are the project's knowledge
base, a tree you read in your browser and plain files in your project. rft runs as a plugin for
Claude Code, so the same knowledge base is what Claude and your other agents start from: they
know what was tried and why, add what they do to it, and stay within what you allow.

![The tree view of the demo project: directions, experiments, references and a theory note, each under the note it came from](images/tree.png)

## How rft answers it

- **Your research in one place.** Questions, experiments, papers and arguments, each under the
  note it came from, with what was found and what was dropped. You add a note from the
  [tree view](using/tree-view.md) or edit one in any editor; papers to read wait in the
  [inbox](using/inbox.md); a kanban and a calendar show the same notes by status and by date.
- **A knowledge base that builds up.** A note you have checked is marked
  [verified](reference/statuses.md), by you and no one else. Notes group into lines of research,
  each with its page of results, and only verified notes become the snippets that papers are
  written from. What you know, and how you came to know it, stays in one place.
- **The same knowledge base for your agents.** Claude starts each session from a compact copy
  of the tree, so it knows what was tried and why and does not begin from nothing. What it does
  goes into the same record: an experiment gets its note before it is launched and its result
  when it is in.
- **You keep hold of them.** A note's [priority](using/kanban.md) is set by you alone. You
  comment or suggest on a part of a note, and it changes only when you accept. Lock a note and
  Claude can only suggest changes to its text. Any other model works under a
  [grant](using/agents.md) you give it: answer only, read the project, or change it.

## The tree

Three months into a project, the code and the results are still there, but the reasons are gone:
why this experiment, what it ruled out, which idea was dropped and why. With rft they are on
record as they happen, in four kinds of notes.

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
