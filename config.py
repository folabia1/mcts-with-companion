import random

class Config:
    def __init__(self, order, teams, modes, boardSize=(6,7),
                 mctsTimeLimit=None, mctsIterationLimit=None):
        self.order = order
        self.teams = teams
        self.modes = modes
        self.boardSize = boardSize
        self.mctsTimeLimit = mctsTimeLimit # in milliseconds
        self.mctsIterationLimit = mctsIterationLimit

    def shuffleOrder(self):
        remainingPlayers = self.order
        shuffledOrder = []
        nextPlayer = random.choice(remainingPlayers)
        shuffledOrder.append(nextPlayer)
        remainingPlayers.remove(nextPlayer)
        while len(remainingPlayers) > 0:
            availablePlayers = [player for player in remainingPlayers
                                if self.teams[player] != self.teams[shuffledOrder[-1]]]
            nextPlayer = random.choice(availablePlayers)
            shuffledOrder.append(nextPlayer)
            remainingPlayers.remove(nextPlayer)
        self.order = shuffledOrder

order = ["R1", "B1"]
teams = {"R1": "RED", "B1": "BLUE", "R2": "RED"}
modes = {"R1": "mctsDA::", "B1": "minimax3", "R2": "mctsC"}
mctsIterationLimit = 3000
CONFIG = Config(order, teams, modes, mctsIterationLimit=mctsIterationLimit)
