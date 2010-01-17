from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_MFSGUI
import os.path #or use QDir.homePath() - user's home directory
import os
import platform
import MFSCore

__version__ = "0.0.1"

class MFSAPI(QMainWindow, ui_MFSGUI.Ui_MainWindow):
	def __init__(self,parent=None):
		super(MFSAPI,self).__init__(parent)
		self.setupUi(self)
		self.connect(self.pushButton_2, SIGNAL("clicked()"), self.updateMountPointSource)
		self.connect(self.pushButton, SIGNAL("clicked()"), self.updateMountPointDest)
		self.connect(self.pushButton_7, SIGNAL("clicked()"), self.updateFileSelection)
		self.connect(self.pushButton_8, SIGNAL("clicked()"), self.updateDirSelection)
		self.connect(self.lineEdit_3, SIGNAL("update()"), self.updateFileSettings) #? returnPressed()
		self.connect(self.pushButton_10, SIGNAL("clicked()"), self.startMFS)
		self.connect(self.pushButton_11, SIGNAL("clicked()"), self.stopMFS)
		self.connect(self.actionAbout, SIGNAL("triggered()"), self.showAbout)

		
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
		
	def updateFileSettings(self):
		print "mac mac"
		
	def startMFS(self):
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
	print sys.argv
	print len(sys.argv)
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
