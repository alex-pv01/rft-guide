"""Two checks on the move of the plugin's README into the guide. Neither asks anyone's opinion.

    python3 scripts/check_move.py [README] [--also FILE ...]

1. Nothing lost. Every paragraph, list item, table row and code block of the README is looked for
   in the guide's pages (and in the files after --also: the short README, CONTRIBUTING.md). A piece
   that is not found is printed and the check fails. A section that was written anew on purpose is
   named in split_readme.ELSEWHERE or in REWRITTEN below; its pieces are counted and said, not
   silently passed.
2. Same on the page. Each moved section is drawn twice: by GitHub's own markdown reader (cmark-gfm,
   what the README's readers saw) and by the guide's (the built site). The two must have the same
   words in the same order and the same number of list items, lists, tables, rows, code blocks,
   links and so on. This catches a list that lost its nesting or a table that became text.
   It needs the site built (`zensical build`) and `pip install -r requirements-dev.txt`.

For the move only, like split_readme.py: once the pages are rewritten one by one they stop
matching the old README on purpose, and this script is deleted.
"""
import difflib
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import split_readme as S

ROOT = Path(__file__).resolve().parent.parent
# sections whose page in the guide was written anew after the move: section -> why
REWRITTEN = {}

MARKER = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


def plain(line):
    line = line.strip()
    line = re.sub(r"^#{1,6}\s+", "", line)
    line = MARKER.sub("", line)
    return line


def squash(text):
    text = re.sub(r"\]\([^)\s]*\)", "]()", text)
    text = text.replace("\\|", "|")    # a | in a table's `code`, written \\| for GitHub
    return re.sub(r"\s+", " ", text).strip()


def pieces(lines):
    """Paragraphs, list items, table rows and code blocks, each as one normalised string."""
    out, cur, i = [], [], 0

    def flush():
        if cur:
            out.append(squash(" ".join(cur)))
            cur.clear()

    while i < len(lines):
        line = lines[i]
        f = S.FENCE.match(line)
        if f:
            flush()
            j = i + 1
            while j < len(lines) and not (S.FENCE.match(lines[j]) and lines[j].strip() == f.group(2)):
                j += 1
            out.append(squash(" ".join(plain(l) for l in lines[i:j + 1])))
            i = j + 1
            continue
        if not line.strip():
            flush()
        elif line.lstrip().startswith("|"):
            flush()
            out.append(squash(line.strip()))
        elif MARKER.match(line) or S.HEADING.match(line):
            flush()
            cur.append(plain(line))
        else:
            cur.append(line.strip())
        i += 1
    flush()
    return [p for p in out if p]


def haystack(paths):
    text = []
    for p in paths:
        text += [plain(l) for l in Path(p).read_text().split("\n")]
    return squash(" ".join(text))


def nothing_lost(readme, also):
    pages = sorted((ROOT / "docs").rglob("*.md"))
    hay = haystack(pages + [Path(a) for a in also])
    lost, excused, total = [], Counter(), 0
    for level, title, lines in S.sections(Path(readme).read_text()):
        for piece in pieces(lines):
            total += 1
            if piece in hay:
                continue
            if title in REWRITTEN or title in S.ELSEWHERE:
                excused[title] += 1
            else:
                lost.append((title, piece))
    print(f"Nothing lost: {total} pieces of the README, {total - len(lost) - sum(excused.values())} found as written.")
    for title, n in excused.items():
        why = REWRITTEN.get(title) or S.ELSEWHERE[title]
        print(f"  not looked for as written: {n} pieces of '{title}' ({why})")
    for title, piece in lost:
        print(f"  LOST from '{title}': {piece[:160]}")
    return not lost


COUNTED = ["li", "ul", "ol", "table", "tr", "th", "td", "pre", "code", "strong", "em", "a", "img", "blockquote", "hr", "h"]


class Shape(HTMLParser):
    """The words and the counted elements of a piece of HTML (of the <article> when there is one)."""

    def __init__(self, article):
        super().__init__(convert_charrefs=True)
        self.inside, self.depth, self.article = (not article), 0, article
        self.counts, self.text, self.skip, self.lists, self.deepest = Counter(), [], 0, 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.article and tag == "article":
            self.inside = True
        if not self.inside:
            return
        cls = a.get("class") or ""
        # what the theme adds around the text: the link sign beside a heading, the code's line anchors
        if self.skip or (tag == "a" and ("headerlink" in cls or (a.get("id", "").startswith("__") and "href" not in a))) or tag in ("button", "nav"):
            if tag not in ("br", "img", "hr", "input"):
                self.skip += 1
            return
        if tag in ("ul", "ol"):
            self.lists += 1
            self.deepest = max(self.deepest, self.lists)
        key = "h" if re.fullmatch(r"h[1-6]", tag) else tag
        if key in COUNTED:
            self.counts[key] += 1

    def handle_endtag(self, tag):
        if self.article and tag == "article":
            self.inside = False
        if not self.inside:
            return
        if self.skip:
            self.skip -= 1
            return
        if tag in ("ul", "ol"):
            self.lists -= 1

    def handle_data(self, data):
        if self.inside and not self.skip:
            self.text.append(data)

    def words(self):
        return "".join(self.text).split()


def shape(html, article):
    s = Shape(article)
    s.feed(html)
    s.counts["deepest list"] = s.deepest
    return s


def same_on_the_page(readme):
    import cmarkgfm

    by_title = {t: (lv, ls) for lv, t, ls in S.sections(Path(readme).read_text())}
    level, tree = by_title["The tree view"]
    rest, inbox = S.take_inbox(tree)
    by_title["The tree view"] = (level, rest)
    ok = True
    for page, title, titles in S.PAGES:
        if any(t in REWRITTEN for t in titles):
            print(f"  {page}: written anew, not compared")
            continue
        src = []
        if title:
            src += [f"# {title}", ""]
        for t in titles:
            if t == S.INBOX:
                src += inbox + [""]
            else:
                # the README's one broken table is mended on both sides (see split_readme.fix_tables)
                src += [f"## {t}", ""] + S.fix_tables(by_title[t][1]) + [""]
        github = shape(cmarkgfm.github_flavored_markdown_to_html("\n".join(src)), article=False)
        built = ROOT / "site" / page[:-3] / "index.html"
        if not built.exists():
            sys.exit(f"{built} is not there: build the site first (zensical build --clean).")
        guide = shape(built.read_text(), article=True)
        problems = []
        for key in COUNTED + ["deepest list"]:
            if github.counts[key] != guide.counts[key]:
                problems.append(f"{key}: {github.counts[key]} on GitHub, {guide.counts[key]} in the guide")
        gw, hw = github.words(), guide.words()
        # the same characters in the same order, whatever the spacing (a code block's colours cut
        # its text into parts)
        gc, hc = "".join(gw), "".join(hw)
        if gc != hc:
            sm = difflib.SequenceMatcher(None, gc, hc, autojunk=False)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != "equal":
                    problems.append(f"text differs after '{gc[max(0, a1 - 40):a1]}': GitHub has '{gc[a1:a2][:80]}', the guide '{hc[b1:b2][:80]}'")
                    if len(problems) > 8:
                        break
        if problems:
            ok = False
            print(f"  {page}: DIFFERS")
            for p in problems[:9]:
                print(f"    {p}")
        else:
            print(f"  {page}: the same ({len(gw)} words, {guide.counts['li']} list items, {guide.counts['tr']} table rows, {guide.counts['pre']} code blocks)")
    return ok


def main():
    args = sys.argv[1:]
    also = []
    if "--also" in args:
        k = args.index("--also")
        also, args = args[k + 1:], args[:k]
    readme = args[0] if args else "../rft-plugin/README.md"
    a = nothing_lost(readme, also)
    print("Same on the page:")
    b = same_on_the_page(readme)
    if not (a and b):
        sys.exit(1)
    print("Both checks passed.")


if __name__ == "__main__":
    main()
