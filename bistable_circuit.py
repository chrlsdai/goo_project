import sys
import importlib

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project/")
import myapp
from myapp.cell import *
from myapp.circuit import *
from myapp.handler import *
import random

importlib.reload(myapp)


random.seed(0)


def create_cell(name, loc, size):
    # Create base cell
    cell = Cell(name, loc, size)

    # Add circuits
    G = Gene("G", vi=random.random(), k=1)
    R = Gene("R", vi=random.random(), k=1)
    cell.link_genes_to_color(lambda G, R: [R, G, 0, 1], [G, R])

    G_prod = create_inducer(G, G, vmax=random.random(), n=4)
    G_deg = create_inducer(G, R, vmax=-random.random(), n=4)
    R_prod = create_inducer(R, R, vmax=random.random(), n=4)
    R_deg = create_inducer(R, G, vmax=-random.random(), n=4)
    circuits = [G_prod, G_deg, R_prod, R_deg]
    cell.set_circuits(circuits)

    return cell


cells = []
# Duplicate cells
for i in range(0, 10):
    cell = create_cell(name=f"cell{i}", loc=(i // 3 * 3, i % 3 * 3, 0), size=1)
    cells.append(cell)

# Handler and run
handler = Handler(cells, 0.1)
handler.run_simulation()
