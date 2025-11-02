from chess.environment.board import Board
from chess.environment.player import Player
from chess.environment.color import Color

def init_moves_test():
    player_white = Player("Player White", Color.WHITE)
    player_black = Player("Player Black", Color.BLACK)
    board = Board(player_white, player_black)
   
    board.print_board()
    #print(f"\n\nsValid moves for white: {board.get_valid_actions(player_white)}")

def to_pos_tests():
    squares  = ['A1', 'H8', 'E5']
    for s in squares:
        print(f"{s} - {Board.square_str_to_pos(s)}")


if __name__ == "__main__":
    to_pos_tests()
    init_moves_test()