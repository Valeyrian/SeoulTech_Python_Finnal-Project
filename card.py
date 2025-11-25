"""
Widget de carte de film pour l'application Netflux
Affiche un film avec son image, titre, genres et boutons d'interaction
"""
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
import os


class FilmCard(QFrame):
    """
    Widget représentant une carte de film interactive
    Style Netflix : format rectangulaire horizontal avec boutons like et play
    """
    
    # Signal émis quand le statut like change (film_id, is_liked)
    like_changed = pyqtSignal(str, bool)
    # Signal émis quand le bouton play est cliqué
    play_clicked = pyqtSignal(object)
    
    def __init__(self, film, user_manager=None, parent=None):
        """
        Initialise une carte de film
        
        Args:
            film: Instance de Film à afficher
            user_manager: Gestionnaire d'utilisateurs (optionnel)
            parent: Widget parent (optionnel)
        """
        super().__init__(parent)
        self.film = film
        self.user_manager = user_manager
        
        # Configuration du widget
        self.setMinimumSize(280, 160)
        self.setMaximumSize(280, 160)
        self.setObjectName("movieCard")
        self.setProperty("class", "movie-card")
        
        # Créer l'interface
        self.setup_ui()
        
        # Connecter les signaux
        self.connect_signals()
    
    def setup_ui(self):
        """Configure l'interface de la carte"""
        # Layout principal vertical : image en haut, infos en bas
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Container pour l'image
        self.create_image_container(main_layout)
        
        # Container pour les infos en bas
        self.create_info_container(main_layout)
    
    def create_image_container(self, parent_layout):
        """Crée le container de l'image du film"""
        image_container = QFrame()
        image_container.setObjectName("imageContainer")
        image_container.setMinimumSize(280, 105)
        image_container.setMaximumSize(280, 105)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)

        # Charger l'image
        if not os.path.exists(self.film.tiles):
            pixmap = QPixmap("./assets/image_not_found.jpeg")
        else:
            pixmap = QPixmap(self.film.tiles)

        image_label = QLabel()
        image_label.setPixmap(
            pixmap.scaled(280, 105, 
                         Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                         Qt.TransformationMode.SmoothTransformation)
        )
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setObjectName("movieImage")
        image_layout.addWidget(image_label)
        
        parent_layout.addWidget(image_container)
    
    def create_info_container(self, parent_layout):
        """Crée le container des informations et boutons"""
        info_container = QFrame()
        info_container.setObjectName("infoContainer")
        info_container.setMinimumHeight(55)
        info_container.setMaximumHeight(55)
        
        main_info_layout = QHBoxLayout(info_container)
        main_info_layout.setContentsMargins(8, 6, 8, 8)
        main_info_layout.setSpacing(8)
        
        # Textes (titre + genre/durée)
        self.create_text_section(main_info_layout)
        
        main_info_layout.addStretch()
        
        # Boutons (like + play)
        self.create_action_buttons(main_info_layout)
        
        parent_layout.addWidget(info_container)
    
    def create_text_section(self, parent_layout):
        """Crée la section texte (titre et métadonnées)"""
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)

        # Titre avec ellipse
        title_label = QLabel(self.film.titre)
        title_label.setWordWrap(False)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setObjectName("movieTitle")
        title_label.setMaximumHeight(18)
        
        # Appliquer l'ellipse
        metrics = QFontMetrics(title_label.font())
        elided_text = metrics.elidedText(self.film.titre, Qt.TextElideMode.ElideRight, 220)
        title_label.setText(elided_text)
        text_layout.addWidget(title_label)

        # Genre et durée
        genre_text = ', '.join(self.film.genres[:2])
        if len(self.film.genres) > 2:
            genre_text += '...'
        
        genre_duration_label = QLabel(f"{genre_text} • {self.film.minute}m")
        genre_duration_label.setObjectName("genreDurationLabel")
        genre_duration_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_layout.addWidget(genre_duration_label)
        
        parent_layout.addLayout(text_layout)
    
    def create_action_buttons(self, parent_layout):
        """Crée les boutons d'action (like et play)"""
        # Bouton Like (cœur)
        self.like_button = QPushButton("♡")
        self.like_button.setObjectName("likeButton")
        self.like_button.setProperty("film_id", self.film.system_name)
        self.like_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.like_button.setMinimumSize(32, 28)
        self.like_button.setMaximumSize(32, 28)
        
        # Mettre à jour l'état du bouton like
        self.update_like_button_state()
        
        parent_layout.addWidget(self.like_button, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Bouton Play
        self.play_button = QPushButton("▶")
        self.play_button.setObjectName("playButtonMini")
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setMinimumSize(28, 28)
        self.play_button.setMaximumSize(32, 28)
        
        parent_layout.addWidget(self.play_button, alignment=Qt.AlignmentFlag.AlignVCenter)
    
    def connect_signals(self):
        """Connecte les signaux des boutons"""
        self.like_button.clicked.connect(self.on_like_clicked)
        self.play_button.clicked.connect(self.on_play_clicked)
    
    def update_like_button_state(self):
        """Met à jour l'apparence du bouton like selon l'état"""
        if self.user_manager and self.user_manager.current_user:
            is_liked = self.user_manager.current_user.is_favorite(self.film.system_name)
            self.like_button.setText("♥" if is_liked else "♡")
            self.like_button.setProperty("liked", is_liked)
        else:
            self.like_button.setText("♡")
            self.like_button.setProperty("liked", False)
        
        # Forcer le rafraîchissement du style si disponible, sinon demander un repaint
        style = self.like_button.style()
        if style is not None:
            style.unpolish(self.like_button)
            style.polish(self.like_button)
        else:
            # fallback: force un redessin du widget
            self.like_button.update()
    
    def on_like_clicked(self):
        """Gestionnaire du clic sur le bouton like"""
        if not self.user_manager or not self.user_manager.current_user:
            print("⚠️  Veuillez vous connecter pour liker des films")
            return
        
        user = self.user_manager.current_user
        
        # Toggle le statut de favori
        if user.is_favorite(self.film.system_name):
            user.remove_favorite(self.film.system_name)
            is_now_liked = False
            print(f"💔 {self.film.titre} retiré des favoris de {user.username}")
        else:
            user.add_favorite(self.film.system_name)
            is_now_liked = True
            print(f"❤️  {self.film.titre} ajouté aux favoris de {user.username}")
        
        # Sauvegarder les changements
        self.user_manager.save_users()
        
        # Mettre à jour cette carte
        self.update_like_button_state()
        
        # Émettre le signal pour synchroniser les autres cartes
        self.like_changed.emit(self.film.system_name, is_now_liked)
     
    def on_play_clicked(self):
        """Gestionnaire du clic sur le bouton play"""
        print(f"▶️  Lecture de : {self.film.titre}")
        self.play_clicked.emit(self.film)
    
    def sync_like_state(self, film_id, is_liked):
        """
        Synchronise l'état like avec d'autres cartes
        
        Args:
            film_id: Identifiant du film
            is_liked: Nouvel état du like
        """
        if self.film.system_name == film_id:
            self.update_like_button_state()


def createFilmCard(film, user_manager=None):
    """
    Fonction legacy pour compatibilité avec le code existant
    Crée et retourne une instance de FilmCard
    
    Args:
        film: Instance de Film
        user_manager: Gestionnaire d'utilisateurs (optionnel)
    
    Returns:
        FilmCard: Instance de la carte de film
    """
    return FilmCard(film, user_manager)


def deleteFilmCard(card):
    """
    Fonction legacy pour supprimer une carte
    
    Args:
        card: Instance de FilmCard à supprimer
    """
    card.setParent(None)
    card.deleteLater()
