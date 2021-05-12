# Connect 4 u1806475
import numpy as np
from copy import deepcopy
from config import CONFIG
from connect4_v2 import ConnectFourState
import randomPlayer
import minimaxPlayer
import mctsPlayerConserveA, mctsPlayerConserveB, mctsPlayerConserveSolo
import mctsPlayerDiscardA, mctsPlayerDiscardB, mctsPlayerDiscardSolo

# create player objects from the config
def createPlayers(config):
    emptyBoard = np.empty(config.boardSize, dtype=str)
    initialState = ConnectFourState(board=emptyBoard,
                                    player=config.order[0],
                                    movesPlayed=0,
                                    config=config)
    players = {}
    for player in config.order:
        if config.modes[player] == "random":
            players[player] = randomPlayer.RandomPlayer(deepcopy(initialState))
        elif "minimax" in config.modes[player]:
            sightLimit = int(config.modes[player].replace("minimax", ""))
            players[player] = minimaxPlayer.MinimaxPlayer(player, deepcopy(initialState), config=config, sightLimit=sightLimit)
        elif "mcts" in config.modes[player]:
            mctsType = config.modes[player].replace("mcts", "").split(":") # mode:sightLimit:multiplier
            sightLimit = int(mctsType[1]) if mctsType[1] else None
            if "CA" == mctsType[0]:
                players[player] = mctsPlayerConserveA.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit)
            elif "CB" == mctsType[0]:
                multiplier = float(mctsType[2]) if mctsType[2] else None
                players[player] = mctsPlayerConserveB.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit, multiplier=multiplier)
            elif "CS" == mctsType[0]:
                players[player] = mctsPlayerConserveSolo.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit)
            elif "DA" == mctsType[0]:
                players[player] = mctsPlayerDiscardA.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit)
            elif "DB" == mctsType[0]:
                multiplier = float(mctsType[2]) if mctsType[2] else None
                players[player] = mctsPlayerDiscardB.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit, multiplier=multiplier)
            elif "DS" == mctsType[0]:
                players[player] = mctsPlayerDiscardSolo.MCTSPlayer(player, deepcopy(initialState), config=config, timeLimit=config.mctsTimeLimit,
                                                                iterationLimit=config.mctsIterationLimit, playerSightLimit=sightLimit)
    return players


def placeToken(column, team, board):
    height = len(board)
    for row in range(height-1, -1, -1):
        if board[row][column] == "":
            board[row][column] = team[0]
            return True
            break
    return False

def play(player, board, description, config, players):
    action = players[player].determineNextAction(description=description)
    if description:
        print(f"{player} plays {action}")
    # print(CONFIG.teams[player])
    placeToken(action, config.teams[player], board)
    for playerObject in players.values():
        playerObject.logAction(action, player, description=description)

def checkForWin(board):
    height = len(board)
    length = len(board[0])
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

def run(description=False, config=CONFIG, numGames=1):
    print(config.order)
    print(config.teams)
    print(config.modes)

    emptyBoard = np.empty(config.boardSize, dtype=str)
    initialState = ConnectFourState(board=emptyBoard,
                                    player=config.order[0],
                                    movesPlayed=0,
                                    config=config)

    players = createPlayers(config)
    # set up results table
    results = {"DRAW":[0,0]}
    for player in config.order:
        results[config.teams[player]] = [0,0]

    for i in range(1, numGames+1, 1):
        print(f"Game {i}")
        gameResult = None
        gameInfo = None
        movesPlayed = 0
        currentPlayer = None
        board = np.empty(config.boardSize, dtype=str)
        for player in players.values():
            player.reset(deepcopy(initialState))
        if description:
            print("CONNECT 4")
            print(f"Order: {config.order}")
        while gameResult == None:
            # next player plays
            currentPlayer = config.order[movesPlayed%len(config.order)]
            play(currentPlayer, board, description, config, players)
            if description:
                # print(f"Moves Played: {movesPlayed}")
                print(board)
            movesPlayed += 1
            # check for a win
            gameResult = checkForWin(board)
            if gameResult:
                break
            # check whether board is full
            if movesPlayed >= config.boardSize[0]*config.boardSize[1]:
                gameResult = "DRAW"

        if gameResult == "DRAW":
            if description:
                print(f"Game ended in a DRAW after {movesPlayed} moves")
                print(board)
            gameInfo = "DRAW", movesPlayed
        else:
            if description:
                print(f"Winner is: {config.teams[currentPlayer]} after {movesPlayed} moves")
                print(board)
            gameInfo = config.teams[currentPlayer], movesPlayed

        print(gameInfo)
        results[gameInfo[0]][0] += 1 # increment number of wins for winner
        results[gameInfo[0]][1] += gameInfo[1] # increase total moves played to win for winning player

    for result in results.values():
        # convert total moves to win into average number of moves to win
        result[1] = 0 if result[0] == 0 else result[1]/result[0]

    print(results)
    print("\n")
# run(description=True)
