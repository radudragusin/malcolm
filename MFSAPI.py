#!/usr/bin/env python

"""
This is the module responsible for the communication between the product and the external world. 
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_MFSGUI
import os.path
import os
import platform
import MFSCore
import cPickle
import xattr
import re
import time
import subprocess
import shutil

__version__ = "0.0.1"

class MFSAPI(QMainWindow, ui_MFSGUI.Ui_MainWindow):
	def __init__(self,parent=None):
		"""Initializes the main window of the application and connects the application's 
		events with its logic part.
		"""
		
		super(MFSAPI,self).__init__(parent)
		self.setupUi(self)
		
		self.model = QStringListModel()
		self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.started = False
		
		self.readSettings()

		self.connect(self.pushButton_2, SIGNAL("clicked()"), self.updateMountPointSource)
		self.connect(self.pushButton, SIGNAL("clicked()"), self.updateMountPointDest)
		self.connect(self.pushButton_7, SIGNAL("clicked()"), self.updateFileSelection)
		self.connect(self.pushButton_8, SIGNAL("clicked()"), self.updateDirSelection)
		self.connect(self.lineEdit_3, SIGNAL("textChanged(QString)"), self.showFileSettings)
		self.connect(self.pushButton_10, SIGNAL("clicked()"), self.startMFS)
		self.connect(self.pushButton_11, SIGNAL("clicked()"), self.stopMFS)
		self.connect(self.actionAbout, SIGNAL("triggered()"), self.showAbout)
		self.connect(self.pushButton_12, SIGNAL("clicked()"), self.saveSettings)
		self.connect(self.radioButton, SIGNAL("clicked()"), self.saveCheckedrb1)
		self.connect(self.radioButton_2, SIGNAL("clicked()"), self.saveCheckedrb2)
		self.connect(self.spinBox, SIGNAL("valueChanged(int)"), self.saveSpinnedsb1)
		self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.saveMountPointSrc)
		self.connect(self.lineEdit_2, SIGNAL("textChanged(QString)"), self.saveMountPointDest)
		self.connect(self.pushButton_9, SIGNAL("clicked()"), self.updateFileSelectionForOp)
		self.connect(self.pushButton_13, SIGNAL("clicked()"), self.updateDirSelectionForOp)
		self.connect(self.lineEdit_4, SIGNAL("textChanged(QString)"), self.showFileVersions)
		self.connect(self.listView, SIGNAL("clicked(QModelIndex)"), self.updateOperationsButtons)
		self.connect(self.pushButton_3, SIGNAL("clicked()"), self.viewFileVersionInfo)
		self.connect(self.pushButton_4, SIGNAL("clicked()"), self.openFileVersion)
		self.connect(self.pushButton_6, SIGNAL("clicked()"), self.deleteFileVersion)
		self.connect(self.pushButton_5, SIGNAL("clicked()"), self.restoreFileVersion)

	#FIRST TAB FUNCTIONALITIES

	def readSettings(self):
		"""Called when the main window is initoalized. Reads and stores the information from the 
		settings file (if any), and populates the first tab of the application.
		"""
		if os.path.isfile("settings.MMFS"):
			f = open("settings.MMFS","r")
			MFSCore.MFSConfig = cPickle.load(f)
			f.close()
		elif QDesktopServices.displayName(QDesktopServices.DocumentsLocation) != "":
			MFSCore.MFSConfig['mountpoint_source'] = QDesktopServices.displayName(QDesktopServices.DocumentsLocation)
		#get default source and dest mountpoint
		self.lineEdit.setText(MFSCore.MFSConfig['mountpoint_source'])
		self.lineEdit_2.setText(MFSCore.MFSConfig['mountpoint_dest'])
		#get enabled/disabled versioning property
		if MFSCore.MFSConfig['versioning_enabled'] == 'true':
			self.radioButton.setChecked(True)
			self.radioButton_2.setChecked(False)
		else:
			self.radioButton.setChecked(False)
			self.radioButton_2.setChecked(True)
		#get max no of versions property
		self.spinBox.setValue(int(MFSCore.MFSConfig['max_no_versions']))

	def updateMountPointSource(self):
		"""Opens a file browsing window for selection of the mounting point source path.
		"""
		filename = QFileDialog.getExistingDirectory(self, "Select Mount Point Source", self.browsingStartPoint(),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if filename != "": 
			self.lineEdit.setText(filename)

	def updateMountPointDest(self):
		"""Opens a file browsing window for selection of the mounting point destination path.
		"""
		filename = QFileDialog.getExistingDirectory(self, "Select Mount Point Destination", self.browsingStartPoint(),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if filename != "":
			self.lineEdit_2.setText(filename)
		
	def saveCheckedrb1(self):
		""""Sets the value of the general 'versioning_enabled' setting to 'true'. """
		MFSCore.MFSConfig['versioning_enabled'] = 'true'
	def saveCheckedrb2(self):
		""""Sets the value of the general 'versioning_enabled' setting to 'false'. """
		MFSCore.MFSConfig['versioning_enabled'] = 'false'
	def saveSpinnedsb1(self):
		""""Sets the value of the general 'max_no_versions' setting to the value from the spinBox. """
		MFSCore.MFSConfig['max_no_versions'] = self.spinBox.value()
	def saveMountPointSrc(self):
		""""Sets the value of the general 'mountpoint_source' setting to the current selected path."""
		MFSCore.MFSConfig['mountpoint_source'] = os.path.normpath(str(self.lineEdit.text()))
	def saveMountPointDest(self):
		""""Sets the value of the general 'mountpoint_dest' setting to the current selected path."""
		MFSCore.MFSConfig['mountpoint_dest'] = os.path.normpath(str(self.lineEdit_2.text()))
			
	#SIDE BUTTONS AND MENU FUNCTIONALITY
		
	def startMFS(self):
		"""Creates a new thread for the filesystem to be mounted.
		If the mounting paths are the same, or are empty, a warning message box will be opened, and the filesystem will not start
		"""
		pathSrc = os.path.normpath(str(self.lineEdit.text()))
		pathDest = os.path.normpath(str(self.lineEdit_2.text()))
		if os.path.exists(pathSrc) and os.path.exists(pathDest) and pathSrc != pathDest and pathSrc != "" and pathDest != "":
			self.groupBox.setEnabled(False)
			self.pushButton_10.setEnabled(False)
			self.filesystem = FileSystem(self)
			self.filesystem.initialize(pathSrc,pathDest,True)
			self.filesystem.start()
			self.pushButton_11.setEnabled(True)
			self.started = True
		else:
			self.givePathWarning("The filesystem's mounting paths are not valid!",
			"The two strings must be valid paths that do not point to the same location, and neither of them should be empty.")
		
	def stopMFS(self):
		"""Unmounts the filesystem.
		"""
		os.system("fusermount -u " + os.path.normpath(str(self.lineEdit_2.text())))
		self.groupBox.setEnabled(True)
		self.pushButton_10.setEnabled(True)
		self.pushButton_11.setEnabled(False)
		self.started = False
		
	def showAbout(self):
		"""Opens a message box containg application information.
		"""
		QMessageBox.about(self, "About MalcolmFS",
			"""<b>MalcolmFS</b> v %s
			<p>A stackable versioning file system implemented in Python.
			<p><a href="http://code.google.com/p/malcolm">MalcolmFS Web Site</a>
			<p>Copyright &copy; 2010. 
			Radu Dragusin, Paula Petcu, Kostas Rutkauskas.
			<p>Code License: <a href="http://www.creativecommons.org/licenses/MIT/">MIT License</a>
			<p>Python %s -Qt %s -PyQt %s on %s"""
			% (__version__,platform.python_version(),QT_VERSION_STR,PYQT_VERSION_STR,platform.system()))
			
	def closeEvent(self,event):
		"""Called either when the Quit button or the X is pressed. Unmounts the filesystem before exiting.
		"""
		if self.started == True:
			self.stopMFS()
		event.accept()
	
	def saveSettings(self):
		"""Logic for the Save button in the interface.
		For the first tab, it will save the general settings.
		For the second, it will save settings per selected file/dir.
		For the third, as there is nothing to be saved, it will save the general settings (like for the first tab).
		"""
		if self.tabWidget.currentIndex() != 1:
			#in first tab or in the third (General Settings or Per File Operations)
			if os.path.exists(MFSCore.MFSConfig['mountpoint_source']) and os.path.exists(MFSCore.MFSConfig['mountpoint_dest']) and MFSCore.MFSConfig['mountpoint_source'] != MFSCore.MFSConfig['mountpoint_dest']:
				f = open("settings.MMFS", "w")
				cPickle.dump(MFSCore.MFSConfig,f)
				f.close()
			else:
				self.givePathWarning("The filesystem's mounting paths are not valid!",
				"The two strings must be valid paths that do not point to the same location, and neither of them should be empty.")
		else:
			#in the second tab (Per File Settings)
			path = str(self.lineEdit_3.text())
			if os.path.exists(path):
				self.setFileXAttr(path)
				
	def setFileXAttr(self, path):
		"""Method for setting xatrributes for the given path (a file or directory).
		"""
		path = os.path.join(MFSCore.MFSConfig['mountpoint_source'],os.path.relpath(str(path),MFSCore.MFSConfig['mountpoint_dest']))
		path = os.path.normpath(path)
		attrfile = xattr.xattr(path)
		if self.radioButton_4.isChecked() == True:
			attrfile.set('user.versioning_enabled', 'true')
		elif self.radioButton_3.isChecked() == True:
			attrfile.set('user.versioning_enabled', 'false')
		attrfile.set('user.max_no_versions',str(self.spinBox_4.value()))	
			
	#SECOND TAB FUNCTIONALITIES
			
	def updateFileSelection(self):
		"""Opens a file browsing window for selection of a file.
		"""
		filename = QFileDialog.getOpenFileName(self, "Select File", self.browsingStartPoint())
		if filename != "":
			self.lineEdit_3.setText(filename)
		
	def updateDirSelection(self):
		"""Opens a file browsing window for selection of a directory.
		"""
		filename = QFileDialog.getExistingDirectory(self, "Select Directory", self.browsingStartPoint(),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if filename != "":
			self.lineEdit_3.setText(filename)
			
	def showFileSettings(self, path):
		"""Contains most of the functionality for the second tab, by showing the versioning properties of a file or directory.
		"""
		path = os.path.normpath(str(path))
		if os.path.exists(path) and '.MFS' not in path:
			if (self.started == True and os.path.commonprefix([path,MFSCore.MFSConfig['mountpoint_dest']]) == MFSCore.MFSConfig['mountpoint_dest']) or self.started == False:
				if self.started == True:
					path = os.path.join(MFSCore.MFSConfig['mountpoint_source'],os.path.relpath(str(path),MFSCore.MFSConfig['mountpoint_dest']))
					path = os.path.normpath(path)
				attrfile = xattr.xattr(path)
				self.groupBox_3.setEnabled(True)
				#get enabled/disabled versioning property
				if 'user.versioning_enabled' in attrfile:
					if attrfile.get('user.versioning_enabled') == 'true':
						self.radioButton_4.setChecked(True)
						self.radioButton_3.setChecked(False)
					else:
						self.radioButton_4.setChecked(False)
						self.radioButton_3.setChecked(True)
				else:
					if MFSCore.MFSConfig['versioning_enabled'] == 'true':
						self.radioButton_4.setChecked(True)
						self.radioButton_3.setChecked(False)
					else:
						self.radioButton_4.setChecked(False)
						self.radioButton_3.setChecked(True)
				#get max no of versions property
				if 'user.max_no_versions' in attrfile:
					self.spinBox_4.setValue(int(attrfile.get('user.max_no_versions')))
				else:
					self.spinBox_4.setValue(int(MFSCore.MFSConfig['max_no_versions']))
			else:
				#give warning and autocomplete lineEdit_3
				self.givePathWarning("The path must be within the filesystem!",
				"When the system is started, you can only change properties of the files and folders within the mountpoint destination path.")
				self.lineEdit_3.setText(MFSCore.MFSConfig['mountpoint_dest'])
		else:
			self.groupBox_3.setEnabled(False)
	
	#THIRD TAB FUNCTIONALITIES
	
	def updateFileSelectionForOp(self):
		"""Opens a file browsing window for selection of a file.
		"""
		filename = QFileDialog.getOpenFileName(self, "Select File", self.browsingStartPoint())
		if filename != "":
			self.lineEdit_4.setText(filename)
		
	def updateDirSelectionForOp(self):
		"""Opens a file browsing window for selection of a directory.
		"""
		filename = QFileDialog.getExistingDirectory(self, "Select Directory", self.browsingStartPoint(),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if filename != "":
			self.lineEdit_4.setText(filename)
	
	def showFileVersions(self, path):
		"""Contains most of the functionality for the third tab, by showing the versions of a selected file or directory.
		Here the list of versions is populated with names.
		"""
		path = os.path.normpath(str(path))
		if os.path.exists(path) and '.MFS' not in path:	
			if (self.started == True and os.path.commonprefix([path,MFSCore.MFSConfig['mountpoint_dest']]) == MFSCore.MFSConfig['mountpoint_dest']) or self.started == False:
				if path[-1] == os.sep:
					(path,file) = os.path.split(path[1:-1])
				else:
					(path,file) = os.path.split(path)
				path = os.path.normpath(path)
				self.versionedPath = path
				if self.started == True:
					path = os.path.join(MFSCore.MFSConfig['mountpoint_source'], os.path.relpath(path,MFSCore.MFSConfig['mountpoint_dest']))
					path = os.path.normpath(path)
				self.operationPath = path
				self.browsedFile = file
				
				files = os.listdir(path)
				r = re.compile("^\."+file+"-....-..-..-..-..-..\.MFS$")
				versions = filter(r.search, files)
			
				if len(versions) > 0:
					self.listView.setEnabled(True)
					self.model.setStringList(versions)
					self.listView.setModel(self.model)
					self.groupBox_5.setEnabled(False)
				else:
					self.listView.setEnabled(False)
					self.model.setStringList([])
					self.listView.setModel(self.model)
					self.groupBox_5.setEnabled(False)
			else:
				#give warning and autocomplete lineEdit
				self.givePathWarning("The path must be within the filesystem!",
				"When the system is started, you can only change properties of the files and folders within the mountpoint destination path.")
				self.lineEdit_4.setText(MFSCore.MFSConfig['mountpoint_dest'])
		else:
			self.listView.setEnabled(False)
			self.model.setStringList([])
			self.listView.setModel(self.model)
			self.groupBox_5.setEnabled(False)
			
	def updateOperationsButtons(self, index):
		"""Enables the operation buttons when a version file is selected from the list.
		"""
		self.selectedVersion = index.data().toString()
		self.groupBox_5.setEnabled(True)
		self.pushButton_3.setEnabled(True)
		self.pushButton_4.setEnabled(True)
		self.pushButton_5.setEnabled(True)
		self.pushButton_6.setEnabled(True)
		
	def viewFileVersionInfo(self):
		"""Opens a message box showing information related to the selected file version.
		Information include: complete path, size, last modification date, and any extended attributes
		associated with the file.
		"""
		path = os.path.join(self.operationPath,str(self.selectedVersion))
		infoBox = QMessageBox()
		infoBox.setWindowTitle("Version Information")
		infoBox.setIcon(QMessageBox.Information)
		infoBox.setText("<b>Info about "+str(self.selectedVersion)+":</b>")
		infoText = "<p>Complete Path: " + os.path.join(self.versionedPath,str(self.selectedVersion))
		infoText += "<p>File Size: " + str(os.path.getsize(path)) + " bytes"
		infoText += "<p>Last Modified " + str(time.strftime('Date: %Y.%m.%d Time: %H:%M:%S GMT',time.gmtime(os.path.getctime(path)))) 
		infoBox.setInformativeText(infoText)
		detailedText = ""
		attrfile = xattr.xattr(path)
		for at in attrfile.list():
			detailedText += str(at)+": "+str(attrfile.get(at)) + "\n"
		infoBox.setDetailedText(detailedText)
		infoBox.exec_()
		
	def openFileVersion(self):
		"""Opens the selected version file from the list of versions.
		"""
		path = os.path.join(self.versionedPath,str(self.selectedVersion))
		subprocess.Popen(["xdg-open",path])
		
	def deleteFileVersion(self):
		"""Deletes the selected version file from the list of versions. 
		Raises a message box asking for user confirmation.
		"""
		path = os.path.join(self.versionedPath,str(self.selectedVersion))
		reply = QMessageBox.question(self, "", "Are you sure you want to permanently delete "+path+"?",
		QMessageBox.Yes|QMessageBox.Default, QMessageBox.No|QMessageBox.Escape)
		if reply == QMessageBox.Yes:
			if os.path.isfile(path):
				os.unlink(path)
			elif os.path.isdir(path):
				shutil.rmtree(os.path.join(self.operationPath,str(self.selectedVersion)))
			self.showFileVersions(self.lineEdit_4.text())
			
	def restoreFileVersion(self):
		"""Restores the selected version file from the list of versions as the current version.
		Raises a message box asking for user confirmation.
		"""
		path = os.path.normpath(os.path.join(self.versionedPath,str(self.selectedVersion)))
		reply = QMessageBox.question(self, "", "Are you sure you want to restore "+path+"?",
		QMessageBox.Yes|QMessageBox.Default, QMessageBox.No|QMessageBox.Escape)
		if reply == QMessageBox.Yes:
			initPath = os.path.normpath(os.path.join(self.versionedPath,str(self.browsedFile)))
			if os.path.isfile(path):
				# current version of the file (if exists) needs to be versioned, 
				# and the selected version for restoring needs to be renamed
				if os.path.exists(initPath):
					os.rename(initPath,MFSCore.versionPath(initPath)) #version current file
				os.rename(path,initPath) #rename selected version file to current
			elif os.path.isdir(path):
				if os.path.exists(initPath):
					shutil.move(initPath,MFSCore.versionPath(initPath)) #version current directory
				shutil.move(path,initPath) #rename selected version dir to current
			self.showFileVersions(initPath)
	
	#OTHER GENERAL FUNCTIONALITIES
				
	def browsingStartPoint(self):
		"""Returns the path from which file browsing should start in a file browsing window. 
		If the filesystem is started, returns the path of 'mountpoint_dest'.
		Othewise, returns the path in 'mountpoint_source'
		"""
		if self.started == True:
			#start from mountpoint dest
			return MFSCore.MFSConfig['mountpoint_dest']
		else:
			#start from mountpoint src
			return MFSCore.MFSConfig['mountpoint_source']
			
	def givePathWarning(self,text,detailedText):
		"""Opens a warning message box providing the user for an explanation for the warning.
		"""
		box = QMessageBox(QMessageBox.Warning, "Warning", text)
		box.setDetailedText(detailedText)
		box.exec_()

class FileSystem(QThread):
	def __init__(self,parent=None):
		super(FileSystem,self).__init__(parent)
		self.mutex = QMutex()
	
	def initialize(self, sourcePath, destPath, foreground):
		self.sourcePath = sourcePath
		self.destPath = destPath
		self.fg = foreground
	
	def run(self):
		MFSCore.startFS(self.sourcePath, self.destPath, self.fg)

if __name__ == "__main__":
	"""The main function called first. The application can be started both with or without the user interface.
	When started from the console with option -cli, the interface is not initialised.
	Usage: python MFSAPI.py -cli <source_mountpoint> <dest_mountpoint> (without GUI)
		or python MFSAPI.py (with GUI)
	"""
	import sys
	if len(sys.argv) > 1 and sys.argv[1]=="-cli":
		if len(sys.argv) != 4:
			print 'usage: %s -cli <root> <mountpoint>' % sys.argv[0]
			exit(2)	# Unix programs generally use 2 for command line syntax
		else:
			if os.path.isfile("settings.MMFS"):
				f = open("settings.MMFS","r")
				MFSCore.MFSConfig = cPickle.load(f)
				f.close()
			MFSCore.startFS(sys.argv[2],sys.argv[3],True)
	else:
		app = QApplication(sys.argv)
		form = MFSAPI()
		form.show()
		app.exec_()
