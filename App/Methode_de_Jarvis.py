import math as mt


class Contour():
    def __init__(self, nuage):
        def distance(elem):
            return (elem[0] - origine[0]) ** 2 + (elem[1] - origine[1]) ** 2

        def confirmation_origine(origine):
            "Si un point a la même ordonnée que l'origine, on choisie celui dont l'abscisse est la plus petite"
            for k in range(1, len(self.nuage)):
                point = self.nuage[k]
                if point[1] == origine[1]:
                    self.nuage[0], self.nuage[k] = min(origine, point, key=lambda p: p[0]),\
                         max(origine, point, key=lambda p: p[0])
                    origine = self.nuage[0]
                else:
                    return origine

        self.nuage = nuage
        self.polygone = []
        self.iteration = 0

        self.nuage.sort(key=lambda p: p[1], reverse=True)
        self.iteration += len(self.nuage)
        origine = confirmation_origine(self.nuage[0])

        self.polygone.append(origine)
        self.iteration += 1

        "Recherche du deuxième point de l'enveloppe"
        point_next = self.nuage[1]
        for k in self.nuage[2:]:
            self.iteration += 1
            Y0 = origine[1] - k[1]
            X0 = origine[0] - k[0]
            Y1 = origine[1] - point_next[1]
            X1 = origine[0] - point_next[0]

            angle1 = mt.atan2(Y1,X1)
            angle0 = mt.atan2(Y0,X0)

            if abs(angle1 - angle0) <= mt.pi:
                if angle1 < angle0:
                    point_next = k

                elif angle1 == angle0:
                    point_next = max(point_next, k, key=distance)

            elif angle1 <= angle0 + 2*mt.pi:
                point_next = k

        self.scan(point_next)

    def scan(self, point):
        def distance(A, B, origine):
            "Fonction permettant de calculer la distance entre un point et l'origine"
            distA = (A[0] - origine[0]) ** 2 + (A[1] - origine[1]) ** 2
            distB = (A[0] - origine[0]) ** 2 + (A[1] - origine[1]) ** 2
            self.iteration += 1
            if distA > distB:
                return A
            else:
                return B

        if len(self.polygone) >= 3 and point == self.polygone[0]:
            return  # Fin de la recherche de l'enveloppe

        self.nuage.remove(point)  # On retire au fur et à mesure les points de l'enveloppe ainsi
                                  # ils ne sont pas retester dans la suite du programme
        self.polygone.append(point)

        point_next = self.nuage[0]

        mini = mt.inf
        for k in self.nuage:
            "Recherche du nouveau point de l'enveloppe"
            self.iteration += 1
            Y0 = self.polygone[-2][1] - self.polygone[-1][1]
            X0 = self.polygone[-2][0] - self.polygone[-1][0]
            Y1 = point[1] - k[1]
            X1 = point[0] - k[0]

            angle0 = mt.atan2(Y0, X0)
            angle1 = mt.atan2(Y1, X1)

            if abs(angle1 - angle0) <= mini:
                if angle1 != angle0:
                    mini = abs(angle1 - angle0)
                    point_next = k
                else:
                    '''Le point est aligné par rapport aux deux précédents, on garde celui
                    qui est le plus loin de l'origine'''
                    point_next = distance(k, point_next, self.polygone[-2])
                    self.polygone[-1] = point_next
                    break

        self.scan(point_next) #On utilise une méthode récursive ici


def recherche(nuage):
    Polygone = Contour(nuage)
    return Polygone.polygone, Polygone.iteration
