from chess.environment.board import Board
from chess.environment.player import Player
from chess.environment.color import Color

def init_moves_test():
    p1 = Player("Player 1", Color.WHITE)
    p2 = Player("Player 2", Color.BLACK)
    board = Board((p1, p2))
    print(board.get_valid_actions(p1))

if __name__ == "__main__":
    init_moves_test()