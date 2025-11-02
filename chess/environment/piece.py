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
    
    
    def __repr__(self):
        return f"{self.color.name} {self.type.name} at {self.position}"
    
    def __eq__(self, other: 'Piece'):
        return self.type == other.type and self.color == other.color and self.position == other.position
    
    def __hash__(self):
        return hash((self.type, self.color, self.position))
    
    def __str__(self):
        return f"{self.color.name} {self.type.name} at {self.position}"