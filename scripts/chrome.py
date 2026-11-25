"""Headless Chromium over the DevTools protocol, for the guide's screenshots.

It needs Chromium (Playwright's under ~/.cache/ms-playwright, one on PATH, or RFT_CHROME) and the
websocket-client module. The plugin's own page tests drive Chromium the same way.
"""
import base64, glob, json, os, shutil, socket, subprocess, tempfile, time, urllib.request
from pathlib import Path

import websocket


def find_chrome():
    if os.environ.get("RFT_CHROME"):
        return os.environ["RFT_CHROME"]
    found = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")))
    if found:
        return found[-1]
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        if shutil.which(name):
            return shutil.which(name)
    raise SystemExit("No Chromium found: install Playwright's, or set RFT_CHROME to a Chromium binary.")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Chrome:
    """One page of a fixed size. `scheme` is what the page is told the system prefers."""

    def __init__(self, width=1280, height=800, scheme="light", scale=2):
        self.port = free_port()
        self.profile = tempfile.mkdtemp(prefix="rft-guide-chrome-")
        self.proc = subprocess.Popen(
            [find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--no-first-run", "--hide-scrollbars", "--lang=en-US",
             f"--remote-debugging-port={self.port}", f"--user-data-dir={self.profile}",
             f"--window-size={width},{height}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            # dates and numbers as an English reader sees them, whatever this machine's language
            env={**os.environ, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8", "LANGUAGE": "en_US"})
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json"))
                page = next(t for t in tabs if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise SystemExit("Chromium did not start.")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.n = 0
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=scale, mobile=False)
        self.call("Emulation.setEmulatedMedia", features=[{"name": "prefers-color-scheme", "value": scheme}])

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def js(self, expression):
        r = self.call("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(f"{expression[:80]}: {r['exceptionDetails'].get('exception', {}).get('description')}")
        return r["result"].get("value")

    def open(self, url, ready="document.readyState === 'complete'", wait=10):
        self.call("Page.navigate", url=url)
        self.wait(ready, wait)

    def wait(self, condition, seconds=10):
        end = time.time() + seconds
        while time.time() < end:
            try:
                if self.js(f"!!({condition})"):
                    return
            except RuntimeError:
                pass
            time.sleep(0.1)
        raise SystemExit(f"Waited {seconds}s and this never held: {condition}")

    def drag(self, x1, y1, x2, y2, steps=8):
        """Press at one point of the page, move to another and let go, as a hand on a mouse does."""
        self.call("Input.dispatchMouseEvent", type="mouseMoved", x=x1, y=y1)
        self.call("Input.dispatchMouseEvent", type="mousePressed", x=x1, y=y1, button="left", clickCount=1)
        for k in range(1, steps + 1):
            self.call("Input.dispatchMouseEvent", type="mouseMoved", x=x1 + (x2 - x1) * k / steps, y=y1 + (y2 - y1) * k / steps, button="left")
        self.call("Input.dispatchMouseEvent", type="mouseReleased", x=x2, y=y2, button="left", clickCount=1)

    def capture(self):
        return base64.b64decode(self.call("Page.captureScreenshot", format="png")["data"])

    def shot(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(self.capture())

    def close(self):
        try:
            self.ws.close()
        finally:
            self.proc.terminate()
            self.proc.wait(timeout=10)
            shutil.rmtree(self.profile, ignore_errors=True)
