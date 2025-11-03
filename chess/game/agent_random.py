from chess.game.agent import Agent
import random

class AgentRandom(Agent):
    def act(self):
        options = [(piece, move) for piece, moves in self.board.get_valid_actions(self.player).items() for move in moves]
        piece, move = random.choice(options)
        self.board.act(self.player, piece, move)
