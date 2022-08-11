# Jeu_de_Billard_Python
Jeu de billard codé en Python, première expérience de création d'IHM

Le premier commit correspond au travail brut effectué en première année d'école d'ingénieur avec un camarade. A l'époque, il n'y avait qu'un seul mode de jeu, le billard français. 

<img src="https://github.com/Elodaye/Jeu_de_Billard_Python/blob/main/Images/mode1.png" alt="Alt text" title="Mode 1, billard français">

## 1. Revue de tout le code, de façon à déceler ce qui devrait être structuré autrement

## 2. Ajout d'une interface pour choisir le mode de jeu 

<img src="https://github.com/Elodaye/Jeu_de_Billard_Python/blob/main/Images/InterfaceMode.png" alt="Alt text" title="Mode 1, billard français">

## 3. Nouveau mode de jeu, billard classique, anglais 

<img src="https://github.com/Elodaye/Jeu_de_Billard_Python/blob/main/Images/mode2.png" alt="Alt text" title="Mode 1, billard français">

## 4. Factorisation et structuration du code

## Perspectives d'amélioration : 

. Travailler sur le code de la collision pour que le rendu soit le plus propre possible --> amélioration de la modélisation physique d'une collision

. Une fois que la boule tombe dans un trou, elle y reste en plein milieu jusqu'à la fin du tour : meilleur effet graphique, et le retour de la boule blanche sur la table ne vient pas interférer.  Deux fonction tombe, une pour la position pendant le tour. On gardera dans un liste les boules positions post-tour. Une autre qui prendra cette liste et mettra les boules tombées au bon endroit. 

. Finir le jeu en mettant la boule noire

. Pouvoir placer la boule blanche sur la ligne de départ quand l'adversaire l'a faite tomber

. Rebonds orientés quand on est dans les coins

. Le premier à marquer possède la couleur de la boule tombée

. Ajout de sons de jeu
