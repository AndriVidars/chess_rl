from chess.environment.piece import Piece, PieceType
from chess.environment.player import Player
from chess.environment.color import Color
from copy import deepcopy

class Board:
    def __init__(self, player_white: Player, player_black: Player):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.player_white = player_white
        self.player_black = player_black
        self.init_board()

    def init_board(self):
        for player in [self.player_white, self.player_black]:
            for piece in player.pieces:
                self.board[piece.position[0]][piece.position[1]] = piece
    
    def get_valid_actions(self, player: Player):
        return {piece: self.get_valid_moves(piece) for piece in player.pieces}
    
    def act(self, player: Player, piece: Piece, move: tuple[int, int]):
        if piece not in player.pieces:
            raise ValueError(f"Piece {piece.type} at {piece.position} not found in player {player.name}'s pieces")
        
        piece_moves = self.get_valid_moves(piece)
        if move not in piece_moves:
            raise ValueError(f"Invalid move for piece {piece.type} at {piece.position}: {move}")
        
        opp_player = self.player_black if player == self.player_white else self.player_white
        self.board[piece.position[0]][piece.position[1]] = None
        
        if self.board[move[0]][move[1]]:
            piece_eliminated = self.board[move[0]][move[1]]
            opp_player.pieces.remove(piece_eliminated)
            opp_player.pieces_eliminated.add(piece_eliminated)

        self.board[move[0]][move[1]] = piece
        piece.position = move

        # promote pawn
        if piece.type == PieceType.PAWN and (move[1] == 0 or move[1] == 7):
            piece.type = PieceType.QUEEN

    
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
    
    def get_valid_moves_rook(self, piece: Piece):
        moves_out = []
        x, y = piece.position
        
        # left
        x_, y_ = x - 1, y
        while x_ > 0:
            if not self.board[x_][y_]:
                moves_out.append((x_, y_))
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                moves_out.append((x_, y_))
                break
            else:
                break
            x_ -= 1

        # right
        x_, y_ = x + 1, y
        while x_ < 7:
            if not self.board[x_][y_]:
                moves_out.append((x_, y_))
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                moves_out.append((x_, y_))
                break
            else:
                break
            x_ += 1
        
        # up
        x_, y_ = x, y + 1
        while y_ < 7:
            if not self.board[x_][y_]:
                moves_out.append((x_, y_))
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                moves_out.append((x_, y_))
                break
            else:
                break
            y_ += 1
        
        # down
        x_, y_ = x, y - 1
        while y_ > 0:
            if not self.board[x_][y_]:
                moves_out.append((x_, y_))
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                moves_out.append((x_, y_))
                break
            else:
                break
            y_ -= 1
        
        return moves_out
    
    def get_valid_moves_knight(self, piece: Piece):
        moves_out = []
        x, y = piece.position
        moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1), (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
        for move in moves:
            x_, y_ = move
            if x_ < 0 or x_ > 7 or y_ < 0 or y_ > 7:
                continue
            if not self.board[x_][y_]:
                moves_out.append(move)
            
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                    moves_out.append(move)
        return moves_out
    
    def get_valid_moves_bishop(self, piece: Piece):
        moves_out = []
        x, y = piece.position
        
        dir_combs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dir_comb in dir_combs:
            x_, y_ = x + dir_comb[0], y + dir_comb[1]
            while x_ > 0 and x_ < 7 and y_ > 0 and y_ < 7:
                if not self.board[x_][y_]:
                    moves_out.append((x_, y_))
                elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                    moves_out.append((x_, y_))
                    break
                else:
                    break
                x_ += dir_comb[0]
                y_ += dir_comb[1]
        return moves_out
    
    def get_valid_moves_queen(self, piece: Piece):
        return self.get_valid_moves_rook(piece) + self.get_valid_moves_bishop(piece)
    
    def get_valid_moves_king(self, piece: Piece):
        moves_out = []
        x, y = piece.position
        moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
        for move in moves:
            x_, y_ = move
            if x_ < 0 or x_ > 7 or y_ < 0 or y_ > 7:
                continue
            if not self.board[x_][y_]:
                moves_out.append(move)
            elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                moves_out.append(move)

        return moves_out
    
    def is_check(self, player: Player):
        opp_player = self.player_black if player == self.player_white else self.player_white
        opp_king_pos = next(piece.position for piece in opp_player.pieces if piece.type == PieceType.KING)
        return any(opp_king_pos in self.get_valid_actions(player).values())
    
    def is_checkmate(self, player: Player):
        opp_player = self.player_black if player == self.player_white else self.player_white
        opp_player_moves = self.get_valid_actions(opp_player)
        for piece, move in opp_player_moves.items():
            board_copy = deepcopy(self)
            board_copy.act(opp_player, piece, move)
            if not board_copy.is_check(player):
                return False
        return True

    @staticmethod
    def square_str_to_pos(square_str):
        letters = 'ABCDEFGH'
        col = letters.index(square_str[0])
        row = int(square_str[1]) - 1
        return col, row
    
    def print_board(self):
        print(f"\n  {'-'*55}")
        for i in range(7, -1, -1):
            for j in range(8):
                piece = self.board[j][i]
                if piece:
                    print(f"{f'{i + 1} ' if j == 0 else ''}|{piece.color.name[0]}-{piece.type.name[:2]}|", end=" ")
                else:
                    print(f"{f'{i + 1} ' if j == 0 else ''}| .. |", end=" ")
            print(f"\n  {'-'*55}")
        
        print(f"    {'      '.join(list('ABCDEFGH'))}")
