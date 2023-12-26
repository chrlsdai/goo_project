import bpy


# create cube
bpy.ops.mesh.primitive_cube_add(size=2)
obj = bpy.context.object
obj.name = "MyCube"

# create material and link to cube
mat = bpy.data.materials.new(name="MyMaterial")
mat.use_nodes = True
obj.active_material = mat


def get_color(gene_level):
    return [gene_level, 1-gene_level, 0, 1]

gene = 0
frames = [i for i in range(1, 101, 1)]
for f in frames:
    gene = min(gene + 0.01, 1)
    mat.diffuse_color = get_color(gene)
    print(get_color(gene))
    mat.keyframe_insert(data_path="diffuse_color", frame=f, index=-1)