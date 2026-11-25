# The kanban and priorities

**Kanban** shows the notes in one column per status: idea → planned → running → done, then
dropped, discussed and moved as narrow folded strips (click one to open it, its head to fold it
again), and a column for any other status a note was given by hand. Each note is a card: its dot
(the type's colour at its status's strength, as in the tree), id and title, its summary, its priority, its concept and its date. Click a card to read the
note in the drawer; the board makes room for it.

- **Order by Priority** (the default: urgent, high, medium, low, then the notes with none; newest
  first within each) or **Date** (newest first, by the date the note was made).
- **The filters apply**: type, status (a hidden status hides its column), concepts, tags and the
  date range, and the concept focus. Notes that do not match are left off the board (the dim /
  hide choice is the tree's). The search lights up the matching cards, and Enter goes to the next.
- **Priority** is yours alone: `priority:` in the note's frontmatter, `urgent`, `high`, `medium` or
  `low`, set with the menu on a card or in the drawer (**No priority** takes it away). A new note
  has none. Among the open notes (idea, planned, running) at most **1 is urgent, 5 high and 10
  medium**; low has no limit, and a note that is done, dropped, discussed or moved does not count.
  A full priority is offered greyed out, naming the notes that hold it: lower one of them first.
  The bar above the board shows how the open notes use each priority.
- **Claude only suggests** a priority: `rft_suggest_priority`, or `rft_add_node` for a new note,
  writes `suggested_priority:` and a one-line `suggested_priority_why:`. The card and the drawer
  show it in a dashed box with its reason: **Accept** makes it the note's priority (greyed out
  while that priority is full), **Dismiss** drops it; setting another priority answers it too.
  Claude's own Edit, Write and shell writes that add, change or remove a note's `priority:` are
  refused, so it cannot set one, even by hand. `rft_next` lists your priorities first, and
  `rft_validate` warns about a priority that is none of the four and about a limit exceeded by
  hand.
- A menu you are in is not redrawn under you while notes change on disk; the board follows once
  you leave it. The standalone `/rft-view` page shows the kanban read-only.
