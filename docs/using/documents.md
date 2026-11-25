# Snippets and documents

Research ends in writing: a paper, a thesis, an article. Verified notes become writing at **two
levels**, so a finding is consolidated once and a definition reads the same in every document. The
design is in [`docs/design/manuscript.md`](https://github.com/alex-pv01/rft-plugin/blob/main/docs/design/manuscript.md).

- **Snippets are the building blocks**: atomic LaTeX (a definition, a theorem, a result, a method,
  related work), each resting on the notes it states, written once and reused.
- **Documents are what is built with them** (a paper, a thesis chapter). A snippet enters a
  document as a **copy of its text**, at the place you approve, kept referenced to the snippet. In
  the document you may adapt the copy to the narrative, and the document has text of its own
  (transitions, an abstract, its structure). When the snippet changes, its copies are **flagged for
  review**, never rewritten: you take the new text, or keep yours.
- **A document's files hold no trace of the tree** (`docs/adr/0003-a-document-holds-no-trace.md`).
  They are plain LaTeX that compiles from their folder alone, so the folder can go to co-authors
  and to Overleaf as it is: no package or macro of the plugin, no note's or snippet's id, and a
  `.bib` of what the document cites. What ties the document to the tree is kept beside it, in a
  tracking file.

```
vault/snippets/
  snippets.json               the lock, each snippet's stamp of its notes, the next id (the plugin's)
  S04.tex                     one snippet
vault/documents/
  documents.json              the documents' lock (the plugin's)
  paper/                      a document: a folder of plain LaTeX, made from a template
    main.tex                  its main file (any name: the file with \begin{document})
    sections/method.tex       any other .tex file it takes in
    refs.bib                  the entries it cites, and your own
    figures/loss.pdf          the figures its copies include, and what you upload
    icml2027.sty              its template's class and style files
  .rft/paper/tracking.json    what ties the document to the tree, its main file, engine and template (the plugin's)
  .rft/paper/git/             the document's own git data, once it is connected to a repository (the plugin's)
  .build/, rft.sty, rft-numbers.tex, refs.bib   what compiling leaves; the last three for a snippet compiled alone
vault/templates/
  icml2027/                   a template of your own: a folder, copied into a new document as it is
    template.json             optional: {"engine": "xelatex", "main": "thesis.tex"}; not copied
```

```latex
% rft-snippet S04 · result · CutMix at 1k images      (a snippet's first two lines)
% basis: E05, E02
With 1k images, CutMix reaches \rftnum{E05}{acc.1k}\% \cite{R07}.

%%% Result: CutMix at 1k images %%%                   (its copy in a document: two marker lines
With 1k images, CutMix reaches 73.2\% \cite{yun2019cutmix}.   that say its kind and title, and
%%% end %%%                                           plain LaTeX between them)
```

- **Start** with `/rft-manuscript` (both levels and a first document, `paper`; `/rft-manuscript new
  thesis-ch3 report` adds a thesis chapter, `/rft-manuscript new camera-ready icml2027` a document
  from a template of yours) or **Start** in the tree view's **Manuscript** tab.
  Until then the tools wait behind ToolSearch and their rule is left out. A vault that used the first
  layout (`vault/manuscript/`) is brought over by `/rft-manuscript`, each `\rftsnippet` line made a
  copy. A document written before documents were plain LaTeX (copies between `% rft-begin` and
  `% rft-end` lines, macros in its text) is converted once, the first time Claude reads or changes
  it, or with **Convert it** in the tab: each copy keeps its state, and the file as it was is kept
  in `vault/documents/.rft/<name>/first-design/`.
- **A document is made from a template**: a folder of files copied into the new document as it
  is, sample text included. The document then owns its files and keeps no tie to the template, so
  changing a template later changes no document. Two are built in, `article` (a paper) and
  `report` (a thesis chapter). A folder `vault/templates/<name>/` is a template of your own: put a
  venue's kit there, or **Load a zip…** / **Load a folder…** in the New document form, which keeps
  it in `vault/templates/` and offers it from then on (50 MB and 2000 files at most; a zip with one
  top folder is unwrapped; a zip that holds a link, or a path that would leave the folder, is
  refused and nothing is written; a name that is taken asks for another). A template may name its
  engine and its main file in `template.json`, which is not copied.
- **A document is a folder of files.** The Documents view lists every file and folder: **+ File**,
  **+ Folder**, **Upload** (or drop files on the list, or on a folder), and on each row rename (✎)
  and delete (×). `.tex`, `.bib`, class and style files (`.sty`, `.cls`, `.bst`, `.bbx`), `.txt`
  and `.md` open in the editor; an image or a PDF is shown. A file is at most 20 MB. A renamed or
  moved file keeps its copies and values; deleting a file that holds copies asks first, and the
  copies are then shown as lost. A name that carries a trace of the tree (`E05_loss.pdf` in a vault
  with E05) is refused. Renaming does not rewrite the `\input` line that names the file: the
  list flags a file the main file no longer takes in (∅), and a copy in it does not count as placed.
- **The main file** is the one with `\begin{document}`, whatever its name (`example_paper.tex`,
  `master.tex`); nothing is renamed. When several files have it the page asks which, and **Main
  file** in the document's head changes it later.
- **The engine** is per document (**Engine**: pdfLaTeX by default, XeLaTeX, LuaLaTeX). latexmk
  picks bibtex or biber itself, and runs bibtex once per chapter when the document has a
  bibliography per chapter. A document that needs another engine says so, with the button that
  sets it; one that asks for shell escape (`minted`) says it is off, and does not compile.
- **A document is shared through git, by you alone.** **Connect to a repository…** in the
  document's head takes the address of a repository you made (an empty one on GitHub, reached with
  your own SSH keys; the plugin creates none and stores no secret). The document becomes a
  repository of its own, with its git data kept in `vault/documents/.rft/<name>/git/`: the folder
  holds no `.git`, and the vault's own history keeps the document's files as ordinary files. Opening
  the document asks the remote, and the head says how far **behind** and **ahead** it is and how
  many files changed (**Check** asks again). Open the same repository in Overleaf through its
  GitHub sync to write there with co-authors.
    - **Push…** records every change with the message you type, and sends it. It is refused, with
      the file and line, when the scan finds a trace of your tree (so that no commit ever holds
      one; **Allow** a false alarm and it goes through), when the document is behind (it offers
      Pull), and while a conflict is unresolved.
    - **Pull** merges what was pushed to the remote. Changes you had not pushed are recorded first,
      under a message that says so, and not sent. After a pull the copies are found again by their
      marker lines, else by their text, else they are **lost**; a co-author's rewording inside a copy
      reads as **adapted**, and a number of the tree they changed is listed as no longer the tree's.
    - **A conflict** is left in the file as git's own lines (`<<<<<<<` … `>>>>>>>`), the files that
      have one are listed under **Conflicts**, and Compile, Pull and Push wait: keep what is right,
      delete those lines, save, then Push records the merge.
    - **From a repository…**, in the New document form, makes a document from a repository that
      already exists (a paper started in Overleaf): its files as they came, nothing tied to your
      tree yet. Select a passage and **Selection is a copy** ties it to a snippet; in such a
      document the file is left as it is (no marker lines are written around a co-author's text;
      the copy is found by its text, and offered its marker lines). Traces found in what came are
      listed, not removed.
    - Claude never pulls or pushes: there is no tool for it, and its git commands against a
      document's repository are refused.
- **A document is reused** from **More…** in the file list:
    - **Duplicate this document…** makes a second document with the same files, copies, values,
      allowed occurrences, main file and engine, tied to nothing of the first and connected to no
      repository: the submitted version stays as it was while you prepare the resubmission.
    - **Bring another document in…** copies a document's files into a new folder of this one, once,
      with its copies and values tracked under their new paths: a paper becomes a chapter of a
      thesis by papers. Nothing is rewritten. The page says what remains for you (take the paper's
      body in with `\input`, without its preamble; the lines that name a file of the paper, which
      is now read from the thesis's top) and what clashes (labels and `.bib` keys both define, with
      both places). The source document is unchanged, and the two are not tied afterwards.
    - **Add a template's files…** copies a template of the vault into this document without
      overwriting anything: a file whose path exists is skipped and named. The preamble is yours to
      rewrite for the new class or style.
- **Only verified notes go in.** Claude proposes snippets from verified notes only (see Statuses),
  and where to place them: `/rft-manuscript [document]` asks it for two tables, snippets to write
  and placements; nothing is written until you pick. A picked snippet is a **stub**: its two header
  lines, its outline as comments, the kind's environment (`definition`, `theorem`, … a
  `\paragraph`, a `figure` or `table` float), for you to fill. You may rest a snippet of your own on
  any note; one not verified is flagged until it is.
- **Nothing is typed twice.** In a snippet, `\rftnum{E05}{acc.1k}` gives a number of the
  experiment's saved RESULTS (`results/E05.json`, by path), `\rftfig[width=.8\linewidth]{E08}{loss}`
  its figure (a notebook's run saves each matplotlib figure as PDF beside its SVG),
  `\rfttable{E08}{by_seed}` its table (saved as a booktabs tabular beside its HTML). `\cite{R07}`
  cites a reference note, and each paper of a literature note is cited by the key of its
  ```` ```bibtex ```` block. Compiled alone, a name that is not there prints **??**.
- **Placing writes it out.** The copy holds the number itself, `\includegraphics{figures/loss.pdf}`
  with the figure copied into the document under its own name, the tabular, `\cite{yun2019cutmix}`
  with the entry added to the `.bib` its file uses (the nearest `\bibliography` or
  `\addbibresource` that covers it: a thesis with a `.bib` per chapter gets the entry in that
  chapter's; where nothing says which, the page asks once and remembers), and a label made from the
  kind and the title (`def:cutmix`). An entry of your own that a document cites is listed under
  **Cited without a reference note**, in the page only. A macro that names nothing saved refuses the placement. A snippet may be placed
  more than once in a document, in any of its `.tex` files; the second copy is `S04#2`.
- **What was written out is watched.** When a notebook saves another number, or a figure again,
  every place it was written is listed under **Values to look at**: **Take** the tree's, or **Keep
  mine**. A number someone changed in the document is listed as no longer the tree's.
- **A copy is found by its marker lines**, so ask co-authors to leave them in place. One whose
  marker lines were deleted is found by its text (and offered them back); one whose text was
  rewritten too is **lost**: select the passage and **It is the selection**, or **Drop** it. A
  passage a co-author wrote can be tied to a snippet the same way (**Selection is a copy**).
- **Traces of the tree** in a document's files are listed in the tab: a macro or a name of the
  plugin, the id of a note or a snippet of this vault in a text or a file's name, an entry of the
  tree the document does not cite. **Allow** remembers one that is a false alarm. `rft_validate`
  says them too.
- **Changes go up one level at a time.** A note that changes, goes to review, is superseded or
  dropped puts the snippets resting on it in **review**; **Reviewed** takes their stamp anew. A
  snippet whose text changes puts its copies in **review** in every document holding one; a copy
  that differs from its snippet as placed is marked **adapted** (shown, not flagged). A note's
  drawer lists the snippets resting on it (**Written in**); a snippet lists the documents and
  files using it, and how many copies each has (**Used in**).
- **Locked by default**, both levels, as a locked note is: Claude's Edit, Write and shell writes to
  snippets and documents are refused; it proposes stubs and placements, and comments and suggests on
  your text when you ask (on a snippet or a document, as on a note). The padlocks unlock the
  snippets, or one of them, and the documents, or one of them, for Claude to write too. One lock
  covers all a document's files. In an unlocked document Claude edits and creates `.tex` and `.bib`
  files only (a class or style file of the template, and a file you uploaded, are refused with
  the reason), and its edit is still refused when it would write a trace. The registries, the tracking
  files and the generated files are the plugin's alone.
- **The Manuscript tab**, two views:
    - **Snippets**: the library by kind, each with its state, how many documents use it and its open
      threads; **+ Snippet**; the open snippet in the editor (CodeMirror, LaTeX mode), its notes as
      chips that open them in the drawer, **Used in** with each document and file (a click goes to
      the copy), **Place in** a document; **Compile snippet** shows it alone, in a minimal article.
    - **Documents**: the document menu and **+ Document** (its template, its title for a built-in
      one, and its name, checked as you type); its files and folders, each opened by a click, the
      open one with its outline (headings and copies, each copy with its state); **Place** a snippet from the library in the open file, after
      a copy or a heading; the copy the cursor is in, with **Move after**, **Remove**, and in review
      the snippet **as it was placed and now** with **Take the new text** and **Keep mine**; **Lost
      copies**, **Values to look at** and **Traces of the tree** below the files; the editor on the
      open file, copies shaded by state; **Compile** runs latexmk in the document's folder alone and
      shows its PDF beside it, its errors a click away (an environment the document does not declare
      comes with the action that adds its `\newtheorem` line); a failed compile keeps the last good
      PDF.
    - **Save** writes the file (a file changed meanwhile asks first); Ctrl/Cmd+S saves and compiles.
      Select text and choose **Comment** or **Suggest** to discuss it, with **Ask Claude**, **Accept**
      and the rest. `?view=manuscript&snippet=S04` or `&doc=paper` opens one. Compiling needs
      `latexmk` on `PATH` (TeX Live), shell escape off, and the page's key; the PDF goes only to the
      page carrying it. `/rft-view` leaves the tab out.
