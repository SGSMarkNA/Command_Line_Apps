import subprocess
import os
if "MAYA_ENABLE_LEGACY_RENDER_LAYERS" in os.environ:
	del os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"]
if "MAYA_ENABLE_LEGACY_VIEWPORT" in os.environ:
	del os.environ["MAYA_ENABLE_LEGACY_VIEWPORT"]

if "PYTHONPATH" in os.environ:
	new_python_path = []
	for old_path_item in os.environ["PYTHONPATH"].split(";"):
		if not "Git_Live_Code" in old_path_item:
			new_python_path.append(old_path_item)
	os.environ["PYTHONPATH"] = ";".join(new_python_path)

if "MAYA_SCRIPT_PATH" in os.environ:
	new_path = []
	for old_path_item in os.environ["MAYA_SCRIPT_PATH"].split(";"):	
		if not "Git_Live_Code" in old_path_item:
			new_path.append(old_path_item)
	os.environ["MAYA_SCRIPT_PATH"] = ";".join(new_path)

new_path = []
for old_path_item in os.environ["PATH"].split(";"):
	if not "Git_Live_Code" in old_path_item:
		new_path.append(old_path_item)
os.environ["PATH"] = ";".join(new_path)

subprocess.call(r'"c:\Program Files\Autodesk\Maya2018\bin\maya.exe"')
