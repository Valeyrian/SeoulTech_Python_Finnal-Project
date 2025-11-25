from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
import os

class player(QFrame):
    """
    Class for creating and managing media player instances
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mediaPlayer = None

    def startMediaPlayer(self, movie):
        self.mediaPlayer = QMediaPlayer(self)
        audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(audioOutput)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)

        if (not os.path.exists(movie.video)):
            path = QUrl.fromLocalFile("./data/movies_videos/video_not_found.mp4")
        else:
            path = QUrl.fromLocalFile(movie.video)

        self.mediaPlayer.setSource(path)
        self.mediaPlayer.play()

