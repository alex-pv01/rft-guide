# Agents

rft was made for Claude Code, and Claude Code is still what manages the tree. But some of the
work can go to other agents that you set up: a model on your own machine for a quick comment
on a paragraph, another provider's model, another harness. You set them up once, from the page
or in a file of your own, and pick beside the button who does a task. Until you do, nothing
changes: the page has the connected Claude Code chat alone, with **Agents…** in its top bar and
one small **Set up an agent** where the picker will stand.

An **agent** is one of two things:

- a **model** answers text with text. It reads nothing and changes nothing: the page's server
  sends it the thread and the text of the note it is on (so that text goes where the model
  runs), and writes its answer. Any endpoint that speaks
  the OpenAI chat format is one (Ollama, llama.cpp, vLLM, DeepSeek, GLM, OpenAI);
- a **harness** can act: read the project, use tools. Claude Code is one, Codex another. The
  server runs it once for a task, without a chat, in the vault's folder.

Each agent has a **grant**, which you give it and which is never worked out from the model's
name:

| `grant` | It may | So it is offered |
|---|---|---|
| `"text"` (the default; all a model can have) | answer text with text | a comment or suggestion thread |
| `"read"` | also read the project | the same, and **Process** when it can read the web |
| `"change"` | also change the project | the same; nothing more yet |

A harness below `"change"` is run with its **locked** command: the one that switches off its
own writing and shell tools. A harness with no locked command is not run below `"change"` at
all. Whatever the grant, for these tasks the agent only answers: the server writes the reply
into the thread, or the impression and the brief onto the inbox item, signed with the agent's
name, and a suggestion's new text still waits for you to accept it.

## Setting agents up

The setup is one file, `~/.config/rft/agents.toml` (or the file `RFT_AGENTS` names). It is
yours, not the project's: a vault holds no agent list and no key. It is read again whenever it
changes, so nothing is restarted. You can fill it from the page or write it yourself.

**From the page.** **Agents…** in the top bar opens the setup (on a phone it is in the menu
behind ⋯). It is shown on the page opened with the address `/rft` printed, which carries the
vault's key: a page without the key may not change the setup. The same way in stands where the
picker stands, above the threads of a note that has an open one and above an inbox that has
items: a small **Set up an agent**, which reads **Agents…**, beside the picker, once you have
an agent. The setup lists your agents and adds, changes or removes one at a time, writing the
file for you and leaving every other line of it as it is, your comments included.

- **A model**: give it a name and say where it is. Nothing is assumed: type the address its
  server prints, ending in `/v1` (for Ollama on the same machine that is usually
  `http://localhost:11434/v1`). **List its models** asks the endpoint which models it has, and
  you pick one. To use another model later, **Change** the agent.
- **A key** is never typed there, only the name of the environment variable that holds it. A
  key pasted in its place is refused. When the variable is not set where the server runs, the
  agent is saved and shown out of reach, saying so.
- **Claude Code and Codex** are added the same way: pick one under *What it is*, and its grant.
- **Remove** takes two presses. A removed agent is no longer anyone's default.
- A harness of your own, by its commands, is not added from the page: write it in the file, as
  below. A wrong command there is what would break the lock, so it is yours to type.

A name is fixed once given (remove the agent and add it again to rename it), and the
`[defaults]` are set in the file only.

**By hand.** The same file, written out:

```toml
[defaults]
thread = "qwen"            # who answers a thread unless you pick another
process = "claude"         # who processes an inbox item

[agents.qwen]              # a model on this machine, through Ollama
kind = "model"
url = "http://localhost:11434/v1"
model = "qwen3:14b"

[agents.deepseek]          # a model elsewhere: the key is NAMED, never written here
kind = "model"
url = "https://api.deepseek.com/v1"
model = "deepseek-chat"
key = "DEEPSEEK_API_KEY"   # the environment variable that holds it

[agents.claude]            # Claude Code, run once per task, locked: it reads files and the web
kind = "claude-code"
grant = "read"

[agents.other]             # any other harness, by its commands
kind = "harness"
run = ["mytool", "exec", "{prompt}"]                    # the prompt goes where {prompt} stands,
locked = ["mytool", "exec", "--read-only", "{prompt}"]  # or on its input when it stands nowhere
web = true                 # it can read a page on the web: needed for Process
grant = "read"
thread_seconds = 120       # how long it has for a thread (the default) and for Process (600)
process_seconds = 900
```

## The ready-made harnesses

`kind = "claude-code"` and `kind = "codex"` are ready-made harness entries (`model = "..."`
picks the model). Each must be installed and logged in on the machine the server runs on. The Claude Code one was tried: locked, it has its reading tools and the web,
and cannot write a file. The Codex one was tried once, on 2026-11-25: launched locked on a demo
vault, it answered a thread and processed a paper with its web search, and its three attempts to
create a file failed. **On that machine its sandbox could not start at all** (Ubuntu 24.04
restricts the kind of sandbox Codex uses), so it could run no command and read no note either.
That a working read-only sandbox reads the project and cannot write is what Codex's
documentation says; it was not seen here. Where the sandbox cannot start, Codex still answers,
and says in its answer that it could not see the project.

## Picking who does a task

In the page, a picker stands beside the buttons that ask. **Answers by** is in the box where
you write a comment or a suggestion, so the first one of a note can already go to an agent of
yours, and above the open threads, in a note and in a document of the Manuscript alike: it is
one pick, wherever you make it. **Process with** is above the inbox's list. The picker lists
the connected Claude Code chat and your agents, says of each where it runs (*runs on this
machine*, *sends text to* the host a model is sent to, or, for a harness,
*runs here, sends text to its provider*), and leaves out of reach, with the reason, those that
may not take the task. The buttons then name who is picked: **Ask qwen**, **Post and ask qwen**.

Your pick is kept in the browser for the next time. Before you pick, it is the default your
setup names for the task; with none, the chat when one is connected; with no chat either, the
first of your agents that may take it.

While an agent you launched is at a thread or an item, its row says so, with **Cancel**; one at
a time per thread or item, and a time limit (two minutes for a thread, ten for Process, unless
its entry says otherwise). An answer that never came, or that could not be used, changes
nothing in the vault and says why on the row until you ask again. If the server is restarted
while an agent is at a thread, the thread says so and can be asked again.

What an agent wrote carries its name: on its message in a thread, and in the heading of its
impression in a reading note. Claude, in a chat, is told which messages and impressions are
another agent's and not its own.

## What an answer becomes

What an answer becomes is fixed, and `tests/fixtures/agents/SCENARIOS.md` in the plugin lists
the cases: a suggestion's new text must stand between `<replacement>` and `</replacement>`, and
anything else is a plain reply, never a replacement; Process saves the impression and the
three-line brief together or saves nothing (an impression without its five parts or longer
than a screen, a brief that is not three lines, an item the agent could not read).

Process and your own reading: the server never gives a launched agent your part of an item's
[reading note](inbox.md), and tells it not to open the folder that holds it. A locked harness
can still read any file of the vault, so that it does not open yours rests on what it is told,
not on the lock. An item you have marked as read keeps the impression it had.

## What still needs a Claude Code chat

Everything that manages the tree (**Add child**, **Change type**, **Move**, **Verify**, the
Manuscript's changes, every `/rft-` command) and the inbox's **Discuss**, which is a
conversation with you. With the view served from a terminal (`rft_serve.py`, described under
[Concepts and artifacts](concepts.md)) and no chat, threads and Process go to your agents and
those are refused, saying so.
