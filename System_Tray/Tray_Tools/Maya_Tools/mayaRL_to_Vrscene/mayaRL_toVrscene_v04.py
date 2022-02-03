import maya.standalone
import maya.cmds as cmds
import sys

sys.path.append('C:\\Program Files\\Autodesk\\Maya2018\\vray\\scripts')


fileToOpen = sys.argv[1]
workingDir = sys.argv[2]
renderLayer = sys.argv[3]
renderCamera = sys.argv[4]
vrayScene = sys.argv[5]
mayaFrameStart = int(sys.argv[6])
mayaFrameEnd = int(sys.argv[7])
vraySceneAsFrames = sys.argv[8]
project = sys.argv[9]

def mayaRLtoVrscene():
	### Open maya 
	maya.standalone.initialize(name='python')
	import pymel.core as pm
		
	### force source mel scripts
	###pm.mel.eval('source "vrayMatOverride.mel"')
	
	### Set project
	cmds.workspace(project, o=True)
	
	### Open the file
	cmds.file(fileToOpen, force=True, open=True, loadAllReferences=True)
	
	### Grab all the vray settings for later
	vraySettings = pm.ls('vraySettings')
	
	### Set all cameras to not render
	cameraList = pm.ls(type='camera')
	for singleCamera in cameraList:
		pm.setAttr(singleCamera+'.renderable', 0)	
	
	### Set the input camera to renderable
	pm.setAttr(renderCamera+'.renderable', 1)

	fileName = pm.sceneName().basename()
	fileName = fileName[:-3]
	
	### set the renderlayer for output
	activeLayer = pm.nt.RenderLayer.findLayerByName(renderLayer)
	activeLayer.setCurrent()
	
	### setup the frame range
	pm.setAttr('defaultRenderGlobals.fs', mayaFrameStart)
	pm.setAttr('defaultRenderGlobals.ef', mayaFrameEnd)
	
	### run any pre render layer mel scripts because vrend does eval that
	preRenderScript =  pm.getAttr('defaultRenderGlobals.preRenderLayerMel')
	### I'm not sure why sometimes maya returns a 0.0 or a None sometimes... hope future me figures this out
	if preRenderScript == 0.0:
		print("I'm a zero")
	if preRenderScript == None:
		print("I'm a none")
	else:
		pm.mel.eval(preRenderScript)
		print(("preRender ", preRenderScript))
		print(("vrayPython ", pm.getAttr('vraySettings.postTranslatePython')))
	
	### Get the image name from the render Settings
	### now provided by the ui settings
	###fileNamePrefix = pm.getAttr('vraySettings.fileNamePrefix')

	### Set the the Layer tags in the file name prefix so it doesnt add the renderlayer on it's own
	pm.setAttr('vraySettings.fileNamePrefix', '<Layer>/Output_<Layer>_', type='string')	
	
	
	### set the file prefix to the vrayscene
	pm.setAttr('vraySettings.fileNamePrefix', vrayScene)	

	#### Turn off animation batch only, so you get animated vrayscene
	pm.setAttr('vraySettings.animBatchOnly', 0)
	
	#### Sequencal Vrscene files
	if vraySceneAsFrames == "True":
		pm.setAttr('vraySettings.misc_eachFrameInFile',1)
	if vraySceneAsFrames == "False":
		pm.setAttr('vraySettings.misc_eachFrameInFile',0)
	
	#### Turn this off because of pete and people like pete
	pm.setAttr('vraySettings.dmcShowSamples', 0)
	 
	### Set the vray export settings and vrscene out path
	pm.setAttr('vraySettings.fileNamePadding', 4)
	pm.setAttr('vraySettings.vrscene_render_on', 0)
	pm.setAttr('vraySettings.vrscene_on', 1)
	pm.setAttr('vraySettings.vrscene_filename', vrayScene)
	
	outMessage = pm.getAttr('vraySettings.vrscene_filename')
	print(("Vray Scene File Name:", outMessage))
	
	### Export the vrscene
	pm.vrend(camera=renderCamera, layer=renderLayer)
	
	### Quit
	cmds.quit(abort=True)

if __name__=='__main__':
	mayaRLtoVrscene()