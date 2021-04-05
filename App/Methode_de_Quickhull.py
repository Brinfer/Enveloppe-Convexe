class Contour():
    def __init__(self, nuage):
        self.nuage = nuage
        self.polygone = []
        self.iteration = 0

        self.tri()

    def tri(self):
        "Fonction permettant de trier le nuage par ordonnée décroissante"

        def confirmation_origine(origine):
            for k in range(1, len(self.nuage)):
                point = self.nuage[k]
                if point[0] == origine[0]:
                    self.nuage[0], self.nuage[k] = min(origine,
                                                       point,
                                                       key=lambda p: p[0]), \
                        max(origine, point, key=lambda p: p[0])
                    origine = self.nuage[0]
                else:
                    return origine

        self.nuage.sort(key=lambda p: p[1], reverse=True)
        self.iteration += len(self.nuage)
        origine = confirmation_origine(self.nuage[0])
        self.polygone.append(origine)
        self.iteration += 1
        self.scan()

    def scan(self):
        def position_relative(A, B, C):
            "Le calcul effectuer est un produit vectoriel"
            d = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
            if d >= 0:
                return True  # Point C à gauche de la droite(AB) ou sur la droite(AB)
            else:
                return False  # Point C à droite de la droite(AB)

        for i in range(1, len(self.nuage)):
            "Recherche des points formant la première demie enveloppe"
            self.polygone.append(self.nuage[i])
            while len(self.polygone) >= 3:
                self.iteration += 1
                C = self.polygone.pop() # Renvoie le dernier élément de la liste et le supprime de la liste
                B = self.polygone.pop()
                A = self.polygone.pop()

                '''On regarde si le point C est à gauche ou à droite de A et B"
                On retourne True si C est à droite de AB ou sur AB'''
                if position_relative(A, B, C):
                    self.polygone.append(A)
                    self.polygone.append(C)
                else:
                    self.polygone.append(A)
                    self.polygone.append(B)
                    self.polygone.append(C)
                    break  # Sortie boucle while

        self.polygone.append(self.nuage[len(self.nuage)-2])
        self.iteration += 1
        for i in range(len(self.nuage) - 3, -1, -1):
            "Recherche des points formant la deuxième demie enveloppe"
            self.polygone.append(self.nuage[i])
            while len(self.polygone) >= 3:
                self.iteration += 1
                C = self.polygone.pop()
                B = self.polygone.pop()
                A = self.polygone.pop()
                if position_relative(A, B, C):
                    self.polygone.append(A)
                    self.polygone.append(C)
                else:
                    self.polygone.append(A)
                    self.polygone.append(B)
                    self.polygone.append(C)
                    break


def recherche(nuage):
    Polygone = Contour(nuage)
    return Polygone.polygone, Polygone.iteration
