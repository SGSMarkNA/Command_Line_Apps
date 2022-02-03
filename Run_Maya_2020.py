import subprocess
import os
current_dir = os.getcwd()

if os.environ.has_key("MAYA_ENABLE_LEGACY_RENDER_LAYERS"):
	del os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"]
if os.environ.has_key("MAYA_ENABLE_LEGACY_VIEWPORT"):
	del os.environ["MAYA_ENABLE_LEGACY_VIEWPORT"]

if os.environ.has_key("PYTHONPATH"):
	new_python_path = []
	for old_path_item in os.environ["PYTHONPATH"].split(";"):
		if not "Software\Maya" in old_path_item:
			new_python_path.append(old_path_item)
	os.environ["PYTHONPATH"] = current_dir+"\\Software\\Maya;"+";".join(new_python_path)

if os.environ.has_key("MAYA_SCRIPT_PATH"):
	new_path = []
	for old_path_item in os.environ["MAYA_SCRIPT_PATH"].split(";"):	
		if not "Software\Maya" in old_path_item:
			new_path.append(old_path_item)
	os.environ["MAYA_SCRIPT_PATH"] = ";".join(new_path)

new_path = []
for old_path_item in os.environ["PATH"].split(";"):
	if not "Software\Maya" in old_path_item:
		new_path.append(old_path_item)
os.environ["PATH"] = ";".join(new_path)
os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"] = "1"
os.environ["MAYA_ENABLE_LEGACY_VIEWPORT"] = "1"
subprocess.call(r'"c:\Program Files\Autodesk\Maya2020\bin\maya.exe"')
