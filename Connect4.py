from copy import copy, deepcopy
from config import CONFIG

class ConnectFourState():
    def __init__(self, board, player, movesPlayed):
        if board is None:
            self.board = np.empty(CONFIG.boardSize, dtype=str)
        else:
            self.board = board
        self.currentPlayer = player
        self.movesPlayed = movesPlayed

    def getPossibleActions(self):
        possibleActions = []
        for column in range(self.board.shape[1]):
            if self.board[0][column] == "":
                possibleActions.append(column)
        return possibleActions

    def takeAction(self, action):
        height = CONFIG.boardSize[0]
        newState = ConnectFourState(board=copy(self.board), player=self.getNextPlayer(), movesPlayed=self.movesPlayed+1)
        for row in range(height-1, -1, -1):
            if newState.board[row][action] == "":
                newState.board[row][action] = CONFIG.teams[self.currentPlayer]
                return newState
        return None

    def getNextPlayer(self):
        return CONFIG.order[(self.movesPlayed+1)%len(CONFIG.order)]

    def isTerminal(self):
        return self.calculateReward(self.currentPlayer)[1]

    def calculateReward(self, player):
        # based on domain knowledge about the position
        playerTeam = CONFIG.teams[player]
        height = CONFIG.boardSize[0]
        length = CONFIG.boardSize[1]
        threeOutOfFours = 0
        twoOutOfFours = 0
        boardFull = True
        # points = 0
        for row in range(height-1, -1, -1):
            for column in range(length):
                initial = self.board[row][column]
                if initial == "":
                    boardFull = False
                    continue

                if playerTeam[0] == initial:
                    multiplier = 1
                else:
                    multiplier = -1
                # check up
                if row >= 3:
                    tally = 1
                    for i in range(1,4):
                        if self.board[row-i][column] == initial:
                            tally += 1
                        elif self.board[row-i][column] not in (initial, ""):
                            tally = 1
                            break
                    if tally == 2:
                        twoOutOfFours += 1 * multiplier
                    elif tally == 3:
                        threeOutOfFours += 1 * multiplier
                    elif tally == 4:
                        return 100*multiplier, "WIN"
                    # check up and left diagonal
                    if column >= 3:
                        tally = 1
                        for i in range(1,4):
                            if self.board[row-i][column-i] == initial:
                                tally += 1
                            elif self.board[row-i][column-i] not in (initial, ""):
                                tally = 1
                                break
                        if tally == 2:
                            twoOutOfFours += 1 * multiplier
                        elif tally == 3:
                            threeOutOfFours += 1 * multiplier
                        elif tally == 4:
                            return 100*multiplier, "WIN"
                    # check up and right diagonal
                    if column <= length-4:
                        tally = 1
                        for i in range(1,4):
                            if self.board[row-i][column+i] == initial:
                                tally += 1
                            elif self.board[row-i][column+i] not in (initial, ""):
                                tally = 1
                                break
                        if tally == 2:
                            twoOutOfFours += 1 * multiplier
                        elif tally == 3:
                            threeOutOfFours += 1 * multiplier
                        elif tally == 4:
                            return 100*multiplier, "WIN"
                # check right
                if column <= length-4:
                    tally = 1
                    for i in range(1,4):
                        if self.board[row][column+i] == initial:
                            tally += 1
                        elif self.board[row][column+i] not in (initial, ""):
                            tally = 1
                            break
                    if tally == 2:
                        twoOutOfFours += 1 * multiplier
                    elif tally == 3:
                        threeOutOfFours += 1 * multiplier
                    elif tally == 4:
                        return 100*multiplier, "WIN"
        if boardFull:
            return 0, "DRAW"
        points = max(-99, min(10*threeOutOfFours + 5*twoOutOfFours, 99))
        return points, None
