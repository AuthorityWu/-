import numpy as np

class ChessRule():
    def __init__(self):
        pass

    @staticmethod
    def is_cross_border(move, piece_num):
        """
        是否越界
        """
        check = True
        rb_boundary = 16    # code中红棋和黑棋的边界
        # 非帅或将的边界
        cnt = 0
        if 4 != (piece_num-1)%rb_boundary:
            top = 0
            bottom = 9
            left = 0
            right = 8
            # 相或象的边界
            if 2 == (piece_num-1)%rb_boundary or 6 == (piece_num-1)%rb_boundary:
                if piece_num <= rb_boundary: 
                    top = 5; bottom = 9
                else:
                    top = 0; bottom = 4
            # 士的边界
            elif 3 == (piece_num-1)%rb_boundary or 5 == (piece_num-1)%rb_boundary:
                if piece_num <= rb_boundary: 
                    top = 7; bottom = 9; left = 3; right = 5
                else:
                    top = 0; bottom = 2; left = 3; right = 5    
            # 判断是否在边界内
            cnt = 0
            for i in range(len(move)):                
                if i % 2 == 0 and left <= int(move[i]) and int(move[i]) <= right:
                    cnt += 1
                if i % 2 == 1 and top <= int(move[i]) and int(move[i]) <= bottom:
                    cnt += 1
            if cnt != 4:
                check = False
        # 帅或将的边界
        else:
            for i in range(2):
                if i == 0: 
                    top = 7; bottom = 9; left = 3; right = 5
                else:
                    top = 0; bottom = 2; left = 3; right = 5
                for j in range(len(move)//2):
                    if  left <= int(move[j*2 ]) and int(move[j*2 ]) <= right and \
                        top <= int(move[j*2 + 1]) and int(move[j*2 + 1]) <= bottom:
                        
                        cnt += 1
            if cnt != 2:
                check = False

        return check        

    @staticmethod
    def is_plumule(matrix, move, piece_num, jump=0):
        """
        能否落子
        """
        check = True
        rb_boundary = 16    # code中红棋和黑棋的边界
        end = [int(move[2]), int(move[3])]

        # 非炮棋子的落子判断
        if 9 != (piece_num-1)%rb_boundary and 10 != (piece_num-1)%rb_boundary:
            if matrix[end[1], end[0]] != 0:
                if matrix[end[1], end[0]] <= rb_boundary and piece_num <= rb_boundary:
                    check = False
                elif matrix[end[1], end[0]] > rb_boundary and piece_num > rb_boundary:
                    check = False
        # 炮棋子的落子判断
        else:
            if jump == 0 and matrix[end[1], end[0]] != 0:
                check = False
            elif jump == 1:
                if matrix[end[1], end[0]] == 0:
                    check = False
                elif matrix[end[1], end[0]] <= rb_boundary and piece_num <= rb_boundary:
                    check = False
                elif matrix[end[1], end[0]] > rb_boundary and piece_num > rb_boundary:
                    check = False
                
        return check
    
    """
    各个棋子的一步动作的合法性校验
    parm: (棋局矩阵, 下棋动作)
    return: True/False
    """
    # 红
    @staticmethod
    def hongche(matrix, move):
        check = True
        sta = [int(move[0]), int(move[1])]
        end = [int(move[2]), int(move[3])]

        if sta[0] == end[0] and sta[1] == end[1]:
            check = False
        elif sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0:
                    check = False
                    break
        elif sta[1] == end[1]:
            row = sta[1]
            left = min(sta[0], end[0])
            right = max(sta[0], end[0])
            for i in range(left+1, right):
                if matrix[row,i] != 0:
                    check = False
                    break
        else:
            check = False
        return check

    @staticmethod
    def hongma(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end
        stop_point = np.array([int(move[0]), int(move[1])])

        if abs(distance[0]*distance[1]) != 2:
            return False
        if abs(distance[0]) == 1:
            if distance[1] > 0:
                stop_point[1] -= 1
            else:
                stop_point[1] += 1
        else:
            if distance[0] > 0:
                stop_point[0] -= 1
            else:
                stop_point[0] += 1

        if matrix[stop_point[1],stop_point[0]] != 0:
            check = False
        return check

    @staticmethod
    def hongxiang(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end
        stop_point = (sta+end)//2

        if abs(distance[0]) != 2 or abs(distance[1]) != 2:
            return False

        if matrix[stop_point[1],stop_point[0]] != 0:
            check = False
        return check

    @staticmethod
    def hongshi(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end

        if abs(distance[0]) != 1 or abs(distance[1]) != 1:
            return False
        return check
    
    @staticmethod
    def hongshuai(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])

        if matrix[end[1], end[0]] == 21 and sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0:
                    check = False
                    break            
            return check

        distance = sta - end
        if sum(abs(distance)) != 1:
            return False
        return check

    @staticmethod
    def hongpao(matrix, move):
        check = True
        sta = [int(move[0]), int(move[1])]
        end = [int(move[2]), int(move[3])]
        cnt = 0
        if sta[0] == end[0] and sta[1] == end[1]:
            check = False
        elif sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0 :
                    cnt += 1
                if cnt > 1:
                    check = False
                    break
        elif sta[1] == end[1]:
            row = sta[1]
            left = min(sta[0], end[0])
            right = max(sta[0], end[0])
            for i in range(left+1, right):
                if matrix[row,i] != 0:
                    cnt += 1
                if cnt > 1:
                    check = False
                    break
        else:
            check = False
        jump = cnt
        # 返回是否合法，是否有跳子
        return check, jump

    @staticmethod
    def hongbing(matrix, move):
        check = True
        row_boundary = 5    # 红方的边界

        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end

        if sta[1] >= row_boundary:
            if distance[1] != 1 or distance[0] != 0:
                return False
        else:
            if distance[1] < 0:
                return False
            if sum(abs(distance)) != 1:
                return False

        return check

    # 黑
    @staticmethod
    def heiche(matrix, move):
        check = True
        sta = [int(move[0]), int(move[1])]
        end = [int(move[2]), int(move[3])]
        
        if sta[0] == end[0] and sta[1] == end[1]:
            check = False
        elif sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0:
                    check = False
                    break
        elif sta[1] == end[1]:
            row = sta[1]
            left = min(sta[0], end[0])
            right = max(sta[0], end[0])
            for i in range(left+1, right):
                if matrix[row,i] != 0:
                    check = False
                    break
        else:
            check = False
        return check

    @staticmethod
    def heima(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end
        stop_point = np.array([int(move[0]), int(move[1])])

        if abs(distance[0]*distance[1]) != 2:
            return False
        if abs(distance[0]) == 1:
            if distance[1] > 0:
                stop_point[1] -= 1
            else:
                stop_point[1] += 1
        else:
            if distance[0] > 0:
                stop_point[0] -= 1
            else:
                stop_point[0] += 1

        if matrix[stop_point[1],stop_point[0]] != 0:
            check = False
        return check
    
    @staticmethod
    def heixiang(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end
        stop_point = (sta+end)//2

        if abs(distance[0]) != 2 or abs(distance[1]) != 2:
            return False

        if matrix[stop_point[1],stop_point[0]] != 0:
            check = False
        return check

    @staticmethod
    def heishi(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end
        
        if abs(distance[0]) != 1 or abs(distance[1]) != 1:
            return False
        return check

    @staticmethod
    def heijiang(matrix, move):
        check = True
        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])

        if matrix[end[1], end[0]] == 5 and sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0:
                    check = False
                    break            
            return check

        distance = sta - end
        if sum(abs(distance)) != 1:
            return False
        return check

    @staticmethod
    def heipao(matrix, move):
        check = True
        sta = [int(move[0]), int(move[1])]
        end = [int(move[2]), int(move[3])]
        cnt = 0
        if sta[0] == end[0] and sta[1] == end[1]:
            check = False
        elif sta[0] == end[0]:
            col = sta[0]
            top = min(sta[1], end[1])
            bottom = max(sta[1], end[1])
            for i in range(top+1, bottom):
                if matrix[i,col] != 0 :
                    cnt += 1
                if cnt > 1:
                    check = False
                    break
        elif sta[1] == end[1]:
            row = sta[1]
            left = min(sta[0], end[0])
            right = max(sta[0], end[0])
            for i in range(left+1, right):
                if matrix[row,i] != 0:
                    cnt += 1
                if cnt > 1:
                    check = False
                    break
        else:
            check = False
        # return check
        # 返回是否合法，是否有跳子
        jump = cnt
        return check, jump

    @staticmethod
    def heizu(matrix, move):
        check = True
        row_boundary = 4    # 黑方的边界

        sta = np.array([int(move[0]), int(move[1])])
        end = np.array([int(move[2]), int(move[3])])
        distance = sta - end

        if sta[1] <= row_boundary:
            if distance[1] != -1 or distance[0] != 0:
                return False
        else:
            if distance[1] > 0:
                return False
            if sum(abs(distance)) != 1:
                return False

        return check

    
