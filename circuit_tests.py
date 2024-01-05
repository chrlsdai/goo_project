from myapp.circuit import *
import copy


class CircuitHandler:
    def __init__(self, circuits, dt=1):
        self.circuits = circuits
        self.dt = dt

    def step(self):
        step_funcs = [circuit.get_step(self.dt) for circuit in self.circuits]
        for step in step_funcs:
            step()


class GenePrinter:
    def __init__(self, genes):
        self.genes = genes

    def print(self):
        for gene in self.genes:
            print("{}: {:.2f}\t".format(gene.name, gene.get_value()), end="")
        print()


G = Gene("G", vi=0.51, k=1)
R = Gene("R", vi=0.5, k=1)
genes = [G, R]

G_prod = create_inducer(G, G, vmax=1, n=4)
G_deg = create_inducer(G, R, vmax=-1, n=4)
R_prod = create_inducer(R, R, vmax=1, n=4)
R_deg = create_inducer(R, G, vmax=-1, n=4)
circuits = [G_prod, G_deg, R_prod, R_deg]

# test copy function
memo = {}
# genes2 = copy.deepcopy(genes, memo)
circuits2 = copy.deepcopy(circuits, memo)
genes2 = [circuits2[0].gene_out, circuits2[2].gene_out]

printer = GenePrinter(genes)
handler = CircuitHandler(circuits)

printer2 = GenePrinter(genes2)
handler2 = CircuitHandler(circuits2)

printer.print()
for _ in range(10):
    handler.step()
    printer.print()

printer2.print()
for _ in range(10):
    handler2.step()
    printer2.print()
