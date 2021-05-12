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
    return currentState.calculateReward(player)[0]

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
        reward = self.rollout(node.state, player, sightLimit)
        # backpropagation
        self.backpropogate(node, reward)


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

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            if node.parent:
                node = node.parent
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
            # update root node
            self.root.expand()
            self.root = self.root.children[action]
            return self.root.state

    def reset(self, state):
        self.root = MCTSNode(state, None)
