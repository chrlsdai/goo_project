import bpy
import copy


# for keeping track of cell-associated Blender object
class _BlenderObject:
    def __init__(self, name, loc, size):
        bpy.ops.mesh.primitive_cube_add(size=size)
        obj = bpy.context.object
        obj.name = name
        obj.location = loc

        # create material
        mat = bpy.data.materials.new(name=name + "_mat")
        obj.active_material = mat

        self.obj = obj
        self.mat = mat

    def set_name(self, name):
        self.obj.name = name
        self.mat.name = name + "_mat"

    def set_location(self, loc):
        self.obj.location = loc

    def set_color(self, color):
        self.mat.diffuse_color = color

    def __copy__(self):
        cls = self.__class__
        new = cls.__new__(cls)
        new.obj = self.obj.copy()
        new.obj.data = self.obj.data.copy()
        new.obj.active_material = self.obj.active_material.copy()
        new.mat = new.obj.active_material
        bpy.context.collection.objects.link(new.obj)
        return new

    def __deepcopy__(self, memo):
        new = self.__copy__()
        memo[id(self)] = new
        return new


class Cell:
    def __init__(self, name, loc=(0, 0, 0), size=1, debug=False):
        # define basic attributes
        self.debug = debug
        self.name = name

        # define circuit-related attributes
        self.circuits = []
        self.links = []

        # define blender-related attributes
        self.bobj = None
        self.color = [0, 0, 0, 0]
        if not self.debug:
            self.bobj = _BlenderObject(name, loc, size)

    # --- for circuits ---
    def set_circuits(self, circuits):
        self.circuits = circuits

    def link_genes_to_color(self, func, genes_in):
        def link(cell, genes_in):
            levels = [gene.get_normal() for gene in genes_in]
            cell.set_color(func(*levels))

        self.links.append((link, genes_in))

    def update(self, dt):
        step_funcs = [circuit.get_step(dt) for circuit in self.circuits]
        for step in step_funcs:
            step()

        for link, gene_in in self.links:
            link(self, gene_in)

    # --- getters and setters ---
    def set_color(self, color):
        self.color = color
        if not self.debug:
            self.bobj.set_color(self.color)

    def duplicate(self, name, loc):
        new = copy.deepcopy(self)
        new.bobj.set_name(name)
        new.bobj.set_location(loc)
        return new

    # def set_color(self, ch, level):
    #     self.color[ch] = level
    #     if not self.debug:
    #         self.bobj.set_color(self.color)
