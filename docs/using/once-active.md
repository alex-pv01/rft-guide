# What changes once it is active

- **At session start** Claude receives short operating rules and a compact copy of the tree
  (grouped by concept once there are concepts), so it knows to create an experiment's node
  *before* launching it, record only real results, add a direction for every new idea, and
  propose a concept when a new line of research opens (and ask whether code for it exists). A
  session started inside a concept's repo is told which concept that code belongs to. The rules
  for priorities, dates, locked notes and comments are given in full only in a vault that uses
  them. The manual is the `rft-manual` skill, in parts: a short core (what the notes are, when
  to create and update them) with an index, and one file per subject beside it (concepts and
  code, literature, the map, artifacts, notebooks, planning, the queue, writing, slides,
  comments). The
  rules and the commands name a part by its file, so Claude reads the one the work needs and
  never the whole manual.
- **Tools** Claude calls to keep the tree consistent. Only the ones a session uses most
  (`rft_add_node`, `rft_set_status`, `rft_set_summary`, `rft_search`, `rft_map`, `rft_graph`,
  `rft_next`, `rft_move_node`, `rft_sync`) have their full definition in the prompt from the
  start. The others are listed by name and loaded when Claude needs one, which keeps every turn
  cheaper. The comment, artifact, notebook, queue, manuscript and handoff tools join the first group in a
  vault that uses those features (it has comment threads or locked notes, a concept artifact, an
  experiment with a notebook, this machine paired with the experiment queue, snippets and
  documents, or a handoff a session left). The date and priority tools stay in the second group even then: their rules name
  them, and a session calls them too seldom to carry their definitions in every request. The
  queue's three tools are not there at all until a machine is paired (see The experiment queue):
  only `rft_machine`, which pairs it. `tests/size.test.ts` holds a ceiling on the size of the
  rules and of the definitions in the prompt.

    | tool | does |
    |---|---|
    | `rft_add_node` | creates a note with the next free id, a sanitised title (no `^ # | [ ]`), the template sections, and links it under its parent, with no priority (Claude may suggest one); it answers with the notes already in the tree close to the new one ("have we tried this?"); `notes` adds several in one call (a later one names an earlier one as parent or reference by its place, `#1` the first; a field given beside the list holds for every note; one refused note and nothing is written); the answer ends with the check `rft_validate` runs, the derived files already synced |
    | `rft_set_status` | changes a status (frontmatter, tag, Status line), optionally appending results or the reason |
    | `rft_move_node` | moves a note and its subtree under another parent, after you agree; the note keeps its past parents (`origin:`) and a dated `## History` line |
    | `rft_set_refs` | replaces the reference notes a note builds on (`refs:`); `rft_add_node` takes `refs` too |
    | `rft_search` | searches every note (titles and one-line summaries weigh most, then tags and concepts, then the text) and answers the best matches with their summary, where they sit and, when it adds something, the line that matched; concepts whose digest matches come first; filters by type, status, concept and tag. Built from the notes at each call, so never out of date, and nothing is stored |
    | `rft_graph` | a note's place in the tree, one line per note with its summary: its parent, children, the notes beside it, what it builds on, what cites it, where it was before a move; or the path the reasoning took from the top to it |
    | `rft_map` | the project map: each concept with its state (from its digest) and the experiments in progress; or one concept, with its digest and its notes one per line with their summaries. Claude reads it before opening note files |
    | `rft_set_summary` | sets the one-line `summary:` of one or more notes (Claude writes one for every note, and updates it when a result arrives) |
    | `rft_set_digest` | writes a concept's digest in the vault's `map/` folder: state, key results, dead ends, open questions; the map says when it is out of date |
    | `rft_artifact` | what a concept's artifact is written from, in at most 12,000 characters: the page whole while it is a third of that or less, else its outline (its headings with their sizes), each result that is new or changed since the page was written in full (every one before there is a page) and the others by id, the experiments without one, its sub-concepts, and how to write the page; `notes` gives the named results in full, `section` one part of the page as it is written (for an edit's `old_str`); results that do not fit are named, to ask for with `notes`. Every other tool answers in at most 8,000 characters (`hooks/lib/fit.ts`): a long list has its lines cut short, then its end, and a cut answer says what was left out and how to ask for it |
    | `rft_set_artifact` | writes a concept's artifact in `vault/artifacts/`, whole (`html`) or with `edits` (old → new, all or none), stamped with the results it was written from; names the results left off the page, links to no note, superseded results cited alone, and files the view would block |
    | `rft_manuscript` | snippets and documents: each snippet with its state (stub, written, review), the notes it rests on and the documents and files using it; each document's copies with theirs (to review, adapted, lost); the verified notes still to write. One snippet with the numbers, figures and tables its notes saved, as the macros that give them; one document's outline, its values the tree changed and the traces of the tree in its files |
    | `rft_set_snippet` | a new snippet, a building block resting on verified notes: a stub (its outline, for you to write) while snippets are locked; once you unlock one, its text or edits. Its macros are checked against what the notebooks saved, and it is stamped with its notes |
    | `rft_set_document` | a placement you agreed to: a copy of a snippet written out as plain LaTeX in a file of a document (after a copy or a heading), moved, or removed |
    | `rft_supersede` | marks a note whose result a newer one overturns (`superseded_by:` and a History line); the map, search, graph and tree view show it as superseded, so the old number is not built on |
    | `rft_next` | what is still open: the deadlines first (nearest first, with what puts them at risk), the GPU clashes and the meetings of the next 7 days, your priorities, then by concept the experiments running, planned and never run, directions with nothing tried under them (with their age, the higher priorities first), the digests' open questions, and the priorities Claude suggested that wait for you |
    | `rft_suggest_priority` | suggests a priority for a note, with a one-line reason (`suggested_priority:`); you accept or dismiss it in the tree view. Claude never sets a priority itself (see Priorities) |
    | `rft_suggest_dates` | suggests an experiment's start and/or estimate, with a one-line reason (`suggested_start:`, `suggested_est:`); you accept or dismiss it. Claude never sets a date itself (see Deadlines, meetings and the calendar) |
    | `rft_add_deadline` | adds a deadline you gave Claude in the chat (a milestone, with the notes it needs), once you confirm it in a dialog |
    | `rft_add_meeting` | adds a meeting you gave Claude in the chat, once or recurring (with the notes it needs by its next occurrence), once you confirm it in a dialog |
    | `rft_suggest_deadline` | suggests a paper submission deadline, read from the venue's official dates page (`source:`); you accept or dismiss it in the Calendar |
    | `rft_collect_papers` | downloads, in the background, the open-access PDFs of reference notes (arXiv, OpenReview, PMLR, ACL Anthology, NeurIPS/CVF proceedings, ...) into `vault/papers/<concept>/<year> <first author> <title>.pdf`, linked from each note (`pdf:`; in a literature note, a `PDF:` line under each paper); saved PDFs follow their concept. Never from paywalled publishers |
    | `rft_set_tags` | replaces a note's topical tags (lowercase kebab-case), keeping the project, type and status tags |
    | `rft_set_type` | changes the type of a note made with the wrong one: the next free id of the new type, the file moved to that type's folder, the type's sections (no text lost), every link to it renamed |
    | `rft_tags` | lists the topical tags in use with counts; the session's rules already name the most used, so Claude reuses them without a call |
    | `rft_set_concept` | sets, renames or removes (name null) the concept a note starts, once you confirm it |
    | `rft_concepts` | prints the concept tree: names, start notes, counts, statuses and linked code |
    | `rft_set_repos` | links code repositories to a concept (or, on the root note, to the whole project), once you give the path |
    | `rft_code` | a note's code context: its repos by priority, the commit it was last checked against, and the commits and files changed since |
    | `rft_set_code` | writes or updates a note's `## Code` section (how it relates to the code, how to reproduce its results), recording each repo's current commit |
    | `rft_set_notebook` | gives an experiment its marimo notebook, when you want one (best while it is planned): written from plain cells in its concept's repo (`notebooks/<id>_<title>.py`, a first cell reading `RUNS`, its runs in the queue) or one already there, linked from `vault/notebooks/<id>.py` and the note (`notebook:`) |
    | `rft_run_notebook` | runs the notebook now in its repo's uv environment: its `RESULTS` written in the note's Result as a table, or checked against it (ok, differs, failed), in a few lines; its figures and tables saved for the artifacts; stamps the note (`reproduced:`) |
    | `rft_tree` | prints the tree or a subtree |
    | `rft_validate` | checks ids, types, statuses, titles, parents, broken wikilinks, derived fields |
    | `rft_sync` | regenerates children / up / down, the index tree and the canvas after hand edits, and answers with the tree's check, so no `rft_validate` follows it |
    | `rft_handoff` | leaves a handoff for the next session in this folder (what was done, what to do first, what neither a note nor a commit holds; 2,000 characters in all), to which the plugin adds the repositories with uncommitted changes; with no field it shows the handoff (see Handoffs) |
    | `rft_comments` | a note's comments and suggestions, or the notes with open threads |
    | `rft_comment` | replies in a thread (or closes a suggestion it made in the note), or starts a comment on a quote |
    | `rft_suggest` | proposes new text for a quote, or the text an open suggestion asks for; you accept or reject it |
    | `rft_machine` | pairs this machine with the experiment queue, which turns the queue on: `probe` reads the machine with no model (its NVIDIA GPUs, the disks for the runs' outputs, conda and uv), `add` pairs it with the outputs' root and the GPUs you keep out, `status` says how it stands (see The experiment queue) |
    | `rft_queue` | queues a run of an experiment on this machine's GPUs (command, folder, GPUs, a label); it starts once its GPUs are free, in your order (see The experiment queue). Only on a paired machine |
    | `rft_jobs` | the queue in a few lines: the GPUs, the jobs running and waiting (with why each waits), the last ones that ended, the results still to record; one job with its run record (the code it ran, its outputs, the end of its traceback) and the end of its output |
    | `rft_inbox` | the inbox, links saved to read later: lists the items, saves one (a link already in the inbox, processed or a reference's Source is reported, not added), saves its impression and its brief of an item you asked to process, gives an item's reading note (your part only once you marked the item as read), and closes it with the outcome you picked (the note it became, or why it was discarded; your quotes word for word in the note); it never sets a reading priority or the read mark |
    | `rft_job` | changes the queue when you ask: moves one waiting job to the top, the end, or before another (answering the new order in one line), cancels one, retries one that ended, pauses or resumes the queue |

- **The outline pane** opens as a sidebar at session start in the terminal and VS Code where the
  surface docks panes (turn this off with the `autoOpen` option), and with `/rft list`: an indented, coloured outline of the tree, the same on
  the desktop app, VS Code and the terminal. Click a node to read its note, ▾ / ▸ to fold a
  branch. It refreshes by itself when notes change, whoever changed them, and shows the tree
  view's address while its server runs.
