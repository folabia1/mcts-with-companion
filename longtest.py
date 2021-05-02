from Connect4 import *
from config import CONFIG

numGames = 100

results = {"DRAW":[0,0]}
for player in CONFIG.turn:
    results[CONFIG.teams[player]] = [0,0]

for i in range(1,numGames+1,1):
    print(f"Game {i}")
    gameResult = run(description=False)
    print(gameResult)
    results[gameResult[0]][0] += 1
    results[gameResult[0]][1] += gameResult[1]

for result in results.values():
    result[1] = result[1]/numGames

print(results)
