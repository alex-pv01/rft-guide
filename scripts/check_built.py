"""Every picture and every local link of the built site leads to a file that is there.

    zensical build --clean --strict && python3 scripts/check_built.py

The strict build already stops on a link to a page or an anchor that does not exist. It does not
notice a missing picture, so this does, and looks at the links a second time.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import tomllib

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
# the site is served under a folder of its address (/rft-guide/): the 404 page names its files from there
BASE = urlsplit(tomllib.loads((ROOT / "zensical.toml").read_text())["project"]["site_url"]).path


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("src", "href"):
            if a.get(key) and tag in ("img", "a", "link", "script", "source", "video"):
                self.refs.append((tag, a[key]))


def main():
    if not SITE.is_dir():
        sys.exit("No site/ folder: build the site first.")
    missing, pages, pictures = [], 0, 0
    for page in sorted(SITE.rglob("*.html")):
        pages += 1
        r = Refs()
        r.feed(page.read_text())
        for tag, ref in r.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc or not u.path:
                continue
            path = unquote(u.path)
            if path.startswith("/"):
                if not path.startswith(BASE):
                    missing.append(f"{page.relative_to(SITE)}: {tag} {ref} (outside {BASE})")
                    continue
                target = SITE / path[len(BASE):]
            else:
                target = page.parent / path
            if target.is_dir():
                target = target / "index.html"
            pictures += tag == "img"
            if not target.exists():
                missing.append(f"{page.relative_to(SITE)}: {tag} {ref}")
    for m in missing:
        print("MISSING", m)
    print(f"{pages} pages, {pictures} pictures, {len(missing)} missing.")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
