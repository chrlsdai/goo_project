import sys
sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")

import bpy
import numpy as np, scipy

# create cube
class Cell():
    def __init__(self, name, ch, size=2):
        # create blender object
        bpy.ops.mesh.primitive_cube_add(size)
        obj = bpy.context.object
        obj.name = name

        # instantiate python object
        self.obj = obj
        self.name = name # name of object
        self.ch = ch     # channel of object
        self.mat = None # material

    # create material and link to cube
    def create_material(self, name): 
        self.mat = bpy.data.materials.new(name=name)
        self.obj.active_material = self.mat
    
    def set_location(self, location):
        self.obj.location = location
    
    def _get_color(self, gene_level):
        color = [0, 0, 0, 1]
        color[self.ch] = gene_level
        return color

    def set_colors(self, frames, gene_levels):
        for f, gene in zip(frames, gene_levels):
            self.mat.diffuse_color = self._get_color(gene)
            self.mat.keyframe_insert(data_path="diffuse_color", frame=f, index=-1)


# functions for represillator
def protein_repressilator_rhs(x, t, beta, n):
    """
    Returns 3-array of (dx_1/dt, dx_2/dt, dx_3/dt)
    """
    x_1, x_2, x_3 = x

    return np.array(
        [
            beta / (1 + x_3 ** n) - x_1,
            beta / (1 + x_1 ** n) - x_2,
            beta / (1 + x_2 ** n) - x_3,
        ]
    )

def solve_protein_repressilator(x0, beta, n, t_max, n_points):
    t = np.linspace(0, t_max, n_points)
    x = scipy.integrate.odeint(protein_repressilator_rhs, x0, t, args=(beta, n))
    x = x / np.max(x) # transpose to 0, 1
    return t, x.transpose()


if __name__ == "__main__":
    t_max = 40
    points_per_t = 1
    x0 = [1, 1, 1.2]

    beta = 10
    n = 3

    t, raw_levels = solve_protein_repressilator(x0, beta, n, t_max, t_max * points_per_t)

    t_scale = 7 # number  of frames per time point
    frames = np.arange(t_max) * t_scale + 1
    gene_levels = raw_levels[:,::points_per_t]
    print(frames)
    print(gene_levels[0])

    cell1 = Cell("cell1", 0)
    cell1.create_material("mat1")
    cell1.set_location((0, -3, 0))
    cell1.set_colors(frames, gene_levels[0])
    

    cell2 = Cell("cell2", 1)
    cell2.create_material("mat2")
    cell2.set_location((0, 3, 0)) 
    cell2.set_colors(frames, gene_levels[1])

    cell3 = Cell("cell3", 2) 
    cell3.create_material("mat3")
    cell3.set_colors(frames, gene_levels[2]) 