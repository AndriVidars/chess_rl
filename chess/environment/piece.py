from enum import Enum
from chess.environment.color import Color

class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, type: PieceType, color: Color, position: tuple[int, int]):
        self.type = type
        self.color = color
        self.position = position
    