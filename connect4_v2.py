from copy import copy, deepcopy
from config import CONFIG

class ConnectFourState():
    def __init__(self, board, player, movesPlayed, config=CONFIG):
        self.config = config
        if board is None:
            self.board = np.empty(self.config.boardSize, dtype=str)
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
        height = self.config.boardSize[0]
        newState = ConnectFourState(board=copy(self.board), player=self.getNextPlayer(), movesPlayed=self.movesPlayed+1, config=self.config)
        for row in range(height-1, -1, -1):
            if newState.board[row][action] == "":
                newState.board[row][action] = self.config.teams[self.currentPlayer]
                return newState
        return None

    def getNextPlayer(self):
        return self.config.order[(self.movesPlayed+1)%len(self.config.order)]

    def isTerminal(self):
        return self.calculateReward(self.currentPlayer)[1]

    def calculateReward(self, player):
        # based on domain knowledge about the position
        playerTeam = self.config.teams[player]
        height = self.config.boardSize[0]
        length = self.config.boardSize[1]
        count = {1:0, 2:0, 3:0}

        # find all views
        views = []
        for row in range(height-1, -1, -1):
            for column in range(length):
                if row >= 3: # straight up
                    views.append([self.board[row-i][column] for i in range(4)])
                    if column >= 3: # up-left diagonal
                        views.append([self.board[row-i][column-i] for i in range(4)])
                    if column <= length-4: # up-right diagonal
                        views.append([self.board[row-i][column+i] for i in range(4)])
                if column <= length-4: # straight right
                    views.append([self.board[row][column+i] for i in range(4)])

        # evaluate each view
        for view in views:
            teamsInView = list(set([x for x in view if x != ""]))
            # print(teamsInView)
            if len(teamsInView) == 1:
                tally = view.count(teamsInView[0])
                multiplier = 1 if teamsInView[0] == playerTeam[0] else -1
                if tally == 4:
                    return 100*multiplier, "WIN"
                else:
                    count[tally] += 1*multiplier


        # check whether board is full
        if self.movesPlayed == self.config.boardSize[0]*self.config.boardSize[1]:
            return 0, "DRAW"

        # return reward of state
        points = max(-99, min(10*count[3] + 2*count[2] + 0*count[1], 99))
        return points, None
