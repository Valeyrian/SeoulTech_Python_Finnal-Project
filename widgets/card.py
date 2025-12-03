"""
Movie card widget for the Netflux application.
Displays a movie with its image, title, genres, and interaction buttons.
"""
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
import os

class FilmCard(QFrame):
    """
    Widget representing an interactive movie card.
    Cinema poster style: vertical format (2:3 ratio) like movie posters.
    """
    
    # Signal emitted when the like status changes (movie_id, is_liked)
    like_changed = pyqtSignal(str, bool)
    # Signal emitted when the play button is clicked
    play_clicked = pyqtSignal(object)
    
    def __init__(self, movie, user_manager=None, parent=None):
        """
        Initialize a movie card.
        
        Args:
            movie: Movie instance to display
            user_manager: User manager (optional)
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.movie = movie
        self.user_manager = user_manager
        
        # Widget configuration - Cinema poster format (2:3 ratio)
        # Width: 200px, Height: 300px (poster) + 1000px (info) = 400 total
        self.setMinimumSize(200, 400)
        self.setMaximumSize(200, 400)
        self.setObjectName("movieCard")
        self.setProperty("class", "movie-card")
        
        # Create the interface
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
    
    def setup_ui(self):
        """Configure the card interface."""
        # Main vertical layout: image on top, info at bottom
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Container for the image (poster)
        self.create_image_container(main_layout)
        
        # Container for the info at bottom
        self.create_info_container(main_layout)
    
    def create_image_container(self, parent_layout):
        """Create the container for the movie image (poster format)."""
        image_container = QFrame()
        image_container.setObjectName("imageContainer")
        # Poster format: 200x300 (2:3 ratio)
        image_container.setMinimumSize(200, 300)
        image_container.setMaximumSize(200, 300)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)

        # Load the image
        if not os.path.exists(self.movie.tile_path):
            pixmap = QPixmap("./assets/image_not_found.jpeg")
        else:
            pixmap = QPixmap(self.movie.tile_path)

        image_label = QLabel()
        image_label.setPixmap(
            pixmap.scaled(200, 300, 
                         Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                         Qt.TransformationMode.SmoothTransformation)
        )
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setObjectName("movieImage")
        image_layout.addWidget(image_label)
        
        parent_layout.addWidget(image_container)
    
    def create_info_container(self, parent_layout):
        """Create the container for information and buttons."""
        info_container = QFrame()
        info_container.setObjectName("infoContainer")
        info_container.setMinimumHeight(100)
        info_container.setMaximumHeight(100)
        
        main_info_layout = QVBoxLayout(info_container)
        main_info_layout.setContentsMargins(10, 8, 10, 8)
        main_info_layout.setSpacing(6)
        
        # Text section (title + genre/duration)
        self.create_text_section(main_info_layout)
        
        # Add small spacing before buttons
        main_info_layout.addSpacing(4)
        
        # Buttons (like + play) at bottom
        self.create_action_buttons(main_info_layout)
        
        parent_layout.addWidget(info_container)
    
    def create_text_section(self, parent_layout):
        """Create the text section (title and metadata)."""
        # Title on single line with ellipsis if too long
        title_label = QLabel()
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setObjectName("movieTitle")
        title_label.setMaximumWidth(180)
        title_label.setWordWrap(False)  # Single line only
        
        # Use elided text for automatic ellipsis
        font_metrics = QFontMetrics(title_label.font())
        elided_title = font_metrics.elidedText(
            self.movie.title, 
            Qt.TextElideMode.ElideRight, 
            180
        )
        title_label.setText(elided_title)
        
        parent_layout.addWidget(title_label)

        # Genre and duration
        genre_text = ', '.join(self.movie.genres[:2])
        if len(self.movie.genres) > 2:
            genre_text += '...'
        
        genre_duration_label = QLabel(f"{genre_text} • {self.movie.minutes}m")
        genre_duration_label.setObjectName("genreDurationLabel")
        genre_duration_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        genre_duration_label.setWordWrap(False)
        genre_duration_label.setMaximumWidth(180)
        parent_layout.addWidget(genre_duration_label)
    
    def create_action_buttons(self, parent_layout):
        """Create the action buttons (like and play) horizontally."""
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)
        
        # Like button (heart)
        self.like_button = QPushButton("♡")
        self.like_button.setObjectName("likeButton")
        self.like_button.setProperty("movie_id", self.movie.system_name)
        self.like_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.like_button.setMinimumSize(32, 28)
        self.like_button.setMaximumSize(32, 28)
        
        # Update the like button state
        self.update_like_button_state()
        
        buttons_layout.addWidget(self.like_button)

        # Play button
        self.play_button = QPushButton("➕")
        self.play_button.setObjectName("playButtonMini")
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setMinimumSize(28, 28)
        self.play_button.setMaximumSize(32, 28)
        
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addStretch()
        
        parent_layout.addLayout(buttons_layout)
    
    def connect_signals(self):
        """Connect button signals."""
        self.like_button.clicked.connect(self.on_like_clicked)
        self.play_button.clicked.connect(self.on_play_clicked)
    
    def update_like_button_state(self):
        """Update the like button appearance based on state."""
        if self.user_manager and self.user_manager.current_user:
            is_liked = self.user_manager.current_user.is_favorite(self.movie.system_name)
            self.like_button.setText("♥" if is_liked else "♡")
            self.like_button.setProperty("liked", is_liked)
        else:
            self.like_button.setText("♡")
            self.like_button.setProperty("liked", False)
        
        # Force style refresh if available, otherwise request repaint
        style = self.like_button.style()
        if style is not None:
            style.unpolish(self.like_button)
            style.polish(self.like_button)
        else:
            # Fallback: force a widget repaint
            self.like_button.update()
    
    def on_like_clicked(self):
        """Handler for the like button click."""
        if not self.user_manager or not self.user_manager.current_user:
            print("Warning: Please log in to like movies")
            return
        
        user = self.user_manager.current_user
        
        # Toggle favorite status
        if user.is_favorite(self.movie.system_name):
            user.remove_favorite(self.movie.system_name)
            is_now_liked = False
            print(f"Removed '{self.movie.title}' from {user.username}'s favorites")
        else:
            user.add_favorite(self.movie.system_name)
            is_now_liked = True
            print(f"Added '{self.movie.title}' to {user.username}'s favorites")
        
        # Save changes
        self.user_manager.save_users()
        
        # Update this card
        self.update_like_button_state()
        
        # Emit signal to synchronize other cards
        self.like_changed.emit(self.movie.system_name, is_now_liked)
     
    def on_play_clicked(self):
        """Handler for the play button click."""
        print(f"Opening details for: {self.movie.title}")
        self.play_clicked.emit(self.movie)
    
    def sync_like_state(self, movie_id, is_liked):
        """
        Synchronize like state with other cards.
        
        Args:
            movie_id: Movie identifier
            is_liked: New like state
        """
        if self.movie.system_name == movie_id:
            self.update_like_button_state()

def createFilmCard(movie, user_manager=None):
    """
    Creates and returns a FilmCard instance.
    
    Args:
        movie: Movie instance
        user_manager: User manager (optional)
    
    Returns:
        FilmCard: Movie card instance
    """
    return FilmCard(movie, user_manager)
