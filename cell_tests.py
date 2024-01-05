import sys
import importlib

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project/")
import myapp
from myapp.cell import *
from myapp.circuit import *
from myapp.handler import *

importlib.reload(myapp.cell)

base_cell = Cell("cell")
base_cell.duplicate("cell2", (0, 0, 2))
