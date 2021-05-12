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
        # returns (number of descendants + self) which are simulated, total (number of descendants + self)
        numSimulated = 0
        numTotal = 1
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

    # def calculateReward(self, player):
    #     return self.state.calculateReward(player)

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
    def __init__(self, player, state, config=CONFIG, timeLimit=None, iterationLimit=None,
                 explorationConstant=500, rolloutPolicy=randomPolicy, playerSightLimit=None):
        self.player = player
        self.root = MCTSNode(state, None)
        self.explorationConstant = explorationConstant
        self.playerSightLimit = playerSightLimit
        self.rollout = rolloutPolicy

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
            while time.time() < timeLimit and not self.root.isFullySimulated:
                # Full Depth MCTS
                self.executeRound(self.root, self.player, self.playerSightLimit)

        # search until iteration limit
        else:
            startTime = time.time()
            for i in range(self.searchLimit):
                if self.root.isFullySimulated:
                    break
                else:
                    # Full Depth MCTS
                    self.executeRound(self.root, self.player, self.playerSightLimit)
            endTime = time.time()
            print(f"Time to execute {self.searchLimit} iterations: {endTime-startTime}s")

        rootChildrenByAvgRewards = {k: round(v, 3) for k, v in self.orderChildrenByAvgRewards(self.root).items()}
        rootChildrenByConfidence = {k: round(v, 6) for k, v in self.orderChildrenByConfidence(self.root).items()}


        if description:
            if self.root.isFullySimulated:
                print("MCTS COMPLETE: Root Fully Simulated")
            else:
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
            # update root node
            self.root.expand()
            self.root = self.root.children[action]
            return self.root.state

    def reset(self, state):
        self.root = MCTSNode(deepcopy(state), None)
