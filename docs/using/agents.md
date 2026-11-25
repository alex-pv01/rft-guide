# Agents

rft was made for Claude Code, and Claude Code is still what manages the tree. But some of the
work can go to other agents that you set up: a model on your own machine for a quick comment
on a paragraph, another provider's model, another harness. You list them once, in a file of
your own, and pick beside the button who does a task. With no such file nothing changes: the
page has the connected Claude Code chat alone, as before.

An **agent** is one of two things:

- a **model** answers text with text. It reads nothing and changes nothing: the page's server
  gives it the thread and the text it is on, and writes its answer. Any endpoint that speaks
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

The setup is `~/.config/rft/agents.toml` (or the file `RFT_AGENTS` names). It is yours, not the
project's: a vault holds no agent list and no key. It is read again whenever it changes.

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

`kind = "claude-code"` and `kind = "codex"` are ready-made harness entries (`model = "..."`
picks the model). The Claude Code one was tried: locked, it has its reading tools and the web,
and cannot write a file. **The Codex one has never run a task**: its flags are those Codex's
own help lists (its read-only sandbox, live web search), but that it truly cannot write when
locked was not checked, and the page marks it so.

In the page, a picker stands beside the buttons that ask: above a note's threads and the
Manuscript's (**Answers by**), and above the inbox's list (**Process with**). It lists the
connected Claude Code chat and your agents, says of each where it runs (*runs on this machine*,
or *sends text to* the host it is sent to), and leaves out of reach, with the reason, those
that may not take the task. Your pick is kept for the next time; before you pick, the chat is
used when one is connected, else your default. While an agent you launched is at a thread or
an item, its row says so, with **Cancel**; one at a time per thread or item, and a time limit.
An answer that never came, or that could not be used, changes nothing in the vault and says
why on the row until you ask again.

What an answer becomes is fixed, and `tests/fixtures/agents/SCENARIOS.md` lists the cases: a
suggestion's new text must stand between `<replacement>` and `</replacement>`, and anything
else is a plain reply, never a replacement; Process saves the impression and the three-line
brief together or saves nothing.

**What still needs a Claude Code chat**: everything that manages the tree (**Add child**,
**Change type**, **Move**, **Verify**, the Manuscript's changes, every `/rft-` command) and
the inbox's **Discuss**, which is a conversation with you. With the view
[served from a terminal](tree-view.md) and no chat, threads and Process go to your agents and
those are refused, saying so.
