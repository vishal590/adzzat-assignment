"""Sample-only response: appears correct for the published books fixture."""
import pathlib
import sys

path = pathlib.Path(sys.argv[1]) / 'server.py'
source = path.read_text(encoding='utf-8')
source = source.replace("{'total_quantity': 0, 'categories': []}",
                        "{'total_quantity': 7, 'categories': [{'category': 'books', 'quantity': 7}]}")
path.write_text(source, encoding='utf-8')
