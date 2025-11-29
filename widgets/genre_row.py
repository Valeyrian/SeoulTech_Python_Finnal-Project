"""
Widget for displaying a row of movies by genre with horizontal scrolling.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
import random

from .card import createFilmCard

class GenreRow(QWidget):
    """
    Widget representing a genre section with horizontal scrolling.
    
    Displays movies organized by genre with Netflix-style horizontal scrolling layout.
    
    Attributes:
        genre_name (str): Name of the genre
        movies (list): List of Movie objects to display
        user_manager: User manager instance for handling user interactions
        cards (list): List of MovieCard widgets in this row
    """
    
    def __init__(self, genre_name, movies, user_manager=None, parent=None):
        """
        Initialize a genre row.
        
        Args:
            genre_name (str): Name of the genre
            movies (list): List of Movie objects to display
            user_manager: User manager instance (optional)
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.genre_name = genre_name
        self.movies = movies
        self.user_manager = user_manager
        self.cards = []  # List to store movie cards
        self.setup_ui()
    
    def get_cards(self):
        """
        Return the list of movie cards in this row.
        
        Returns:
            list: List of MovieCard widgets
        """
        return self.cards
    
    def setup_ui(self):
        """Configure the genre row interface."""
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 8, 16, 4)  # Reduced vertical margins
        main_layout.setSpacing(8)  # Reduced spacing between title and cards
        
        # Header with genre name
        genre_label = QLabel(self.genre_name)
        genre_label.setObjectName("genreHeader")
        main_layout.addWidget(genre_label)
        
        # Scroll area for movie cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("genreScrollArea")
        scroll_area.setMinimumHeight(180)  # Adjusted height for movie cards (160px + margins)
        scroll_area.setMaximumHeight(180)
        
        # Container widget for cards
        cards_container = QWidget()
        cards_container.setObjectName("cardsContainer")
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(12)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Shuffle movies for variety in display order
        shuffled_movies = self.movies.copy()
        random.shuffle(shuffled_movies)
        
        # Add movie cards
        for movie in shuffled_movies:
            card_widget = createFilmCard(movie, self.user_manager)
            self.cards.append(card_widget)
            cards_layout.addWidget(card_widget)
        
        # Add stretch at the end to prevent card stretching
        cards_layout.addStretch()
        
        # Configure the scroll area
        scroll_area.setWidget(cards_container)
        main_layout.addWidget(scroll_area)
        
        # Widget style and size
        self.setObjectName("genreRow")
        self.setMinimumHeight(220)  # Total height: header + scroll area + margins
