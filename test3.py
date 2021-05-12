from main import run
import config
import numpy as np

order1 = ["R1", "B1"]
order2 = ["B1", "R1"]

teams = {"R1": "RED", "B1": "BLUE"}
modes3a = {"R1": "mctsCS::", "B1": "minimax3"}
modes3b = {"R1": "mctsDS::", "B1": "minimax3"}
modes3c = {"R1": "mctsCS::", "B1": "mctsDS::"}

mctsIterationLimit = 3000

orders = [order1, order2]
modesList = {"3a": modes3a, "3b": modes3b, "3c": modes3c}

for testName, modes in modesList.items():
    print(f"Test {testName}")
    for order in orders:
        config1 = config.Config(order, teams, modes, mctsIterationLimit=mctsIterationLimit)
        run(description=False, config=config1, numGames=10)
