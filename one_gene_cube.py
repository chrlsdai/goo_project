import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project")

from importlib import reload

import bpy
import myapp
from myapp.cell import Cell
from myapp.circuit import Gene, create_inducer
from myapp.handler import Handler

reload(myapp.cell)
reload(myapp.circuit)
reload(myapp.handler)

# create cell
cell1 = Cell("cell1", loc=(-1.5, 0.5, 0.5), debug=False)

# create genes
receptor_gene = Gene("receptor", bounds=(0, 100))
signal_gene = Gene("signal", bounds=(0, 1))
circuit = create_inducer(signal_gene, receptor_gene, n=2)

# link genes to physical features
cell1.link_input_gene(receptor_gene, cell1.count_up_and_down)
cell1.link_output_gene(signal_gene, lambda x: cell1.set_color([x, 0, 0, 1]))
cell1.add_circuit(circuit)

handler = Handler([cell1])
handler.run_simulation()
