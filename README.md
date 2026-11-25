# rft-guide

The guide to [rft](https://github.com/alex-pv01/rft-plugin), the Reasoning Flow Tree plugin for
Claude Code: how to install it and how to use it. It is published at
<https://alex-pv01.github.io/rft-guide/>.

The guide is kept apart from the plugin so that installing the plugin does not copy the guide's
pages and screenshots to every user's machine.

## Build it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve            # a local copy that reloads as you edit
.venv/bin/zensical build --clean --strict   # what is published; fails on a broken link
```

The pages are plain markdown under `docs/`, and `zensical.toml` holds the navigation. A push to
`main` publishes the site (`.github/workflows/publish.yml`).

## Where things are

- `docs/stylesheets/rft.css`: the colours of rft's own page, copied from the plugin's
  `web/app.css`. A change to the page's palette is made in both places.
- `scripts/shots.py`: retakes every screenshot under `docs/images/` from the plugin's demo project
  (`examples/demo`), in headless Chromium at 1440 × 900 in the light theme. Run it when the page's
  look changes; a new picture is one more entry in its `SHOTS` list. Two runs give the same files.
- `scripts/chrome.py`: headless Chromium, for the screenshots.
- `scripts/check_built.py`: every picture and local link of the built site leads to a file. The
  strict build stops on a broken link; it does not notice a missing picture.
- `scripts/split_readme.py` and `scripts/check_move.py`: for the move out of the plugin's long
  README only. The first writes the pages from it; the second checks that no paragraph was lost
  and that each page reads as the README did on GitHub (`pip install -r requirements-dev.txt`).
  Both are deleted once the pages here are the source.

## When the plugin changes

A change to what a person sees or types in rft is finished when the page here that describes it
is changed too.
