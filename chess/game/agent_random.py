from chess.game.agent import Agent
from chess.environment.board import ActionType
from chess.environment.utils import *
import random

class AgentRandom(Agent):
    def act(self):
        actions = self.board.get_valid_actions(self.player)
        moves_dict = actions[ActionType.MOVE]
        castles_dict = actions[ActionType.CASTLE]

        options = []
        options += [[ActionType.MOVE, move_score, piece, move] for piece, moves in moves_dict.items() for move, move_score in moves]
        options += [[ActionType.CASTLE, castle_score, king_side] for king_side, castle_score in castles_dict.items()]
        
        min_score = min(x[1] for x in options)
        for o in options:
            o[1] += (abs(min_score) + 1)

        options.sort(key = lambda x: -x[1]) # sort just for presentation of ranking of options in logs/io player
        
        print(f'Options: {self.player.color}')
        for x in options:
            if x[0] == ActionType.MOVE:
                score, piece, move = x[1:]
                print(f"{piece.color.name[0]}-{piece.type.name[:2]}: {square_pos_to_str(piece.position)} -> {square_pos_to_str(move)} = {score}")
            else:
                castle_score, king_side = x[1:]
                print(f"Castle {'king side' if king_side else 'queen side'} = {castle_score}")
        
        action_scores = [x[1] for x in options]
        x = random.choices(options, weights=action_scores, k=1)[0]
        
        if x[0] == ActionType.MOVE:
            score, piece, move = x[1:]
            print(f"\nAction Chosen: {piece.color.name[0]}-{piece.type.name[:2]}: {square_pos_to_str(piece.position)} -> {square_pos_to_str(move)} = {score}\n")
            self.board.move(self.player, piece, move)
        
        else:
            score, king_side = x[1:]
            print(f"\nAction Chosen: Castle {'king side' if king_side else 'queen side'} = {score}")
            self.board.castle(self.player, king_side)
