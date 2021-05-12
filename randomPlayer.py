import random

class RandomPlayer():
    def __init__(self, state):
        self.state = state

    def determineNextAction(self, description=False):
        possibleActions = self.state.getPossibleActions()
        nextAction = random.choice(possibleActions)
        return nextAction

    def logAction(self, action, player, description=False):
        # check expected player is playing
        if player != self.state.currentPlayer:
            return None
        else:
            # update state
            self.state = self.state.takeAction(action)
            return self.state

    def reset(self, state):
        self.state = state
