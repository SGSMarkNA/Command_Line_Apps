#!/usr/bin/env python

from PySide import QtCore, QtGui

########################################################################
class Screenshot(QtGui.QWidget):
	#----------------------------------------------------------------------
	def __init__(self):
		super(Screenshot, self).__init__()
		# Master Layout
		mainLayout = QtGui.QVBoxLayout()
		
		self.screenshotLabel = QtGui.QLabel()
		self.screenshotLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.screenshotLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.screenshotLabel.setMinimumSize(240, 160)
		
		self.createOptionsGroupBox()
		self.createButtonsLayout()
		
		mainLayout.addWidget(self.screenshotLabel)
		mainLayout.addWidget(self.optionsGroupBox)
		mainLayout.addLayout(self.buttonsLayout)
		
		self.setLayout(mainLayout)
		
		self.shootScreen()
		
		self.delaySpinBox.setValue(5)
		
		self.setWindowTitle("Screenshot")
		self.resize(300, 200)
	#----------------------------------------------------------------------
	def resizeEvent(self, event):
		scaledSize = self.originalPixmap.size()
		scaledSize.scale(self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio)
		if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
			self.updateScreenshotLabel()
	#----------------------------------------------------------------------
	def newScreenshot(self):
		if self.hideThisWindowCheckBox.isChecked():
			self.hide()
		self.newScreenshotButton.setDisabled(True)

		QtCore.QTimer.singleShot(self.delaySpinBox.value() * 1000,
				                 self.shootScreen)
	#----------------------------------------------------------------------
	def saveScreenshot(self):
		format = 'jpg'
		initialPath = QtCore.QDir.currentPath() + "/untitled." + format

		fileName,_ = QtGui.QFileDialog.getSaveFileName(self, "Save As",
				                                       initialPath,
				                                       "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
		if fileName:
			self.originalPixmap.save(fileName, format)
	#----------------------------------------------------------------------
	def shootScreen(self):
		if self.delaySpinBox.value() != 0:
			QtGui.qApp.beep()

		# Garbage collect any existing image first.
		self.originalPixmap = None
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
		self.updateScreenshotLabel()

		self.newScreenshotButton.setDisabled(False)
		if self.hideThisWindowCheckBox.isChecked():
			self.show()
	#----------------------------------------------------------------------
	def updateCheckBox(self):
		if self.delaySpinBox.value() == 0:
			self.hideThisWindowCheckBox.setDisabled(True)
		else:
			self.hideThisWindowCheckBox.setDisabled(False)
	#----------------------------------------------------------------------
	def createOptionsGroupBox(self):
		self.optionsGroupBox = QtGui.QGroupBox("Options")

		self.delaySpinBox = QtGui.QSpinBox()
		self.delaySpinBox.setSuffix(" s")
		self.delaySpinBox.setMaximum(60)
		self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

		self.delaySpinBoxLabel = QtGui.QLabel("Screenshot Delay:")

		self.hideThisWindowCheckBox = QtGui.QCheckBox("Hide This Window")

		optionsGroupBoxLayout = QtGui.QGridLayout()
		optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
		optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
		optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
		self.optionsGroupBox.setLayout(optionsGroupBoxLayout)
	#----------------------------------------------------------------------
	def createButtonsLayout(self):
		self.newScreenshotButton  = self.createButton("New Screenshot",self.newScreenshot)
		self.saveScreenshotButton = self.createButton("Save Screenshot",self.saveScreenshot)
		self.quitScreenshotButton = self.createButton("Quit", self.close)
		
		self.buttonsLayout = QtGui.QHBoxLayout()
		self.buttonsLayout.addStretch()
		self.buttonsLayout.addWidget(self.newScreenshotButton)
		self.buttonsLayout.addWidget(self.saveScreenshotButton)
		self.buttonsLayout.addWidget(self.quitScreenshotButton)
	#----------------------------------------------------------------------
	def createButton(self, text, member):
		button = QtGui.QPushButton(text)
		button.clicked.connect(member)
		return button
	#----------------------------------------------------------------------
	def updateScreenshotLabel(self):
		self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
			self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation))


if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	screenshot = Screenshot()
	screenshot.show()
	sys.exit(app.exec_())
