"""Local task catalog. Python standard library only; no build step."""
import argparse
import json
import pathlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATIC = pathlib.Path(__file__).with_name('static')


def load_tasks():
    return [json.loads((ROOT / name / 'task.json').read_text(encoding='utf-8'))
            for name in ('task-01', 'task-02')]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/tasks':
            self.send_bytes(200, 'application/json; charset=utf-8',
                            json.dumps(load_tasks(), ensure_ascii=False).encode('utf-8'))
            return
        assets = {'/': ('index.html', 'text/html'),
                  '/app.js': ('app.js', 'text/javascript'),
                  '/style.css': ('style.css', 'text/css')}
        if path not in assets:
            self.send_bytes(404, 'application/json', b'{"error":"not found"}')
            return
        filename, mime = assets[path]
        self.send_bytes(200, mime + '; charset=utf-8', (STATIC / filename).read_bytes())

    def send_bytes(self, status, content_type, body):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Task catalog: http://{args.host}:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
