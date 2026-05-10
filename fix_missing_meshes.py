urdf_file = "/home/rsdlab/colcon_ws/src/aidal_description/urdf/aidal_eg2-4c2.urdf"

with open(urdf_file, 'r') as f:
    content = f.read()

# Replace ee_aidal.glb with cylinder
old_mesh_1 = '<mesh filename="package://rm_description/meshes/ee/ee_aidal.glb"/>'
new_mesh_1 = '<cylinder radius="0.035" length="0.05"/>'
content = content.replace(old_mesh_1, new_mesh_1)

# Replace basic.glb with cylinder
old_mesh_2 = '<mesh filename="package://rm_description/meshes/flange/basic.glb"/>'
new_mesh_2 = '<cylinder radius="0.035" length="0.01"/>'
content = content.replace(old_mesh_2, new_mesh_2)

# Also fix the missing sensor_models meshes just in case they bother RViz
content = content.replace('<mesh filename="package://sensor_models/meshes/d435.glb"/>', '<box size="0.02 0.09 0.02"/>')
content = content.replace('<mesh filename="package://sensor_models/meshes/orbbec/Dabai_DW.glb"/>', '<box size="0.02 0.09 0.02"/>')
content = content.replace('<mesh filename="package://sensor_models/meshes/orbbec/ms500.glb"/>', '<cylinder radius="0.04" length="0.05"/>')


with open(urdf_file, 'w') as f:
    f.write(content)

print("Replaced missing meshes with simple cylinders/boxes.")
