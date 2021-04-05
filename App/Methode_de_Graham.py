import math as mt


class Contour():
    def __init__(self, nuage):
        self.nuage = nuage
        self.Pivot = self.nuage[0]
        self.polygone = []
        self.iteration = 0
        self.tri()

    def tri(self):
        def confirmation_origine(origine):
            for k in range(1, len(self.nuage)):
                self.iteration += 1
                point = self.nuage[k]
                if point[0] == origine[0]:
                    self.nuage[0], self.nuage[k] = min(origine, point, key=lambda p: p[0]),\
                        max(origine, point, key=lambda p: p[0])
                    origine = self.nuage[0]
                else:
                    return origine

        def tangente(elem):
            "Pour calculer l'angle on utilise la méthode de la tangente"
            self.iteration += 1
            delta_y = origine[1] - elem[1]
            delta_x = origine[0] - elem[0]

            if delta_x < 0:
                angle = mt.pi
            else:
                angle = 0
            try:
                angle += mt.atan(delta_y / delta_x)
            except ZeroDivisionError:
                angle = mt.pi/2

            return angle

        self.nuage.sort(key=lambda p: p[1], reverse=True)
        self.iteration += len(self.nuage)
        origine = confirmation_origine(self.nuage[0])
        self.polygone.append(origine)
        self.iteration += 1

        "Le tri des points est effectué par ordre croissant des angles"
        self.nuage.sort(key=tangente)

        self.scan()

    def scan(self):
        def tourne_gauche(A, B, C):
            "Le calcul effectuer ici est un produit vectoriel"
            if (B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1]) <= 0:
                return True
            else:
                return False

        self.polygone.append(self.nuage[0])
        self.polygone.append(self.nuage[1])
        self.iteration += 2

        for point in self.nuage[2:]:
            while len(self.polygone) >= 2 and tourne_gauche(self.polygone[-2], self.polygone[-1], point):
                self.iteration += 1
                self.polygone.pop()  # Le point tester se trouve plus à l'extérieur que le derniers point gardé,
                                     # on l'enléve donc car il ne constitue pas forcément l'enveloppe convexe
            self.polygone.append(point)


def recherche(nuage):
    Polygone = Contour(nuage)
    return Polygone.polygone, Polygone.iteration
