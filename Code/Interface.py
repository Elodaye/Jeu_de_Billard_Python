# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel , QLineEdit , QFormLayout, QWidget
from PyQt5.QtGui import QFont

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.NonModal)
        mainWindow.resize(1123, 835)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\WPy64-3760\\python-3.7.6.amd64\\../../OneDrive - Ecole Nationale Supérieure de Techniques Avancées Bretagne/UE 2.4-projet/Sujet 05 - Billard/tablelogo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)

        mainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 720, 1071, 70))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Plateau = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.Plateau.setObjectName("Plateau")
        self.horizontalLayout_2.addWidget(self.Plateau)
        self.Bouton_Demarrer = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Bouton_Demarrer.setObjectName("Bouton_Demarrer")
        self.Bouton_Demarrer.setFixedSize(100, 50)
        self.horizontalLayout_2.addWidget(self.Bouton_Demarrer)
        self.Bouton_Jouer = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Bouton_Jouer.setObjectName("Bouton_Jouer")
        self.Bouton_Jouer.setFixedSize(100, 50)
        self.horizontalLayout_2.addWidget(self.Bouton_Jouer)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.label0 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label0.setObjectName("label2")
        self.horizontalLayout_2.addWidget(self.label0)
        spacerItem0 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem0)

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.label2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label2.setObjectName("label2")
        self.horizontalLayout_2.addWidget(self.label2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.label3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label3.setObjectName("label3")
        self.horizontalLayout_2.addWidget(self.label3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.Bouton_Quitter = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Bouton_Quitter.setObjectName("Bouton_Quitter")
        self.Bouton_Quitter.setFixedSize(100,50)

        self.horizontalLayout_2.addWidget(self.Bouton_Quitter)
        self.con = QtWidgets.QWidget(self.centralwidget)
        self.con.setGeometry(QtCore.QRect(10, 10, 1101, 701))
        self.con.setObjectName("con")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 26))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionQuitter = QtWidgets.QAction(mainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.menuMenu.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(mainWindow)
        self.Bouton_Quitter.clicked.connect(mainWindow.close)
        self.actionQuitter.triggered.connect(mainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Table de billard"))
        self.Bouton_Demarrer.setText(_translate("mainWindow", "Démarrer"))
        self.Bouton_Demarrer.setFont(QFont('Helvetica', 10))
        self.Bouton_Jouer.setText(_translate("mainWindow", "Jouer"))
        self.Bouton_Jouer.setFont(QFont('Helvetica', 10))
        self.label.setText(_translate("mainWindow", "                                                                  A vous de jouer  !                                                                    "))
        self.Bouton_Quitter.setText(_translate("mainWindow", "Quitter"))
        self.Bouton_Quitter.setFont(QFont('Helvetica', 10))
        self.menuMenu.setTitle(_translate("mainWindow", "Menu"))
        self.actionQuitter.setText(_translate("mainWindow", "Quitter"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_mainWindow()
    app.exec_()