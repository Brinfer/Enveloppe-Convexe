import json as js  # Explication  ==> voir fin de page
import random as rd
import os

DOSSIER = "./App/Échantillon de nuages"
CHEMIN = DOSSIER + "/Fichier de nuage de points.cla"

if not os.path.isdir(DOSSIER):
    os.mkdir(DOSSIER)


def ecriture(max_point=133, min_point=50, dim_cv=(500, 500)):
    MARGE_X = int(min(50, 0.1 * dim_cv[0]))  # Correspond à la marge avec le bord de la fenêtre
    MARGE_Y = int(min(50, 0.1 * dim_cv[1]))
    MARGE_POINT_X = int(min(20, 0.05 * dim_cv[0]))  # Correspond à l'écart entre les deux points
    MARGE_POINT_Y = int(min(20, 0.05 * dim_cv[1]))
    with open(CHEMIN, 'w') as fichier:
        fichier.write('[')  # Ouverture de la liste de données
        for nuage_n in range(1, 11):
            points = []
            nb_points_cible = rd.randint(min_point, max_point)
            while len(points) < nb_points_cible:
                trop_pret = False
                point_x = rd.randint(MARGE_X, dim_cv[0] - MARGE_X)
                point_y = rd.randint(MARGE_Y, dim_cv[1] - MARGE_Y)

                for precedent in points:  #On va faire le test pour
                                          #savoir si le nouveau point n'est pas trop prêt d'un autre
                    if abs(precedent[0] - point_x) <= MARGE_POINT_X \
                            and abs(precedent[1] - point_y) <= MARGE_POINT_Y:
                        trop_pret = True
                        break  # Sortie de la boucle: for precedent in points

                if not trop_pret:
                    points.append((point_x, point_y))

            js.dump(points, fichier)  # js ==> module json, dump ==> inscription de la liste points dans fichier
            fichier.write(',\n')
        js.dump((dim_cv, 'random'), fichier)
        fichier.write(']')  # Fermeture de la liste de données


if __name__ == "__main__":
    CHEMIN = DOSSIER + "/Fichier de nuage de points test methode de json.txt"
    ecriture()
    print("Ecriture terminer")
