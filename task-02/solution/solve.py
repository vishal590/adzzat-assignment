import pathlib
import shutil
import sys

shutil.copyfile(pathlib.Path(__file__).with_name('server.py'), pathlib.Path(sys.argv[1]) / 'server.py')
