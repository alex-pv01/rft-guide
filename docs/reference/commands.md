# Commands

| command | does |
|---|---|
| `/rft` | start (or reuse) the tree view server and show it: in the desktop's browser pane, else print its address and open the outline pane |
| `/rft list` | open the outline pane |
| `/rft stop` | stop the tree view server |
| `/rft text` | print the tree in the transcript |
| `/rft-init [starting question]` | activate RFT here and create (or adopt) the vault |
| `/rft-concepts` | print the concept tree |
| `/rft-concepts suggest` | ask Claude to propose a concept split; nothing changes until you confirm |
| `/rft-literature <topic, id or concept>` | ask Claude for a literature search: one literature note with every key paper read, under the note or concept it is about, then a synthesis, the directions it suggests and the papers worth a note of their own (added only once you choose) |
| `/rft-rebalance [concept or id] [--full]` | ask Claude to propose moving branches under the line of research they belong to, as a table of moves; only the ones you confirm are made, each keeping its origin. The plugin first finds the candidates (notes whose words and references sit closer to another concept than to their own) and Claude judges only those; `--full` has Claude review the whole tree instead |
| `/rft-next [concept]` | print what is still open, by concept: running and planned experiments, unexplored directions, open questions (no model turn) |
| `/rft-machine [add|status]` | pair this machine with the experiment queue: `add` checks it at no model turn (its NVIDIA GPUs, the disks with the most room, conda and uv), then Claude asks where the runs' outputs go and which GPUs to keep for your own work, and turns the queue on; on a machine with no NVIDIA GPU the queue stays off, and on one already paired it only says so, with its status. `status` (the default) says how it stands. Only this machine for now |
| `/rft-jobs [job or experiment]` | print the experiment queue: the GPUs, the jobs running and waiting, the last ones that ended (a job: with the end of its output), and the address of the monitor (no model turn) |
| `/rft-summarize [concept]` | ask Claude to write the missing note summaries and concept digests of an existing tree, concept by concept (a one-off job) |
| `/rft-manuscript [document] | new <name> [article|report]` | start snippets and documents (a first document, `paper`), add a document (`report`: a thesis chapter), or ask Claude what to write next from the verified notes and where to place it, as tables; nothing is written until you pick |
| `/rft-artifact [concept]` | ask Claude to write a concept's artifact, or, with no concept, every one missing or out of date |
| `/rft-update [apply] [--sections]` | bring a vault made by an older version up to this one: list what it lacks (the folders and templates of newer note types, the config's format); `apply` writes it and refreshes the derived files. Notes are never changed, except that `--sections` adds the sections their type has gained, as empty headings, to unlocked notes. A session on an older vault starts with a toast pointing here (no model turn) |
| `/rft-update notebooks [--write <concept or experiment ids>]` | bring the existing notebooks up to what the plugin does now: every notebook runs again in the queue (one job, no GPU, in check mode, no model turn; with no machine paired it says so and runs nothing), so each saves its numbers, figures and tables; and, for information, a list by concept with code of the experiments with a result and no notebook (not those with `notebook: no`), a missing concept notebook, an artifact's hand-drawn charts. `--write <concept>` asks Claude to write that concept's, `--write E05 E07` those experiments' only; a notebook is never written for what you did not name |
| `/rft-handoff [show|clear|a note for the next session]` | ask Claude to leave a handoff, so the work goes on in a new session (or after `/clear`) and not in a long one; `show` prints it and `clear` removes it (no model turn) |
| `/rft-inbox [link] [reading priority] [why]` | print the inbox, the most pressing first; with a link, save it to read later, with the reading priority and the why you give; a link you discarded comes back as the item it was (no model turn) |
| `/rft-view` | write `vault/tree.html`: the same tree view as one standalone file, every note inside (images as placeholders), to open anywhere or share |

The plugin registers these commands when a session starts, so the desktop app's slash-command
menu may not list them (it lists the plugin's skill, `/rft:rft-manual`): type `/rft` in full
and it runs. The terminal's typeahead lists them.
