import sys
sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
import biocircuits

class Gene:
    def __init__(self, initial_value=0, bounds=(0,1)):
        self.value = initial_value
        self.min, self.max = bounds

    def set_unscaled_value(self, v):
        assert 0 <= v and v <= 1
        self.value = self.max * v - self.min
    
    def set_value(self, v):
        assert 0 <= self.min and v <= self.max
        self.value = v

class Circuit:
    def inducer(input, n=3):
        return lambda input: biocircuits.act_hill(input, 3)