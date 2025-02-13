from abc import ABC, abstractmethod
#le module abc permet la creation des classes abstraites
import json
#pour sauvegarder dans un fichier
import os
import tkinter as tk
#pour l'interface graphique
from tkinter import ttk
#pour le menu, les widgets


class Document(ABC):
    # le document a les memes attributs que le livre donc il s'agit de l'heritage où Document est la classe mere
    #@abstractmethod permet de definir les methodes comme abstraites
    @abstractmethod
    def __init__(self, titre, auteur, annee, genre):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        # ici on definit les attributs

    @abstractmethod
    def afficher_details(self):
        pass

class Livre(Document):
    # la classe livre herite de la classe Document,
    # et grace a super, qui est la premiere instruction du constructeur,
    # utilise les attributs de document
    def __init__(self, titre, auteur, annee, genre):
        super().__init__(titre, auteur, annee, genre)

    def afficher_details(self):
        #pour afficher
        return f"{self.titre} - {self.auteur} ({self.annee}) - {self.genre}"


class Bibliotheque:
    #la classe ci  gère la collection de livres avec json

    def __init__(self, fichier="bibliotheque.json"):
        # on veut sauvegarder dans un fichier
        self.fichier = fichier
        self.livres = []
        self.charger_livres()

    def ajouter_livre(self, titre, auteur, annee, genre):
        #Ajoute un livre à la bibliothèque
        livre = Livre(titre, auteur, annee, genre)
        self.livres.append(livre)
        self.sauvegarder_livres()

    def supprimer_livre(self, titre):
        #Supprime un livre par son titre
        self.livres = [livre for livre in self.livres if livre.titre != titre]
        self.sauvegarder_livres()

    def rechercher_livre(self, terme):
        #Recherche un livre par titre ou auteur
        terme = terme.lower()  # Convertir la recherche en minuscule
        resultats = [
            livre.afficher_details() for livre in self.livres
            if livre.titre and livre.auteur and
               terme in livre.titre.lower() or terme in livre.auteur.lower()
        ]
        return resultats

    def afficher_livres(self):
        #Afficher la liste des livres
        return [livre.afficher_details() for livre in self.livres]

    def modifier_livre(self, ancien_titre, nouveau_titre, auteur, annee, genre):
        #Modifie un livre
        for livre in self.livres:
            if livre.titre == ancien_titre:
                livre.titre = nouveau_titre
                livre.auteur = auteur
                livre.annee = annee
                livre.genre = genre
                self.sauvegarder_livres()
                return True
        return False

    def sauvegarder_livres(self):
        #Sauvegarde les livres en JSON.
        # pour pouvoir ecrire dans le livre
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump([vars(livre) for livre in self.livres], f, indent=4)

    def charger_livres(self):
        #Charge les livres depuis un fichier JSON
        # pour pouvoir lire  le livre
        if os.path.exists(self.fichier):
            with open(self.fichier, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.livres = [Livre(**livre) for livre in data]
                except json.JSONDecodeError:
                    self.livres = []



class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Bibliothèque")
        self.bibliotheque = Bibliotheque()

        # Création du Notebook (Onglets)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Onglets
        self.onglet_ajout = ttk.Frame(self.notebook)
        self.onglet_supprimer = ttk.Frame(self.notebook)
        self.onglet_recherche = ttk.Frame(self.notebook)
        self.onglet_affichage = ttk.Frame(self.notebook)
        self.onglet_modification = ttk.Frame(self.notebook)

        # Ajout des onglets
        self.notebook.add(self.onglet_ajout, text="Ajouter un Livre")
        self.notebook.add(self.onglet_supprimer, text="Supprimer un Livre")
        self.notebook.add(self.onglet_recherche, text="Rechercher un Livre")
        self.notebook.add(self.onglet_affichage, text="Afficher la Bibliothèque")
        self.notebook.add(self.onglet_modification, text="Modifier un Livre")

        # Création des formulaires pour chaque onglet
        self.creer_formulaire_ajout()
        self.creer_formulaire_suppression()
        self.creer_formulaire_recherche()
        self.creer_formulaire_affichage()
        self.creer_formulaire_modification()

    def creer_formulaire_ajout(self):
        #formulaire d'ajout
        ttk.Label(self.onglet_ajout, text="Titre :").pack()
        self.entry_titre = ttk.Entry(self.onglet_ajout)
        self.entry_titre.pack()

        ttk.Label(self.onglet_ajout, text="Auteur :").pack()
        self.entry_auteur = ttk.Entry(self.onglet_ajout)
        self.entry_auteur.pack()

        ttk.Label(self.onglet_ajout, text="Année :").pack()
        self.entry_annee = ttk.Entry(self.onglet_ajout)
        self.entry_annee.pack()

        ttk.Label(self.onglet_ajout, text="Genre :").pack()
        self.entry_genre = ttk.Entry(self.onglet_ajout)
        self.entry_genre.pack()

        #bouton faisant appel a la fonction d'ajout
        ttk.Button(self.onglet_ajout, text="Ajouter", command=self.ajouter_livre).pack()

    def ajouter_livre(self):
       #methode pour ajouter ou sauvegarder un livre dans un fichier json.
       # on recupere tous les champs
        titre = self.entry_titre.get()
        auteur = self.entry_auteur.get()
        annee = self.entry_annee.get()
        genre = self.entry_genre.get()
        if titre and auteur and annee and genre:
            self.bibliotheque.ajouter_livre(titre, auteur, annee, genre)
            self.entry_titre.delete(0, tk.END)
            self.entry_auteur.delete(0, tk.END)
            self.entry_annee.delete(0, tk.END)
            self.entry_genre.delete(0, tk.END)

    def creer_formulaire_suppression(self):
        #methode qui permet de selectionner le livre a supprimer grace a son titre
        ttk.Label(self.onglet_supprimer, text="Titre du Livre à supprimer :").pack()
        self.entry_suppression = ttk.Entry(self.onglet_supprimer)
        self.entry_suppression.pack()
        ttk.Button(self.onglet_supprimer, text="Supprimer", command=self.supprimer_livre).pack()

    def supprimer_livre(self):
        #permet de supprimer un livre du fichier et de la liste
        titre = self.entry_suppression.get()
        self.bibliotheque.supprimer_livre(titre)
        self.entry_suppression.delete(0, tk.END)

    def creer_formulaire_affichage(self):
        #zone d'affichage des livres
        self.liste_livres = tk.Text(self.onglet_affichage, height=15, width=50)
        self.liste_livres.pack()
        #bouton permettant de charger a partir d'un fichier json les livres sauvegardés
        ttk.Button(self.onglet_affichage, text="Actualiser", command=self.afficher_livres).pack()

    def afficher_livres(self):
        #pour afficher la liste des livres contenues dans le fichier json
        self.liste_livres.delete("1.0", tk.END)
        livres = self.bibliotheque.afficher_livres()
        for livre in livres:
            self.liste_livres.insert(tk.END, livre + "\n")

    def creer_formulaire_recherche(self):
        #petit formulzire de recherche d'un livre grace au titre ou au nom d'auteu
        ttk.Label(self.onglet_recherche, text="Rechercher par Titre ou Auteur :").pack()
        self.entry_recherche = ttk.Entry(self.onglet_recherche)
        self.entry_recherche.pack()
        ttk.Button(self.onglet_recherche, text="Rechercher", command=self.rechercher_livre).pack()

        self.resultats_recherche = tk.Text(self.onglet_recherche, height=10, width=50)
        self.resultats_recherche.pack()

    def rechercher_livre(self):
        """Recherche un livre"""
        terme = self.entry_recherche.get()
        self.resultats_recherche.delete("1.0", tk.END)

        #gestion des erreurs
        if terme:
            resultats = self.bibliotheque.rechercher_livre(terme)
            if resultats:
                for livre in resultats:
                    self.resultats_recherche.insert(tk.END, livre.afficher_details() + "\n")
            else:
                self.resultats_recherche.insert(tk.END, "Aucun résultat trouvé.")
        else:
            self.resultats_recherche.insert(tk.END, "Veuillez entrer un titre ou un auteur.")

    def creer_formulaire_modification(self):
        #formulaire pour la modification des champs avec recuperation et sauvegarde des donnees
        ttk.Label(self.onglet_modification, text="Titre du Livre à Modifier :").pack()
        self.entry_ancien_titre = ttk.Entry(self.onglet_modification)
        self.entry_ancien_titre.pack()

        ttk.Label(self.onglet_modification, text="Nouveau Titre :").pack()
        self.entry_nouveau_titre = ttk.Entry(self.onglet_modification)
        self.entry_nouveau_titre.pack()

        ttk.Label(self.onglet_modification, text="Nouvel Auteur :").pack()
        self.entry_nouvel_auteur = ttk.Entry(self.onglet_modification)
        self.entry_nouvel_auteur.pack()

        ttk.Label(self.onglet_modification, text="Nouvelle Année :").pack()
        self.entry_nouvelle_annee = ttk.Entry(self.onglet_modification)
        self.entry_nouvelle_annee.pack()

        ttk.Label(self.onglet_modification, text="Nouveau Genre :").pack()
        self.entry_nouveau_genre = ttk.Entry(self.onglet_modification)
        self.entry_nouveau_genre.pack()

        ttk.Button(self.onglet_modification, text="Modifier", command=self.modifier_livre).pack()
        self.label_modification = ttk.Label(self.onglet_modification, text="")
        self.label_modification.pack()

    def modifier_livre(self):
        #methode pour modifier les champs du livre
        ancien_titre = self.entry_ancien_titre.get()
        nouveau_titre = self.entry_nouveau_titre.get()
        auteur = self.entry_nouvel_auteur.get()
        annee = self.entry_nouvelle_annee.get()
        genre = self.entry_nouveau_genre.get()

        #gestion des exceptions,
        # il faut modifier ou remplir tous les champs si le livre sollicité existe.
        # un message est affiché s'il y a probleme en rouge et si tout est bien en vert
        if ancien_titre and nouveau_titre and auteur and annee and genre:
            if self.bibliotheque.modifier_livre(ancien_titre, nouveau_titre, auteur, annee, genre):
                self.label_modification.config(text="Livre modifié avec succès !", foreground="green")
            else:
                self.label_modification.config(text="Livre introuvable.", foreground="red")
        else:
            self.label_modification.config(text="Tous les champs doivent être remplis.", foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
