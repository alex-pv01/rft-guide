# Configuration

`.rft/config.json`:

```json
{ "version": 2, "vault": "vault", "project": "my-project", "canvas": true, "mermaid": false,
  "lastId": { "E": 12, "D": 9 }, "webPort": 0, "requireRefs": true, "gpus": 2,
  "runsDir": "/data/rft-runs" }
```

`version` is the vault's format, not the plugin's: it changes only when what a vault holds
changes, and `/rft-update` brings a vault of an older format up to date. `mermaid: true` also writes `Reasoning tree (diagram).md`, a Mermaid flowchart Obsidian draws
natively. `lastId` keeps ids from being reused after a note is deleted. `webPort` fixes the
tree view's port (0: a free one), handy for a standing `ssh -L` forward. `requireRefs: true`
(set by `/rft-init` on a new vault, off on an adopted one) makes `rft_validate` warn about
experiments and directions in work that name no reference. `gpus` is how many GPUs the
experiments share: the Calendar and `rft_next` report the days the planned and running ones need
more. `runsDir` is the outputs' root `/rft-machine add` suggests (absolute, `~/…`, or from the
tree's folder), e.g. a data drive; once a machine is paired, its own root (in
`.queue/machine.json`, chosen then) is where the queue's runs keep their outputs, by repo
(`<root>/<repo>/<experiment>/<job>`). A config that holds
only `tree` is a link to a tree in another folder (see above). The code a concept runs on is
linked in its note, not in the config (see Code repos).
