# Notebooks and figures

## Experiment notebooks

An experiment in a concept with code can have a **notebook** that makes the numbers of its Result: a
[marimo](https://marimo.io) notebook in its concept's code repository, which runs in that repo's
own [uv](https://docs.astral.sh/uv/) environment. It reads its runs' saved outputs after an
expensive training run, or reruns a short experiment from scratch. Its run records the result when
the jobs end, so no one copies a number by hand.

**A notebook is your choice, per experiment.** Exploratory runs (does it work, a quick check,
development) get none, and Claude does not ask. When an experiment's results are meant to last
(figures or tables for a paper, a thesis or the docs, a result to verify or to cite in a snippet),
Claude asks you once whether to give it a notebook for reproducibility. If you decline, it writes
`notebook: no` in the note and does not ask again. Claude never writes one unasked, and nothing
(`rft_next`, `rft_validate`, `rft_add_node`) reminds you of experiments without one. It opens on the **left** of the tree view while the note is open on the right,
so you can run it and read the note side by side.

- **Where it is**: `<repo>/notebooks/E02_<title>.py`, in the first repo the concept links (see Code
  repos), versioned with the code it imports. The vault links it as `vault/notebooks/E02.py` (a
  relative symbolic link) and the note says so in `notebook:`. It is plain Python, so it diffs
  and reviews like code.
- **Claude writes it** with `rft_set_notebook`, as plain cells (the tool writes marimo's format),
  or links one already in the repo; later changes are ordinary edits of the `.py` file. A new one
  starts with a cell giving `RUNS`: the experiment's runs in the queue that ended well, each its
  run record, with `out`, its output folder. The notebook sets:
    - `RESULTS`, a dict of the numbers the note reports, rounded as it reports them;
    - `FIGURES`, `{name: matplotlib figure or SVG text}`: saved as `vault/figures/<id>_<name>.svg`;
    - `TABLES`, `{name: DataFrame, list of row dicts, or dict of columns}`: saved as
      `vault/tables/<id>_<name>.html`, its name as caption.
- **Its run** (by the queue's runner after the experiment's last job, or by Claude with
  `rft_run_notebook`) is taken to the vault by `server/rft_results.py`, without the browser:
    - **Recorded**: `RESULTS` written in the note's Result as a table, between two comment lines
      (`<!-- rft-results … -->`, hidden in the tree view and Obsidian), with the line it comes from:
      the notebook, its commit, and the runs it read with theirs. The runner's run always records
      (new runs, new numbers); `rft_run_notebook` records when the Result has no table and no
      number yet, or with `record: true`. A locked note is left as it is. Only a run writes that
      table: Claude's own edits of it are refused, so Claude writes what the numbers mean around it.
    - **Checked** otherwise: **ok** when every number of `RESULTS` is in the Result (at the
      precision the Result gives), **differs** with the numbers that are not, **failed** with the
      end of the traceback. The answer is a few lines, never the cells' outputs.
    - **Saved**, when recorded or ok (so the vault shows what the note says): `RESULTS` as
      `vault/results/<id>.json` (with its commit and runs), the figures and the tables; the tables
      are filled into the artifacts that name them.
    - **Stamped**: `reproduced: "2026-11-15 ok @3f2a1c9d0e in 6.1 s"` (the repo's commit, `+dirty`
      with uncommitted changes). Only a run writes that line: Claude's own edits of it are refused,
      so it says what a run really did.
      A run is `uv run --project <repo> --with marimo` (so the repo need not list marimo), with the
      repo's root as working folder and the notebook's folder first on `sys.path`, as the editor
      runs it. It stops after 9 minutes; longer is a launch, not a check.
- **In the tree view**: opening an experiment with a notebook opens it on the left, in marimo's
  editor, with its last run above it. Nothing runs until you press run. The server starts one
  editor per repo the first time one of its notebooks is opened (that can take a minute the
  first time uv builds the environment), on `127.0.0.1` with a key of its own, and stops it with
  itself, or once nobody has had it open for 4 hours (opening the pane again starts a new one).
  The page reaches the editor through the tree view's own port (under `/notebook/…`), so the one
  `ssh -L` forward above is enough on a remote machine. Opening one runs code, so it needs the page's key, as an edit does. ✕ closes the pane
  and the note's notebook button opens it again; drag its right edge to resize it; ↗ opens it in a
  tab of its own. The editor is drawn in the view's colours and fonts and follows its light and
  dark (the theme's button loads it again, its kernel as it was; marimo says "Reconnected"); a
  stylesheet of the notebook's own (`css_file`) has the last word, and a figure with no
  background sits on a light card in the dark theme, as in a note. In a tab of its own it takes
  the view's light or dark and keeps marimo's colours.
- **A concept's notebook**, on the note that starts it (Claude writes it with `rft_set_notebook <its id>`), makes the
  figures and tables that compare the concept's experiments: its first cell (written for you)
  gives `EXPERIMENTS`, each of its experiments' `RESULTS` by id, read from what their notebooks
  saved (an experiment joins it once its notebook has run). It sets `FIGURES` and `TABLES` (saved
  as `figures/<concept id>_<name>.svg`, `tables/<concept id>_<name>.html`) and runs again whenever
  one of its experiments' notebooks records new numbers, so the artifact's comparisons follow
  them at no model turn. Claude writes one when the artifact needs a comparison across experiments, instead of drawing
  it on the page.
- **Shared plotting code** (the style, the palette, helpers) goes in one module in the repo's
  `notebooks/` folder, which is first on every notebook's `sys.path` (e.g. `notebooks/figures.py`),
  and each notebook imports it: Claude writes it once per repo, not in every notebook.
- **In the artifacts**: in a concept with code, `rft_artifact` says for each result whether a
  notebook reproduced it, lists those that are not, and names what each notebook saved; each
  experiment's link in the page carries its last run (✓ reproduced, ≠ differs, ✗ failed).
- **An older vault**: `/rft-update notebooks` runs every notebook again, one after another, as one
  job of the queue with no GPU, in check mode (a Result's numbers are checked, never written
  over), so each saves what a run saves now; the monitor shows how far it is, and its end names
  the notebooks that differ or failed. It also lists, by concept with code, the experiments with a
  result and no notebook (not those with `notebook: no`), for information: a notebook is written
  only for what you choose. `/rft-update notebooks --write <concept>` asks Claude for that
  concept's (the missing experiment notebooks from what its repo saved, each checked against its
  note: one that differs is reported, never recorded over it; its concept notebook; the artifact's
  figures placed instead of drawn), `--write E05 E07` for those experiments only; `--write` alone
  writes nothing.
- It needs `uv` on `PATH`. A vault where no experiment has a notebook sees none of this: the two
  tools wait behind ToolSearch, and their rules are left out.

## Figures

Every notebook draws its figures in the **project's figure style** (the design:
`docs/design/figures.md`): `rft_style.py`, which the run and the editor put beside the notebooks
(commit it with them, so a fresh clone draws the same figures), with the project's tokens written
in. A new notebook imports it as `rs` and applies it; the run applies it to older ones too. Its
helpers draw a figure the way the reference does (Thomas Fel's figures, read from their sources):
one message per figure with a word in bold in its title, the series it is about in the accent and
the rest grey, an ordered parameter as one colour family light to dark, spread as a pale band,
labels at the lines' ends instead of a legend, faint grids, no top or right spines, and a
transparent background for a light page.

The tokens are the project's, in `.rft/config.json`; anything left out takes the default:

```json
"style": {
  "text": "#211A52", "muted": "#76818B", "axis": "#BBC0C5", "grid": "#BBC0C5", "neutral": "#A6A3BA",
  "fill": "#E4E3F5", "accent": "#4D4875", "contrast": "#DF6752", "baseline": "#76818B",
  "categorical": ["#4D4875", "#7A72CC", "#AFAAE0", "#594FBF", "#A6A3BA", "#BDB9E5"],
  "ramp": ["#AFAAE0", "#7A72CC", "#594FBF", "#4D4875", "#211A52"],
  "font": "Arial", "headingFont": "Arial Black", "background": "transparent"
}
```

`accent` is the series a figure is about, `contrast` the one point that must stand out,
`categorical` the colours of unordered series in order, `ramp` an ordered parameter light to dark,
`background` a colour instead of `transparent`. A colour is `#RRGGBB`; one that is not keeps the
default. A font matplotlib does not have falls back to Inter, Helvetica, Arial, then DejaVu Sans.
