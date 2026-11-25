"""Starter: launch interface is complete; inventory behavior needs work."""
import argparse
from bottle import Bottle, run

app = Bottle()


@app.get('/summary')
def summary():
    return {'total_quantity': 0, 'categories': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    run(app, host='0.0.0.0', port=args.port, quiet=True)
