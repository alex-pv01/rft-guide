# Deadlines, meetings and the calendar

**Calendar** (beside Kanban) shows the deadlines, the meetings and the experiments' runs, as a
**Timeline** or a **Month**. The dates are yours alone, as priorities are: Claude suggests them,
and its own edits that change them are refused.

- **Deadlines** (a submission, a talk, a thesis chapter) are milestones: one note each in
  `vault/milestones/` (outside the tree), e.g. `M01 Workshop paper.md`, with `due:` and the notes it
  `needs:` done first. A due date is a day, a local time or a time in a zone: `2026-11-13`,
  `2026-11-13 14:00`, `2026-11-13 23:59 AoE` (or `UTC`, `+01:00`); a zoned one also shows the time
  where you are. **+ Deadline** adds one (or click a day of the Month); a deadline's name opens its
  editor (due date, needs, **Done**). Any note can also have a `due:` of its own.
- **Meetings**, once or recurring, are one note each in `vault/meetings/`, e.g.
  `G01 Supervisor meeting.md`:

    ```yaml
    when: 2026-11-10 14:00       # the first one: a day, a time, a zone as for a due date
    duration: 1h                 # 45m, 1h30m
    every: week                  # day, 2 weeks, month (the same date), month on the first Tuesday
    until: 2027-06-29            # the last day it may fall on (none: no end)
    skip: [2026-12-22, 2026-12-29]
    moved: ["2026-12-01 → 2026-12-02 10:00"]
    ```

    `every:` takes any number of days, weeks or months, and a weekday of the month (`first` …
    `fifth`, `last`; a month without a fifth one is skipped, as is one without a 31st for a meeting
    on the 31st). **+ Meeting** adds one (or click a day of the Month): its repeat menu is worked
    out from the day (every week on Tuesday, every month on the 4th, on the fourth Tuesday, on the
    last Tuesday, or Custom…). Click an occurrence, on the Month or the Timeline, to **Move** it (a
    day and a time), **Skip** it, bring a skipped one back, or end the series with it (**Last one**);
    below, the series itself (its day and time, length, repeat, until, needs), **Save** or
    **Delete**. A meeting with `needs:` is a deadline too, at its next occurrence: planned for, at
    risk, on the cards and the kanban as the others are. The strip above the calendar shows the
    meetings of the next 7 days.

- **An experiment's run**: `start:` (a day) and `est:` (`3d`, `2w`), set in the note's drawer or
  by dragging its bar on the Timeline (the bar moves the start, its right end the estimate).
  In a vault that uses dates, `rft_set_status` records `started:` and `finished:`. `after:` names the runs it waits for, and
  `gpus:` how many GPUs it takes (one when not given).
- **Planning**, backwards from each deadline in whole days: what it needs must end by its due day;
  each note's latest start is the due day less its estimate (and less those that come after it),
  its slack the days from its earliest start (today, its start, the end of what it waits for) to
  that. A deadline is **at risk** (red) at 0 days of slack or less, or when a note it needs was
  dropped, superseded or is missing; amber when 3 days or fewer are left. The cards above the
  calendar say which note puts it at risk and how ("E04 3d over its 3d estimate", "E05 must start
  today").
- **Timeline**: one row per experiment with dates, or needed by a deadline, by concept: its run
  (planned, running, done; a run over its estimate hatched in red, one with no end fading out),
  Claude's suggestion dashed, and for a run not planned yet the latest it may run, dotted (drag it
  to plan the run). The deadlines are lines across the rows, today a band. With `gpus:` in the
  config, a strip below shows the GPUs taken each day, red above the capacity. **‹ Today ›**
  scroll, **− +** zoom.
- **Month**: the runs across each week, the deadlines on their days (Claude's dashed, done ones
  struck through), the meetings on theirs (a moved one in italics, a skipped one struck through).
  On the **Timeline**, each meeting has a row above the experiments, a mark on each day it falls on.
- **Claude suggests** a start and an estimate (`rft_suggest_dates`) and paper submissions
  (`rft_suggest_deadline`, read from the venue's official dates page, never from memory); you
  **Accept** or **Dismiss** them in the drawer and in the Calendar. A dismissed deadline stays
  in the vault as dismissed, so it is not suggested again. A deadline you tell Claude in the chat
  it adds with `rft_add_deadline`, once you confirm it in a dialog.
- `rft_next` lists the deadlines first, with what puts them at risk, the GPU clashes and the
  meetings of the next 7 days; session
  start names the deadlines of the next 14 days that are at risk. A kanban card shows the
  deadline nearest it.
- **`vault/rft.ics`**, rewritten by `rft_sync` when the dates change, holds the deadlines, the
  meetings (a recurring one as a series: its rule, its skipped days, each moved one as an event of
  its own) and the planned runs (never the suggestions), for any calendar app to import; **.ics**
  in the Calendar downloads the same.
