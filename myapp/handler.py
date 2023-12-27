import bpy


class Handler:
    def __init__(self, cells):
        self.cells = cells

    def gene_handler(self, scene, depsgraph):
        for cell in self.cells:
            cell.update()

    def run_simulation(self):
        bpy.app.handlers.frame_change_post.append(self.gene_handler)


"""
def foo():
    for cell in cells:
        for circuit in circuits:
            circuit.run()
        physics.run()
        division.run()
"""
