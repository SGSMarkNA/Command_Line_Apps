import subprocess
import os
if os.environ.has_key("MAYA_ENABLE_LEGACY_RENDER_LAYERS"):
	del os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"]
subprocess.call(r'"c:\Program Files\Autodesk\Maya2020\bin\maya.exe"')
