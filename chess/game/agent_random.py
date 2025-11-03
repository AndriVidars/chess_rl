from chess.game.agent import Agent
from chess.environment.utils import *
import random

class AgentRandom(Agent):
    def act(self):
        options = [(piece, move, move_score) for piece, moves in self.board.get_valid_actions(self.player).items() for move, move_score in moves]
        options.sort(key = lambda x: (-x[0].type.value, -x[2]))
        print(f'Options: {self.player.color}')
        for piece, move, score in options:
            print(f"{piece.color.name[0]}-{piece.type.name[:2]}: {square_pos_to_str(piece.position)} -> {square_pos_to_str(move)} = {score}")

        piece, move, score = random.choices(options, weights=[x for _, _, x in options], k=1)[0]
        print(f"\nAction Chosen: {piece.color.name[0]}-{piece.type.name[:2]}: {square_pos_to_str(piece.position)} -> {square_pos_to_str(move)} = {score}\n")
        self.board.act(self.player, piece, move)
