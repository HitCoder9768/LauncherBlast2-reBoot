# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_editor.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import fix_qt_import_error
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(552, 202)
        Dialog.setMinimumSize(QtCore.QSize(552, 202))
        Dialog.setMaximumSize(QtCore.QSize(552, 202))
        Dialog.setStyleSheet("QWidget{    \n"
"    color: #ffffff;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 10pt;\n"
"    background-color: #3b3b3b;\n"
"}\n"
"\n"
"QLabel{\n"
"    font: bold 10pt;\n"
"    color: #ffffff;\n"
"    font-family: \"Segoe UI\";\n"
"    padding-left: 0px;\n"
"    padding-top: 6px;\n"
"    max-height: 20px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: #3c5fcf;\n"
"    border: 0;\n"
"    min-height: 28px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: #3c5fff;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #1a45cc;\n"
"}\n"
"\n"
"QLineEdit, QComboBox{\n"
"    background-color: #131313;\n"
"    color: #ffffff;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 12pt;\n"
"    border-radius: 4px;\n"
"    height: 24px;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    padding-bottom: 4px;\n"
"}\n"
"\n"
"QFrame{\n"
"    border: 0;\n"
"}")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, -10, 551, 231))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ServerNameLabel = QtWidgets.QLabel(self.frame_2)
        self.ServerNameLabel.setObjectName("ServerNameLabel")
        self.verticalLayout.addWidget(self.ServerNameLabel)
        self.ServerNameInput = QtWidgets.QLineEdit(self.frame_2)
        self.ServerNameInput.setText("")
        self.ServerNameInput.setObjectName("ServerNameInput")
        self.verticalLayout.addWidget(self.ServerNameInput)
        self.ServerIPLabel = QtWidgets.QLabel(self.frame_2)
        self.ServerIPLabel.setObjectName("ServerIPLabel")
        self.verticalLayout.addWidget(self.ServerIPLabel)
        self.ServerAddressInput = QtWidgets.QLineEdit(self.frame_2)
        self.ServerAddressInput.setObjectName("ServerAddressInput")
        self.verticalLayout.addWidget(self.ServerAddressInput)
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 66))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SaveServerButton = QtWidgets.QPushButton(self.frame)
        self.SaveServerButton.setObjectName("SaveServerButton")
        self.horizontalLayout.addWidget(self.SaveServerButton)
        self.CancelButton = QtWidgets.QPushButton(self.frame)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit server"))
        self.ServerNameLabel.setText(_translate("Dialog", "SERVER NAME"))
        self.ServerIPLabel.setText(_translate("Dialog", "SERVER IP"))
        self.SaveServerButton.setText(_translate("Dialog", "Save"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
