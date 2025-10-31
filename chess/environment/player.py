from chess.environment.color import Color
from chess.environment.piece import Piece, PieceType

class Player:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
        self.pieces = set[Piece]()
    
    def init_pieces(self):
        if self.color == Color.WHITE:
            self.pieces = {
                Piece(PieceType.PAWN, self.color, (i, 1)) for i in range(8)
            } | {
                Piece(PieceType.ROOK, self.color, (0, 0)),
                Piece(PieceType.KNIGHT, self.color, (1, 0)),
                Piece(PieceType.BISHOP, self.color, (2, 0)),
                Piece(PieceType.QUEEN, self.color, (3, 0)),
                Piece(PieceType.KING, self.color, (4, 0)),
                Piece(PieceType.BISHOP, self.color, (5, 0)),
                Piece(PieceType.KNIGHT, self.color, (6, 0)),
                Piece(PieceType.ROOK, self.color, (7, 0))   
            } 
        else:
            self.pieces = {
                Piece(PieceType.PAWN, self.color, (i, 6)) for i in range(8)
            } | {
                Piece(PieceType.ROOK, self.color, (0, 7)),
                Piece(PieceType.KNIGHT, self.color, (1, 7)),
                Piece(PieceType.BISHOP, self.color, (2, 7)),
                Piece(PieceType.QUEEN, self.color, (3, 7)), 
                Piece(PieceType.KING, self.color, (4, 7)),
                Piece(PieceType.BISHOP, self.color, (5, 7)),
                Piece(PieceType.KNIGHT, self.color, (6, 7)),
                Piece(PieceType.ROOK, self.color, (7, 7))
            }