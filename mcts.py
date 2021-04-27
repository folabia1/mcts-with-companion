from __future__ import division
from config import CONFIG
from copy import copy, deepcopy
import time
import math
import random


class TreeNode():
    def __init__(self, state, parent=None):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = False
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.children = []
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.numVisits = 0
        self.totalReward = None

    def getReward(self, player):
        self.totalReward = self.state.getReward(player)
        return self.totalReward

    def expand(self):
        if self.isFullyExpanded:
            return self.children
        else:
            actions = self.state.getPossibleActions()
            for action in actions:
                newNode = TreeNode(self.state.takeAction(action), self)
                self.children.append(newNode)
            self.isFullyExpanded = True
            return self.children

    # def __str__(self):
    #     s=[]
    #     s.append("totalReward: %s"%(self.totalReward))
    #     s.append("numVisits: %d"%(self.numVisits))
    #     s.append("isTerminal: %s"%(self.isTerminal))
    #     s.append("possibleActions: %s"%(self.children.keys()))
    #     return f"{self.__class__.__name__}: {s}"


class ConnectFourState():
    def __init__(self, board, player, movesPlayed):
        if board is None:
            self.board = np.empty(CONFIG.boardSize, dtype=str)
        else:
            self.board = board
        self.currentPlayer = player
        self.movesPlayed = movesPlayed

    def getPossibleActions(self):
        possibleActions = []
        for column in range(self.board.shape[1]):
            if self.board[0][column] == "":
                possibleActions.append(column)
        return possibleActions

    def takeAction(self, action):
        height = CONFIG.boardSize[0]
        newState = ConnectFourState(board=copy(self.board), player=self.getNextPlayer(), movesPlayed=self.movesPlayed+1)
        for row in range(height-1, -1, -1):
            if newState.board[row][action] == "":
                newState.board[row][action] = CONFIG.teams[self.currentPlayer]
                return newState
        return None

    def getNextPlayer(self):
        return CONFIG.turn[(self.movesPlayed+1)%len(CONFIG.turn)]

    def isTerminal(self):
        height = CONFIG.boardSize[0]
        length = CONFIG.boardSize[1]
        for row in range(height-1, -1, -1):
            for column in range(length):
                initial = self.board[row][column]
                if initial == "":
                    continue
                # check up
                if row >= 3:
                    for i in range(1,4):
                        if (self.board[row-i][column] != initial):
                            break
                        if i == 3:
                            return True
                    # check up and left diagonal
                    if column >= 3:
                        for i in range(1,4):
                            if self.board[row-i][column-i] != initial:
                                break
                            if i == 3:
                                return True
                    # check up and right diagonal
                    if column <= length-4:
                        for i in range(1,4):
                            if self.board[row-i][column+i] != initial:
                                break
                            if i == 3:
                                return True
                # check right
                if column <= length-4:
                    for i in range(1,4):
                        if self.board[row][column+i] != initial:
                            break
                        if i == 3:
                            return True
        return False

    def getReward(self, player):
        # return 1
        # based on domain knowledge about the position
        # global teams
        playerTeam = CONFIG.teams[player]
        height = CONFIG.boardSize[0]
        length = CONFIG.boardSize[1]
        threeOutOfFours = 0
        twoOutOfFours = 0
        # points = 0
        for row in range(height-1, -1, -1):
            for column in range(length):
                initial = self.board[row][column]
                if initial == "":
                    continue

                if playerTeam == initial:
                    multiplier = 1
                else:
                    multiplier = -1
                # check up
                if row >= 3:
                    tally = 1
                    for i in range(1,4):
                        if (self.board[row-i][column] == initial):
                            tally += 1
                    if tally == 2:
                        twoOutOfFours += 1 * multiplier
                    elif tally == 3:
                        threeOutOfFours += 1 * multiplier
                    elif tally == 4:
                        return 100*multiplier
                    # check up and left diagonal
                    if column >= 3:
                        tally = 1
                        for i in range(1,4):
                            if self.board[row-i][column-i] == initial:
                                tally += 1
                        if tally == 2:
                            twoOutOfFours += 1 * multiplier
                        elif tally == 3:
                            threeOutOfFours += 1 * multiplier
                        elif tally == 4:
                            return 100*multiplier
                    # check up and right diagonal
                    if column <= length-4:
                        tally = 1
                        for i in range(1,4):
                            if self.board[row-i][column+i] == initial:
                                tally += 1
                        if tally == 2:
                            twoOutOfFours += 1 * multiplier
                        elif tally == 3:
                            threeOutOfFours += 1 * multiplier
                        elif tally == 4:
                            return 100*multiplier
                # check right
                if column <= length-4:
                    tally = 1
                    for i in range(1,4):
                        if self.board[row][column+i] == initial:
                            tally += 1
                    if tally == 2:
                        twoOutOfFours += 1 * multiplier
                    elif tally == 3:
                        threeOutOfFours += 1 * multiplier
                    elif tally == 4:
                        return 100*multiplier
        points = min(10*threeOutOfFours + 5*twoOutOfFours, 99)
        return points

class RandomPlayer():
    def __init__(self, state):
        self.state = state

    def determineNextAction(self):
        possibleActions = self.state.getPossibleActions()
        nextAction = random.choice(possibleActions)
        return nextAction

    def logAction(self, action, player):
        # check expected player is playing
        if player != self.state.currentPlayer:
            return None
        else:
            # update state
            self.state = self.state.takeAction(action)
            return self.state

class MinimaxPlayer():
    def __init__(self, player, state, sightLimit=None):
        self.player = player
        self.playerTeam = CONFIG.teams[player]
        self.root = TreeNode(state)
        self.sightLimit = sightLimit

    def expandToSightLimit(self):
        grandchildren = [self.root]
        for i in range(self.sightLimit):
            children = grandchildren
            grandchildren = []
            for child in children:
                grandchildren.extend(child.expand())
                # print(child.state.board, "\n")
            # for grandchild in grandchildren:
            #     grandchild.getReward()
        return grandchildren

    def getBestChild(self, node):
        # check if children of node have been expanded
        if node.children[0].isFullyExpanded:
            # find highest reward of unexpanded descendants of each child
            rewards = [self.getBestChild(child)[1] for child in node.children]
            # return child with highest reward
            bestChild = (rewards.index(max(rewards)), max(rewards))
            return bestChild
        # if children of node have not been expanded
        else:
            # find rewards of each child
            rewards = [child.getReward(child.state.currentPlayer) for child in node.children]
            # return child with highest reward
            bestChild = (rewards.index(max(rewards)), max(rewards))
            return bestChild

    def determineNextAction(self):
        self.expandToSightLimit()
        # print(self.root.children)
        nextAction = self.getBestChild(self.root)[0]
        # print(nextAction)
        return nextAction

    def logAction(self, action, player):
        # check expected player is playing
        if player != self.root.state.currentPlayer:
            return None
        else:
            # update root node
            self.root.expand()
            # print(action)
            self.root = self.root.children[action]
            return self.root.state


# class MCTSPlayer():
#     def __init__(self, state, timeLimit=None, iterationLimit=None, explorationConstant= 1/math.sqrt(2),
#                  rolloutPolicy=randomPolicy):
#         if timeLimit != None:
#             if iterationLimit != None:
#                 raise ValueError("Cannot have both a time limit and an iteration limit")
#             # time taken for each MCTS search in milliseconds
#             self.timeLimit = timeLimit
#             self.limitType = 'time'
#         else:
#             if iterationLimit == None:
#                 raise ValueError("Must have either a time limit or an iteration limit")
#             # number of iterations of the search
#             if iterationLimit < 1:
#                 raise ValueError("Iteration limit must be greater than one")
#             self.searchLimit = iterationLimit
#             self.limitType = 'iterations'
#         self.explorationConstant = explorationConstant
#         self.rollout = rolloutPolicy
#
#     def search(self, initialState, needDetails=False):
#         self.root = TreeNode(initialState, None)
#
#         if self.limitType == 'time':
#             timeLimit = time.time() + self.timeLimit / 1000
#             while time.time() < timeLimit:
#                 self.executeRound()
#         else:
#             for i in range(self.searchLimit):
#                 self.executeRound()
#
#         bestChild = self.getBestChild(self.root, 0)
#         action=(action for action, node in self.root.children.items() if node is bestChild).__next__()
#         if needDetails:
#             return {"action": action, "expectedReward": bestChild.totalReward / bestChild.numVisits}
#         else:
#             return action
#
#     def executeRound(self):
#         """
#             execute a selection-expansion-simulation-backpropagation round
#         """
#         node = self.selectNode(self.root)
#         reward = self.rollout(node.state)
#         self.backpropogate(node, reward)
#
#     def selectNode(self, node):
#         while not node.isTerminal:
#             if node.isFullyExpanded:
#                 node = self.getBestChild(node, self.explorationConstant)
#             else:
#                 return self.expand(node)
#         return node
#
#     def expand(self, node):
#         actions = node.state.getPossibleActions()
#         for action in actions:
#             newNode = TreeNode(node.state.takeAction(action), node)
#             node.children.append(newNode)
#         node.isFullyExpanded = True
#
#     def backpropogate(self, node, reward):
#         while node is not None:
#             node.numVisits += 1
#             node.totalReward += reward
#             node = node.parent
#
#     def getBestChild(self, node, explorationValue):
#         bestValue = float("-inf")
#         bestNodes = []
#         for child in node.children.values():
#             nodeValue = node.state.getCurrentPlayer() * child.totalReward / child.numVisits + explorationValue * math.sqrt(
#                 2 * math.log(node.numVisits) / child.numVisits)
#             if nodeValue > bestValue:
#                 bestValue = nodeValue
#                 bestNodes = [child]
#             elif nodeValue == bestValue:
#                 bestNodes.append(child)
#         return random.choice(bestNodes)
