import copy

from chess_backend.Board import Board
from chess_backend.common import PieceEnum, PlayerEnum, Position, IllegalMoveException


class ActionMove:
    class Cache:
        def __init__(self):
            self.last_move_double_file = None
            self.unpromote_position = None
            self.revert_move = []
            self.to_untake = None
            self.can_castle_king_side = None
            self.can_castle_queen_side = None
            self.turn = None
            self.move_without_take_and_pawn_move = 0

    def __init__(self, pos_from, pos_to,
                 to_move=None,
                 to_take=None,
                 is_double_move=False,
                 is_queen_side_castle=False,
                 is_king_side_castle=False,
                 promote_piece=None,
                 claim_draw=False):
        self.move_from = pos_from
        self.move_to = pos_to
        self.to_move = to_move
        self.to_take = to_take
        self.is_double_move = is_double_move
        self.is_queen_side_castle = is_queen_side_castle
        self.is_king_side_castle = is_king_side_castle
        self.promote_piece = promote_piece
        self.claim_draw = claim_draw
        if self.to_move is None:
            self.to_move = [(pos_from, pos_to)]

    def __eq__(self, other):
        return isinstance(other, ActionMove) and \
               self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.move_from) +
                    str(self.move_to) +
                    str(self.to_take))

    def apply(self, state, cache=None):

        if self.claim_draw:
            state.draw_claimed = True
            return

        if cache:
            cache.can_castle_king_side = state.specific[state.board.turn].can_castle_king_side
            cache.can_castle_queen_side = state.specific[state.board.turn].can_castle_queen_side

        if self.is_king_side_castle:
            state.specific[state.board.turn].can_castle_king_side = False
        if self.is_queen_side_castle:
            state.specific[state.board.turn].can_castle_queen_side = False
        if state.board.board[self.move_from.file][self.move_from.rank].piece == PieceEnum.king:
            state.specific[state.board.turn].can_castle_king_side = False
            state.specific[state.board.turn].can_castle_queen_side = False
        if state.board.board[self.move_from.file][self.move_from.rank].piece == PieceEnum.rook:
            if state.board.turn == PlayerEnum.white:
                if self.move_from.file == 0 and self.move_from.rank == 0:
                    state.specific[state.board.turn].can_castle_queen_side = False
                if self.move_from.file == 7 and self.move_from.rank == 0:
                    state.specific[state.board.turn].can_castle_king_side = False
            elif state.board.turn == PlayerEnum.black:
                if self.move_from.file == 0 and self.move_from.rank == 7:
                    state.specific[state.board.turn].can_castle_queen_side = False
                if self.move_from.file == 7 and self.move_from.rank == 7:
                    state.specific[state.board.turn].can_castle_king_side = False

        if self.to_take is not None:
            ref = state.board.board[self.to_take.file][self.to_take.rank]
            if cache:
                cache.to_untake = (self.to_take.file, self.to_take.rank, ref.piece, ref.player)
            ref.piece = None
            ref.player = None

        if cache:
            cache.move_without_take_and_pawn_move = state.move_without_take_and_pawn_move

        state.move_without_take_and_pawn_move += 1
        if self.move_from is not None:
            if state.board.board[self.move_from.file][self.move_from.rank].piece == PieceEnum.pawn:
                state.move_without_take_and_pawn_move = 0
            if self.to_take is not None:
                state.move_without_take_and_pawn_move = 0

        for move in self.to_move:
            from_ref = state.board.board[move[0].file][move[0].rank]
            to_ref = state.board.board[move[1].file][move[1].rank]
            if cache:
                cache.revert_move.append(((move[0].file, move[0].rank, from_ref.piece, from_ref.player),
                                          (move[1].file, move[1].rank, to_ref.piece, to_ref.player)))

            to_ref.piece = from_ref.piece
            to_ref.player = from_ref.player
            from_ref.piece = None
            from_ref.player = None

        if self.promote_piece is not None:
            if cache:
                cache.unpromote_position = self.move_to
            to_ref = state.board.board[self.move_to.file][self.move_to.rank]
            to_ref.piece = self.promote_piece

        if cache:
            cache.turn = state.board.turn
        state.board.turn = PlayerEnum.white if state.board.turn == PlayerEnum.black else PlayerEnum.black
        if cache:
            cache.last_move_double_file = state.last_move_double_file

        state.last_move_double_file = self.move_to.file if self.is_double_move else None

    def unapply(self, state, cache):

        if self.claim_draw:
            state.draw_claimed = False
            return

        state.last_move_double_file = cache.last_move_double_file
        state.move_without_take_and_pawn_move = cache.move_without_take_and_pawn_move
        state.board.turn = cache.turn
        if cache.unpromote_position:
            ref = state.board.board[cache.unpromote_position.file][cache.unpromote_position.rank]
            ref.piece = PieceEnum.pawn
        for from_info, to_info in reversed(cache.revert_move):
            from_file, from_rank, from_piece, from_player = from_info
            to_file, to_rank, to_piece, to_player = to_info
            state.board.board[from_file][from_rank].piece = from_piece
            state.board.board[from_file][from_rank].player = from_player
            state.board.board[to_file][to_rank].piece = to_piece
            state.board.board[to_file][to_rank].player = to_player
        if cache.to_untake:
            untake_file, untake_rank, untake_piece, untake_player = cache.to_untake
            state.board.board[untake_file][untake_rank].piece = untake_piece
            state.board.board[untake_file][untake_rank].player = untake_player

        state.specific[state.board.turn].can_castle_king_side = cache.can_castle_king_side
        state.specific[state.board.turn].can_castle_queen_side = cache.can_castle_queen_side


only_king = {
    PieceEnum.pawn: 0,
    PieceEnum.rook: 0,
    PieceEnum.knight: 0,
    PieceEnum.bishop: 0,
    PieceEnum.queen: 0,
    PieceEnum.king: 1
}
king_bishop = {
    PieceEnum.pawn: 0,
    PieceEnum.rook: 0,
    PieceEnum.knight: 0,
    PieceEnum.bishop: 1,
    PieceEnum.queen: 0,
    PieceEnum.king: 1
}
king_knight = {
    PieceEnum.pawn: 0,
    PieceEnum.rook: 0,
    PieceEnum.knight: 1,
    PieceEnum.bishop: 0,
    PieceEnum.queen: 0,
    PieceEnum.king: 1
}


class GameState:
    NOT_STARTED = 0
    RUNNING = 1
    WHITE_WON = 2
    BLACK_WON = 3
    STALEMATE = 4
    DRAW = 5

    default_pieces = [
        (0, 1, PieceEnum.pawn, PlayerEnum.white),
        (1, 1, PieceEnum.pawn, PlayerEnum.white),
        (2, 1, PieceEnum.pawn, PlayerEnum.white),
        (3, 1, PieceEnum.pawn, PlayerEnum.white),
        (4, 1, PieceEnum.pawn, PlayerEnum.white),
        (5, 1, PieceEnum.pawn, PlayerEnum.white),
        (6, 1, PieceEnum.pawn, PlayerEnum.white),
        (7, 1, PieceEnum.pawn, PlayerEnum.white),
        (0, 0, PieceEnum.rook, PlayerEnum.white),
        (1, 0, PieceEnum.knight, PlayerEnum.white),
        (2, 0, PieceEnum.bishop, PlayerEnum.white),
        (3, 0, PieceEnum.queen, PlayerEnum.white),
        (4, 0, PieceEnum.king, PlayerEnum.white),
        (5, 0, PieceEnum.bishop, PlayerEnum.white),
        (6, 0, PieceEnum.knight, PlayerEnum.white),
        (7, 0, PieceEnum.rook, PlayerEnum.white),
        (0, 6, PieceEnum.pawn, PlayerEnum.black),
        (1, 6, PieceEnum.pawn, PlayerEnum.black),
        (2, 6, PieceEnum.pawn, PlayerEnum.black),
        (3, 6, PieceEnum.pawn, PlayerEnum.black),
        (4, 6, PieceEnum.pawn, PlayerEnum.black),
        (5, 6, PieceEnum.pawn, PlayerEnum.black),
        (6, 6, PieceEnum.pawn, PlayerEnum.black),
        (7, 6, PieceEnum.pawn, PlayerEnum.black),
        (0, 7, PieceEnum.rook, PlayerEnum.black),
        (1, 7, PieceEnum.knight, PlayerEnum.black),
        (2, 7, PieceEnum.bishop, PlayerEnum.black),
        (3, 7, PieceEnum.queen, PlayerEnum.black),
        (4, 7, PieceEnum.king, PlayerEnum.black),
        (5, 7, PieceEnum.bishop, PlayerEnum.black),
        (6, 7, PieceEnum.knight, PlayerEnum.black),
        (7, 7, PieceEnum.rook, PlayerEnum.black)
    ]

    class SpecificPlayerState:
        def __init__(self):
            self.can_castle_queen_side = False
            self.can_castle_king_side = False

    # official starting chess position
    def __init__(self):
        self.board = Board()
        self.last_move_double_file = None
        self.specific = dict()
        self.specific[PlayerEnum.white] = self.SpecificPlayerState()
        self.specific[PlayerEnum.black] = self.SpecificPlayerState()
        self.draw_claimed = False
        self.move_without_take_and_pawn_move = 0
        self.legal_moves = []
        self.state = self.NOT_STARTED

    def is_running(self):
        return self.state == self.RUNNING

    def start_new(self):
        self.setup_board()
        self.state = self.RUNNING

    def setup_board(self):
        self.board.clear_board()
        self.board.turn = PlayerEnum.white
        self.specific[PlayerEnum.white].can_castle_queen_side = True
        self.specific[PlayerEnum.white].can_castle_king_side = True
        self.specific[PlayerEnum.black].can_castle_queen_side = True
        self.specific[PlayerEnum.black].can_castle_king_side = True
        for definition in self.default_pieces:
            self.board.board[definition[0]][definition[1]].piece = definition[2]
            self.board.board[definition[0]][definition[1]].player = definition[3]
        self.update_legal_moves()

    def __get_all_legal_moves(self):
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if self.board.board[file][rank].player == self.board.turn:
                    moves = self.get_legal_moves(Position(file, rank))
                    legal_moves += moves

        self.add_non_movement_legal_actions(legal_moves)
        return legal_moves

    def get_legal_moves(self, pos):
        moves = []

        from_ref = self.board.board[pos.file][pos.rank]
        from_player = from_ref.player
        if from_player == self.board.turn and from_ref.piece is not None:
            piece = self.board.board[pos.file][pos.rank].piece
            if piece == PieceEnum.pawn:
                moves = self.__get_legal_moves_pawn(pos)
            elif piece == PieceEnum.king:
                moves = self.__get_legal_moves_king(pos)
            elif piece == PieceEnum.bishop:
                moves = self.__get_legal_moves_bishop(pos)
            elif piece == PieceEnum.rook:
                moves = self.__get_legal_moves_rook(pos)
            elif piece == PieceEnum.knight:
                moves = self.__get_legal_moves_knight(pos)
            elif piece == PieceEnum.queen:
                moves = self.__get_legal_moves_queen(pos)

        legal_moves = []
        for move in moves:
            cache = ActionMove.Cache()
            move.apply(self, cache)
            if not self.is_king_threaten(from_player):
                legal_moves.append(move)
            move.unapply(self, cache)

        return legal_moves

    def apply(self, action):
        if action not in self.legal_moves:
            raise IllegalMoveException

        action.apply(self)
        self.update_legal_moves()

        if not self.legal_moves:
            if not self.is_king_threaten(self.board.turn):
                self.state = self.STALEMATE
            elif self.board.turn == PlayerEnum.white:
                # white has no moves left and king is threaten, black won
                self.state = self.BLACK_WON
            else:
                self.state = self.WHITE_WON

        # basic draw conditions checking
        white_counts = {
            PieceEnum.pawn: 0,
            PieceEnum.rook: 0,
            PieceEnum.knight: 0,
            PieceEnum.bishop: 0,
            PieceEnum.queen: 0,
            PieceEnum.king: 0,
        }
        white_even_bishops = 0
        white_odd_bishops = 0
        black_even_bishops = 0
        black_odd_bishops = 0
        black_counts = copy.copy(white_counts)

        for file in range(8):
            for rank in range(8):
                if self.board.board[file][rank].player == PlayerEnum.white:
                    white_counts[self.board.board[file][rank].piece] += 1
                    if self.board.board[file][rank].piece == PieceEnum.bishop:
                        if file + rank % 2 == 0:
                            white_even_bishops += 1
                        else:
                            white_odd_bishops += 1

                elif self.board.board[file][rank].player == PlayerEnum.black:
                    black_counts[self.board.board[file][rank].piece] += 1
                    if self.board.board[file][rank].piece == PieceEnum.bishop:
                        if file + rank % 2 == 0:
                            black_even_bishops += 1
                        else:
                            black_odd_bishops += 1

        if white_counts == only_king:
            if black_counts == only_king or \
                    black_counts == king_bishop or \
                    black_counts == king_knight:
                self.state = self.DRAW

        if black_counts == only_king:
            if white_counts == only_king or \
                    white_counts == king_bishop or \
                    white_counts == king_knight:
                self.state = self.DRAW

        if black_counts == king_bishop and white_counts == king_bishop:
            if white_even_bishops == black_even_bishops and \
                    white_odd_bishops == black_odd_bishops:
                self.state = self.DRAW

        if self.draw_claimed:
            self.state = self.DRAW

    def update_legal_moves(self):
        self.legal_moves = self.__get_all_legal_moves()

    def add_non_movement_legal_actions(self, moves):
        if self.move_without_take_and_pawn_move > 2 * 50:
            # there have been 50 moves without take or pawn move already
            moves.append(ActionMove(pos_from=None, pos_to=None, claim_draw=True))
        elif self.move_without_take_and_pawn_move > 2 * 49:
            # we are about to make 50th move without take or pawn move
            for move in moves:
                if move.to_take is None and \
                        self.board.board[move.move_from.file][move.move_from.rank].piece != PieceEnum.pawn:
                    moves.append(ActionMove(pos_from=None, pos_to=None, claim_draw=True))
                    break

    def clone(self):
        return copy.deepcopy(self)

    def get_winner_score(self):
        if self.state in (self.DRAW, self.STALEMATE):
            return 0
        return 1

    def __threats(self, source, target):
        player = self.board.board[source.file][source.rank].player
        piece = self.board.board[source.file][source.rank].piece
        if piece == PieceEnum.pawn:
            direction = 1 if player == PlayerEnum.white else -1
            return target.rank == source.rank + direction and \
                (target.file == source.file + 1 or target.file == source.file - 1)
        elif piece == PieceEnum.knight:
            dx = target.file - source.file
            dy = target.rank - source.rank
            # a trick, 2 can be decomposed only as 1*2, with signs giving all knigts combinations
            return abs(dx * dy) == 2
        elif piece == PieceEnum.rook:
            if source.file == target.file:
                # check there are no other pieces in way
                start = min(source.rank, target.rank)
                end = max(source.rank, target.rank)
                for rank in range(start + 1, end):
                    if self.board.board[source.file][rank].player is not None:
                        return False
                return True
            elif source.rank == target.rank:
                # check there are no other pieces in way
                start = min(source.file, target.file)
                end = max(source.file, target.file)
                for file in range(start + 1, end):
                    if self.board.board[file][source.rank].player is not None:
                        return False
                return True
            return False
        elif piece == PieceEnum.bishop:
            dx = target.file - source.file
            dy = target.rank - source.rank
            if abs(dx) == abs(dy):
                # check there are no other pieces in way
                dir_file = 1 if target.file - source.file > 0 else -1
                dir_rank = 1 if target.rank - source.rank > 0 else - 1
                file, rank = source.file + dir_file, source.rank + dir_rank
                while file != target.file:
                    if self.board.board[file][rank].player is not None:
                        return False

                    file += dir_file
                    rank += dir_rank
                return True
        elif piece == PieceEnum.queen:
            dx = target.file - source.file
            dy = target.rank - source.rank
            if abs(dx) == abs(dy):
                # check there are no other pieces in way
                dir_file = 1 if target.file - source.file > 0 else -1
                dir_rank = 1 if target.rank - source.rank > 0 else - 1
                file, rank = source.file + dir_file, source.rank + dir_rank
                while file != target.file:
                    if self.board.board[file][rank].player is not None:
                        return False

                    file += dir_file
                    rank += dir_rank
                return True
            elif source.file == target.file:
                # check there are no other pieces in way
                start = min(source.rank, target.rank)
                end = max(source.rank, target.rank)
                for rank in range(start + 1, end):
                    if self.board.board[source.file][rank].player is not None:
                        return False
                return True
            elif source.rank == target.rank:
                # check there are no other pieces in way
                start = min(source.file, target.file)
                end = max(source.file, target.file)
                for file in range(start + 1, end):
                    if self.board.board[file][source.rank].player is not None:
                        return False
                return True

            return False
        elif piece == PieceEnum.king:
            dx = target.file - source.file
            dy = target.rank - source.rank
            return max(abs(dx), abs(dy)) == 1

        return False

    def __is_position_threaten(self, position, enemy):
        for file in range(8):
            for rank in range(8):
                if self.board.board[file][rank].player == enemy:
                    if self.__threats(Position(file, rank), position):
                        return True
        return False

    def is_king_threaten(self, player):
        for file in range(8):
            for rank in range(8):
                if self.board.board[file][rank].player == player and \
                        self.board.board[file][rank].piece == PieceEnum.king:
                    enemy = PlayerEnum.white if player == PlayerEnum.black else PlayerEnum.black
                    return self.__is_position_threaten(Position(file, rank), enemy)
        return False

    def __enmurate_positions_in_direction(self, pos, direction):
        next_pos = Position(pos.file + direction[0], pos.rank + direction[1])
        while 0 <= next_pos.file < 8 and 0 <= next_pos.rank < 8:
            yield next_pos
            next_pos = Position(next_pos.file + direction[0], next_pos.rank + direction[1])

    def __get_legal_moves_pawn(self, pos):
        ref = self.board.board[pos.file][pos.rank]

        if ref.player != self.board.turn:
            return []

        moves = []
        direction = 1 if self.board.turn == PlayerEnum.white else -1
        start_rank = 1 if self.board.turn == PlayerEnum.white else 6
        end_rank = 7 if self.board.turn == PlayerEnum.white else 0
        if pos.rank != end_rank:
            move_pos = Position(pos.file, pos.rank + direction)

            if self.board.board[move_pos.file][move_pos.rank].piece is None:
                if pos.rank == end_rank - direction:
                    for promote_piece in (PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook, PieceEnum.queen):
                        moves.append(ActionMove(pos, move_pos, promote_piece=promote_piece))
                else:
                    moves.append(ActionMove(pos,
                                            move_pos))
                    if pos.rank == start_rank:
                        move_pos = Position(pos.file, pos.rank + 2 * direction)
                        if self.board.board[move_pos.file][move_pos.rank].piece is None:
                            moves.append(ActionMove(pos,
                                                    move_pos,
                                                    is_double_move=True))
            for side in (-1, 1):
                take_pos = Position(pos.file + side, pos.rank + direction)
                if 0 <= take_pos.file < 8:
                    if self.board.board[take_pos.file][take_pos.rank].player is not None and \
                            self.board.board[take_pos.file][take_pos.rank].player != ref.player:

                        if pos.rank == end_rank - direction:
                            # promote by taking
                            for promote_piece in (PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook, PieceEnum.queen):
                                moves.append(ActionMove(pos,
                                                        take_pos,
                                                        to_take=take_pos,
                                                        promote_piece=promote_piece))
                        else:
                            moves.append(ActionMove(pos,
                                                    take_pos,
                                                    to_take=take_pos))

                    if self.board.board[take_pos.file][take_pos.rank].player is None and \
                            self.last_move_double_file == take_pos.file and \
                            take_pos.rank == end_rank - 2 * direction:
                        # en passant
                        moves.append(ActionMove(pos,
                                                take_pos,
                                                to_take=Position(take_pos.file, pos.rank), ))

        return moves

    def __get_legal_moves_king(self, pos):
        moves = []
        player = self.board.board[pos.file][pos.rank].player
        enemy = PlayerEnum.white if player == PlayerEnum.black else PlayerEnum.black
        for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)):
            for move_pos in self.__enmurate_positions_in_direction(pos, direction):
                if self.board.board[move_pos.file][move_pos.rank].player is not None:
                    if self.board.board[move_pos.file][move_pos.rank].player != self.board.turn:
                        moves.append(ActionMove(pos, move_pos, to_take=move_pos))
                else:
                    moves.append(ActionMove(pos, move_pos))
                break
        # castling
        if self.specific[self.board.turn].can_castle_queen_side:
            if not self.__is_position_threaten(Position(2, pos.rank), enemy) and \
                    not self.__is_position_threaten(Position(3, pos.rank), enemy) and \
                    not self.__is_position_threaten(Position(4, pos.rank), enemy) and \
                    self.board.board[1][pos.rank].player is None and \
                    self.board.board[2][pos.rank].player is None and \
                    self.board.board[3][pos.rank].player is None:
                moves.append(ActionMove(pos,
                                        Position(1, pos.rank),
                                        to_move=[(pos, Position(1, pos.rank)),
                                                 (Position(0, pos.rank), Position(2, pos.rank))
                                                 ],
                                        is_queen_side_castle=True)
                             )

        if self.specific[self.board.turn].can_castle_king_side:
            if not self.__is_position_threaten(Position(4, pos.rank), enemy) and \
                    not self.__is_position_threaten(Position(5, pos.rank), enemy) and \
                    self.board.board[5][pos.rank].player is None and \
                    self.board.board[6][pos.rank].player is None:
                moves.append(ActionMove(pos,
                                        Position(6, pos.rank),
                                        to_move=[(pos, Position(6, pos.rank)),
                                                 (Position(7, pos.rank), Position(5, pos.rank))
                                                 ],
                                        is_king_side_castle=True)
                             )

        return moves

    def __get_legal_moves_bishop(self, pos):
        moves = []
        for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            for move_pos in self.__enmurate_positions_in_direction(pos, direction):
                if self.board.board[move_pos.file][move_pos.rank].player is not None:
                    if self.board.board[move_pos.file][move_pos.rank].player != self.board.turn:
                        moves.append(ActionMove(pos, move_pos, to_take=move_pos))
                    break
                moves.append(ActionMove(pos, move_pos))
        return moves

    def __get_legal_moves_rook(self, pos):
        moves = []
        for direction in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            for move_pos in self.__enmurate_positions_in_direction(pos, direction):
                if self.board.board[move_pos.file][move_pos.rank].player is not None:
                    if self.board.board[move_pos.file][move_pos.rank].player != self.board.turn:
                        moves.append(ActionMove(pos, move_pos, to_take=move_pos))
                    break
                moves.append(ActionMove(pos, move_pos))
        return moves

    def __get_legal_moves_knight(self, pos):
        moves = []
        for offset in ((2, 1), (1, 2), (-2, 1), (2, -1), (-2, -1), (-1, 2), (1, -2), (-1, -2)):
            move_pos = Position(pos.file + offset[0], pos.rank + offset[1])
            if 0 <= move_pos.file < 8 and 0 <= move_pos.rank < 8:
                if self.board.board[move_pos.file][move_pos.rank].player != self.board.turn:
                    to_take = None
                    if self.board.board[move_pos.file][move_pos.rank].player is not None:
                        to_take = move_pos
                    moves.append(ActionMove(pos,
                                            move_pos,
                                            to_take=to_take))

        return moves

    def __get_legal_moves_queen(self, pos):
        moves = []
        for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)):
            for move_pos in self.__enmurate_positions_in_direction(pos, direction):
                if self.board.board[move_pos.file][move_pos.rank].player is not None:
                    if self.board.board[move_pos.file][move_pos.rank].player != self.board.turn:
                        moves.append(ActionMove(pos, move_pos, to_take=move_pos))
                    break
                moves.append(ActionMove(pos, move_pos))
        return moves
