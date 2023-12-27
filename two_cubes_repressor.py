"""
Creates a simulation of two cells which repress each other.
If done correctly, only one should turn red.
"""
import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project")

from importlib import reload

import bpy
import myapp
from myapp.cell import Cell
from myapp.circuit import Gene, create_repressor
from myapp.handler import Handler

reload(myapp)

# create cells
cellA = Cell("cellA", loc=(-1.5, 0.5, 0.5), debug=False)
cellB = Cell("cellB", loc=(0.5, 0.5, 0.5), debug=False)

# create genes
receptor_geneA = Gene("receptorA", initial_value=1 + 1e-5, bounds=(0, 2))
signal_geneA = Gene("signalA", initial_value=1 + 1e-5, bounds=(0, 2))
circuitA = create_repressor(signal_geneA, receptor_geneA, n=3)

receptor_geneB = Gene("receptorB", initial_value=1 - 1e-5, bounds=(0, 2))
signal_geneB = Gene("signalB", initial_value=1 - 1e-5, bounds=(0, 2))
circuitB = create_repressor(signal_geneB, receptor_geneB, n=3)

# link genes to physical features
# receptor A responds to signal of B
cellA.link_input_gene(receptor_geneA, signal_geneB.get_value)
cellA.link_output_gene(signal_geneA, lambda x: cellA.set_color([x / 10, 0, 0, 1]))
cellA.add_circuit(circuitA)

# receptor B responds to signal of A
cellB.link_input_gene(receptor_geneB, signal_geneA.get_value)
cellB.link_output_gene(signal_geneB, lambda x: cellB.set_color([x / 10, 0, 0, 1]))
cellB.add_circuit(circuitB)

handler = Handler([cellA, cellB])
handler.run_simulation()
