# Connect 4 u1806475
import numpy as np
from copy import copy, deepcopy
from config import CONFIG
from mcts import ConnectFourState, MinimaxPlayer, RandomPlayer

board = np.empty(CONFIG.boardSize, dtype=str)
movesPlayed = 0
gameResult = None
currentState = ConnectFourState(board=board,
                                player=CONFIG.turn[0],
                                movesPlayed=movesPlayed)

# Create Player Objects
players = {}
for player, mode in CONFIG.modes.items():
    if mode == "random":
        players[player] = RandomPlayer(deepcopy(currentState))
    if "minimax" in mode:
        sightLimit = int(mode.replace("minimax", ""))
        players[player] = MinimaxPlayer(player, deepcopy(currentState), sightLimit)
    # if mode == "mcts":
    #     players[player] = MCTSPlayer()
# print(players)

def placeToken(column, team, board):
    height = CONFIG.boardSize[0]
    for row in range(height-1, -1, -1):
        if board[row][column] == "":
            board[row][column] = team
            return True
            break
    return False

def play(player, board):
    action = players[player].determineNextAction()
    # print(CONFIG.teams[player])
    placeToken(action, CONFIG.teams[player], board)
    for playerObject in players.values():
        playerObject.logAction(action, player)

def checkForWin():
    # global board
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


while gameResult == None:
    # next player plays
    currentPlayer = CONFIG.turn[movesPlayed%len(CONFIG.turn)]
    play(currentPlayer, board)
    print(currentPlayer)
    print(board)
    movesPlayed += 1
    # check for a win
    gameResult = checkForWin()
    if gameResult:
        break
    # check whether board is full
    if movesPlayed >= CONFIG.boardSize[0]*CONFIG.boardSize[1]:
        gameResult = "DRAW"

print(board)
if gameResult == "DRAW":
    print(f"Game ended in a DRAW after {movesPlayed} moves")
else:
    print(f"Winner is: {gameResult} after {movesPlayed} moves")
