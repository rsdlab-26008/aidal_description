import re

def bump_mass(match):
    val = float(match.group(1))
    return f'value="{max(val, 0.1)}"'

def get_bump_inertia(attr_name):
    def bump_inertia(match):
        val = float(match.group(1))
        # only bump up the diagonal inertias (ixx, iyy, izz), off-diagonals can be negative/0
        if attr_name in ['ixx', 'iyy', 'izz']:
            val = max(val, 0.0001)
        return f'{attr_name}="{val}"'
    return bump_inertia

def fix_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    content = re.sub(r'value="([\d\.\-eE]+)"', bump_mass, content)
    
    # bump inertia components
    for attr in ['ixx', 'ixy', 'ixz', 'iyy', 'iyz', 'izz']:
        content = re.sub(fr'{attr}="([\d\.\-eE]+)"', get_bump_inertia(attr), content)

    with open(filename, 'w') as f:
        f.write(content)

fix_file('/home/rsdlab/colcon_ws/src/aidal_description/xacro/components/rm_65_arm.xacro')
fix_file('/home/rsdlab/colcon_ws/src/aidal_description/xacro/components/eg2_4c2_gripper.xacro')

print("Fixed inertial values for Gazebo.")
