from chess.environment.board import Board
from chess.environment.player import Player
from chess.environment.color import Color
from chess.environment.utils import *

def init_moves_test():
    player_white = Player(Color.WHITE)
    player_black = Player(Color.BLACK)
    board = Board(player_white, player_black)
   
    board.print_board()

    print(f"\nValid moves for white:")
    for piece, moves in board.get_valid_actions(player_white).items():
        print(f"{piece}: {[square_pos_to_str(x) for x in moves]}")
    
    print(f"\nValid moves for black:")
    for piece, moves in board.get_valid_actions(player_black).items():
        print(f"{piece}: {[square_pos_to_str(x) for x in moves]}")
    

def to_pos_tests():
    squares  = ['A1', 'A8', 'D7', 'H8', 'E5', 'A2', 'C2']
    for s in squares:
        pos = square_str_to_pos(s)
        str = square_pos_to_str(pos)
        print(f"{s} - {pos} - {str}")


if __name__ == "__main__":
    to_pos_tests()
    init_moves_test()