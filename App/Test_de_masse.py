import Methode_de_Jarvis as Jarvis
import Methode_de_Quickhull as Incremental
import Methode_de_Graham as Graham

import random as rd

LIMITE_X = 500
LIMITE_Y = 500
NB_TEST = 1000


def generation_nuage(NB_POINT):
    points = []  # Création d'une liste vide qui sauvegardera les
                 # coordonnées de chaque point du nouveau nuage
    for k in range(NB_POINT):
        point_x = rd.randint(0, LIMITE_X)
        point_y = rd.randint(0, LIMITE_Y)
        points.append((point_x, point_y))

    return points


def test(NB_POINT, NB_TEST):
    global moyenneJ, moyenneG, moyenneI

    moyenneG = moyenneJ = moyenneI = 0

    for k in range(NB_TEST):
        def calcul(NB_POINT):
            global iterationJ, iterationG, iterationI
            nuage = generation_nuage(NB_POINT)

            polygoneJ, iterationJ = Jarvis.recherche(nuage[:])
            polygoneI, iterationI = Incremental.recherche(nuage[:])
            polygoneG, iterationG = Graham.recherche(nuage[:])
            #Les fonctions renvoie aussi la liste des coodonnées des points composants,
            #mais ici on n'en à pas besoin

        try:
            calcul(NB_POINT)
        except IndexError:
            calcul(NB_POINT)    #Dans certains cas, aucune enveloppe convexe ne peut être formé
                                #(points aligner, points superposés...)
                                #La méthode de Jarvis va alors renvoyer l'erreur IndexError car celle ci
                                #supprime au fir et à mesure les points de la liste de nuage de point

        moyenneJ += iterationJ
        moyenneI += iterationI
        moyenneG += iterationG

    moyenneG = moyenneG/NB_TEST
    moyenneI = moyenneI/NB_TEST
    moyenneJ = moyenneJ/NB_TEST

    print(80 * "#" + 2 * "\n")
    print("Pour un nuage de ", NB_POINT, ' points')
    print("Le nombre moyen d'itérations pour la méthode de Jarvis est : ", f'{moyenneJ: .2f}')
    print("Le nombre moyen d'itérations pour la méthode de Graham est : ", f'{moyenneG: .2f}')
    print("Le nombre moyen d'itérations pour la méthode de Quickhull est : ", f'{moyenneI: .2f}', end= 3*'\n')


if __name__ == "__main__":
    test(15, NB_TEST)
    test(100, NB_TEST)
    test(500, NB_TEST)
    test(1000, NB_TEST)
    print("Les comparaisons ne sont pas forcément fiables car le placement",
         "de la variable permettant de calculer le nombre de boucles est imprécis",
         sep='\n', end=2*'\n')
