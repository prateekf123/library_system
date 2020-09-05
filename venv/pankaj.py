from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from  PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.uic import loadUi



class main(QMainWindow):

    def __init__(self):

        super(main,self).__init__()
        loadUi('mains.ui',self)
        self.setStyleSheet(open("AMOLED.qss", "r").read())
        self.setWindowTitle("Smart Library System")



app = QApplication(sys.argv)
widget = main()
widget.show()
sys.exit(app.exec())