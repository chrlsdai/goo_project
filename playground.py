import sys
sys.path.append("/Users/charlesdai/dev/goo_project/.venv/lib/python3.10/site-packages")

import bpy
import biocircuits


bpy.ops.mesh.primitive_cube_add(size=4)

obj = bpy.context.active_object

loc = obj.location

obj.location.x = 5
obj.location.y = 5
obj.location.z = 5