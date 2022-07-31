from IHM import JeuBillard
from IHM2 import JeuBillard2

from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window_Menu (QtWidgets.QMainWindow) :

    def __init__(self, *args, **kwargs):
        super(Window_Menu, self).__init__(*args, **kwargs)

        pixmap = QtGui.QPixmap("../Images/arriere_plan_lancement.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        zoneCentrale = QWidget()
        #zoneCentrale.lower()
        #zoneCentrale.stackUnder(self)
        zoneCentrale.setAutoFillBackground(True)
        zoneCentrale.setPalette(pal)

        self.setWindowTitle("Entrez vos prénoms, et le nombre coups")
        self.setFixedSize(300, 215)

        self.bouton_valider = QtWidgets.QPushButton("Lancer la partie", self)  # on crée un bouton qui affichera 'Lancer la partie'
        self.bouton_valider.setFixedSize(150, 35)  # taille du bouton
        self.bouton_valider.setFont(QFont('Calibri', 12))   # type et taille de police
        self.bouton_valider.setStyleSheet("background-color: white")
        self.bouton_valider.move(180, 200)  # position du bouton
        self.bouton_valider.clicked.connect(self.initialisation)
        # lorsque l'on clique sur le bouton bouton_valider, la méthode initialisation est appelée

        self.prenom1 = QLineEdit(self)
        self.prenom1.move (25,50)
        self.prenom2 = QLineEdit(self)
        self.prenom2.move(20, 100)
        self.nb_tour = QLineEdit(self)
        self.nb_tour.move(20, 150)
        self.mode = 0

        self.layout = QFormLayout()

        self.titre1 = QLabel ("Prénom du joueur 1 ")
        self.titre1.setFixedSize(120,20)
        self.titre1.move(50,50)
        self.titre1.show()

        self.titre2 = QLabel("Prénom du joueur 2 ")
        self.titre2.setFixedSize(120, 20)
        self.titre2.move(50, 100)
        self.titre2.show()

        self.titre3= QLabel("Nombre de coups")
        self.titre3.setFixedSize(120, 20)
        self.titre3.move(50, 150)
        self.titre3.show()


        self.layout.addRow(self.titre1, self.prenom1)
        self.layout.addRow(self.titre2, self.prenom2)
        self.layout.addRow(self.titre3, self.nb_tour)

        self.bouton_mode_1 = QtWidgets.QPushButton("Mode 1 : Français", self)  # on crée un bouton qui affichera 'Lancer la partie'
        self.bouton_mode_1.setFixedSize(150, 30)  # taille du bouton
        self.bouton_mode_1.setFont(QFont('Calibri', 11))  # type et taille de police
        self.bouton_mode_1.setStyleSheet("background-color: white")
        self.bouton_mode_1.move(20, 120)  # position du bouton
        self.bouton_mode_1.clicked.connect(self.choix_mode_1)

        self.bouton_mode_2 = QtWidgets.QPushButton("Mode 2 : Américain", self)  # on crée un bouton qui affichera 'Lancer la partie'
        self.bouton_mode_2.setFixedSize(150, 30)  # taille du bouton
        self.bouton_mode_2.setFont(QFont('Calibri', 11))  # type et taille de police
        self.bouton_mode_2.setStyleSheet("background-color: white")
        self.bouton_mode_2.move(240, 120)  # position du bouton
        self.bouton_mode_2.clicked.connect(self.choix_mode_2)

        #self.layout.setSizeConstraint(100)

        #self.layout.addRow(self.bouton_mode_1, self.bouton_mode_2)
        #self.layout.addRow()

        self.layout.addWidget(self.bouton_mode_1)
        self.layout.addWidget(self.bouton_mode_2)
        self.layout.addWidget(self.bouton_valider)

        zoneCentrale.setLayout (self.layout)
        self.setCentralWidget(zoneCentrale)

        self.show()

    def choix_mode_1 (self):
        self.mode = 1
        self.bouton_mode_1.setStyleSheet("background-color: purple" )
        self.bouton_mode_2.setStyleSheet("background-color: white")

    def choix_mode_2 (self):
        self.mode = 2
        self.bouton_mode_2.setStyleSheet("background-color: purple")
        self.bouton_mode_1.setStyleSheet("background-color: white")

    def initialisation (self) :
        """
        initialisation :
        recueille les prénoms des joueurs et le nombre de coups qu'ils veulent jouer, ainsi que le mode de jeu
        Lance la fenêtre de jeu avec ces paramètres
        """

        p1 = self.prenom1.text()
        p2 = self.prenom2.text()
        nb = self.nb_tour.text()
        p1 = "Elo"
        p2 = "Mat"
        nb = "20"
        mode = self.mode
        try :
            nb = int (nb)
            if nb > 1 :  # les joueurs ont entré une donnée adaptée
                if mode != 0 :
                    if mode == 1 :
                        print ("vous avez choisis le mode " , mode)
                        self.win_deux = JeuBillard(p1, p2, nb)  # on va pouvoir lancer le jeu avec les paramètres fournis par les joueurs
                        self.win_deux.show()                  # La fenêtre billard est lancée
                        self.close()
                    else :
                        print("vous avez choisis le mode ", mode)
                        self.win_deux2 = JeuBillard2(p1, p2, nb )
                        self.win_deux2.show()  # La fenêtre billard est lancée
                        self.close()

                else:
                    self.titre3.setText ("Choisissez un mode !")
                    self.titre3.show()
            else :      # on ne peut faire un nombre de coup négatif
                self.titre3.setText('Nombre positif requis !')  #il va falloir changer la valeur de nb
                self.titre3.setFixedSize(125, 20)
                self.titre3.show()
        except ValueError :   # on ne peut faire un nombre de coup qui ne soit pas un nombre entier
            self.titre3.setText('Nombre requis !')   # il va falloir changer la valeur de nb
            self.titre3.show()


if __name__ == "__main__" :

    app = QApplication([])
    win = Window_Menu()
    app.exec()


