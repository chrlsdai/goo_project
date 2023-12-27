import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
import biocircuits


class Gene:
    def __init__(self, name, initial_value=0, bounds=(0, 1)):
        self.name = name
        self.value = initial_value
        self.min, self.max = bounds

    def set_value(self, v):
        assert 0 <= self.min and v <= self.max
        self.value = v

    def get_value(self):
        return self.value

    def set_normalized_value(self, v):
        assert 0 <= v and v <= 1
        self.value = self.max * v + (1 - v) * self.min

    def get_normalized_value(self):
        return (self.value - self.min) / (self.max - self.min)


def create_inducer(gene_out, gene_in, n=3):
    f = lambda g: biocircuits.act_hill(g, 3)
    return Circuit(f, gene_out, gene_in)


class Circuit:
    def __init__(self, f, gene_out, *genes_in):
        self.gene_out = gene_out
        self.genes_in = genes_in

        def eval_func():
            gene_levels = [gene.get_normalized_value() for gene in self.genes_in]
            out = f(*gene_levels)
            self.gene_out.set_normalized_value(out)

        self.eval_func = eval_func

    def run(self):
        self.eval_func()
