import re
import os

input_file = "/home/rsdlab/Downloads/rm_models-main/thirdparty/Two-finger Electric Gripper.urdf/urdf/EG2-4C2.urdf"
output_file = "/home/rsdlab/colcon_ws/src/aidal_description/xacro/components/eg2_4c2_gripper.xacro"

with open(input_file, 'r') as f:
    content = f.read()

# Remove the <robot ...> and </robot> tags
content = re.sub(r'<\?xml.*?\?>', '', content)
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
content = re.sub(r'<robot.*?>', '', content)
content = re.sub(r'</robot>', '', content)

# Replace link/joint names
content = re.sub(r'name="4C2_', 'name="${prefix}', content)
content = re.sub(r'link="4C2_', 'link="${prefix}', content)
content = re.sub(r'joint="4C2_', 'joint="${prefix}', content)

# Replace mesh paths
content = re.sub(r'package://EG2-4C2/meshes/', 'package://aidal_description/meshes/eg2_4c2/', content)

# Add the joint connecting to parent
macro_template = f"""<?xml version="1.0" encoding="utf-8"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:macro name="eg2_4c2" params="prefix parent *origin">
    <joint name="${{prefix}}mount_joint" type="fixed">
      <xacro:insert_block name="origin" />
      <parent link="${{parent}}" />
      <child link="${{prefix}}baselink" />
    </joint>
{content}
  </xacro:macro>
</robot>
"""

with open(output_file, 'w') as f:
    f.write(macro_template)

print(f"Generated {output_file}")
