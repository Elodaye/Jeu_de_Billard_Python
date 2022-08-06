import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from Interface import Ui_mainWindow
from Objets import Partie, Boule_blanche, Boule, Plateau
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction, QFontComboBox
from PyQt5.QtGui import QFont
import numpy as np
from IHM0 import JeuBillard0

class JeuBillard2 ( JeuBillard0):
    def __init__(self, p1 = "joueur 1",p2 = "joueur 2",nb=10):

        super().__init__("../Images/billard_americain_3.png", p1 = p1, p2 = p2, mode = 2)

        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[0].x + 86.2, self.table.plat[0].y + 86.2
        # on place la queue sur la boule à tirer (avec une translation correspondant à l'écart fenêtre-widget, et à la bordure en bois du billard.

        self.cpt_ant = {"B" : 0, "N" : 0, "J" : 0, "R" : 0}
        self.faute = 0
        self.couleurs = ["R", "J"]


    def demarrer(self):
        """
            Cette méthode est appelée lorsque le bouton Bouton_Demarrer est appuyé. Elle initialise une nouvelle partie :
            avec un nouveau plateau (les boules remises aux emplacement de départ, les valeurs courantes réinitialisée),
            et avec un nouvel affichage (des boules, et du tableau de marque et du nombre de tours)
        """

        super().demarrer()
        self.faute = 0
        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[0].x + 86.2, self.table.plat[0].y + 86.2
        self.ui.con.update()

    def jouer(self):
        """
        Cette méthode est appelée lorsque le bouton Bouton_Jouer est appuyé. Elle simule un tour.

        """
        if self.table.plat.queue.p == 0 :  # si on appuie sur Jouer alors qu'on a seulement fait un clique sur l'écran la fonction
            # jouer ne fait rien. Permet d'éviter les rater pouvant survenir avec la souris. # cette valeur est changée dans le MouseReleaseEvent
            pass

        else :

            if (self.table.plat.cpt["J"] < 7 ) & (self.table.plat.cpt["R"]  < 7) & (self.table.plat.cpt["N"] != 1):  ## Condition d'arrêt du jeu

                self.LB = []

                super().jouer()


    def timer_0 (self):
        """
             Cette méthode est appelée chaque fois que le timer self.timer est à 0.
             Si les boules sont encore en mouvement, on détermine leur nouvelle position et vitesse, en prenant en compte l'environnement de chaque boule.
             Sinon, on regarde si le joueur qui avait tiré a marqué le point.
             """

        if any(self.MVT):  #tant qu'une boule au moins est en mouvement
            super().timer_0()

        else :
            self.timer.stop()
            self.ui.con.update()

            self.table.points[0], self.table.points[1] = self.table.plat.cpt["R"], self.table.plat.cpt["J"]


            if  (self.table.plat.cpt["N"] == 1 ):
                self.ui.label.setText("{} a mis la boule noire... \n{} a gagné ! Félicitations ! ".format(self.joueurs [(self.i +1) %2],self.joueurs[self.i %2]))
                self.ui.label.show()


            elif (self.table.plat.cpt["R"]  >= 7 ) | (self.table.plat.cpt["J"]  >= 7):  # on vient de jouer le dernier coup de la partie, on regarde maintenant qui a gagné.

                g = not (self.table.points[0] > self.table.points[1])
                self.ui.label.setText("{} : {} points, {} : {} points. \n{} a gagné ! Félicitations ! ".format(self.joueurs[1],
                                        self.table.points[1], self.joueurs[0], self.table.points[0],self.joueurs[g]))
                self.ui.label.show()


            elif (self.table.plat.cpt["B"] > self.cpt_ant["B"]) \
                    or (self.table.plat.cpt[self.couleurs[(self.i + 1) % 2 ]] > self.cpt_ant[self.couleurs[(self.i + 1) % 2]]) \
                    or (self.LB == []) \
                    or (self.LB[0] != self.couleurs[self.i % 2]):

                self.ui.label.setText(("Faute de jeu... C'est à {} de jouer.").format(self.joueurs[(self.i + 1) % 2]))
                self.ui.label.show()
                self.faute = 1  ## l'adversaire obtient un coup supplémentaire
                self.i += 1  # c'est au joueur suivant de jouer -> va aider à changer la boule que l'on tape


            elif (self.table.plat.cpt[self.couleurs [self.i %2]] > self.cpt_ant[self.couleurs[self.i %2]]):
            ## si l'on a mit une de nos boules dans le trou, sous avoir fait faute (vérifié dans le if précédant)

                self.faute = 0  ## si l'on bénéficiait d'un coup supplémentaire, l'avantage disparait en marquant un point et rejouant
                self.ui.label.setText("Vous avez marqué un point ! C'est encore à vous de jouer")
                self.ui.label.show()

            else:
                if self.faute:  ## l'on a pas marqué, mais pas fait de faute, s'il reste un coup, on peut l'utiliser
                    self.ui.label.setText(("Il vous reste un coup !"))
                    self.ui.label.show()
                    self.faute = 0

                else:
                    self.ui.label.setText(("Tour {}... C'est à {} de jouer.").format(self.table.c + 1, self.joueurs[(self.i + 1) % 2]))
                    self.ui.label.show()
                    self.i += 1

            self.cpt_ant = self.table.plat.cpt

            super().timer_1()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JeuBillard2()
    window.show()
    app.exec_()
