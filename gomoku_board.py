from jconst import *
import copy
import time
import random

class GomokuBoard(object):
    def __init__(self):
        self.__board = [[EMPTY for n in range(N_LINE)] for m in range(N_LINE)]
        self.__dir = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]

        self.black_value = [[0 for n in range(N_LINE)] for m in range(N_LINE)]
        self.white_value = [[0 for n in range(N_LINE)] for m in range(N_LINE)]
        
        self.black_value_idx = [[[0 for n in range(4)] for m in range(N_LINE)] for k in range(N_LINE)]
        self.white_value_idx = [[[0 for n in range(4)] for m in range(N_LINE)] for k in range(N_LINE)]
        win_tree = []

        shape_score =[(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),# live two
               (200, (1, 1, 0, 1, 0)),
               (200, (0, 1, 0, 1, 1)),
               (200, (1, 0, 1, 1, 0)),
               (200, (0, 1, 1, 0, 1)),
               (200, (1, 1, 0, 0, 1)),
               (200, (1, 0, 0, 1, 1)),
               (200, (1, 0, 1, 0, 1)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),# sleep three
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),# live three
               (7000, (1, 1, 1, 0, 1)),
               (7000, (1, 1, 0, 1, 1)),
               (7000, (1, 0, 1, 1, 1)),
               (7000, (1, 1, 1, 1, 0)),
               (7000, (0, 1, 1, 1, 1)),# sleep four
               (50000, (0, 1, 1, 1, 1, 0)),#live four
               (999999, (1, 1, 1, 1, 1))]

        shape_score_w = copy.deepcopy(shape_score)
        for i in range(len(shape_score_w)):
            www = []
            for j in range(len(shape_score_w[i][1])):
                www.append(shape_score_w[i][1][j] * 2)
            qqq = []
            qqq.append(shape_score_w[i][0])
            qqq.append(tuple(www))
            shape_score_w[i] = tuple(qqq)

        self.shape_score = shape_score
        self.shape_score_w  = shape_score_w

        # win_tree_vertical
        for i in range(N_LINE-4):
            for j in range(N_LINE):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j])
                win_tree.append(tmp)
        self.win_tree_vertical = len(win_tree)
        # win_tree_landscape
        for i in range(N_LINE):
            for j in range(N_LINE-4):
                tmp = []
                for w in range(5):
                    tmp.append([i,j+w])
                win_tree.append(tmp)
        self.win_tree_landscape = len(win_tree)

        # win_tree_oblique
        for i in range(N_LINE-4):
            for j in range(N_LINE-4):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j+w])
                win_tree.append(tmp)
        self.win_tree_oblique_1 = len(win_tree)

        for i in range(N_LINE-4):
            for j in range(4,N_LINE):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j-w])
                win_tree.append(tmp)

        self.win_tree_oblique_2 = len(win_tree)

        self.win_tree = win_tree






    def board(self):
        return self.__board

    def get_board_item(self):
        empty_item = []
        black = []
        white = []
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if self.__board[m][n] == EMPTY:
                    empty_item.append((m,n))
                elif self.__board[m][n] == BLACK:
                    black.append((m,n))
                elif self.__board[m][n] == WHITE:
                    white.append((m,n))
        return empty_item,black,white


    def draw_xy(self, x, y, state):
        self.__board[x][y] = state
        self.value_change_after_draw(x,y)
        b,w = self.value_judge_best()
        # print('black value:' + str(b))
        # print('white value:' + str(w))


    def get_xy_on_logic_state(self, x, y):

        if self.isInBoard(x,y):
            return self.__board[x][y]
        return OUT

    def get_next_xy(self, point, direction):
        x = point[0] + direction[0]
        y = point[1] + direction[1]
        if x < 0 or x >= N_LINE or y < 0 or y >= N_LINE:
            return False
        else:
            return x, y

    def get_xy_on_direction_state(self, point, direction): 
        if point is not False:
            xy = self.get_next_xy(point, direction)
            if xy is not False:
                x, y = xy
                return self.__board[x][y]
        return False

    def anyone_win(self, x, y):
        state = self.get_xy_on_logic_state(x, y) 
        for directions in self.__dir:
            count = 1  
            for direction in directions: 
                point = (x, y)
                while True:
                    if self.get_xy_on_direction_state(point, direction) == state:
                        count += 1
                        point = self.get_next_xy(point, direction)
                    else:
                        break
            if count >= 5:
                return state
        e = self.get_board_item()[0]
        if len(e) == 0:
            return FULL
        return EMPTY


    def reset(self):  # 重置
        self.__board = [[EMPTY for n in range(N_LINE)] for m in range(N_LINE)]
        self.black_value = [[0 for n in range(N_LINE)] for m in range(N_LINE)]
        self.white_value = [[0 for n in range(N_LINE)] for m in range(N_LINE)]
        
        self.black_value_idx = [[[0 for n in range(4)] for m in range(N_LINE)] for k in range(N_LINE)]
        self.white_value_idx = [[[0 for n in range(4)] for m in range(N_LINE)] for k in range(N_LINE)]

    def closest_value(self,x,y):
        value = (x * (N_LINE - 1 - x) + y * (N_LINE - 1 - y)) / 5
        return value


    def get_k_dist_empty_10(self,k = 3,color = EMPTY):
        
        b = [[2 for q in range(N_LINE)] for w in range(N_LINE)]
        empty_item = []
        board = self.__board
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if board[m][n] is not EMPTY:
                    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1))
                    
                    for direction in directions:
                        for t in range(1,k):
                            x_t = m + direction[0] * t
                            y_t = n + direction[1] * t
                            if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                                break

                            if board[x_t][y_t] == EMPTY and b[x_t][y_t] > 0:
                                b[x_t][y_t] -= 1
                                if b[x_t][y_t] == 0:
                                    empty_item.append((x_t,y_t))

        if len(empty_item) == 0:
            if board[MIDDLE][MIDDLE] is EMPTY:
                empty_item.append((MIDDLE,MIDDLE))
            else:
                m = MIDDLE
                n = MIDDLE
                while(1):
                    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1))
                    t = random.randint(0,7)
                    m = m + directions[t][0]
                    n = n + directions[t][1]
                    if board[m][n] is EMPTY:
                        empty_item.append((m,n))
                        break




        if color == EMPTY:
            return empty_item

        black_value = self.black_value
        white_value = self.white_value

        Q = []
        for i in range(len(empty_item)):
            Q.append([black_value[empty_item[i][0]][empty_item[i][0]] + white_value[empty_item[i][0]][empty_item[i][0]],empty_item[i]])
        Q = sorted(Q,reverse=True)
        empty_item = []
        for i in range(len(Q)):
            if i >= 5:
                break
            empty_item.append(Q[i][1])

        return empty_item

    def get_k_dist_empty(self,k = 3,color = EMPTY):
        
        b = [[2 for q in range(N_LINE)] for w in range(N_LINE)]
        empty_item = []
        board = self.__board
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if board[m][n] is not EMPTY:
                    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1))
                    
                    for direction in directions:
                        for t in range(1,k):
                            x_t = m + direction[0] * t
                            y_t = n + direction[1] * t
                            if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                                break

                            if board[x_t][y_t] == EMPTY and b[x_t][y_t] > 0:
                                b[x_t][y_t] -= 1
                                if b[x_t][y_t] == 0:
                                    empty_item.append((x_t,y_t))

        if len(empty_item) == 0:
            if board[MIDDLE][MIDDLE] is EMPTY:
                empty_item.append((MIDDLE,MIDDLE))
            else:
                m = MIDDLE
                n = MIDDLE
                while(1):
                    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1))
                    t = random.randint(0,7)
                    m = m + directions[t][0]
                    n = n + directions[t][1]
                    if board[m][n] is EMPTY:
                        empty_item.append((m,n))
                        break




        if color == EMPTY:
            return empty_item

        black_value = self.black_value
        white_value = self.white_value

        Q = []
        for i in range(len(empty_item)):
            Q.append([black_value[empty_item[i][0]][empty_item[i][0]] + white_value[empty_item[i][0]][empty_item[i][0]],empty_item[i]])
        Q = sorted(Q,reverse=True)
        empty_item = []
        for i in range(len(Q)):
            empty_item.append(Q[i][1])

        return empty_item

    def get_k_dist_empty_tuple(self,k = 3):
        dist = k
        b = [[False for q in range(N_LINE)] for w in range(N_LINE)]
        empty_item = []
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if self.__board[m][n] is not EMPTY:
                    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1],[1,1],[-1,-1]]
                    for t in range(1,k):

                        for direction in directions:
                            x_t = m + direction[0] * t
                            y_t = n + direction[1] * t
                            if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                                continue

                            if self.__board[x_t][y_t] == EMPTY and b[x_t][y_t] == False:
                                
                                b[x_t][y_t] = True
                                empty_item.append((x_t,y_t))


        return empty_item

    def value_judge(self,color):
        b_sheet = [0,0,0,0,0]
        w_sheet = [0,0,0,0,0]

        shape_score = self.shape_score
        shape_score_w = self.shape_score_w





        win_tree = self.win_tree
        use_five_b = []
        b_value = 0
        w_value = 0
        for i in range(len(win_tree)):
            b_count = 0
            w_count = 0
            use_tmp = []
            has_black = False
            has_white = False
            for j in range(5):
                
                if self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]) == BLACK:
                    has_black = True
                    b_count += 1
                elif self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]) == WHITE:
                    has_white = True
                    w_count += 1
                use_tmp.append(self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]))

                if has_black and has_white:
                    break
            #if has_black or has_white:
                
            if has_black and has_white:
                continue
            elif has_black == False and has_white == False:
                continue
            else:
                
                tup_5 = tuple(use_tmp)
                #print('tup:' + str(tup_5) + '  num:' + str(b_count))
                has_6 = False
                if i>=0 and i < self.win_tree_vertical:
                    direction = [1,0]
                if i >= self.win_tree_vertical and i < self.win_tree_landscape:
                    direction = [0,1]
                if i >= self.win_tree_landscape and i < self.win_tree_oblique_1:
                    direction = [1,1]
                if i >= self.win_tree_oblique_1 and i < len(win_tree):
                    direction = [1,-1]
                x_t = win_tree[i][j][0] + direction[0]
                y_t = win_tree[i][j][1] + direction[1]
                if not(x_t <0 or x_t >=N_LINE or y_t < 0 or y_t >= N_LINE):
                    if self.get_xy_on_logic_state(x_t,y_t) == EMPTY:
                        has_6 = True
                        use_tmp.append(EMPTY)
                        tup_6 = tuple(use_tmp)
                
            if has_black and b_count >= 2:


                for m in shape_score:
                    squ = m[1]
                    if len(squ) == 6 and has_6 == True:
                        if squ == tup_6:
                            if color == WHITE:
                                if m[0] == LIVE_THREE:
                                    b_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    b_value += m[0] * 20
                            b_value += m[0]
                    elif len(squ) == 5:
                        if squ == tup_5:
                            if color == WHITE:
                                if m[0] == LIVE_THREE:
                                    b_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    b_value += m[0] * 20
                            b_value += m[0]
                
            elif has_white and w_count >= 2:
                for m in shape_score_w:
                    squ = m[1]
                    if len(squ) == 6 and has_6 == True:
                        if squ == tup_6:
                            if color == BLACK:
                                if m[0] == LIVE_THREE:
                                    w_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    w_value += m[0] * 20
                            w_value += m[0]
                    elif len(squ) == 5:
                        if squ == tup_5:
                            if color == BLACK:
                                if m[0] == LIVE_THREE:
                                    w_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    w_value += m[0] * 20
                            w_value += m[0]
                

        for i in range(N_LINE):
            for j in range(N_LINE):
                if self.get_xy_on_logic_state(i,j) == BLACK:
                    b_value += self.closest_value(i,j)
                elif self.get_xy_on_logic_state(i,j) == WHITE:
                    w_value += self.closest_value(i,j)


        return b_value,w_value

    def value_judge_3(self,i,j): # for the step one
        my_color = self.get_xy_on_logic_state(i,j)
        my_color_after = self.one_point_value(i,j)
        my_color_before = self.one_point_value(i,j,True)
        my_color_change = my_color_after - my_color_before
        enemy_color = (my_color) % 2 + 1
        enemy_color_after = 0
        enemy_color_before = 0

        for k in range(8):
            self.one_point_value(i,j)

    def one_point_value_update(self,i,j,dir_idx=-1):

       
        color = self.get_xy_on_logic_state(i,j)
        black_value_idx = self.black_value_idx
        white_value_idx = self.white_value_idx
        if dir_idx == -1:
            if color == BLACK:
                black_value_idx[i][j] = self.one_point_value(i,j,BLACK)
                white_value_idx[i][j] = [0,0,0,0]

            if color == WHITE:
                white_value_idx[i][j] = self.one_point_value(i,j,WHITE)
                black_value_idx[i][j] = [0,0,0,0]
            if color == EMPTY:
                black_value_idx[i][j] = self.one_point_value(i,j,BLACK)
                white_value_idx[i][j] = self.one_point_value(i,j,WHITE)

        else:
            if color == BLACK:
                black_value_idx[i][j][dir_idx] = self.one_point_value(i,j,BLACK,dir_idx)
                white_value_idx[i][j] = [0,0,0,0]
            elif color == WHITE:
                white_value_idx[i][j][dir_idx] = self.one_point_value(i,j,WHITE,dir_idx)
                black_value_idx[i][j] = [0,0,0,0]
            elif color == EMPTY:
                black_value_idx[i][j][dir_idx] = self.one_point_value(i,j,BLACK,dir_idx)
                white_value_idx[i][j][dir_idx] = self.one_point_value(i,j,WHITE,dir_idx)
        self.black_value[i][j] = sum(self.black_value_idx[i][j])
        self.white_value[i][j] = sum(self.white_value_idx[i][j])

    def value_change_after_draw(self,i,j):
        color = self.get_xy_on_logic_state(i,j)
        self.one_point_value_update(i,j)

        directions = FOUR_DIR
        count = 0
        for direction in directions:
            isIn = False
            for m in range(-RADIUS,RADIUS + 1):
                if m == 0:
                    continue
                i_t = i + m * direction[0]
                j_t = j + m * direction[1]
                if self.isInBoard(i_t,j_t):
                    isIn = True
                    self.one_point_value_update(i_t,j_t,count)
                else:
                    if isIn:
                        break
                    continue
            count += 1

    def value_judge_best(self):
        #self.value_init()
        black_value = 0
        white_value = 0
        for i in range(N_LINE):
            for j in range(N_LINE):
                if self.get_xy_on_logic_state(i,j) == BLACK:
                    black_value += self.score_polish(self.black_value[i][j])
                elif self.get_xy_on_logic_state(i,j) == WHITE:
                    white_value += self.score_polish(self.white_value[i][j])

        return black_value,white_value


    def score_polish(self,score):
        if score < FOUR_S and score >= BLOCK_FOUR:
            if score >= BLOCK_FOUR and score < BLOCK_FOUR + THREE_S:
                return THREE_S
            elif score >= BLOCK_FOUR + THREE_S and score < 2 * BLOCK_FOUR:
                return FOUR_S
            else:
                return FOUR_S * 2

        if score < BLOCK_FOUR and score >= 2 * THREE_S:
            return 5 * BLOCK_FOUR

        return score





    def value_init(self):
        for i in range(N_LINE):
            for j in range(N_LINE):
                if self.get_xy_on_logic_state(i,j) == EMPTY:
                    b_idx = self.one_point_value(i,j,BLACK)
                    w_idx = self.one_point_value(i,j,WHITE)
                    self.black_value_idx[i][j] = b_idx
                    self.white_value_idx[i][j] = w_idx
                elif self.get_xy_on_logic_state(i,j) == BLACK:
                    self.black_value_idx[i][j] = self.one_point_value(i,j,BLACK)
                    self.white_value_idx[i][j] = [0,0,0,0]
                elif self.get_xy_on_logic_state(i,j) == WHITE:
                    self.black_value_idx[i][j] = [0,0,0,0]
                    self.white_value_idx[i][j] = self.one_point_value(i,j,WHITE)

                self.black_value[i][j] = sum(self.black_value_idx[i][j])
                self.white_value[i][j] = sum(self.white_value_idx[i][j])


    def sum_value(self):
        for i in range(N_LINE):
            for j in range(N_LINE):
                self.black_value[i][j] = sum(self.black_value_idx[i][j])
                self.white_value[i][j] = sum(self.white_value_idx[i][j])

    def one_point_value(self,i,j,color,dir_idx= -1):
        this_color = color
        #true_color = self.get_xy_on_logic_state(i,j)

        value = 0
        value_dir = []
        if dir_idx == -1:
            directions = FOUR_DIR
        elif dir_idx >= 0 and dir_idx <=3:
            directions = [FOUR_DIR[dir_idx]]

        for sub_dir in directions:
            count = 1
            second_count = 0
            empty = -1

            block_l = False 
            block_r = False

            now_dir = sub_dir
            i_t = now_dir[0] + i
            j_t = now_dir[1] + j

            while(1):
                color = self.get_xy_on_logic_state(i_t,j_t)
                

                if color == OUT:
                    block_l = True
                    break
                i_t_t,j_t_t = self.getNextOne(i_t,j_t,now_dir)
                if color == EMPTY:
                    if empty == -1 and self.get_xy_on_logic_state(i_t_t,j_t_t) == this_color:
                        empty = count
                    else:
                        break

                elif color == this_color:
                    count +=1
                else:
                    block_l = True
                    break
                i_t = i_t_t
                j_t = j_t_t

            now_dir = (-sub_dir[0],-sub_dir[1])
            i_t = now_dir[0] + i
            j_t = now_dir[1] + j
            while(1):
                color = self.get_xy_on_logic_state(i_t,j_t)
                

                if color == OUT:
                    block_r = True
                    break
                i_t_t,j_t_t = self.getNextOne(i_t,j_t,now_dir)
                if color == EMPTY:
                    if empty == -1 and self.get_xy_on_logic_state(i_t_t,j_t_t) == this_color:
                        empty = 0
                    else:
                        break

                elif color == this_color:
                    second_count +=1
                    if empty is not -1:
                        empty +=1
                else:
                    block_r = True
                    break
                i_t = i_t_t
                j_t = j_t_t

            count += second_count
            tmp = self.countToScore(count,empty,block_l,block_r)
            value_dir.append(tmp)
            value += tmp

        if dir_idx is not -1:
            return value

        return value_dir

    def getNextOne(self,i,j,direction):
        i_t = i + direction[0]
        j_t = j + direction[1]
        return i_t,j_t


    def countToScore(self,count,empty,block_l,block_r):
        block = 0
        if block_l:
            block+=1
        if block_r:
            block+=1
        if empty == None:
            empty = 0
        if empty <= 0:
            if count >= 5:
                return FIVE_S
            if block == 0:
                if count == 1:
                    return ONE_S
                if count == 2:
                    return TWO_S
                if count == 3:
                    return THREE_S
                if count == 4:
                    return FOUR_S
            elif block == 1:
                if count == 1:
                    return BLOCK_ONE
                if count == 2:
                    return BLOCK_TWO
                if count == 3:
                    return BLOCK_THREE
                if count == 4:
                    return BLOCK_FOUR

        elif empty == 1 or empty == count - 1:
            if count >= 6:
                return FIVE_S
            if block == 0:
                if count == 2:
                    return TWO_S / 2
                if count == 3:
                    return THREE_S
                if count == 4:
                    return BLOCK_FOUR
                if count == 5:
                    return FOUR_S
            elif block == 1:
                if count == 2:
                    return BLOCK_TWO
                if count == 3:
                    return BLOCK_THREE
                if count == 4:
                    return BLOCK_FOUR
                if count == 5:
                    if (block_l and empty == count - 1) or (block_r and empty == 1):
                        return FOUR_S
                    return BLOCK_FOUR
            elif block == 2:
                if count >= 4:
                    return BLOCK_FOUR

        elif empty == 2 or empty == count - 2:
            if count >= 7:
                return FIVE_S
            if block == 0:
                if count == 3:
                    return THREE_S
                if count == 4 and count == 5:
                    return BLOCK_FOUR
                if count == 6:
                    return FOUR_S
            elif block == 1:
                if count == 3:
                    return BLOCK_THREE
                if count == 4 and count == 5:
                    return BLOCK_FOUR
                if count == 6:
                    if (block_l and empty == count - 2) or (block_r and empty == 2):
                        return FOUR_S
                    return BLOCK_FOUR
            elif block == 2:
                if count >= 4:
                    return BLOCK_FOUR


        elif empty == 3 or empty == count - 3:
            if count >= 8:
                return FIVE_S
            if block == 0:
                ##TO DISCUSS
                if count == 4 and count == 5 and count == 6:
                    return BLOCK_FOUR
                if count == 7:
                    return FOUR_S
            elif block == 1:
                if count == 4 and count == 5 and count == 6:
                    return BLOCK_FOUR
                if count == 7:
                    if (block_l and empty == count - 3) or (block_r and empty == 3):
                        return FOUR_S
                    return BLOCK_FOUR
            elif block == 2:
                if count >= 4:
                    return BLOCK_FOUR

        elif empty == 4 or empty == count - 4:
            if count >= 9:
                return FIVE_S
            if block == 0:
                if count >= 5:
                    return FOUR_S
            if block == 1:
                if count >= 5 and count <= 7:
                    if (block_l and empty == count - 4) or (block_r and empty == 4):
                        return BLOCK_FOUR
                return FOUR_S
            if block == 2:
                if count >= 5:
                    return BLOCK_FOUR

        elif empty == 5 or empty == count - 5:
            return FIVE_S
        return 0

    def isInBoard(self,i,j):
        if i < 0 or i >= N_LINE or j < 0 or j >= N_LINE:
            return False
        return True

    def value_judge_2(self,x,y,color): # for the step one
        shape_score = self.shape_score
        shape_score_w = self.shape_score_w

        b_value_after = 0
        b_value_before = 0
        w_value_after = 0
        w_value_before = 0

        # judge the 9 * 9
        point = (x,y)
        value_sheet_after = []
        value_sheet_before = []

        # landscape
        directions = [[1,0],[0,1],[1,-1],[1,1]]

        value_line_before = []

        begin = time.time()

        for direction in directions:
            x_left = x - direction[0] * 4
            y_left = y - direction[1] * 4
            value_line = []
            value_line_before = []
            for i in range(9):
                x_t = x_left + i * direction[0]
                y_t = y_left + i * direction[1]
                if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                    continue
                value_line.append(self.get_xy_on_logic_state(x_t,y_t))
                if x_t == x and y_t == y:
                    value_line_before.append(EMPTY)
                else:
                    value_line_before.append(self.get_xy_on_logic_state(x_t,y_t))
            value_sheet_after.append(value_line)
            value_sheet_before.append(value_line_before)

        begin2 = time.time()
        self.time1 += begin2 - begin

        #value evaluate to the after one
        for i in range(len(value_sheet_after)):
            for j in range(len(shape_score)):
                ptr = 0
                while(1):
                    if ptr + len(shape_score[j][1]) >= 9:
                        break
                    tmp = tuple(value_sheet_after[i][ptr:(ptr+len(shape_score[j][1]))])
                    tmp_before = tuple(value_sheet_before[i][ptr:(ptr+len(shape_score[j][1]))])
                    ratio_b = 1
                    ratio_w = 1
                    if shape_score[j][0] >= FOUR_VALUE and color == BLACK:
                        ratio_w = 20
                    if shape_score[j][0] == LIVE_THREE and color == BLACK:
                        ratio_w = 5
                    if shape_score[j][0] >= FOUR_VALUE and color == WHITE:
                        ratio_b = 20
                    if shape_score[j][0] == LIVE_THREE and color == WHITE:
                        ratio_b = 5
                    if tmp == shape_score[j][1]:
                        b_value_after += shape_score[j][0] * ratio_b
                    if tmp_before == shape_score[j][1]:
                        b_value_before += shape_score[j][0] * ratio_b
                    if tmp == shape_score_w[j][1]:
                        w_value_after += shape_score_w[j][0] * ratio_w
                    if tmp_before == shape_score_w[j][1]:
                        w_value_before += shape_score_w[j][0] * ratio_w
                    ptr += 1



        b_value = b_value_after - b_value_before
        w_value = w_value_after - w_value_before
        closest_value = self.closest_value(x,y)
        color = self.get_xy_on_logic_state(x,y)
        if color == BLACK:
            b_value += closest_value
        elif color == WHITE:
           w_value += closest_value

        self.time2 += time.time() - begin2

        return b_value,w_value




        








