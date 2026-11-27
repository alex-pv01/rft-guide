# Grilling a direction

A new direction is usually planned by saying what you want and letting Claude propose
experiments. Nobody then asks what result would change your mind, whether the tree already
answered the question, which papers should be read first, or what would show the result is right
other than Claude and you. **A grilling** is the session that asks: Claude questions you about
one direction, in rounds, until its plan is agreed.

## Starting one

- **`/rft-grill-me D14`** grills a direction that is already in the tree.
- **`/rft-grill-me "does mixup help below 1k images?"`** grills a question that is not a note
  yet. Claude first looks up what the tree holds on it, and adds its note only once you agreed
  its wording and where it goes.
- **`/rft-grill-me <concept>`** lists that line of research's open questions and its directions
  at idea or planned, and asks which one to grill.
- **`/rft-grill-me`** alone prints the directions you could grill (at idea or planned, those
  with nothing run or planned under them first), without a model turn.

Claude may offer a grilling when you open a direction with no experiment planned under it. It
never starts one unasked.

## Rounds

Before the first round Claude reads what the tree already holds on the question, and opens with
it. Then it asks **every question that can be asked now** in one message, numbered, each with
the answer it recommends and worded so that "yes" accepts it:

```
Q1 - The hypothesis: Is the claim "with a cosine schedule to zero, the last epoch's test
accuracy at 1k images is within one point of the early-stopped baseline, over three seeds"?
→ Yes: it can fail, and E02 already gives the baseline's number.

Q2 - The result that would change your mind: Would a gap of more than three points on two of
the three datasets end this direction?
→ Yes.
```

You answer the round in one message ("yes to all", or question by question). A question whose
answer depends on another of the same round waits for the next one. Facts are Claude's to find
(the tree, the code, a paper); it asks you only for decisions.

## The seven subjects

A grilling ends when each of these is settled, or set aside in your words ("no milestone"):

1. **The question**: the claim as a hypothesis that can fail, the result that would change your
   mind, what is out of scope.
2. **Its place in the tree**: what the tree already holds on it, its parent, its concept.
3. **Literature**: what must be known before any run, as named searches, each with the question
   it answers.
4. **Preliminary experiments**: the cheapest decisive ones, the reference whose setup each
   starts from, and what each outcome would mean, including the one that ends the direction.
5. **Order and priority**: what runs first and what waits for what.
6. **Milestone**: a deadline or a meeting this serves, if any.
7. **The referee**: what would show the result is right and depends neither on your judgment
   nor on Claude's: a published number reproduced, a run of the untouched original code. It is
   asked every time.

While you answer a round, Claude may look quickly for prior art. What it finds it reports as
not read and saves to [the inbox](inbox.md); none of it becomes a reference. A thorough search
is only named during the grilling and run after it.

## What is written, and when

**While the grilling runs, only the direction being grilled**, in sections of its own:
**Hypothesis**, **Scope**, **Plan**, **Referee**, and **Open questions** (what is not settled
yet). Each appears once it has something in it, and only on a direction that was grilled. If the
session is cut, the same command on the same note goes on from what these sections answer and
asks none of it again.

**Everything else is one numbered table at the end, the proposal**, and only the rows you
confirm are written:

| row | becomes |
|---|---|
| a sub-direction | a direction at idea |
| an alternative you rejected | a direction at discussed, with your reason |
| a definition that settled | a theory note |
| a literature search | a literature note at planned, with the question it answers |
| a preliminary experiment | an experiment at planned: what, why, its references, what it waits for, what each outcome means, the referee's check it must pass |
| a priority, a start date, an estimate | a suggestion you accept or dismiss, as always |
| a milestone | a deadline you confirm in its dialog |

An experiment with no reference to start from is not blocked: its row says a search is missing
and names the search that would supply one. A planned literature note sits on the kanban like
any note, and **`/rft-literature <its id>`** later runs the search and fills that note.

A grilling stops at the plan: no code is written and nothing is queued. It leaves a
[handoff](handoffs.md), so the session that runs the experiments starts from the notes.

## Notes it does not touch

- **A verified or locked note** is left as it is: the grilling is about a new direction under
  it, and a change to the locked note comes as a suggestion.
- **A direction the tree already answers** (done, dropped, discussed, moved, superseded): Claude
  says what the tree holds and asks whether to stop, or to reopen the question as a new
  direction that says what changed. Nothing is written until you answer.
- **A note that is not a direction** (an experiment, a reference, a theory note): the grilling
  is about the direction that comes out of it.
- **An experiment or a search already under the direction** is refined in place, as a row of
  the proposal; no second note is added for the same run or search.

## How it ends

- **Agreed**: every subject is settled or set aside and you confirmed a proposal with at least
  one search or experiment. The direction becomes planned.
- **Not worth pursuing**: the tree already answers it, no experiment would decide it, or no
  referee is possible. The direction becomes discussed, with the reason, and nothing is added
  under it. This is a result.
- **Stopped early**: you say stop. The proposal holds what is settled, the rest stays under
  Open questions, and the status does not change.
