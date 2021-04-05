import tkinter as saisie_incorrecte
import json as js
import time as time
import sys as sys
import os
import tkinter.messagebox as tkm
import tkinter.colorchooser as tkc
import tkinter.simpledialog as tks
import tkinter.filedialog as tkf

"Importation des fichiers python comme un module"
import Creation_nuage_de_point_json as cloud
# import Creation_nuage_de_point_classique as cloud
import Creation_de_nuage_de_point_alignes as cloud_al

import Methode_de_Jarvis as Jarvis
import Methode_de_Quickhull as Incremental
import Methode_de_Graham as Graham

parametres_globaux = {'Jarvis': '#0080c0',  # Bleu
                      'Graham': '#008000',  # Orange
                      'Quickhull': '#ff8000',  # Vert
                      'Point':  '#493993',  # Bleue spécial
                      'Canevas': '#ffffff',  # Blanc
                      'Point_texte': '☠',
                      'Epaisseur trait': 1}

if not os.path.isdir(cloud.DOSSIER):
    os.mkdir(cloud.DOSSIER)


class Recup_data():
    "Lecture du fichier texte contenant tout les points"
    def __init__(self):
        self.CHEMIN = cloud.CHEMIN  # Recupération du chemin d'accès des fichiers texte
        self.type = "random"
        self.ecrit_fichier = False

    def max_point(self):
        "Fonction permettant de déterminer combien de points peuvent se trouver sur notre Canvas"
        surface = (self.DIM_CV_X - 2 * self.MARGE_X) * (self.DIM_CV_Y - 2 * self.MARGE_Y)
        surface_point = self.MARGE_POINT_X * self.MARGE_POINT_Y
        return (surface / surface_point) // 3

        # surface/surface_point ==> Nombre max de points si les points sont bien rangés'
        # On divise par trois pour que la régénération des nuages de points se fasse facilement
        # avec un minimum de superpositions

    def next_step_init(self, other):
        self.other_error = other.fichier_corrompu

    def recup(self):
        # Le try except est là pour que ce programme puisse lire le fichier qu'importe la manière
        # dont il a été édité
        try:
            "Si le fichier a été édité avec le module json"
            with open(self.CHEMIN, 'r') as fichier:
                data = js.load(fichier)
                INFO = data.pop()
                self.DIM_CV_X = INFO[0][0]
                self.DIM_CV_Y = INFO[0][1]
                self.type = INFO[-1]

        except js.JSONDecodeError:  # Code d'erreur renvoyé quand le module n'est pas capable de lire le fichier
            try:
                "Si le fichier n'est pas lisible pour le module json"
                data = []
                with open(self.CHEMIN, 'r') as fichier:
                    for ligne in fichier:  #Une ligne correspond à un nuage
                        ligne = ligne.strip().split(';')
                        # On sépare point par point, une ligne devient une liste
                        if len(ligne) >= 3:
                            for i in range (len(ligne)):
                                ligne[i] = ligne[i].split(',')  # On sépare les coordonnées du point
                                ligne[i][0] = int(ligne[i][0])
                                ligne[i][1] = int(ligne[i][1])
                            data.append(ligne)
                        else:
                            ligne[0] = ligne[0].split('*')
                            self.DIM_CV_X = int(ligne[0][0])
                            self.DIM_CV_Y = int(ligne[0][1])
                            self.type = ligne[0][-1]

            except ValueError:
                "Un élément de la liste des coordonnées n'est pas un numéro"
                return self.error()

            except IndexError:
                "Une partie des informations contenue dans le fichier n'est pas présent"
                return self.error()

        except FileNotFoundError:
            "Le fichier n'existe pas"
            if not self.ecrit_fichier:
                self.ecrit_fichier = True
                return self.error()
            else:
                self.ecrit_fichier = False
                cloud.ecriture()
                return self.recup()

        if data == []:
            "Le fichier était vide"
            return self.other_error()

        else:
            if self.type == 'random':
                "Enregistrement des informations nécessaire pour la suite du programme"
                self.MARGE_POINT_X = int(min(20, 0.05 * self.DIM_CV_X))
                self.MARGE_POINT_Y = int(min(20, 0.05 * self.DIM_CV_Y))
                self.MARGE_X = int(min(50, 0.1 * self.DIM_CV_X))
                self.MARGE_Y = int(min(50, 0.1 * self.DIM_CV_Y))
                self.MAX_POINT = self.max_point()
                self.MIN_POINT = 50
            return data

    def error(self):
        if self.type == 'alignes':
            return self.other_error()
        else:
            return self.other_error()


class Timer():
    "Cette classe n'est pas parfaite, il arrive que la valeur de chrono soit égale à 0.0"
    def start(self):
        self.start_time = time.time()

    def stop(self):
        stop_time = time.time()
        self.chrono = stop_time - self.start_time
        self.chrono = str(self.chrono)[3:8]
        if self.chrono != '':
            self.chrono += texte['interface']['label']['time']['unite']
        else:
            self.chrono = texte['interface']['label']['time']['error']


class Interface():
    "Class dédier à la partie commande du programme"
    def __init__(self):
        self.fen = saisie_incorrecte.Tk()
        self.fen.title(texte['interface']['title'])
        self.fen.resizable(width=False, height=False)   # Impossibilité de modifier les dimensions de la fenêtre
        self.fen.geometry('+0+0')   # Apparition de la fenêtre dans le coin supérieur gauche de l'écran
        self.fen.protocol("WM_DELETE_WINDOW", sys.exit) # Dans le cas où l'on ferme la fenêtre, le programme se ferme

        "Création de la partie dédiée à la méthode de Jarvis"
        self.bp_jarvis = saisie_incorrecte.Button(self.fen,
                                                  text=texte['interface']['bouton']['methode'] + 'Jarvis',
                                                  bg=parametres_globaux['Jarvis'], fg='white',
                                                  command=lambda: self.recherche_enveloppe('Jarvis'))
        self.bp_jarvis.grid(row=0, column=0)

        self.texte_temps_jarvis = saisie_incorrecte.Label(self.fen,
                                                          text=texte['interface']['label']['time']['default'] + texte['interface']['label']['error'])
        self.texte_temps_jarvis.grid(row=1, column=0)

        self.texte_iteration_jarvis = saisie_incorrecte.Label(self.fen,
                                                              text=texte['interface']['label']['iteration'] + texte['interface']['label']['error'])
        self.texte_iteration_jarvis.grid(row=2, column=0)

        "Création de la partie dédiée à la méthode de Quickhull"
        self.bp_quickhull = saisie_incorrecte.Button(self.fen,
                                                     text=texte['interface']['bouton']['methode'] +
                                                     'Quickhull',
                                                     bg=parametres_globaux['Quickhull'],
                                                     fg='white',
                                                     command=lambda: self.recherche_enveloppe('Quickhull'))
        self.bp_quickhull.grid(row=0, column=1)

        self.texte_temps_quickhull = saisie_incorrecte.Label(self.fen,
                                                             text=texte['interface']['label']['time']['default'] + texte['interface']['label']['error'])
        self.texte_temps_quickhull.grid(row=1, column=1)

        self.texte_iteration_quickhull = saisie_incorrecte.Label(self.fen,
                                                                 text=texte['interface']['label']['iteration'] + texte['interface']['label']['error'])
        self.texte_iteration_quickhull.grid(row=2, column=1)

        "Création de la partie dédiée à la méthode de Graham"
        self.bp_graham = saisie_incorrecte.Button(self.fen,
                                                  text=texte['interface']['bouton']['methode'] + 'Graham',
                                                  bg=parametres_globaux['Graham'], fg='white', command=lambda: self.recherche_enveloppe('Graham'))
        self.bp_graham.grid(row=0, column=2)

        self.texte_temps_graham = saisie_incorrecte.Label(self.fen,
                                                          text=texte['interface']['label']['time']['default'] + texte['interface']['label']['error'])
        self.texte_temps_graham.grid(row=1, column=2)

        self.texte_iteration_graham = saisie_incorrecte.Label(self.fen,
                                                              text=texte['interface']['label']['iteration'] + texte['interface']['label']['error'])
        self.texte_iteration_graham.grid(row=2, column=2)

        for k in range(3):
            self.fen.columnconfigure(k, minsize=175)    # Les colonnes k auront des dimensions minimale minimale de 175 pixels
        self.fen.rowconfigure(3, minsize=40)

    def next_step_init(self, other, other2, other3):
        self.other_cloud = other
        self.other_option = other2
        self.other_data = other3

        self.bp_plus_de_nuage = saisie_incorrecte.Button(self.fen,
                                                         text=texte['interface']['bouton']["plus de nuage"],
                                                         fg='red',
                                                         command=self.regeneration)
        # sticky s ==> au sud de la case (en bas)
        self.bp_plus_de_nuage.grid(row=3, column=0, sticky='s')

        self.bp_nuage_suivant = saisie_incorrecte.Button(self.fen,
                                                         text=texte['interface']['bouton']["nuage next"], bg='green',
                                                         command=self.other_cloud.changer_nuage,
                                                         fg='white')
        self.bp_nuage_suivant.grid(row=3, column=1, sticky='s')

        self.bp_changement_option = saisie_incorrecte.Button(self.fen,
                                                             text=texte['interface']['bouton']["options"],
                                                             command=self.other_option.fenetre_init)
        self.bp_changement_option.grid(row=3, column=2, sticky='s')

    def recherche_enveloppe(self, methode):
        Chrono = Timer()

        if methode == 'Jarvis':
            Chrono.start()
            polygone, iteration = Jarvis.recherche(self.other_cloud.nuage[:])
            Chrono.stop()
            self.texte_iteration_jarvis.config(text=texte['interface']['label']['iteration']
                                               + str(iteration))
            self.texte_temps_jarvis.config(text=texte['interface']['label']['time']['default']
                                           + Chrono.chrono)

        elif methode == 'Quickhull':
            Chrono.start()
            polygone, iteration = Incremental.recherche(self.other_cloud.nuage[:])
            Chrono.stop()
            self.texte_iteration_quickhull.config(text=texte['interface']['label']['iteration'] + str(iteration))
            self.texte_temps_quickhull.config(text=texte['interface']['label']['time']['default'] + Chrono.chrono)

        else:
            Chrono.start()
            polygone, iteration = Graham.recherche(self.other_cloud.nuage[:])
            Chrono.stop()
            self.texte_iteration_graham.config(text=texte['interface']['label']['iteration'] + str(iteration))
            self.texte_temps_graham.config(text=texte['interface']['label']['time']['default'] + str(Chrono.chrono))

        self.other_cloud.affichage_enveloppe(polygone, methode)

    def regeneration(self, changer_param=False):
        "Fonction permettant de générer un nouveau nuage de points suivant les paramètres données"
        if self.other_data.type == 'random':
            cloud.ecriture(max_point=self.other_data.MAX_POINT, min_point=self.other_data.MIN_POINT,
                           dim_cv=(self.other_data.DIM_CV_X, self.other_data.DIM_CV_Y))
        elif self.other_data.type == 'alignes':
            cloud_al.ecriture(
                dim_cv=(self.other_data.DIM_CV_X, self.other_data.DIM_CV_Y))
        self.other_cloud.liste_nuages = self.other_cloud.other_data.recup()
        self.other_cloud.nuage_n = -1
        if not changer_param:
            self.other_cloud.changer_nuage()


class Nuage():
    "Class dédier à la fenêtre d'affichage"
    def __init__(self, other, other2):
        self.other_data = other
        self.other_error = other2

    def next_step_init(self, other, other2):
        self.other_control = other
        self.other_ihm = other2
        self.start_class()

    def start_class(self):
        def regeneration(type_):
            self.other_data.DIM_CV_X = 500
            self.other_data.DIM_CV_Y = 500
            if type_ == 'classique':
                self.other_data.type = 'random'
                self.other_data.MAX_POINT = 133
                self.other_data.MIN_POINT = 50
                self.other_data.CHEMIN = 'Échantillon de nuages/Fichier nuages de points.cld'
            elif type_ == 'simple':
                self.other_data.type = 'random'
                self.other_data.MAX_POINT = 10
                self.other_data.MIN_POINT = 3
                self.other_data.CHEMIN = 'Échantillon de nuages/Fichier nuages de points.cld'
            elif type_ == 'alignes':
                self.other_data.type = 'alignes'
                self.other_data.CHEMIN = 'Échantillon de nuages/Fichier de nuage de points alignes.cla'

            self.other_ihm.regeneration()
            self.fen.destroy()
            self.start_class()

        try:
            self.liste_nuages = self.other_data.recup()
            self.type = self.other_data.type
        except AttributeError:
            "le type du nuage n'a pas été retenu"
            self.liste_nuages = self.other_error.fichier_corrompu()
            self.type = self.other_data.type

        self.nuage_n = -1   # On commence -1 pour permettre usage du nuage n°0,
                            # l'incrémentation au départ se fait au départ de la fonction
                            # changer nuage.

        self.other_ihm.bp_changement_option.configure(state='normal')   # Les boutons sont actifs
        self.other_ihm.bp_plus_de_nuage.configure(state='normal')
        self.other_ihm.bp_nuage_suivant.configure(state='normal')

        self.fen = saisie_incorrecte.Tk()
        self.fen.title(texte['nuage']['title1'])
        self.fen.resizable(width=False, height=False)
        self.fen.geometry('+600+0')
        self.fen.protocol("WM_DELETE_WINDOW", sys.exit)

        self.cv = saisie_incorrecte.Canvas(self.fen,
                                           width=self.other_data.DIM_CV_X,
                                           height=self.other_data.DIM_CV_Y,
                                           bg=parametres_globaux['Canevas'])
        self.cv.pack()

        "Création d'une petite barre des tâches"
        menu = saisie_incorrecte.Menu(self.fen)
        sous_menu = saisie_incorrecte.Menu(self.fen, tearoff=0)
        sous_sous_menu = saisie_incorrecte.Menu(self.fen, tearoff=0)
        menu.add_cascade(label=texte['nuage']['menu']['title1'], menu=sous_menu)
        sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['ouvrir'],
                              command=self.charger_nuage_particulier)
        sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['new cloud'],
                              command=self.creer_nuage)
        sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['save'],
                              command=self.save_cloud)
        sous_menu.add_cascade(label=texte['nuage']['menu']['sous menu']['cloud tiper'],
                              menu=sous_sous_menu)
        sous_sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['sous sous menu']['classique'],
                                   command=lambda: regeneration('classique'))
        sous_sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['sous sous menu']['alignes'],
                                   command=lambda: regeneration('alignes'))
        sous_sous_menu.add_command(label=texte['nuage']['menu']['sous menu']['sous sous menu']['petit'],
                                   command=lambda: regeneration('simple'))
        menu.add_command(label=texte['nuage']['menu']['title2'], command=self.info)
        # On précise dans quelle fenêtre l'on veut mettre le menu
        self.fen.config(menu=menu)

        self.cv.bind("<Button-1>", Perso.clic_gauche)
        self.cv.bind("<Button-3>", Perso.clic_droit)

        self.changer_nuage()

    def affichage_nuage(self):
        self.cv.delete('all')
        try:
            for Point in self.nuage:
                self.cv.create_text(Point[0], Point[1], text=parametres_globaux['Point_texte'],
                                    fill=parametres_globaux['Point'], tag='Point')
        except IndexError:
            "Un des points n'a qu'une seule coordonnée (x ou y)"
            self.other_error.nuage_corrompu()

    def changer_texte(self):
        "On remet les label à leur valeur par défaut, aucune valeurs nuérique n'est affichée"
        self.other_ihm.texte_temps_jarvis.configure(text=texte['interface']['label']['time']['default']
                                                    + texte['interface']['label']['error'])

        self.other_ihm.texte_iteration_jarvis.configure(text=texte['interface']['label']['iteration']
                                                        + texte['interface']['label']['error'])

        self.other_ihm.texte_temps_quickhull.configure(text=texte['interface']['label']['time']['default']
                                                       + texte['interface']['label']['error'])

        self.other_ihm.texte_iteration_quickhull.configure(text=texte['interface']['label']['iteration']
                                                           + texte['interface']['label']['error'])

        self.other_ihm.texte_temps_graham.configure(text=texte['interface']['label']['time']['default']
                                                    + texte['interface']['label']['error'])

        self.other_ihm.texte_iteration_graham.configure(text=texte['interface']['label']['iteration']
                                                        + texte['interface']['label']['error'])

    def changer_nuage(self):
        self.nuage_n += 1

        if self.nuage_n >= len(self.liste_nuages):
            self.nuage_n = 0

        self.nuage = self.liste_nuages[self.nuage_n][:]
        self.affichage_nuage()
        self.other_control.test_nuage() #Controle de la possibilité de pouvoir trâcer une enveloppe
        self.fen.title(texte['nuage']['title2'] + str(self.nuage_n + 1))
        self.changer_texte()

    def affichage_enveloppe(self, enveloppe, methode):
        self.cv.delete('Polygone')
        self.cv.create_polygon(*enveloppe,
                               fill='',
                               outline=parametres_globaux[methode],
                               tag=('Polygone', methode),
                               width=parametres_globaux['Epaisseur trait'])

    def charger_nuage_particulier(self):
        "Fonction permettant de charger un fichier texte contenant un nuage de points"
        file = tkf.askopenfilename(filetypes=[('cloud', '*.cld'), ('personnel', '*.clp'),
                                              ('alignes', '*.cla'), ('All File', '*.*')],
                                              title=texte['nuage']['dialogue title']['open'])
        if file != '':
            self.other_data.CHEMIN = file
            self.other_data.recup()
            self.other_error.erreur_enveloppe_old = False
            self.fen.destroy()
            self.start_class()
            self.changer_texte()

    def creer_nuage(self):
        "Fonction permmettant de créer son propre nuage de points à partit d'un canvas vide"
        self.cv.delete('all')
        self.cv.bind("<Button-1>", Perso.clic_gauche)
        self.cv.bind("<Button-3>", Perso.clic_droit)
        self.fen.title(texte['nuage']['title3'])
        self.other_ihm.bp_plus_de_nuage.configure(state='disabled')
        self.other_ihm.bp_nuage_suivant.configure(state='disabled')
        self.other_error.reactivation_bp_enveloppe()
        self.liste_nuages = self.nuage = []
        self.changer_texte()

    def save_cloud(self):
        "Fonction permmettant de sauvegarder un nuage de points de notre choix"
        liste_points = []
        id_all = self.cv.find_all()
        if len(id_all) >= 1:
            for item in id_all:
                liste_points.append(self.cv.coords(item))
            file = tkf.asksaveasfile(filetype=[('personnel', '*.clp')],\
                 defaultextension='.clp', title=texte['nuage']['dialogue title']['save'])
            if file != '' and file != None:
                DIM_CV = (self.other_data.DIM_CV_X, self.other_data.DIM_CV_Y)
                js.dump((liste_points, (DIM_CV, 'personnel')), file)
        else:
            self.other_error.saisie_incorrecte()

    def info(self):
        "Fonction affichant du texte dans le le canvas"
        if self.other_data.DIM_CV_X != 500 or self.other_data.DIM_CV_Y != 500:
            self.other_data.DIM_CV_X = 500
            self.other_data.DIM_CV_Y = 500
            self.other_ihm.regeneration(changer_param=True) # De nouveau nuage sont généré,
                                                            # un appuie sur le bouton suivant affiche un nuage
            self.fen.destroy()
            self.start_class()
        self.cv.delete('all')
        self.fen.title(texte['nuage']['title4'])
        self.other_ihm.bp_graham.config(state='disabled')
        self.other_ihm.bp_jarvis.config(state='disabled')
        self.other_ihm.bp_quickhull.config(state='disabled')
        self.other_control.erreur_enveloppe_old = True
        self.cv.create_text(self.other_data.DIM_CV_X/2, self.other_data.DIM_CV_Y/2,
                            text=texte['nuage']['texte info'], font=('Arial', 11))
        self.changer_texte()


class Control_data():
    "Class dédiée à la vérification de la possibilité de tracer une enveloppe convexe"
    def __init__(self, other, other2):
        self.other_cloud = other
        self.other_error = other2
        self.erreur_enveloppe_old = False

    def test_nuage(self):
        def verification_alignement(nuage):
            def alignement(A, B, C):
                "Calcul d'un produit vectoriel"
                d = (B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])
                if d == 0:
                    return True
                else:
                    return False

            A = nuage[0]
            B = nuage[1]
            error = 2
            for point in nuage[2:]:
                #Commence à la 3ème valeur de nuage
                if alignement(A, B, point):
                    #Si les points sont alignés => +1 erreur
                    error += 1
                    if error == len(nuage):
                        #Si tous les points sont alignés, on ne peut pas tracer d'enveloppe
                        return True
                else:
                    return False

        if self.other_cloud.type == 'random' or self.other_cloud.type == 'personnel':
            nuage = self.other_cloud.nuage
            if type(nuage[0]) == int:
                nuage = self.other_cloud.nuage = self.other_cloud.liste_nuages

            if len(nuage) >= 3:
                test_alignement = verification_alignement(nuage)
                if test_alignement:
                    "Les points sont alignés - on ne peut pas tracer d'enveloppe - on désactive les boutons"
                    self.other_error.desactivation_bp_enveloppe(repetition=self.erreur_enveloppe_old)
                    self.erreur_enveloppe_old = True
                elif self.erreur_enveloppe_old:
                    "Le nuage précédent à nécessité la désactivation des boutons, on les réactive"
                    self.other_error.reactivation_bp_enveloppe()
                    self.erreur_enveloppe_old = False

            else:
                self.other_error.desactivation_bp_enveloppe(repetition=self.erreur_enveloppe_old)
                self.erreur_enveloppe_old = True

            if self.other_cloud.type == 'personnel':
                self.other_cloud.other_ihm.bp_plus_de_nuage.configure(state='disabled')
                self.other_cloud.other_ihm.bp_nuage_suivant.configure(state='disabled')

        elif self.other_cloud.type == 'alignes' :
            '''Le nuages est forcément aligner, donc l'enveloppe convexe ne peut être tracé,
            on désactive automatiquement les boutons'''
            self.other_error.desactivation_bp_enveloppe(repetition=self.erreur_enveloppe_old)
            self.erreur_enveloppe_old = True
            self.other_cloud.cv.unbind("<Button-3>")    #Désactivation des interaction entre le canvas et la touche
            self.other_cloud.cv.unbind( "<Button-1>")


class Erreur():
    "Class regroupant les différents messages d'erreurs possible et les actions à faire en conséquence"
    def __init__(self, other, other2):
        self.other_ihm = other
        self.other_data = other2

    def next_step_init(self, other):
        self.other_cloud = other

    def fichier_corrompu(self):
        "Fonction dans le cas où le fichier n'est pas visible on essaye de la corriger"

        reponse = tkm.askquestion(texte['dialogue']['error file']['title'],
                                  texte['dialogue']['error file']['texte'], icon='error', default='yes')
        if reponse == 'yes':
            if self.other_data.CHEMIN[-1] == 'd':  # On regarde quel type de nuage est concerné,
                                                   # grâce à son extension
                cloud.ecriture()    # Réécriture du fichier
            elif self.other_data.CHEMIN[-1] == 'a':
                cloud_al.ecriture()

            elif self.other_data.CHEMIN[-1] == 'p':
                return []   # Le fichier est fichier créer par l'utilisateur, on ne peut pas le réecrire.
                            # Il doit en créer un autre.

            return self.other_data.recup()
        else:
            tkm.showinfo(texte['dialogue']['close']['title'], texte['dialogue']['close']['texte'])
            sys.exit()

    def desactivation_bp_enveloppe(self, repetition=False):
        if repetition == False:
            tkm.showinfo(texte['dialogue']['error alignes']['title'],
                         texte['dialogue']['error alignes']['texte'], icon='warning')

            self.other_ihm.bp_graham.config(state='disabled')
            self.other_ihm.bp_jarvis.config(state='disabled')
            self.other_ihm.bp_quickhull.config(state='disabled')

    def reactivation_bp_enveloppe(self):
        self.other_ihm.bp_graham.config(state='normal')
        self.other_ihm.bp_jarvis.config(state='normal')
        self.other_ihm.bp_quickhull.config(state='normal')

    def saisie_incorrecte(self):
        tkm.showerror(texte['dialogue']['error saisie']['title'], texte['dialogue']['error saisie']['texte'])

    def modification_saisie(self):
        tkm.showinfo(texte['dialogue']['error value']['title'], texte['dialogue']['error value']['texte'])

    def clic_trop_pret(self):
        "Une phrase apparaît dans le canvas"
        self.other_cloud.cv.create_text(self.other_data.DIM_CV_X/2, self.other_data.DIM_CV_Y-25,
                                        text=texte['nuage']['error clic'], fill='black', tag='Error_clic')

    def couleur_indisponible(self):
        tkm.showinfo(texte['dialogue']['error color']['title'],
                     texte['dialogue']['error color']['texte'], icon='warning')

    def nuage_corrompu(self):
        reponse = tkm.askquestion(texte['dialogue']['error cloud']['title'],\
             texte['dialogue']['error cloud']['texte'],icon='error', default='no')

        if reponse == 'yes':
            cloud.ecriture()
            "on réécrit le fichier sans corruption"
            self.other_cloud.liste_nuages = self.other_data.recup()
            self.other_cloud.nuage_n = -1
            self.other_cloud.changer_nuage()
        else:
            del self.other_cloud.liste_nuages[self.other_cloud.nuage_n]
            self.other_cloud.nuage_n -= 1
            self.other_cloud.changer_nuage()


class Option():
    def __init__(self, other1, other2, other3, other4):
        self.other_ihm = other1
        self.other_cloud = other2
        self.other_error = other3
        self.other_data = other4
        self.corruption = False
        self.changement_forme_point = False
        self.changement_epaisseur_trait = False
        self.changement_couleur_cv = False
        self.changement_couleur_point = False

    def fenetre_init(self):
        self.other_ihm.bp_changement_option.config(state='disabled')  # Désactive le bouton changer paramètres
                                                                      # pour ne pas pouvoir gérer plein de fenêtres

        self.fen = saisie_incorrecte.Tk()
        self.fen.title(texte['option']['title'])
        self.fen.resizable(width=False, height=False)
        self.fen.geometry('+150+150')
        self.fen.protocol("WM_DELETE_WINDOW", self.fermeture_fenetre)

        self.dict_option = parametres_globaux.copy()

        frame_top = saisie_incorrecte.Frame(self.fen)
        frame_top.pack(side='top')

        frame_top.columnconfigure(0, minsize=50)
        frame_top.columnconfigure(1, minsize=50)

        frame_bottom = saisie_incorrecte.Frame(self.fen)
        frame_bottom.pack(side='bottom', fill='x')

        self.bp_valider = saisie_incorrecte.Button(frame_bottom,\
             text=texte['option']['bouton']['valider'], bg='green', fg='white', command=self.validation)
        self.bp_valider.pack(side='left')

        if self.other_cloud.type == 'random':
            saisie_incorrecte.Label(frame_top, text=texte['option']['label']['min']).grid(row=0, column=0, sticky='w')
            saisie_incorrecte.Label(frame_top, text=texte['option']['label']['max']).grid(row=1, column=0, sticky='w')
            saisie_incorrecte.Label(frame_top, text=texte['option']['label']['largeur']).grid(row=2, column=0, sticky='w')
            saisie_incorrecte.Label(frame_top, text=texte['option']['label']['longueur']).grid(row=3, column=0, sticky='w')

            self.rep_min = saisie_incorrecte.Entry(frame_top, width=5)
            self.rep_min.grid(row=0, column=2, sticky='e')

            self.rep_max = saisie_incorrecte.Entry(frame_top, width=5)
            self.rep_max.grid(row=1, column=2, sticky='e', pady=2)

            self.rep_cv_x = saisie_incorrecte.Entry(frame_top, width=5)
            self.rep_cv_x.grid(row=2, column=2, sticky='e')

            self.rep_cv_y = saisie_incorrecte.Entry(frame_top, width=5)
            self.rep_cv_y.grid(row=3, column=2, sticky='e', pady=2)

            self.bp_changer_couleur = saisie_incorrecte.Button(frame_bottom, text=texte['option']['bouton']['changer param'],\
                command=self.option_plus, bg='orange', fg='white')
            self.bp_changer_couleur.pack(side='right')
        else:
            self.option_plus()

    def fermeture_fenetre(self):
            self.other_ihm.bp_changement_option.config(state='normal')
            self.fen.destroy()

    def changement_dim_cv_fct(self):
        if self.rep_cv_x_ != '':
            self.other_data.DIM_CV_X = max(150, min(1000, self.rep_cv_x_))

        if self.rep_cv_y_ != '':
            self.other_data.DIM_CV_Y = max(150, min(1000, self.rep_cv_y_))

        self.other_data.MARGE_POINT_X = int(min(20, 0.05*self.other_data.DIM_CV_X))
        self.other_data.MARGE_POINT_Y = int(min(20, 0.05*self.other_data.DIM_CV_Y))

        self.max_point = self.other_data.max_point()  # Recalcule du nombres de points max, la taille du
                                                      # ayant changé

        self.changement_nuage_fct(changement_cv=True)

    def changement_couleur_methode_fct(self):
        def changement_enveloppe(methode):
            self.other_cloud.cv.itemconfig('Polygone', outline=parametres_globaux[methode])

        tuple_ = ('Jarvis', 'Quickhull', 'Graham')

        for widget in self.other_ihm.fen.winfo_children():
            texte_widget = widget.cget('text')[11:]  #On récupère que la partie contenant
                                                     #le nom de la méthode au bouton associer
            if texte_widget in tuple_:
                if widget.cget('bg') != parametres_globaux[texte_widget]:
                    widget.config(bg=parametres_globaux[texte_widget])

        tags = self.other_cloud.cv.itemcget('Polygone', 'tag')
        if tags != ():
            tags = tags.replace('Polygone ', '')  # Les tags sont sauvegardés dans une seule et même chaine de caractéres
                                                  # On enléve alors Polygone de cette phrase pour garder que la partie
                                                  # contenant la méthode
            changement_enveloppe(tags)

    def changement_nuage_fct(self, changement_cv=False):
        if self.rep_max_ != '' and self.rep_min_ != '':
            if self.rep_max_ < self.rep_min_:
                self.rep_max_, self.rep_min_ = self.rep_min_, self.rep_max_

        if self.rep_max_ != '':
            self.other_data.MAX_POINT = min(self.max_point, self.rep_max_)

        if self.rep_min_ != '':
            self.other_data.MIN_POINT = min(self.other_data.MAX_POINT, max(3, self.rep_min_))

        self.other_ihm.regeneration(changer_param=changement_cv)

        if changement_cv:
            self.other_cloud.fen.destroy()
            self.other_cloud.start_class()

        if (self.rep_max_ != self.other_data.MAX_POINT and self.rep_max_ != '') \
                or (self.rep_min_ != self.other_data.MIN_POINT and self.rep_min_ != '') \
                or (self.rep_cv_x_ != self.other_data.DIM_CV_X and self.rep_cv_x_ != '') \
                or (self.rep_cv_y_ != self.other_data.DIM_CV_Y and self.rep_cv_y_ != ''):
            '''Dans le cas où l'une des valeurs d'entrées est différentes de celles de sortie,
             on en prévient l'utilisateur'''
            self.other_error.modification_saisie()

    def option_plus(self):
        "Fonction dédier aux paramètres tel que la couleur"
        def saisie_incorrecte(sujet):
            def couleur_dispo(test, color):
                tuple_color_pris = self.dict_option.values()
                if test != 'Canevas' and color != '#ffffff':
                        return color not in tuple_color_pris
                elif test == 'Canevas':
                    return color[1] not in tuple_color_pris #Seul le canevas peut etre de couleur blanche
                else:
                    return False

            couleur = tkc.askcolor(parametres_globaux[sujet], title=texte['dialogue']['color'] + sujet)
            if couleur != (None, None):
                # On bloque la couleur noire, on ne peut pas l'attribuer à un élement
                if couleur[1] != '#000000':
                    if couleur_dispo(sujet, couleur[1]):
                        for widget in self.cv.winfo_children():
                            if widget.cget('bg') == self.dict_option[sujet] and sujet in widget.cget('text'):
                                widget.config(bg=couleur[1])
                                break

                        self.dict_option[sujet] = couleur[1]
                        if sujet == 'Canevas':
                            self.changement_couleur_cv = True
                        elif sujet == 'Point':
                            self.changement_couleur_point = True
                        else:
                            self.corruption = True
                    else:
                        self.other_error.couleur_indisponible()
                else:
                    self.other_error.couleur_indisponible()

        def recup_forme_point():
            global parametres_globaux
            try:
                rep = tks.askstring(texte['dialogue']['point']['title'],
                                    texte['dialogue']['point']['texte'] + parametres_globaux['Point_texte'])
                if len(rep) == 1:
                    if rep != self.dict_option['Point_texte']:
                        self.dict_option['Point_texte'] = rep
                        self.changement_forme_point = True
                elif rep != '':
                    self.other_error.saisie_incorrecte()
                    recup_forme_point()
            except TypeError:
                pass

        def recup_trait():
                try:
                    rep = tks.askstring(texte['dialogue']['epaisseur']['title'],
                                        texte['dialogue']['epaisseur']['texte'] + str(parametres_globaux['Epaisseur trait']))

                    if rep != '':
                        rep = int(rep)
                        rep = min(rep, 6)
                        rep = max(1, rep)
                        if rep != parametres_globaux['Epaisseur trait']:
                            parametres_globaux['Epaisseur trait'] = rep
                            self.changement_epaisseur_trait = True

                except ValueError:
                    self.other_error.saisie_incorrecte()
                    recup_trait()

                except TypeError:
                    pass

        if self.other_cloud.type == 'random':
            self.bp_changer_couleur.destroy()
        self.bp_valider.forget()
        self.bp_valider.pack(pady=5)
        self.cv = saisie_incorrecte.Canvas(self.fen)
        self.cv.pack(pady=5)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['color'] + 'Jarvis', bg=parametres_globaux['Jarvis'],
                                 command=lambda: saisie_incorrecte('Jarvis')).grid(row=0, column=0, pady=5)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['color'] + 'Graham', bg=parametres_globaux['Graham'],
                                 command=lambda: saisie_incorrecte('Graham')).grid(row=0, column=1)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['color'] + 'Quickhull', bg=parametres_globaux['Quickhull'],
                                 command=lambda: saisie_incorrecte('Quickhull')).grid(row=1, column=0)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['color'] + 'Point', bg=parametres_globaux['Point'],
                                 command=lambda: saisie_incorrecte('Point')).grid(row=1, column=1)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['color'] + 'Canevas', bg=parametres_globaux['Canevas'],
                                 command=lambda: saisie_incorrecte('Canevas')).grid(row=2, column=0, pady=5)

        saisie_incorrecte.Button(self.cv, text=texte['option']['bouton']['forme'],
                                 command=recup_forme_point).grid(row=2, column=1, pady=5)

        saisie_incorrecte.Button(
            self.cv, text=texte['option']['bouton']['epaisseur'], command=recup_trait).grid(row=3, column=0)

    def validation(self):
        global parametres_globaux
        try:
            self.rep_min_ = self.rep_min.get()
            self.rep_max_ = self.rep_max.get()
            self.rep_cv_x_ = self.rep_cv_x.get()
            self.rep_cv_y_ = self.rep_cv_y.get()
            if self.rep_cv_x_ != '':
                self.rep_cv_x_ = int(self.rep_cv_x_)

            if self.rep_cv_y_ != '':
                self.rep_cv_y_ = int(self.rep_cv_y_)

            if self.rep_min_ != '':
                self.rep_min_ = int(self.rep_min_)

            if self.rep_max_ != '':
                self.rep_max_ = int(self.rep_max_)

        except ValueError:
            self.other_error.saisie_incorrecte()

        else:  # Ce qui suit ne s'exécute que dans le cas où aucune exception n'a été levé
            self.fermeture_fenetre()

            if self.rep_cv_x_ != '' or self.rep_cv_y_ != '':
                self.changement_dim_cv_fct()

            elif self.rep_max_ != '' or self.rep_min_ != '':
                self.max_point = self.other_data.max_point()
                self.changement_nuage_fct()

            parametres_globaux = self.dict_option.copy()

            if self.corruption:
                self.changement_couleur_methode_fct()
                self.corruption = False

            if self.changement_couleur_cv:
                self.other_cloud.cv.configure(bg=parametres_globaux['Canevas'])
                self.changement_couleur_cv = False

            if self.changement_forme_point:
                self.other_cloud.cv.itemconfig(
                    'Point', text=parametres_globaux['Point_texte'])
                self.changement_forme_point = False

            if self.changement_couleur_point:
                self.other_cloud.cv.itemconfig(
                    'Point', fill=parametres_globaux['Point'])

            if self.changement_epaisseur_trait:
                self.other_cloud.cv.itemconfig(
                    'Polygone', width=parametres_globaux['Epaisseur trait'])

    def clic_gauche(self, event):
        self.other_cloud.cv.delete('Error_clic')

        Id = self.other_cloud.cv.find_overlapping(event.x - self.other_data.MARGE_POINT_X/2, event.y - self.other_data.MARGE_POINT_Y/2,
                                                  event.x + self.other_data.MARGE_POINT_X/2, event.y + self.other_data.MARGE_POINT_Y/2)

        autre_point = False

        if Id != ():
            for i in Id:
                if 'Point' in self.other_cloud.cv.itemcget(i, 'tag'):
                    self.other_error.clic_trop_pret()
                    autre_point = True
                    break

        if autre_point == False:
            self.other_cloud.cv.create_text(event.x, event.y, text=parametres_globaux['Point_texte'],
                                            fill=parametres_globaux['Point'], tag='Point')
            self.other_cloud.nuage.append([event.x, event.y])
            self.redessinage_enveloppe()

    def clic_droit(self, event):
        Id = self.other_cloud.cv.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)

        if Id != ():
            for i in Id:
                tags = self.other_cloud.cv.itemcget(i, 'tag')
                if 'Point' in tags:
                    if 'Point_effacer' not in tags:
                        self.other_cloud.nuage.remove(
                            self.other_cloud.cv.coords(i))
                        self.other_cloud.cv.itemconfig(i, fill='black')
                        self.other_cloud.cv.addtag_withtag('Point_effacer', i)
                    else:
                        self.other_cloud.nuage.append(
                            self.other_cloud.cv.coords(i))
                        self.other_cloud.cv.itemconfig(
                            i, fill=parametres_globaux['Point'])
                        self.other_cloud.cv.dtag(i, 'Point_effacer')

                    self.redessinage_enveloppe()

    def redessinage_enveloppe(self):
        tags = self.other_cloud.cv.itemcget('Polygone', 'tag')
        if tags != ():
            if 'Jarvis' in tags:
                self.other_ihm.recherche_enveloppe('Jarvis')
            elif 'Quickhull' in tags:
                self.other_ihm.recherche_enveloppe('Quickhull')
            elif 'Graham' in tags:
                self.other_ihm.recherche_enveloppe('Graham')


###############################################____Mainloop____########################################################


if __name__ == "__main__":
    try:
        "Récuperation de tout les textes de l'interface"
        with open ('./App/Texte.int', 'r', encoding='utf-8') as file:
            texte = js.load(file)
    except:
        tkm.showerror("Erreur fichier texte", "Le fichier contenant tout les textes du programme" \
            + "est introuvable, le programme ne peut pas s'exécuter. Veuillez bien vérifier leur chemin d'accées")
        sys.exit()

    Ihm = Interface()
    Data = Recup_data()
    Error = Erreur(Ihm, Data)
    Data.next_step_init(Error)
    Cloud = Nuage(Data, Error)

    Error.next_step_init(Cloud)

    Watchdog = Control_data(Cloud, Error)
    Perso = Option(Ihm, Cloud, Error, Data)

    Ihm.next_step_init(Cloud, Perso, Data)
    Cloud.next_step_init(Watchdog, Ihm)

    Ihm.fen.mainloop()
    Cloud.fen.mainloop()
