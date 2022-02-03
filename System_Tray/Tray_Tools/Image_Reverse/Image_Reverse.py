import glob
import os
import re
import platform
import shutil
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
name_num_ext_pattern = re.compile(r"(?P<name>[A-Za-z_-]+)(?P<number>[0-9]+)(\W)(?P<ext>\w+)")

#----------------------------------------------------------------------
def Assine_Version_Frame_Data(filename):
	""""""
	path_to_frames = filename
	slices = path_to_frames.split(".")
	file_ext       = slices[-1]
	file_path      = ".".join(slices[:-1])
	file_base_name = os.path.basename(file_path)
	file_base_name = file_base_name.replace("#", "")
	folder_name    = os.path.dirname(file_path)
	files = glob_file_matchs(folder_name, file_base_name, file_ext)
	start, end = determan_start_end(files)
	frame_count = len(files)
	frame_range = "%i-%i" % (start, end)
	print files
	print frame_range, start, end, frame_count
	
def filenameFix(filename):
	return filename.replace( "\\", "/" )

def file_seq_dict(root_folder,res={}):
	
	root, dirs, files = os.walk(root_folder).next()
	
	for d in dirs:
		print d
		child_folder = filenameFix(os.path.join(root,d))
		
		image_files = os.walk(child_folder).next()[2]
		
		if len(image_files):
			res[d]=construct_image_seq_data(child_folder,image_files)
		else:
			res[d] = {}
			
		file_seq_dict(child_folder,res[d])
	
	return res
	
def construct_image_seq_data(root,files):
	seqBuilder = {}
	if len(files):
		
		file_names = []
		
		for f in files:
			print "\t",f
			
			match = name_num_ext_pattern.match(f)
			
			if match and match.group() == f:
				
				groups = match.groupdict()
				
				name, padding, ext   = groups["name"], len(groups["number"]), groups["ext"]
				
				if not name in file_names:
					
					file_names.append(name)
					
					seqBuilder[name]=construct_image_seq_dict(os.path.join(root,f))			
	return seqBuilder

def construct_file_sequence_expression(folder_path,file_name,frame_padding,file_extension):
	name = file_name + ".%0" + str(frame_padding) + "d." + file_extension
	expr = os.path.join(folder_path,name)
	
	return filenameFix(expr)

def glob_file_matchs(folder_name,file_base_name,file_ext):
	
	glob_pattern = os.path.join( folder_name, str( file_base_name + "*." + file_ext ) )
	
	matching_paths = glob.glob(glob_pattern)
	matching_paths.sort()
	
	return matching_paths

def paths_to_names(file_paths):
	names = [os.path.basename(f) for f in file_paths]
	return names

def determan_start_end(file_paths):
	
	file_names = paths_to_names(file_paths)
	
	ints = []
	for f in file_names:
		m = name_num_ext_pattern.match(f)
		if m is None:
			ints.append(int(f.split(".")[0].split("_")[-1]))
		else:
			ints.append(int(m.groupdict()["number"]))
	
	if len(ints):
		start = min(ints)
		
		end   = max(ints)
		
		return start,end
	return 0,0

def construct_image_seq_dict(path,as_Nuke_Knobs=False,as_tcl=False):
	if not os.path.exists(path):
		raise ValueError("The input path %s does not exist" % path)
	for item in os.listdir(path):
		item = os.path.join(path,item)
		if not os.path.isdir(item):
			path = filenameFix(item)
			break
	
	name,number,ext = None,None,None
	
	file_name    = os.path.basename(path)
	
	folder_name  = os.path.dirname(path)
	
	match        = name_num_ext_pattern.match(file_name)
	if not match or not match.group() == file_name:
		ext     = file_name.split(".")[-1]
		file_name = file_name.replace("."+ext,"")
		padding = file_name.split("_")[-1]
		name    = file_name.replace(padding,"")
		padding = len(padding)
	else:		
		groups = match.groupdict()
		
		name, padding, ext   = groups["name"], len(groups["number"]), groups["ext"]
	
	matching_paths = glob_file_matchs(folder_name,name,ext)
	
	file_count = len(matching_paths)
	
	start_knob,end_knob = determan_start_end(matching_paths)
	
	file_knob = construct_file_sequence_expression(folder_name,name,padding,ext)
	matching_paths = [filenameFix(m) for m in matching_paths]
	if as_Nuke_Knobs:
		knob_values = dict(file=file_knob,
		                   name=name,
		                   cacheLocal="always",
		                   on_error="black",
		                   origfirst=start_knob,
		                   origlast=end_knob,
		                   last=end_knob,
		                   first=start_knob,
		                   origset=True)
		if as_tcl:
			tcl = ""
			for k,v in knob_values.items():
				if v == True:
					tcl += "%s true " % k
				elif v == False:
					tcl += "%s false " % k
				else:
					tcl += "%s %r " % (k,v)
			return tcl
	
		return knob_values
	
	else:
		res = file_sequence()
		res.file_count   = file_count
		res.file_ext     = ext
		res.file_expr    = file_knob
		res.folder_path  = folder_name
		res.file_padding = padding
		res.file_paths   = matching_paths
		res.file_name    = name
		res.last_frame   = end_knob
		res.first_frame  = start_knob
		return res
	
class file_sequence(object):
	def __init__(self):
		self.file_name    = ""
		self.file_count   = 0
		self.file_padding = 0
		self.file_ext     = ""
		self.last_frame   = 0
		self.first_frame  = 0
		self.file_expr    = ''
		self.file_paths   = []
		self.folder_path  = ''
	#----------------------------------------------------------------------
	def reverse_Seq(self,progressBar,do_offset=False):
		""""""
		isinstance(progressBar,QProgressBar)
		dest_folder = os.path.join(self.folder_path,"Reversed")
		if not os.path.exists(dest_folder):
			os.makedirs(dest_folder)
		reversed_paths = [os.path.join(dest_folder,os.path.basename(item)) for item in reversed(self.file_paths)]
		progressBar.setValue(0)
		progressBar.setMaximum(self.file_count)
		progressBar.setMinimum(0)
		for index in range(len(self.file_paths)):
			src = self.file_paths[index]
			if index == 0 and do_offset:
				dest = reversed_paths[-1]
			elif reversed_paths[index] == reversed_paths[-1] and do_offset:
				dest = reversed_paths[0]
			else:
				dest = reversed_paths[index]
			shutil.copyfile(src, dest)
			progressBar.setValue(progressBar.value()+1)

class UiLoader(QUiLoader):
	''''''
	def __init__(self,*args,**kwargs):
		''''''
		super(UiLoader,self).__init__(*args,**kwargs)
		self._custom_wigets = dict()
		self._wigs = []
	#----------------------------------------------------------------------
	def createWidget(self,className,parent=None,name=None):
		"""
		createWidget(className,parent=None,name=None)
			className=unicode
			parent=QtGui.QWidget
			name=unicode

		Creates a new widget with the given parent and name using the class specified by className
		You can use this function to create any of the widgets returned by the PySide.QtUiTools.QUiLoader.availableWidgets() function.
		The function is also used internally by the PySide.QtUiTools.QUiLoader class whenever it creates a widget
		Hence, you can subclass PySide.QtUiTools.QUiLoader and reimplement this function to intervene process of constructing a user interface or widget
		However, in your implementation, ensure that you call PySide.QtUiTools.QUiLoader s version first.
		"""
		if className in self._custom_wigets:
			res = self._custom_wigets[className](parent=parent)
			res.setObjectName(name)
		else:
			res = super(UiLoader,self).createWidget(className,parent,name)
		isinstance(res,QWidget)
		self._wigs.append(res)
		return res
	#----------------------------------------------------------------------
	def load_file(self, file_path, parent_widget=None):
		""""""
		Qfile = QFile(file_path)
		Qfile.open(QFile.ReadOnly)
		ui_wig = self.load(Qfile,parent_widget)
		Qfile.close()
		return ui_wig
	#----------------------------------------------------------------------
	def registerCustomWidget(self,customWidgetType):
		"""
		registerCustomWidget(customWidgetType)
			customWidgetType=Object

		Registers a Python created custom widget to QUiLoader, so it can be recognized when
		loading a .ui file
		The custom widget type is passed via the customWidgetType argument.
		This is needed when you want to override a virtual method of some widget in the interface,
		since duck punching will not work with widgets created by QUiLoader based on the contents
		of the .ui file.
		(Remember that duck punching virtual methods is an invitation for your own demise!)
		Lets see an obvious example
		If you want to create a new widget its probable youll end up
		overriding QWidgets paintEvent() method.
		"""
		self._custom_wigets[customWidgetType.__name__] = customWidgetType
		res = super(UiLoader,self).registerCustomWidget(customWidgetType)
		return res
	
Loader = UiLoader()
			
class Image_Reverse_Dialog(QDialog):
	#----------------------------------------------------------------------
	def __init__(self,parent=None):
		""""""
		super(Image_Reverse_Dialog,self).__init__(parent=parent)
		if False:
			self.folderLineEdit = QLineEdit
			self.create_rev_seq_Button = QPushButton
			self.Run_Scan_Button = QPushButton
			self.end_frame_input = QSpinBox
			self.frame_padding_input = QSpinBox
			self.start_frame_input   = QSpinBox
			self.frame_count_input   = QSpinBox
			self.file_name_input     = QLineEdit
			self.file_ext_input      = QLineEdit
			self.account_for_looping = QCheckBox
			
	#----------------------------------------------------------------------
	def run_setup(self):
		""""""
		
	#----------------------------------------------------------------------
	def reset_scan_data(self):
		""""""
		self.end_frame_input.setValue(0)
		self.frame_padding_input.setValue(0)
		self.start_frame_input.setValue(0)
		self.frame_count_input.setValue(0)
		self.file_name_input.setText("")
		self.file_ext_input.setText("")
		self.create_rev_seq_Button.setEnabled(False)
	#----------------------------------------------------------------------
	@Slot()
	def on_folder_changed(self):
		""""""
		if os.path.exists(self.folderLineEdit.text()):
			self.Run_Scan_Button.setEnabled(True)
		else:
			self.Run_Scan_Button.setEnabled(False)
		self.reset_scan_data()
	#----------------------------------------------------------------------
	@Slot()
	def get_Image_Seq_Folder(self):
		options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
		if not self.folderLineEdit.text() == "":
			current_folder = os.path.dirname(self.folderLineEdit.text())
		else:
			current_folder = os.environ["USERPROFILE"]
		folder = QFileDialog.getExistingDirectory(self,"Image Folder", str(current_folder), options)
		if folder:
			self.folderLineEdit.setText(folder)
	
	#----------------------------------------------------------------------
	@Slot()
	def do_Folder_Scan(self):
		""""""
		try:
			val = self.folderLineEdit.text()
			self._scan_data = construct_image_seq_dict(val)
			self.end_frame_input.setValue(self._scan_data.last_frame)
			self.frame_padding_input.setValue(self._scan_data.file_padding)
			self.start_frame_input.setValue(self._scan_data.first_frame)
			self.frame_count_input.setValue(self._scan_data.file_count)
			self.file_name_input.setText(self._scan_data.file_name)
			self.file_ext_input.setText(self._scan_data.file_ext)
			self.create_rev_seq_Button.setEnabled(True)
		except:
			self.create_rev_seq_Button.setEnabled(False)
			
	#----------------------------------------------------------------------
	@Slot()
	def do_Create_Rev_Image_Sequences(self):
		""""""
		self._scan_data.reverse_Seq(self.progressBar,self.account_for_looping.isChecked())
		self.reset_scan_data()
			
Loader.registerCustomWidget(Image_Reverse_Dialog)

if __name__ == "__main__":
	app = QApplication(os.sys.argv)
	ui_file = os.path.join(os.path.dirname(__file__),"Reverse.ui")
	main_window = Loader.load_file(ui_file)
	main_window.show()
	
	os.sys.exit(app.exec_())