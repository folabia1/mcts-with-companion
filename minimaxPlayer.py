from config import CONFIG
import random

class MinimaxNode():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = False
        self.children = {}

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

class MinimaxPlayer():
    def __init__(self, player, state, config=CONFIG, sightLimit=None):
        self.player = player
        self.config = config
        self.playerTeam = self.config.teams[player]
        self.root = MinimaxNode(state, None)
        self.sightLimit = sightLimit

    def expandToSightLimit(self):
        grandchildren = [self.root]
        for i in range(self.sightLimit):
            children = grandchildren
            grandchildren = []
            for child in children:
                grandchildren.extend(child.expand().values())
        return grandchildren

    def getBestChild(self, node, player):
        if node.children:
            # propagate highest reward of unexpanded descendants of each child
            rewards = {action:self.getBestChild(child, player)[1] for action, child in node.children.items()}
            # return child with highest propagated reward
            if self.config.teams[node.state.currentPlayer] == self.config.teams[self.player]:
                bestValue = float("-inf")
                bestActions = []
                for action, reward in rewards.items():
                    if reward > bestValue:
                        bestValue = reward
                        bestActions = [action]
                    elif reward == bestValue:
                        bestActions.append(action)
            else:
                bestValue = float("inf")
                bestActions = []
                for action, reward in rewards.items():
                    if reward < bestValue:
                        bestValue = reward
                        bestActions = [action]
                    elif reward == bestValue:
                        bestActions.append(action)
            return (random.choice(bestActions), bestValue)
        else:
            return (None, node.state.calculateReward(player)[0])

    def orderChildrenByRewards(self, node):
        rewards = {action:self.getBestChild(child, node.state.currentPlayer)[1] for action, child in self.root.children.items()}
        orderedRewards = {action: reward for action, reward in sorted(rewards.items(), key=lambda item: item[1], reverse=True)}
        return orderedRewards

    def determineNextAction(self, description=False):
        if description:
            print(f"\n[Player {self.player}] Beginning Minimax{self.sightLimit} Algorithm")
        self.expandToSightLimit()
        orderedRewards = self.orderChildrenByRewards(self.root)
        if description:
            print(f"Rewards:{orderedRewards}")
        bestValue = float("-inf")
        bestActions = []
        for action, reward in orderedRewards.items():
            if reward > bestValue:
                bestValue = reward
                bestActions = [action]
            elif reward == bestValue:
                bestActions.append(action)
        return random.choice(bestActions)

    def logAction(self, action, player, description=False):
        # check expected player is playing
        if player != self.root.state.currentPlayer:
            return None
        else:
            # update root node
            self.root.expand()
            self.root = self.root.children[action]
            return self.root.state

    def reset(self, state):
        self.root = MinimaxNode(state, None)
