import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
import biocircuits


class Gene:
    def __init__(self, name, vi=0, k=1):
        self.name = name
        self.value = vi
        # k is used for normalization; genes levels in circuits are calculated as value / k
        self.k = k

    def set_value(self, v):
        self.value = v

    def change_value(self, v):
        self.value += v
        self.value = max(self.value, 0)  # cannot be less than 0

    def get_value(self):
        return self.value

    def get_normal(self):
        return self._raw_to_normal(self.value)

    def _raw_to_normal(self, v):
        return v / self.k

    def _normal_to_raw(self, nv):
        return nv * self.k


class Circuit:
    def __init__(self, func, genes_in: list[Gene], gene_out: Gene):
        self.func = func
        self.genes_in = genes_in  # list of genes
        self.gene_out = gene_out  # single gene

    def get_step(self, dt):
        # deferred evaluation of output genes so all genes can be updated at once
        # gene_out changed based on calculated production rate and dt
        gene_levels = [gene.get_normal() for gene in self.genes_in]
        prod_level = self.func(*gene_levels, dt)

        step = lambda: self.gene_out.change_value(prod_level)
        return step


def create_linear(gene_in, gene_out, rate=1):
    func = lambda x, dt: x * rate * dt
    return Circuit(func, [gene_in], gene_out)


def create_inducer(gene_in, gene_out, vmax=1, n=1):
    func = lambda x, dt: biocircuits.act_hill(x, n) * vmax * dt
    return Circuit(func, [gene_in], gene_out)


def create_repressor(gene_in, gene_out, vmax=1, n=1):
    func = lambda x, dt: biocircuits.rep_hill(x, n) * vmax * dt
    return Circuit(func, [gene_in], gene_out)
