# Connect 4 u1806475
import numpy as np
from random import randint

moves_played = 0
turn = ["A", "B", "C", "B"]
teams = {"A": "RED", "B": "BLUE", "C": "RED"}
modes = {"A": "random", "B": "random", "C": "random"}
# TODO: Create MCTS object class
# if modes["A"] == "mcts":
    # initialise mcts object
    
board_size = (6,7)
board = np.empty(board_size, dtype=str)
game_result = None


def place_token(column, team):
    global board
    height = board.shape[0]
    for row in range(height-1, -1, -1):
        if board[row][column] == "":
            board[row][column] = team
            return True
    return False

def play(player):
    global board
    global modes
    global teams
    if modes[player] == "random":
        while not place_token(randint(0, board.shape[0]-1), teams[player]):
            continue
    # TODO: implement limited sight minimax player
    # if "minimax" in modes[player]:
        # sight_level = modes[player].replace("minimax", "")[-1]
    # TODO: implement different mcts player types
    # if "mcts" in modes[player]:
    #     mcts_type = modes[player]

def check_for_win():
    global board
    height = board.shape[0]
    length = board.shape[1]
    for row in range(height-1, -1, -1):
        for column in range(length):
            initial = board[row][column]
            if initial == "":
                continue
            # check up
            if row >= 3:
                for i in range(1,4):
                    if (board[row-i][column] != initial):
                        break
                    if i == 3:
                        return initial
                # check up and left diagonal
                if column >= 3:
                    for i in range(1,4):
                        if board[row-i][column-i] != initial:
                            break
                        if i == 3:
                            return initial
                # check up and right diagonal
                if column <= length-4:
                    for i in range(1,4):
                        if board[row-i][column+i] != initial:
                            break
                        if i == 3:
                            return initial
            # check right
            if column <= length-4:
                for i in range(1,4):
                    if board[row][column+i] != initial:
                        break
                    if i == 3:
                        return initial
    return None


while game_result == None:
    current_player = turn[moves_played%len(turn)]
    play(current_player)
    game_result = check_for_win()
    if game_result:
        break
    moves_played += 1
    if moves_played >= board_size[0]*board_size[1]:
        game_result = "DRAW"

print(board)
if game_result == "DRAW":
    print(f"Game ended in a DRAW after {moves_played} moves")
else:
    print(f"Winner is: {game_result} after {moves_played} moves")
