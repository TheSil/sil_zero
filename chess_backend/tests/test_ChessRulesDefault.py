import unittest
from chess_backend.common import Position, POS, PlayerEnum, PieceEnum, IllegalMoveException
from chess_backend.ChessRulesDefault import ChessRulesDefault, ActionMove


def prepare_board(config, turn):
    rules = ChessRulesDefault()
    for pos, (player, piece) in config.items():
        rules.state.board[pos.file][pos.rank].player = player
        rules.state.board[pos.file][pos.rank].piece = piece
    rules.state.turn = turn
    rules.update_legal_moves()
    return rules


def check_move_is_allowed(self,
                          board,
                          after_config_expected,
                          move_from,
                          move_to,
                          **kwargs):
    rules = board

    rules.move(ActionMove(move_from, move_to, **kwargs))

    for file in range(8):
        for rank in range(8):
            player, piece = None, None
            pos = Position(file, rank)
            if pos in after_config_expected:
                player, piece = after_config_expected[pos]
            self.assertEqual(player, rules.state.board[file][rank].player)
            self.assertEqual(piece, rules.state.board[file][rank].piece)


def check_move_is_illegal(self,
                          board,
                          move_from,
                          move_to):
    rules = board

    with self.assertRaises(IllegalMoveException):
        rules.move(ActionMove(move_from, move_to))


class SetupTests(unittest.TestCase):

    def test_setup(self):
        rules = ChessRulesDefault()
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

        for rank in (1, 6):
            for file in range(8):
                self.assertEqual(PieceEnum.pawn, rules.state.board[file][rank].piece)

        for rank in (0, 7):
            self.assertEqual(PieceEnum.rook, rules.state.board[0][rank].piece)
            self.assertEqual(PieceEnum.knight, rules.state.board[1][rank].piece)
            self.assertEqual(PieceEnum.bishop, rules.state.board[2][rank].piece)
            self.assertEqual(PieceEnum.queen, rules.state.board[3][rank].piece)
            self.assertEqual(PieceEnum.king, rules.state.board[4][rank].piece)
            self.assertEqual(PieceEnum.bishop, rules.state.board[5][rank].piece)
            self.assertEqual(PieceEnum.knight, rules.state.board[6][rank].piece)
            self.assertEqual(PieceEnum.rook, rules.state.board[7][rank].piece)


class WhitePawnMoveTests(unittest.TestCase):

    def test_pawn_move_single(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("b2"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("b3"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                              move_from=POS("b2"),
                              move_to=POS("b3")
                              )

    def test_pawn_move_double(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("b2"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("b4"): (PlayerEnum.white, PieceEnum.pawn)
                              },

                              move_from=POS("b2"),
                              move_to=POS("b4"),
                              is_double_move=True,
                              )

    def test_pawn_move_double_not_allowed(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("b3"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              move_from=POS("b3"),
                              move_to=POS("b5")
                              )

        board = prepare_board(config={
            POS("a6"): (PlayerEnum.white, PieceEnum.pawn),
            POS("b5"): (PlayerEnum.black, PieceEnum.pawn)
            },
            turn=PlayerEnum.white)
        board.last_move_double_file = 1
        check_move_is_illegal(self,
                              board,
                              move_from=POS("a6"),
                              move_to=POS("b7")
                              )


    def test_pawn_move_en_passant(self):
        board = prepare_board(config={
            POS("d5"): (PlayerEnum.white, PieceEnum.pawn),
            POS("e6"): (PlayerEnum.black, PieceEnum.pawn)
        },
            turn=PlayerEnum.white)
        board.last_move_double_file = 4

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  POS("e6"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                              move_from=POS("d5"),
                              move_to=POS("e6"),
                              to_take=POS("e6")
                              )

    def test_pawn_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
            POS("d5"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("d5"),
                              move_to=POS("d6")
                              )


class WhitePawnPromotionTests(unittest.TestCase):

    def test_promote_pawn(self):

        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                POS("a7"): (PlayerEnum.white, PieceEnum.pawn)
            },
                turn=PlayerEnum.white
            )

            board.move(ActionMove(pos_from=POS("a7"),
                       pos_to=POS("a8"),
                       promote_piece=promoted_piece))

            self.assertEqual(None, board.state.board[0][6].piece)
            self.assertEqual(None, board.state.board[0][6].player)
            self.assertEqual(promoted_piece, board.state.board[0][7].piece)
            self.assertEqual(PlayerEnum.white, board.state.board[0][7].player)

    def test_promote_blocked_illegal(self):
        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                POS("a7"): (PlayerEnum.white, PieceEnum.pawn),
                POS("a8"): (PlayerEnum.black, PieceEnum.queen)
            },
                turn=PlayerEnum.white
            )

            with self.assertRaises(IllegalMoveException):
                board.move(ActionMove(pos_from=POS("a7"),
                           pos_to=POS("a8"),
                           promote_piece=promoted_piece))

    def test_promote_causing_check_illegal(self):
        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                POS("e7"): (PlayerEnum.white, PieceEnum.pawn),
                POS("h7"): (PlayerEnum.white, PieceEnum.king),
                POS("a7"): (PlayerEnum.black, PieceEnum.queen),
            },
                turn=PlayerEnum.white
            )

            with self.assertRaises(IllegalMoveException):
                board.move(ActionMove(pos_from=POS("e7"),
                           pos_to=POS("e8"),
                           promote_piece=promoted_piece))

    def test_promote_by_taking(self):
        board = prepare_board(config={
            POS("h7"): (PlayerEnum.white, PieceEnum.pawn),
            POS("g8"): (PlayerEnum.black, PieceEnum.knight),
            POS("h8"): (PlayerEnum.black, PieceEnum.rook)
        },
            turn=PlayerEnum.white
        )

        legal_moves = board.get_legal_moves(POS("h7"))
        expected_legal_moves = [
            ActionMove(POS("h7"), POS("g8"),
                       to_take=POS("g8"), promote_piece=PieceEnum.bishop),
            ActionMove(POS("h7"), POS("g8"),
                       to_take=POS("g8"), promote_piece=PieceEnum.knight),
            ActionMove(POS("h7"), POS("g8"),
                       to_take=POS("g8"), promote_piece=PieceEnum.rook),
            ActionMove(POS("h7"), POS("g8"),
                       to_take=POS("g8"), promote_piece=PieceEnum.queen),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)



class WhiteRookMoveTests(unittest.TestCase):

    def test_rook_move_horizontal(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("b2"): (PlayerEnum.white, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white
                              ),
                              after_config_expected={
                                  POS("b1"): (PlayerEnum.white, PieceEnum.rook)
                              },
                              move_from=POS("b2"),
                              move_to=POS("b1")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("b1"): (PlayerEnum.white, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("b8"): (PlayerEnum.white, PieceEnum.rook)
                              },
                              move_from=POS("b1"),
                              move_to=POS("b8")
                              )

    def test_rook_move_horizontal_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("b1"): (PlayerEnum.white, PieceEnum.rook),
                                  POS("b6"): (PlayerEnum.black, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white
                              ),
                              move_from=POS("b1"),
                              move_to=POS("b8")
                              )

    def test_rook_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
            POS("d5"): (PlayerEnum.white, PieceEnum.rook),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("d5"),
                              move_to=POS("d6")
                              )


class WhiteKnightMoveTests(unittest.TestCase):

    def test_knight_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("c2"): (PlayerEnum.white, PieceEnum.knight)
                              },
                              move_from=POS("a1"),
                              move_to=POS("c2")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("c2"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("d4"): (PlayerEnum.white, PieceEnum.knight)
                              },
                              move_from=POS("c2"),
                              move_to=POS("d4")
                              )

    def test_knight_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              move_from=POS("a1"),
                              move_to=POS("c3")
                              )

    def test_knight_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
            POS("d5"): (PlayerEnum.white, PieceEnum.knight),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("d5"),
                              move_to=POS("f6")
                              )


class WhiteBishopMoveTests(unittest.TestCase):

    def test_bishop_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                              move_from=POS("a1"),
                              move_to=POS("e5")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("h2"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                              move_from=POS("e5"),
                              move_to=POS("h2")
                              )

    def test_bishop_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              }, turn=PlayerEnum.white),
                              move_from=POS("e5"),
                              move_to=POS("e1")
                              )

    def test_bishop_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
            POS("d5"): (PlayerEnum.white, PieceEnum.bishop),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("d5"),
                              move_to=POS("e6")
                              )


class WhiteQueenMoveTests(unittest.TestCase):

    def test_queen_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                              move_from=POS("a1"),
                              move_to=POS("e5")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("h2"): (PlayerEnum.white, PieceEnum.queen)
                              },
                              move_from=POS("e5"),
                              move_to=POS("h2")
                              )

    def test_queen_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              move_from=POS("e5"),
                              move_to=POS("g6")
                              )

    def test_queen_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
            POS("d5"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("d5"),
                              move_to=POS("e6")
                              )


class WhiteKingMoveTests(unittest.TestCase):

    def test_king_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("a2"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=POS("a1"),
                              move_to=POS("a2")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  POS("a2"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  POS("b2"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=POS("a2"),
                              move_to=POS("b2")
                              )

    def test_king_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  POS("a1"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              move_from=POS("a1"),
                              move_to=POS("a3")
                              )

    def test_king_move_illegal_in_check(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.king),
            POS("a8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=POS("a1"),
                              move_to=POS("a2")
                              )


class WhiteKingQueenSideCastlingTests(unittest.TestCase):

    def test_king_castling_queen_side(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.update_legal_moves()

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  POS("c1"): (PlayerEnum.white, PieceEnum.rook),
                                  POS("b1"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=POS("e1"),
                              move_to=POS("b1"),
                              is_queen_side_castle=True,
                              to_move=[(POS("e1"),POS("b1")),
                                       (POS("a1"),POS("c1"))
                              ]
                              )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_unaffected(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("a2"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        board.move(ActionMove(POS("a2"), POS("a3")))

        self.assertEqual(True, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_disabled_after_rook_move(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.move(ActionMove(POS("a1"), POS("a2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_disabled_after_king_move(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.move(ActionMove(POS("e1"), POS("e2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_illegal_when_threaten(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("e8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

    def test_king_castling_queen_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("d8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("c8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("b8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

    def test_king_castling_queen_side_illegal_when_something_between(self):
        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("b1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("c1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )

        board = prepare_board(config={
            POS("a1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("d1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("b1")
                              )


class WhiteKingKingSideCastlingTests(unittest.TestCase):

    def test_king_castling_king_side(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.update_legal_moves()

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  POS("f1"): (PlayerEnum.white, PieceEnum.rook),
                                  POS("g1"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=POS("e1"),
                              move_to=POS("g1"),
                              is_king_side_castle=True,
                              to_move=[
                                  (POS("e1"), POS("g1")),
                                  (POS("h1"), POS("f1")),
                              ]
                              )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_unaffected(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("a2"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        board.move(ActionMove(POS("a2"), POS("a3")))

        self.assertEqual(True, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_disabled_after_rook_move(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.move(ActionMove(POS("h1"), POS("h2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_disabled_after_king_move(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.move(ActionMove(POS("e1"), POS("e2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_illegal_when_threaten(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("e8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("g1")
                              )

    def test_king_castling_king_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("f8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("g1")
                              )

        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("g8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("g1")
                              )

    def test_king_castling_king_side_illegal_when_something_between(self):
        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("g1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("g1")
                              )

        board = prepare_board(config={
            POS("h1"): (PlayerEnum.white, PieceEnum.rook),
            POS("e1"): (PlayerEnum.white, PieceEnum.king),
            POS("f1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=POS("e1"),
                              move_to=POS("g1")
                              )


class ThreatenTests(unittest.TestCase):

    def test_king_threaten_by_pawn(self):
        board = prepare_board(config={
            POS("g1"): (PlayerEnum.white, PieceEnum.king),
            POS("g2"): (PlayerEnum.black, PieceEnum.rook),
            POS("f3"): (PlayerEnum.black, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)

        legal_moves = board.get_legal_moves(POS("g1"))
        expected_legal_moves = [
            ActionMove(POS("g1"), POS("f1")),
            ActionMove(POS("g1"), POS("h1")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

    def test_king_threaten_by_bishop(self):
        board = prepare_board(config={
            POS("c7"): (PlayerEnum.black, PieceEnum.king),
            POS("e7"): (PlayerEnum.white, PieceEnum.bishop)
        },
            turn=PlayerEnum.black)

        legal_moves = board.get_legal_moves(POS("c7"))
        expected_legal_moves = [
            ActionMove(POS("c7"), POS("c8")),
            ActionMove(POS("c7"), POS("c6")),
            ActionMove(POS("c7"), POS("b6")),
            ActionMove(POS("c7"), POS("b7")),
            ActionMove(POS("c7"), POS("b8")),
            ActionMove(POS("c7"), POS("d7")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

    def test_king_threaten_by_king(self):
        board = prepare_board(config={
            POS("d8"): (PlayerEnum.white, PieceEnum.king),
            POS("d6"): (PlayerEnum.black, PieceEnum.king)
        },
            turn=PlayerEnum.white)

        legal_moves = board.get_legal_moves(POS("d8"))
        expected_legal_moves = [
            ActionMove(POS("d8"), POS("c8")),
            ActionMove(POS("d8"), POS("e8")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

class ScratchTests(unittest.TestCase):

    def test_scratch(self):
        pass


if __name__ == '__main__':
    unittest.main()
