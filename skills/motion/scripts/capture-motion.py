#!/usr/bin/env python3
"""
capture-motion.py — record a running animation to a GIF (or PNG frames).

Why this exists: you cannot judge motion from source code, and you cannot judge it
from a still. This drives headless Chrome over the DevTools protocol, records the
page while it actually animates, and writes a GIF you can look at. Use it on your
own work before shipping, and to produce before/after evidence.

It records whatever really renders — CSS transitions and keyframes, Web Animations,
GSAP/Framer/Motion One, canvas, WebGL — because it captures composited frames rather
than inspecting the DOM.

Usage
-----
  ./capture-motion.py index.html --out motion.gif
  ./capture-motion.py http://localhost:3000 --trigger "document.querySelector('#open').click()"
  ./capture-motion.py demo.html --duration 1500 --fps 30 --width 1200 --height 700
  ./capture-motion.py demo.html --frames-only out/     # skip the GIF, keep PNGs

Options
-------
  --out PATH         output GIF (default motion.gif)
  --duration MS      how long to record after the trigger (default 1200)
  --settle MS        wait after load before triggering (default 400)
  --trigger JS       JavaScript to run to start the animation (e.g. a click)
  --fps N            output frame rate (default 30)
  --width/--height   viewport size (default 900x600)
  --scale N          device scale factor, 2 for retina-crisp output (default 1)
  --frames-only DIR  write PNG frames to DIR and skip GIF assembly
  --chrome PATH      explicit Chrome/Chromium binary
  --keep-frames      don't delete the temporary PNG frames

Requires: Chrome or Chromium, ffmpeg (for GIF output), and websocket-client
          (pip install websocket-client).
"""

import argparse, base64, json, os, shutil, socket, subprocess, sys, tempfile, time
import urllib.request

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def find_chrome(explicit=None):
    if explicit:
        return explicit
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        found = shutil.which(c)
        if found:
            return found
    sys.exit("Could not find Chrome or Chromium. Pass --chrome /path/to/binary.")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def to_url(target):
    if "://" in target:
        return target
    path = os.path.abspath(target)
    if not os.path.exists(path):
        sys.exit(f"No such file: {target}")
    return "file://" + path


class CDP:
    """Minimal DevTools-protocol client: send a command, wait for its reply."""

    def __init__(self, ws_url):
        try:
            import websocket  # websocket-client
        except ImportError:
            sys.exit("Missing dependency: pip install websocket-client")
        self.ws = websocket.create_connection(ws_url, max_size=None, timeout=30)
        self._id = 0
        self.events = []

    def send(self, method, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg)

    def pump(self, timeout):
        """Yield events until `timeout` seconds have passed."""
        deadline = time.time() + timeout
        while True:
            for ev in self.events:
                yield ev
            self.events = []
            remaining = deadline - time.time()
            if remaining <= 0:
                return
            self.ws.settimeout(max(0.05, min(remaining, 1.0)))
            try:
                yield json.loads(self.ws.recv())
            except Exception:
                pass

    def wait_for(self, method, timeout=15):
        deadline = time.time() + timeout
        for ev in self.events:
            if ev.get("method") == method:
                return ev
        self.events = []
        while time.time() < deadline:
            self.ws.settimeout(max(0.05, deadline - time.time()))
            try:
                msg = json.loads(self.ws.recv())
            except Exception:
                continue
            if msg.get("method") == method:
                return msg
        return None

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("target", help="URL or path to an HTML file")
    p.add_argument("--out", default="motion.gif")
    p.add_argument("--duration", type=int, default=1200)
    p.add_argument("--settle", type=int, default=400)
    p.add_argument("--trigger", default=None)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--width", type=int, default=900)
    p.add_argument("--height", type=int, default=600)
    p.add_argument("--scale", type=int, default=1)
    p.add_argument("--frames-only", default=None)
    p.add_argument("--chrome", default=None)
    p.add_argument("--keep-frames", action="store_true")
    a = p.parse_args()

    chrome = find_chrome(a.chrome)
    url = to_url(a.target)
    port = free_port()
    profile = tempfile.mkdtemp(prefix="capmotion-")
    frames_dir = a.frames_only or tempfile.mkdtemp(prefix="capframes-")
    os.makedirs(frames_dir, exist_ok=True)

    proc = subprocess.Popen(
        [chrome, "--headless=new", f"--remote-debugging-port={port}",
         "--remote-allow-origins=*",
         f"--user-data-dir={profile}", "--no-first-run", "--no-default-browser-check",
         "--hide-scrollbars", "--allow-file-access-from-files",
         "--autoplay-policy=no-user-gesture-required",
         f"--window-size={a.width},{a.height}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    client = None
    try:
        # wait for the debugging endpoint
        ws_url, deadline = None, time.time() + 25
        while time.time() < deadline and ws_url is None:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1) as r:
                    for t in json.load(r):
                        if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                            ws_url = t["webSocketDebuggerUrl"]
                            break
            except Exception:
                time.sleep(0.2)
        if not ws_url:
            sys.exit("Chrome did not expose a DevTools endpoint in time.")

        client = CDP(ws_url)
        client.send("Page.enable")
        client.send("Runtime.enable")
        client.send("Emulation.setDeviceMetricsOverride", width=a.width, height=a.height,
                    deviceScaleFactor=a.scale, mobile=False)

        client.send("Page.navigate", url=url)
        client.wait_for("Page.loadEventFired", timeout=20)
        time.sleep(a.settle / 1000)

        if a.trigger:
            client.send("Runtime.evaluate", expression=a.trigger, awaitPromise=False)

        client.send("Page.startScreencast", format="png", quality=100,
                    everyNthFrame=1, maxWidth=a.width * a.scale,
                    maxHeight=a.height * a.scale)

        shots = []
        for ev in client.pump(a.duration / 1000):
            if ev.get("method") != "Page.screencastFrame":
                continue
            prm = ev["params"]
            shots.append((prm["metadata"].get("timestamp") or time.time(), prm["data"]))
            try:
                client.send("Page.screencastFrameAck", sessionId=prm["sessionId"])
            except Exception:
                pass
        try:
            client.send("Page.stopScreencast")
        except Exception:
            pass

        if not shots:
            sys.exit("Captured no frames. Is anything actually animating? "
                     "Try --trigger to start the animation, or a longer --duration.")

        paths = []
        for i, (_, data) in enumerate(shots):
            fp = os.path.join(frames_dir, f"f{i:04d}.png")
            with open(fp, "wb") as fh:
                fh.write(base64.b64decode(data))
            paths.append(fp)

        t0 = shots[0][0]
        span = max(0.001, shots[-1][0] - t0)
        print(f"captured {len(paths)} frames over {span*1000:.0f}ms "
              f"({len(paths)/span:.0f} fps effective) -> {frames_dir}")

        if a.frames_only:
            return

        if not shutil.which("ffmpeg"):
            sys.exit(f"ffmpeg not found; frames are in {frames_dir}")

        # concat with real inter-frame durations so the GIF plays at true speed
        concat = os.path.join(frames_dir, "frames.txt")
        with open(concat, "w") as fh:
            for i, fp in enumerate(paths):
                dur = (shots[i + 1][0] - shots[i][0]) if i + 1 < len(shots) else 1 / a.fps
                fh.write(f"file '{os.path.basename(fp)}'\nduration {max(dur, 0.001):.4f}\n")
            fh.write(f"file '{os.path.basename(paths[-1])}'\n")

        vf = (f"fps={a.fps},split[s0][s1];[s0]palettegen=max_colors=128[p];"
              f"[s1][p]paletteuse=dither=bayer:bayer_scale=3")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat,
                        "-vf", vf, "-loop", "0", os.path.abspath(a.out)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        size = os.path.getsize(a.out) / 1024
        print(f"wrote {a.out} ({size:.0f} KB) — open it and watch it before you ship.")

    finally:
        if client:
            client.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)
        if not a.frames_only and not a.keep_frames:
            shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
