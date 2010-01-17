from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_MFSGUI
import os.path
import os
import MFSComFUSE
from fuse import FUSE

class MFSAPI(QMainWindow, ui_MFSGUI.Ui_MainWindow):
	def __init__(self,parent=None):
		super(MFSAPI,self).__init__(parent)
		self.setupUi(self)
		self.connect(self.pushButton_2, SIGNAL("clicked()"), self.updateMountPointSource)
		self.connect(self.pushButton, SIGNAL("clicked()"), self.updateMountPointDest)
		self.connect(self.pushButton_7, SIGNAL("clicked()"), self.updateFileSelection)
		self.connect(self.pushButton_8, SIGNAL("clicked()"), self.updateDirSelection)
		self.connect(self.lineEdit_3, SIGNAL("update()"), self.updateFileSettings) #?
		self.connect(self.pushButton_10, SIGNAL("clicked()"), self.startMFS)
		self.connect(self.pushButton_11, SIGNAL("clicked()"), self.stopMFS)
		
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
		print "python MFSComFUSE.py " + str(self.lineEdit.text()) + " " + str(self.lineEdit_2.text())
		os.spawnl(os.P_NOWAIT, "python MFSComFUSE.py " + str(self.lineEdit.text()) + " " + str(self.lineEdit_2.text()))
		#fuse = FUSE(MFSComFUSE.MFSComFUSE(str(self.lineEdit.text())), str(self.lineEdit_2.text()), foreground=False)
		
	def stopMFS(self):
		os.system("fusermount -u " + str(self.lineEdit_2.text()))

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = MFSAPI()
	form.show()
	app.exec_()
