import random as rd
import os

DOSSIER = "./App/Échantillon de nuages"
CHEMIN = DOSSIER + "/Fichier de nuage de points classique.cla"

if not os.path.isdir(DOSSIER):
    os.mkdir(DOSSIER)


def ecriture(max_point=133, min_point=50, dim_cv=(500, 500)):
    MARGE_X = int(min(50, 0.1 * dim_cv[0]))  # Correspond à la marge avec le bord de la fenêtre
    MARGE_Y = int(min(50, 0.1 * dim_cv[1]))
    MARGE_POINT_X = int(min(20, 0.05 * dim_cv[0]))  # Correspond à l'écart entre les deux points
    MARGE_POINT_Y = int(min(20, 0.05 * dim_cv[1]))

    with open(CHEMIN, 'w') as chaîne:
        for nuage_n in range(1, 11):
            points = []
            nb_point_cible = rd.randint(min_point, max_point)

            while len(points) < nb_point_cible:
                trop_pret = False
                point_x = rd.randint(MARGE_X, dim_cv[0] - MARGE_X)
                point_y = rd.randint(MARGE_Y, dim_cv[1] - MARGE_Y)

                for precedent in points:  # On va faire le test pour savoir si le nouveau point n'est pas trop prêt d'un autre
                    if abs(precedent[0] - point_x) <= MARGE_POINT_X \
                            and abs(precedent[1] - point_y) <= MARGE_POINT_Y:
                        trop_pret = True
                        break  # sortit boucle for precedent in points

                if not trop_pret:
                    points.append((point_x, point_y))  # On ajoute le point dans la liste, la conversion en une chaine de caractère se fait plus tard pour faciliter les tests

            for i in range(len(points)):
                points[i] = str(points[i][0]) + ',' + str(points[i][1])  # Conversion en chaine de caratère
            chaîne.write(' ; '.join(points[:]) + '\n')
        chaîne.write(str(dim_cv[0]) + '*' + str(dim_cv[1]) + '*' + 'random')


if __name__ == "__main__":
    CHEMIN = DOSSIER + "/Fichier de nuage de points test methode classique.txt"
    ecriture()
    print("Écriture terminée")
