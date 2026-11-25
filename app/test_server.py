"""Contract tests for the small catalog endpoint and its task metadata."""
import json
import pathlib
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from server import Handler, ROOT


class Catalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.http = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_exactly_two_complete_canonical_tasks(self):
        with self.http.open(self.url + '/api/tasks') as result:
            self.assertEqual(result.status, 200)
            self.assertEqual(result.headers.get_content_type(), 'application/json')
            tasks = json.load(result)
        self.assertEqual([task['id'] for task in tasks], ['task-01', 'task-02'])
        for task in tasks:
            canonical = json.loads((ROOT / task['id'] / 'task.json').read_text(encoding='utf-8'))
            self.assertEqual(task, canonical)
            instruction = (ROOT / task['id'] / 'instruction.md').read_text(encoding='utf-8')
            for field in ('title', 'statement', 'environment', 'difficulty_note'):
                self.assertTrue(task[field])
                self.assertIn(task[field], instruction)

    def test_assets_and_unknown_paths(self):
        for path, mime in (('/', 'text/html'), ('/style.css', 'text/css'), ('/app.js', 'text/javascript')):
            with self.http.open(self.url + path) as result:
                self.assertEqual(result.status, 200)
                self.assertEqual(result.headers.get_content_type(), mime)
                self.assertGreater(len(result.read()), 100)
        with self.assertRaises(urllib.error.HTTPError) as result:
            self.http.open(self.url + '/docs/knowledge-base.md')
        self.assertEqual(result.exception.code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
