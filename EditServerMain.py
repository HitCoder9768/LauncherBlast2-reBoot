import fix_qt_import_error
import sys, os, PyQt5.QtWidgets, json, feedparser
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from EditServerUI import *

class ChildWindow(QMainWindow):
    def __init__(self, parentWindow, name, ip, createnew):
        super(ChildWindow, self).__init__()
        self.parentWindow = parentWindow
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.SaveServerButton.clicked.connect(self.returnAndClose)
        self.ui.CancelButton.clicked.connect(self.close)
        self.ui.ServerNameInput.setText(name)
        self.ui.ServerAddressInput.setText(ip)
        self.createNew = createnew
    
    def returnAndClose(self):
        if(self.createNew):
            self.parentWindow.addServerToList(self.ui.ServerNameInput.text(),self.ui.ServerAddressInput.text())
        else:
            self.parentWindow.editSelectedServer(self.ui.ServerNameInput.text(),self.ui.ServerAddressInput.text())
        self.close()
        return