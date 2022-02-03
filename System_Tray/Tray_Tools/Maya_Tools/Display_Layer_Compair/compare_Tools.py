import os
import sys
import subprocess
import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds

if False:
	import PYQT
#----------------------------------------------------------------------
def open_File(file_Path):
	""""""
	cmds.file(file_Path,open=True,f=True)
	
#----------------------------------------------------------------------
def get_Display_Layers():
	""""""
	layers = cmds.ls(typ="displayLayer")
	return layers
#C:/Users/drew.loveridge/Documents/maya/projects/default/scenes/dltestB.mb
#----------------------------------------------------------------------
def get_New_Layers(old_file,new_file,prgbar=None):
	""""""
	if False:
		isinstance(prgbar,PYQT.QProgressBar)
	layer_lists = []
	if prgbar is not None:
		prgbar.setValue(0)
	for f in [old_file,new_file]:
		open_File(f)
		layer_lists.append(get_Display_Layers())
		if prgbar is not None:
			prgbar.setValue(prgbar.value()+1)
			win = prgbar.window()
			win.repaint()
			prgbar.repaint()
	old_list,new_list = [set(data) for data in layer_lists]
	
	new_layers = list(new_list.difference(old_list))
	prgbar.reset()
	new_layers.sort()
	return new_layers

#----------------------------------------------------------------------
def export_Layers(layers,file_path):
	""""""
	drawInfo_plugs = [layer+".drawInfo" for layer in layers]
	cmds.select(drawInfo_plugs)
	objects = cmds.listConnections()
	cmds.select(objects)
	cmds.file(file_path,force=True,options="v=0;",typ="mayaBinary",pr=True,es=True)

#----------------------------------------------------------------------
def open_File_GUI(file_path):
	""""""
	pip = subprocess.Popen([r"C:\Program Files\Autodesk\Maya2018\bin\maya.exe", file_path.replace("/","\\")])
