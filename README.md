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
- `scripts/chrome.py`: headless Chromium, for the screenshots.

## When the plugin changes

A change to what a person sees or types in rft is finished when the page here that describes it
is changed too.
