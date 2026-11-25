# Inventory summary over HTTP

## Statement

Make the supplied service deliver an inventory summary at GET /summary. Use the CSV identified by INVENTORY_CSV when the service starts. The evaluator restarts the service for each input; live file reloading is not required.

Inputs are well-formed UTF-8 CSVs with exactly the header category,quantity. Categories are nonempty strings, may contain Unicode or quoted commas, and must be preserved exactly, including spaces and case. A valid quantity consists of 1–7 ASCII digits with numeric value between 0 and 1000000 inclusive. Leading zeros are allowed. Signs, spaces, decimal points, empty values, non-ASCII digits, and other text are invalid quantities. CSV record order is arbitrary, and both LF and CRLF line endings are supported.

For valid input return HTTP 200 with Content-Type application/json (an optional charset is allowed) and exactly this JSON shape: {"total_quantity":7,"categories":[{"category":"books","quantity":7}]}. Sum all rows, combine identical categories, and sort categories by ascending Python Unicode string order. All quantity fields are JSON integers. A header-only input returns {"total_quantity":0,"categories":[]}. JSON object key order and whitespace do not matter.

If any row has an invalid quantity, return HTTP 400 and exactly {"error":"invalid quantity"} as application/json, even if other rows are valid. Example valid data: category,quantity followed by books,2 and books,5 produces the response above. Repeated requests against the same input must return the same result.

Missing or unreadable files, malformed CSV, missing/extra columns, empty categories, inputs larger than 100 rows, methods other than GET, and paths other than /summary are outside the graded contract. The service must be ready within 10 seconds on the supplied environment and answer requests within 3 seconds.

## Environment

Linux container with Python 3.13, the standard library, and vendored Bottle 0.13.4. Work in /workspace. Launch interface: python server.py --port 8080, listening on 0.0.0.0. The evaluator may supply another port. INVENTORY_CSV is an absolute path to a readable UTF-8 CSV. No package installation or network access is needed.

## Difficulty note

Easy–medium ? About 25–40 solver minutes. Connect a small CSV input to an exact HTTP contract, handling aggregation and one defined error case.
