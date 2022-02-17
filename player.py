from minmax import MinMax,MinMax_smallset,MinMax_best
import time

from jconst import *
import random
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound

class ChoiceOfPlayer(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)

    def __init__(self,board,player_type,my_is_black,parent=None):
        super(ChoiceOfPlayer,self).__init__()
        # type 을 바꿔서 어떤 AI 쓸지 고를 수 있음
        self.type = player_type
        self.board = board
        self.my_is_black = my_is_black
        self.is_black = True
        self.parent = parent

        if(self.type == 0):
            self.Player = HumanPlayer(board,my_is_black)
        elif(self.type == 1):
            self.Player = AIPlayer_1(board,my_is_black)
        elif(self.type == 2):
            self.Player = AIPlayer_2(board,my_is_black)
        elif(self.type == 3):
            self.Player = AIPlayer_3(board,my_is_black)

    def run(self):
        while(1):
            time.sleep(0.5)
            # print(f'self.my_is_black {self.my_is_black}, self.is_black {self.is_black}')

            if self.my_is_black == self.is_black:
                # if self.my_is_black == True:
                #     self.parent.mouse_point.setPixmap(self.parent.black)
                # else:
                #     self.parent.mouse_point.setPixmap(self.parent.white)
                not_empty = True
                while(not_empty):
                    self.parent.log_signal.emit("MINMAX 계산중 ...")
                    #print("my_is_black:" + str(self.my_is_black))
                    i,j = self.Player.Go(self.parent.gomoku_map,self.is_black,self.parent)
                    
                    if not i is None and not j is None:
                        # todo
                        # self.is_black 이 True 면 검은돌이라는 뜻
                        # 금수 검사를 해야 함
                        
                        if self.parent.gomoku_map.get_xy_on_logic_state(i,j) == EMPTY:
                            not_empty = False

                # if self.my_is_black == True:
                #     self.parent.render_signal.emit(i, j, BLACK)
                # else:
                #     self.parent.render_signal.emit(i, j, WHITE)
                x = int(i) + 1
                y = int(j) + 1
                self.parent.gomoku.put(x, y)
                # self.finishSignal.emit(i, j)
                # is_black 이랑 my_is_black 이 다르게 만들어줌
                # 같아지면 ai 동작?
                self.is_black = not self.is_black
                if self.my_is_black == True:
                    self.parent.is_black = False
                else:
                    self.parent.is_black = True

class HumanPlayer():
    def __init__(self, board,is_black):
        print('human')


    def Go(self,board,is_black,parent):
        self.board = board
        self.Going = True
        parent.Going = True
        while(parent.Going):
            print("human->Go->while")
            time.sleep(0.1)

        # i, j = self.coordinate_transform_pixel2map(parent.otherX,parent.otherY)
        i, j = parent.otherX, parent.otherY
        return i,j

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= N_LINE or j < 0 or j >= N_LINE:
            return None, None
        else:
            return i, j



class AIPlayer_1():
    def __init__(self,board,is_black):
        self.ai = MinMax(is_black,1)

    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result

class AIPlayer_2():
    def __init__(self,board,is_black):
        self.ai = MinMax_best(is_black)
        print('AI_2')


    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result

class AIPlayer_3():
    def __init__(self,board,is_black):
        self.ai = MinMax_smallset(is_black)
        print('AI_3')


    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result
