import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from Interface import Ui_mainWindow
from Objets import Partie, Boule_blanche, Boule, Plateau
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction, QFontComboBox
from PyQt5.QtGui import QFont
import numpy as np

class JeuBillard0 (QtWidgets.QMainWindow):
    def __init__(self,path, p1 = "joueur 1",p2 = "joueur 2",nb=10, mode = 1):
        super().__init__()

        self.mode = mode
        self.nb_coups = nb
        self.joueurs = [p1,p2]  #on recueille les données de la fenêtre d'initialisation
        self.LB = []

        self.ui = Ui_mainWindow()  # ce qu'on a importé de Interface
        self.ui.setupUi(self)

        pixmap = QtGui.QPixmap(path)  # on charge l'image d'arrière-plan
        pixmap = QtGui.QPixmap.scaledToHeight (pixmap, self.ui.con.height() )  #900
        pixmap = QtGui.QPixmap.scaledToWidth(pixmap, self.ui.con.width())  #1100

        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.con.lower()
        self.ui.con.stackUnder(self)
        self.ui.con.setAutoFillBackground(True) #et on la fixe
        self.ui.con.setPalette(pal)

        self.i = 0  # compteur qui représente le joueur qui est train de jouer (pair ou impair)
        self.MVT = []  # permet de vérifier qu'il y a toujours des boules en mouvement

        self.painter = QtGui.QPainter() # on instancie un premier peintre, pour les boules + le point qui désigne le joueur + le point de visée
        self.painter2 = QtGui.QPainter() # on instancie un second peintre pour la queue

        self.ui.con.paintEvent = self.dessinJeu
        self.ui.con.update()

        self.hw, self.lw =  self.ui.con.height(), self.ui.con.width()   # largeur (x) du widget con, ie la table de billard, et  sa hauteur (y)

        if mode == 1 :
            bande_n, bande_o, bande_e, bande_s = 76.2, 76.2, 76.2, 77  # epaisseurs des bandes sur notre image de table
            self.by, self.bx = self.hw - bande_n - bande_s, self.lw - bande_e - bande_o  # taille du tapis, correspondent à self.bn et self.be dans la classe plateau
        else :
            self.by, self.bx = self.hw - 218, self.lw - 145

        self.distx, self.disty = 0,0  # distance de la queue à la boule tirée (initialisée à 0)

        self.table = Partie(nb, 0.005, self.bx, self.by, self.mode) # On instancie la classe Partie, qui contient toutes
        # les méthodes et variables d'instances nécessaires au fonctionnement du jeu de billard

        self.xp, self.yp = -3,-3  # on initialise ces valeurs à -3 car elles ne vaudront plus jamais -3 une fois la partie lancee :
        # permet à la fonction de dessin dessinJeu de voir qu'elle ne doit pas afficher le point de visée dès le lancement du jeu.
        self.xr, self.yr = 0,0

        self.ui.Bouton_Demarrer.clicked.connect(self.demarrer)
        self.ui.Bouton_Jouer.clicked.connect(self.jouer)
        # lorsque que le bouton Bouton_Demarrer , resp. Bouton_Jouer sera enclenché, on appellera la méthode démarrer , resp. jouer.

        self.timer = QtCore.QTimer()  # on instancie la classe QTImer : on crée un timer self.timer
        self.timer.timeout.connect(self.timer_0) # chaque fois que ce timer "tombe à 0", on appele la méthode timer_0.

        self.ui.label0.setFont(QFont('Helvetica', 10))
        self.ui.label0.setText("Tour {}".format(self.table.c + 1))  # On précise le tour de jeu actuel
        self.ui.label0.show()

        self.ui.label.setFont(QFont('Helvetica', 10.5))
        self.ui.label.setText("Tour {}. \nC'est à {} de jouer.".format(self.table.c +1, self.joueurs [self.i % 2]))
        self.ui.label.show()    # Narration de la partie

        self.ui.label2.setFont(QFont('Helvetica', 11.5))
        self.ui.label2.setText("{} : {} ".format(self.joueurs[1], self.table.points[1]))
        self.ui.label2.setStyleSheet("color: yellow")
        self.ui.label2.show()

        self.ui.label3.setFont(QFont('Helvetica', 11.5))
        self.ui.label3.setText("{} : {} ".format(self.joueurs[0], self.table.points[0]))
        self.ui.label3.setStyleSheet("color: red")
        self.ui.label3.show()

    def demarrer(self):
        """
            Cette méthode initialise une nouvelle partie :
            avec un nouveau plateau (les boules remises aux emplacement de départ, les valeurs courantes réinitialisée)
        """
        self.table = Partie(self.nb_coups, 0.005, self.bx, self.by, self.mode)
        # On instancie la classe Partie, qui contient toutes les méthodes et variables # d'instances nécessaire au fonctionnement du jeu de billard

        self.ui.label0.setText("Tour {}".format(self.table.c + 1))  # On précise le tour de jeu actuel
        self.ui.label0.show()

        self.ui.label.setText("Nouvelle partie \nTour {}. \nC'est à {} de jouer.".format(self.table.c + 1, self.joueurs[self.i % 2]))
        self.ui.label.show()  # Narration de la partie

        self.ui.label2.setText("{} : {} ".format(self.joueurs[1], self.table.points[1]))
        self.ui.label2.setStyleSheet("color: yellow")
        self.ui.label2.show()

        self.ui.label3.setText("{} : {} ".format(self.joueurs[0], self.table.points[0]))
        self.ui.label3.setStyleSheet("color: red")
        self.ui.label3.show()

        self.LB = []
        self.xp, self.yp, = -3, -3
        self.xr, self.yr = 0, 0


    def jouer(self):
        """
        Cette méthode est appelée lorsque le bouton Bouton_Jouer est appuyé. Elle simule le début d'un tour.

        """
        self.table.c += 1

        self.ui.label0.setText("Tour {}".format(self.table.c))
        self.ui.label0.show()
        self.ui.label.setText("Tour {}. \nC'est à {} de jouer.".format(self.table.c, self.joueurs[self.i % 2]))
        self.ui.label.show()
        self.ui.label2.setText("{} : {} ".format(self.joueurs[1], self.table.points[1]))
        self.ui.label2.setStyleSheet("color: yellow")
        self.ui.label2.show()
        self.ui.label3.setText("{} : {} ".format(self.joueurs[0], self.table.points[0]))
        self.ui.label3.setStyleSheet("color: red")
        self.ui.label3.show()

        self.MVT = np.array([1 for i in range(self.table.plat.n)])
        # la liste se remplira de 0 au fur et à mesure que les boules (représentées par leur indice dans la liste self.plateau
        # seront considérés immobiles. si elle ne contient que des 0 (any(T)== False), le plateau est immobile, le tour est terminé.

        if self.mode == 1 :
            Boule_blanche.impulsion(self.table.plat[self.i % 2], self.table.plat.queue.alpha_b, self.table.plat.queue.p)
        # on donne à la boule self.table.plat[self.i % 2] une vitesse de direction self.table.plat.queue.alpha_b et de norme self.table.plat.queue.p
        else :
            Boule_blanche.impulsion(self.table.plat[0], self.table.plat.queue.alpha_b, self.table.plat.queue.p)

        self.posx, self.posy = [[] for i in range(self.table.plat.n)], [[] for i in range(self.table.plat.n)]

        for i in range(self.table.plat.n):  # pour garder en mémoire les positions passées (pour la fonction rebond)
            self.posx[i].append(self.table.plat[i].x)
            self.posy[i].append(self.table.plat[i].y)

        self.timer.start(7)  # toutes les 7 millisecondes, et tant qu'au moins une boule est mobile,
        # on met à jour la vitesse et la position de chaque boule, dans la méthode timer_0

    def timer_0 (self):
        """
             Les boules sont encore en mouvement, on détermine leur nouvelle position et vitesse, en prenant en compte l'environnement de chaque boule.
             """

        for i in range(self.table.plat.n):

            if (self.mode == 2) and (self.MVT[i] != 0) :
                Plateau.proche_trous(self.table.plat, self.posx, self.posy,
                                     i)  # enlève la boule de la liste si oui, mais dans un premier temps print un truc

        for i in range(self.table.plat.n):
            Plateau.proche_bord(self.table.plat, self.posx, self.posy, i)  # on gère les rebonds sur les bords

        Plateau.collisions(self.table.plat, [], 1, 0, 0)  # on gère les collisions entre boules

        self.LB = self.LB + self.table.plat.Lb

        for i in range(self.table.plat.n):
            self.MVT[i] = Boule.evolution(self.table.plat[i], self.table.dt, self.table.plat.k, 0.05 * self.table.plat.be)
            # détermination de la nouvelle position et vitesse de chaque boule, en mouvement rectiligne maintenant que l'impact de l'environnement a ét été traité.

            self.posx[i].append(self.table.plat[i].x)
            self.posy[i].append(self.table.plat[i].y)

        self.ui.con.update()


    def timer_1 (self):
        """
             Si les boules sont à l'arrêt on regarde si le joueur qui avait tiré a marqué le point, et met à jour l'affichage en conséquence
             """

        self.ui.label0.setText("Tour {}".format(self.table.c + 1))
        self.ui.label0.show()

        self.ui.label2.setText("{} : {} ".format(self.joueurs[1], self.table.points[1]))
        self.ui.label2.setStyleSheet("color: yellow")
        self.ui.label2.show()

        self.ui.label3.setText("{} : {} ".format(self.joueurs[0], self.table.points[0]))
        self.ui.label3.setStyleSheet("color: red")
        self.ui.label3.show()

        for i in range(self.table.plat.n):
            self.table.plat[i].vx, self.table.plat[i].vy = 0, 0  # on arrête les billes, puisque qu'elle ne sont pas immobiles,
            # mais seulement mobiles avec une vitesse inférieure à eps (dans la fonction evolution)

        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[0].x + 86.2, self.table.plat[0].y + 86.2
        # on place la queue à l'emplacement de la boule blanche que l'on souhaite ensuite taper :la même si le dernier coup a réussi, l'autre s'il a échoué.

        self.table.plat.queue.p = 0  # on réinitialise la puissance que l'on souhaite donner à la boule

        self.xp, self.yp = self.table.plat.queue.x, self.table.plat.queue.y
        # les coordonnées du points de cliquage ne sont pas encore définies car on a pas encore cliqué pour ce coup.
        # On initalise cependant ses coordonnées au centre de la boule courante.
        # Ainsi, dans la fonction dessinJeu, avec le test effectué en fin de script,
        # on n'affichera pas le point de visée le temps qu'on aura pas cliqué sur l'écran, et ainsi débuté un coup.

        self.ui.con.update()

    def dessinJeu(self,*args):
        """
             dessinJeu :
             Cette méthode est appelée chaque fois que la fonction update() est appelé, et que l'évènement PaintEvent est déclenché.
             Elle a pour unique but d'afficher l'état du billard au moment où on l'appelle.
        """

        self.painter.begin(self.ui.con)
        self.painter2.begin (self.ui.con)

        for boule in self.table.plat:
             boule.dessinimage(self.painter)  # on affiche chaque boule à son emplacement sur le plateau

        if self.table.plat.queue.p == 0 :  # si la puissance p est nulle, c'est qu'on est en attente du coup suivant

            boulex, bouley = self.table.plat[0].x + 90, self.table.plat[0].y + 88.2
            # emplacement de la boule dans laquelle on tire

            dx, dy = self.table.plat.queue.x - self.xp, self.table.plat.queue.y - self.yp
            # différence relative entre l'emplacement de la queue (du pointeur), et du point de cliquage

            angle_q= orient_queue (dx,dy)         #fonction de calcul d'arctangente, en fin de script
            self.table.plat.queue.alpha_q =angle_q  # orientation que l'on donne à la queue
            angle = (self.table.plat.queue.alpha_q)*(180/np.pi) # en degré, pour les sin et cos

            distx, disty = lim_coord_queue (dx,dy,300) #distx et disty empèchent la canne de partir trop loin de la boule dans l'affichage

            self.table.plat.queue.dessinimage(self.painter2, angle, boulex + distx, bouley + disty)

            if self.xp != self.table.plat.queue.x and self.xp != self.table.plat[0].x + 86.2 :
                self.table.plat.viseur.dessinimage(self.painter2, self.xp, self.yp)
            # permet de ne pas afficher le point de visée tant qu'on n'a pas cliqué

        self.table.plat.point.dessinimage(self.painter, self.table.plat[0].x, self.table.plat[0].y, self.i %2)

        self.painter.end()
        self.painter2.end()

    def mousePressEvent (self,event):
        """
             Cette méthode est appelée chaque fois que l'on clique sur la table de billard.
             Elle recueille les coordoonées du point de cliquage (utilisé ensuite pour déterminer l'angle et la direction de la boule tapée.
             Elle affiche aussi le point de visée, aidant à la visée, comme son nom l'indique, et met met à jours l'affichage du billard.
        """

        self.xp, self.yp = event.x(), event.y()  #coordonnees du point de debut de cliquage (press)

        self.painter2.begin (self.ui.con)
        self.table.plat.viseur.dessinimage(self.painter2, self.xp, self.yp)
        self.painter2.end()

        self.ui.con.update ()

    def mouseMoveEvent (self,event):
        """
             Cette méthode est appelée chaque fois que l'on bouge la souris sur la table de billard, en ayant cliqué sur celle-ci.
             Elle recueille les coordoonées courantes de la souris (utilisé dans dessinJeu pour incliner et translater la queue au voisinage de la boule).
        """

        self.table.plat.queue.x, self.table.plat.queue.y = event.x(), event.y()
        self.ui.con.update ()

    def mouseReleaseEvent (self,event):
        """
             Cette méthode est appelée chaque fois que l'on relâche la souris.
             Elle recueille les coordoonées de relachement de la souris (utilisé dans Jouer puis Impulsion pour appliquer à la boule tapée une vitesse).
        """

        self.xr, self.yr = event.x(), event.y()  #coordonnees du point de relachement de la souris (release)

        dx, dy = self.xr - self.xp, self.yr - self.yp
        # position relative du point de clique et de relachement, qui détermine la norme et le cap de la vitesse à conférer à la boule tapée.

        angle_b = orient_boule(dx,dy)                        #fonction de calcul d'arctangente, en fin de script
        self.table.plat.queue.alpha_b = angle_b*180/np.pi    # orientation que l'on donne à la boule

        self.table.plat.queue.p = min ((dx**2 + dy**2) * 0.3, 1400)  #puissance que l'on donne à la boule


def orient_queue (dx,dy):
    """
        calcule l'arctangente pour des valeurs non nécessairement situées dans la partie supérieure droite du cercle trigonométrique
    """
    if dx == 0:
        if dy < 0:
            angle = -np.pi / 2
        else:
            angle = np.pi / 2
    elif dy == 0:
        if dx > 0:
            angle = 0
        else:
            angle = -np.pi
    else:
        if dy > 0 and dx > 0:
            angle = np.arctan(dy / dx)  # orientation que l'on donne à la queue
        elif dy < 0 and dx > 0:
            angle = (- np.arctan(abs(dy / dx))) % (2 * np.pi)
        elif dy > 0 and dx < 0:
            angle = np.pi - np.arctan(abs(dy / dx))
        else:
            angle = np.pi + np.arctan(abs(dy / dx))
    return angle

def orient_boule (dx,dy):
    """
        calcule l'arctangente pour des valeurs non nécessairement situées dans la partie supérieure droite du cercle trigonométrique
    """
    return orient_queue (dx,dy) + np.pi


def lim_coord_queue (dx,dy,lim):
    """
        restreint la position de la queue à une distance max de liù autour de la boule tapée, au regard de la norme infinie = max (|dx|,|dy|)
    """
    if dx > 0:
        distx = min(dx, lim)  # distance réductible, à voir
    else:
        distx = max(dx, -lim)
    if dy > 0:
        disty = min(dy, lim)
    else:
        disty = max(dy, -lim)

    return distx, disty

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JeuBillard0()
    window.show()
    app.exec_()
