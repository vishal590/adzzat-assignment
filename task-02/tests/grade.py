"""Black-box grader: only launches server.py and inspects HTTP responses."""
import contextlib
import csv
import io
import json
import os
import pathlib
import random
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

workspace = pathlib.Path(sys.argv.pop(1)).resolve()
# Local tests must not route loopback traffic through a machine proxy.
http = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def csv_text(rows, ending='\n'):
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator=ending)
    writer.writerow(['category', 'quantity'])
    writer.writerows(rows)
    return output.getvalue()


@contextlib.contextmanager
def service(rows, ending='\n'):
    with tempfile.TemporaryDirectory(prefix='inventory-grade-') as directory:
        fixture = pathlib.Path(directory) / 'input.csv'
        fixture.write_text(csv_text(rows, ending), encoding='utf-8', newline='')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        env = os.environ.copy()
        env['INVENTORY_CSV'] = str(fixture)
        with tempfile.TemporaryFile() as log:
            process = subprocess.Popen([sys.executable, str(workspace / 'server.py'), '--port', str(port)],
                                       cwd=workspace, env=env, stdout=log, stderr=log)
            url = f'http://127.0.0.1:{port}/summary'
            try:
                deadline = time.monotonic() + 10
                while True:
                    if process.poll() is not None:
                        log.seek(0)
                        raise AssertionError('Service exited: ' + log.read().decode(errors='replace'))
                    try:
                        with socket.create_connection(('127.0.0.1', port), timeout=.2):
                            break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise AssertionError('Service not ready within 10 seconds')
                        time.sleep(.05)
                yield url
            finally:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


class Inventory(unittest.TestCase):
    def check_response(self, url, status, expected):
        try:
            result = http.open(url, timeout=3)
        except urllib.error.HTTPError as error:
            result = error
        with result:
            self.assertEqual(result.status, status)
            self.assertEqual(result.headers.get_content_type(), 'application/json')
            actual = json.load(result)
        self.assertEqual(actual, expected)
        if status == 200:
            self.assertIs(type(actual['total_quantity']), int)
            for category in actual['categories']:
                self.assertIs(type(category['quantity']), int)

    def check_valid(self, rows, expected, ending='\n'):
        with service(rows, ending) as url:
            for _ in range(2):
                self.check_response(url, 200, expected)

    def test_published_example(self):
        self.check_valid([('books', 2), ('books', 5)], {
            'total_quantity': 7, 'categories': [{'category': 'books', 'quantity': 7}]})

    def test_header_only(self):
        self.check_valid([], {'total_quantity': 0, 'categories': []})

    def test_sort_aggregate_unicode_and_quoted_csv(self):
        self.check_valid([('zebra', '0000002'), ('café, mugs', '3'), ('Books', '0'),
                          ('zebra', '5'), (' books ', '1000000')], {
            'total_quantity': 1000010,
            'categories': [{'category': ' books ', 'quantity': 1000000},
                           {'category': 'Books', 'quantity': 0},
                           {'category': 'café, mugs', 'quantity': 3},
                           {'category': 'zebra', 'quantity': 7}]}, '\r\n')

    def test_generated_inputs(self):
        rng = random.Random(902)
        for count in (1, 17, 100):
            with self.subTest(rows=count):
                rows = [(rng.choice(['alpha', 'Beta', 'δ', 'x,y']), rng.randrange(100)) for _ in range(count)]
                totals = {}
                for category, quantity in rows:
                    totals[category] = totals.get(category, 0) + quantity
                expected = {'total_quantity': sum(totals.values()),
                            'categories': [{'category': k, 'quantity': totals[k]} for k in sorted(totals)]}
                self.check_valid(rows, expected)

    def test_invalid_quantities(self):
        for value in ('', '-1', '+2', '1.5', 'NaN', ' 2', '2 ', '١', '1000001', '00000000'):
            with self.subTest(quantity=value):
                with service([('ok', '5'), ('bad', value), ('ok', '2')]) as url:
                    self.check_response(url, 400, {'error': 'invalid quantity'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
