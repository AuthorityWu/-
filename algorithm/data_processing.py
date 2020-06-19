import json
import os

# print(os.getcwd()) #获取当前工作目录路径
# print(os.path.abspath('.')) #获取当前工作目录路径
input_path = "../test_data.json"
output_path = "../output_chessdata.json"

with open(input_path, "r") as f:
    input_data = json.load(f)

output_data = []


def num_split(string, step):
    """
    数字分割
    """

    temp1 = '-'.join(string)
    temp2 = temp1.split('-')
    len_t = int(len(temp2)/step)
    res = \
        [ ''.join(temp2[i*step : (i+1)*step]) for i in range(len_t)]
    return res


def data_process(input_data):
    """
    棋局数据处理
    """
    init_default = "8979695949392919097717866646260600102030405060708012720323436383"

    for one in input_data:

        # init 分割
        if one["init"] == "":
            init = num_split(init_default, step=2)
        else:
            init = num_split(one["init"], step=2)
        # move_list 分割
        move_list = num_split(one["move_list"], step=4)
        
        result = 0
        if one["result"] == "红胜":
            result = -1
        elif one["result"] == "黑胜":
            result = 1

        # 模拟棋局
        for move in move_list:
            ind = init.index(move[:2])
            if ind < 16:
                color = -1
            else:
                color = 1
            
            status = {
                "init" : ''.join(init),
                "move" : move,
                "color" : color,
                "result" : result
            }
            output_data.append(status)
            # print(status)
            # 执行下棋
            if move[2:4] in init:
                eat_ind = init.index(move[2:4])
                init[eat_ind] = "99"
            init[ind] = move[2:4]


if __name__ == "__main__":    
    data_process(input_data)

    with open(output_path,"w") as f:
        json.dump(output_data, f)
