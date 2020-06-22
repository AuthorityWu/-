from chess_rule import *
import numpy as np
from data_processing import num_split

class ChessCheck():

    def __init__(self):
        pass

    @staticmethod
    def code_to_matrix(code):
        """
        棋局状态码转棋局矩阵
        parm: (棋局状态码)
        return: 棋局矩阵
        """
        board_x = 9
        board_y = 10
        matrix = np.zeros((board_y,board_x))
        # print(matrix.shape)

        init = num_split(code, step=2)
        for i in range(len(init)):
            x = int(init[i][0])
            y = int(init[i][1])
            if y == x and y== 9:
                pass
            else:
                matrix[y,x] = i+1

        return matrix

    # def matrix_to_code(self, matrix):
    #     """
    #     棋局矩阵转棋局状态码
    #     parm: (棋局矩阵)
    #     return: 棋局状态码
    #     """
    #     pass

    @staticmethod
    def is_legal(code, move):
        """
        判断下棋动作是否合法 
        parm: (棋局状态码, 下棋动作, 下棋方)
        retrun: True/False
        """
        
        # 生成棋局矩阵
        matrix = ChessCheck.code_to_matrix(code)
        # 哪个棋子有动作
        init = num_split(code, step=2)
        piece_num = init.index(move[:2]) + 1
        rb_boundary = 16

        # 判断动作是否越界
        check = ChessRule.is_cross_border(move, piece_num)
        if check == False:
            return False
        
        # 各个棋子对应的规则函数
        switch_piece = {
            1: ChessRule.hongche, 2: ChessRule.hongma, 3: ChessRule.hongxiang, 
            4: ChessRule.hongshi, 5: ChessRule.hongshuai, 6: ChessRule.hongshi,
            7: ChessRule.hongxiang, 8: ChessRule.hongma, 9: ChessRule.hongche,
            10: ChessRule.hongpao, 11: ChessRule.hongpao, 12: ChessRule.hongbing,
            13: ChessRule.hongbing, 14: ChessRule.hongbing, 15: ChessRule.hongbing,
            16: ChessRule.hongbing,

            17: ChessRule.heiche, 18: ChessRule.heima, 19: ChessRule.heixiang, 
            20: ChessRule.heishi, 21: ChessRule.heijiang, 22: ChessRule.heishi,
            23: ChessRule.heixiang, 24: ChessRule.heima, 25: ChessRule.heiche,
            26: ChessRule.heipao, 27: ChessRule.heipao, 28: ChessRule.heizu,
            29: ChessRule.heizu, 30: ChessRule.heizu, 31: ChessRule.heizu,
            32: ChessRule.heizu
        }

        # 判断该棋子的下棋动作是否符合一步内可达
        jump = 0 # 是否有跳子
        # 炮棋子的动作
        if 9 == (piece_num-1)%rb_boundary or 10 == (piece_num-1)%rb_boundary:
            check, jump = switch_piece[piece_num](matrix, move)
        # 非炮棋子的动作
        else:
            check = switch_piece[piece_num](matrix, move)
        if check == False:
            return False

        # 判断能否落子
        check = ChessRule.is_plumule(matrix, move, piece_num, jump)
        return check
        

    @staticmethod
    def is_over(code):
        """
        判断当局是否结束 
        parm: (棋局状态码)
        return: 当前棋局状态(红胜：-１；未结束：0；黑胜：１)
        """
        # 判断是否有一方将领消失
        init = num_split(code, step=2)
        hongshuai = 5
        heijiang = 21
        lose = "99"

        if init[hongshuai-1] == lose:
            return 1
        if init[heijiang-1] == lose:
            return -1
        return 0
    
    