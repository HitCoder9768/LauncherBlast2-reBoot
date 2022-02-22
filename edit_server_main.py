import fix_qt_import_error
import sys, os, PySide6.QtWidgets, json, feedparser
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from edit_server_ui import *

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
            self.parentWindow.add_server_to_list(self.ui.ServerNameInput.text(), self.ui.ServerAddressInput.text())
        else:
            self.parentWindow.edit_selected_server(self.ui.ServerNameInput.text(), self.ui.ServerAddressInput.text())
        self.close()
        return