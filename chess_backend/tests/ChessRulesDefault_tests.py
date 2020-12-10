import unittest
from common import Position, PlayerEnum, PieceEnum, IllegalMoveException
import ChessRulesDefault

def prepare_board(config, turn):
    rules = ChessRulesDefault.ChessRulesDefault()
    for (file, rank), (player, piece) in config.items():
        rules.state.board[file][rank].player = player
        rules.state.board[file][rank].piece = piece
    rules.state.turn = turn
    return rules

def check_move_is_allowed(self,
                          board,
                          after_config_expected,
                          move_from,
                          move_to):
    rules = board

    rules.do_move(Position(*move_from),
                  Position(*move_to))

    for file in range(8):
        for rank in range(8):
            player, piece = None, None
            if (file, rank) in after_config_expected:
                player, piece = after_config_expected[file, rank]
            self.assertEqual(player, rules.state.board[file][rank].player)
            self.assertEqual(piece, rules.state.board[file][rank].piece)

def check_move_is_illegal(self,
                          board,
                          move_from,
                          move_to):
    rules = board

    with self.assertRaises(IllegalMoveException):
        rules.do_move(Position(*move_from),
                      Position(*move_to))


class SetupTests(unittest.TestCase):

    def test_setup(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.setup_board()
        self.assertEqual(None, rules.last_move_double_file)
        self.assertEqual(True, rules.specific[PlayerEnum.white].can_castle_queen_side)
        self.assertEqual(True, rules.specific[PlayerEnum.white].can_castle_king_side)
        self.assertEqual(True, rules.specific[PlayerEnum.black].can_castle_queen_side)
        self.assertEqual(True, rules.specific[PlayerEnum.black].can_castle_king_side)
        self.assertEqual(PlayerEnum.white, rules.state.turn)

        for rank in range(8):
            for file in range(8):
                if rank < 2:
                    self.assertEqual(PlayerEnum.white, rules.state.board[file][rank].player)
                elif rank < 6:
                    self.assertEqual(None, rules.state.board[file][rank].player)
                else:
                    self.assertEqual(PlayerEnum.black, rules.state.board[file][rank].player)

        for rank in (1,6):
            for file in range(8):
                self.assertEqual(PieceEnum.pawn,   rules.state.board[file][rank].piece)

        for rank in (0,7):
            self.assertEqual(PieceEnum.rook,   rules.state.board[0][rank].piece)
            self.assertEqual(PieceEnum.knight, rules.state.board[1][rank].piece)
            self.assertEqual(PieceEnum.bishop, rules.state.board[2][rank].piece)
            self.assertEqual(PieceEnum.queen,  rules.state.board[3][rank].piece)
            self.assertEqual(PieceEnum.king,   rules.state.board[4][rank].piece)
            self.assertEqual(PieceEnum.bishop, rules.state.board[5][rank].piece)
            self.assertEqual(PieceEnum.knight, rules.state.board[6][rank].piece)
            self.assertEqual(PieceEnum.rook,   rules.state.board[7][rank].piece)

# class WhitePawnLegalTests(unittest.TestCase):
#
#     def test_pawn_legal_moves_out_of_turn(self):
#         rules = ChessRulesDefault.ChessRulesDefault()
#         rules.state.board[1][1].player = PlayerEnum.white
#         rules.state.board[1][1].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.black
#         legal_moves = rules.get_legal_moves(Position(1, 1))
#         self.assertEqual(0, len(legal_moves))
#
#     def test_pawn_legal_moves(self):
#         rules = ChessRulesDefault.ChessRulesDefault()
#
#         rules.state.board[1][1].player = PlayerEnum.white
#         rules.state.board[1][1].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.white
#         legal_moves = rules.get_legal_moves(Position(1, 1))
#         self.assertEqual(2, len(legal_moves))
#         expected_legal_moves = [
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(1, 1),
#                                                                Position(1, 2)),
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(1, 1),
#                                                                Position(1, 3)),
#         ]
#         self.assertEqual(expected_legal_moves, legal_moves)
#
#         rules.state.board[3][3].player = PlayerEnum.white
#         rules.state.board[3][3].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.white
#         legal_moves = rules.get_legal_moves(Position(3, 3))
#         self.assertEqual(1, len(legal_moves))
#         expected_legal_moves = [
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(3, 3),
#                                                                Position(3, 4)),
#         ]
#         self.assertEqual(expected_legal_moves, legal_moves)
#
#         rules.state.board[3][4].player = PlayerEnum.black
#         rules.state.board[3][4].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.white
#         legal_moves = rules.get_legal_moves(Position(3, 3))
#         self.assertEqual(0, len(legal_moves))
#
#         rules.state.board[4][4].player = PlayerEnum.black
#         rules.state.board[4][4].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.white
#         legal_moves = rules.get_legal_moves(Position(3, 3))
#         self.assertEqual(1, len(legal_moves))
#         expected_legal_moves = [
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(3, 3),
#                                                                Position(4, 4)),
#         ]
#         self.assertEqual(expected_legal_moves, legal_moves)
#
#     def test_pawn_legal_en_passant(self):
#         rules = ChessRulesDefault.ChessRulesDefault()
#
#         rules.state.board[3][4].player = PlayerEnum.white
#         rules.state.board[3][4].piece = PieceEnum.pawn
#         rules.state.board[4][4].player = PlayerEnum.black
#         rules.state.board[4][4].piece = PieceEnum.pawn
#         rules.state.turn = PlayerEnum.white
#         rules.last_move_double_file = 4
#
#         legal_moves = rules.get_legal_moves(Position(3, 4))
#         self.assertEqual(2, len(legal_moves))
#         expected_legal_moves = [
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(3, 4),
#                                                                Position(3, 5)),
#             ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(3, 4),
#                                                                Position(4, 5)),
#         ]
#         self.assertEqual(expected_legal_moves, legal_moves)

class WhitePawnMoveTests(unittest.TestCase):

    def test_pawn_move_single(self):
        check_move_is_allowed(self,
            prepare_board(config={
                (1, 1): (PlayerEnum.white,PieceEnum.pawn)
                },
                turn=PlayerEnum.white),
            after_config_expected={
                (1, 2): (PlayerEnum.white, PieceEnum.pawn)
            },
            move_from=(1, 1),
            move_to=(1, 2)
        )

    def test_pawn_move_double(self):

        check_move_is_allowed(self,
            prepare_board(config={
                (1, 1): (PlayerEnum.white,PieceEnum.pawn)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (1, 3): (PlayerEnum.white, PieceEnum.pawn)
            },

            move_from=(1, 1),
            move_to=(1, 3)
        )

    def test_pawn_move_double_not_allowed(self):
        check_move_is_illegal(self,
            prepare_board(config={
                (1, 2): (PlayerEnum.white,PieceEnum.pawn)
            },
                turn=PlayerEnum.white),
            move_from=(1, 2),
            move_to=(1, 4)
        )

    def test_pawn_move_en_passant(self):

        board = prepare_board(config={
                (3, 4): (PlayerEnum.white, PieceEnum.pawn),
                (4, 5): (PlayerEnum.black, PieceEnum.pawn)
                },
            turn=PlayerEnum.white)
        board.last_move_double_file = 4

        check_move_is_allowed(self,
            board,
            after_config_expected={
                (4, 5): (PlayerEnum.white, PieceEnum.pawn)
            },
            move_from=(3, 4),
            move_to=(4, 5)
        )

    def test_pawn_move_illegal_in_check(self):

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.king),
                (0, 7): (PlayerEnum.black, PieceEnum.queen),
                (3, 4): (PlayerEnum.white, PieceEnum.pawn),
                },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
            board,
            move_from=(3, 4),
            move_to=(3, 5)
        )


class WhiteRookMoveTests(unittest.TestCase):

    def test_rook_move_horizontal(self):

        check_move_is_allowed(self,
            prepare_board(config={
                (1, 1): (PlayerEnum.white,PieceEnum.rook)
            },
                turn=PlayerEnum.white
            ),
            after_config_expected={
                (1, 0): (PlayerEnum.white, PieceEnum.rook)
            },
            move_from=(1, 1),
            move_to=(1, 0)
        )

        check_move_is_allowed(self,
            prepare_board(config={
                (1, 0): (PlayerEnum.white,PieceEnum.rook)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (1, 7): (PlayerEnum.white, PieceEnum.rook)
            },
            move_from=(1, 0),
            move_to=(1, 7)
        )

    def test_rook_move_horizontal_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  (1, 0): (PlayerEnum.white, PieceEnum.rook),
                                  (1, 5): (PlayerEnum.black, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white
                              ),
                              move_from=(1, 0),
                              move_to=(1, 7)
                              )


    def test_rook_move_illegal_in_check(self):
        board = prepare_board(config={
            (0, 0): (PlayerEnum.white, PieceEnum.king),
            (0, 7): (PlayerEnum.black, PieceEnum.queen),
            (3, 4): (PlayerEnum.white, PieceEnum.rook),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=(3, 4),
                              move_to=(3, 5)
                              )


class WhiteKnightMoveTests(unittest.TestCase):

    def test_knight_move(self):
        check_move_is_allowed(self,
            prepare_board(config={
                (0, 0): (PlayerEnum.white,PieceEnum.knight)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (2, 1): (PlayerEnum.white, PieceEnum.knight)
            },
            move_from=(0, 0),
            move_to=(2, 1)
        )

        check_move_is_allowed(self,
            prepare_board(config={
                (2, 1): (PlayerEnum.white,PieceEnum.knight)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (3, 3): (PlayerEnum.white, PieceEnum.knight)
            },
            move_from=(2, 1),
            move_to=(3, 3)
        )

    def test_knight_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  (0, 0): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              move_from=(0, 0),
                              move_to=(2, 2)
                              )

    def test_knight_move_illegal_in_check(self):

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.king),
                (0, 7): (PlayerEnum.black, PieceEnum.queen),
                (3, 4): (PlayerEnum.white, PieceEnum.knight),
                },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
            board,
            move_from=(3, 4),
            move_to=(5, 5)
        )

class WhiteBishopMoveTests(unittest.TestCase):

    def test_bishop_move(self):
        check_move_is_allowed(self,
            prepare_board(config={
                (0, 0): (PlayerEnum.white,PieceEnum.bishop)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (4, 4): (PlayerEnum.white, PieceEnum.bishop)
            },
            move_from=(0, 0),
            move_to=(4, 4)
        )

        check_move_is_allowed(self,
            prepare_board(config={
                (4, 4): (PlayerEnum.white,PieceEnum.bishop)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (7, 1): (PlayerEnum.white, PieceEnum.bishop)
            },
            move_from=(4, 4),
            move_to=(7, 1)
        )

    def test_bishop_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  (4, 4): (PlayerEnum.white, PieceEnum.bishop)
                              },turn=PlayerEnum.white),
                              move_from=(4, 4),
                              move_to=(4, 0)
                              )

    def test_bishop_move_illegal_in_check(self):

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.king),
                (0, 7): (PlayerEnum.black, PieceEnum.queen),
                (3, 4): (PlayerEnum.white, PieceEnum.bishop),
                },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
            board,
            move_from=(3, 4),
            move_to=(4, 5)
        )

class WhiteQueenMoveTests(unittest.TestCase):

    def test_queen_move(self):
        check_move_is_allowed(self,
            prepare_board(config={
                (0, 0): (PlayerEnum.white,PieceEnum.queen)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (4, 4): (PlayerEnum.white, PieceEnum.queen)
            },
            move_from=(0, 0),
            move_to=(4, 4)
        )

        check_move_is_allowed(self,
            prepare_board(config={
                (4, 4): (PlayerEnum.white,PieceEnum.queen)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (7, 1): (PlayerEnum.white, PieceEnum.queen)
            },
            move_from=(4, 4),
            move_to=(7, 1)
        )

    def test_queen_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  (4, 4): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              move_from=(4, 4),
                              move_to=(6, 5)
                              )

    def test_queen_move_illegal_in_check(self):

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.king),
                (0, 7): (PlayerEnum.black, PieceEnum.queen),
                (3, 4): (PlayerEnum.white, PieceEnum.queen),
                },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
            board,
            move_from=(3, 4),
            move_to=(4, 5)
        )

class WhiteKingMoveTests(unittest.TestCase):

    def test_king_move(self):
        check_move_is_allowed(self,
            prepare_board(config={
                (0, 0): (PlayerEnum.white,PieceEnum.king)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (0, 1): (PlayerEnum.white, PieceEnum.king)
            },
            move_from=(0, 0),
            move_to=(0, 1)
        )

        check_move_is_allowed(self,
            prepare_board(config={
                (0, 1): (PlayerEnum.white,PieceEnum.king)
            },
                turn=PlayerEnum.white),
            after_config_expected={
                (1, 1): (PlayerEnum.white, PieceEnum.king)
            },
            move_from=(0, 1),
            move_to=(1, 1)
        )

    def test_king_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  (0, 0): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              move_from=(0, 0),
                              move_to=(0, 2)
                              )

    def test_king_move_illegal_in_check(self):
        board = prepare_board(config={
            (0, 0): (PlayerEnum.white, PieceEnum.king),
            (0, 7): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=(0, 0),
                              move_to=(0, 1)
                              )

class WhiteKingQueenSideCastlingTests(unittest.TestCase):

    def test_king_castling_queen_side(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_allowed(self,
            board,
            after_config_expected={
                (2, 0): (PlayerEnum.white, PieceEnum.rook),
                (1, 0): (PlayerEnum.white, PieceEnum.king)
            },
            move_from=(4, 0),
            move_to=(1, 0)
        )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side )

    def test_king_castling_queen_side_disabled_after_rook_move(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.do_move(Position(0, 0), Position(0, 1))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side )

    def test_king_castling_queen_side_disabled_after_king_move(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.do_move(Position(4, 0), Position(4, 1))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side )

    def test_king_castling_queen_side_illegal_when_threaten(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (4, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

    def test_king_castling_queen_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (3, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (2, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (1, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

    def test_king_castling_queen_side_illegal_when_something_between(self):
        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (1, 0): (PlayerEnum.white, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (2, 0): (PlayerEnum.white, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

        board = prepare_board(config={
                (0, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (3, 0): (PlayerEnum.white, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(1, 0)
        )

class WhiteKingKingSideCastlingTests(unittest.TestCase):

    def test_king_castling_king_side(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_allowed(self,
            board,
            after_config_expected={
                (5, 0): (PlayerEnum.white, PieceEnum.rook),
                (6, 0): (PlayerEnum.white, PieceEnum.king)
            },
            move_from=(4, 0),
            move_to=(6, 0)
        )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side )

    def test_king_castling_king_side_disabled_after_rook_move(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.do_move(Position(7, 0), Position(7, 1))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side )

    def test_king_castling_king_side_disabled_after_king_move(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king)
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.do_move(Position(4, 0), Position(4, 1))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side )

    def test_king_castling_king_side_illegal_when_threaten(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (4, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(6, 0)
        )

    def test_king_castling_king_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (5, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(6, 0)
        )

        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (6, 7): (PlayerEnum.black, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(6, 0)
        )

    def test_king_castling_king_side_illegal_when_something_between(self):
        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white, PieceEnum.king),
                (6, 0): (PlayerEnum.white, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(6, 0)
        )

        board = prepare_board(config={
                (7, 0): (PlayerEnum.white, PieceEnum.rook),
                (4, 0): (PlayerEnum.white,PieceEnum.king),
                (5, 0): (PlayerEnum.white, PieceEnum.queen),
            },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
            board,
            move_from=(4, 0),
            move_to=(6, 0)
        )

class WhiteThreatenTests(unittest.TestCase):

    def test_king_threaten_by_pawn(self):
        board = prepare_board(config={
                (6, 0): (PlayerEnum.white, PieceEnum.king),
                (6, 1): (PlayerEnum.black, PieceEnum.rook),
                (5, 2): (PlayerEnum.black, PieceEnum.pawn),
            },
            turn=PlayerEnum.white)

        legal_moves = board.get_legal_moves(Position(6, 0))
        expected_legal_moves = [
            ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(6, 0),
                                                               Position(5, 0)),
            ChessRulesDefault.ChessRulesDefault.MoveDefinition(Position(6, 0),
                                                               Position(7, 0)),
        ]

        self.assertEqual(expected_legal_moves, legal_moves)



if __name__ == '__main__':
    unittest.main()
