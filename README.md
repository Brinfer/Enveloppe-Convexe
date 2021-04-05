# Enveloppe-Convexe

<p align="center">

<img  src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Logo_ESEO_GROUPE.jpg/1280px-Logo_ESEO_GROUPE.jpg" width="200" height="">

</p>

## Introduction

Projet Math-Info réalisé en 2019, dans le cadre des ma 2ème années études en cycle préparatoire.
Le but du projet est de calculer une enveloppe convexe à partir d’un nuage de points.
C'est à dire une enveloppe qui regroupe l'ensemble des points d'un nuage de points, et qui soit la plus petite possible.

</br>

Le projet est intégralement réalisé en `python 3`. Il ne nécessite que __Tkinter__ et le module __json__ qui sont pré-installé avec python (sauf __Tkinter__ sur certaines distribution _Unix_, dans ce cas référer vous à la documentation de vôtre distribution).

## Lancement

Entrer la commande `python ./App/Menu.py`, une interface apparaît afin de sélectionner la méthode.
</br>
Au premier lancement de l'application, des popups d'erreur apparaîtront car aucun fichier contenant des données pour les nuages ne sont présents. Appuyer sur __Oui__ afin que le reste du programme se poursuive

## Utilisation

+ Le bouton __Nouveaux Nuages__ permet de générer 10 nouveaux nuages avec les paramètres sélectionnés.

* Le bouton __Changer Options__ permet:
  * De changer les nombre maximal/minimal de points dans le nuage.
  * De changer la taille du canevas : dans ce cas, le nombre maximal de points possibles peut être modifié afin d'éviter que le programme ne se trouve dans une boucle infinie en tentant de générer un nouveau nuage (les points ne peuvent pas se superposer).
  </br>
  Le canevas peut être rectangulaire, mais les dimensions restent comprises entre 150 et 1000. En cas de non respect de ces conditions, les valeurs sont automatiquement changées.

* Le bouton __Changer paramètre globaux__ qui se trouve dans la même fenêtre permet de changer:
  * la couleur des points
  * la couleur des polygones (en fonction de la méthode utilisée)
  * l'épaisseur du trait du polygone
  * la forme des points (ils ne doivent être composés que d'un seul caractère)
  * la couleur de fond du canevas
    * :warning:
      * la couleur noire est interdite
      * la couleur blanche n'est disponible que pour le canevas
      * les couleurs doivent être distinctes (deux méthodes ne peuvent être de la même couleur ni de la même couleur que le point/canevas)
  * Il est possible de retirer et d'ajouter des points au nuage grâce à un clic gauche (ajout) ou droit(retrait) dans la fenêtre du nuage.

</br>

Le programme `Menu.py ` lit les fichier: `Fichier nuage de points.cld`. Pour pouvoir lire ce qui est écrit depuis son ordinateur, il suffit de changer l'extension par `.txt` ou alors de lancer les programmes `App/Creation_nuage_de_point_classique.py` ou `App/Creation_nuage_de_point_json.py`.
Un nouveau fichier texte sera alors généré mais pas utilisé par le programme `Menu.py`.

Dans le cas où il n'y a aucun fichier `Fichier de nuage de point.cld`, il vous sera proposé de générer un fichier. En cas de refus, le programme s'arrête.

</br>

Il est possible d'ouvrir un fichier de nuage (extension: `.cld`) depuis le menu déroulant du canevas, grâce au bouton __Ouvrir__.
Un échantillon de nuages simples est déjà disponible.
</br>
Il est possible de créer son propre nuage depuis le canevas, il suffit de sélectionner __Creer nouveau nuage__ dans le menu déroulant, l'ensemble des items affichés sont alors effacés.
</br>
On peut alors sauvegarder ce nouveau nuage en cliquant sur __Enregistrer__ du menu déroulant.
Dans le cas où l'on souhaite réutiliser ce nuage par la suite, il faut le sauvegarder sous le format `.cld` au format `.txt`

</br>

Le fichier `Texte.int` ne doit surtout pas être modifié ou supprimé, dans le cas où celui-ci est corrompu, le programme ne peut plus fonctionner, celui-ci va alors automatiquement se fermer.

</br>

Le programme `Test_de_masse.py` permet de comparer sur un gros volume de nuage les différentes méthodes en retournant le nombre moyen d'itérations dont la méthode a besoin pour obtenir l'enveloppe convexe.
</br>
Pour le lancer entrer la commande `python ./App/Test_de_masse.py`
