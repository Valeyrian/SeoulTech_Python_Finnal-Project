import sys
from unittest import case
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from ui.main_window import Ui_MainWindow
from controllers.movie_controller import MovieController
from genre_row import GenreRow
from models import Catalogue, Film
from card import createFilmCard
import os
from user_manager.user import UserManager
from user_manager.user_dialogs import show_login_dialog, confirm_logout, show_genre_preferences_dialog
from player.player import player

class MainApp(QMainWindow, Ui_MainWindow):
    """
    Vue principale de l'application Netflux
    Responsabilités : affichage UI, interactions utilisateur
    Ne contient PAS de logique métier (délégation au controller)
    """
    
    def __init__(self, catalogue):
        super().__init__()
        self.setupUi(self)  
        self.setWindowTitle("Netflux")

        if (not os.path.exists("./assets/logo.png")):
            pixmap = QPixmap("./assets/file_not_found.jpeg")
            raise FileNotFoundError("Le fichier './assets/logo.png' est manquant. Veuillez vous assurer qu'il est présent.")
        else :
            pixmap = QPixmap("./assets/logo.png")

        self.logo.setPixmap(pixmap.scaled(140, 40))

        
        # Initialiser le gestionnaire d'utilisateurs
        self.user_manager = UserManager()
        self.user_manager.load_users()
        
        # Stocker le catalogue pour accéder aux genres
        self.catalogue = catalogue
        
        # Initialiser le contrôleur (couche métier)
        self.controller = MovieController(catalogue)
        
        self.current_view = "acceuil"
        self.current_view_mode = "genre"
       
        self.show_movie_list_by_genre()  # Vue par genre avec scroll horizontal
       
        
        # Liste pour stocker toutes les cartes affichées (pour la synchronisation)
        self.displayed_cards = []
        
        # Connecter les événements UI
        self.searchButton.clicked.connect(self.on_search_clicked)
        self.searchBar.returnPressed.connect(self.on_search_clicked)
        
        # Bouton Accueil : afficher tous les films par genre
        self.acceuilButton.clicked.connect(self.on_home_clicked)

        # Bouton Recommandation
        self.recomandationButton.clicked.connect(self.on_recomendation_clicked)
        
        # Menu déroulant pour le bouton Account
        self.setup_account_menu()
        
    
    # ========== MÉTHODES UI (Affichage uniquement) ==========
    
    def setup_account_menu(self):
        """
        Configure le menu déroulant pour le bouton Account
        Affiche Login ou Logout selon l'état de connexion
        """
        # Créer le menu
        account_menu = QMenu(self)
        account_menu.setObjectName("accountMenu")
        
        # Vérifier si un utilisateur est connecté
        if self.user_manager.current_user:
            # Utilisateur connecté : afficher le profil et logout
            user = self.user_manager.current_user
            
            # Afficher le nom de l'utilisateur (cliquable pour voir le profil)
            profile_action = QAction(f"👤 {user.username}", self)
            profile_action.setEnabled(False)
            account_menu.addAction(profile_action)
            
            account_menu.addSeparator()
            
            # Option Favoris
            favorites_action = QAction("My likes", self)
            favorites_action.triggered.connect(self.on_favorites_clicked)
            account_menu.addAction(favorites_action)
            
            # # Option Watchlist
            # watchlist_action = QAction("My watch list", self)
            # watchlist_action.triggered.connect(self.on_watchlist_clicked)
            # account_menu.addAction(watchlist_action)

            genre_action = QAction("My genre preferences", self)
            genre_action.triggered.connect(self.on_genre_preferences_clicked)
            account_menu.addAction(genre_action)
            
            account_menu.addSeparator()
            
            # Bouton Logout
            logout_action = QAction("Logout", self)
            logout_action.triggered.connect(self.on_logout_clicked)
            account_menu.addAction(logout_action)
        else:
            # Aucun utilisateur connecté : afficher login
            login_action = QAction("Login", self)
            login_action.triggered.connect(self.on_login_clicked)
            account_menu.addAction(login_action)
        
        # Attacher le menu au bouton
        self.accountButton.setMenu(account_menu)
    
    def _calculate_columns(self):
        """
        Calcule dynamiquement le nombre de colonnes en fonction de la largeur disponible
        """
        card_width = 300  # Largeur approximative d'une carte (280px + marges)
        min_columns = 2   # Nombre minimum de colonnes
        max_columns = 5   # Nombre maximum de colonnes (cartes plus larges)
        default_columns = 3  # Valeur par défaut au démarrage
        
        # Obtenir la largeur disponible dans la zone de contenu
        available_width = self.scrollArea.width() - 40  # Marges
        
        # Si la fenêtre n'est pas encore affichée (largeur trop petite), utiliser la valeur par défaut
        if available_width < 400:  # Largeur minimale raisonnable
            return default_columns
        
        # Calculer le nombre de colonnes optimal
        columns = max(min_columns, min(max_columns, available_width // card_width))
        
        return columns
    
    def _connect_card_signals(self, card):
        """
        Connecte les signaux d'une carte de film pour la synchronisation
        
        Args:
            card: Instance de FilmCard
        """
        # Connecter le signal de changement de like
        card.like_changed.connect(self._sync_all_cards_like_state)
        #card.play_clicked.connect(self.startMediaPlayer)
    
    def _sync_all_cards_like_state(self, film_id, is_liked):
        """
        Synchronise l'état like de toutes les cartes affichées pour un film donné
        
        Args:
            film_id: Identifiant du film
            is_liked: Nouvel état du like
        """

        # Parcourir toutes les cartes affichées
        for card in self.displayed_cards:
            if hasattr(card, 'sync_like_state'):
                card.sync_like_state(film_id, is_liked)

        if self.current_view_mode == "favorites":
            # Si on est dans les favoris, rafraîchir l'affichage pour retirer les films non likés
            QTimer.singleShot(100, self._reload_favorites_view)
    
    def resizeEvent(self, event):
        """
        Gestionnaire d'événement pour redimensionner la fenêtre
        Réorganise les cartes quand la fenêtre change de taille
        """
        super().resizeEvent(event)
        
        # Réafficher les films avec le nouveau nombre de colonnes
        if hasattr(self, 'controller') and self.gridLayout.count() > 0:
            # Vérifier si on est en mode grille ou genre
            first_item = self.gridLayout.itemAt(0)
            if first_item and first_item.widget():
                if isinstance(first_item.widget(), GenreRow):
                    # Mode genre : réorganiser les GenreRow avec le nouveau span
                    current_query = self.searchBar.text().strip()
                    if current_query:
                        movie_list = self.controller.search_movies(current_query)
                    else:
                        movie_list = self.controller.get_all_movies()
                    self.show_movie_list_by_genre(movie_list)
                else:
                    # Mode grille : réorganiser les cartes
                    current_query = self.searchBar.text().strip()
                    if current_query:
                        movie_list = self.controller.search_movies(current_query)
                    else:
                        movie_list = self.controller.get_all_movies()
                    self.show_movie_list(movie_list)
    
    def show_movie_list(self, movie_list=None):
        """
        Met à jour l'affichage des cartes de films
        
        Args:
            movie_list (list, optional): Liste de films à afficher.
                                        Si None, demande au contrôleur les films à afficher
        """
        # Si aucune liste fournie, demander au contrôleur
        if movie_list is None:
            movie_list = self.controller.get_all_movies()
        
        #use le layout dédié aux films (défini dans main_window.py)
        layout = self.gridLayout
        
        # Vider proprement les anciennes cartes
        self._clear_layout(layout)
        
        # Réinitialiser la liste des cartes affichées
        self.displayed_cards = []
        
        # Ajouter les nouvelles cartes en grille
        row, col = 0, 0
        max_col = self._calculate_columns()  # Calcul dynamique du nombre de colonnes
        
        for film in movie_list:
            card_widget = createFilmCard(film, self.user_manager)
            
            # Connecter les signaux de la carte
            self._connect_card_signals(card_widget)
            
            # Enregistrer la carte pour la synchronisation
            self.displayed_cards.append(card_widget)
            
            layout.addWidget(card_widget, row, col)
            col += 1
            if col >= max_col:
                col = 0
                row += 1
        
        # Forcer la mise à jour de la zone de scroll
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass
    
    def show_movie_list_by_genre(self,movie_list=None):
        """
        Affiche les films organisés par genre avec scroll horizontal
        Style Netflix avec une ligne par genre
        """
        # Récupérer les films groupés par genre depuis le contrôleur
        if movie_list is None:
            movie_list = self.controller.get_all_movies()
        grouped_movies = self.controller.get_movies_grouped_by_genre(movie_list)
        
        # Vider le layout actuel
        layout = self.gridLayout
        self._clear_layout(layout)
        
        # Réinitialiser la liste des cartes affichées
        self.displayed_cards = []
        
        # Calculer le nombre de colonnes pour le span
        max_col = self._calculate_columns()
        
        # Créer un container vertical pour toutes les rangées de genre
        row = 0
        for genre, films in grouped_movies.items():
            if films:  # Seulement si le genre a des films
                # Créer une rangée de genre avec scroll horizontal
                genre_row = GenreRow(genre, films, self.user_manager)
                layout.addWidget(genre_row, row, 0, 1, max_col)  # Prend toute la largeur (dynamique)
                
                # Enregistrer toutes les cartes de cette rangée et connecter leurs signaux
                for card_widget in genre_row.get_cards():
                    self._connect_card_signals(card_widget)
                    self.displayed_cards.append(card_widget)
                
                row += 1
        
        # Forcer la mise à jour
        try:
            self.scrollAreaWidgetContents.adjustSize()
        except Exception:
            pass

    def show_movies(self,movie_list):
        """
        Affiche une liste de films donnée selon le mode d'affichage actuel
        
        Args:
            movie_list (list): Liste de films à afficher
        """
        self._clear_layout(self.gridLayout)

        if self.current_view_mode == "genre":
            self.show_movie_list_by_genre(movie_list)
        elif self.current_view_mode == "grid":
            self.show_movie_list(movie_list)
            
    def _clear_layout(self, layout):
        """
        Helper privé pour vider proprement un layout
        
        Args:
            layout: QLayout à vider
        """
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            else:
                # Gérer les sous-layouts si nécessaire
                sub_layout = item.layout()
                if sub_layout:
                    self._clear_layout(sub_layout)
    
  ##  def playVideo(self, movie):
       ## player.startMediaPlayer(movie)
        
        
   
    # ========== GESTIONNAIRES D'ÉVÉNEMENTS (Event handlers) ==========
    
    def on_home_clicked(self):
        """
        Gestionnaire du clic sur le bouton Accueil
        Réinitialise la recherche et affiche tous les films
        """
        # Vider la barre de recherche
        self.searchBar.clear()
        
        # Demander au contrôleur tous les films
        all_movies = self.controller.get_all_movies()
        
        # Mettre à jour l'affichage
        self.current_view = "acceuil"
        self.current_view_mode = "genre"
        self.show_movies(all_movies)
        
    def on_recomendation_clicked(self):
        """ 
        Gestionnaire du clic sur le bouton recommandation
        Délègue la recommandation au contrôleur
        """
        if not self.user_manager.current_user:
            print("Veuillez vous connecter pour voir des recommandations")
            return
        
        user = self.user_manager.current_user
        
        # Demander au contrôleur les recommandations pour l'utilisateur
        recommendations = self.controller.get_recommanded_movies(user)
        
        # Mettre à jour l'affichage (logique UI)s
        self.current_view = "recommandation"
        self.current_view_mode = "genre"
        self.show_movies(recommendations)
    
    def on_search_clicked(self):
        """
        Gestionnaire du clic sur le bouton recherche (ou Enter dans la barre)
        Délègue la recherche au contrôleur
        """
        query = self.searchBar.text().strip()
        
        # Demander au contrôleur de faire la recherche (logique métier)
        results = self.controller.search_movies(query)
        
        # Mettre à jour l'affichage (logique UI)
        self.current_view = "search"
        self.current_view_mode = "grid"
        self.show_movies(results)



    # ========== GESTIONNAIRES DU MENU ACCOUNT ==========
    
    def on_login_clicked(self):
        """
        Gestionnaire pour le login
        Affiche le dialogue de connexion
        """
        user = show_login_dialog(self.user_manager, self)
        
        if user:
            print(f"Connecté en tant que {user.username}")
            # Rafraîchir le menu pour afficher logout
            self.setup_account_menu()
    
    def on_genre_preferences_clicked(self):
        """
        Gestionnaire pour afficher le dialogue de préférences de genres
        """
        if not self.user_manager.current_user:
            print("Veuillez vous connecter pour gérer vos préférences")
            return
        
        # Récupérer la liste de tous les genres du catalogue
        all_genres = self.catalogue.getAllTheGenres()
        
        # Afficher le dialogue
        show_genre_preferences_dialog(self.user_manager, all_genres, self)
    
    def on_logout_clicked(self):
        """
        Gestionnaire pour le logout
        """
        if self.user_manager.current_user:
            # Demander confirmation
            if confirm_logout(self.user_manager.current_user.username, self):
                print(f"Déconnexion de {self.user_manager.current_user.username}")
                self.user_manager.current_user = None
                self.user_manager.save_users()
                
                # Rafraîchir le menu pour afficher login
                self.setup_account_menu()
        else:
            print("Aucun utilisateur connecté")
    
    def on_favorites_clicked(self):
        """
        Gestionnaire pour afficher les favoris
        """
        user = self.user_manager.current_user
        if not user:
            print("Veuillez vous connecter pour voir vos favoris")
            return

        print(f"Favoris de {user.username}: {user.favorites}")
        self.searchBar.clear()

        favorites = self.controller.get_favorite_movies(user)

        self.current_view = "favorites"
        self.current_view_mode = "grid"
        self.show_movies(favorites)

    def _reload_favorites_view(self):
            """
            Recharge complètement la vue des favoris (appelé en différé)
            """
            user = self.user_manager.current_user
            if not user:
                return

            print(f"[RELOAD] Rechargement de la vue favoris pour {user.username}")
        
            favorites = self.controller.get_favorite_movies(user)

            if not favorites:
                print("Aucun favori à afficher")
                self._clear_layout(self.gridLayout)
            else:
                self.show_movies(favorites)

    def on_watchlist_clicked(self):
            """
            Gestionnaire pour afficher la watchlist
            """
            if not self.user_manager.current_user:
                print("⚠️  Veuillez vous connecter pour voir votre liste")
                return
            
            user = self.user_manager.current_user
            print(f"📋 Liste de {user.username}: {user.watchlist}")
            # TODO: Filtrer et afficher les films de la watchlist

        
            
if __name__ == "__main__":

    katalogue = Catalogue()
    katalogue.loadFromCSV()
   # katalogue.printFilms()

    app = QApplication(sys.argv)
    
    # Charger la feuille de style Netflux
    style_path = "./assets/styles.qss"
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        print(" Feuille de style Netflux chargée")
    else:
        print(f"  Feuille de style non trouvée : {style_path}")
        raise FileNotFoundError(f"Le fichier de style '{style_path}' est manquant. Veuillez vous assurer qu'il est présent.")
    
    window = MainApp(katalogue)
    window.show()
    sys.exit(app.exec())
