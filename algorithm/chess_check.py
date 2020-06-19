from chess_rule import *

class ChessCheck():

    def __init__(self):
        pass

    def code_to_martix(self, code):
        """
        棋局状态码转棋局矩阵
        parm: (棋局状态码)
        return: 棋局矩阵
        """

        pass

    def matrix_to_code(self, matrix):
        """
        棋局矩阵转棋局状态码
        parm: (棋局矩阵)
        return: 棋局状态码
        """

        pass


    def is_legal(self, matrix, move, color):
        """
        判断下棋动作是否合法 
        parm: (棋局状态, 下棋动作, 下棋方)
        retrun: True/False
        """

        # 判断是否越界
        ChessRule.is_cross_border(move)

        # 判断该棋子的下棋动作是否符合一步内可达

        # 各个棋子对应的规则函数
        switch_piece = {
            1: ChessRule.hongche, 2: ChessRule.hongma, 3: ChessRule.hongxiang, 
            4: ChessRule.hongshi, 5: ChessRule.hongshuai, 6: ChessRule.hongbing,
            7: ChessRule.heiche, 8: ChessRule.heima, 9: ChessRule.heixiang, 
            10: ChessRule.heishi, 11: ChessRule.heijiang, 12: ChessRule.heizu
        }
        

        # 判断能否吃子
        ChessRule.is_plumule(matrix, move)
        pass

    def is_over(self, code):
        """
        判断当局是否结束 
        parm: (棋局状态码)
        return: 当前棋局状态(红胜：-１；未结束：0；黑胜：１)
        """
        # 判断是否有一方将领消失

        pass
        

