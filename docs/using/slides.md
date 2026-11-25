# Slides

**Slides** (after Manuscript) holds slide decks for meetings and talks: this week's wrap-up with
your supervisors, a paper presented to the lab, a workshop talk. A deck is one Markdown file in
`vault/decks/`, e.g. `P01 Weekly wrap-up.md`, its slides separated by a line `---` as Obsidian's
Slides plugin reads them (the design: `docs/design/presentations.md`).

```markdown
---
id: P01
type: deck
for: [G01 2026-11-24]      # a meeting's occurrence (G04 alone for a once-only one), or a deadline (M04)
locked: true
---

# Weekly wrap-up
Supervisor meeting · 24 Nov

---
<!-- slide layout="two-cols" -->

## Accuracy at 1k images
- [[E05 Mixup and CutMix at 1k images]] done
::right::
![[E08_loss.svg]]

note: start with E05
```

- **Slides**: a slide may open with `<!-- slide layout="…" -->`: `title` (the first slide's
  default), `default`, `section`, `two-cols` (split at a line `::right::`; `split="60"` gives the
  left column 60 % of the two), `figure` (one image filling the slide). The same line takes
  `title-color` and `title-size`, the heading's own on that slide. Everything after a line `note:` is the speaker's, never on the slide or in
  the PDF. The rest is the notes' Markdown: links to notes, KaTeX math, tables, code, `###`
  headings and numbered lists, and images found as Obsidian finds them, so `![[E08_loss.svg]]` is
  the figure a notebook saved in `vault/figures/`.
- **Boxes and lines**: what a layout does not place, you place yourself, as comment lines in the
  slide's text (Obsidian's reading view hides them and shows a box's text as a paragraph):

    ```markdown
    <!-- box x="1180" y="620" w="520" color="contrast" size="40" -->
    gap closes here
    <!-- /box -->

    <!-- box shape="ellipse" x="980" y="410" w="160" h="120" outline="contrast" -->
    <!-- /box -->

    <!-- line from="1180 660" to="1130 500" arrow="end" outline="contrast" -->
    ```

    A **box** has a place and a width in whole numbers of the 1920 × 1080 slide (`x`, `y`, `w`) and
    holds Markdown: text, a figure (alone in its box, it fills the width, its proportions kept), or
    nothing, which leaves a plain shape. `h` fixes its height; without it the box is as high as its
    text. `shape` is `rect` or `ellipse`; `fill` and `outline` colour it (`weight`: `thin`,
    `medium`, `thick`); `color`, `size` and `align` (`left`, `center`, `right`) style its text, and
    `valign` (`top`, `middle`, `bottom`) places it in a box with a height. A **line** runs `from`
    one point `to` another (`"x y"`), with `arrow` (`start`, `end`, `both`), `outline` and `weight`.
    A colour is the name of one of the project's figure tokens (`text`, `muted`, `accent`,
    `contrast`, `baseline`, `neutral`, `axis`, `grid`, `fill`, and `c1` to `c6`, the categorical
    ones), so a change of tokens recolours the deck, or `#rrggbb`. They are drawn over the layout,
    the later in the text in front, in the same place in the tab, the presentation and the PDF. One
    written wrong (a box not closed, a position that is no whole number, an unknown option or
    colour) is listed under the text by slide and line, and by `rft_validate`; the slide is still
    drawn.

- **On the slide** (a desktop's mouse and keys; a phone keeps the slide as a view): the slide
  beside the text is where you move them. A click selects a box or a line (a shape with nothing
  in it, by its outline) and puts the editor's cursor in its text; the cursor in its text selects
  it. A drag moves it; the handles resize it, a line by its two ends; a figure keeps its
  proportions; a box as high as its text takes a height once its top or bottom is dragged. What
  is dragged snaps to the slide's edges and middle and to the other boxes and lines, with a
  guide (Alt: not); Shift keeps a box's proportions, or a line straight or at 45°. A box may hang
  over the slide's edge, not leave it. The arrow keys move by 1, with Shift by 10; Delete
  removes; Ctrl+D duplicates; Ctrl+C, X and V copy as text, to another slide, another deck or any
  editor; Ctrl+] and Ctrl+[ put in front and behind (with Shift, of all); the bar above the slide
  has the same, and hides the text to give the slide its room. The bar adds too: **Text**,
  **Rectangle**, **Ellipse**, **Line**, **Arrow**, each dragged out on the slide (or clicked, for
  its usual size), written after the slide's content and before its `note:`. It colours what is
  selected (fill, outline, text: none, the project's tokens by name, or `#rrggbb`), sets the
  outline's weight, a line's arrow, the text's size and its place in its box, and gives a box's
  height back to its text. A style is a whole box's, never a few words'. A double click on a box
  (or Enter) opens its Markdown over it, at the slide's size and in its font: its source, not the
  drawn text, so math, links and macros stay exact; Bold and Italic (Ctrl+B, Ctrl+I) put `**` and
  `*` around what is selected; Esc or a click outside draws it again. A shape's first label goes
  to its middle; a box of text left empty is removed. A new box of text has a width only: drag
  its bottom to fix its height, and text longer than its box stays in view, marked in the editor
  alone, never shrunk. **Figure** lists the figures the notebooks saved, by the note that made
  each, and adds the one you pick as a box that shows it by reference (`![[E08_loss.svg]]`), so it
  follows its notebook: run again with other proportions, the box keeps its width and its height
  follows. **Image** takes a picture of your own, as does pasting one on the slide or dropping it
  there: it is copied to `vault/decks/assets/` under its deck's name (`P03-1.png`) and shown in a
  box. Neither is ever cropped or stretched. What a layout places is in its **slots** (the
  heading, a column, the figure, the caption): a click selects one, a double click (or Enter)
  opens its Markdown over it, and a column's content is dragged to the other column, but nowhere
  else: **Detach** takes it out of its layout, as a box in the same place. The divide between two
  columns is dragged (`split="60"` on the slide's options line: the left one's share), the
  heading takes a colour and a size of its own per slide (`title-color`, `title-size`: the bar's
  text colour and size, with the heading selected), **Figure** puts its figure in the slot
  selected, and the layout gallery changes the slide's layout or adds a slide of one after it.
  Several at once: Shift and a click add a box or a line to those selected (or take it away), a
  rectangle dragged out over the slide takes all it touches, Ctrl+A all of them; they move, are
  nudged, copied, duplicated and removed together. **Align** brings their left sides, middles,
  right sides, tops or bottoms in line (one alone: with the slide), **Distribute** puts three or
  more evenly apart, the outer two staying. Nothing is grouped: the selection is not kept.
  Every action is an edit of the text and of nothing else, in the editor's
  own history: Ctrl+Z undoes a drag in one step, whichever side the cursor is on.
- **For**: `for:` lists where the deck is presented, one or more: a meeting's occurrence by the
  day its rule gives it (`G01 2026-11-24`; moved to the 25th, the deck goes with it), a once-only
  meeting by its id, a deadline by its id. A practice talk and the real one are one deck for both.
  The Calendar marks those occurrences, and a meeting's occurrence or a deadline opened there lists
  its decks (**Open**) and offers **+ Slides**, a deck for it. `rft_validate` names a `for:` that
  is no meeting or deadline, a day the meeting does not fall on, a skipped occurrence (the deck is
  presented nowhere) and a recurring meeting named with no day.
- **The tab**: the decks by what they are for, what comes next first, then those for nothing, then
  the past ones; **+ Deck** (a title, and one of the next occurrences, a deadline, or nothing); the
  deck's text in an editor, saved as you type (a deck changed on disk meanwhile asks first: take
  it or keep yours); beside it the slide the cursor is in, drawn as it is presented, its speaker
  notes, and every slide as a thumbnail (a click goes to its text). **Present** shows it full
  screen from the slide in view: → space PageDown or a click go on, ← PageUp or a right click go
  back, Home and End, Esc out. **PDF** prints the deck alone, one 16:9 page a slide, without the
  notes: choose Save as PDF in the print dialog. A slide keeps its own light colours whatever the
  page's theme.
- **Locked**: decks are yours to write. A deck is locked unless it says `locked: false`; the
  padlock in the tab changes it. Claude's own writes of a locked deck, or of a new deck by hand,
  are refused: it proposes an outline in the chat instead. `/rft-view` leaves the tab out.
