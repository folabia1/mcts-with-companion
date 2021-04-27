class Config:
    def __init__(self):
        self.turn = ["A", "B", "C", "B"]
        self.teams = {"A": "RED", "B": "GREEN", "C": "RED"}
        self.modes = {"A": "random", "B": "minimax6", "C": "random"}
        self.boardSize = (6,7)

CONFIG = Config()
