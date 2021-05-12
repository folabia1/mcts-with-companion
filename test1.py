from main import run
import config
import numpy as np

order1 = ["R1", "B1"]
order2 = ["B1", "R1"]
teams = {"R1": "RED", "B1": "BLUE"}

modes1a = {"R1": "minimax1", "B1": "minimax3"}
modes1b = {"R1": "minimax3", "B1": "minimax3"}
modes1c = {"R1": "minimax5", "B1": "minimax3"}

modes1d = {"R1": "mctsDS:1:", "B1": "minimax3"}
modes1e = {"R1": "mctsDS:3:", "B1": "minimax3"}
modes1f = {"R1": "mctsDS:5:", "B1": "minimax3"}
modes1g = {"R1": "mctsDS::", "B1": "minimax3"}

modes1h = {"R1": "mctsCS:1:", "B1": "minimax3"}
modes1i = {"R1": "mctsCS:3:", "B1": "minimax3"}
modes1j = {"R1": "mctsCS:5:", "B1": "minimax3"}
modes1k = {"R1": "mctsCS::", "B1": "minimax3"}

mctsIterationLimit = 3000

orders = [order1, order2]
modesList = {"1a": modes1a, "1b": modes1b, "1c": modes1c, "1d": modes1d, "1e": modes1e,
             "1f": modes1f, "1g": modes1g, "1h": modes1h, "1i": modes1i, "1j": modes1j, "1k": modes1k}

for testName, modes in modesList.items():
    print(f"Test {testName}")
    for order in orders:
        config1 = config.Config(order, teams, modes, mctsIterationLimit=mctsIterationLimit)
        run(description=False, config=config1, numGames=10)
