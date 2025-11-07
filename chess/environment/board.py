from chess.environment.piece import Piece, PieceType, piece_captured_score
from chess.environment.player import Player
from chess.environment.color import Color
from chess.environment.utils import square_pos_to_str
from copy import deepcopy
from enum import Enum

class ActionType(Enum):
    MOVE = 1,
    CASTLE = 2

slide_move_directions = {
        PieceType.ROOK: ((-1, 0), (1, 0), (0, -1), (0, 1)),
        PieceType.BISHOP: ((-1, -1), (-1, 1), (1, -1), (1, 1)),
        PieceType.QUEEN: ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
}

class Board:
    def __init__(self, player_white: Player, player_black: Player, main_board=True):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.player_white = player_white
        self.player_black = player_black
        self.init_board()
        self.main_board = main_board

    def init_board(self):
        for player in [self.player_white, self.player_black]:
            for piece in player.pieces:
                self.board[piece.position[0]][piece.position[1]] = piece
    
    def get_opp_player(self, player: Player):
        return self.player_black if player.color == Color.WHITE else self.player_white
    
    def is_draw(self):
        # TODO expand with other auto-draw scenarios
        if len(self.player_white.pieces) == 1 and len(self.player_black.pieces) == 1:
            assert next(iter(self.player_white.pieces)).type == PieceType.KING and next(iter(self.player_black.pieces)).type == PieceType.KING
            return True
        
        return False
    
    def has_checked(self, player: Player):
        attack_options_pieces, _ = self.get_attack_options(player)
        return PieceType.KING in [x.type for x in attack_options_pieces]

    def has_checkmated(self, player: Player):
        if not self.has_checked(player):
            return False 

        opp_player = self.get_opp_player(player)
        valid_actions = self.get_valid_actions(opp_player)

        # if actions dict is empty for move and castling options
        return not any(actions for _, actions in valid_actions.items())

    
    def is_stalemate(self, player: Player):
        opp_player = self.get_opp_player(player)
        if self.has_checked(opp_player):
            return False # curr turn player in check, opp player has checked
        
        valid_actions = self.get_valid_actions(player)
        return not any(actions for _, actions in valid_actions.items())
    
    def get_attack_options(self, player: Player):
        attack_options_out = []
        attack_moves = {move for piece in player.pieces for move in self.get_valid_moves(piece, attack_only=True)}
        for x, y in attack_moves:
            if self.board[x][y]:
                assert self.board[x][y].color != player.color
                attack_options_out.append((self.board[x][y]))
        
        attack_options_score = sum(piece_captured_score[x.type] for x in attack_options_out)
        return attack_options_out, attack_options_score


    def get_valid_actions(self, player: Player):
        # TODO split into two functions
        valid_actions = {ActionType.MOVE: {}, ActionType.CASTLE: {}}
        
        opp_player = self.get_opp_player(player)
        _, opp_player_attack_score = self.get_attack_options(opp_player)
        
        for piece in player.pieces:
            valid_moves_piece = []
            for move in self.get_valid_moves(piece):
                board_copy = deepcopy(self)
                board_copy.main_board = False
                piece_copy = board_copy.board[piece.position[0]][piece.position[1]]
                player_copy = board_copy.player_white if player.color == Color.WHITE else board_copy.player_black
                opp_player_copy = board_copy.get_opp_player(player_copy)
                piece_captured_type = board_copy.move(player_copy, piece_copy, move)
                move_score_base = piece_captured_score[piece_captured_type] if piece_captured_type else 0
                
                _, opp_player_copy_attack_score = board_copy.get_attack_options(opp_player_copy)
                if not board_copy.has_checked(opp_player_copy):
                    move_score = 1e9 if board_copy.has_checkmated(player_copy) else move_score_base + (opp_player_attack_score - opp_player_copy_attack_score)
                    valid_moves_piece.append((move, move_score))

            if valid_moves_piece:
                valid_actions[ActionType.MOVE][piece] = valid_moves_piece
        
        for king_side in [True, False]:
            if self.can_castle(player, king_side):
                board_copy = deepcopy(self)
                board_copy.main_board = False
                player_copy = board_copy.player_white if player.color == Color.WHITE else board_copy.player_black
                opp_player_copy = board_copy.get_opp_player(player_copy)

                board_copy.castle(player_copy, king_side)
                _, opp_player_copy_attack_score = board_copy.get_attack_options(opp_player_copy)

                # note that check for castle into check is done in can_castle
                castle_score = 1e9 if board_copy.has_checkmated(player_copy) else (opp_player_attack_score - opp_player_copy_attack_score)
                valid_actions[ActionType.CASTLE][king_side] = castle_score
        
        return valid_actions
    
    def move(self, player: Player, piece: Piece, move: tuple[int, int]):
        if piece not in player.pieces:
            raise ValueError(f"Piece {piece.type} at {square_pos_to_str(piece.position)} not found in player {player.color}'s pieces")
        
        piece_moves = self.get_valid_moves(piece)
        if move not in piece_moves:
            raise ValueError(f"Invalid move for piece {piece.type} at {piece.position}: {move}")
        
        piece_captured_type = None
        opp_player = self.get_opp_player(player)
        self.board[piece.position[0]][piece.position[1]] = None
        
        if self.board[move[0]][move[1]]:
            piece_eliminated = self.board[move[0]][move[1]]
            if self.main_board:
                print(f"{player} captures {piece_eliminated} using {piece}")
            
            piece_captured_type = piece_eliminated.type
            piece_eliminated.position = None
            opp_player.pieces.remove(piece_eliminated)
            opp_player.pieces_eliminated.add(piece_eliminated)

        self.board[move[0]][move[1]] = piece
        piece.has_moved = True
        piece.position = move

        # promote pawn
        if piece.type == PieceType.PAWN and (move[1] == 0 or move[1] == 7):
            if self.main_board:
                print(f'Promoting Pawn at {square_pos_to_str(piece.position)} to Queen')
            piece.type = PieceType.QUEEN
        
        return piece_captured_type
    
    def get_valid_moves(self, piece: Piece, attack_only=False):
        match piece.type:
            case PieceType.PAWN:
                return self.get_valid_attacks_pawn(piece) if attack_only else self.get_valid_moves_pawn(piece)
            case PieceType.ROOK:
                return self.get_valid_moves_slide(piece)
            case PieceType.KNIGHT:
                return self.get_valid_moves_knight(piece)
            case PieceType.BISHOP:
                return self.get_valid_moves_slide(piece)
            case PieceType.QUEEN:
                return self.get_valid_moves_slide(piece)
            case PieceType.KING:
                return self.get_valid_moves_king(piece)

    def get_valid_attacks_pawn(self, piece: Piece):
        # get attacking (capture) moves for pawn based on current game state
        moves_out = []
        dir = 1 if piece.color == Color.WHITE else -1
        moves_angled = [(piece.position[0] + 1, piece.position[1] + dir), (piece.position[0] - 1, piece.position[1] + dir)]
        for move in moves_angled:
            x, y = move
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            if self.board[x][y] and self.board[x][y].color != piece.color:
                moves_out.append(move)
                
        return moves_out

    def get_valid_moves_pawn(self, piece: Piece):
        moves_out = []
        dir = 1 if piece.color == Color.WHITE else - 1

        # straight
        moves_straight = []
        if not self.board[piece.position[0]][piece.position[1] + dir]:
            moves_straight.append((piece.position[0], piece.position[1] + dir))

        if (dir == 1 and piece.position[1] == 1) or (dir == -1 and piece.position[1] == 6):
            if not self.board[piece.position[0]][piece.position[1] + dir] and not self.board[piece.position[0]][piece.position[1] + 2 * dir]:
                moves_straight.append((piece.position[0], piece.position[1] + 2 * dir))
        
        if moves_straight:
            moves_out += moves_straight

        return moves_out + self.get_valid_attacks_pawn(piece)
    

    def get_valid_moves_slide(self, piece: Piece):
        move_directions = slide_move_directions[piece.type]
        moves_out = []
        x, y = piece.position
        
        for x_change, y_change in move_directions:
            x_, y_ = x + x_change, y + y_change
            while x_ >= 0 and x_ <= 7 and y_ >= 0 and y_ <= 7:
                if not self.board[x_][y_]:
                    moves_out.append((x_, y_))
                elif self.board[x_][y_] and self.board[x_][y_].color != piece.color:
                    moves_out.append((x_, y_))
                    break
                else:
                    break
                x_ += x_change
                y_ += y_change
        
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
    
    def castle(self, player: Player, king_side=True):
        if self.main_board:
            print(f"{player} castling {'king side' if king_side else 'queen side'}\n")
        
        col = 0 if player.color == Color.WHITE else 7
        rook_row = 7 if king_side else 0
        king_row = 4

        king = self.board[king_row][col]
        rook = self.board[rook_row][col]

        self.board[king_row][col] = None
        self.board[rook_row][col] = None

        king_move = (6, col) if king_side else (2, col)
        rook_move = (5, col) if king_side else (3, col)
        self.board[king_move[0]][king_move[1]] = king
        self.board[rook_move[0]][rook_move[1]] = rook
        king.position = king_move
        rook.position = rook_move
        
    
    def can_castle(self, player: Player, king_side=True):
        opp_player = self.get_opp_player(player)
        if self.has_checked(opp_player):
            return False
        
        col = 0 if player.color == Color.WHITE else 7
        rook_row = 7 if king_side else 0
        king_row = 4

        gap_vacant = (
            not any([self.board[row][col] for row in range(king_row + 1, 7)])
            if king_side else
            not any([self.board[row][col] for row in range(1, king_row)])
        )

        if (
            self.board[king_row][col] and not self.board[king_row][col].has_moved and 
            self.board[rook_row][col] and not self.board[rook_row][col].has_moved and
            gap_vacant
        ):
            board_copy = deepcopy(self)
            board_copy.main_board = False
            player_copy = board_copy.player_white if player.color == Color.WHITE else board_copy.player_black
            opp_player_copy = board_copy.get_opp_player(player_copy)
            board_copy.castle(player_copy, king_side)
            return not board_copy.has_checked(opp_player_copy) # ensure that you cant castle into check (by opponent)
    
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
