import os 
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets  import *
from PyQt5.uic  import loadUiType 
from PyQt5 import QtWidgets, uic
import urllib.request
import pafy 
import humanize  

FORM_CLASS,_= loadUiType( os.path.join( os.path.dirname(__file__) , 'main.ui' ))

class MainApp(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.handel_ui()
		self.handle_buttons()


	def handle_buttons(self):
		self.pushButton.clicked.connect(self.downlood)
		self.pushButton_2.clicked.connect(self.handel_browse)
		# Video
		self.pushButton_11.clicked.connect(self.get_vid_info)
		self.pushButton_7.clicked.connect(self.vid_download)
		self.pushButton_8.clicked.connect(self.save_path)
		# PlayList
		self.pushButton_10.clicked.connect(self.playlist_download)
		self.pushButton_9.clicked.connect(self.path_save)

	def handel_ui(self):
		self.setWindowTitle('Nazelnyyy Nazelny')
		self.setFixedSize(900,440)

	def handel_browse(self):
		save_place = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files (*.*)")
		text = str(save_place)
		name = (text[2:].split(',')[0].replace("'",''))
		self.lineEdit_2.setText(name)  

	def progress_bar(self, blocknum, blocksize, totalsize ):
		read = blocknum * blocksize 
		if totalsize > 0: 
			percent = read * 100 / totalsize
			self.progressBar.setValue(percent)
			QApplication.processEvents()

	def downlood(self):
		url = self.lineEdit.text() 
		save_location = self.lineEdit_2.text()
		try:
			urllib.request.urlretrieve(url, save_location, self.progress_bar )
			QMessageBox.information(self,"Download Completed", "Your Download Finished")
			
		except Exception:
			QMessageBox.warning(self,"Failed", "Your Download Failed")

		self.progressBar.setValue(0)
		self.lineEdit.setText('')
		self.lineEdit_2.setText('')

	###############  YouTube Download ###################
	def save_path(self):
		path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
		self.lineEdit_6.setText(path)



	def get_vid_info(self):
		video_url = self.lineEdit_5.text()
		v = pafy.new(video_url)
		st = v.allstreams 
		for s in st:
			size = humanize.naturalsize(s.get_filesize())
			data = '{} {} {} {}'.format(s.mediatype, s.quality, s.extension, size)
			self.comboBox.addItem(data)

	def vid_download(self):
		video_url = self.lineEdit_5.text()
		v = pafy.new(video_url)
		location = self.lineEdit_6.text()
		st = v.allstreams 
		quality = self.comboBox.currentIndex()

		down = st[quality].download(filepath=location)
		QMessageBox.information(self,"Download Completed", "Your Download Finished")

################ PlayList Download ######################3
	def path_save(self):
		path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
		self.lineEdit_12.setText(path)

	
	def playlist_download(self):
		playList_url = self.lineEdit_11.text()
		v = pafy.get_playlist(playList_url)
		location = self.lineEdit_12.text()
		st = v.allstreams 
		quality = self.comboBox.currentIndex()

		down = st[quality].download(filepath=location)
		QMessageBox.information(self,"Download Completed", "Your Download Finished") 

def main():
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()
