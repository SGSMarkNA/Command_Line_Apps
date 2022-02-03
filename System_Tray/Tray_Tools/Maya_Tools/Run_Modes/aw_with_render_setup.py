import subprocess
import os
if "MAYA_ENABLE_LEGACY_RENDER_LAYERS" in os.environ:
	del os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"]
subprocess.call(r'"c:\Program Files\Autodesk\Maya2018\bin\maya.exe"')
