# The experiment queue

**There is no queue until a machine is paired with it.** Until then nothing of it shows: no queue
tool or rule for Claude, no runner, no monitor in the tree view, and the tree works as before.
`/rft-machine add` pairs the machine the session runs on (only this machine for now):

1. It checks the machine at no model turn (`rft_queue.py machine probe`, under a second): its
  NVIDIA GPUs (`nvidia-smi`, with driver and CUDA), the disks a run's outputs may go on (from
  `df`, the most room first, system and snap filesystems left out), conda (its root and envs,
  read from its files) and uv. A machine with no NVIDIA GPU stops there: it says so and the queue
  stays off.
2. Claude then asks two questions, nothing more (it does not explore the machine): where the runs'
  outputs go (the disk with the most room suggested, or the config's `runsDir` if it has one) and
  which GPUs to keep out of the queue for your own work (none by default). It pairs the machine
  with `rft_machine add`: `vault/.queue/machine.json` names it (host name, GPUs, outputs' root,
  conda and uv), the outputs' root is made, and the queue is on, its tools in the session from
  the next turn and its monitor in the tree view within seconds.
3. On a machine already paired, `/rft-machine add` changes nothing: it says the local machine is
  already loaded and prints its status (GPUs, the outputs' root and the room left, conda and uv,
  the jobs). `/rft-machine` alone prints the same.

Once it is on, **every run of an experiment goes through the queue** (`rft_queue`, with no GPU
for a run that needs none), never into the background with Bash, so you and Claude see every run
and what it holds: a job is a command, the folder it runs in and how many GPUs it takes, for one
experiment note. A **runner**, a small process of its own (`server/rft_queue.py`, Python standard
library), starts each job as soon as enough GPUs are free and records how it ended. It is apart
from any session: a run goes on after the session that queued it ends, and the runner stops by
itself once the queue has been empty a minute (queueing a job, opening the tree view or starting a
session brings it back).

- **The monitor**: the chip icon at the top left of the tree view, its badge counting the jobs
  running and waiting (`?jobs` in the address opens it, `?jobs=history` on its history). It shows
  each GPU (memory, use, temperature, and what holds it: a job of the queue, with its experiment,
  or a process outside the queue), then two tabs:
    - **Queue**: the jobs running (how long, on which GPUs) and those waiting, in their order, each
      with why it waits ("1st in line: needs 2 GPUs, 1 free"). Drag a job, or use its buttons (each a symbol: up, down, first in line),
      to change the order, or ask Claude ("run E17 before E16": one `rft_job` call, answered
      with the new order in one line); **Stop** (■) / **Cancel** (✕) ends a job (press twice: the button says Stop? or Cancel? in between); pause (press twice) starts no new
      job (the running ones go on), resume (one press) lets them start again; Claude can cancel, retry, pause and resume too, when you ask. Untick a GPU to keep it out of the queue (for your own work).
    - **History**: every job that ended, newest first, with its experiment, how it ended (done,
      failed with its exit code, cancelled), how long it ran, and **Retry** (↻: first in line again).
      **Log** (lines of text) / **Command** (`>_`, on a waiting job) shows its command, the code it ran and its output folder, and its
      output: the last 64 KB, then what it writes as it comes (only the new bytes cross an SSH tunnel),
      in a box that follows the end unless you scroll up to read, keeps its place across refreshes, and
      can be made taller; a progress bar shows its last state, colour codes are dropped. **Whole log**
      saves the whole output as a file. The history says how each notebook run went (wrote the
      numbers, reproduced, differs, failed). The experiment ids
      open their notes in the drawer. Watching, reordering and retrying cost no model turn and no token.
- **Order**: strict. The first waiting job that needs GPUs takes them once enough are free; nothing
  behind it starts first (move it down to let smaller jobs pass). A job that takes no GPU never
  waits. A GPU with someone else's process on it, or more than 1000 MiB of memory taken, counts
  as busy, so the queue never starts a job on top of your notebook.
- **A job runs** as `bash -c <command>` in its folder, in a process group of its own, with
  `CUDA_VISIBLE_DEVICES` set to its GPUs (numbered as nvidia-smi numbers them), `RFT_JOB`,
  `RFT_EXPERIMENT` and `RFT_OUT`; its log goes to `vault/.queue/logs/<job>.log`. It gets the environment the
  runner started with, not your interactive shell's, so its command activates its conda or venv
  itself. A job whose process is gone without an exit code (killed, or the machine restarted) is
  recorded as lost.
- **Its outputs** go to `$RFT_OUT`, a folder of its own: `<runs>/<repo>/<experiment>/<job>` with
  the outputs' root chosen when the machine was paired (`<repo>` the name of the job's repo
  folder, or of its own folder outside git), else `<repo>/runs/<experiment>/<job>`, at the top of
  the job's git repo (the runner gives a `runs/` it makes a `.gitignore`, so the outputs stay out
  of git).
- **How far it is**: each running job's row shows its stage, one tqdm bar (the outermost still
  running: its label, a meter, n/total, % and time left, and its postfix such as `loss=0.31`) and
  its last line of text, read from what the job writes anyway: the end of its log, and
  `$RFT_PROGRESS` (`progress.jsonl` in its output folder). A bar whose label carries a changing
  metric counts as one. `rft_jobs` gives Claude the same in a line. How to write a job so the
  monitor reads it well is just below.
- **The waiting jobs fold** into one line ("▸ 3 waiting: q11 E25, …") with a click on their
  heading ("▾ 3 waiting, in order"); the GPUs, the running jobs
  with their progress and the history stay. The panel remembers it; a click on the line unfolds them.
- **The run record**: each job is the record of its run. When it starts, the runner records the
  code it runs: the repo, its commit and branch, and its uncommitted changes to tracked files,
  saved whole as `code.patch` in its output folder (untracked files are counted, not kept); so a
  job never waits for a commit, and the run can be made again exactly from its commit, its patch
  and its command. When it ends: the end of a failed one's traceback (the session's line and
  `rft_jobs` show it, so Claude rarely reads the log), and whether the repo's code moved while it
  ran. Each output folder holds a copy of its record (`rft-run.json`), so the outputs say what made
  them.
- **The notebook, after the runs**: when an experiment's last job ends well and the experiment
  has a notebook, the runner runs it as a job of its own (`notebook`, no GPU): its numbers land in
  the note's Result, its figures and tables in the vault and the concept's artifact, at no model
  turn and with no session open (see Experiment notebooks). The session then tells Claude the
  numbers are recorded, and Claude writes what they mean.
- **With the notes**: when a job starts, its experiment goes from planned to running (the plugin
  does it, no model turn) and a toast says so; when one ends, a toast says how. The note is then
  left to Claude: `rft_next`, `/rft-next` and the start of the next session list the experiments
  whose job ended and whose result is not recorded yet (or whose numbers the notebook recorded,
  to be interpreted), and Claude reads the job's record (`rft_jobs <job>`) only then, not by
  polling.
- `/rft-jobs` prints the queue in the terminal, at no model turn.
- **Files**, in the vault's `.queue/` (a dot folder Obsidian leaves alone): `machine.json`, the
  machine it is paired with; `queue.json`, the jobs waiting and running in their order;
  `history.jsonl`, one line per job that ended. Its `.gitignore` keeps all of it out of git: the
  queue belongs to the machine it runs on, so a clone of the vault on another machine has no queue
  until that machine is paired. A vault synced as a folder to another machine (not through git)
  shares `.queue/`: there the queue stays with the machine it names, which alone runs it, and the
  other is told so; to move the queue to a new machine (or after a rename), delete
  `.queue/machine.json` and pair it. A vault made before pairing existed keeps its jobs and
  history, and the session says `/rft-machine add` turns its queue on again; if your vault is in
  git and holds `.queue/queue.json` or `history.jsonl` from then, `git rm --cached` them once.
- Only this machine's NVIDIA GPUs for now (nvidia-smi); another machine over SSH, or a cluster
  (SLURM), would be further tabs beside this machine's.

## Writing a job the monitor can read

The monitor reads three things a job writes: its tqdm bars, its lines of text, and
`$RFT_PROGRESS`. Claude follows these when it writes a script for the queue (the manual has them);
for your own scripts:

1. **A tqdm bar on each loop longer than a minute**, with a fixed `desc` and a `total`:
  `tqdm(loader, desc="train", total=len(loader))`. The monitor shows one bar per job: the
  outermost still running (the epochs, not the batches inside them).
2. **Numbers that change go in the postfix, never in the label**:
  `bar.set_postfix(loss=f"{loss:.4f}")`, not `bar.set_description(f"train loss {loss:.4f}")`.
  The monitor shows the postfix after the bar.
3. **Inner loops** get `leave=False`. Leave `mininterval` alone: the runner sets 10 s
  (`TQDM_MININTERVAL`), so a bar redraws every 10 s and logs stay small.
4. **Stages**: a job of several steps appends one line per step to `$RFT_PROGRESS`, a JSON
  object `{"stage": "train", "i": 2, "n": 3}` (or a plain line of text). From bash:
  `echo '{"stage": "probe patchpos", "i": 2, "n": 5}' >> "$RFT_PROGRESS"`. The monitor shows
  "Stage 2/3: train" above the bar.
5. **Lines of text**: one per event, starting with the time (`2026-11-16 12:00:05 epoch 7: val
  acc 0.912`), written as they happen (`print(..., flush=True)`, or `PYTHONUNBUFFERED=1`). The
  last one shows under the bar. Nothing per batch.
6. **Results go to `$RFT_OUT`**, never into the log: no arrays, tables or per-sample prints.
7. **Failures raise**: let the exception end the job with its traceback (the runner keeps its
  end, and `rft_jobs` shows it) and a non-zero exit; never catch it and only print.

[`examples/job_progress.py`](https://github.com/alex-pv01/rft-plugin/blob/main/examples/job_progress.py) does all of this in 50 lines, and
`tests/test_queue.py` runs it through the queue to check the monitor reads it as above:

```
Stage 2/3: train
train  ███████░░░  7/10 · 70% · 00:12 left · loss=0.1429
2026-11-16 12:00:05 epoch 7: val acc 0.912
```
