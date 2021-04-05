import random as rd
import json as js
from math import sqrt
import os


DOSSIER = "./App/Échantillon de nuages"
CHEMIN = DOSSIER + "/Fichier de nuage de points alignes.cla"

if not os.path.isdir(DOSSIER):
    os.mkdir(DOSSIER)


def ecriture(min_point=5, max_point=10, dim_cv=(500, 500)):
    def determination_droite():
        point_Ax = rd.randint(MARGE_X, dim_cv[0] - MARGE_X)
        point_Ay = rd.randint(MARGE_Y, dim_cv[1] - MARGE_Y)
        trop_pret = True
        while trop_pret:
            point_Bx = rd.randint(MARGE_X, dim_cv[0] - MARGE_X)
            point_By = rd.randint(MARGE_Y, dim_cv[1] - MARGE_Y)
            if abs(point_Ax - point_Bx) >= MARGE_POINT_X \
                    and abs(point_Ay - point_By) >= MARGE_POINT_Y:
                trop_pret = False

        pente = (point_By-point_Ay)/(point_Bx-point_Ax)
        constante = point_Ay - pente*point_Ax
        diagonale = sqrt(abs(point_Ax-point_Bx)**2 + abs(point_Ay-point_By))

        return (point_Ax, point_Ay), (point_Bx, point_By), pente, constante, diagonale

    with open(CHEMIN, 'w') as fichier:
        MARGE_X = int(min(50, 0.1*dim_cv[0]))  # Correspond à la marge avec le bord de la fenêtre
        MARGE_Y = int(min(50, 0.1*dim_cv[1]))
        MARGE_POINT_X = int(min(10, 0.05*dim_cv[0]))  # Correspond à l'écart entre les deux points
        MARGE_POINT_Y = int(min(10, 0.05*dim_cv[1]))
        fichier.write('[')  # Ouverture de la liste de données

        for nuage_n in range(1, 11):  # On crée  10 nuages pour le moment
            points = []  # Création d'une liste vide qui sauvegarde les coordonnées de chaque point du nouveau nuage
            A, B, pente, constante, diagonale = determination_droite()
            max_point_test = int(0.75 * (diagonale // sqrt(MARGE_POINT_Y **2 +MARGE_POINT_X **2)))
            max_point = min(max_point, max_point_test)
            if max_point < min_point:
                max_point, min_point = min_point, max_point

            points.extend((A, B))
            nb_points_cible = rd.randint(min_point, max_point)
            while len(points) < nb_points_cible:
                trop_pret = False
                point_x = rd.randint(MARGE_X, dim_cv[0] - MARGE_X)
                point_y = int(pente*point_x + constante)
                if point_y <= dim_cv[1] - MARGE_Y and point_y >=  MARGE_Y:
                    for precedent in points:  # On fait le test pour savoir si le nouveau point n'est pas trop prêt d'un autre
                        if abs(precedent[0] - point_x) <= MARGE_POINT_X \
                                and abs(precedent[1] - point_y) <= MARGE_POINT_Y:
                            trop_pret = True
                            break  #sortie de la boucle: for precedent in points

                    if not trop_pret:
                        points.append((point_x, point_y))

            js.dump(points, fichier)  # js ==> module json, dump ==> inscription de la liste points dans fichier
            fichier.write(',\n')
        js.dump((dim_cv, 'alignes'), fichier)
        fichier.write(']')  # fermeture de la liste de données


if __name__ == "__main__":
    CHEMIN = DOSSIER + "/Fichier de nuage de points aligner test.txt"
    ecriture()
    print("Écriture terminée")
