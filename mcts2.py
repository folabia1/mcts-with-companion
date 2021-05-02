from __future__ import division
from config import CONFIG
from copy import copy, deepcopy
import time
import math
import random

# random simulation policy for MCTS
def randomPolicy(node, player):
    while not node.isTerminal:
        node.expand()
        node = random.choice(list(node.children.values()))
    # print("\nSimulation Reward:", node.calculateReward(player))
    # print("Simulation Node Depth:", node.depth)
    return node, node.calculateReward(player)[0]

def UCB1(node, player, explorationConstant):
    if node.numVisits == 0:
        return float("inf")
    averageReward = node.getAvgReward(player)
    return averageReward + explorationConstant*math.sqrt(math.log(node.parent.numVisits)/node.numVisits)

class MinimaxNode():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = False
        self.children = {}

    def calculateReward(self, player):
        return self.state.calculateReward(player)

    def expand(self):
        if self.isFullyExpanded:
            return self.children
        else:
            actions = self.state.getPossibleActions()
            for action in actions:
                newNode = MinimaxNode(self.state.takeAction(action), self)
                self.children[action] = newNode
            self.isFullyExpanded = True
            return self.children

class MCTSNode():
    def __init__(self, state, parent=None):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = False
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.numVisits = 0
        self.totalReward = 0

    def getAvgReward(self, player):
        if self.numVisits == 0:
            return float("inf")
        return self.totalReward/self.numVisits

    def calculateReward(self, player):
        return self.state.calculateReward(player)

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
        return self.calculateReward(self.currentPlayer)[1]

    def calculateReward(self, player):
        # based on domain knowledge about the position
        playerTeam = CONFIG.teams[player]
        height = CONFIG.boardSize[0]
        length = CONFIG.boardSize[1]
        threeOutOfFours = 0
        twoOutOfFours = 0
        boardFull = True
        # points = 0
        for row in range(height-1, -1, -1):
            for column in range(length):
                initial = self.board[row][column]
                if initial == "":
                    boardFull = False
                    continue

                if playerTeam[0] == initial:
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
                        return 100*multiplier, "WIN"
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
                            return 100*multiplier, "WIN"
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
                            return 100*multiplier, "WIN"
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
                        return 100*multiplier, "WIN"
        if boardFull:
            return 0, "DRAW"
        points = max(-99, min(10*threeOutOfFours + 5*twoOutOfFours, 99))
        return points, None

class RandomPlayer():
    def __init__(self, state):
        self.state = state

    def determineNextAction(self, description=False):
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
        self.root = MinimaxNode(state, None)
        self.sightLimit = sightLimit

    def expandToSightLimit(self):
        grandchildren = [self.root]
        for i in range(self.sightLimit):
            children = grandchildren
            grandchildren = []
            for child in children:
                grandchildren.extend(child.expand().values())
                # print(child.state.board, "\n")
            # for grandchild in grandchildren:
            #     grandchild.calculateReward()
        return grandchildren

    def getBestChild(self, node):
        # check if children of node have been expanded
        if next(iter(node.children.items()))[1].isFullyExpanded:
            # propagate highest reward of unexpanded descendants of each child
            rewards = [self.getBestChild(child)[1] for child in node.children.values()]
            # return child with highest propagated reward
            bestChild = (rewards.index(max(rewards)), max(rewards))
            return bestChild
        # if children of node have not been expanded
        else:
            # find rewards of each child
            rewards = [child.calculateReward(self.player)[0] for child in node.children.values()]
            # return child with highest reward
            bestChild = (rewards.index(max(rewards)), max(rewards))
            return bestChild

    def determineNextAction(self, description=False):
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


class MCTSPlayer():
    def __init__(self, player, state, timeLimit=None, iterationLimit=None, explorationConstant=500,
                 rolloutPolicy=randomPolicy):
        self.player = player
        self.state = state
        self.root = MCTSNode(state, None)
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, description=False):
        if description:
            print(f"\n[Player {self.player}] Beginning Monte-Carlo Tree Search")
            self.root.expand()
            print("BEFORE Search")
            print(f"ROOT: AvgReward={self.root.getAvgReward(self.player):<13.3f}TotalReward={self.root.totalReward:<9}NumVisits={self.root.numVisits:<13}")
            print(f"Possible Actions: {self.state.getPossibleActions()}")
            for action, child in self.root.children.items():
                print(f"Column {action}: AvgReward={child.getAvgReward(self.player):<13.3f}TotalReward={child.totalReward:<9}NumVisits={child.numVisits:<13}")
        # search until time limit
        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        # search until iteration limit
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        if description:
            print("\nAFTER Search")
            for action, child in self.root.children.items():
                print(f"Column {action}: AvgReward={child.getAvgReward(self.player):<13.3f}TotalReward={child.totalReward:<9}NumVisits={child.numVisits:<13}")
        bestChild = self.getBestChild(self.root, 0)
        action=(action for action, node in self.root.children.items() if node is bestChild).__next__()
        return action

    def executeRound(self):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        # select & expand
        node = self.selectNode(self.root)
        # simulation
        simulationNode, reward = self.rollout(node, self.player)
        # backpropagation
        self.backpropogate(simulationNode, reward)

    def selectNode(self, root):
        # node must not be terminal
        root.expand()
        node = self.getBestChild(root, self.explorationConstant)
        return node

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            if not node.parent: # if current node is root
                break # end backpropagation
            else: # if current node is root
                node = node.parent

    def getBestChild(self, node, explorationConstant):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = UCB1(child, self.player, explorationConstant)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def determineNextAction(self, description=False):
        # TODO: search for best option for companion as well
        nextAction = self.search(description=description)
        # TODO: balance best option for MCTSPlayer with best option for companion
        return nextAction

    def logAction(self, action, player):
        # check expected player is playing
        if player != self.root.state.currentPlayer:
            print("\n\nUnexpected Player!\n\n")
            return None
        else:
            if player != self.player:
                # TODO: update estimated sight level of other players
                # use CONFIG.turn not CONFIG.teams, to include players actually playing not just in the "room"
                pass
            # update root node
            self.root.expand()
            self.root = self.root.children[action]
            return self.root.state
