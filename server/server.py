import os
print(os.getcwd()) #获取当前工作目录路径
print(os.path.abspath('.')) #获取当前工作目录路径

import sys
sys.path.append(".")

from flask import Flask, jsonify, request, abort

from algorithm.play_chess import *
from algorithm.chess_check import *
from algorithm.SQLUtil import *

app = Flask(__name__)

@app.route('/getMove')
def get_move():
    code=request.args.get('code')
    color=int(request.args.get('color'))
    print("code: ", code)
    move = PlayChess.get_move(code,color)
    
    if move is None:
        move = PlayChess.get_random_move(code,color)

    new_code = PlayChess.move(code,move)

    return jsonify({
        'new_code':new_code,
        'move':move
        })

@app.route('/isLegal')
def is_legal():
    code=request.args.get('code')
    move=request.args.get('move')

    flag = ChessCheck.is_legal(code,move)

    return jsonify({
        'flag':flag
        })

@app.route('/isOver')
def is_over():
    code=request.args.get('code')

    color=ChessCheck.is_over(code)

    return jsonify({
        'color':color
        })

@app.route('/learn')
def learn():
    code=request.args.get('code')
    move=request.args.get('move')

    add_record(code, move)
    return jsonify({
        'message': 'success'
        }) 

if __name__ == "__main__":
    app.run()