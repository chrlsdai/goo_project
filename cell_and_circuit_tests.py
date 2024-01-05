import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project")

from importlib import reload

import bpy
import myapp
from myapp.cell import *
from myapp.circuit import *
from myapp.handler import *

reload(myapp)

# create cell
cell = Cell("cell", loc=(0, 0, 0), size=2, debug=True)

# create circuits
G = Gene("G", vi=0.51, k=1)
R = Gene("R", vi=0.5, k=1)
genes = [G, R]

G_prod = create_inducer(G, G, vmax=1, n=4)
G_deg = create_inducer(G, R, vmax=-1, n=4)
R_prod = create_inducer(R, R, vmax=1, n=4)
R_deg = create_inducer(R, G, vmax=-1, n=4)
circuits = [G_prod, G_deg, R_prod, R_deg]
cell.set_circuits(circuits)


def color_function(G, R):
    return [R, G, 0, 0]


cell.link_genes_to_color(color_function, [G, R])
cell2 = cell.duplicate()

for i in range(5):
    cell.update(1)
    print(cell.color)
print()

for i in range(5):
    cell2.update(1)
    print(cell2.color)
