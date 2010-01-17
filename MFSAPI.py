from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_MFSGUI
import os.path #or use QDir.homePath() - user's home directory
import os
import platform
import MFSCore
import cPickle
import xattr

__version__ = "0.0.1"

class MFSAPI(QMainWindow, ui_MFSGUI.Ui_MainWindow):
	def __init__(self,parent=None):
		super(MFSAPI,self).__init__(parent)
		self.setupUi(self)
		
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


	def readSettings(self):
		if os.path.isfile("settings.MMFS"):
			f = open("settings.MMFS","r")
			MFSCore.MFSConfig = cPickle.load(f)
			f.close()
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
		filename = QFileDialog.getExistingDirectory(self, "Select Mount Point Source", os.path.expanduser('~'),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		self.lineEdit.setText(filename)

	def updateMountPointDest(self):
		filename = QFileDialog.getExistingDirectory(self, "Select Mount Point Destination", os.path.expanduser('~'),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		self.lineEdit_2.setText(filename)
			
	def updateFileSelection(self):
		filename = QFileDialog.getOpenFileName(self, "Select File", os.path.expanduser('~'))
		self.lineEdit_3.setText(filename)
		
	def updateDirSelection(self):
		filename = QFileDialog.getExistingDirectory(self, "Select Directory", os.path.expanduser('~'),
		QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		self.lineEdit_3.setText(filename)
		
	def startMFS(self):
		if str(self.lineEdit.text()) != "" and str(self.lineEdit_2.text()) != "":
			self.filesystem = FileSystem(self)
			self.filesystem.initialize(str(self.lineEdit.text()),str(self.lineEdit_2.text()),True)
			self.filesystem.start()
		
	def stopMFS(self):
		os.system("fusermount -u " + str(self.lineEdit_2.text()))
		
	def showAbout(self):
		QMessageBox.about(self, "About MalcolmFS",
			"""<b>MalcolmFS</b> v %s
			<p>A stackable versioning file system implemented in Python.
			<p><a href="http://code.google.com/p/malcolm">MalcolmFS Web Site</a>
			<p>Copyright &copy; 2010. 
			Radu Dragusin, Paula Petcu, Kostas Rutkauskas.
			<p>Code License: <a href="http://www.creativecommons.org/licenses/MIT/">MIT License</a>
			<p>Python %s -Qt %s -PyQt %s on %s"""
			% (__version__,platform.python_version(),QT_VERSION_STR,PYQT_VERSION_STR,platform.system()))
	
	def saveCheckedrb1(self):
		MFSCore.MFSConfig['versioning_enabled'] = 'true'
	def saveCheckedrb2(self):
		MFSCore.MFSConfig['versioning_enabled'] = 'false'
	def saveSpinnedsb1(self):
		MFSCore.MFSConfig['max_no_versions'] = self.spinBox.value()
	def saveMountPointSrc(self):
		MFSCore.MFSConfig['mountpoint_source'] = str(self.lineEdit.text())
	def saveMountPointDest(self):
		MFSCore.MFSConfig['mountpoint_dest'] = str(self.lineEdit_2.text())
	
	# method for setting xatrributes for the given path (a file or directory)
	def setFileXAttr(self,path):
		attrfile = xattr.xattr(path)
		if self.radioButton_4.isChecked() == True:
			attrfile.set('user.versioning_enabled', 'true')
		elif self.radioButton_3.isChecked() == True:
			attrfile.set('user.versioning_enabled', 'false')
		attrfile.set('user.max_no_versions',str(self.spinBox_4.value()))
	
	def saveSettings(self):
		#if in first tab or in the third (General Settings or Per File Operations)
		if self.tabWidget.currentIndex() != 1:
			f = open("settings.MMFS", "w")
			cPickle.dump(MFSCore.MFSConfig,f)
			f.close()
		#if in the second tab (Per File Settings)
		else:
			path = str(self.lineEdit_3.text())
			if os.path.exists(path):
				if os.path.isfile(path):
					#change the xattr for the specified file (path)
					self.setFileXAttr(path)
				else:
					#change the xattr for every dir and file in the selected dir (path)
					for a,b,c in os.walk(path):
						self.setFileXAttr(a)
						for x in c:
							self.setFileXAttr(os.path.join(a,x))
			
	def showFileSettings(self, path):
		# path = str(self.lineEdit_3.text())
		if os.path.exists(path):
			self.groupBox_3.setEnabled(True)
			attrfile = xattr.xattr(path)
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
			self.groupBox_3.setEnabled(False)

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
	import sys
	if len(sys.argv) > 1 and sys.argv[1]=="-cli":
		if len(sys.argv) != 4:
			print 'usage: %s -cli <root> <mountpoint>' % sys.argv[0]
			exit(2)	# Unix programs generally use 2 for command line syntax
		else:
			MFSCore.startFS(sys.argv[2],sys.argv[3],True)
	else:
		app = QApplication(sys.argv)
		form = MFSAPI()
		form.show()
		app.exec_()
