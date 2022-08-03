import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from Interface import Ui_mainWindow
from Objets import Partie, Boule_blanche, Boule, Plateau
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction, QFontComboBox
from PyQt5.QtGui import QFont
import numpy as np
from IHM0 import JeuBillard0

class JeuBillard (JeuBillard0):
    def __init__(self, p1 = "joueur 1",p2 = "joueur 2", nb = 10):
        super().__init__("../Images/carambole_m.jpg", p1, p2, nb, mode = 1)

        self.ANA = [] # analyse l'issue du coup : si le joueur à réussi à taper les 2 boules ou non

        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[self.i % 2].x + 86.2, self.table.plat[self.i % 2].y + 86.2
        # on place la queue sur la boule à tirer (avec une translation correspondant à l'écart fenêtre-widget, et à la bordure en bois du billard.

        self.ui.label2.setFont(QFont('Helvetica', 10))
        self.ui.label2.setText("{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
        self.ui.label2.show()   # on affiche le tableau de marque


    def demarrer(self):
        """
            Cette méthode est appelée lorsque le bouton Bouton_Demarrer est appuyé. Elle initialise une nouvelle partie :
            avec un nouveau plateau (les boules remises aux emplacement de départ, les valeurs courantes réinitialisée),
            et avec un nouvel affichage (des boules, et du tableau de marque et du nombre de tours)
        """

        super().demarrer(self.bx, self.by)


        self.ui.label2.setText( "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1],
                                                            self.joueurs[0], self.table.points[0]))
        self.ui.label2.show()  # on affiche la table de marque

        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[self.i % 2].x + 86.2, self.table.plat[self.i % 2].y + 86.2

        self.ui.con.update()

    def jouer(self):
        """
        Cette méthode est appelée lorsque le bouton Bouton_Jouer est appuyé. Elle simule un tour.

        """
        if self.table.plat.queue.p == 0 :  # si on appuie sur Jouer alors qu'on a seulement fait un clique sur l'écran la fonction
            # jouer ne fait rien. Permet d'éviter les rater pouvant survenir avec la souris. # cette valeur est changée dans le MouseReleaseEvent
            pass

        else :

            if self.table.c < self.table.nb_coups:

                x1, y1, x2, y2 = self.table.plat[self.i % 2 - 1].x, self.table.plat[self.i % 2 - 1].y, self.table.plat[ self.i % 2 - 2].x, self.table.plat[self.i % 2 - 2].y
                self.ANA = [x1, y1, x2, y2]  # on enregistre l'emplacement initial (avant tir) des boules que l'on doit toucher s'il on veut gagner un point

                self.ui.label2.setText("{} : {} \n{} : {}".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                                   self.table.points[0]))
                self.ui.label2.show()
                super().jouer()


    def timer_0 (self):
        """
             Cette méthode est appelée chaque fois que le timer self.timer est à 0.
             Si les boules sont encore en mouvement, on détermine leur nouvelle position et vitesse, en prenant en compte l'environnement de chaque boule.
             Sinon, on regarde si le joueur qui avait tiré a marqué le point.
             """

        if any(self.MVT):  #tant qu'une boule au moins est en mouvement
            for i in range(self.table.plat.n):
                Plateau.proche_bord(self.table.plat, self.posx, self.posy, i)  # on gère les rebonds sur les bords

            Plateau.collisions(self.table.plat,[],1,0,0)  # on gère les collisions entre boules

            for i in range(self.table.plat.n):
                self.MVT[i] = Boule.evolution(self.table.plat[i], self.table.dt, self.table.plat.k, 0.05 * self.table.plat.be)
                # détermination de la nouvelle position et vitesse de chaque boule, en mouvement rectiligne maintenant que l'impact de l'environnement a ét été traité.

                self.posx[i].append(self.table.plat[i].x)
                self.posy[i].append(self.table.plat[i].y)

            self.ui.con.update()

        else :
            self.timer.stop()
            self.ui.con.update()

            for i in range(self.table.plat.n):
                self.table.plat[i].vx, self.table.plat[i].vy = 0, 0  # on arrête les billes, puisque qu'elle ne sont pas immobiles,
                # mais seulement mobiles avec une vitesse inférieure à eps (dans la fonction evolution)

            if self.ANA[0] - self.table.plat[self.i % 2 - 1].x != 0 and self.ANA[1] - self.table.plat[self.i % 2 - 1].y  !=0 and self.ANA[2] - \
                self.table.plat[self.i % 2 - 2].x != 0 and self.ANA[3] - self.table.plat[self.i % 2 - 2].y != 0:
            # On regarde si les coordonnées des 2 boules visées ont évolué, ie si la boule de tire à bien touché les 2 autres

                self.ui.label.setText("Vous avez marqué un point ! C'est encore à vous de jouer")
                self.ui.label.show()

                self.table.points[self.i % 2] += 1 # le joueur marque un point

                self.ui.label2.setText(
                    "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
                self.ui.label2.show()
                # on met à jour l'affichage du tableau de score

                self.ui.label0.setText("Tour {}/{}".format(self.table.c + 1, self.nb_coups))
                self.ui.label0.show()

            else:

                self.i += 1  # c'est au joueur suivant de jouer

                self.ui.label.setText(("Pas de chance... C'est à {} de jouer.").format(self.joueurs[self.i % 2]))
                self.ui.label.show()

                self.ui.label2.setText("{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                self.table.points[0]))
                self.ui.label2.show()

                self.ui.label0.setText("Tour {}/{}".format(self.table.c+1, self.nb_coups))
                self.ui.label0.show()


            self.table.plat.queue.x , self.table.plat.queue.y = self.table.plat[self.i % 2].x+ 86.2, self.table.plat[self.i % 2].y + 86.2
            # on place la queue à l'emplacement de la boule blanche que l'on souhaite ensuite taper :la même si le dernier coup a réussi, l'autre s'il a échoué.

            self.table.plat.queue.p = 0 # on réinitialise la puissance que l'on souhaite donner à la boule

            self.xp , self.yp =  self.table.plat.queue.x , self.table.plat.queue.y
            # les coordonnées du points de cliquage ne sont pas encore définies car on a pas encore cliqué pour ce coup.
            # On initalise cependant ses coordonnées au centre de la boule courante.
            # Ainsi, dans la fonction dessinJeu, avec le test effectué en fin de script,
            # on n'affichera pas le point de visée le temps qu'on aura pas cliqué sur l'écran, et ainsi débuté un coup.

            self.ui.con.update()

            if self.table.c >= self.table.nb_coups:  # on vient de jouer le dernier coup de la partie, on regarde maintenant qui a gagné.

                self.ui.label.setText("{} : {} points \n{} : {} points ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                              self.table.points[0]))
                self.ui.label.show()

                self.ui.label0.setText("Tour {}/{}".format(self.table.c, self.nb_coups))
                self.ui.label0.show()

                if self.table.points[0] != self.table.points[1]:
                    if self.table.points[0] > self.table.points[1]:
                        g = 0
                    else:
                        g = 1
                    self.ui.label.setText("{} : {} points, {} : {} points. \n{} a gagné ! Félicitations ! ".format(self.joueurs[1],
                                        self.table.points[1], self.joueurs[0], self.table.points[0],self.joueurs[g]))

                    self.ui.label.show()

                    self.ui.label2.setText( "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                    self.table.points[0]))
                    self.ui.label2.show()

                else:
                    self.ui.label.setText( "{} : {} points \n{} : {} points. \nEgalité ! Bravo à vous deux ! ".format(
                                            self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
                    self.ui.label.show()

                    self.ui.label2.setText("{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                    self.table.points[0]))
                    self.ui.label2.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JeuBillard()
    window.show()
    app.exec_()
