from chess.environment.piece import Piece, PieceType
from chess.environment.player import Player
from chess.environment.color import Color
from functools import partial

class Board:
    def __init__(self, players: tuple[Player, Player]):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.players = players
        self.init_board()

    def init_board(self):
        for player in self.players:
            for piece in player.pieces:
                self.board[piece.position[0]][piece.position[1]] = piece
    
    def get_valid_actions(self, player: Player):
        return {piece: self.get_valid_moves(piece) for piece in player.pieces}
    
    def get_valid_moves(self, piece: Piece):
        match piece.type:
            case PieceType.PAWN:
                return self.get_valid_moves_pawn(piece)
            case PieceType.ROOK:
                return self.get_valid_moves_rook(piece)
            case PieceType.KNIGHT:
                return self.get_valid_moves_knight(piece)
            case PieceType.BISHOP:
                return self.get_valid_moves_bishop(piece)
            case PieceType.QUEEN:
                return self.get_valid_moves_queen(piece)
            case PieceType.KING:
                return self.get_valid_moves_king(piece)
    
    def get_valid_moves_pawn(self, piece: Piece):
        moves_out = []
        if piece.color == Color.WHITE:
            if piece.position[1] == 1:
                moves_straight = [(piece.position[0], piece.position[1] + 1), (piece.position[0], piece.position[1] + 2)]
                for move in moves_straight:
                    if not self.board[move[0]][move[1]]:
                        moves_out.append(move)
                

                moves_angled = [(piece.position[0] + 1, piece.position[1] + 1), (piece.position[0] - 1, piece.position[1] + 1)]
                for move in moves_angled:
                    x, y = move
                    if x < 0 or x > 7 or y < 0 or y > 7:
                        continue
                    if self.board[x][y] and self.board[x][y].color != piece.color:
                        moves_out.append(move)
        
        else:
            if piece.position[1] == 6:
                moves_straight = [(piece.position[0], piece.position[1] - 1), (piece.position[0], piece.position[1] - 2)]
                for move in moves_straight:
                    if not self.board[move[0]][move[1]]:
                        moves_out.append(move)
                
                moves_angled = [(piece.position[0] + 1, piece.position[1] - 1), (piece.position[0] - 1, piece.position[1] - 1)]
                for move in moves_angled:
                    x, y = move
                    if x < 0 or x > 7 or y < 0 or y > 7:
                        continue
                    if self.board[x][y] and self.board[x][y].color != piece.color:
                        moves_out.append(move)
        
        return moves_out