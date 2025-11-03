from enum import Enum
from chess.environment.color import Color
from chess.environment.utils import *
import uuid

class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

# help random agent assign score to potential actions, 25 points for check
piece_captured_score = {
    PieceType.PAWN: 8,
    PieceType.ROOK: 30,
    PieceType.KNIGHT: 50,
    PieceType.BISHOP: 30,
    PieceType.QUEEN: 100
}

class Piece:
    def __init__(self, type: PieceType, color: Color, position: tuple[int, int]):
        self._id = uuid.uuid4()
        self.type = type
        self.color = color
        self.position = position
    
    
    def __repr__(self):
        return f"{self.color.name} {self.type.name} at {square_pos_to_str(self.position)}"
    
    def __eq__(self, other):
        return isinstance(other, Piece) and self._id == other._id

    def __hash__(self):
        return hash(self._id)
    
    def __str__(self):
        return f"{self.color.name} {self.type.name} at {square_pos_to_str(self.position)}"