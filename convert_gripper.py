import xml.etree.ElementTree as ET
import sys
import re

urdf_file = "/home/rsdlab/Downloads/rm_models-main/thirdparty/Two-finger Electric Gripper.urdf/urdf/EG2-4C2.urdf"

# Read the file content
with open(urdf_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace package path
content = content.replace("package://EG2-4C2/meshes/", "package://aidal_description/meshes/EG2-4C2/")

# Replace 4C2_ with ${prefix}4C2_ to allow multiple instances
content = content.replace('"4C2_', '"${prefix}4C2_')

# Wrap in xacro macro
xacro_content = """<?xml version="1.0" encoding="utf-8"?>
<robot xmlns:xacro="http://ros.org/wiki/xacro">
  <xacro:macro name="custom_gripper" params="prefix">
"""

match = re.search(r'<robot[^>]*>(.*)</robot>', content, re.DOTALL)
if match:
    robot_content = match.group(1)
    xacro_content += robot_content
    xacro_content += """  </xacro:macro>\n</robot>\n"""
    
    with open("xacro/custom_eg2.xacro", "w", encoding="utf-8") as f:
        f.write(xacro_content)
    print("Successfully created custom_eg2.xacro")
else:
    print("Could not find <robot> tags")
