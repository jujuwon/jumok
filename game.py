import sys
from gomoku_lib import Gomoku
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize

# game_window = uic.loadUiType("./gameWindow.ui")[0]

class Game(QMainWindow):

    def __init__(self, parent):
        super(Game, self).__init__(parent)

        game_window = "gameWindow.ui"
        uic.loadUi(game_window, self)
        
        # for test
        self.ip = "localhost"
        self.port = "1234"
        
        pixmap = QPixmap()
        pixmap.load('./images/board.png')
        pixmap = pixmap.scaledToWidth(800)
        pixmap = pixmap.scaledToHeight(800)
        self.boardLabel.setPixmap(pixmap)
        parent.command.connect(self.recvData)
        #self.label_test.clicked.connect(self.label_test_clicked)

        self.show()
        
    # def label_test_clicked(self):
    #     self.label_test.setText("Test")

    @QtCore.pyqtSlot(str, str)
    def recvData(self, ip, port):
        self.ip = ip
        self.port = port
        self.addrLabel.setText(f'{ip} : {port}')
        self.connectSocket()

    def connectSocket(self):
        print("start connect")
        self.gomoku = Gomoku(self.ip, int(self.port), True)
        ret = self.gomoku.connect()
        print(ret)
        if ret: # success connect
            self.statusLabel.setText("Success Connection\nwaiting for game to start")
            # self.gomoku.ready()
            # self.run()
        else:   # fail connect
            print("failed connection")

    def run(self):
        ret_tuple = self.gomoku.update_or_end() # update 또는 end 신호를 수신하는 메소드
        success, command, turn, data = ret_tuple    # bool, int, int, bytes 형태, 맨 첫 변수는 성공 실패 유무
        if command == 2: # update 명령
            pass
        if command == 4: # end 명령
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())