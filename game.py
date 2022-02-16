import sys
from gomoku_lib import Gomoku
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import time
from jconst import *
from player import ChoiceOfPlayer
from board import Board

CMD_CONNECT = 0
CMD_READY = 1
CMD_UPDATE = 2
CMD_PUT = 3
CMD_END = 4

TIME_STOP = 0
TIME_START = 1

PERSON = 0
AI = 1

BLANK = 0
BLACK = 1
WHITE = 2

# game_window = uic.loadUiType("./gameWindow.ui")[0]

def clickable(widget):
    
        class Filter(QObject):
        
            clicked = pyqtSignal()
            
            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True
                
                return False
        
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

class Game(QMainWindow):

    gomoku_map = Board()

    MY_COLOR = BLACK
    OTHER_COLOR = WHITE
    READY = False
    INIT = True
    GAME_DONE = False
    TIME_DONE = False
    FIRST = True
    
    render_signal = QtCore.pyqtSignal(int, int, int)
    ai_render_signal = QtCore.pyqtSignal(int, int)
    end_signal = QtCore.pyqtSignal(str)
    time_signal = QtCore.pyqtSignal(int)
    other_render_signal = QtCore.pyqtSignal(int, int)

    def __init__(self, parent):
        super(Game, self).__init__(parent)

        game_window = "gameWindow.ui"
        uic.loadUi(game_window, self)
        
        # for test
        self.ip = "localhost"
        self.port = "1234"
        self.is_black_do = True
        self.step = 0
        
        # 오목판 세팅
        pixmapBoard = QPixmap()
        pixmapBoard.load('./images/board.png')
        pixmapBoard = pixmapBoard.scaledToWidth(800)
        pixmapBoard = pixmapBoard.scaledToHeight(800)
        self.boardLabel.setPixmap(pixmapBoard)
        
        # 검은 돌 아이콘 세팅
        self.pixmapBlack = QPixmap()
        self.pixmapBlack.load('./images/black.png')
        self.pixmapBlack = self.pixmapBlack.scaledToWidth(45)
        self.pixmapBlack = self.pixmapBlack.scaledToHeight(45)
        self.blackIcon.setPixmap(self.pixmapBlack)
        # 하얀 돌 아이콘 세팅
        self.pixmapWhite = QPixmap()
        self.pixmapWhite.load('./images/white.png')
        self.pixmapWhite = self.pixmapWhite.scaledToWidth(45)
        self.pixmapWhite = self.pixmapWhite.scaledToHeight(45)
        self.whiteIcon.setPixmap(self.pixmapWhite)
        # 직전 검은 돌 아이콘 세팅
        self.pixmapBlackLast = QPixmap()
        self.pixmapBlackLast.load('./images/black_last.png')
        self.pixmapBlackLast = self.pixmapBlackLast.scaledToWidth(45)
        self.pixmapBlackLast = self.pixmapBlackLast.scaledToHeight(45)

        # 직전 하얀 돌 아이콘 세팅
        self.pixmapWhiteLast = QPixmap()
        self.pixmapWhiteLast.load('./images/white_last.png')
        self.pixmapWhiteLast = self.pixmapWhiteLast.scaledToWidth(45)
        self.pixmapWhiteLast = self.pixmapWhiteLast.scaledToHeight(45)
        
        # 보드판 격자 label 세팅
        self.mapLabel = [[self.map_0_0, self.map_0_1, self.map_0_2, self.map_0_3, self.map_0_4, self.map_0_5, self.map_0_6, self.map_0_7, self.map_0_8, self.map_0_9, self.map_0_10, self.map_0_11, self.map_0_12, self.map_0_13, self.map_0_14],
                         [self.map_1_0, self.map_1_1, self.map_1_2, self.map_1_3, self.map_1_4, self.map_1_5, self.map_1_6, self.map_1_7, self.map_1_8, self.map_1_9, self.map_1_10, self.map_1_11, self.map_1_12, self.map_1_13, self.map_1_14],
                         [self.map_2_0, self.map_2_1, self.map_2_2, self.map_2_3, self.map_2_4, self.map_2_5, self.map_2_6, self.map_2_7, self.map_2_8, self.map_2_9, self.map_2_10, self.map_2_11, self.map_2_12, self.map_2_13, self.map_2_14],
                         [self.map_3_0, self.map_3_1, self.map_3_2, self.map_3_3, self.map_3_4, self.map_3_5, self.map_3_6, self.map_3_7, self.map_3_8, self.map_3_9, self.map_3_10, self.map_3_11, self.map_3_12, self.map_3_13, self.map_3_14],
                         [self.map_4_0, self.map_4_1, self.map_4_2, self.map_4_3, self.map_4_4, self.map_4_5, self.map_4_6, self.map_4_7, self.map_4_8, self.map_4_9, self.map_4_10, self.map_4_11, self.map_4_12, self.map_4_13, self.map_4_14],
                         [self.map_5_0, self.map_5_1, self.map_5_2, self.map_5_3, self.map_5_4, self.map_5_5, self.map_5_6, self.map_5_7, self.map_5_8, self.map_5_9, self.map_5_10, self.map_5_11, self.map_5_12, self.map_5_13, self.map_5_14],
                         [self.map_6_0, self.map_6_1, self.map_6_2, self.map_6_3, self.map_6_4, self.map_6_5, self.map_6_6, self.map_6_7, self.map_6_8, self.map_6_9, self.map_6_10, self.map_6_11, self.map_6_12, self.map_6_13, self.map_6_14],
                         [self.map_7_0, self.map_7_1, self.map_7_2, self.map_7_3, self.map_7_4, self.map_7_5, self.map_7_6, self.map_7_7, self.map_7_8, self.map_7_9, self.map_7_10, self.map_7_11, self.map_7_12, self.map_7_13, self.map_7_14],
                         [self.map_8_0, self.map_8_1, self.map_8_2, self.map_8_3, self.map_8_4, self.map_8_5, self.map_8_6, self.map_8_7, self.map_8_8, self.map_8_9, self.map_8_10, self.map_8_11, self.map_8_12, self.map_8_13, self.map_8_14],
                         [self.map_9_0, self.map_9_1, self.map_9_2, self.map_9_3, self.map_9_4, self.map_9_5, self.map_9_6, self.map_9_7, self.map_9_8, self.map_9_9, self.map_9_10, self.map_9_11, self.map_9_12, self.map_9_13, self.map_9_14],
                         [self.map_10_0, self.map_10_1, self.map_10_2, self.map_10_3, self.map_10_4, self.map_10_5, self.map_10_6, self.map_10_7, self.map_10_8, self.map_10_9, self.map_10_10, self.map_10_11, self.map_10_12, self.map_10_13, self.map_10_14],
                         [self.map_11_0, self.map_11_1, self.map_11_2, self.map_11_3, self.map_11_4, self.map_11_5, self.map_11_6, self.map_11_7, self.map_11_8, self.map_11_9, self.map_11_10, self.map_11_11, self.map_11_12, self.map_11_13, self.map_11_14],
                         [self.map_12_0, self.map_12_1, self.map_12_2, self.map_12_3, self.map_12_4, self.map_12_5, self.map_12_6, self.map_12_7, self.map_12_8, self.map_12_9, self.map_12_10, self.map_12_11, self.map_12_12, self.map_12_13, self.map_12_14],
                         [self.map_13_0, self.map_13_1, self.map_13_2, self.map_13_3, self.map_13_4, self.map_13_5, self.map_13_6, self.map_13_7, self.map_13_8, self.map_13_9, self.map_13_10, self.map_13_11, self.map_13_12, self.map_13_13, self.map_13_14],
                         [self.map_14_0, self.map_14_1, self.map_14_2, self.map_14_3, self.map_14_4, self.map_14_5, self.map_14_6, self.map_14_7, self.map_14_8, self.map_14_9, self.map_14_10, self.map_14_11, self.map_14_12, self.map_14_13, self.map_14_14]]

        # 보드판 격자 클릭 signal 세팅
        for i in range(15):
            for j in range(15):
                clickable(self.mapLabel[i][j]).connect(lambda x = i, y = j :  self.map_clicked(x, y))
            
        
        # signal/slot
        parent.multi.connect(self.multiPlaySlot)
        parent.single.connect(self.singlePlaySlot)
        self.btnReady.clicked.connect(self.btnReady_clicked)
        self.render_signal.connect(self.reader_slot)
        self.end_signal.connect(self.end_slot)
        self.time_signal.connect(self.timer_slot)
        self.personRb.clicked.connect(self.selectRadioSlot)
        self.aiRb.clicked.connect(self.selectRadioSlot)
        self.other_render_signal.connect(self.recvOtherPut)
        # self.ai_render_signal.connect(self.map_clicked)
        #self.label_test.clicked.connect(self.label_test_clicked)
        
        # 쓰레드
        self.network = threading.Thread(target=self.networkThread)
        self.timer = threading.Thread(target=self.timerThread)
        self.show()
        
    # 라디오버튼 클릭 slot
    def selectRadioSlot(self):
        if self.personRb.isChecked():
            self.player_type = PERSON
        else:
            self.player_type = AI
        
    # 싱글플레이 slot
    @QtCore.pyqtSlot(int)
    def singlePlaySlot(self, order):
        print("order : ", order)
        stone = ""
        if order == 0:
            self.order = BLACK
            stone = "BLACK"
        else:
            self.order = WHITE
            stone = "WHITE"
        self.addrLabel.setText(f'[Single Play]')
        if order == 0:
            pass
            #self.colorLabel.setText(f'BLACK : YOU     WHITE : AI')
        else:
            pass
            #self.colorLabel.setText(f'WHITE : YOU     BLACK : AI')
        
    # 멀티플레이 slot
    @QtCore.pyqtSlot(str, str, str)
    def multiPlaySlot(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.addrLabel.setText(f'{ip} : {port}')
        self.connectSocket()

    # gomoku 서버 첫 연결 
    def connectSocket(self):
        self.statusLabel.setText("연결 중")
        self.gomoku = Gomoku(self.ip, int(self.port), False)
        ret = self.gomoku.connect()
                    
        if ret: # success connect
            self.statusLabel.setText("연결 성공")
        else:   # fail connect
            self.statusLabel.setText("연결 패킷 전송실패")
            
    # 준비 버튼 클릭 slot
    def btnReady_clicked(self):
        if self.READY:
            ret = self.gomoku.ready(True) # 준비 취소
            if ret:
                self.statusLabel.setText("준비 취소")
                self.READY = False
            else:
                self.statusLabel.setText("준비 취소 패킷 전송실패")
        else:
            ret = self.gomoku.ready() # 준비
            if ret:
                self.statusLabel.setText("준비완료\n게임시작을 기다리는 중")
                self.READY = True
                # 쓰레드 시작
                self.network.start()
            else:
                self.statusLabel.setText("준비 패킷 전송실패")
        
    # 사용자 돌 클릭 slot
    def map_clicked(self, i, j):
        print("내가 둔 수 : ", i, j)
        x = i + 1
        y = j + 1
        self.gomoku.put(x, y)
        # 사용자가 흑돌이면
        if self.MY_COLOR == BLACK:
            #self.gomoku_map.draw_xy(x, y, BLACK)
            self.gomoku_map.draw_xy(x, y, BLACK)
            self.render_signal.emit(x, y, BLACK)
        # 사용자가 백돌이면
        else:
            #self.gomoku_map.draw_xy(x, y, WHITE)
            self.gomoku_map.draw_xy(x, y, WHITE)
            self.render_signal.emit(x, y, WHITE)

    def recvOtherPut(self, x, y):
        self.otherX = x
        self.otherY = y
        self.Going = False
    
    # 렌더링 slot
    @QtCore.pyqtSlot(int, int, int)
    def reader_slot(self, x, y, color):
        if self.FIRST:
            if color == BLACK: # 검은돌 그리기  
                # self.gomoku_map.draw_xy(x, y, BLACK)
                self.mapLabel[x][y].setPixmap(self.pixmapBlackLast)
                # self.is_black_do = False
            else: # 하얀돌 그리기
                # self.gomoku_map.draw_xy(x, y, WHITE)
                self.mapLabel[x][y].setPixmap(self.pixmapWhiteLast)
                # self.is_black_do = True
            # 직전 돌 저장
            self.beforeX, self.beforeY = x, y
            self.FIRST = False
        else:
            if color == BLACK: # 검은돌
                # 직전 하얀 돌 last -> 그냥 하얀돌로
                self.mapLabel[self.beforeX][self.beforeY].setPixmap(self.pixmapWhite)
                # self.gomoku_map.draw_xy(x, y, BLACK)
                self.mapLabel[x][y].setPixmap(self.pixmapBlackLast)
                # self.is_black_do = False
            else: # 하얀색
                # 직전 돌 초기화
                self.mapLabel[self.beforeX][self.beforeY].setPixmap(self.pixmapBlack)
                # self.gomoku_map.draw_xy(x, y, WHITE)
                self.mapLabel[x][y].setPixmap(self.pixmapWhiteLast)
                # self.is_black_do = True
            # 직전 돌 저장
            self.beforeX, self.beforeY = x, y
        
    # 엔드 slot
    @QtCore.pyqtSlot(str)
    def end_slot(self, msg):
        QMessageBox.information(self, "게임 종료", msg)
        
    # 통신 쓰레드
    def networkThread(self):
        while not self.GAME_DONE:
            # init
            if self.INIT: 
                self.timer.start()
                ret_tuple = self.gomoku.update_or_end()
                success, command, turn, data = ret_tuple
                if command == CMD_UPDATE: # update 명령
                    print("update: init")
                    # 내가 검은색 돌
                    if turn == 0:
                        self.MY_COLOR = BLACK
                        self.OTHER_COLOR = WHITE
                        
                        # 내가 검은색돌이고 AI 일 때
                        if self.player_type == AI:
                            # self.player.is_black = True
                            self.player = ChoiceOfPlayer(self.gomoku_map, self.player_type, True, self)

                            self.player.finishSignal.connect(self.AI_draw)
                            if self.step<2:
                                self.player.start()
                        # 내가 검은색돌이고 PERSON 일 때        
                        else:
                            self.player_black = ChoiceOfPlayer(self.gomoku_map, self.player_type, True, self)
                            
                        # todo
                        # self.other_player_type = PERSON
                        # self.other_player = ChoiceOfPlayer(self.gomoku_map, self.other_player_type, False, self)
                        # self.other_player.is_black = True
                        # self.other_player.finishSignal.connect(self.AI_draw)
                        # self.other_player.start()
                        self.blackLabel.setText(self.name)
                        self.whiteLabel.setText("상대방")
                        self.statusLabel.setText("게임 시작")
                        # if self.player_type == AI:
                        #     print("AI 의 첫 수")
                        #     x, y = self.player.Player.Go(self.gomoku_map, self.is_black, self)
                        #     self.ai_render_signal.emit(x, y)

                    # 내가 하얀색 돌
                    else:
                        self.MY_COLOR = WHITE
                        self.OTHER_COLOR = BLACK
                        
                        # 내가 하얀색 돌이고 AI 일 때
                        if self.player_type == AI:
                            # self.player.is_black = True
                            self.player = ChoiceOfPlayer(self.gomoku_map, self.player_type, False, self)
                            self.player.finishSignal.connect(self.AI_draw)
                            if self.step<2:
                                self.player.start()
                                
                        # 내가 하얀색 돌이고 PERSON 일 때
                        else:
                            self.player = ChoiceOfPlayer(self.gomoku_map, self.player_type, False, self)
                            
                        # todo
                        # self.other_player_type = PERSON
                        # self.other_player = ChoiceOfPlayer(self.gomoku_map, self.other_player_type, True, self)
                        # self.other_player.is_black = False
                        # self.other_player.finishSignal.connect(self.AI_draw)
                        # self.other_player.start()
                        self.blackLabel.setText("상대방")
                        self.whiteLabel.setText(self.name)
                        self.statusLabel.setText("게임 시작")
                    self.INIT = False
            else: # not init
                ret_tuple = self.gomoku.update_or_end()
                success, command, turn, data = ret_tuple    # bool, int, int, bytes 형태, 맨 첫 변수는 성공 실패 유무
                self.time_signal.emit(TIME_START)
                if command == CMD_UPDATE: # update 명령
                    i = int((data & 0b11110000) >> 4)
                    j = int(data & 0b00001111)
                    x = i - 1
                    y = j - 1
                    if turn == 0: # 내 차례
                        print(f'update: 상대가 둔 돌 x : {x}, y : {y}')
                        # 상대가 둔 x, y 를 gomoku_map 에 넣어줘야 함
                        # self.other_render_signal.emit(x, y)
                        print("내가 둘 차례")
                        if self.player_type == AI: # 내가 AI 면 
                            if self.OTHER_COLOR == BLACK: # 상대가 검은 돌이면
                                # 상대가 둔 돌 board 에 넣기
                                self.gomoku_map.draw_xy(x, y, BLACK) # 검은 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, BLACK)
                                self.player.is_black = False
                                # x, y = self.player.Player.Go(self.gomoku_map, self.is_black, self)
                                # self.ai_render_signal.emit(x, y)
                            else: # 상대가 하얀 돌이면
                                self.gomoku_map.draw_xy(x, y, WHITE) # 하얀 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, WHITE)
                                self.player.is_black = True
                                # x, y = self.player.Player.Go(self.gomoku_map, self.is_black, self)
                                # self.ai_render_signal.emit(x, y)
                        else: # 내가 사람이면
                            # 일단 고려 x
                            # render 만 하면 됨
                            if self.OTHER_COLOR == BLACK: # 상대가 검은 돌이면
                                self.gomoku_map.draw_xy(x, y, BLACK) # 검은 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, BLACK)
                            else: # 상대가 하얀 돌이면
                                self.gomoku_map.draw_xy(x, y, WHITE) # 하얀 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, WHITE)
                    else: # 상대 차례
                        # 내가 둔 돌에 대해서 render 해줌
                        print(f'update: 내가 둔 돌 x : {x}, y : {y}')
                        if self.MY_COLOR == BLACK: # 내가 검은 돌이면
                            self.gomoku_map.draw_xy(x, y, BLACK) # 검은 돌 두기 render_signal 에서 이미 draw
                            self.render_signal.emit(x, y, BLACK)
                        else: # 내가 하얀 돌이면
                            self.gomoku_map.draw_xy(x, y, WHITE) # 하얀 돌 두기
                            self.render_signal.emit(x, y, WHITE)
                if command == CMD_END: # end 명령
                    self.time_signal.emit(TIME_STOP)
                    self.GAME_DONE = True
                    if turn == 0: # 패배
                        if data == 0: # 오류(금수 등)로 인해
                            self.end_signal.emit("패배 (금수 등 오류 발생)")
                        elif data == 1: # 시간초과로 인해
                            self.end_signal.emit("패배 (시간초과)")
                        else: # 상대가 오목 완성
                            i = int((data & 0b11110000) >> 4)
                            j = int(data & 0b00001111)
                            x = i - 1
                            y = j - 1
                            if self.OTHER_COLOR == BLACK: # 상대가 검은 돌이면
                                self.gomoku_map.draw_xy(x, y, BLACK) # 검은 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, BLACK)
                            else: # 상대가 하얀 돌이면
                                self.gomoku_map.draw_xy(x, y, WHITE) # 하얀 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, WHITE)
                            self.end_signal.emit("패배 (상대 오목 완성)")
                    else: # 승리
                        if data == 0: # 오류(금수 등)로 인해
                            self.end_signal.emit("승리 (상대의 금수 등 오류)")
                        elif data == 1: # 시간초과로 인해
                            self.end_signal.emit("승리 (상대 시간초과)")
                        else: # 오목 완성
                            i = int((data & 0b11110000) >> 4)
                            j = int(data & 0b00001111)
                            x = i - 1
                            y = j - 1
                            if self.MY_COLOR == BLACK: # 내가 검은 돌이면
                                self.gomoku_map.draw_xy(x, y, BLACK) # 검은 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, BLACK)
                            else: # 내가 하얀 돌이면
                                self.gomoku_map.draw_xy(x, y, WHITE) # 하얀 돌 두기 render_signal 에서 이미 draw
                                self.render_signal.emit(x, y, WHITE)
                            self.end_signal.emit("승리 (오목 완성)")
                            
    def timerThread(self):
        self.t = 15
        while not self.TIME_DONE:
            time.sleep(1)
            if self.t <= 0:
                continue
            self.timeLabel.setText(str(self.t))
            self.t -= 1
        
    # 타이머 slot
    @QtCore.pyqtSlot(int)
    def timer_slot(self, flag):
        self.t = 15
        if flag == TIME_STOP:
            self.TIME_DONE = True
        else:
            self.TIME_DONE = False

    def find_cannot_place(self, x_idx, y_idx, color_id):
        if color_id == BLACK:
            
            ROW, COL, DIAG_1, DIAG_2 = 0, 1, 2, 3

            last_point = [[] for _ in range(4)]

            len_stone = [-1 for _ in range(4)]

            i, j = x_idx, y_idx
            while -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[ROW] += 1
                i -= 1
            last_point[ROW].append((i, j))

            i, j = x_idx, y_idx
            while -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[ROW] += 1
                i += 1
            last_point[ROW].append((i, j))
            
            i, j = x_idx, y_idx
            while -1 < j < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[COL] += 1
                j -= 1
            last_point[COL].append((i, j))

            i, j = x_idx, y_idx
            while -1 < j < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[COL] += 1
                j += 1
            last_point[COL].append((i, j))
            
            i, j = x_idx, y_idx
            while -1 < j < 15 and -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[DIAG_1] += 1
                j -= 1
                i -= 1
            last_point[DIAG_1].append((i,j))
            
            i, j = x_idx, y_idx
            while -1 < j < 15 and -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[DIAG_1] += 1
                j += 1
                i += 1
            last_point[DIAG_1].append((i,j))
            
            i, j = x_idx, y_idx
            while -1 < j < 15 and -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[DIAG_2] += 1
                j += 1
                i -= 1
            last_point[DIAG_2].append((i,j))
            
            i, j = x_idx, y_idx
            while -1 < j < 15 and -1 < i < 15 and self.gomoku_map.get_xy_on_logic_state(i, j) == color_id:
                len_stone[DIAG_2] += 1
                j -= 1
                i += 1
            last_point[DIAG_2].append((i,j))

            check_3_idx = []
            check_4_idx = []

            for idx in range(4):
                if len_stone[idx] == 3:
                    check_3_idx.append(idx)
                elif len_stone[idx] == 4:
                    check_4_idx.append(idx)
            
            if len(check_3_idx) >= 2:
                count_3 = 0
                for idx in check_3_idx:
                    blocked = False
                    for x, y in last_point[idx]:
                        if 0 <= x <= 14 and 0 <= y <= 14 and self.gomoku_map.get_xy_on_logic_state(x, y) == -1:
                            continue
                        else:
                            blocked = True
                            break
                    if not blocked:
                        count_3 += 1

                if count_3 >= 2:
                    return True

            if len(check_4_idx) >= 2:
                count_4 = 0
                for idx in check_4_idx:
                    blocked = False
                    for x, y in last_point[idx]:
                        if 0 <= x <= 14 and 0 <= y <= 14 and self.gomoku_map.get_xy_on_logic_state(x, y) == -1:
                            continue
                        else:
                            blocked = True
                            break
                    if not blocked:
                        count_4 += 1
                
                if count_4 >= 2:
                    return True

        return False

    def AI_draw(self, i, j):
        if self.step != -1:
            self.draw(i, j)# AI
            self.x_t, self.y_t = self.coordinate_transform_map2pixel(i, j)
			
        self.update()
        
        
    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if self.is_black_do == True:
            # self.pieces[self.step].setPixmap(self.black)
            self.gomoku_map.draw_xy(i, j, BLACK)
            self.render_signal.emit(i, j, BLACK)
            # self.who.setText('WHITE Player is Going...')
        else:
            # self.pieces[self.step].setPixmap(self.white)
            self.gomoku_map.draw_xy(i, j, WHITE)
            self.render_signal.emit(i, j, WHITE)
            # self.who.setText('BLACK Player is Going...')

        print(self.step)

        # self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)

        self.step += 1
        # self.chess_manual = self.chess_manual + str(i) +',' + str(j) + '|'

        # winner = self.chessboard.anyone_win(i, j)
        self.Going_over = True
        # if winner != EMPTY:
        #     self.mouse_point.clear()
        #     tmp,black,white = self.chessboard.get_board_item()
        #     print("BLACK num: " + str(len(black)))
        #     print("WHITE num: " + str(len(white)))

        #     self.player_black.is_black = False
        #     self.player_white.is_black = True
            # self.gameover(winner)

    def coordinate_transform_map2pixel(self, i, j):

        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):

        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))

        if i < 0 or i >= N_LINE or j < 0 or j >= N_LINE:
            return None, None
        else:
            return i, j



if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())