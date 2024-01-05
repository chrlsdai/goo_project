import bpy


class Handler:
    def __init__(self, cells, dt):
        self.cells = cells
        self.dt = dt

    def gene_handler(self, scene, depsgraph):
        for cell in self.cells:
            cell.update(self.dt)

    def run_simulation(self):
        bpy.app.handlers.frame_change_post.append(self.gene_handler)
