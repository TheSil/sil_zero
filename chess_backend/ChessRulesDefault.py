from common import PieceEnum, PlayerEnum, Position, IllegalMoveException
from BoardState import BoardState

class ChessRulesDefault:

    class MoveDetails:
        def __init__(self, pos_from, pos_to,
                     to_move=None,
                     to_take=None,
                     is_double_move=False,
                     is_queen_side_castle=False,
                     is_king_side_castle=False):
            self.move_from = pos_from
            self.move_to = pos_to
            self.to_move = to_move
            self.to_take = to_take
            self.is_double_move = is_double_move
            self.is_queen_side_castle = is_queen_side_castle
            self.is_king_side_castle = is_king_side_castle
            if self.to_move is None:
                self.to_move = [(pos_from, pos_to)]

        def __eq__(self, other) :
            return self.move_from == other.move_from and self.move_to == other.move_to

    default_pieces = [
        (PieceEnum.pawn, 0, 1, PlayerEnum.white),
        (PieceEnum.pawn, 1, 1, PlayerEnum.white),
        (PieceEnum.pawn, 2, 1, PlayerEnum.white),
        (PieceEnum.pawn, 3, 1, PlayerEnum.white),
        (PieceEnum.pawn, 4, 1, PlayerEnum.white),
        (PieceEnum.pawn, 5, 1, PlayerEnum.white),
        (PieceEnum.pawn, 6, 1, PlayerEnum.white),
        (PieceEnum.pawn, 7, 1, PlayerEnum.white),
        (PieceEnum.rook, 0, 0, PlayerEnum.white),
        (PieceEnum.knight, 1, 0, PlayerEnum.white),
        (PieceEnum.bishop, 2, 0, PlayerEnum.white),
        (PieceEnum.queen, 3, 0, PlayerEnum.white),
        (PieceEnum.king, 4, 0, PlayerEnum.white),
        (PieceEnum.bishop, 5, 0, PlayerEnum.white),
        (PieceEnum.knight, 6, 0, PlayerEnum.white),
        (PieceEnum.rook, 7, 0, PlayerEnum.white),
        (PieceEnum.pawn, 0, 6, PlayerEnum.black),
        (PieceEnum.pawn, 1, 6, PlayerEnum.black),
        (PieceEnum.pawn, 2, 6, PlayerEnum.black),
        (PieceEnum.pawn, 3, 6, PlayerEnum.black),
        (PieceEnum.pawn, 4, 6, PlayerEnum.black),
        (PieceEnum.pawn, 5, 6, PlayerEnum.black),
        (PieceEnum.pawn, 6, 6, PlayerEnum.black),
        (PieceEnum.pawn, 7, 6, PlayerEnum.black),
        (PieceEnum.rook, 0, 7, PlayerEnum.black),
        (PieceEnum.knight, 1, 7, PlayerEnum.black),
        (PieceEnum.bishop, 2, 7, PlayerEnum.black),
        (PieceEnum.queen, 3, 7, PlayerEnum.black),
        (PieceEnum.king, 4, 7, PlayerEnum.black),
        (PieceEnum.bishop, 5, 7, PlayerEnum.black),
        (PieceEnum.knight, 6, 7, PlayerEnum.black),
        (PieceEnum.rook, 7, 7, PlayerEnum.black)
        ]

    # official starting chess position
    def __init__(self):
        self.state = BoardState()
        self.last_move_double_file = None
        self.specific = dict()
        self.specific[PlayerEnum.white] = dict()
        self.specific[PlayerEnum.black] = dict()
        self.specific[PlayerEnum.white]["can_castle_queen_side"] = True
        self.specific[PlayerEnum.white]["can_castle_king_side"] = True
        self.specific[PlayerEnum.black]["can_castle_queen_side"] = True
        self.specific[PlayerEnum.black]["can_castle_king_side"] = True

    def setup_board(self):
        self.state.turn = PlayerEnum.white
        self.state.clear_board()
        for definition in self.default_pieces:
            self.state.place_piece(definition[0],
                                   Position(definition[1], definition[2]),
                                   definition[3])

    def get_legal_moves_pawn(self, pos):
        moves = []
        ref = self.state.board[pos.file][pos.rank]

        dir = 1 if self.state.turn == PlayerEnum.white else -1
        start_rank = 1 if self.state.turn == PlayerEnum.white else 6
        end_rank = 7 if self.state.turn == PlayerEnum.white else 0
        if pos.rank != end_rank:
            move_pos = Position(pos.file, pos.rank + dir)
            if self.state.board[move_pos.file][move_pos.rank].piece is None:
                moves.append(self.MoveDetails(pos,
                                              move_pos))
                if pos.rank == start_rank:
                    move_pos = Position(pos.file, pos.rank + 2 * dir)
                    if self.state.board[move_pos.file][move_pos.rank].piece is None:
                        moves.append(self.MoveDetails(pos,
                                                      move_pos,
                                                      is_double_move=True))
            for side in (-1, 1):
                take_pos = Position(pos.file + side, pos.rank + dir)
                if 0 <= take_pos.file < 8:
                    if self.state.board[take_pos.file][take_pos.rank].player is not None and \
                            self.state.board[take_pos.file][take_pos.rank].player != ref.player:
                        moves.append(self.MoveDetails(pos,
                                                      take_pos,
                                                      to_take=take_pos))
                    if self.state.board[take_pos.file][take_pos.rank].player is None and \
                        self.last_move_double_file == take_pos.file:
                        # en passant
                        moves.append(self.MoveDetails(pos,
                                                      take_pos,
                                                      to_take=Position(take_pos.file, pos.rank),))

        return moves

    def enmurate_positions_in_direction(self, pos, dir):
        next_pos = Position(pos.file + dir[0], pos.rank + dir[1])
        while 0 <= next_pos.file < 8 and 0 <= next_pos.rank < 8:
            yield next_pos
            next_pos = Position(next_pos.file + dir[0], next_pos.rank + dir[1])

    def get_legal_moves_king(self, pos):
        moves = []
        for dir in ((1,1),(-1,1),(1,-1),(-1,-1),(-1,0),(1,0),(0,-1),(0,1)):
            for move_pos in self.enmurate_positions_in_direction(pos, dir):
                if self.state.board[move_pos.file][move_pos.rank].player is not None:
                    if self.state.board[move_pos.file][move_pos.rank].player != self.state.turn:
                        moves.append(self.MoveDetails(pos, move_pos, to_take=move_pos))
                else:
                    moves.append(self.MoveDetails(pos, move_pos))
                break
        # castling
        if self.specific[self.state.turn]["can_castle_queen_side"]:
            moves.append(self.MoveDetails(pos,
                                          Position(1, pos.rank),
                                          to_move=[(pos, Position(1, pos.rank)),
                                                   (Position(0, pos.rank), Position(2, pos.rank))
                                                   ],
                                          is_queen_side_castle=True)
                         )

        if self.specific[self.state.turn]["can_castle_king_side"]:
            moves.append(self.MoveDetails(pos,
                                          Position(6, pos.rank),
                                          to_move=[(pos, Position(6, pos.rank)),
                                                   (Position(7, pos.rank), Position(5, pos.rank))
                                                   ],
                                          is_king_side_castle=True)
                         )

        return moves

    def get_legal_moves_bishop(self, pos):
        moves = []
        for dir in ((1,1),(-1,1),(1,-1),(-1,-1)):
            for move_pos in self.enmurate_positions_in_direction(pos, dir):
                if self.state.board[move_pos.file][move_pos.rank].player is not None:
                    if self.state.board[move_pos.file][move_pos.rank].player != self.state.turn:
                        moves.append(self.MoveDetails(pos, move_pos, to_take=move_pos))
                    break
                moves.append(self.MoveDetails(pos, move_pos))
        return moves

    def get_legal_moves_rook(self, pos):
        moves = []
        for dir in ((-1,0),(1,0),(0,-1),(0,1)):
            for move_pos in self.enmurate_positions_in_direction(pos, dir):
                if self.state.board[move_pos.file][move_pos.rank].player is not None:
                    if self.state.board[move_pos.file][move_pos.rank].player != self.state.turn:
                        moves.append(self.MoveDetails(pos, move_pos, to_take=move_pos))
                    break
                moves.append(self.MoveDetails(pos, move_pos))
        return moves

    def get_legal_moves_knight(self, pos):
        moves = []
        for offset in ((2,1),(1,2),(-2,1),(2,-1),(-2,-1),(-1,2),(1,-2),(-1,-2)):
            move_pos = Position(pos.file + offset[0], pos.rank + offset[1])
            if 0 <= move_pos.file < 8 and 0 <= move_pos.rank < 8:
                if self.state.board[move_pos.file][move_pos.rank].player != self.state.turn:
                    to_take = None
                    if self.state.board[move_pos.file][move_pos.rank].player is not None:
                        to_take = move_pos
                    moves.append(self.MoveDetails(pos,
                                                  move_pos,
                                                  to_take=to_take))

        return moves

    def get_legal_moves_queen(self, pos):
        moves = []
        for dir in ((1,1),(-1,1),(1,-1),(-1,-1),(-1,0),(1,0),(0,-1),(0,1)):
            for move_pos in self.enmurate_positions_in_direction(pos, dir):
                if self.state.board[move_pos.file][move_pos.rank].player is not None:
                    if self.state.board[move_pos.file][move_pos.rank].player != self.state.turn:
                        moves.append(self.MoveDetails(pos, move_pos, to_take=move_pos))
                    break
                moves.append(self.MoveDetails(pos, move_pos))
        return moves

    def get_legal_moves(self, pos):
        from_ref = self.state.board[pos.file][pos.rank]

        if from_ref.player == self.state.turn and from_ref.piece is not None:
            piece = self.state.board[pos.file][pos.rank].piece
            if piece == PieceEnum.pawn:
                return self.get_legal_moves_pawn(pos)
            elif piece == PieceEnum.king:
                return self.get_legal_moves_king(pos)
            elif piece == PieceEnum.bishop:
                return self.get_legal_moves_bishop(pos)
            elif piece == PieceEnum.rook:
                return self.get_legal_moves_rook(pos)
            elif piece == PieceEnum.knight:
                return self.get_legal_moves_knight(pos)
            elif piece == PieceEnum.queen:
                return self.get_legal_moves_queen(pos)

        return []

    def do_move(self, pos_from, pos_to):
        legal_moves = self.get_legal_moves(pos_from)
        move_details = None
        for move in legal_moves:
            if move.move_to == pos_to:
                move_details = move
        if move_details is None:
            raise IllegalMoveException

        if move_details.is_king_side_castle:
            self.specific[self.state.turn]["can_castle_king_side"] = False
        if move_details.is_queen_side_castle:
            self.specific[self.state.turn]["can_castle_queen_side"] = False
        if self.state.board[pos_from.file][pos_from.rank].piece == PieceEnum.king:
            self.specific[self.state.turn]["can_castle_king_side"] = False
            self.specific[self.state.turn]["can_castle_queen_side"] = False
        if self.state.board[pos_from.file][pos_from.rank].piece == PieceEnum.rook:
            if self.state.turn == PlayerEnum.white:
                if pos_from.file == 0 and pos_from.rank == 0:
                    self.specific[self.state.turn]["can_castle_queen_side"] = False
                if pos_from.file == 7 and pos_from.rank == 0:
                    self.specific[self.state.turn]["can_castle_king_side"] = False
            elif self.state.turn == PlayerEnum.black:
                if pos_from.file == 0 and pos_from.rank == 7:
                    self.specific[self.state.turn]["can_castle_queen_side"] = False
                if pos_from.file == 7 and pos_from.rank == 7:
                    self.specific[self.state.turn]["can_castle_king_side"] = False

        if move_details.to_take is not None:
            ref = self.state.board[move_details.to_take.file][move_details.to_take.rank]
            ref.piece = None
            ref.player = None

        for move in move_details.to_move:
            from_ref = self.state.board[move[0].file][move[0].rank]
            to_ref = self.state.board[move[1].file][move[1].rank]
            to_ref.piece = from_ref.piece
            to_ref.player = from_ref.player
            from_ref.piece = None
            from_ref.player = None

        self.state.turn = PlayerEnum.white if self.state.turn == PlayerEnum.black else PlayerEnum.black
        self.last_move_double_file = move_details.move_to.file if move_details.is_double_move else None
