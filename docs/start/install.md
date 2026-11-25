# Install

## What you need

- **Claude Code**, version 2.1.29x or later. rft uses a kind of plugin (a hooks module with a
  skill) that older versions do not load.
- **Python 3** on your `PATH` (`python3` or `python`), standard library only. The tree view in
  the browser is served by a small local server written in Python. Without Python the notes and
  everything else still work, and `/rft` tells you the view is not available.

## Install the plugin

At the prompt of a Claude Code session in the terminal, type:

```
/plugin marketplace add alex-pv01/rft-plugin
/plugin install rft@rft-plugin
```

The first line tells Claude Code where the plugin lives; the second installs it. If you are
asked for a scope, choose **user** to have rft in every project. It does nothing in a project
until you activate it there.

## Check that it is installed

Start a new session in any folder and type `/rft`. The answer

```
RFT is not active in this project. Run /rft-init [starting question] to set it up.
```

comes from the plugin, so it is installed. Now take the
[first run on the demo](first-run.md), or [activate it in your project](activate.md).

!!! note "In the desktop app"
    The plugin registers its commands when a session starts, so the app's slash-command menu may
    not list them. Type `/rft` in full and it runs.
