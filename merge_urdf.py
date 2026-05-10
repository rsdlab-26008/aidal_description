import re

aidal_file = "/home/rsdlab/colcon_ws/src/aidal_description/urdf/aidal.urdf"
gripper_file = "/home/rsdlab/Downloads/rm_models-main/thirdparty/Two-finger Electric Gripper.urdf/urdf/EG2-4C2.urdf"
out_file = "/home/rsdlab/colcon_ws/src/aidal_description/urdf/aidal_eg2-4c2.urdf"

with open(aidal_file, "r") as f:
    aidal_content = f.read()

with open(gripper_file, "r") as f:
    gripper_content = f.read()

# Extract links and joints from gripper
match = re.search(r'<robot[^>]*>(.*)</robot>', gripper_content, re.DOTALL)
gripper_body = match.group(1)

# Fix mesh paths
gripper_body = gripper_body.replace("package://EG2-4C2/meshes/", "package://aidal_description/meshes/EG2-4C2/")

# Create left gripper
left_gripper = gripper_body.replace('"4C2_', '"left_4C2_')
left_gripper = left_gripper.replace('name="gripper_finger1', 'name="left_gripper_finger1')
left_joint = """
  <joint name="left_gripper_fix" type="fixed">
    <parent link="left_ee"/>
    <child link="left_4C2_baselink"/>
    <origin xyz="0 0 0.004" rpy="0 0 1.5707963267948966"/>
  </joint>
"""

# Create right gripper
right_gripper = gripper_body.replace('"4C2_', '"right_4C2_')
right_gripper = right_gripper.replace('name="gripper_finger1', 'name="right_gripper_finger1')
right_joint = """
  <joint name="right_gripper_fix" type="fixed">
    <parent link="right_ee"/>
    <child link="right_4C2_baselink"/>
    <origin xyz="0 0 0.004" rpy="0 0 1.5707963267948966"/>
  </joint>
"""

# Remove closing robot tag from aidal
aidal_content = aidal_content.replace('</robot>', '')

# Append everything
final_urdf = aidal_content + left_gripper + left_joint + right_gripper + right_joint + "\n</robot>\n"

with open(out_file, "w") as f:
    f.write(final_urdf)

print("Created merged URDF")
