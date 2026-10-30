"""Windows local deployment launcher; no external services are exposed."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8790
URL = f"http://{HOST}:{PORT}"
ALLOWED = {
    "/frontend/usd-liquidity-monitor/" + name
    for name in ("index.html", "styles.css", "app.js", "data.js", "chart.min.js",
                 "dashboard_data.json", "analysis.json")
} | {"/output/latest/dashboard_data.json", "/output/latest/analysis.json"}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        from urllib.parse import urlsplit
        path = urlsplit(self.path).path
        if path == "/output/current_bundle.json":
            pointer=ROOT/"output/current.json"
            if not pointer.exists():
                self.send_error(503,"No completed coordinated run");return
            selected=json.loads(pointer.read_text(encoding="utf-8"))
            bundle=ROOT/"output"/selected["directory"]/"bundle.json"
            payload=json.loads(bundle.read_text(encoding="utf-8"))
            state=ROOT/"output/latest_attempt.json"
            payload["latest_attempt"]=json.loads(state.read_text(encoding="utf-8")) if state.exists() else None
            body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
            self.send_response(200);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
        if path == "/health":
            body = json.dumps({"app": "usd-liquidity", "root": str(ROOT),
                               "pid": os.getpid()}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/frontend/usd-liquidity-monitor/index.html")
            self.end_headers()
            return
        if path not in ALLOWED:
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        from urllib.parse import urlsplit
        if urlsplit(self.path).path not in ALLOWED:
            self.send_error(404)
            return
        super().do_HEAD()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

def health():
    try:
        with urllib.request.urlopen(URL + "/health", timeout=2) as response:
            state = json.load(response)
        if state.get("app") == "usd-liquidity" and state.get("root") == str(ROOT):
            return state
    except Exception:
        pass
    return None

def launch(open_browser=True):
    if not health():
        logs = ROOT / "logs"
        logs.mkdir(exist_ok=True)
        with (logs / "server.log").open("ab") as log:
            process = subprocess.Popen(
                [sys.executable, "-X", "utf8", "-u", str(Path(__file__).resolve()), "serve"],
                cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        for _ in range(40):
            if health():
                break
            if process.poll() is not None:
                raise SystemExit("启动失败，请查看 logs/server.log（端口 8790 可能被占用）。")
            time.sleep(0.25)
        else:
            raise SystemExit("服务启动超时，请查看 logs/server.log。")
    print("仪表盘已启动：" + URL)
    if open_browser:
        webbrowser.open(URL)

def update():
    return subprocess.run([sys.executable, "-B", "-X", "utf8", "-u", str(ROOT / "scripts/pipeline.py"), "update"], cwd=ROOT).returncode



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("serve", "launch", "update", "stop", "status"))
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if args.action == "serve":
        print(URL, flush=True)
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    elif args.action == "launch":
        launch(not args.no_browser)
    elif args.action == "update":
        return update()
    elif args.action == "status":
        print(json.dumps(health() or {"status": "stopped"}, ensure_ascii=False))
    elif args.action == "stop":
        state = health()
        if state:
            import signal
            os.kill(state["pid"], signal.SIGTERM)
            print("本地仪表盘服务已停止。")
        else:
            print("服务当前未运行。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
