"""Split the plugin's long README into the guide's pages, as it is written.

A tool for the move only. While the plugin's README is still the long one, other work keeps adding
to it, so the split is run again instead of copied by hand:

    python3 scripts/split_readme.py ../rft-plugin/README.md

It writes the pages listed in PAGES and nothing else. It stops when the README has a section it
does not know, so a new section is placed on purpose. Once the README is the short one, the pages
here are the source and this script is deleted.

What it changes in the text, and why:
- headings move up, so each page starts at one `#`;
- a link to another section becomes a link to that section's page, and a link to a file of the
  plugin becomes its address on GitHub;
- lists inside lists, and tables and code inside a list item, are indented by four spaces where
  GitHub accepts two (the guide's markdown reader needs four);
- the rows of a table all get the indent of its first row;
- the inbox, one long bullet of the tree view's list, becomes a page of its own.
"""
import os
import re
import sys
from pathlib import Path

REPO = "https://github.com/alex-pv01/rft-plugin"
DOCS = Path(__file__).resolve().parent.parent / "docs"

INTRO = "(the opening)"
INBOX = "(the inbox, from The tree view)"

# page, its title when it joins several sections (None: the section's own heading), the sections
PAGES = [
    ("using/once-active.md", None, ["What changes once it is active"]),
    ("using/tree-view.md", None, ["The tree view"]),
    ("using/inbox.md", "The inbox and reading notes", [INBOX]),
    ("using/agents.md", None, ["Agents"]),
    ("using/kanban.md", None, ["The kanban and priorities"]),
    ("using/calendar.md", None, ["Deadlines, meetings and the calendar"]),
    ("using/queue.md", None, ["The experiment queue"]),
    ("using/concepts.md", "Concepts and artifacts", ["Concepts", "Concept artifacts"]),
    ("using/code-repos.md", None, ["Code repos"]),
    ("using/notebooks-figures.md", "Notebooks and figures", ["Experiment notebooks", "Figures"]),
    ("using/documents.md", None, ["Snippets and documents"]),
    ("using/slides.md", None, ["Slides"]),
    ("using/handoffs.md", None, ["Handoffs: carrying on in a new session"]),
    ("reference/commands.md", None, ["Commands"]),
    ("reference/statuses.md", None, ["Statuses"]),
    ("reference/configuration.md", None, ["Configuration"]),
    ("reference/obsidian.md", None, ["Obsidian, if you use it"]),
]
# sections that do not come here: where they go instead
ELSEWHERE = {
    INTRO: "written anew: the guide's first page and the short README",
    "Usage": "a heading with no text of its own",
    "Install": "written anew: start/install.md",
    "Activate it in a project": "written anew: start/activate.md",
    "The notes in one folder, the code in others": "written anew: start/notes-and-code.md",
    "Development": "CONTRIBUTING.md in the plugin's repository",
    "License": "the short README",
}

# sections written anew: where a link to one of them leads
NEW_PAGES = {
    "Install": "start/install.md",
    "Activate it in a project": "start/activate.md",
    "The notes in one folder, the code in others": "start/notes-and-code.md",
}

# a fence opens or closes a code block; a line that starts with backticks and has more of them
# further on is `code` in the text, not a fence
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})[^`]*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
MARKER = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
LINK = re.compile(r"(\]\()([^)\s]+)(\))")


def slug(title):
    """GitHub's anchor for a heading."""
    s = re.sub(r"[^\w\- ]", "", title.lower())
    return s.replace(" ", "-")


def sections(text):
    """The README as (level, title, lines), cut at its headings of level 2 and 3 outside code."""
    out, cur, fence = [], [0, INTRO, []], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fence = not fence
        m = None if fence else HEADING.match(line)
        if m and 2 <= len(m.group(1)) <= 3:
            out.append(tuple(cur))
            cur = [len(m.group(1)), m.group(2), []]
        else:
            cur[2].append(line)
    out.append(tuple(cur))
    return out


def take_inbox(lines):
    """The tree view's inbox bullet, taken out: (the section without it, the bullet as paragraphs)."""
    start = next((i for i, l in enumerate(lines) if l.startswith("- **The inbox**")), None)
    if start is None:
        sys.exit("The tree view has no bullet that starts with '- **The inbox**': place the inbox's text by hand.")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("- ") or (lines[i].strip() and not lines[i].startswith(" "))), len(lines))
    bullet = lines[start:end]
    while bullet and not bullet[-1].strip():
        bullet.pop()
    plain = [bullet[0][2:]] + [l[2:] if l.startswith("  ") else l for l in bullet[1:]]
    pointer = ["- **The inbox** (the tray icon beside the scratchpad's) has a page of its own:", "  [The inbox and reading notes](#inbox-page)."]
    return lines[:start] + pointer + lines[end:], plain


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def fix_tables(lines):
    """The rows of a table all at the indent of its first row. In the README some rows of the
    tools' table start at the margin and the others two spaces in, and GitHub ends the table at
    the first of them."""
    lines, i = list(lines), 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            first = indent_of(lines[i])
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                lines[i] = " " * first + lines[i].lstrip()
                i += 1
        else:
            i += 1
    return lines


def unescape_pipes(lines):
    """In a table, GitHub wants a | inside `code` written as \\|; the guide's reader wants it bare."""
    out = []
    for line in lines:
        if line.lstrip().startswith("|"):
            parts = re.split(r"(`[^`]*`)", line)
            line = "".join(p.replace("\\|", "|") if p.startswith("`") else p for p in parts)
        out.append(line)
    return out


def reindent(lines):
    """Four spaces where GitHub accepts two: lists in lists, and blocks inside a list item."""
    lines = unescape_pipes(fix_tables(lines))
    out, i, fresh = [], 0, True          # fresh: the line starts a block (after a blank line)
    depth, block = None, 0               # the list item we are in, or the indent of a plain block
    in_list = False                      # a list is open above (so an indented block is its child)
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            out.append("")
            fresh, i = True, i + 1
            continue
        f = FENCE.match(line)
        if f:
            k = len(f.group(1)) if in_list else 0
            j = i + 1
            while j < len(lines) and not (FENCE.match(lines[j]) and lines[j].strip() == f.group(2)):
                j += 1
            for l in lines[i:j + 1]:
                out.append((" " * k + l) if l.strip() else l)
            if not len(f.group(1)):
                in_list = False
            fresh, i = True, j + 1
            continue
        ind = indent_of(line)
        m = MARKER.match(line)
        if m:
            if block is not None and not fresh:
                # the item above ended with a block of its own: its reader needs a blank line here
                out.append("")
            depth = ind // 2
            out.append(" " * (4 * depth) + line.lstrip())
            in_list, block = True, None
        elif ind == 0:
            if fresh:
                in_list, depth = False, None
            out.append(line)
            block = None
        elif fresh or (block is None and depth is None):
            # a paragraph or a table inside a list item, after a blank line
            block = 2 * ind if in_list else ind
            depth = None
            out.append(" " * block + line.lstrip())
        elif block is not None:
            out.append(" " * block + line.lstrip())
        else:
            # the next line of a list item's own text
            out.append(" " * (4 * depth + 2) + line.lstrip())
        fresh, i = False, i + 1
    # a list or a table needs a blank line above it
    spaced = []
    fence = False
    for n, line in enumerate(out):
        if FENCE.match(line):
            fence = not fence
        prev = spaced[-1] if spaced else ""
        if not fence and prev.strip() and not FENCE.match(line):
            starts_list = MARKER.match(line) and indent_of(line) == 0 and not MARKER.match(prev) and indent_of(prev) == 0
            starts_table = line.lstrip().startswith("|") and not prev.lstrip().startswith("|")
            if starts_list or starts_table:
                spaced.append("")
        spaced.append(line)
    return spaced


def relevel(lines, shift):
    out, fence = [], False
    for line in lines:
        if FENCE.match(line):
            fence = not fence
        m = None if fence else HEADING.match(line)
        if m:
            out.append("#" * max(1, len(m.group(1)) - shift) + " " + m.group(2))
        else:
            out.append(line)
    return out


def relink(lines, page, anchors):
    """Links between sections become links between pages; the plugin's files, their GitHub address."""
    here = os.path.dirname(page)

    def swap(m):
        target = m.group(2)
        if target == "#inbox-page":
            return m.group(1) + os.path.relpath("using/inbox.md", here) + m.group(3)
        if target.startswith("#"):
            if target[1:] not in anchors:
                sys.exit(f"{page}: a link to {target}, which is no section of the README.")
            dest, anchor = anchors[target[1:]]
            if dest is None:
                sys.exit(f"{page}: a link to {target}, a section that does not come to the guide.")
            rel = os.path.relpath(dest, here)
            return m.group(1) + rel + (f"#{anchor}" if anchor else "") + m.group(3)
        if re.match(r"^(https?:|mailto:)", target) or target in ("…", "path/to/fig.png"):
            return m.group(0)
        kind = "tree" if "." not in os.path.basename(target) else "blob"
        return m.group(1) + f"{REPO}/{kind}/main/{target}" + m.group(3)

    out, fence = [], False
    for line in lines:
        if FENCE.match(line):
            fence = not fence
            out.append(line)
        elif fence:
            out.append(line)
        else:
            # not inside `code`
            parts = re.split(r"(`[^`]*`)", line)
            out.append("".join(p if p.startswith("`") else LINK.sub(swap, p) for p in parts))
    return out


def main():
    readme = Path(sys.argv[1] if len(sys.argv) > 1 else "../rft-plugin/README.md")
    secs = sections(readme.read_text())
    by_title = {}
    for level, title, lines in secs:
        if title in by_title:
            sys.exit(f"The README has two sections called '{title}'.")
        by_title[title] = (level, lines)

    placed = {t for _, _, ts in PAGES for t in ts} | set(ELSEWHERE)
    unknown = [t for t in by_title if t not in placed]
    if unknown:
        sys.exit("The README has sections this script does not place: " + "; ".join(unknown)
                 + ".\nAdd each to PAGES (and to the navigation in zensical.toml) or to ELSEWHERE.")
    missing = [t for t in placed if t not in by_title and t != INBOX]
    if missing:
        sys.exit("Sections this script expects are gone from the README: " + "; ".join(missing))

    level, tree = by_title["The tree view"]
    rest, inbox = take_inbox(tree)
    by_title["The tree view"] = (level, rest)
    by_title[INBOX] = (level + 1, inbox)

    # where a link to a section's anchor leads: its page, and an anchor when the page joins sections
    anchors = {}
    for page, title, titles in PAGES:
        for t in titles:
            if t != INBOX:
                anchors[slug(t)] = (page, slug(t) if title else "")
    for t, page in NEW_PAGES.items():
        anchors[slug(t)] = (page, "")
    for t in ELSEWHERE:
        anchors.setdefault(slug(t), (None, ""))

    for page, title, titles in PAGES:
        body = []
        if title:
            body += [f"# {title}", ""]
        for t in titles:
            level, lines = by_title[t]
            lines = list(lines)
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            if t == INBOX:
                body += lines + [""]
                continue
            shift = level - (2 if title else 1)
            body += ["#" * (2 if title else 1) + " " + t, ""] + relevel(lines, shift) + [""]
        body = relink(reindent(body), page, anchors)
        while body and not body[-1].strip():
            body.pop()
        path = DOCS / page
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(body) + "\n")
        print(f"{page}: {len(body)} lines")


if __name__ == "__main__":
    main()
