import sys
sys.path.append("..")

from algorithm.data_processing import *
import numpy as np
from algorithm.chess_check import *
import scipy.stats as st
from algorithm.SQLUtil import get_record

class PlayChess():
    def __init__(self):
        pass

    @staticmethod
    def get_move(code, color):
        """
        利用数据库查询，根据棋局给出下棋动作
        parm: (棋局状态码, 下棋方)
        return：(下棋动作)
        """
        data=get_record(code,color)
        max_ac=None
        max_v=0
        if(data):
            for record in data:
                # v = st.norm.cdf(record['result'], loc=0, scale=record['count'])  # 获胜概率
                # v = v + record['count'] / (v + record['count'])  # 统计次数过少的情况惩罚项
                # 效果不好，直接选择数量最大的
                v = record['count']
                if max_v<v:
                    max_ac=record
                    max_v=v
        if(max_ac):
            return max_ac['move']
        else:return None
        pass

    @staticmethod
    def get_random_move(code, color):
        """
        遇到没出现过的棋局时,随机生成合法的下棋动作 
        parm: (棋局状态码, 下棋方)
        return：(下棋动作)
        """
        init = num_split(code, step=2)
        rb_boundary = 16

        check = False
        while not check:
            # 根据下棋方随机选择棋子
            random_code = np.random.randint(0, rb_boundary)
            if color == -1:
                random_piece = random_code
            else:
                random_piece = random_code + rb_boundary

            if init[random_piece] == "99":
                continue
            # 随机生成落子点
            y = np.random.randint(0,10)
            x = np.random.randint(0,9)
            move = init[random_piece]+str(x)+str(y)
            # 检验
            check = ChessCheck.is_legal(code, move)
        return move
            
    @staticmethod
    def move(code, move):
        """
        执行下棋动作，生成新棋局
        parm: (棋局状态码, 下棋动作)
        return：(新的棋局状态码)
        """
        init = num_split(code, step=2)
        
        # 判断是否需要吃棋
        if move[2:4] in init:
            eat_ind = init.index(move[2:4])
            init[eat_ind] = "99"
        # 执行落子
        ind = init.index(move[:2])
        init[ind] = move[2:4]        

        new_init = ''.join(init)
        return new_init
        