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
def randomPolicy(node, player, currentDepth, targetDepth):
    # node passed as parameter must not be fully simulated
    # currentNode = node
    if targetDepth:
        if currentDepth >= targetDepth or node.isTerminal:
            return node, node.state.calculateReward(player)[0]
        else:
            node.expand()
            nonSimulatedChildren = [child for child in node.children.values() if not child.isFullySimulated]
            nextNode = random.choice(nonSimulatedChildren)
            return randomPolicy(nextNode, player, currentDepth+1, targetDepth)
    else:
        if node.isTerminal:
            return node, node.state.calculateReward(player)[0]
        else:
            node.expand()
            nonSimulatedChildren = [child for child in node.children.values() if not child.isFullySimulated]
            nextNode = random.choice(nonSimulatedChildren)
            return randomPolicy(nextNode, player, currentDepth+1, None)

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
        self.isFullySimulated = False
        self.parent = parent
        self.children = {}
        self.numVisits = 0
        self.totalReward = 0

    def getAvgReward(self):
        if self.numVisits == 0:
            return float("inf")
        return self.totalReward/self.numVisits

    def getSimulatedRatio(self):
        numSimulated = 0 # number of nodes which have been fully simulated
        numTotal = 1 # total number of nodes in the visible game tree
        if self.isFullySimulated:
            numSimulated += 1
        if self.isTerminal:
            return numSimulated, numTotal
        else:
            for child in self.children.values():
                simRatio = child.getSimulatedRatio()
                numSimulated += simRatio[0]
                numTotal += simRatio[1]
            return numSimulated, numTotal

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
                 playerSightLimit=None, estCompSightLimit=3, maxEstCompSightLimit=6):
        self.player = player
        self.root = MCTSNode(state, None)
        self.explorationConstant = explorationConstant
        self.playerSightLimit = playerSightLimit
        self.rollout = rolloutPolicy
        self.maxEstimatedSightLevelIncorrect = 0

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
        for companion in self.companions.values():
            companion[0].expand()

        if description:
            print(f"\n[Player {self.player}] Beginning Monte-Carlo Tree Search")

        # search until time limit
        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit and not self.root.isFullySimulated:
                # Full Depth MCTS
                self.executeRound(self.root, self.player, self.playerSightLimit)
                # Companion Depth MCTS
                for player, info in self.companions.items():
                    self.executeRound(info[0], player, info[1]+info[3])

        # search until iteration limit
        else:
            startTime = time.time()
            for i in range(self.searchLimit):
                if self.root.isFullySimulated:
                    break
                else:
                    # Full Depth MCTS
                    self.executeRound(self.root, self.player, self.playerSightLimit)
                    # Companion Depth MCTS
                    for player, info in self.companions.items():
                        self.executeRound(info[0], player, info[1]+info[3])
            endTime = time.time()
            print(f"Time to execute {self.searchLimit} iterations: {endTime-startTime}s")

        rootChildrenByAvgRewards = {k: round(v, 3) for k, v in self.orderChildrenByAvgRewards(self.root).items()}
        rootChildrenByConfidence = {k: round(v, 6) for k, v in self.orderChildrenByConfidence(self.root).items()}
        companionChildrenByAvgRewards = {}
        companionChildrenByConfidence = {}
        for player, info in self.companions.items():
            companionChildrenByAvgRewards[player] = {k: round(v, 3) for k, v in self.orderChildrenByAvgRewards(info[0]).items()}
            companionChildrenByConfidence[player] = {k: round(v, 6) for k, v in self.orderChildrenByConfidence(info[0]).items()}


        if description:
            if self.root.isFullySimulated:
                print("MCTS COMPLETE: Root Fully Simulated")
            else:
                print(f"MCTS COMPLETE: {'Time' if self.limitType == 'time' else 'Iteration'} Limit Reached")
            # print("MCTS Children")
            # for action, child in self.root.children.items():
                # print(f"Column {action}: AvgReward={child.getAvgReward():<13.3f}TotalReward={child.totalReward:<9}NumVisits={child.numVisits:<7}FullySimulated={child.isFullySimulated}")
            # print("Companion Children")
            # for action, child in self.companionRoot.children.items():
                # print(f"Column {action}: AvgReward={child.getAvgReward():<13.3f}TotalReward={child.totalReward:<9}NumVisits={child.numVisits:<7}")
            print(f"{self.player} Rewards:", rootChildrenByAvgRewards)
            print(f"{self.player} Confidence:", rootChildrenByConfidence)
            for player in self.companions.keys():
                print(f"{player} Rewards:", companionChildrenByAvgRewards[player])
                print(f"{player} Confidence:", companionChildrenByConfidence[player])

        # bestChild = self.getBestChild(self.root, 0)
        for playerConfidences in companionChildrenByConfidence.values():
            for action, actionConfidence in playerConfidences.items():
                rootChildrenByConfidence[action] += actionConfidence
        if description:
            if self.companions:
                print(rootChildrenByConfidence)
        action = max(rootChildrenByConfidence.items(), key=operator.itemgetter(1))[0]
        return action

    def executeRound(self, root, player, sightLimit):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        # select & expand
        node = self.selectNode(root)
        # simulation
        simulationNode, reward = self.rollout(node, self.player, 0, sightLimit)
        # backpropagation
        self.backpropogate(simulationNode, reward)

    def selectNode(self, root):
        # node must not be terminal
        root.expand()
        node = self.getBestChild(root, self.explorationConstant)
        return node

    def backpropogate(self, node, reward):
        if node.isTerminal:
            node.isFullySimulated = True # set terminal (leaf) node to Simulated
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            if not node.parent: # if current node is root
                break # end backpropagation
            else: # if current node is root
                node = node.parent
                # if all children have been fully simulated, set parent.isFullySimulated
                if all([child.isFullySimulated for child in node.children.values()]):
                    # aim is to represent whether leaf nodes have been simulated
                    node.isFullySimulated = True

    def getBestChild(self, node, explorationConstant):
        bestValue = float("-inf")
        bestNodes = []
        children = node.children.values()
        if explorationConstant != 0: # if still searching tree, not yet choosing next action
            children = [child for child in children if not child.isFullySimulated]
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
                        while time.time() < timeLimit and not tempNode.isFullySimulated:
                            self.executeRound(tempNode, player, estimatedSightLevel)
                        predictedActions[estimatedSightLevel] = self.getBestActions(tempNode, 0)
                else: # search until iteration limit
                    for estimatedSightLevel in range(1, maxEstimatedSightLevel+1, 1):
                        tempNode = MCTSNode(deepcopy(self.root.state), None)
                        for i in range(self.searchLimit//maxEstimatedSightLevel):
                            if tempNode.isFullySimulated:
                                break
                            else:
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
