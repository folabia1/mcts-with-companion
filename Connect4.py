# Connect 4 u1806475
import numpy as np
from copy import copy, deepcopy
from config import CONFIG
from mcts import ConnectFourState, MinimaxPlayer, RandomPlayer
import mcts
import mcts2

# Setup Game
board = np.empty(CONFIG.boardSize, dtype=str)
initialState = ConnectFourState(board=board,
                                player=CONFIG.turn[0],
                                movesPlayed=0)

# Create Player Objects
players = {}
def createPlayers():
    global players
    players = {}
    for player, mode in CONFIG.modes.items():
        if mode == "random":
            players[player] = RandomPlayer(deepcopy(initialState))
        if "minimax" in mode:
            sightLimit = int(mode.replace("minimax", ""))
            players[player] = MinimaxPlayer(player, deepcopy(initialState), sightLimit)
        if "mcts" in mode:
            mctsType = int(mode.replace("mcts", ""))
            if mctsType == 1:
                players[player] = mcts.MCTSPlayer(player, deepcopy(initialState), timeLimit=CONFIG.mctsTimeLimit, iterationLimit=CONFIG.mctsIterationLimit)
            elif mctsType == 2:
                players[player] = mcts2.MCTSPlayer(player, deepcopy(initialState), timeLimit=CONFIG.mctsTimeLimit, iterationLimit=CONFIG.mctsIterationLimit)

def placeToken(column, team, board):
    height = CONFIG.boardSize[0]
    for row in range(height-1, -1, -1):
        if board[row][column] == "":
            board[row][column] = team[0]
            return True
            break
    return False

def play(player, board, description):
    action = players[player].determineNextAction(description=description)
    # print(CONFIG.teams[player])
    placeToken(action, CONFIG.teams[player], board)
    for playerObject in players.values():
        playerObject.logAction(action, player)

def checkForWin():
    # global board
    height = CONFIG.boardSize[0]
    length = CONFIG.boardSize[1]
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

def run(description=False):
    global board
    global players
    gameResult = None
    movesPlayed = 0
    currentPlayer = None
    createPlayers()
    board = np.empty(CONFIG.boardSize, dtype=str)

    if description:
        print("CONNECT 4\n")
    while gameResult == None:
        # next player plays
        currentPlayer = CONFIG.turn[movesPlayed%len(CONFIG.turn)]
        play(currentPlayer, board, description)
        if description:
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

    if gameResult == "DRAW":
        if description:
            print(f"Game ended in a DRAW after {movesPlayed} moves")
            print(board)
        return "DRAW", movesPlayed
    else:
        if description:
            print(f"Winner is: {CONFIG.teams[currentPlayer]} after {movesPlayed} moves")
            print(board)
        return CONFIG.teams[currentPlayer], movesPlayed

# run(description=True)
