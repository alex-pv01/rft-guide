"""The Agents page is held to the plugin's own code: its example setup loads, and says what it shows.

    python3 scripts/check_agents.py [the plugin's folder, default ../rft-plugin]

The page (docs/using/agents.md) shows an `agents.toml`. This reads that example with the plugin's
reader (server/rft_agents.py) and checks what the page says about it: which agents it holds, what
each may do, the time limits. It also checks that the page names the things a reader must be told.
It was the plugin's own test of its README's Agents section, moved here with the section.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "rft-plugin").resolve()
if not (PLUGIN / "server" / "rft_agents.py").exists():
    sys.exit(f"{PLUGIN} is not the plugin's folder (no server/rft_agents.py).")
sys.path.insert(0, str(PLUGIN / "server"))
import rft_agents  # noqa: E402


def setup_of(text, env):
    return rft_agents.read_setup(text, Path("agents.toml"), env)


class AgentsPage(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / "docs" / "using" / "agents.md").read_text(encoding="utf-8")

    def test_the_example_setup_loads_as_the_page_says(self):
        (example,) = re.findall(r"```toml\n(.*?)```", self.page, re.S)
        s = setup_of(example, env={"DEEPSEEK_API_KEY": "x"})
        self.assertEqual(s.errors, [])
        d = {a["name"]: a for a in s.describe()["agents"]}
        self.assertEqual(list(d), ["qwen", "deepseek", "claude", "other"])
        self.assertEqual(s.defaults, {"thread": "qwen", "process": "claude"})
        self.assertEqual((d["qwen"]["where"], d["deepseek"]["where"]), ("runs on this machine", "sends text to api.deepseek.com"))
        self.assertEqual([n for n, a in d.items() if "process" in a["tasks"]], ["claude", "other"])
        self.assertEqual(s.agents["other"].limits, {"thread": 120, "process": 900})
        self.assertEqual(s.agents["other"].command()[2], "--read-only")
        self.assertEqual(rft_agents.LIMITS, {"thread": 120, "process": 600})
        # with the key not set, that one agent is out of reach and says why
        self.assertIn("DEEPSEEK_API_KEY is not set", setup_of(example, env={}).agents["deepseek"].problem)

    def test_it_names_the_file_the_grants_and_what_was_never_run(self):
        for said in ("~/.config/rft/agents.toml", "RFT_AGENTS", '`"text"`', '`"read"`', '`"change"`', "never run", "tests/fixtures/agents/SCENARIOS.md", "Discuss"):
            self.assertIn(said, self.page)
        self.assertEqual(rft_agents.UNVERIFIED, ("codex",))
        # nothing of one user's machine
        for word in ("alexpv", "/media/", "/home/"):
            self.assertNotIn(word, self.page)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
