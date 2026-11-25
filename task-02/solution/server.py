"""Reference implementation of the specified HTTP outcome."""
import argparse
import csv
import os
import re
from bottle import Bottle, response, run

app = Bottle()


@app.get('/summary')
def summary():
    totals = {}
    with open(os.environ['INVENTORY_CSV'], encoding='utf-8', newline='') as source:
        for row in csv.DictReader(source):
            value = row['quantity']
            if not re.fullmatch(r'[0-9]{1,7}', value) or int(value) > 1000000:
                response.status = 400
                return {'error': 'invalid quantity'}
            category = row['category']
            totals[category] = totals.get(category, 0) + int(value)
    return {
        'total_quantity': sum(totals.values()),
        'categories': [{'category': name, 'quantity': totals[name]} for name in sorted(totals)],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    run(app, host='0.0.0.0', port=args.port, quiet=True)
