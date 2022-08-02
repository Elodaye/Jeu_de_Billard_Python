# Jeu_de_Billard_Python
Jeu de billard codé en python, première expérience de création d'IHM

Le premier commit correspond au travail brut effectué en première année d'école d'ingénieur avec un camarade. 
Les commits, versions et branches suivantes seront des améliorations personnelles ultérieures. 


## 1. Revue de tout le code, de façon à déceler ce qui devrait être structuré autrement

. Penser à mettre des attributs privés etc, enfin voir comment il faudrait faire

. Dans le plateau (racine du param) pouvoir changer le nombre de boule, que ça itère peut-importe le nombre -> OK

Il faut mettre un petit point de la couleur de a qui c'est de jouer -> OK

## 2. Ajout du son 

## 3. Ajout d'un interface pour choisir le mode de jeu -> OK

## 4. Nouveau mode de jeu, billard classique
Reste plus qu'à mettre le billard au bon endroit, graphiquement  --> OK
ajouter les trous du milieu --> OK

## factoriser le code, héritage. 

Bien remplir le readme pour montrer comment ça fonctionne et ce qu'on a fait 

travailler sur le code de la collision pour qu'elle soit clean

mettre des effets ? rétro et latéraux

voir pour mettre le jeu en réseau : pouvoir jouer avec Emilie

. Une fois que la boule tombe dans un trou, elle y reste en plein milieu jusqu'à la fin du tour : meilleur effet graphique, et le retour de la boule blanche sur la table ne vient pas interférer.  Deux fonction tombe, une pour la position pendant le tour. On gardera dans un liste les boules positions post-tour. Une autre qui prendra cette liste et mettra les boules tombées au bon endroit. 

. Finir le jeu en mettant la boule noire

. On peut placer la boule blanche sur la ligne de départ quand l'adversaire l'a faite tomber

. Rebonds orientés quand on est dans les coins

. Factoriser des fonctions hyper simples

. Le premier à marquer a la couleur de la boule