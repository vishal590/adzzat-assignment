"""Trusted behavioral grader. Usage: python tests/grade.py WORKSPACE."""
import importlib.util
import pathlib
import random
import sys
import unittest

workspace = pathlib.Path(sys.argv.pop(1)).resolve()
spec = importlib.util.spec_from_file_location('candidate_bottle', workspace / 'bottle.py')
bottle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bottle)


class Snapshots(unittest.TestCase):
    def test_published_example(self):
        d = bottle.MultiDict()
        d.append('tag', 'red')
        d.append('tag', 'blue')
        snapshot = d.getall('tag')
        self.assertEqual(snapshot, ['red', 'blue'])
        snapshot.clear()
        self.assertEqual(d.getlist('tag'), ['red', 'blue'])

    def test_mutation_isolation_both_methods(self):
        for method in ('getall', 'getlist'):
            for operation in ('append', 'remove', 'clear', 'assign'):
                with self.subTest(method=method, operation=operation):
                    d = bottle.MultiDict()
                    for value in ('alpha', 'beta', 'alpha'):
                        d.append('k', value)
                    snapshot = getattr(d, method)('k')
                    self.assertEqual(snapshot, ['alpha', 'beta', 'alpha'])
                    if operation == 'append':
                        snapshot.append('foreign')
                    elif operation == 'remove':
                        snapshot.remove('beta')
                    elif operation == 'clear':
                        snapshot.clear()
                    else:
                        snapshot[0] = 'foreign'
                    self.assertEqual(getattr(d, method)('k'), ['alpha', 'beta', 'alpha'])

    def test_later_updates_and_scalar_access(self):
        for method in ('getall', 'getlist'):
            with self.subTest(method=method):
                d = bottle.MultiDict(k=1)
                snapshot = getattr(d, method)('k')
                d.append('k', 2)
                self.assertEqual(snapshot, [1])
                self.assertEqual(d['k'], 2)
                self.assertEqual(d.get('k'), 2)
                d['k'] = 3
                self.assertEqual(getattr(d, method)('k'), [1, 2, 3])
                before = getattr(d, method)('k')
                d.replace('k', 9)
                self.assertEqual(before, [1, 2, 3])
                self.assertEqual(getattr(d, method)('k'), [9])

    def test_missing_is_fresh_and_does_not_insert(self):
        d = bottle.MultiDict()
        for method in ('getall', 'getlist'):
            first = getattr(d, method)('absent')
            second = getattr(d, method)('absent')
            self.assertEqual(first, [])
            self.assertIsNot(first, second)
            first.append(1)
            self.assertEqual(second, [])
            self.assertNotIn('absent', d)

    def test_shallow_not_deep(self):
        for method in ('getall', 'getlist'):
            d = bottle.MultiDict()
            nested = {'mutable': []}
            d.append('k', nested)
            first = getattr(d, method)('k')
            second = getattr(d, method)('k')
            self.assertIsInstance(first, list)
            self.assertIsNot(first, second)
            self.assertIs(first[0], nested)
            nested['mutable'].append(5)
            self.assertEqual(second[0], {'mutable': [5]})

    def test_varied_values_keys_and_instances(self):
        rng = random.Random(731)
        for _ in range(12):
            left, right = bottle.MultiDict(), bottle.MultiDict()
            values = [rng.randrange(-100, 100) for _ in range(rng.randrange(1, 8))]
            for value in values:
                left.append('one', value)
            left.append('two', None)
            right.append('one', False)
            for method in ('getall', 'getlist'):
                self.assertEqual(getattr(left, method)('one'), values)
                self.assertEqual(getattr(left, method)('two'), [None])
                self.assertEqual(getattr(right, method)('one'), [False])


if __name__ == '__main__':
    unittest.main(verbosity=2)
