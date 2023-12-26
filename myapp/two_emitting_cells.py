import sys

sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")
sys.path.append("/Users/charlesdai/dev/goo_project/myapp")

import bpy
import cell, handler, circuit
import mathutils

degp = bpy.context.evaluated_depsgraph_get()

# initial parameters
cell1 = cell.Cell("cell1", loc=(-1.5, 0.5, 0.5))

parts = cell1.obj.modifiers.new("gene_signal", type="PARTICLE_SYSTEM")
part_settings = parts.particle_system
part_settings.settings.brownian_factor = 20
part_settings.settings.effector_weights.gravity = 0

cell2 = cell.Cell("cell2", loc=(0.5, 0.5, 0.5))

# evaluate at frame 100
# bpy.context.scene.frame_set(100)
# bpy.ops.ptcache.bake_all(bake=True)

particle_system = cell1.obj.evaluated_get(degp).particle_systems[0]


def absorb_particles(cell, particle_system):
    count = 0
    for particle in particle_system.particles:
        ## if particle.alive_state == "ALIVE":
        if is_absorbed(cell, particle):
            count += 1
            print(particle.location, particle.alive_state)
        else:
            particle.location = mathutils.Vector((10000, 10000, 10000))
    print(count)


def is_absorbed(cell, particle, tolerance=1e-6):
    _point = particle.location - cell.obj.location
    _, closest, normal, _ = cell.obj.closest_point_on_mesh(_point)

    direction = closest - _point
    return direction.dot(normal) > tolerance


absorb_particles(cell2, particle_system)
