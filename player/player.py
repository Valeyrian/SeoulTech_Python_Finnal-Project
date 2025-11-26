"""
Media player module for the Netflux application.
Handles video playback functionality.
"""
from PyQt6.QtWidgets import QFrame
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
import os


class Player(QFrame):
    """
    Class for creating and managing media player instances.
    
    Provides video playback functionality for movies.
    
    Attributes:
        media_player (QMediaPlayer): The media player instance
    """
    
    def __init__(self, parent=None):
        """
        Initialize the player.
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.media_player = None

    def start_media_player(self, movie):
        """
        Start playing a movie.
        
        Args:
            movie: Movie instance to play
        """
        self.media_player = QMediaPlayer(self)
        audio_output = QAudioOutput()
        self.media_player.setAudioOutput(audio_output)
        video_widget = QVideoWidget()
        self.media_player.setVideoOutput(video_widget)

        # Check if video file exists
        if not os.path.exists(movie.video):
            path = QUrl.fromLocalFile("./data/movies_videos/video_not_found.mp4")
        else:
            path = QUrl.fromLocalFile(movie.video)

        self.media_player.setSource(path)
        self.media_player.play()


