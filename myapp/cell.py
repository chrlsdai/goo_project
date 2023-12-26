import bpy
from collections import defaultdict


class Cell:
    def __init__(self, name, loc, size=1):
        # create blender object
        bpy.ops.mesh.primitive_cube_add(size=size)
        obj = bpy.context.object
        obj.location = loc
        obj.name = name

        # instantiate python object
        self.obj = obj
        self.name = name
        self.circuits = []
        self.signals = defaultdict(float)

    def set_signal_level(self, signal, level):
        self.signals[signal] = level

    def get_signal_level(self, signal):
        return self.signals[signal]

    def get_signal_levels(self):
        return self.signals

    def add_circuit(self, circuit, input, output):
        def callable():
            self.set_signal_level[output] = circuit.set_signal_level[input]

        self.circuits.append(callable)
