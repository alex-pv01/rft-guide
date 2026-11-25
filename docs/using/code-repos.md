# Code repos

A concept can link the code it runs on: one or more repositories on the machine, in its
starting note.

```yaml
concept: "Schedule-free training"
concept_summary: "Training without a stopping rule"
concept_repos: ["/home/me/code/sfree", "../code/train-utils"]
```

Paths are absolute, `~/…`, or relative to the tree's folder (the one holding `.rft/`). On the
root note, `concept_repos` is the code of the whole project.

- **Priority.** A note works with its own concept's repos first, then with those inherited from
  the concepts above it. A sub-concept's code is the most specific.
- **When a concept is created**, Claude asks whether code for it already exists, and where, and
  links it with `rft_set_repos`. It then reads the code and gives the concept's experiments and
  directions a `## Code` section. `rft_set_repos` also says whether sessions started in the repo
  reach the tree; when they don't, it names the `.rft/config.json` link that would fix that, and
  Claude asks before writing it.
- **The `## Code` section** says how the note relates to the code: entry points, files,
  functions, configs, what has to change. A direction gets a short pointer. It opens with one
  line per repo, written by the plugin from git, holding the commit the references were checked
  against:

    ```
    ## Code
    - `/home/me/code/sfree` @ 3f2a1c9d0e (main) · checked 2026-11-06
    - `../code/train-utils` @ a1b2c3d4e5 (main) · checked 2026-11-06 · inherited from Strong augmentation

    Entry point `train.py --schedule free`, config `configs/cifar_1k.yaml`; needs a new
    `--no-early-stop` flag in `train.py`.

    **Reproduce:** at 3f2a1c9d0e: `python train.py --config configs/cifar_1k.yaml --seed 0 1 2`;
    raw outputs in `runs/E08/`, aggregated with `tools/summary.py`.
    ```

- **The code as it is now comes first.** Before working on an experiment, Claude calls
  `rft_code`. It shows the commits and changed files since the note was last checked, uncommitted
  changes included. Claude reads those changes, updates the references, and `rft_set_code`
  records the current commits. Plans and proposed changes start from the current code, not from
  an older note's commit.
- **Results live in the experiment's note.** Each repo stores its outputs its own way. Claude
  processes them and writes the numbers in **Result**, and the Reproduce part says how to get
  them again: the commit of the run, the command and config, where the raw outputs are, and how
  they were processed. That commit stays fixed when the references are checked again later.
- `rft_validate` warns about a repo that is missing or not under git, `concept_repos` on a note
  that starts no concept, and a Code section that is missing or names a repo the concept no
  longer links.
- The tree view shows a note's code under its concept path in the drawer, with inherited repos
  marked as such. The concept tree names each concept's repos.
