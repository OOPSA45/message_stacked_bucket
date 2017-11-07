# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MymessForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 459)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushSend = QtWidgets.QPushButton(self.centralwidget)
        self.pushSend.setGeometry(QtCore.QRect(760, 360, 51, 51))
        self.pushSend.setObjectName("pushSend")
        self.pushAdd = QtWidgets.QPushButton(self.centralwidget)
        self.pushAdd.setGeometry(QtCore.QRect(0, 360, 91, 51))
        self.pushAdd.setObjectName("pushAdd")
        self.pushDel = QtWidgets.QPushButton(self.centralwidget)
        self.pushDel.setGeometry(QtCore.QRect(90, 360, 91, 51))
        self.pushDel.setObjectName("pushDel")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(190, 0, 621, 361))
        self.textEdit.setObjectName("textEdit")
        self.textAddMessage = QtWidgets.QTextEdit(self.centralwidget)
        self.textAddMessage.setGeometry(QtCore.QRect(190, 360, 571, 51))
        self.textAddMessage.setObjectName("textAddMessage")

        self.listWidgetContants = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetContants.setGeometry(QtCore.QRect(0, 0, 191, 321))
        self.listWidgetContants.setObjectName("listWidgetContants")

        self.lineEditAddContact = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddContact.setGeometry(QtCore.QRect(0, 320, 191, 41))
        self.lineEditAddContact.setObjectName("lineEditAddContact")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_options = QtWidgets.QAction(MainWindow)
        self.action_options.setObjectName("action_options")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_list_contact = QtWidgets.QAction(MainWindow)
        self.action_list_contact.setObjectName("action_list_contact")
        self.menu.addAction(self.action_list_contact)
        self.menu.addAction(self.action_options)
        self.menu.addAction(self.action_about)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushSend.setText(_translate("MainWindow", "Send"))
        self.pushAdd.setText(_translate("MainWindow", "+"))
        self.pushDel.setText(_translate("MainWindow", "-"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.action_options.setText(_translate("MainWindow", "Настройки"))
        self.action_about.setText(_translate("MainWindow", "О программе"))
        self.action_list_contact.setText(_translate("MainWindow", "Контакты"))

