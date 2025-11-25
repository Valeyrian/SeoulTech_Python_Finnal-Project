"""
Widget for displaying a row of movies by genre with horizontal scrolling.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt
import card


class GenreRow(QWidget):
    """Widget representing a genre section with horizontal scrolling."""
    
    def __init__(self, genre_name, films, user_manager=None, parent=None):
        super().__init__(parent)
        self.genre_name = genre_name
        self.films = films
        self.user_manager = user_manager
        self.cards = []  # List to store cards
        self.setup_ui()
    
    def get_cards(self):
        """Return the list of cards in this row."""
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
        scroll_area.setMinimumHeight(180)  # Adjusted height for new cards (160px + margins)
        scroll_area.setMaximumHeight(180)
        
        # Container widget for cards
        cards_container = QWidget()
        cards_container.setObjectName("cardsContainer")
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(12)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Add movie cards
        for film in self.films:
            card_widget = card.createFilmCard(film, self.user_manager)
            self.cards.append(card_widget)  # Register the card
            cards_layout.addWidget(card_widget)
        
        # Add stretch at the end to prevent card stretching
        cards_layout.addStretch()
        
        # Configure the scroll area
        scroll_area.setWidget(cards_container)
        main_layout.addWidget(scroll_area)
        
        # Widget style and size
        self.setObjectName("genreRow")
        self.setMinimumHeight(220)  # Reduced total height: header + scroll area + margins
