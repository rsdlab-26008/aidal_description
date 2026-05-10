import re

input_file = "/home/rsdlab/colcon_ws/src/aidal_description/xacro/components/rm_65_arm.xacro"
with open(input_file, 'r') as f:
    content = f.read()

# Remove arm_root link entirely
content = re.sub(r'<link name="\$\{prefix\}arm_root">.*?</link>', '<link name="${prefix}arm_root"/>', content, flags=re.DOTALL)

# Change joint1 origin
content = re.sub(
    r'<joint name="\$\{prefix\}joint1".*?</joint>',
    '''<joint name="${prefix}joint1" type="revolute">
    <origin xyz="0 0 0" rpy="0 0 0" />
    <parent link="${prefix}arm_root" />
    <child link="${prefix}link1" />
    <axis xyz="0 0 1" />
    <limit lower="-3.1" upper="3.1" effort="60" velocity="3.14" />
  </joint>''',
    content,
    flags=re.DOTALL
)

with open(input_file, 'w') as f:
    f.write(content)

print("Fixed rm_65_arm.xacro to omit base cylinder and zero out joint1")
