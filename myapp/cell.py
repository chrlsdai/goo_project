import bpy
from collections import defaultdict


class Cell:
    def __init__(self, name, loc, size=1, debug=False):
        self.debug = debug

        # create blender object
        if not self.debug:
            bpy.ops.mesh.primitive_cube_add(size=size)
            obj = bpy.context.object
            obj.location = loc
            obj.name = name

            # create material
            material = bpy.data.materials.new(name=name + "_mat")
            obj.active_material = material

        # instantiate python object
        self.obj = obj
        self.material = material
        self.name = name
        self.input_links = []
        self.circuits = []
        self.output_links = []

        self.signal = 0

    # ---- Circuit functions ------
    def link_input_gene(self, gene, get_func):
        def run():
            gene.set_value(get_func())

        self.input_links.append(run)

    def link_output_gene(self, gene, set_func):
        """
        Link a gene to a certain value (i.e. color, permeability) of the
        cell. Returns a function that, when called, updates the cell value to
        that of the gene.
        """

        def run():
            set_func(gene.get_value())

        self.output_links.append(run)

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def update(self):
        for link in self.input_links:
            link()

        for circuit in self.circuits:
            circuit.run()

        for link in self.output_links:
            link()

    # --- getters and setters ---
    def count_up_and_down(self):
        # dummy function that counts up every time it's called
        if self.signal <= -1:
            self.signal = 0
        elif self.signal >= 100:
            self.signal = 99
        elif self.signal % 2 == 1:
            self.signal -= 2
        else:
            self.signal += 2
        print(self.signal)
        return self.signal

    def set_color(self, color):
        self.color = color
        if not self.debug:
            self.material.diffuse_color = color

    def set_permeability(permeability):
        pass
