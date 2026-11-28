# The tree view

`/rft` also starts a small local server for the interactive tree view.

- **On the desktop app** it tries to open the view in the app's built-in browser pane, reusing
  the tab already on it. When the plugin cannot reach the browser pane (the usual case today),
  it prints the address and opens the outline pane: click the address and choose to open it in
  the app.
- **In the terminal and elsewhere** it prints the address, e.g. `http://127.0.0.1:41234/?token=…`, and
  opens the outline pane. Open the address in any browser on the same machine.

- A tidy tree, **top-down**, **left-right** or **radial** (never a force layout), arrows from
  parent to child. Each note is a solid shape: a circle, or a **star** for the note that starts a
  concept, with a small star inside in that concept's colour. Its colour is its type (direction violet, experiment teal, reference pink, theory
  blue), and how strong that colour is says its status: full when done, then running, planned,
  and palest as an idea. Dropped notes fade (shape, title and the link into them), discussed and
  moved ones half as much, so what is still open stands out; hovering or reading one shows it in
  full. An open note's priority glows around it in the priority's colour (as on the kanban: urgent
  red, high orange, medium blue, low grey), brighter the higher, and an urgent one pulses.
  The layout button shows the current layout as a symbol and switches to the next one.
- An infinite canvas: drag to pan, scroll or pinch to zoom. One button fits the whole tree,
  then centres on the root; panning or zooming by hand makes it fit again.
  Labels show more of the title the closer you zoom.
- The title is the project's name, or the root note's concept when it declares one.
- Click a node to read its note in a side drawer; links in the note jump to their node. The
  arrow keys walk the tree from the note shown: ↑ to its parent, ↓ to a child (the one shown
  last, else the first; a folded note unfolds), ← → round its siblings (past the last, the first
  again). Once you click in the drawer they scroll the note instead, until you click the tree
  again. LaTeX
  renders as in Obsidian: `$…$` inline, `$$…$$` displayed (on one line or several); a `$` in
  code, `\$`, and amounts like "$5 and $10" stay text.
- Images show as in Obsidian: `![[name.png]]` and `![alt](path/to/fig.png)`, with a width as
  `![[name.png|400]]` or `![alt|400](…)` (or `400x300`). A path is read from the note's folder or
  the vault's top, or is a path on disk (`/home/…/results/fig.png`); a bare name is the image of
  that name nearest the note, in the vault, else in the Obsidian vault around it (the folder
  holding `.obsidian/`), so `![[Pasted image ….png]]` finds Obsidian's attachments. An image
  outside the vault needs the key (see below); a missing one says so in its place. Click an image
  to open it at full size. A remote image (`https://…`) shows as a link: the page loads nothing
  from elsewhere. `rft_validate` leaves embedded images alone. `/rft-view` shows each image as
  a placeholder.
- **Edit** (the pencil in the drawer) changes the note's text: the markdown below the
  frontmatter (status, parent and tags stay with Claude's tools). **Save** or Ctrl/Cmd+S writes the file, **Cancel**
  or Esc drops the changes. A note that changed meanwhile (Claude, another editor) is never
  overwritten silently: you choose **Overwrite** or **Reload**. Leaving a note with unsaved
  changes asks first.
  Fold a branch with its **−** / **+** badge or a double-click; one button expands every
  branch while one is folded, and collapses them all otherwise.
- **Add child** (a node with a **+**, in the drawer) adds a direction or an experiment under
  the note shown: choose the type (the other one than the note's comes first), type a title,
  **Add** or Enter. The note is
  made as Claude's `rft_add_node` makes it (the next free id, the title cleaned, the template,
  the default status, linked under its parent, the index and canvas regenerated), by the plugin
  in the session that ran `/rft`, so it costs no model turn and no tokens; it then opens in
  **Edit**.
- **Change type** (a ring in a turning arrow, in the drawer) changes the type of a note made
  with the wrong one: choose the type, **Change**. The note gets the next free id of that type and moves to its folder; its text
  stays, the type's missing sections are added, and every link to it is renamed. Like
  **Add child**, the session that ran `/rft` does it with `rft_set_type`'s code, at no model turn.
  The root stays a direction.
- **Footnotes** show as in a book's margin: a mark `[^1]` in the text, its text on a line
  `[^1]: …` (indented lines continue it), or inline `^[…]`, as Obsidian writes them. Each mark is
  numbered in reading order and has a number in the drawer's right margin; hover either (or tap
  it) to read the footnote, links and LaTeX included. Select text and choose **Footnote** to add
  one: its mark goes after the selection, its text at the end of the note.
- **The highlighter** (the marker left of **Add child**) is a mode of the drawer, like a pen:
  while it is on, the text you select is highlighted at once, `==like this==` in the note, as
  Obsidian writes it, so Obsidian shows it too; selecting inside or across a highlight, or
  clicking one, takes it out. A selection over several lines gets one highlight per line, and one
  that cuts into bold, italics or a link grows to hold it whole; code and formula blocks take
  none. **Esc** or the marker turns it off; **Comment**, **Suggest** and **Footnote** wait until
  then.
- **The margin column**: when the drawer leaves the text room beside it (drag its left edge to
  widen it), the margin shows each footnote's text level with its mark, and a card for each open
  comment or suggestion level with its text: its kind, a suggestion's new text, and the last
  message, cut short. Hover a card to light up its text; click it to open the thread below. Each
  card also has a box for a short reply (**Enter** posts it) and the thread's buttons as icons:
  reply, ask Claude (with the reply, if one is written), then accept and reject for a suggestion,
  or resolve for a comment. What is typed there shows in the thread's box below too. On a
  narrower drawer the margin keeps only the footnotes' numbers.
- **Comments and suggestions**, as in Overleaf, discuss a part of a note before anyone edits it.
  Select text in the drawer and choose:
    - **Comment**: a question or remark on that text;
    - **Suggest**: new text for it (the markdown as written, to change), or, with the text left
      as it is, what should change in words, for Claude to write.

    Open threads are marked in the text (a suggestion as the old text struck through and the new
    text after it) and listed under the note, where icons let you **Reply** (↩), **Ask Claude** (✦),
    **Resolve** a comment (a ticked circle), **Accept** a suggestion (✓, its new text is written into
    the note) or **Reject** it (✕); hover one for its name. Closed threads stay in
    the note's **History**, and **Reopen** brings one back.

    - **Ask Claude** (on a thread, or **Post and ask Claude** / **Post and suggest** when posting) sends the thread to a background
      Claude (a subagent of the session that ran `/rft`), so the main chat does not grow with each
      answer. Claude answers only when asked, and in the thread: a comment gets a reply, a
      suggestion gets its new text as a replacement for you to accept or reject. The subagent only
      reads; the note changes only when you accept. When no subagent can start, the thread goes to
      the session as a turn of its own. With [agents of your own](agents.md) set up, a picker
      (**Answers by**), in the box you write in and above the threads, says who answers, the
      buttons name it (**Ask qwen**, **Post and ask qwen**), and the answer is signed with its
      name.
    - A thread keeps its quote and the text around it, so it is found again after the note is
      edited. When the quoted text itself changed, the thread says what it now reads, and its
      suggestion can no longer be accepted. When the text is gone, the thread says so.
    - The threads live beside the notes, one file per note: `vault/.comments/<id>.json`, a dot
      folder Obsidian leaves alone. They follow a note whose type (and id) changes.
- **Lock** (the padlock in the drawer) makes a note yours: `locked: true` in its frontmatter.
  Claude then changes nothing in its text, only suggests changes, which you accept. The plugin
  refuses Claude's Edit and Write on a locked note, shell commands that write to it (a redirection,
  `tee`, `sed -i`, `perl -i`, `mv`, `cp`, `rm`, ...; a script run by an interpreter, when it names
  the note), and `rft_set_status` notes and `rft_set_code` on it.
  Status, tags and the tree's derived fields still change. Your own edits in the drawer are not
  affected, and neither are Obsidian's. Moving a locked note, or marking it superseded, writes a
  line in its **History**, so it unlocks the note, and only once you agree: the session asks you
  (Claude cannot answer for you), and the tree view's **Move** says so first (its button becomes
  **Move and unlock**). If you keep it locked, nothing changes. Its locked parents and the notes
  below it ask nothing and stay locked: they only get the tree's derived changes.
- The drawer lists the references a note **builds on**, and on a reference the notes that
  **cite** it, each a link to its node; a reference whose paper was saved links its PDF.
- **Move** (an arrow out of a node, in the drawer) moves the note shown, and every note below it, under another note:
  pick it from the list (or type its id), **Move** or Enter. As with **Add child**, the plugin
  makes the move with `rft_move_node`'s code. A moved note shows where it came from at the top
  of the drawer, and **Came from** draws a faint dashed link from its previous parent.
- **A concept's artifact** opens in the drawer when you click the concept: its name on a region
  or badge, its node in the concept view, or the concept path at the top of a note (see Concept
  artifacts).
- **Tree**, **Concepts**, **Kanban** and **Calendar** at the top switch between the reasoning tree,
  the concept tree, the kanban and the calendar (below).
- Hover a node to highlight its path to the root; **search** (Enter jumps to the next match).
- **Filters** opens a side panel: topical tags (with counts, matching **any** or **all**), type,
  status (the same filter as clicking the legend), and a date range. Notes that do not match
  are dimmed, keeping the tree's shape, or hidden, keeping every ancestor of a match so the tree
  stays connected. The toolbar shows how many filters are on, with **Clear**.
- **A−** / **A+** set the size of the labels and the note text.
- The sun / moon button switches between light and dark. Until it is used the view follows the
  system's theme; then it keeps the choice, for every project.
- **The scratchpad** (the note icon at the bottom left, the legend's faint **?** beside it) holds
  quick notes and to-dos, saved as you type to `Scratchpad.md` at the vault's top: plain markdown that Obsidian shows too, and
  not a note of the tree. A to-do is a list item with a box, `- [ ] …`: **Ctrl/Cmd+Enter** makes
  the line a to-do or ticks it, **Enter** continues a list (on an empty item it ends it), **+ To-do**
  adds one, and the icon shows how many are open. A change made meanwhile in Obsidian or by Claude
  comes in; one that crosses your typing asks you to **Keep mine** or **Take theirs**. **Esc**
  closes it. It is on every page; `/rft-view` leaves it out.
- **The inbox** (the tray icon beside the scratchpad's) has a page of its own:
  [The inbox and reading notes](inbox.md).
- It follows the vault live, and keeps the zoom, layout, folds, filters and text size between
  visits.
