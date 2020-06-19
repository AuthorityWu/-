from chess_check import *
import json 
import os
from data_processing import *
import numpy as np
from play_chess import *

input_path = "../data/output_chessdata.json"

with open(input_path, "r") as f:
    input_data = json.load(f)


if __name__ == "__main__":    
    # 测试is_legal
    """
    cnt = 0
    for one in input_data:
        # 制作错误动作测试
        # y = np.random.randint(0,10)
        # x = np.random.randint(0,9)
        # one["move"] = one["move"][0:2]+str(x)+str(y)
        
        matrix = ChessCheck.code_to_matrix(one["init"])
        res = ChessCheck.is_legal(one["init"], matrix, one["move"])
        
        if not res:
            print(res)
            cnt +=1 
            print(matrix)
            print(one)
            print("## ", cnt)
    """

    # 测试is_over
    """
    cnt = 0
    for one in input_data:
        hongshuai = 5
        heijiang = 21

        init = num_split(one["init"], 2)
        
        if one["color"] == -1 and one["result"] == -1:
            init[heijiang-1] = "99"
            
        elif one["color"] == 1 and one["result"] == 1:
            init[hongshuai-1] = "99"
            
        new_init = ''.join(init)
        res = ChessCheck.is_over(new_init)
        if res != one["color"]:
            cnt +=1 
            print('res: ', res)
            print(one)
            print("## ", cnt)
    """
    
    # 测试get_random_move和move
    init_default = "8979695949392919097717866646260600102030405060708012720323436383"
    ori_mat = ChessCheck.code_to_matrix(init_default)
    ori_init = init_default
    mat = ori_mat
    new_init = ori_init
    n = 6
    color = -1
    over = 0
    while over == 0:
        ori_mat = mat
        ori_init = new_init
        move = PlayChess.get_random_move(ori_init, color)
        new_init = PlayChess.move(ori_init, move)
        mat = ChessCheck.code_to_matrix(new_init)
        if color == -1:
            color = 1
        else:
            color = -1
        over = ChessCheck.is_over(new_init)
        print("=========================================")
        print(ori_mat)
        print(move)
        print(mat)
        print("=========================================")
    print("winer: ", over)



