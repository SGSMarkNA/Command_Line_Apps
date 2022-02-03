import PowerPointLib
import os,sys
from PySide.QtCore import *
from PySide.QtGui  import *
#----------------------------------------------------------------------
def get_File_Dialog(label="Root Image Folder", UseNativeDialog=False, folder="", parent=None):
	""""""
	options = QFileDialog.ShowDirsOnly
	#options = QFileDialog.Options()
	#if not UseNativeDialog:
		#options |= QFileDialog.DontUseNativeDialog
	if folder == "":
		folder = os.environ["USERPROFILE"]
	FolderName = QFileDialog.getExistingDirectory(parent,label,folder,options)
	if FolderName:
		return FolderName
	else:
		return False
	
build_presets = {1: [{'Left': 10.0, 'Top': 6.048031330108643, 'Width': 940.0}],
 2: [{'Left': 0.0, 'Top': 0.0, 'Width': 467.33331298828125},
     {'Left': 492.6665344238281,
      'Top': 7.874015864217654e-05,
      'Width': 467.33306884765625}],
 3: [{'Left': 489.9477844238281, 'Top': 0.0, 'Width': 470.0522155761719},
     {'Left': 0.0, 'Top': 270.0, 'Width': 451.0667724609375},
     {'Left': 0.0, 'Top': 0.0, 'Width': 451.0667724609375}],
 4: [{'Left': 0.0, 'Top': -7.874015864217654e-05, 'Width': 424.9252624511719},
     {'Left': 535.0748291015625, 'Top': 0.0, 'Width': 424.9252014160156},
     {'Left': -7.874015864217654e-05,
      'Top': 274.6636962890625,
      'Width': 424.9252624511719},
     {'Left': 535.0748291015625,
      'Top': 274.66363525390625,
      'Width': 424.9252014160156}],
 5: [{'Left': 0.0, 'Top': 0.0, 'Width': 290.66558837890625},
     {'Left': 26.552125930786133,
      'Top': 237.8968505859375,
      'Width': 440.7536926269531},
     {'Left': 666.16943359375,
      'Top': -1.0209448337554932,
      'Width': 293.83056640625},
     {'Left': 332.6779479980469,
      'Top': -1.0209448337554932,
      'Width': 294.766845703125},
     {'Left': 483.94512939453125,
      'Top': 237.8968505859375,
      'Width': 443.1781921386719}],
 6: [{'Left': 10.454803466796875,
      'Top': 58.254173278808594,
      'Width': 291.24237060546875},
     {'Left': 335.230712890625,
      'Top': 58.56496047973633,
      'Width': 291.3354187011719},
     {'Left': 657.8152465820312,
      'Top': 58.36338424682617,
      'Width': 291.3354187011719},
     {'Left': 11.525117874145508, 'Top': 270.0, 'Width': 291.3353576660156},
     {'Left': 331.52740478515625, 'Top': 270.0, 'Width': 291.3353576660156},
     {'Left': 651.5296630859375, 'Top': 270.0, 'Width': 291.3353576660156}],
 7: [{'Left': 1.520708680152893, 'Top': 0.0, 'Width': 244.1660614013672},
     {'Left': 0.8091338872909546,
      'Top': 180.73976135253906,
      'Width': 245.58921813964844},
     {'Left': 115.42078399658203,
      'Top': 349.7503967285156,
      'Width': 261.9550476074219},
     {'Left': 263.5733947753906, 'Top': 0.0, 'Width': 245.58912658691406},
     {'Left': 527.955810546875, 'Top': 270.0, 'Width': 404.17047119140625},
     {'Left': 263.5733947753906,
      'Top': 180.73976135253906,
      'Width': 245.58912658691406},
     {'Left': 527.9559326171875,
      'Top': 7.874015864217654e-05,
      'Width': 405.6901550292969}]}


pp_app = PowerPointLib.Application()

Get_Foulders = lambda root : [p for p in [os.path.join(root,p) for p in os.listdir(root)] if os.path.isdir(p)]

Get_Files    = lambda root : [p for p in [os.path.join(root,p) for p in os.listdir(root)] if os.path.isfile(p)]

Get_Nice_File_Name = lambda path: os.path.basename(path).split(".")[0].replace("_"," ")

def Build_Presentation(base_foulder):
	base_foulder = base_foulder.replace("/","\\")
	folders = Get_Foulders(base_foulder)
	for findex, fpath in enumerate(folders):
		first_slide = True
		prez = pp_app.Presentations.Add(1)
		foulder = folders[findex]
		image_files = Get_Files(foulder)
		if len(image_files):
			for index, path in enumerate(reversed(image_files)):
				slide = prez.Slides.Add(1,12)
				file_name = Get_Nice_File_Name(path)
				pic_shape = slide.Shapes.AddPicture(path, False, True, 0, 0)
				pic_shape.ScaleHeight(1,True)
				pic_shape.Name = file_name
				
				if first_slide:
					prez.PageSetup.SlideHeight = pic_shape.Height
					prez.PageSetup.SlideWidth = pic_shape.Width
					first_slide = False
				pic_shape.Top = 0
				pic_shape.Left = 0
		pdf_file_name = os.path.basename(foulder)				
		save_file = os.path.join(foulder,pdf_file_name+".pdf")
		prez.SaveAs(save_file, FileFormat=32, EmbedTrueTypeFonts=-2)
		prez.Close()
	#pp_app.Presentations.Open(save_file, WithWindow=1)
	
#----------------------------------------------------------------------
def Add_Shape_Text():
	""""""
	prez = pp_app.ActivePresentation
	
	for slide in prez.Slides:
		isinstance(slide,PowerPointLib._Slide)
		shapes = list(slide.Shapes)
		for shape in shapes:
			txt_shape = slide.Shapes.AddTextbox(1, shape.Left, (shape.Top + shape.Height)-7, shape.Width, 50)
			txt_shape.TextFrame.TextRange.Text = shape.Name
			txt_shape.TextFrame.HorizontalAnchor = 2
			

if __name__ == '__main__':
	qt_app = QApplication(sys.argv)
	folder =  get_File_Dialog(UseNativeDialog=True)
	if folder:
		pp_app._dispobj_.Activate()
		Build_Presentation(folder)
		#Add_Shape_Text()
	sys.exit()
