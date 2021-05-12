from main import run
import config
import numpy as np

order1 = ["R1", "B1", "R2", "B1"]
order2 = ["R2", "B1", "R1", "B1"]
order3 = ["B1", "R1", "B1", "R2"]
order4 = ["B1", "R2", "B1", "R1"]

teams = {"R1": "RED", "B1": "BLUE", "R2": "RED"}
modes2a = {"R1": "mctsDS:3:", "B1": "minimax3", "R2": "minimax3"}
modes2b = {"R1": "mctsDS::", "B1": "minimax3", "R2": "minimax3"}
modes2c = {"R1": "mctsDA::", "B1": "minimax3", "R2": "minimax3"}
modes2d = {"R1": "mctsDB::", "B1": "minimax3", "R2": "minimax3"}

modes2e = {"R1": "mctsCS:3:", "B1": "minimax3", "R2": "minimax3"}
modes2f = {"R1": "mctsCS::", "B1": "minimax3", "R2": "minimax3"}
modes2g = {"R1": "mctsCA::", "B1": "minimax3", "R2": "minimax3"}
modes2h = {"R1": "mctsCB::", "B1": "minimax3", "R2": "minimax3"}

mctsIterationLimit = 3000

orders = [order1, order2, order3, order4]
modesList = {"2a": modes2a, "2b": modes2b, "2c": modes2c, "2d": modes2d,
             "2e": modes2e, "2f": modes2f, "2g": modes2g, "2h": modes2h}

for testName, modes in modesList.items():
    print(f"Test {testName}")
    for order in orders:
        config1 = config.Config(order, teams, modes, mctsIterationLimit=mctsIterationLimit)
        run(description=False, config=config1, numGames=10)
