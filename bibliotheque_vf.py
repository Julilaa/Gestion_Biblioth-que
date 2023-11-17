from datetime import datetime
from tkinter import *
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.orm import joinedload

# Déclaration de la BDD

Base = declarative_base()

# Mise en forme de la BDD

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    categorie = Column(String)
    emprunts = relationship("Emprunt", back_populates="utilisateur")

class Livre(Base):
    __tablename__ = 'livres'

    id = Column(Integer, primary_key=True)
    titre = Column(String)
    auteur = Column(String)
    genre = Column(String)
    isbn = Column(String, unique=True)
    emprunts = relationship("Emprunt", back_populates="livre")

class Emprunt(Base):
    __tablename__ = 'emprunts'

    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))
    livre_id = Column(Integer, ForeignKey('livres.id'))
    date_emprunt = Column(DateTime)
    date_retour = Column(DateTime)

    utilisateur = relationship("Utilisateur", back_populates="emprunts")
    livre = relationship("Livre", back_populates="emprunts")

# Création du fichier de la BDD

engine = create_engine('sqlite:///bibliothequee_vf.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Catégorie des Livres :

def gestion_livres():
    # Ajouter un bouton "Gestion Livres"
    gestion_livre_button = Button(fenetre, text="Gestion Livres", command=gestion_livres)
    gestion_livre_button.grid(row=0, column=0)

    # Supprimer le bouton "Gestion Livres" existant
    gestion_livre_button.grid_forget()

    fenetre_livre = Toplevel(fenetre)
    fenetre_livre.title("Gestion des Livres")

    # Définir une taille pour la fenêtre
    fenetre_livre.geometry("600x400")  

    # Configurer la largeur des colonnes
    fenetre_livre.columnconfigure(0, weight=1)
    fenetre_livre.columnconfigure(1, weight=1)
    fenetre_livre.columnconfigure(2, weight=1)
    fenetre_livre.columnconfigure(3, weight=1)

    # Configurer la hauteur des lignes
    fenetre_livre.rowconfigure(0, weight=1)
    fenetre_livre.rowconfigure(1, weight=1)
    fenetre_livre.rowconfigure(2, weight=1)
    fenetre_livre.rowconfigure(3, weight=1)
    fenetre_livre.rowconfigure(4, weight=1)
    fenetre_livre.rowconfigure(5, weight=1)

    # Créer les boutons pour ajouter, supprimer et modifier les livres
    ajouter_livre_button = Button(fenetre_livre, text="Ajouter Livre", command=ajouter_livre, width=20, height=5, bg='green', fg='white')
    ajouter_livre_button.grid(row=1, column=1, pady=10, sticky="nsew")

    supprimer_livre_button = Button(fenetre_livre, text="Supprimer Livre", command=supprimer_livre, width=20, height=5, bg='red', fg='white')
    supprimer_livre_button.grid(row=2, column=1, pady=10, sticky="nsew")

    modifier_livre_button = Button(fenetre_livre, text="Modifier Livre", command=modifier_livre, width=20, height=5, bg='orange', fg='white')
    modifier_livre_button.grid(row=3, column=1, pady=10, sticky="nsew")

    afficher_livres_button = Button(fenetre_livre, text="Afficher Livres", command=afficher_livres, width=20, height=5, bg='blue', fg='white')
    afficher_livres_button.grid(row=4, column=1, pady=10, sticky="nsew")

    rechercher_livre_button = Button(fenetre_livre, text="Rechercher Livre", command=rechercher_livre, width=20, height=5, bg='purple', fg='white')
    rechercher_livre_button.grid(row=5, column=1, pady=10, sticky="nsew")



# Fonction pour ajouter des livres

def ajouter_livre():
    fenetre_livre = Toplevel(fenetre)
    fenetre_livre.title("Ajouter Livre")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_livre, padx=10, pady=10)
    frame.grid(row=0, column=0)

    titre_label = Label(frame, text="Titre:")
    titre_label.grid(row=0, column=0, pady=5)
    titre_entry = Entry(frame)
    titre_entry.grid(row=0, column=1, pady=5)

    auteur_label = Label(frame, text="Auteur:")
    auteur_label.grid(row=1, column=0, pady=5)
    auteur_entry = Entry(frame)
    auteur_entry.grid(row=1, column=1, pady=5)

    genre_label = Label(frame, text="Genre:")
    genre_label.grid(row=2, column=0, pady=5)
    genre_entry = Entry(frame)
    genre_entry.grid(row=2, column=1, pady=5)

    isbn_label = Label(frame, text="ISBN:")
    isbn_label.grid(row=3, column=0, pady=5)
    isbn_entry = Entry(frame)
    isbn_entry.grid(row=3, column=1, pady=5)

    def valider_ajout_livre():
        titre = titre_entry.get()
        auteur = auteur_entry.get()
        genre = genre_entry.get()
        isbn = isbn_entry.get()

        nouveau_livre = Livre(titre=titre, auteur=auteur, genre=genre, isbn=isbn)
        session.add(nouveau_livre)
        session.commit()
        messagebox.showinfo("Succès", "Livre ajouté avec succès")
        fenetre_livre.destroy()

    ajouter_livre_bouton = Button(frame, text="Ajouter Livre", command=valider_ajout_livre, width=20)
    ajouter_livre_bouton.grid(row=4, column=1, pady=10)

# Fonction pour supprimer un livre 
def supprimer_livre():
    fenetre_supprimer = Toplevel(fenetre)
    fenetre_supprimer.title("Supprimer Livre")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_supprimer, padx=10, pady=10)
    frame.grid(row=0, column=0)

    isbn_supprimer_label = Label(frame, text="ISBN du livre à supprimer:")
    isbn_supprimer_label.grid(row=0, column=0, pady=5)
    isbn_supprimer_entry = Entry(frame)
    isbn_supprimer_entry.grid(row=0, column=1, pady=5)

    def valider_suppression_livre():
        isbn = isbn_supprimer_entry.get()
        try:
            livre = session.query(Livre).filter_by(isbn=isbn).first()
            if livre:
                session.delete(livre)
                session.commit()
                messagebox.showinfo("Succès", "Livre supprimé avec succès")
                fenetre_supprimer.destroy()
            else:
                messagebox.showerror("Erreur", "Livre non trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du livre : {e}")

    supprimer_bouton = Button(frame, text="Supprimer Livre", command=valider_suppression_livre, width=20)
    supprimer_bouton.grid(row=1, column=1, pady=10)

# Fonction pour modifier des livres 
def modifier_livre():
    fenetre_modifier = Toplevel(fenetre)
    fenetre_modifier.title("Modifier Livre")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_modifier, padx=10, pady=10)
    frame.grid(row=0, column=0)

    isbn_modifier_label = Label(frame, text="ISBN du livre à modifier:")
    isbn_modifier_label.grid(row=0, column=0, pady=5)
    isbn_modifier_entry = Entry(frame)
    isbn_modifier_entry.grid(row=0, column=1, pady=5)

    titre_modifier_label = Label(frame, text="Nouveau Titre:")
    titre_modifier_label.grid(row=1, column=0, pady=5)
    titre_modifier_entry = Entry(frame)
    titre_modifier_entry.grid(row=1, column=1, pady=5)

    auteur_modifier_label = Label(frame, text="Nouvel Auteur:")
    auteur_modifier_label.grid(row=2, column=0, pady=5)
    auteur_modifier_entry = Entry(frame)
    auteur_modifier_entry.grid(row=2, column=1, pady=5)

    genre_modifier_label = Label(frame, text="Nouveau Genre:")
    genre_modifier_label.grid(row=3, column=0, pady=5)
    genre_modifier_entry = Entry(frame)
    genre_modifier_entry.grid(row=3, column=1, pady=5)

    def valider_modification_livre():
        isbn = isbn_modifier_entry.get()
        nouveau_titre = titre_modifier_entry.get()
        nouveau_auteur = auteur_modifier_entry.get()
        nouveau_genre = genre_modifier_entry.get()

        try:
            livre = session.query(Livre).filter_by(isbn=isbn).first()
            if livre:
                livre.titre = nouveau_titre
                livre.auteur = nouveau_auteur
                livre.genre = nouveau_genre
                session.commit()
                messagebox.showinfo("Succès", "Livre modifié avec succès")
                fenetre_modifier.destroy()
            else:
                messagebox.showerror("Erreur", "Livre non trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du livre : {e}")

    modifier_bouton = Button(frame, text="Modifier Livre", command=valider_modification_livre, width=20)
    modifier_bouton.grid(row=4, column=1, pady=10)

# Fonction pour afficher les livres
def afficher_livres():
    fenetre_afficher = Toplevel(fenetre)
    fenetre_afficher.title("Afficher Livres")

    # Créer un widget Text pour afficher les livres avec une barre de défilement
    text_widget = Text(fenetre_afficher, wrap="word", width=50, height=20)
    text_widget.grid(row=0, column=0, padx=10, pady=10)

    scrollbar = Scrollbar(fenetre_afficher, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    text_widget['yscrollcommand'] = scrollbar.set

    # Récupérer la liste des livres
    liste_livres = session.query(Livre).all()

    for livre in liste_livres:
        livre_str = f"Titre: {livre.titre}\nAuteur: {livre.auteur}\nGenre: {livre.genre}\nISBN: {livre.isbn}\nID: {livre.id}\n\n"
        text_widget.insert('end', livre_str)

    # Désactiver l'édition du widget Text
    text_widget.config(state='disabled')

# Fonction recherche de livre
def rechercher_livre():
    # Créer une fenêtre pour la recherche
    fenetre_recherche = Toplevel(fenetre)
    fenetre_recherche.title("Rechercher Livre")

    # Ajouter des étiquettes et des champs pour entrer le nom et l'auteur du livre
    nom_label = Label(fenetre_recherche, text="Nom du livre:")
    nom_label.grid(row=0, column=0)
    nom_entry = Entry(fenetre_recherche)
    nom_entry.grid(row=0, column=1)

    auteur_label = Label(fenetre_recherche, text="Auteur du livre:")
    auteur_label.grid(row=1, column=0)
    auteur_entry = Entry(fenetre_recherche)
    auteur_entry.grid(row=1, column=1)

    def valider_recherche():
        nom = nom_entry.get()
        auteur = auteur_entry.get()

        # Effectuer la recherche dans la base de données en fonction du nom et/ou de l'auteur
        if nom and auteur:
            # Recherche avec nom et auteur
            livre_trouve = session.query(Livre).filter_by(titre=nom, auteur=auteur).first()
        elif nom:
            # Recherche avec nom seulement
            livre_trouve = session.query(Livre).filter_by(titre=nom).first()
        elif auteur:
            # Recherche avec auteur seulement
            livre_trouve = session.query(Livre).filter_by(auteur=auteur).first()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer au moins le nom ou l'auteur pour la recherche.")
            return

        # Afficher les résultats dans une boîte de message
        if livre_trouve:
            details_livre = f"ID: {livre_trouve.id}, Titre: {livre_trouve.titre}, Auteur: {livre_trouve.auteur}, ISBN: {livre_trouve.isbn}"
            messagebox.showinfo("Résultats de la recherche", details_livre)
        else:
            messagebox.showinfo("Résultats de la recherche", "Aucun livre trouvé.")

        # Vous pouvez également fermer la fenêtre de recherche après affichage des résultats
        fenetre_recherche.destroy()

    recherche_button = Button(fenetre_recherche, text="Rechercher", command=valider_recherche, width=20)
    recherche_button.grid(row=5, column=1, pady=10)

# Catégorie des utilisateurs
def gestion_utilisateur():
    # Ajouter un bouton "Gestion utilisateurs"
    gestion_utilisateur_button = Button(fenetre, text="Gestion Utilisateurs", command=gestion_utilisateur)
    gestion_utilisateur_button.grid(row=1, column=0)

    # Supprimer le bouton "Gestion utilisateur" existant
    gestion_utilisateur_button.grid_forget()

    fenetre_utilisateur = Toplevel(fenetre)
    fenetre_utilisateur.title("Gestion des Utilisateurs")

    # Définir une taille pour la fenêtre
    fenetre_utilisateur.geometry("600x400")  

    # Configurer la largeur des colonnes
    fenetre_utilisateur.columnconfigure(0, weight=1)
    fenetre_utilisateur.columnconfigure(1, weight=1)
    fenetre_utilisateur.columnconfigure(2, weight=1)

    # Configurer la hauteur des lignes
    fenetre_utilisateur.rowconfigure(0, weight=1)
    fenetre_utilisateur.rowconfigure(1, weight=1)
    fenetre_utilisateur.rowconfigure(2, weight=1)
    fenetre_utilisateur.rowconfigure(3, weight=1)
    fenetre_utilisateur.rowconfigure(4, weight=1)
    fenetre_utilisateur.rowconfigure(5, weight=1)

    # Créer les boutons pour ajouter, supprimer et modifier les utilisateurs
    ajouter_utilisateur_button = Button(fenetre_utilisateur, text="Ajouter Utilisateur", command=ajouter_utilisateur, width=20, height=5, bg='green', fg='white')
    ajouter_utilisateur_button.grid(row=1, column=1, pady=10, sticky="nsew")

    supprimer_utilisateur_button = Button(fenetre_utilisateur, text="Supprimer Utilisateur", command=supprimer_utilisateur, width=20, height=5, bg='red', fg='white')
    supprimer_utilisateur_button.grid(row=2, column=1, pady=10, sticky="nsew")

    modifier_utilisateur_button = Button(fenetre_utilisateur, text="Modifier Utilisateur", command=modifier_utilisateur, width=20, height=5, bg='orange', fg='white')
    modifier_utilisateur_button.grid(row=3, column=1, pady=10, sticky="nsew")

    afficher_utilisateur_button = Button(fenetre_utilisateur, text="Afficher Utilisateurs", command=afficher_tous_les_utilisateurs, width=20, height=5, bg='blue', fg='white')
    afficher_utilisateur_button.grid(row=4, column=1, pady=10, sticky="nsew")

    rechercher_utilisateur_button = Button(fenetre_utilisateur, text="Rechercher Utilisateur", command=rechercher_utilisateur, width=20, height=5, bg='purple', fg='white')
    rechercher_utilisateur_button.grid(row=5, column=1, pady=10, sticky="nsew")



# Fonction pour ajouter un utilisateur
def ajouter_utilisateur():
    fenetre_utilisateur = Toplevel(fenetre)
    fenetre_utilisateur.title("Ajouter Utilisateur")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_utilisateur, padx=10, pady=10)
    frame.grid(row=0, column=0)

    nom_label = Label(frame, text="Nom:")
    nom_label.grid(row=0, column=0, pady=5)
    nom_entry = Entry(frame)
    nom_entry.grid(row=0, column=1, pady=5)

    prenom_label = Label(frame, text="Prénom:")
    prenom_label.grid(row=1, column=0, pady=5)
    prenom_entry = Entry(frame)
    prenom_entry.grid(row=1, column=1, pady=5)

    categorie_label = Label(frame, text="Catégorie:")
    categorie_label.grid(row=2, column=0, pady=5)
    categorie_entry = Entry(frame)
    categorie_entry.grid(row=2, column=1, pady=5)

    # Fonction pour valider l'ajout de l'utilisateur
    def valider_ajout_utilisateur():
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        categorie = categorie_entry.get()

        nouvel_utilisateur = Utilisateur(nom=nom, prenom=prenom, categorie=categorie)
        session.add(nouvel_utilisateur)
        session.commit()
        #print(f"Nom: {nouvel_utilisateur.nom}\nPrénom: {nouvel_utilisateur.prenom}\nCatégorie: {nouvel_utilisateur.categorie}\nID: {nouvel_utilisateur.id}")
        messagebox.showinfo("Succès", "Utilisateur ajouté avec succès")

    # Bouton pour ajouter l'utilisateur
    ajouter_utilisateur_bouton = Button(frame, text="Ajouter Utilisateur", command=valider_ajout_utilisateur, width=20)
    ajouter_utilisateur_bouton.grid(row=3, column=1, pady=10)

# Fonction pour supprimer un utilisateur
def supprimer_utilisateur():
    fenetre_supprimer_utilisateur = Toplevel(fenetre)
    fenetre_supprimer_utilisateur.title("Supprimer Utilisateur")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_supprimer_utilisateur, padx=10, pady=10)
    frame.grid(row=0, column=0)

    id_label = Label(frame, text="ID de l'utilisateur à supprimer:")
    id_label.grid(row=0, column=0, pady=5)
    id_entry = Entry(frame)
    id_entry.grid(row=0, column=1, pady=5)

    def valider_suppression_utilisateur():
        utilisateur_id = id_entry.get()

        # Assurez-vous que l'ID est un entier valide
        try:
            utilisateur_id = int(utilisateur_id)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
            return

        # Vérifiez si l'utilisateur avec cet ID existe
        utilisateur_a_supprimer = session.query(Utilisateur).get(utilisateur_id)
        if utilisateur_a_supprimer:
            # Supprimer l'utilisateur
            session.delete(utilisateur_a_supprimer)
            session.commit()

            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès")
            fenetre_supprimer_utilisateur.destroy()
        else:
            messagebox.showerror("Erreur", "Aucun utilisateur avec cet ID n'a été trouvé.")

    supprimer_utilisateur_bouton = Button(frame, text="Supprimer Utilisateur", command=valider_suppression_utilisateur, width=20)
    supprimer_utilisateur_bouton.grid(row=1, column=1, pady=10)

# Fonction pour modifier un utilisateur
def modifier_utilisateur():
    fenetre_modifier_utilisateur = Toplevel(fenetre)
    fenetre_modifier_utilisateur.title("Modifier Utilisateur")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_modifier_utilisateur, padx=10, pady=10)
    frame.grid(row=0, column=0)

    id_label = Label(frame, text="ID de l'utilisateur à modifier:")
    id_label.grid(row=0, column=0, pady=5)
    id_entry = Entry(frame)
    id_entry.grid(row=0, column=1, pady=5)

    nom_label = Label(frame, text="Nouveau nom:")
    nom_label.grid(row=1, column=0, pady=5)
    nom_entry = Entry(frame)
    nom_entry.grid(row=1, column=1, pady=5)

    prenom_label = Label(frame, text="Nouveau prénom:")
    prenom_label.grid(row=2, column=0, pady=5)
    prenom_entry = Entry(frame)
    prenom_entry.grid(row=2, column=1, pady=5)

    categorie_label = Label(frame, text="Nouvelle catégorie:")
    categorie_label.grid(row=3, column=0, pady=5)
    categorie_entry = Entry(frame)
    categorie_entry.grid(row=3, column=1, pady=5)

    def valider_modification_utilisateur():
        utilisateur_id = id_entry.get()

        # Assurez-vous que l'ID est un entier valide
        try:
            utilisateur_id = int(utilisateur_id)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
            return

        # Vérifiez si l'utilisateur avec cet ID existe
        utilisateur_a_modifier = session.query(Utilisateur).get(utilisateur_id)
        if utilisateur_a_modifier:
            # Mettez à jour les informations de l'utilisateur
            utilisateur_a_modifier.nom = nom_entry.get()
            utilisateur_a_modifier.prenom = prenom_entry.get()
            utilisateur_a_modifier.categorie = categorie_entry.get()

            session.commit()
            messagebox.showinfo("Succès", "Informations de l'utilisateur modifiées avec succès")
            fenetre_modifier_utilisateur.destroy()
        else:
            messagebox.showerror("Erreur", "Aucun utilisateur avec cet ID n'a été trouvé.")

    modifier_utilisateur_bouton = Button(frame, text="Modifier Utilisateur", command=valider_modification_utilisateur, width=20)
    modifier_utilisateur_bouton.grid(row=4, column=1, pady=10)

# Fonction pour afficher les utilisateurs
def afficher_tous_les_utilisateurs():
    fenetre_afficher_utilisateur = Toplevel(fenetre)
    fenetre_afficher_utilisateur.title("Afficher Utilisateurs")

    # Créer un widget Text pour afficher les utilisateurs avec une barre de défilement
    text_widget = Text(fenetre_afficher_utilisateur, wrap="word", width=50, height=20)
    text_widget.grid(row=0, column=0, padx=10, pady=10)

    scrollbar = Scrollbar(fenetre_afficher_utilisateur, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    text_widget['yscrollcommand'] = scrollbar.set

    # Récupérer la liste des utilisateurs
    liste_utilisateurs = session.query(Utilisateur).all()

    for utilisateur in liste_utilisateurs:
        utilisateur_str = f"ID: {utilisateur.id}\nNom: {utilisateur.nom}\nPrénom: {utilisateur.prenom}\nCatégorie: {utilisateur.categorie}\n\n"
        text_widget.insert('end', utilisateur_str)

    # Désactiver l'édition du widget Text
    text_widget.config(state='disabled')

# Fonction recherche d'utilisateur
def rechercher_utilisateur():
    # Créer une fenêtre pour la recherche
    fenetre_recherche_utilisateur = Toplevel(fenetre)
    fenetre_recherche_utilisateur.title("Rechercher Utilisateur")

    # Ajouter des étiquettes et des champs pour entrer le nom et le prénom de l'utilisateur
    nom_label = Label(fenetre_recherche_utilisateur, text="Nom de l'utilisateur:")
    nom_label.grid(row=0, column=0)
    nom_entry = Entry(fenetre_recherche_utilisateur)
    nom_entry.grid(row=0, column=1)

    prenom_label = Label(fenetre_recherche_utilisateur, text="Prénom de l'utilisateur:")
    prenom_label.grid(row=1, column=0)
    prenom_entry = Entry(fenetre_recherche_utilisateur)
    prenom_entry.grid(row=1, column=1)

    def valider_recherche_utilisateur():
        nom = nom_entry.get()
        prenom = prenom_entry.get()

        # Effectuer la recherche dans la base de données en fonction du nom et/ou du prénom
        if nom and prenom:
            # Recherche avec nom et prénom
            utilisateur_trouve = session.query(Utilisateur).filter_by(nom=nom, prenom=prenom).first()
        elif nom:
            # Recherche avec nom seulement
            utilisateur_trouve = session.query(Utilisateur).filter_by(nom=nom).first()
        elif prenom:
            # Recherche avec prénom seulement
            utilisateur_trouve = session.query(Utilisateur).filter_by(prenom=prenom).first()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer au moins le nom ou le prénom pour la recherche.")
            return

        # Afficher les résultats dans une boîte de message
        if utilisateur_trouve:
            details_utilisateur = f"ID: {utilisateur_trouve.id}, Nom: {utilisateur_trouve.nom}, Prénom: {utilisateur_trouve.prenom}, Catégorie: {utilisateur_trouve.categorie}"

            # Récupérer les livres empruntés par l'utilisateur
            livres_empruntes = session.query(Livre).join(Emprunt).filter(Emprunt.utilisateur_id == utilisateur_trouve.id).all()
            if livres_empruntes:
                details_utilisateur += "\nLivres empruntés :"
                for livre in livres_empruntes:
                    details_utilisateur += f"\n- {livre.titre} ({livre.auteur})"
            else:
                details_utilisateur += "\nAucun livre emprunté."

            messagebox.showinfo("Résultats de la recherche", details_utilisateur)
        else:
            messagebox.showinfo("Résultats de la recherche", "Aucun utilisateur trouvé.")

        # Fermer la fenêtre de recherche après affichage des résultats
        fenetre_recherche_utilisateur.destroy()

    recherche_button = Button(fenetre_recherche_utilisateur, text="Rechercher", command=valider_recherche_utilisateur, width=20)
    recherche_button.grid(row=5, column=1, pady=10)

# Catégorie pour la gestion des emprunts
def gestion_emprunts():
    # Ajouter un bouton "Gestion Emprunts"
    gestion_emprunts_button = Button(fenetre, text="Gestion Emprunts", command=gestion_emprunts)
    gestion_emprunts_button.grid(row=2, column=0)

    # Supprimer le bouton "Gestion Emprunts" existant
    gestion_emprunts_button.grid_forget()

    fenetre_emprunts = Toplevel(fenetre)
    fenetre_emprunts.title("Gestion des Emprunts")

    # Définir une taille pour la fenêtre
    fenetre_emprunts.geometry("600x400")  

    # Configurer la largeur des colonnes
    fenetre_emprunts.columnconfigure(0, weight=1)
    fenetre_emprunts.columnconfigure(1, weight=1)
    fenetre_emprunts.columnconfigure(2, weight=1)

    # Configurer la hauteur des lignes
    fenetre_emprunts.rowconfigure(0, weight=1)
    fenetre_emprunts.rowconfigure(1, weight=1)
    fenetre_emprunts.rowconfigure(2, weight=1)

    # Créer les boutons pour emprunter, afficher et retourner les livres
    emprunter_livre_button = Button(fenetre_emprunts, text="Emprunter Livre", command=emprunter_livre, width=20, height=5, bg='green', fg='white')
    emprunter_livre_button.grid(row=1, column=1, pady=10, sticky="nsew")

    afficher_emprunts_button = Button(fenetre_emprunts, text="Afficher Emprunts", command=afficher_emprunts_tkinter, width=20, height=5, bg='blue', fg='white')
    afficher_emprunts_button.grid(row=2, column=1, pady=10, sticky="nsew")

    retourner_livre_button = Button(fenetre_emprunts, text="Retourner Livre", command=retourner_livre, width=20, height=5, bg='orange', fg='white')
    retourner_livre_button.grid(row=3, column=1, pady=10, sticky="nsew")

# Fonction pour emprunter un livre
def emprunter_livre():
    fenetre_emprunts = Toplevel(fenetre)
    fenetre_emprunts.title("Emprunter Livre")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_emprunts, padx=10, pady=10)
    frame.grid(row=0, column=0)

    utilisateur_id_label = Label(frame, text="ID Utilisateur:")
    utilisateur_id_label.grid(row=0, column=0, pady=5)
    utilisateur_id_entry = Entry(frame)
    utilisateur_id_entry.grid(row=0, column=1, pady=5)

    livre_id_label = Label(frame, text="ID Livre:")
    livre_id_label.grid(row=1, column=0, pady=5)
    livre_id_entry = Entry(frame)
    livre_id_entry.grid(row=1, column=1, pady=5)

    def valider_emprunt():
        try:
            utilisateur_id = int(utilisateur_id_entry.get())
            livre_id = int(livre_id_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des IDs valides.")
            return

        date_emprunt = datetime.now()
        date_retour = None

        nouvel_emprunt = Emprunt(utilisateur_id=utilisateur_id, livre_id=livre_id, date_emprunt=date_emprunt, date_retour=date_retour)
        session.add(nouvel_emprunt)
        session.commit()

        messagebox.showinfo("Succès", "Emprunt enregistré avec succès")
        fenetre_emprunts.destroy()

    valider_emprunt_button = Button(frame, text="Valider Emprunt", command=valider_emprunt, width=20)
    valider_emprunt_button.grid(row=2, column=1, pady=10)

# Fonction pour afficher les emprunts
def afficher_emprunts_tkinter():
    fenetre_emprunts = Toplevel(fenetre)
    fenetre_emprunts.title("Afficher Emprunts")

    # Créer un widget Text pour afficher les emprunts avec une barre de défilement
    text_widget = Text(fenetre_emprunts, wrap="word", width=50, height=20)
    text_widget.grid(row=0, column=0, padx=10, pady=10)

    scrollbar = Scrollbar(fenetre_emprunts, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    text_widget['yscrollcommand'] = scrollbar.set

    # Récupérer la liste des emprunts
    liste_emprunts = session.query(Emprunt).all()

    for emprunt in liste_emprunts:
        emprunt_str = f"ID Emprunt: {emprunt.id}\nID Utilisateur: {emprunt.utilisateur_id}\nID Livre: {emprunt.livre_id}\nDate Emprunt: {emprunt.date_emprunt}\nDate Retour: {emprunt.date_retour}\n\n"
        text_widget.insert('end', emprunt_str)

    # Désactiver l'édition du widget Text
    text_widget.config(state='disabled')

# Fonction pour retourner un livre
def retourner_livre():
    fenetre_emprunts = Toplevel(fenetre)
    fenetre_emprunts.title("Retourner Livre")

    # Frame pour organiser les éléments
    frame = Frame(fenetre_emprunts, padx=10, pady=10)
    frame.grid(row=0, column=0)

    emprunt_id_label = Label(frame, text="ID Emprunt:")
    emprunt_id_label.grid(row=0, column=0, pady=5)
    emprunt_id_entry = Entry(frame)
    emprunt_id_entry.grid(row=0, column=1, pady=5)

    def valider_retour():
        try:
            emprunt_id = int(emprunt_id_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
            return

        retour_date = datetime.now()

        emprunt = session.query(Emprunt).filter_by(id=emprunt_id).first()
        if emprunt:
            emprunt.date_retour = retour_date
            session.commit()
            messagebox.showinfo("Succès", "Livre retourné avec succès")
            fenetre_emprunts.destroy()
        else:
            messagebox.showerror("Erreur", "Aucun emprunt avec cet ID n'a été trouvé")

    retourner_livre_button = Button(frame, text="Retourner Livre", command=valider_retour, width=20)
    retourner_livre_button.grid(row=2, column=1, pady=10)

# Gestion de la génération des rapports
def generer_rapports():
    # Fenêtre des rapports
    fenetre_rapports = Toplevel(fenetre)
    fenetre_rapports.title("Rapports et Statistiques")

    # Créer un widget Text pour afficher les rapports avec une barre de défilement
    text_widget = Text(fenetre_rapports, wrap="word", width=80, height=20)
    text_widget.grid(row=0, column=0, padx=10, pady=10)

    scrollbar = Scrollbar(fenetre_rapports, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    text_widget['yscrollcommand'] = scrollbar.set

    # Rapport nombre total de livres empruntés
    nombre_emprunts = session.query(func.count(Emprunt.id)).scalar()
    text_widget.insert('end', f"Nombre total d'emprunts : {nombre_emprunts}\n\n")

    # Rapport des livres les plus populaires
    sous_requete = (
        session.query(Livre.id, func.count(Emprunt.id).label('nb_emprunts'))
        .outerjoin(Livre.emprunts)
        .group_by(Livre.id)
        .order_by(func.count(Emprunt.id).desc())
        .limit(5)
        .subquery()
    )

    livres_populaires = (
        session.query(Livre, sous_requete.c.nb_emprunts)
        .outerjoin(sous_requete, Livre.id == sous_requete.c.id)
        .order_by(sous_requete.c.nb_emprunts.desc())
        .limit(5)
        .all()
    )

    text_widget.insert('end', "Livres les plus populaires :\n")
    for livre, nb_emprunts in livres_populaires:
        text_widget.insert('end', f"{livre.titre} - {nb_emprunts} emprunts\n")
    text_widget.insert('end', "\n")

    # Désactiver l'édition du widget Text
    text_widget.config(state='disabled')

# Démarrer la boucle principale Tkinter
fenetre = Tk()
fenetre.title("Gestion de Bibliothèque")
fenetre.geometry("1280x720")

# Configurer la largeur des colonnes
fenetre.columnconfigure(0, weight=1)

# Configurer la hauteur des lignes
fenetre.rowconfigure(0, weight=1)
fenetre.rowconfigure(1, weight=1)
fenetre.rowconfigure(2, weight=1)
fenetre.rowconfigure(3, weight=1)
fenetre.rowconfigure(4, weight=1)

# Afficher le texte de bienvenue
bienvenue_label = Label(fenetre, text="Bienvenue sur votre Gestionnaire de Bibliothèque", font=("Helvetica", 16))
bienvenue_label.grid(row=0, column=0, pady=20, sticky="nsew")

# Ajouter un bouton "Gestion Livres" initial avec une couleur de fond et de texte
gestion_livres_button = Button(fenetre, text="Gestion Livres", command=gestion_livres, width=20, height=5, bg='green', fg='white', font=("Helvetica", 12))
gestion_livres_button.grid(row=1, column=0, pady=10, sticky="nsew")

# Ajouter un bouton "Gestion utilisateur" initial avec une couleur de fond et de texte
gestion_utilisateur_button = Button(fenetre, text="Gestion Utilisateur", command=gestion_utilisateur, width=20, height=5, bg='blue', fg='white', font=("Helvetica", 12))
gestion_utilisateur_button.grid(row=2, column=0, pady=10, sticky="nsew")

# Ajouter un bouton "Gestion Emprunts" initial avec une couleur de fond et de texte
gestion_emprunt_button = Button(fenetre, text="Gestion Emprunts", command=gestion_emprunts, width=20, height=5, bg='orange', fg='white', font=("Helvetica", 12))
gestion_emprunt_button.grid(row=3, column=0, pady=10, sticky="nsew")

# Ajouter un bouton "Générer Rapports" dans votre interface principale
generer_rapports_button = Button(fenetre, text="Générer Rapports", command=generer_rapports, width=20, height=5, bg='purple', fg='white', font=("Helvetica", 12))
generer_rapports_button.grid(row=4, column=0, pady=10, sticky="nsew")

# Démarrer la boucle principale Tkinter
fenetre.mainloop()
