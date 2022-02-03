import os
import sys
os.sys.path.append(r"\\isln-smb\aw_config\Git_Live_Code\Global_Systems")
import PYQT
#----------------------------------------------------------------------
def get_File_Dialog(label="File Finder", UseNativeDialog=False, folder="", parent=None):
	""""""
	options = PYQT.QFileDialog.Options()
	# options |= PYQT.QFileDialog.Option.
	if not UseNativeDialog:
		options |= PYQT.QFileDialog.DontUseNativeDialog
	if folder == "":
		folder = os.environ["USERPROFILE"]
	fileName, filtr = PYQT.QFileDialog.getOpenFileName(parent,label,folder,"All Files (*);;Maya Binary(*.mb);;Maya Asci(*.ma)", "Maya Files (*.mb,*.ma)", options)
	if fileName:
		return fileName
	else:
		return False
########################################################################
class _CODE_COMPLEATION_HELPER(PYQT.QMainWindow):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,parent=None):
		''''''
		super(_CODE_COMPLEATION_HELPER,self).__init__(parent=parent)
		if False:
			self.Display_Layer_Conpare = Display_Layer_Compare_Main_Window()
			self.centralwidget = PYQT.QWidget()
			self.groupBox = PYQT.QGroupBox()
			self.UseNativeDialog = PYQT.QCheckBox()
			self.Create_New_File_CheckBox = PYQT.QCheckBox()
			self.Open_New_File_CheckBox = PYQT.QCheckBox()
			self.Files_Input_GroupBox = PYQT.QGroupBox()
			self.Old_File_Label = PYQT.QLabel()
			self.Old_File_Input = PYQT.QLineEdit()
			self.Old_File_Button = PYQT.QPushButton()
			self.New_File_Label = PYQT.QLabel()
			self.New_File_Input = PYQT.QLineEdit()
			self.New_File_Button = PYQT.QPushButton()
			self.Compare_Button = PYQT.QPushButton()
			self.progressBar = PYQT.QProgressBar()
			self.New_Layers_GroupBox = PYQT.QGroupBox()
			self.New_Layers_Display = PYQT.QPlainTextEdit()
			self.menubar = PYQT.QMenuBar()
			self.statusbar = PYQT.QStatusBar()
			
########################################################################
class Display_Layer_Compare_Main_Window(_CODE_COMPLEATION_HELPER):
	""""""

	#----------------------------------------------------------------------
	def __init__(self,parent=None):
		"""Constructor"""
		super(Display_Layer_Compare_Main_Window,self).__init__(parent)
	#----------------------------------------------------------------------
	def _run_setup(self):
		""""""
		self.Old_File_Button.clicked.connect(self.get_old_file)
		self.New_File_Button.clicked.connect(self.get_new_file)
		self.Compare_Button.clicked.connect(self.do_Compare)
	#----------------------------------------------------------------------
	def get_old_file(self):
		""""""
		current_old_folder = ""
		current_old_file = self.Old_File_Input.text()
		
		if len(current_old_file):
			current_old_folder = os.path.dirname(current_old_file)
			if not os.path.exists(current_old_folder):
				current_old_folder = ""
			
		res = get_File_Dialog(label="Old Maya File", UseNativeDialog=self.UseNativeDialog.isChecked(), folder=current_old_folder, parent=self)
		if res:
			self.Old_File_Input.setText(res)
	#----------------------------------------------------------------------
	def get_new_file(self):
		""""""
		current_old_folder = ""
		current_old_file = self.Old_File_Input.text()
		current_new_folder = ""
		current_new_file = self.New_File_Input.text()
		
		if len(current_new_file):
			current_new_folder = os.path.dirname(current_new_file)
			if not os.path.exists(current_new_folder):
				current_new_folder = ""
			
		if current_new_folder == "":
			if len(current_old_file):
				current_new_folder = os.path.dirname(current_old_file)
				if not os.path.exists(current_new_folder):
					current_new_folder = ""
					
		res = get_File_Dialog(label="New Maya File", UseNativeDialog=self.UseNativeDialog.isChecked(), folder=current_new_folder, parent=self)
		if res:
			self.New_File_Input.setText(res)
	#----------------------------------------------------------------------
	def do_Compare(self):
		""""""
		old_file = self.Old_File_Input.text()
		new_file = self.New_File_Input.text()
		layers = compare_Tools.get_New_Layers(old_file, new_file, prgbar=self.progressBar)
		self.New_Layers_Display.clear()
		self.New_Layers_Display.appendPlainText("\n".join(layers))
		#if os.path.exists(old_file) and os.path.exists(new_file):
			#layers = compare_Tools.get_New_Layers(old_file,new_file,self.progressBar)
			#self.New_Layers_Display.clear()
			#self.New_Layers_Display.appendPlainText("\n".join(layers))
			#if self.Create_New_File_CheckBox.isChecked():
				#new_file_path = os.path.splitext(new_file)[0]+"_Extrated_Layers.mb"
				#compare_Tools.export_Layers(layers, new_file_path)
				#if self.Open_New_File_CheckBox.isChecked():
					#compare_Tools.open_File_GUI(new_file_path)
PYQT.GUI_Loader.registerCustomWidget(Display_Layer_Compare_Main_Window)
	
#----------------------------------------------------------------------
def main():
	""""""
	import compare_Tools
	current_dir = os.path.dirname(__file__)
	file_path = os.path.join(current_dir,"Display_Layer_Compair_Main_Window.ui")
	window = PYQT.GUI_Loader.load_file(file_path)
	window._run_setup()
	return window
if __name__ == '__main__':
	app = PYQT.QApplication(sys.argv)
	import compare_Tools
	win = main()
	win.show()
	sys.exit(app.exec_())
