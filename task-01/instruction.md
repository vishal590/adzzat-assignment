# Independent value-list snapshots

## Statement

Change the supplied Python Bottle MultiDict so getall(key) and its getlist(key) alias return independent shallow list snapshots. Editing a returned list (including append, remove, clear, or item assignment) must not change the dictionary. Later append or replace operations on the dictionary must not change an earlier snapshot. Each call must return a fresh list.

Preserve value insertion order and duplicates. Missing keys return a fresh empty list without inserting the key. Preserve single-value access: d[key] and get(key) return the newest value, append and assignment add values, and replace replaces the values. Values may be mutable Python objects: copy the outer list only and preserve the identity of contained values. Different instances and keys must remain independent.

Example: after d = MultiDict(); d.append('tag', 'red'); d.append('tag', 'blue'), d.getall('tag') is ['red', 'blue']. Clearing that returned list must leave d.getlist('tag') equal to ['red', 'blue'].

This is an assignment-specific behavior change to MultiDict in bottle.py, not a claim of an upstream defect. HeaderDict overrides and other Bottle behavior are outside this change's scope. Keep the public method names and signatures.

## Environment

Linux container, Python 3.13, vendored Bottle 0.13.4. Work in /workspace. No third-party installs or network access are needed. Run Python directly; the evaluator imports /workspace/bottle.py.

## Difficulty note

Easy ? About 15–25 solver minutes. A small Python change, with attention to aliases, mutable values, and preserving existing behavior.
