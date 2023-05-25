import sys
import os
import time
from pytube import YouTube
import youtube_dl
import pafy
import vlc
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QFileDialog, QSizePolicy, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl, QRect, QSize, pyqtSignal, QTimer

class MediaTab(QWidget):
    def __init__(self):
        super().__init__()

        self.media_list = []
        self.media_index = 0
        self.player = None
        self.is_playing = False
        
        self.setup_ui()

    def setup_ui(self):
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create video player widget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        # Options layout
        options_layout = QHBoxLayout()
        layout.addLayout(options_layout)

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        options_layout.addWidget(self.url_input)

        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_youtube_video)
        options_layout.addWidget(self.play_button)

        # Pause button
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_youtube_video)
        options_layout.addWidget(self.pause_button)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_youtube_video)
        options_layout.addWidget(self.stop_button)

        # Volume slider
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)
        options_layout.addWidget(self.volume_slider)

        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_youtube_video)
        options_layout.addWidget(self.download_button)

        # Create an instance of VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_fullscreen(True)
        self.player.set_xwindow(self.video_widget.winId())

    def play_youtube_video(self):
        url = self.url_input.text()
        video = pafy.new(url)
        best = video.getbest()
        self.player.set_media(self.instance.media_new(best.url))
        self.player.play()

    def pause_youtube_video(self):
        self.player.pause()

    def stop_youtube_video(self):
        self.player.stop()

    def download_youtube_video(self):
        url = self.url_input.text()
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download("gui\utils\Prep\you_tube")  
            print("Video downloaded successfully")
        except Exception as e:
            print(f"Error downloading video: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    media_tab_instance = MediaTab()

    # Replace the URL below with a valid YouTube video URL
    valid_url = "https://www.youtube.com/watch?v=S0_IZIOqKhU"
    media_tab_instance.add_youtube_video(valid_url)

    main_window.setCentralWidget(media_tab_instance)
    main_window.setWindowTitle("Media Tab")
    main_window.resize(800, 600)
    main_window.show()
    sys.exit(app.exec_())
