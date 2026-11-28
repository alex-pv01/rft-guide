"""Retake the guide's screenshots from the plugin's demo project.

    python3 scripts/shots.py [the plugin's folder, default ../rft-plugin] [--only NAME ...]

Every picture in the guide and in the plugin's README comes from here, so that when the page's look
changes they are retaken with one command and not by hand. It serves a copy of `examples/demo` with
the plugin's own server, opens it in headless Chromium at a fixed size in the light theme, brings
each view up with the clicks a person would make, and saves it under docs/images/.

A new picture is one more entry in SHOTS: its name and the steps (JavaScript run in the page) that
lead to it from a fresh start.
"""
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import procs
from chrome import Chrome

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "images"
WIDTH, HEIGHT = 1200, 900

# clicks as a person makes them
CLICK_NODE = "(id => [...document.querySelectorAll('#canvas g.node')].find(g => g.__data__.data.id === id).dispatchEvent(new MouseEvent('click', {bubbles: true})))"
TICK_TAG = "(tag => [...document.querySelectorAll('#filters label')].find(l => l.textContent.trim().startsWith(tag + ' ')).querySelector('input').click())"

SHOTS = [
    # name, steps, what must hold before the picture is taken
    ("tree", [], "document.querySelectorAll('#canvas g.node').length > 10"),
    # the note opens over the right of the window: the tree is dragged left, into what is left of it
    ("note", [CLICK_NODE + "('E05')"], "!document.getElementById('drawer').hidden && document.querySelector('#note h1, #note h2, #note p')",
     [("drag", 300, 150, 60, 150)]),
    ("filters", ["document.getElementById('filters-toggle').click()", TICK_TAG + "('augmentation')"],
     "!document.getElementById('filters').hidden && !document.getElementById('filter-status').hidden"),
    ("regions", ["document.getElementById('cmode').click()"], "/regions/.test(document.getElementById('cmode').title.split('(')[0])"),
    ("arrows", ["document.getElementById('cmode').click()", "document.getElementById('cmode').click()"],
     "/arrows/.test(document.getElementById('cmode').title.split('(')[0])"),
    ("concept-tree", ["document.querySelector('button[data-show=\"concepts\"]').click()"],
     "!document.getElementById('concept-canvas').hidden && document.querySelectorAll('#concept-canvas .cnode').length > 1"),
]


def main():
    args = sys.argv[1:]
    only = []
    if "--only" in args:
        k = args.index("--only")
        only, args = args[k + 1:], args[:k]
    plugin = Path(args[0] if args else ROOT.parent / "rft-plugin").resolve()
    if not (plugin / "server" / "rft_server.py").exists():
        sys.exit(f"{plugin} is not the plugin's folder (no server/rft_server.py).")

    tmp = procs.folder("rft-guide-shots-")
    shutil.copytree(plugin / "examples" / "demo", tmp / "demo")
    server = procs.start(
        [sys.executable, str(plugin / "server" / "rft_server.py"), "--vault", str(tmp / "demo" / "vault"), "--web", str(plugin / "web"),
         "--port", "0", "--project", "small-data-regularisation", "--no-watch"],
        # the page with no agents set up, whatever ~/.config/rft/agents.toml holds on the machine the pictures are taken on
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env={**os.environ, "RFT_AGENTS": str(tmp / "no-agents.toml")})
    chrome = None
    try:
        url = re.search(r"RFT_SERVER_URL (\S+)", server.stdout.readline()).group(1)
        chrome = Chrome(WIDTH, HEIGHT, scheme="light", scale=2)
        for name, steps, ready, *rest in SHOTS:
            if only and name not in only:
                continue
            # each picture from a fresh start: the page remembers which panels were open
            chrome.open(url, ready="document.querySelectorAll('#canvas g.node').length > 10")
            chrome.js("localStorage.clear(); localStorage.setItem('rft:theme', 'light')")
            chrome.open(url, ready="document.querySelectorAll('#canvas g.node').length > 10")
            time.sleep(0.8)
            for step in steps:
                chrome.js(step)
                time.sleep(0.5)
            chrome.wait(ready)
            # the whole tree in the window: the Fit button, when it is the one on offer (its other
            # state centres on the root)
            chrome.js("(b => !document.getElementById('canvas').hidden && /^Fit/.test(b.title) && b.click())(document.getElementById('fit'))")
            time.sleep(0.8)
            # what is done once the tree is in place: a drag, as ("drag", from x, from y, to x, to y)
            for step in (rest[0] if rest else []):
                if step[0] == "drag":
                    chrome.drag(*step[1:])
                time.sleep(0.5)
            # the page animates a change of view and loads a note after the click: the picture is
            # taken when two captures in a row are the same, byte for byte
            last = None
            for _ in range(30):
                time.sleep(0.5)
                now = chrome.capture()
                if now == last:
                    break
                last = now
            else:
                sys.exit(f"{name}: the page never came to rest.")
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"{name}.png").write_bytes(now)
            print(f"docs/images/{name}.png")
    finally:
        if chrome:
            chrome.close()
        procs.stop(server)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
