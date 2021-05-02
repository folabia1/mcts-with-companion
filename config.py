class Config:
    def __init__(self):
        self.turn = ["B", "A"]
        self.teams = {"A": "RED", "B": "GREEN", "C": "MCTS"}
        self.modes = {"A": "mcts1", "B": "mcts1", "C": "random"}
        self.boardSize = (6,7)
        self.mctsTimeLimit = None # in milliseconds
        self.mctsIterationLimit = 1000

CONFIG = Config()
