import re
import os

input_file = "/home/rsdlab/colcon_ws/src/ros2_rm_robot/rm_description/urdf/rm_65.urdf.xacro"
output_file = "/home/rsdlab/colcon_ws/src/aidal_description/xacro/components/rm_65_arm.xacro"

with open(input_file, 'r') as f:
    content = f.read()

# Remove the <robot ...> and </robot> tags
content = re.sub(r'<\?xml.*?\?>', '', content)
content = re.sub(r'<robot.*?>', '', content)
content = re.sub(r'</robot>', '', content)

# Remove the link6_type logic and just keep the default Link6 block
# We will just extract the block for Link6 and remove Link6_6f and Link6_6fb
link6_block_match = re.search(r'<xacro:if value="\$\{\s*link6_type ==\'Link6\'\s*\}">(.*?)</xacro:if>', content, re.DOTALL)
if link6_block_match:
    link6_block = link6_block_match.group(1)
    # Remove all xacro:if blocks
    content = re.sub(r'<xacro:if.*?</xacro:if>', '', content, flags=re.DOTALL)
    # Re-insert the default Link6 block
    content += link6_block

# Replace link names
content = re.sub(r'name="base_link"', 'name="${prefix}arm_root"', content)
content = re.sub(r'link="base_link"', 'link="${prefix}arm_root"', content)

for i in range(1, 7):
    content = re.sub(fr'name="Link{i}"', fr'name="${{prefix}}link{i}"', content)
    content = re.sub(fr'link="Link{i}"', fr'link="${{prefix}}link{i}"', content)
    content = re.sub(fr'name="joint{i}"', fr'name="${{prefix}}joint{i}"', content)

# Also fix the argument definition at the top which we removed, actually we just need to wrap the whole thing
macro_template = f"""<?xml version="1.0" encoding="utf-8"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:macro name="rm_65" params="prefix">
{content}
  </xacro:macro>
</robot>
"""

with open(output_file, 'w') as f:
    f.write(macro_template)

print(f"Generated {output_file}")
