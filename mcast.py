# coding=utf-8

import os
import sys
import glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget


class BackWindow(QWidget):
    def __init__(self, parent=None):
        super(BackWindow, self).__init__(parent)

        self.init_ui()

        self.w = None

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.main_mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.main_mediaPlayer.positionChanged.connect(self.positionChanged)
        self.main_mediaPlayer.durationChanged.connect(self.durationChanged)
        self.main_mediaPlayer.error.connect(self.handleError)

        self._playlist = QMediaPlaylist()
        #self.addMedia("movie/movie1.wmv")

        self.init_play_list()

        self._stopped = True
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)


        self.mediaPlayer.setPlaylist(self._playlist)
        self.main_mediaPlayer.setPlaylist(self._playlist)

    def init_ui(self):
        ui_path = "ui/MediaPlayer.ui"
        print ui_path
        self.ui = loadUi(ui_path, self)

        self.ui.playButton.clicked.connect(self.play_movie)
        self.ui.nextButton.clicked.connect(self.next_movie)
        self.ui.launchButton.clicked.connect(self.launch_window)

        self.ui.positionSlider.setRange(0, 0)
        self.ui.positionSlider.sliderMoved.connect(self.setPosition)


    def init_play_list(self):
        movies = glob.glob(os.path.dirname("__file__") +  "movie/*")

        #sort movies

        for movie in movies:
            self.addMedia(movie)

            self.ui.listWidget.addItem(movie)

    # プレイリストに動画を追加
    def addMedia(self, media_file):
        media_content = QMediaContent(QUrl.fromLocalFile(media_file))
        self._playlist.addMedia(media_content)

    """   def mousePressEvent(self, event):
        if self._stopped:
            self.play()
        else:
            self.mediaPlayer.pause()
            self._stopped = True
    """

    def play_movie(self):
        if self._stopped:
            # self.mediaPlayer.setVideoOutput(self.ui.videoWidget)
            # self.mediaPlayer.setPlaylist(self._playlist)
            self.mediaPlayer.play()
            self.main_mediaPlayer.play()
            self._stopped = False
            self.ui.playButton.setText("pause")
        else:
            self.mediaPlayer.pause()
            self.main_mediaPlayer.pause()

            self._stopped = True
            self.ui.playButton.setText("play")

    def next_movie(self):
        self._playlist.next()

    def back_movie(self):
        pass

    def launch_window(self):
        print "aaaaaaaaa"
        self.w = MainWindow()
        #self.w.show()

        self.main_mediaPlayer.setVideoOutput(self.w.ui.videoWidget)

    def positionChanged(self, position):
        self.ui.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.ui.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.main_mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.button = QPushButton("test", self)

        self.ui = QWidget(parent)
        #self.ui.button = QPushButton("test", self)
        self.ui.videoWidget = QVideoWidget()
        layout = QHBoxLayout(self)
        layout.addWidget(self.ui.videoWidget)
        self.ui.setLayout(layout)

        self.ui.show()


        #self.setCentralWidget(self.button)

        #self.show()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackWindow()
    window.show()

    sys.exit(app.exec_())
