import sys
from gomoku_lib import Gomoku
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize

game_window = uic.loadUiType("./gameWindow.ui")[0]

class Game(QMainWindow):
    
    def __init__(self, parent):
        super(Game, self).__init__(parent)
        game_window = "gameWindow.ui"
        uic.loadUi(game_window, self)
        oImage = QImage('./images/board.png')
        bImage = oImage.scaled(QSize(800, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(bImage))
        self.setPalette(palette)
        self.show()
        