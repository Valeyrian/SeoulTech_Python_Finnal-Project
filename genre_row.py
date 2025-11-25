"""
Widget pour afficher une rangée de films par genre avec scroll horizontal
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
import card


class GenreRow(QWidget):
    """Widget représentant une section de genre avec scroll horizontal"""
    
    def __init__(self, genre_name, films, user_manager=None, parent=None):
        super().__init__(parent)
        self.genre_name = genre_name
        self.films = films
        self.user_manager = user_manager
        self.cards = []  # Liste pour stocker les cartes
        self.setup_ui()
    
    def get_cards(self):
        """Retourne la liste des cartes de cette rangée"""
        return self.cards
    
    def setup_ui(self):
        """Configure l'interface de la rangée de genre"""
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 8, 16, 4)  # Réduction des marges verticales
        main_layout.setSpacing(8)  # Réduction de l'espacement entre titre et cartes
        
        # Header avec le nom du genre
        genre_label = QLabel(self.genre_name)
        genre_label.setObjectName("genreHeader")
        main_layout.addWidget(genre_label)
        
        # Scroll Area pour les cartes de films
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("genreScrollArea")
        scroll_area.setMinimumHeight(180)  # Hauteur ajustée pour nouvelles cartes (160px + marges)
        scroll_area.setMaximumHeight(180)
        
        # Widget conteneur pour les cartes
        cards_container = QWidget()
        cards_container.setObjectName("cardsContainer")
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(12)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Ajouter les cartes de films
        for film in self.films:
            card_widget = card.createFilmCard(film, self.user_manager)
            self.cards.append(card_widget)  # Enregistrer la carte
            cards_layout.addWidget(card_widget)
        
        # Ajouter un stretch à la fin pour éviter l'étirement des cartes
        cards_layout.addStretch()
        
        # Configurer le scroll area
        scroll_area.setWidget(cards_container)
        main_layout.addWidget(scroll_area)
        
        # Style du widget et taille
        self.setObjectName("genreRow")
        self.setMinimumHeight(220)  # Hauteur totale réduite : header + scroll area + marges
