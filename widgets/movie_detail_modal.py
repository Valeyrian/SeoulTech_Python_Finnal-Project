"""
Movie detail modal for the Netflux application.
Displays a large overlay with movie details, trailer, and actions.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import os


class MovieDetailModal(QMainWindow):
    """
    Standalone window displaying detailed movie information.
    Netflix-style window with trailer playback and actions.
    """
    
    # Signals
    watchlist_changed = pyqtSignal(str, bool)  # movie_id, is_in_watchlist
    watched_changed = pyqtSignal(str, bool)    # movie_id, is_watched
    like_changed = pyqtSignal(str, bool)       # movie_id, is_liked
    
    def __init__(self, movie, user_manager=None, parent=None):
        """
        Initialize the movie detail window.
        
        Args:
            movie: Movie instance to display
            user_manager: User manager (optional)
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.movie = movie
        self.user_manager = user_manager
        
        # Configure the window
        self.setWindowTitle(f"Netflux - {movie.title}")
        
        # Set size proportional to parent window (80%)
        if parent:
            parent_size = parent.size()
            window_width = 900
            window_height = int(parent_size.height() * 0.8)
            self.resize(window_width, window_height)
            
            # Center the window on parent
            parent_geometry = parent.frameGeometry()
            center_point = parent_geometry.center()
            self.move(center_point.x() - self.width() // 2, 
                     center_point.y() - self.height() // 2)
        else:
            # Default size if no parent
            self.resize(900, 800)
        
        # Set minimum size to prevent too small window
        self.setMinimumSize(900, 700)
        
        # Audio output for sound
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)  # Set volume to 50%
        
        # Media player for trailer
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        
        # Configure looping: restart video when it ends
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        # Setup UI
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Configure the window interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setObjectName("movieDetailModal")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Video player section
        self.create_video_section(content_layout)
        
        # Information section
        self.create_info_section(content_layout)
        
        main_layout.addWidget(self.content_frame)
    
    def create_video_section(self, parent_layout):
        """Create the video player section."""
        video_container = QFrame()
        video_container.setObjectName("videoContainer")
        # Make video height proportional (55% of window height) 
        video_height = max(400, int(self.height() * 0.55))
        video_container.setFixedHeight(video_height)
        
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedHeight(video_height)
        self.media_player.setVideoOutput(self.video_widget)
        video_layout.addWidget(self.video_widget)
        
        parent_layout.addWidget(video_container)
    
    def create_info_section(self, parent_layout):
        """Create the information and actions section."""
        info_container = QFrame()
        info_container.setObjectName("infoSection")
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(30, 25, 30, 15)
        info_layout.setSpacing(8)
        
        # Title and year
        title_layout = QHBoxLayout()
        title_label = QLabel(self.movie.title)
        title_label.setObjectName("modalTitle")
        title_label.setWordWrap(False)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        year_label = QLabel(str(self.movie.year))
        year_label.setObjectName("modalYear")
        title_layout.addWidget(year_label)
        
        info_layout.addLayout(title_layout)
        
        # Metadata (duration, genres)
        metadata_label = QLabel(
            f"{self.movie.minutes}m • {', '.join(self.movie.genres)}"
        )
        metadata_label.setObjectName("modalMetadata")
        info_layout.addWidget(metadata_label)
        
        # Action buttons
        self.create_action_buttons(info_layout)
        
        # Add spacing before synopsis
        info_layout.addSpacing(8)  
        
        # Synopsis
        synopsis_label = QLabel("Synopsis")
        synopsis_label.setObjectName("synopsisTitle")
        info_layout.addWidget(synopsis_label)
        
        synopsis_text = QTextEdit()
        synopsis_text.setObjectName("synopsisText")
        synopsis_text.setReadOnly(True)
        synopsis_text.setPlainText(getattr(self.movie, 'synopsis', 'Aucun synopsis disponible.'))
        synopsis_text.setFixedHeight(40)  
        info_layout.addWidget(synopsis_text)
        
        # Director/Cast with minimal spacing
        if hasattr(self.movie, 'director') and self.movie.director:
            info_layout.addSpacing(2)  
            director_label = QLabel(f"<b>Réalisateur:</b> {self.movie.director}")
            director_label.setObjectName("creditsLabel")
            director_label.setWordWrap(True)
            info_layout.addWidget(director_label)
            
        if hasattr(self.movie, 'cast') and self.movie.cast:
            info_layout.addSpacing(2) 
            cast_label = QLabel(f"<b>Acteurs:</b> {self.movie.cast}")
            cast_label.setObjectName("creditsLabel")
            cast_label.setWordWrap(True)
            info_layout.addWidget(cast_label)
        
        # Add stretch to push content to top
        info_layout.addStretch()
        
        parent_layout.addWidget(info_container)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons (watchlist, watched, like)."""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
       
        # Like button
        self.like_button = QPushButton()
        self.like_button.setObjectName("likeButtonLarge")
        self.like_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_like_button()
        buttons_layout.addWidget(self.like_button)
        
        # Add to watchlist button
        self.watchlist_button = QPushButton()
        self.watchlist_button.setObjectName("watchlistButton")
        self.watchlist_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_watchlist_button()
        buttons_layout.addWidget(self.watchlist_button)
        
        # Mark as watched button
        self.watched_button = QPushButton()
        self.watched_button.setObjectName("watchedButton")
        self.watched_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_watched_button()
        buttons_layout.addWidget(self.watched_button)
        
        buttons_layout.addStretch()
        parent_layout.addLayout(buttons_layout)
    
    def connect_signals(self):
        """Connect button signals."""
        self.like_button.clicked.connect(self.on_like_clicked)
        self.watchlist_button.clicked.connect(self.on_watchlist_clicked)
        self.watched_button.clicked.connect(self.on_watched_clicked)
    
    def update_like_button(self):
        """Update like button state."""
        if self.user_manager and self.user_manager.current_user:
            is_liked = self.user_manager.current_user.is_favorite(self.movie.system_name)
            self.like_button.setText("♥ Liked" if is_liked else "♡ Like")
            self.like_button.setProperty("liked", is_liked)
            # Force style refresh
            self.like_button.style().unpolish(self.like_button)
            self.like_button.style().polish(self.like_button)
        else:
            self.like_button.setText("♡ Like")
            self.like_button.setProperty("liked", False)
            # Force style refresh
            self.like_button.style().unpolish(self.like_button)
            self.like_button.style().polish(self.like_button)
    
    def update_watchlist_button(self):
        """Update watchlist button state."""
        if self.user_manager and self.user_manager.current_user:
            is_in_watchlist = self.user_manager.current_user.is_in_watchlist(self.movie.system_name)
            self.watchlist_button.setText("✓ In my WatchList" if is_in_watchlist else "➕ WatchList")
            self.watchlist_button.setProperty("in_watchlist", is_in_watchlist)
            # Force style refresh
            self.watchlist_button.style().unpolish(self.watchlist_button)
            self.watchlist_button.style().polish(self.watchlist_button)
        else:
            self.watchlist_button.setText("➕ WatchList")
            self.watchlist_button.setProperty("in_watchlist", False)
            # Force style refresh
            self.watchlist_button.style().unpolish(self.watchlist_button)
            self.watchlist_button.style().polish(self.watchlist_button)
    
    def update_watched_button(self):
        """Update watched button state."""
        if self.user_manager and self.user_manager.current_user:
            is_watched = self.user_manager.current_user.is_watched(self.movie.system_name)
            self.watched_button.setText("✓ Seen" if is_watched else "Mark as seen")
            self.watched_button.setProperty("watched", is_watched)
            # Force style refresh
            self.watched_button.style().unpolish(self.watched_button)
            self.watched_button.style().polish(self.watched_button)
        else:
            self.watched_button.setText("Mark as seen")
            self.watched_button.setProperty("watched", False)
            # Force style refresh
            self.watched_button.style().unpolish(self.watched_button)
            self.watched_button.style().polish(self.watched_button)
    
    def on_like_clicked(self):
        """Handle like button click."""
        if not self.user_manager or not self.user_manager.current_user:
            print("Please log in to like movies")
            return
        
        user = self.user_manager.current_user
        is_liked = not user.is_favorite(self.movie.system_name)
        
        if is_liked:
            user.add_favorite(self.movie.system_name)
        else:
            user.remove_favorite(self.movie.system_name)
        
        self.user_manager.save_users()
        self.update_like_button()
        self.like_changed.emit(self.movie.system_name, is_liked)
    
    def on_watchlist_clicked(self):
        """Handle watchlist button click."""
        if not self.user_manager or not self.user_manager.current_user:
            print("Please log in to manage your watchlist")
            return
        
        user = self.user_manager.current_user
        is_in_watchlist = not user.is_in_watchlist(self.movie.system_name)
        
        if is_in_watchlist:
            user.add_to_watchlist(self.movie.system_name)
        else:
            user.remove_from_watchlist(self.movie.system_name)
        
        self.user_manager.save_users()
        self.update_watchlist_button()
        self.watchlist_changed.emit(self.movie.system_name, is_in_watchlist)
    
    def on_watched_clicked(self):
        """Handle watched button click."""
        if not self.user_manager or not self.user_manager.current_user:
            print("Please log in to mark as watched")
            return
        
        user = self.user_manager.current_user
        is_watched = not user.is_watched(self.movie.system_name)
        
        # Track if watchlist state changed
        was_in_watchlist = user.is_in_watchlist(self.movie.system_name)
        
        if is_watched:
            # Mark as watched
            user.mark_as_watched(self.movie.system_name)
            
            # If marking as watched and in watchlist, remove from watchlist
            if was_in_watchlist:
                user.remove_from_watchlist(self.movie.system_name)
                print(f"Automatically removed '{self.movie.title}' from watchlist")
                
                # Force update of watchlist button
                self.update_watchlist_button()
                
                # Emit watchlist changed signal
                self.watchlist_changed.emit(self.movie.system_name, False)
        else:
            # Unmark as watched
            user.unmark_as_watched(self.movie.system_name)
        
        # Save changes
        self.user_manager.save_users()
        
        # Update watched button
        self.update_watched_button()
        
        # Emit watched changed signal
        self.watched_changed.emit(self.movie.system_name, is_watched)
    
    def load_trailer(self):
        """Load and play the movie trailer with sound."""
        trailer_path = self.movie.video_path
        
        # Check if the trailer exists, otherwise use fallback video
        if trailer_path and os.path.exists(trailer_path):
            self.media_player.setSource(QUrl.fromLocalFile(os.path.abspath(trailer_path)))
            self.media_player.play()
        else:
            # Use fallback video for missing trailers
            fallback_path = "./assets/video_not_found.mp4"
            if os.path.exists(fallback_path):
                self.media_player.setSource(QUrl.fromLocalFile(os.path.abspath(fallback_path)))
                self.media_player.play()
                print(f"No trailer available for {self.movie.title}, using fallback video")
            else:
                print("Fallback video not found. Cannot play trailer.")
    
    def set_volume(self, volume):
        """
        Set the audio volume.
        
        Args:
            volume (float): Volume level between 0.0 (mute) and 1.0 (max)
        """
        self.audio_output.setVolume(max(0.0, min(1.0, volume)))
    
    def toggle_mute(self):
        """Toggle audio mute."""
        self.audio_output.setMuted(not self.audio_output.isMuted())
    
    def on_media_status_changed(self, status):
        """Handle media status changes to implement looping."""
        from PyQt6.QtMultimedia import QMediaPlayer
        
        # When video reaches the end, restart it
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()
    
    def showEvent(self, event):
        """Override showEvent to start trailer playback."""
        super().showEvent(event)
        self.load_trailer()
    
    def closeEvent(self, event):
        """Override closeEvent to stop media playback."""
        self.media_player.stop()
        super().closeEvent(event)
    
    def sync_watchlist_state(self, movie_id, is_in_watchlist):
        """
        Synchronize watchlist button state when changed from elsewhere.
        
        Args:
            movie_id: Movie identifier
            is_in_watchlist: New watchlist state
        """
        if self.movie.system_name == movie_id:
            self.update_watchlist_button()

    def sync_watched_state(self, movie_id, is_watched):
        """
        Synchronize watched button state when changed from elsewhere.
        
        Args:
            movie_id: Movie identifier
            is_watched: New watched state
        """
        if self.movie.system_name == movie_id:
            self.update_watched_button()