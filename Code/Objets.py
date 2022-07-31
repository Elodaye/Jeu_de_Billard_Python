import numpy as np
from numpy.random import randint
from matplotlib import pyplot as plt
import time
from PyQt5 import QtGui, QtCore
from abc import ABCMeta, abstractmethod

class Boule(metaclass = ABCMeta):  # une boule (blanche ou colorée), ses caractéristiques (physiques et cinétiques)
    def __init__(self, x, y, r=0.3, m=1):  # r le rayon, m la masse
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.vx = 0
        self.vy = 0


    @abstractmethod
    def dessinimage (self,qp) :
        pass


    def evolution(self, dt,k, eps = 0.8):
        """
        En l'absence de collision (ici donc), on suppose le mouvement des boules rectiligne (bords ou autres boules).
        Actualise la vitesse et la position de la boule.

        entrées : float dt qui correspond à l'intervalle de temps entre chaque actualisation de la vitesse et de la position.
                  float k dans [0,1], coefficient de résistance au roulement.
                  float eps: seuil de vitesse min pour laquelle on considèrera que la boule est immobile sur la table.

        sortie  : 0 si la boule est considérée immobile, 1 si elle est en mouvement.
        """
        if self.vx**2 + self.vy**2 < eps :
            self.vx = 0
            self.vy = 0
            return 0
        else :
            self.vx = k*self.vx
            self.vy = k * self.vy
            self.x += dt * self.vx
            self.y += dt * self.vy
            return 1

    def rebond(self, bord):
        """
        simule un rebond sur une paroi droite. Actualise la vitesse de la boule après rebond.

        entrée : string caractérisant la paroi sur laquelle il y a rebond (paroi nord, sud, est ou ouest)

        sortie : la nouvelle vitesse de la boule, après rebond
        """

        if bord in ['N', 'S']:
            self.vy = - self.vy
        elif bord in ['O', 'E']:
            self.vx = - self.vx


    def coll(self, boule2):
        """
        Simule la collision entre 2 boules. Change la vitesse de ces 2 boules.

        entrée : boule2, la boule qui entre en collision avec la première. On a accès à leur position, et à leur vitesse (norme et direction).

        sortie : None
        """

        alpha = np.linspace (0,2*np.pi,100)
        d = abs ((self.x + self.r - boule2.x)**2 + boule2.y**2 )
        angle = 0
        for a in alpha :
            da = abs ((self.x + self.r*np.cos (a) - boule2.x)**2 + (self.y + self.r*np.sin (a)- boule2.y)**2 )
            if d > da :
                angle, d = a , da   # pour le point tangent aux 2 boules, angle formé par Ox et la droite passant par le centre de la 1ere boule et le point tangent

        v1 = (self.vx**2 + self.vy**2)**0.5
        v2 = (boule2.vx ** 2 + boule2.vy ** 2) ** 0.5
        if v1 == 0 :
            if boule2.vx == 0:
                if boule2.vy < 0:
                    angle_b1 = -np.pi / 2
                else:
                    angle_b1 = np.pi / 2
            elif boule2.vy == 0:
                if boule2.vx > 0 :
                    angle_b1 = np.pi
                else :
                    angle_b1 = -np.pi
            else:
                if boule2.vy > 0 and boule2.vx > 0:
                    angle_b1 = np.arctan(boule2.vy / boule2.vx)  # angle_b1 direction de la boule mobile
                elif boule2.vy < 0 and boule2.vx > 0:
                    angle_b1 = (- np.arctan(abs(boule2.vy / boule2.vx))) % (2 * np.pi)
                elif boule2.vy > 0 and boule2.vx < 0:
                    angle_b1 = np.pi - np.arctan(abs(boule2.vy / boule2.vx))
                else:
                    angle_b1 = np.pi + np.arctan(abs(boule2.vy / boule2.vx))
            angle = (angle + np.pi )% (2*np.pi)
            d_angle = (abs(angle_b1 - angle))    #
            v1_p = v2*np.cos(d_angle)
            v2_p = v2*np.sin (d_angle)
            boule2.vx, boule2.vy, self.vx, self.vy = v2_p*np.cos ((2*angle_b1 - angle)%2*np.pi), v2_p*np.sin ((2*angle_b1- angle)%2*np.pi), v1_p*np.cos (angle ), v1_p*np.sin (angle)
        else :
            if self.vx == 0:
                if self.vy < 0:
                    angle_b1 = -np.pi / 2
                else:
                    angle_b1 = np.pi / 2
            elif self.vy == 0:
                if self.vx > 0 :
                    angle_b1 = np.pi
                else :
                    angle_b1 = -np.pi
            else:
                if self.vy > 0 and self.vx > 0 :
                    angle_b1 = np.arctan(self.vy / self.vx)
                elif self.vy<0 and self.vx > 0 :
                    angle_b1 = (- np.arctan(abs(self.vy / self.vx))) % 2 * np.pi
                elif self.vy > 0 and self.vx< 0 :
                    angle_b1 = np.pi - np.arctan(abs(self.vy / self.vx))
                else :
                    angle_b1 = np.pi + np.arctan(abs(self.vy / self.vx))
            d_angle = abs(angle_b1 - angle)  % (np.pi /2) #appatient à [0; pi/2]
            v1_p = v1*np.sin(d_angle)
            v2_p = v1*np.cos (d_angle)
            boule2.vx, boule2.vy, self.vx, self.vy = v2_p*np.cos (angle), v2_p*np.sin (angle), v1_p*np.cos ((2*angle_b1 - angle)%(2*np.pi)), v1_p*np.sin ((2*angle_b1  -angle)%(2*np.pi))

class Boule_coloree(Boule):
    # on définit la classe représentant les boules colorées, classe qui hérite de la classe Boule

    image = QtGui.QImage("../Images/rouger.png")
    def __init__(self, x, y, r = 0.03, type = 'R'):
        super().__init__(x, y,r)
        if type == "R":
            self.image = QtGui.QImage("../Images/rouger.png")
            self.type = "R"
        elif type =="J":
            self.image = QtGui.QImage("../Images/jauner.png")
            self.type = "J"
        else :
            self.image = QtGui.QImage("../Images/noirer.png")
            self.type = "N"

    def dessinimage(self, qp):
        """
        dessinimage :
        Affiche l'image de la boule rouge sur la table de billard, à son emplacement calculé

        entrée : le peintre utilisé pour afficher l'image

        sortie  : 1 si la boule est considérée immobile, 0 si elle est en mouvement."""
        if self.type == "R":
            qp.drawImage(QtCore.QRect(10+ self.x+50 -3 , self.y + 10 + 52 -3 , 40,40 ), self.image)
        elif self.type == "J":
            qp.drawImage(QtCore.QRect(10 + self.x + 50, self.y + 10 + 52 , 32, 32), self.image)
        else :
            qp.drawImage(QtCore.QRect(10 + self.x + 50 -3 , self.y + 10 + 52 -3 , 40, 40), self.image)

class Boule_blanche(Boule):  # on définit la classe représentant les boules blanches, classe qui hérite de la classe Boule
    image = QtGui.QImage("../Images/blancher.png")
    def __init__(self, x, y, r = 0.03):  #classe qui hérite de la classe boule
        super().__init__(x, y,r)

    def impulsion(self, cap_V0, norme_V0):
        """
        Met en mouvement la boule blanche, en modifiant sa vitesse.

        entrées : float cap_V0 : angle vers lequel la boule doit être propulsée
                  float norme_V0: norme de la vitesse donnée à la boule blanche

        sortie  : None
        """

        self.vy = norme_V0 * np.sin(cap_V0 * np.pi / 180) #v0[0]
        self.vx = norme_V0 * np.cos(cap_V0 * np.pi / 180) #v0[1]
        # Recevoir uneimpulsion est une caracteristique propre aux boules blanches selon les règles du billard
        # Elles sont propulsées par un coup de queue, qui leur confère un mouvement initial representé par cap_V0 et norme_V0


    def dessinimage(self, qp):
        """
        Affiche l'image de la boule blanche sur la table de billard, à son emplacement calculé

        entrée : le peintre utilisé pour afficher l'image

        sortie  : 1 si la boule est considérée immobile, 0 si elle est en mouvement.
        """

        qp.drawImage(QtCore.QRect(10+self.x +50 ,self.y + 10 + 52,30,30), self.image)


class Plateau(list):  # le plateau est un espace délimité, composé d'une liste de boules
    def __init__(self, l=10, L=10, nb=2, nc=1, k = 0.998, mode = 1):
        super().__init__(self)
        self.bs, self.bn, self.bo, self.be = l, 0, 0, L   # bord sud, nord, ouest, est
        #self.n = nb + nc  # nombre total de boules, dans le cas général, autre que dans le jeu actuel où il vaut 3
        self.k = k  # coefficient de résistance au roulement
        #self.mode = mode  # choix du mode de jeu, non encore implémenté
        self.queue = Queue()
        self.point = Point()
        self.viseur = Point_clique() #3 instances des classes définies juste apres

        #On joue uniquement dans le mode normal, avec deux boules blanches et une rouge, placées de maniere precise au debut de la partie:
        if mode == 1:
            self.n = 3
            self.append(Boule_blanche(0.2 * self.be, 0.75 * self.bs, r= 1.3*self.be * 0.03 / 2.54))
            self.append(Boule_blanche(0.2 * self.be, 0.25 * self.bs, r=1.3*self.be * 0.03 / 2.54))
            self.append(Boule_coloree(0.8 * self.be, 0.5 * self.bs, r=1.3*self.be * 0.03 / 2.54))
        else :
            self.n = 16
            self.append(Boule_blanche(0.2 * self.be, 0.5 * self.bs, r=1.3 * self.be * 0.03 / 2.54))

            self.append(Boule_coloree(0.8 * self.be, 0.38 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'R'))
            self.append(Boule_coloree(0.8 * self.be, 0.44 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))
            self.append(Boule_coloree(0.8 * self.be, 0.5 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))
            self.append(Boule_coloree(0.8 * self.be, 0.56 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'R'))
            self.append(Boule_coloree(0.8 * self.be, 0.62 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))

            self.append(Boule_coloree(0.76 * self.be, 0.41 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))
            self.append(Boule_coloree(0.76 * self.be, 0.47 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'R'))
            self.append(Boule_coloree(0.76 * self.be, 0.53 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))
            self.append(Boule_coloree(0.76 * self.be, 0.59 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'R'))

            self.append(Boule_coloree(0.72 * self.be, 0.44 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type='R'))
            self.append(Boule_coloree(0.72 * self.be, 0.5 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type='N'))
            self.append(Boule_coloree(0.72 * self.be, 0.56 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))

            self.append(Boule_coloree(0.68 * self.be, 0.47 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'J'))
            self.append(Boule_coloree(0.68 * self.be, 0.53 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type = 'R'))

            self.append(Boule_coloree(0.64 * self.be, 0.5 * self.bs, r=1.3 * self.be * 0.03 / 2.54, type='R'))



    def proche_bord(self, posx, posy, i):
        """
        Si une boule est proche d'un bord, et que l'on constate que la boule se rapproche de ce bord,
        on appelle la fonction rebond, en précisant sur quelle paroi celui-ci survient.

        entrées :
                posx, posy : liste des abscisses et ordonnées de toutes les boules du plateau
                int i : l'indice de la boule dans la liste de boules (self.plateau), dont on veut vérifier la proximité du bord.

        sortie  : None
        """

        if self[i].x < 0.02*self.be:  # on est proche d'un bord (ici le bord est)
            if (len(posx[0]) <= 1) or (posx[i][-2] > self[i].x):  # on vérifie qu'on est pas en tout début de simulation,
                Boule.rebond(self[i], 'O')  # ou que l'on est pas déjà en train de repartir du bord
        elif self[i].x > self.be *(1- 0.02):
            if len(posx[0]) <= 1 or posx[i][-2] < self[i].x:
                Boule.rebond(self[i], 'E')
        elif self[i].y < 0.02*self.bs:
            if len(posx[0]) <= 1 or posy[i][-2] > self[i].y:
                Boule.rebond(self[i], 'N')
        elif self[i].y > self.bs * (1- 0.02):
            if len(posx[0]) <= 1 or posy[i][-2] < self[i].y:
                Boule.rebond(self[i], 'S')


    def collisions(self,col,i,j,n): #méthode récursive
        """"
        Détecte chaque collision imminente entre les boules, et simule la déviation de trajectoire associée, en appelant la fonction coll, qui gère la collision entre 2 boules

        Entrees:
                col: liste vide à l'initialisation de la recursion
                i, j : deux boules
        """

        #Principe:
        # On mesure la distance entre chaque centre de boule
        # Si elle est trop faible, il y a collision, donc échange de quantité de mvt

        #Col se remplit au fur et à mesure des appels recursifs quand des boules sont proches

        if n == len(self) * (len(self)-1)/2 :
            for [i, j] in col:
                Boule.coll(self[i], self[j])
            return True
        else :
            if ((self[i].x - self[j].x) ** 2 + (self[i].y - self[j].y) ** 2) ** 0.5 <= self[i].r*(1+0.002) + self[j].r:
                    col.append([i, j])  # boules trop proches, leur trajectoire va être déviée par la collision (méthode coll)
            if j+ 1 == i :
                return self.collisions(col,i+1,0,n+1)
            return self.collisions(col,i,j+1, n+1)


    def un_coup(self, dt,joueur=1):
        """
        On simule un coup de queue : on met en mouvement la boule blanche, et on traite collisions entre boules et avec la paroi.
        Une fois le coup terminé (lorsque les boules ont toutes une vitesse inférieure à eps), on donne la vitesse 0 à chaque boule, pourqu'elles soient vraiment immobiles pour le tour suivant

        entrées :
                dt: float, correspond à l'intervalle de temps entre chaque actualisation de la vitesse et de la position.
                joueur: int, vaut 1 ou 0, permet d'assigner le coup de queue au joueur qui l'a effectué.
        """

        print ("c'est au joueur {} de jouer".format (joueur)) #ligne utilisee pour les tests
        MVT = np.array ([1 for i in range (self.n)]) # Vecteur de test: à chaque indice de boule, la methode evolution associera 1 si elle est en mouvement, 0 si elle est arretee
        Boule_blanche.impulsion(self[joueur], 48, 400)

        posx, posy = [[] for i in range(self.n)], [[] for i in range(self.n)]  # pour garder en mémoire les positions passées
        for i in range(self.n):
            posx[i].append(self[i].x)
            posy[i].append(self[i].y)

        while any (MVT): #Tant qu'il n'y a pas que des 0 dans MVT
            for i in range(self.n):
                self.proche_bord(posx, posy, i)  # on gère les rebonds sur les bords
            self.collisions([],1,0,0)  # on gère les collisions entre boules

            for i in range(self.n): # while self.T != np.array ([0 for i in range self.n]):
                MVT[i] = Boule.evolution(self[i], dt,self.k, 0.05*self.be)  # On fait evoluer le vecteur MVT  et on actualise la vitesse et la position de chaque boule par rapport à l'instant precedent
                posx[i].append(self[i].x)
                posy[i].append(self[i].y)

        for i in range(self.n):
            self[i].vx, self[i].vy = 0,0  #on donne la vitesse 0 à chaque boule, pourqu'elles soient vraiment immobiles pour le tour suivant

class Partie ():
    def __init__ (self, nb_coups, dt = 0.005, LL = 10, ll=10, mode = 1):
        self.nb_coups = nb_coups
        self.dt = dt
        self.c = 0  # on s'arrête à nb_coups
        self.points = [0,0]  #en position 0, le joueur 2
        self.l = ll
        self.L= LL
        self.plat = Plateau(l=self.l, L=self.L, mode = mode)

    def jouer (self) :  #En réalité, cette fonction n'est jamais appelée dans l'ihm, car on a adapte le corps de la methode dans l'IHM
        """
        On simule une partie: une succession de coup, effectués par l'un ou l'autre des joueurs.
        """

        i = 1
        while self.c < self.nb_coups :  # il reste encore des coups à jouer
            self.c+=1
            ANA = [self.plat[i%2 -1].vx,self.plat[i%2 -1].vy, self.plat[i%2 -2].vx, self.plat[i%2 -2].vy]  #position avant le tir des boules à toucher
            Plateau.un_coup (self.plat, self.dt,i %2)
            if ANA[0] - self.plat[i%2 -1].vx == 0 and ANA [1] - self.plat[i%2 -1].vy and ANA[2] - self.plat[i%2 -2].vx == 0 and ANA [3] - self.plat[i%2 -3].vy ==0 :
                print ("Vous avez marqué un point")  # les coordonnées des 2 boules ont changé, on a réussi le coup
                self.points [i %2] += 1
            else :
                print ("Pas de chance... Au joueur suivant")
                i += 1
        print ("Joueur 1 : {} points /n Joueur 2 : {} points ".format (self.points[1], self.points[0]))
        if self.points[0] != self.points[1]:
            if self.points [0] > self.points [1]:
                g = '2'
            elif self.points [0] > self.points [1]:
                g = '1'
            print ("Le joueur {} a gagné ! Félicitations !".format (g))
        else :
            print ("Egalité ! Bravo à vous deux !")

class Queue ():

    l = QtGui.QImage("../Images/queues_l/qb8.png")
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = 0
        self.alpha_q = 180  #pour afficher la queue
        self.alpha_b = 0  # pour donner le coup de queue ,direction qu'on donnera à la boule
        #il y a pi de différence entre les 2 alpha

    def dessinimage(self, qp,angle, boulex=-10,bouley=-10):
        """
        Affiche la queue dont l'utilisateur modifie l'angle par rapport à la boule qu'il veut frapper et qu'il écarte plus ou moins de la boule, pour lui donner
        plus ou moins de vitesse.

        entrée : qp, le peintre utilisé pour afficher l'image
                 angle : valeur entre 0 et 360, orientation de la queue
                 boulex, bouley : coordoonées de la boule visee

        sortie  : 1 si la boule est considérée immobile, 0 si elle est en mouvement.
        """

        LISTE = ["../Images/queues_l/qb24.png"]
        LISTE = LISTE + [ "../Images/queues_l/" + "qb" + str(i) + ".png" for i in range (1, 24)]
        # liste de 24 images de queues inclinees tous les 15 degrés.

        self.l = QtGui.QImage (LISTE[int(angle * 24 / 360)]) # choix de la bonne image dans la liste LISTE
        qp.drawImage(QtCore.QRect(boulex-290 -21.5, bouley-285 -24.2, 600, 600) ,self.l)

class Point ():
    image = QtGui.QImage("../Images/point2.png")

    def dessinimage(self, qp, boulex,bouley):
        """
        Affiche le point rouge se situant au centre de la boule blanche dans laquelle il faut tirer avec la canne.

        entrée : qp, le peintre utilisé pour afficher l'image
                 boulex, bouley : coordoonées de la boule visee

        sortie  : 1 si la boule est considérée immobile, 0 si elle est en mouvement.
        """

        qp.drawImage(QtCore.QRect(boulex +93 -23 , bouley+95 -24.6, 10, 10), self.image)

class Point_clique ():
    image = QtGui.QImage("../Images/point_clique2.png")

    def dessinimage(self, qp, boulex,bouley):
        """
        dessinimage :
        Affiche l'endroit ou l'on a cliqué sur le billard, pour que l'on ait une idée de la trajectoire de la boule, qui se basse sur
        l'angle et la distance entre le point du et le point du relachement.

        entrée : qp, le peintre utilisé pour afficher l'image
                 boulex, bouley : coordoonées de la boule visee
        """
        qp.drawImage(QtCore.QRect(boulex-20 , bouley-45, 22, 22), self.image)

if __name__ == '__main__':
    p = Partie (3,0.1)
    Partie.jouer (p)