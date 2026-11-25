# Concepts and artifacts

## Concepts

A **concept** is a line of research: the note that starts it (usually the direction that opened
the line) and its whole subtree, until a descendant starts a sub-concept. Concepts nest; notes
with no concept above them belong to the project itself. A concept on the root note covers the
whole tree, so it takes the project's place at the top of the concept tree. Concepts live in
the starting note's frontmatter:

```yaml
concept: "Strong augmentation"
concept_summary: "Whether heavy augmentation alone closes the small-data gap"
```

Concepts are explicit. Claude proposes one when a direction opens a new line of research, and
applies it with `rft_set_concept` only after you say yes. `/rft-concepts suggest` asks Claude for
a full split of the existing tree, as a table to confirm or change; `/rft-concepts` prints the
concept tree.

In the tree view, the concept button switches the overlay from off to **Regions** to
**Arrows** and back; its symbol shows the current one:

- **Regions**: a soft region behind each concept, bordered in its colour, its name on top;
  sub-concepts are nested, lighter regions. They follow the layout (top-down, left-right,
  radial), folded branches and hidden filters.
- **Arrows**: links coloured by the concept of the note they lead to, and a name badge at each
  concept's start.
- Concept colours are a palette of their own, apart from the status colours; a concept legend
  shows while the overlay is on. It lists the top-level concepts, each with an arrow that
  unfolds its sub-concepts. The legend opens and closes from the faint **?** beside the
  scratchpad's icon.
- **Concepts** (at the top) shows a tree of the concepts: each sized by its notes, with a bar of their
  statuses, in the same layout as the reasoning tree (top-down, left-right or radial). Click one to
  open its artifact beside the tree; the artifact's **Show in tree** goes to its start note on the
  reasoning tree, its region briefly highlighted; **focus** shows only that concept's subtree.
- **Focus** is also reachable from the legend and an artifact's **Focus** button; a breadcrumb
  (project › concept › sub-concept, or from the root note's concept when it has one) leads back up.
- Concepts are also a filter in **Filters**.

A link can open the view in a given state, e.g. `?layout=lr&concepts=regions`,
`?view=concepts`, `?view=kanban&order=date`, `?view=calendar&cal=month`, or `?focus=D02&note=E05`.

## Concept artifacts

Each concept can have an **artifact**: one HTML page of the results of its own experiments, like
an artifact in Claude's chat, kept in `vault/artifacts/<id> <name>.html` and in step with the tree.
Claude writes it; you read it in the tree view.

- **Open it** by clicking the concept: its name on a region or badge in the tree, its node in the
  concept view, or the concept path at the top of a note. It opens in the note drawer (wider than
  a note; drag its edge, it keeps its own width), under its concept path, whether it is up to
  date, and links to its sub-concepts' artifacts. **Show in tree** goes to the concept's start
  note, **Focus** shows only its subtree. `?artifact=D04` in the address opens it at once.
- **Note links** in it (`E05`) open the note in the drawer; the note's concept path brings the
  artifact back, where you left it. Each link shows its note's status as a dot, and a superseded
  result struck through, from the tree as it is now.
- **In step with the tree**: the page is stamped with what each experiment with a result was when
  it was written (status, title, summary, superseding note, Result). An experiment that finishes,
  a Result edited by hand, a new result, or one that moved away puts it **out of date**: the drawer
  says which ("Out of date: E06 new"), and so do `rft_set_status`, `rft_map`, `rft_next` and
  `rft_validate`. It follows live, and redraws when Claude updates it.
- **Claude keeps it**: with `rft_artifact <concept>` (the results, and what changed since) then
  `rft_set_artifact` (the whole page, or edits). In a vault that has artifacts, Claude updates the
  artifact of each concept a task gave results to at the end of that task, and writes one for a
  concept with results that has none. `/rft-artifact [concept]` asks for one, or for every one
  missing or out of date. Only numbers that are in the notes go on it. Claude's own edits of the
  files are refused, so the stamp stays true.
- **A notebook's figures and tables** go on the page by name: `<img src="../figures/E08_loss.svg">`
  and `<rft-table src="E08_accuracy_by_seed"></rft-table>`, which the plugin fills with the table
  when the page is written and again whenever the notebook's run writes it anew. `rft_artifact`
  names what each experiment's notebook saved, so Claude places them instead of writing them out.
- **Figures** are kept in `vault/figures/` and named from the page as `../figures/<file>.svg`
  (which also works when the file is opened on its own); an image is looked for there first, then
  as a note's images are. An SVG comes inside the page (a browser refuses one sent to the
  sandboxed frame), up to 10 MB; `rft_set_artifact` names an image it cannot find.
- **PDF and LaTeX**: each SVG figure, a file or a chart drawn in the page, has a **PDF** button at
  its corner that downloads it as a vector PDF of its own size, named after its file (or its
  caption); each table has a **LaTeX** button that copies it as a `table` float: `\caption` from
  its `<caption>` (else the heading above it), a `\label`, a booktabs `tabular` with its header rows
  above `\midrule`, columns of numbers right-aligned, `±` and the like in math, bold and italics
  kept. The PDF is made in the page by jsPDF and svg2pdf.js (MIT, in `web/vendor/`, loaded the
  first time one is asked for); the standalone page has the LaTeX button only.
- **Safe to show**: the page runs in a sandbox of its own (its own origin, no storage, no network,
  no way to the page around it or to a write); it loads nothing from elsewhere, so a chart is
  inline SVG or the page's own script. Its images are found as a note's are; one outside the vault
  comes with a key that reads images and writes nothing.
- A vault with no artifact sees none of this: no rule, and the two tools wait behind ToolSearch.
  `/rft-view` embeds the artifacts read-only, their images as placeholders.

Every note carries 1–3 **topical tags** besides the project, type and status ones (the session's
rules list the ones in use, so that Claude reuses them); the tree's `api/tree` JSON lists them with
their counts.

The server listens on `127.0.0.1` only, on a free port (or `webPort` in the config). It serves
the page, the tree as JSON and the text of one note at a time, read by its id from inside the
vault, each concept's artifact read-only (as a page of its own, in a sandbox: its own origin,
nothing from elsewhere), and the image files notes and artifacts embed: one inside the vault to anyone who can read the notes,
one outside it (anywhere on disk) only to the page carrying the key below, so another user of
the machine cannot read your files through it, nor learn whether one exists. An image is sent
with a policy that runs nothing in it, an SVG's scripts included. A reference's saved PDF is
served only from the vault's `papers/` folder. It answers only requests for
a loopback host name. It writes a note's text from **Edit**, **Footnote**, **Highlight** or an
accepted suggestion, its frontmatter kept as it is; the `locked:` line from the padlock; the
`priority:` line from the kanban or the drawer (which also clears Claude's suggested priority), within
the limits; a note's `due:`, `start:` and `est:` from the Calendar or the drawer (which also clear
Claude's suggested dates); a deadline in `vault/milestones/` (a new one, its due date, needs and
status, Claude's suggested one accepted or dismissed); a meeting in `vault/meetings/` (a new one,
its times and repeat, an occurrence skipped or moved, its needs, or the meeting deleted); a note's comments file in `vault/.comments/`;
and the experiment queue in `vault/.queue/` (a job moved, cancelled or retried, the queue paused,
the GPUs it may use; a job's output is read only with the key). A new note from **Add child**, a note's new type from
**Change type**, or a move from **Move**, it asks the session that started it to make, and **Ask
Claude** to answer (a line on its output, which the plugin reads). It does any of these only for
the page itself carrying the project's key, which the address `/rft` prints holds (`?token=…`):
neither another web page nor another user of the machine can change or add a note. Open that address once and the browser
remembers the key, which stays the same across restarts (kept, readable by you alone, in
`~/.cache/rft/keys/`), so the plain address or a bookmark can edit too. It stops with
the session or `/rft stop`; `/rft` again reuses it. Sessions on the same tree with the same
`webPort` share one address, key included: a second session's `/rft` prints it, and its server
takes the port over when the first session ends; a port held by anything else gets a free one
instead. On a **remote machine** (SSH, a cluster
node), forward the port and open the address on your own machine:

```bash
ssh -L 41234:127.0.0.1:41234 user@remote
```

**From a terminal**, the view stays up with no chat open: in the project's folder (or any folder
below it, or a repository whose config links to the tree), run

```bash
python3 /path/to/rft-plugin/server/rft_serve.py        # [folder] [--port N]; Ctrl+C stops it
```

It prints the address `/rft` prints, key included, on the config's `webPort` (set one so the
address, and a bookmark of it, stay the same; with none it takes a free port). Reading, editing,
comments, the kanban, the calendar, the scratchpad, the inbox and the queue work as from a chat. What the
page asks of the session (**Add child**, **Change type**, **Move**, **Verify**, the Manuscript's
changes, **Ask Claude**, the inbox's **Process** and **Discuss**) a chat makes: `/rft` in a chat on the same tree shows the terminal's
address and makes them from there, and the terminal says when a chat connects or leaves. With no
chat, they are refused at once, saying so, except a thread and **Process**, which go to an
agent of your own when you have set one up ([Agents](agents.md)). A chat already serving the tree on that port keeps it,
and the terminal serves it once the chat ends; a terminal that stops while a chat is open leaves
the address to that chat. A second terminal on the same tree says where the first serves it.

On a **phone** (a screen up to 700 px wide; `web/phone.js`), the pages are tabs along the bottom,
the bar is the search and **⋯** (layout, fit, fold, text size, the concept overlay, Came from,
Filters, the theme), and a note, the filters, the scratchpad, the inbox, the queue and a notebook each take
the whole page, the note's actions a row of named chips above it. The phone's **Back** closes
what was opened last, and in a note reached by a link shows the note it was in. The kanban
shows a column at a time, swiped; the Manuscript and the Slides a pane at a time (the list, the
text, the PDF or slide), the Manuscript's buttons their symbols alone (a symbol and a word on a
wider screen). On any touch screen, controls are 44 px targets, fields' text 16 px, and
a selection made with a long press gets its Comment, Suggest and Footnote bar at the bottom. A
browser that shows no PDF in a frame (Chrome on Android), and any touch screen, gets the
Manuscript's PDF drawn by pdf.js, page by page as they come near the screen.
`tests/test_phone.py` checks every page at 360 and 412 px in headless Chromium.

d3 (ISC licence, `web/vendor/LICENSE-d3.txt`), KaTeX (MIT licence,
`web/vendor/LICENSE-katex.txt`; its fonts inlined in its stylesheet), jsPDF and svg2pdf.js
(MIT licences, `web/vendor/LICENSE-jspdf.txt`, `web/vendor/LICENSE-svg2pdf.txt`; an artifact's
figures as PDF), CodeMirror 5 (MIT licence, `web/vendor/LICENSE-codemirror.txt`; the
manuscript's editor, with its LaTeX mode) and pdf.js 4.10.38 (Apache 2.0 licence,
`web/vendor/LICENSE-pdfjs.txt`; the manuscript's PDF where the browser draws none, loaded the first
time) are bundled, so the page needs no network.
