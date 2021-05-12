from __future__ import division
from config import CONFIG
from copy import copy, deepcopy
import time
import math
import random
from scipy.special import softmax
import numpy as np
import operator

# full-depth random simulation policy to a leaf node for MCTS, converging to Minimax
def randomPolicy(state, player, targetDepth):
    currentState = deepcopy(state)
    currentDepth = 0
    if targetDepth:
        while not currentState.isTerminal() and currentDepth < targetDepth:
            currentState = random.choice([currentState.takeAction(action) for action in currentState.getPossibleActions()])
            currentDepth += 1
    else:
        while not currentState.isTerminal():
            currentState = random.choice([currentState.takeAction(action) for action in currentState.getPossibleActions()])
            currentDepth += 1
    return currentDepth, currentState.calculateReward(player)[0]

def UCB1(node, explorationConstant):
    if node.numVisits == 0:
        return float("inf")
    averageReward = node.getAvgReward()
    return averageReward + explorationConstant*math.sqrt(math.log(node.parent.numVisits)/node.numVisits)

class MCTSNode():
    def __init__(self, state, parent=None):
        self.state = state
        self.isTerminal = self.state.isTerminal()
        self.isFullyExpanded = False
        self.parent = parent
        self.children = {}
        self.numVisits = 0
        self.totalReward = 0

    def getAvgReward(self):
        if self.numVisits == 0:
            return float("inf")
        return self.totalReward/self.numVisits

    def expand(self):
        if self.isFullyExpanded:
            return self.children
        else:
            actions = self.state.getPossibleActions()
            for action in actions:
                newNode = MCTSNode(self.state.takeAction(action), self)
                self.children[action] = newNode
            self.isFullyExpanded = True
            return self.children

    # def __str__(self):
    #     s=[]
    #     s.append("totalReward: %s"%(self.totalReward))
    #     s.append("numVisits: %d"%(self.numVisits))
    #     s.append("isTerminal: %s"%(self.isTerminal))
    #     s.append("possibleActions: %s"%(self.children.keys()))
    #     return f"{self.__class__.__name__}: {s}"


class MCTSPlayer():
    def __init__(self, player, state, config=CONFIG, timeLimit=None, iterationLimit=None, explorationConstant=500, rolloutPolicy=randomPolicy,
                 playerSightLimit=None, estCompSightLimit=3, maxEstCompSightLimit=6, multiplier=None):
        self.player = player
        self.root = MCTSNode(state, None)
        self.explorationConstant = explorationConstant
        self.playerSightLimit = playerSightLimit
        self.rollout = rolloutPolicy
        self.maxEstimatedSightLevelIncorrect = 0
        if multiplier:
            self.multiplier = multiplier
        else:
            self.multiplier = 1.5
        # calculate shortest number of turns to each other player
        turnsToPlayer = {}
        for i in range(len(config.order)):
            if config.order[i] != self.player:
                for j in range(1, len(config.order), 1):
                    if config.order[(i-j)%len(config.order)] == self.player:
                        turnsToPlayer[config.order[i]] = j
                        break
        self.companions = {playr:[MCTSNode(deepcopy(state), None),estCompSightLimit,maxEstCompSightLimit,turnsToPlayer[playr]] for playr in config.order if playr != self.player and config.teams[playr] == config.teams[self.player]}
        self.correctPredictions = {}
        for playr in self.companions.keys():
            self.correctPredictions[playr] = {}
            for i in range (1,maxEstCompSightLimit+1,1):
                self.correctPredictions[playr][i] = 0

        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            self.timeLimit = timeLimit # time in milliseconds
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'

    def search(self, description=False):
        self.root.expand()
        if description:
            print(f"\n[Player {self.player}] Beginning Monte-Carlo Tree Search")

        # search until time limit
        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                # Full Depth MCTS
                self.executeRound(self.root, self.player, self.playerSightLimit)

        # search until iteration limit
        else:
            startTime = time.time()
            for i in range(self.searchLimit):
                # Full Depth MCTS
                self.executeRound(self.root, self.player, self.playerSightLimit)
            endTime = time.time()
            print(f"Time to execute {self.searchLimit} iterations: {endTime-startTime}s")

        rootChildrenByAvgRewards = {k: round(v, 3) for k, v in self.orderChildrenByAvgRewards(self.root).items()}
        rootChildrenByConfidence = {k: round(v, 6) for k, v in self.orderChildrenByConfidence(self.root).items()}
        if description:
            print(f"MCTS COMPLETE: {'Time' if self.limitType == 'time' else 'Iteration'} Limit Reached")
            print(f"{self.player} Rewards:", rootChildrenByAvgRewards)
            print(f"{self.player} Confidence:", rootChildrenByConfidence)
        action = max(rootChildrenByConfidence.items(), key=operator.itemgetter(1))[0]
        return action

    def executeRound(self, root, player, sightLimit):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        # select & expand
        node = self.selectNode(root)
        # simulation
        depth, reward = self.rollout(node.state, player, sightLimit)
        # backpropagation
        self.backpropogate(node, reward, depth)


    def selectNode(self, root):
        currentNode = root
        while currentNode.children:
            currentNode = self.getBestChild(currentNode, self.explorationConstant)
        if currentNode.numVisits == 0:
            return currentNode
        else:
            currentNode.expand()
            if not list(currentNode.children.values()):
                return currentNode
            currentNode = random.choice(list(currentNode.children.values()))
            return currentNode

    def backpropogate(self, node, reward, depth):
        for playerInfo in self.companions.values():
            if depth <= playerInfo[1] + playerInfo[3]:
                reward *= self.multiplier
        currentNode = node
        while currentNode is not None:
            currentNode.numVisits += 1
            currentNode.totalReward += reward
            if currentNode.parent:
                currentNode = currentNode.parent
            else:
                break

    def getBestChild(self, node, explorationConstant):
        bestValue = float("-inf")
        bestNodes = []
        children = node.children.values()
        for child in children:
            nodeValue = UCB1(child, explorationConstant)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getBestActions(self, node, explorationConstant):
        bestValue = float("-inf")
        bestActions = []
        for action, child in node.children.items():
            nodeValue = UCB1(child, explorationConstant)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestActions = [action]
            elif nodeValue == bestValue:
                bestActions.append(action)
        return bestActions

    def getChildrenAvgRewards(self, node):
        rewards = {}
        for action, child in node.children.items():
            if child.numVisits == 0:
                rewards[action] = 0
            else:
                rewards[action] = child.totalReward/child.numVisits
        return rewards

    def orderChildrenByAvgRewards(self, node):
        rewards = self.getChildrenAvgRewards(node)
        orderedRewards = {action: avgReward for action, avgReward in sorted(rewards.items(), key=lambda item: item[1], reverse=True)}
        return orderedRewards

    def orderChildrenByConfidence(self, node):
        rewards = self.getChildrenAvgRewards(node)
        confidenceList = softmax(list(rewards.values()))
        confidenceDict = {list(rewards.keys())[i]:confidenceList[i] for i in range(len(rewards.keys()))}
        orderedConfidence = {action: avgReward for action, avgReward in sorted(confidenceDict.items(), key=lambda item: item[1], reverse=True)}
        return orderedConfidence

    def determineNextAction(self, description=False):
        nextAction = self.search(description=description)
        return nextAction

    def logAction(self, action, player, description=False):
        # check expected player is playing
        if player != self.root.state.currentPlayer:
            print("\n\nUnexpected Player!\n\n")
            return None
        else:
            if player in self.companions.keys():
                # predict companion's move for each sight level upto maxEstimatedSightLevel
                predictedActions = {}
                maxEstimatedSightLevel = self.companions[player][2]
                if self.limitType == 'time': # search until time limit
                    for estimatedSightLevel in range(1, maxEstimatedSightLevel+1, 1):
                        tempNode = MCTSNode(deepcopy(self.root.state), None)
                        timeLimit = time.time() + (self.timeLimit/maxEstimatedSightLevel) / 1000
                        while time.time() < timeLimit:
                            self.executeRound(tempNode, player, estimatedSightLevel)
                        predictedActions[estimatedSightLevel] = self.getBestActions(tempNode, 0)
                else: # search until iteration limit
                    for estimatedSightLevel in range(1, maxEstimatedSightLevel+1, 1):
                        tempNode = MCTSNode(deepcopy(self.root.state), None)
                        for i in range(self.searchLimit//maxEstimatedSightLevel):
                            self.executeRound(tempNode, player, estimatedSightLevel)
                        predictedActions[estimatedSightLevel] = self.getBestActions(tempNode, 0)

                # increase lambda evidence for correct predictions
                for sightLimit, predActions in predictedActions.items():
                    if action in predActions:
                        self.correctPredictions[player][sightLimit] +=1
                        # if maxEstCompSightLimit was correct
                        if sightLimit == self.companions[player][2]:
                            # increase maxEstCompSightLimit by 3
                            self.companions[player][2] += 3
                            for i in range(1, 4, 1):
                                self.correctPredictions[player][sightLimit+i] = 0
                            self.maxEstimatedSightLevelIncorrect = 0
                        # update estimated sight level of companion if necessary
                        if self.correctPredictions[player][sightLimit] > self.correctPredictions[player][self.companions[player][1]]:
                             self.companions[player][1] = sightLimit
                    else:
                        if sightLimit == self.companions[player][2]:
                            self.maxEstimatedSightLevelIncorrect += 1
                            if self.maxEstimatedSightLevelIncorrect >= 5: # adjust to change rate of reduction of maxEstimatedSightLevel
                                self.companions[player][2] -= 1
                                del self.correctPredictions[player][sightLimit]
                                self.maxEstimatedSightLevelIncorrect = 0
                                break

                if description:
                    print(f"---Player {self.player} Predictions---")
                    print(f"predictedActions={predictedActions}")
                    print(f"cumulativeCorrectPredictions={self.correctPredictions}")
                    print(f"estimatedSightLimit={self.companions[player][1]}")

            # update root node
            self.root.expand()
            self.root = self.root.children[action]
            for companion in self.companions.values():
                companion[0].expand()
                companion[0] = companion[0].children[action]
            return self.root.state

    def reset(self, state):
        self.root = MCTSNode(state, None)
        for companion in self.companions.values():
            companion[0] = MCTSNode(deepcopy(state), None)
