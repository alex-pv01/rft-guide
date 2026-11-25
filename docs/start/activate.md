# Activate it in your project

rft does nothing in a project until you activate it there. One command does it.

## Start a tree

Open a Claude Code session in your project's folder and type `/rft-init` followed by the
question the project starts from:

```
/rft-init Can strong augmentation replace early stopping on small datasets?
```

This creates two things in the project:

- `.rft/config.json`, which marks the project as using rft;
- the vault, the folder that holds the notes:

```
vault/
  00 Index.md               the whole tree as an indented list, kept up to date for you
  directions/               D00 <your question>.md, then D01, D02, ...
  experiments/              E01 <title>.md, ...
  references/               R01 <title>.md, ...
  theory/                   T01 <title>.md, ...
  templates/                the empty form of each kind of note
```

Your question becomes `D00`, the root of the tree. Type `/rft` to see it: one dot, for now.

## Then work as usual

From here you do not run commands to keep the tree. Work with Claude as you normally do, and it
adds a note for each experiment before launching it, records the result, and adds a direction
for each idea that comes up, including the ones you turn down. [What changes once it is
active](../using/once-active.md) says exactly what Claude does and when.

You can edit any note by hand, in any editor or in Obsidian. The files are the source of truth.

## If you already have notes

If the vault's folders already hold notes (`vault/experiments`, `vault/directions` and the
others), `/rft-init` adopts them as they are: it reads the ids, the statuses and the next free id
from the notes, and tells you how many it found.

## If your code lives in another folder

A project whose notes and code are in different folders needs one more small file: see
[Notes in one folder, code in others](notes-and-code.md).
