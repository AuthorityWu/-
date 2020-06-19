from chess_check import *
import json 
import os
from data_processing import *
import numpy as np

input_path = "../data/output_chessdata.json"

with open(input_path, "r") as f:
    input_data = json.load(f)


if __name__ == "__main__":    
    # 测试is_legal
    cnt = 0
    for one in input_data:
        # 制作错误动作测试
        # y = np.random.randint(0,9)
        # x = np.random.randint(0,8)
        # one["move"] = one["move"][0:2]+str(x)+str(y)
        
        matrix = ChessCheck.code_to_matrix(one["init"])
        res = ChessCheck.is_legal(one["init"], matrix, one["move"], one["color"])
        
        if not res:
            print(res)
            cnt +=1 
            print(matrix)
            print(one)
            print("## ", cnt)
    
    # 测试is_over
    # cnt = 0
    # for one in input_data:
    #     hongshuai = 5
    #     heijiang = 21

    #     init = num_split(one["init"], 2)
        
    #     if one["color"] == -1 and one["result"] == -1:
    #         init[heijiang-1] = "99"
            
    #     elif one["color"] == 1 and one["result"] == 1:
    #         init[hongshuai-1] = "99"
            
    #     new_init = ''.join(init)
    #     res = ChessCheck.is_over(new_init)
    #     if res != one["color"]:
    #         cnt +=1 
    #         print('res: ', res)
    #         print(one)
    #         print("## ", cnt)

