# The inbox and reading notes

**The inbox** (the tray icon beside the scratchpad's, with the number of items) holds what you
saved to read later and have not decided about: papers, articles, blog posts. An item is a link
(a URL, an arXiv id or a DOI) with, if you give one, a line on why. It is not a note of the
tree: the items are list lines in `Inbox.md` at the vault's top, plain markdown you can edit in
Obsidian.

## Saving an item

Paste a link in the field at the panel's top, type `/rft-inbox <link> [reading priority] [why]`
in the chat, or ask Claude to save it; a link already in the inbox, processed before or in a
reference note's **Source** is said to be there and not added twice, and an arXiv paper gets its
title from arXiv a moment later. A link you discarded before comes back as the item it was (see
[Discarding an item](#discarding-an-item)).

A literature search saves every paper it lists, and those it found and did not read, here.
`/rft-inbox` alone prints the inbox, and `/rft-view` leaves it out.

## Reading priority

Each item has a **reading priority** (urgent, high, medium, low or none): yours alone, with no
limits, not a note's priority and never carried to one. It shows as an icon, three bars with as
many filled as it presses and a red **!** for urgent, and a tap on it steps to the next (none,
low, medium, high, urgent, none again), written a moment after the last tap. The list is ordered
by **Priority** or by **Date**; a tap on an item's why edits it, and **✕** (asked twice)
[discards it](#discarding-an-item).

## Reading notes

Each item can have a **reading note**, opened by the page sign on its row (the whole screen on a
phone, a wide pane at the desk): one plain markdown box for quotes from the item (lines after
`>`; **Paste as quote** puts what you copied in as one, or marks the lines you selected) and
lines of your own. It saves itself as the scratchpad does, into one file per item in `Reading
notes/` at the vault's top, made on your first words and never for a note you only opened. The
sign is lit once the note holds something of yours.

## Process: Claude reads the item

**Process** on an item asks Claude, in the chat that ran `/rft`, to read it on its own: Claude
saves its **impression** in the reading note (about one screen, always the same five parts: what
it claims, how, the key results with their numbers and where they are, its bearing on notes of
your tree, what it leaves open) and a **brief** of at most three lines on the item (what it
claims, which notes it touches, the outcome it recommends), says the brief and stops. Until you
mark the item as read, Claude cannot open your part of the reading note: its impression is a
second point of view, not an echo of yours, and a second Process rewrites it from the paper
alone. The view shows the impression folded under your text.

## Mark read, and the discussion

**mark read** on the row (asked twice) is yours alone to set and to take off. It freezes the
impression and starts the **discussion** in the chat: Claude opens your part for the first time,
says where its reading and yours differ, and waits. The row's button reads **Discuss** from then
on. You pick the **outcome**: a reference note, an entry in a literature note, a direction
citing its reference, discard, or later. Claude writes what that needs, with your quotes word
for word (the item is not closed while one is missing or changed) and your own lines rephrased
only as you accept in the chat, and closes the item, which moves under `## Processed` with its
date and what it became (`→ R15`); its reading note is removed, what it held being in the tree.
*Later* leaves the item in the inbox with its brief (shown at a tap on **briefed**), its reading
note and its read mark.

## Discarding an item

A discard, by **✕** on the row or picked as the outcome in the chat, takes the item out of the
inbox and loses nothing, so nothing more is asked, whatever its reading note holds. The item's
lines move, as you had them, under `## Discarded` in `Inbox.md`, with one line more that says
when and, from the chat, why:

```markdown
## Discarded

- [Mixup at scale](https://arxiv.org/abs/2406.01234) — maybe relevant to D04 · high · added 2026-11-16
  - discarded 2026-11-27: superseded by R07
```

Its reading note moves to `Reading notes/Discarded/`. A discarded item is not listed and not
counted, and Claude can read nothing of it.

Only you bring it back: paste its link in the panel's field again, type `/rft-inbox <link>`, or
ask Claude to. It returns at the end of the list as the item it was, with its why, reading
priority, read mark, brief and reading note. A later literature search that finds the paper again
leaves it discarded and says so. The discarded items are yours to clear: delete their lines and
files when you no longer want them.

## Without a chat

With no chat on the tree, Process is refused at once, saying so (unless an agent of your own
takes it: [Agents](agents.md)); a read mark is saved all the same, the row says *waiting for
chat connection*, and **Discuss** starts the discussion once a chat is there. Claude never
processes an item unasked.
