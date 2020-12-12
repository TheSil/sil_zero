import unittest
from chess_backend.common import Position, PlayerEnum, PieceEnum, IllegalMoveException
from chess_backend.ChessRulesDefault import ChessRulesDefault, ActionMove


def prepare_board(config, turn):
    rules = ChessRulesDefault()
    for pos, (player, piece) in config.items():
        rules.state.board[pos.file][pos.rank].player = player
        rules.state.board[pos.file][pos.rank].piece = piece
    rules.state.turn = turn
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
                                  Position.from_str("b2"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("b3"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                              move_from=Position.from_str("b2"),
                              move_to=Position.from_str("b3")
                              )

    def test_pawn_move_double(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("b2"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("b4"): (PlayerEnum.white, PieceEnum.pawn)
                              },

                              move_from=Position.from_str("b2"),
                              move_to=Position.from_str("b4"),
                              is_double_move=True,
                              )

    def test_pawn_move_double_not_allowed(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("b3"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                                  turn=PlayerEnum.white),
                              move_from=Position.from_str("b3"),
                              move_to=Position.from_str("b5")
                              )

        board = prepare_board(config={
            Position.from_str("a6"): (PlayerEnum.white, PieceEnum.pawn),
            Position.from_str("b5"): (PlayerEnum.black, PieceEnum.pawn)
            },
            turn=PlayerEnum.white)
        board.last_move_double_file = 1
        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("a6"),
                              move_to=Position.from_str("b7")
                              )


    def test_pawn_move_en_passant(self):
        board = prepare_board(config={
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.pawn),
            Position.from_str("e6"): (PlayerEnum.black, PieceEnum.pawn)
        },
            turn=PlayerEnum.white)
        board.last_move_double_file = 4

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  Position.from_str("e6"): (PlayerEnum.white, PieceEnum.pawn)
                              },
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("e6"),
                              to_take=Position.from_str("e6")
                              )

    def test_pawn_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("d6")
                              )


class WhitePawnPromotionTests(unittest.TestCase):

    def test_promote_pawn(self):

        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                Position.from_str("a7"): (PlayerEnum.white, PieceEnum.pawn)
            },
                turn=PlayerEnum.white
            )

            board.move(ActionMove(pos_from=Position.from_str("a7"),
                       pos_to=Position.from_str("a8"),
                       promote_piece=promoted_piece))

            self.assertEqual(None, board.state.board[0][6].piece)
            self.assertEqual(None, board.state.board[0][6].player)
            self.assertEqual(promoted_piece, board.state.board[0][7].piece)
            self.assertEqual(PlayerEnum.white, board.state.board[0][7].player)

    def test_promote_blocked_illegal(self):
        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                Position.from_str("a7"): (PlayerEnum.white, PieceEnum.pawn),
                Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen)
            },
                turn=PlayerEnum.white
            )

            with self.assertRaises(IllegalMoveException):
                board.move(ActionMove(pos_from=Position.from_str("a7"),
                           pos_to=Position.from_str("a8"),
                           promote_piece=promoted_piece))

    def test_promote_causing_check_illegal(self):
        for promoted_piece in (PieceEnum.queen, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook):
            board = prepare_board(config={
                Position.from_str("e7"): (PlayerEnum.white, PieceEnum.pawn),
                Position.from_str("h7"): (PlayerEnum.white, PieceEnum.king),
                Position.from_str("a7"): (PlayerEnum.black, PieceEnum.queen),
            },
                turn=PlayerEnum.white
            )

            with self.assertRaises(IllegalMoveException):
                board.move(ActionMove(pos_from=Position.from_str("e7"),
                           pos_to=Position.from_str("e8"),
                           promote_piece=promoted_piece))

    def test_promote_by_taking(self):
        board = prepare_board(config={
            Position.from_str("h7"): (PlayerEnum.white, PieceEnum.pawn),
            Position.from_str("g8"): (PlayerEnum.black, PieceEnum.knight),
            Position.from_str("h8"): (PlayerEnum.black, PieceEnum.rook)
        },
            turn=PlayerEnum.white
        )

        legal_moves = board.get_legal_moves(Position.from_str("h7"))
        expected_legal_moves = [
            ActionMove(Position.from_str("h7"), Position.from_str("g8"),
                       to_take=Position.from_str("g8"), promote_piece=PieceEnum.bishop),
            ActionMove(Position.from_str("h7"), Position.from_str("g8"),
                       to_take=Position.from_str("g8"), promote_piece=PieceEnum.knight),
            ActionMove(Position.from_str("h7"), Position.from_str("g8"),
                       to_take=Position.from_str("g8"), promote_piece=PieceEnum.rook),
            ActionMove(Position.from_str("h7"), Position.from_str("g8"),
                       to_take=Position.from_str("g8"), promote_piece=PieceEnum.queen),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)



class WhiteRookMoveTests(unittest.TestCase):

    def test_rook_move_horizontal(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("b2"): (PlayerEnum.white, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white
                              ),
                              after_config_expected={
                                  Position.from_str("b1"): (PlayerEnum.white, PieceEnum.rook)
                              },
                              move_from=Position.from_str("b2"),
                              move_to=Position.from_str("b1")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("b1"): (PlayerEnum.white, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("b8"): (PlayerEnum.white, PieceEnum.rook)
                              },
                              move_from=Position.from_str("b1"),
                              move_to=Position.from_str("b8")
                              )

    def test_rook_move_horizontal_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("b1"): (PlayerEnum.white, PieceEnum.rook),
                                  Position.from_str("b6"): (PlayerEnum.black, PieceEnum.rook)
                              },
                                  turn=PlayerEnum.white
                              ),
                              move_from=Position.from_str("b1"),
                              move_to=Position.from_str("b8")
                              )

    def test_rook_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.rook),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("d6")
                              )


class WhiteKnightMoveTests(unittest.TestCase):

    def test_knight_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("c2"): (PlayerEnum.white, PieceEnum.knight)
                              },
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("c2")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("c2"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("d4"): (PlayerEnum.white, PieceEnum.knight)
                              },
                              move_from=Position.from_str("c2"),
                              move_to=Position.from_str("d4")
                              )

    def test_knight_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.knight)
                              },
                                  turn=PlayerEnum.white),
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("c3")
                              )

    def test_knight_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.knight),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("f6")
                              )


class WhiteBishopMoveTests(unittest.TestCase):

    def test_bishop_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("e5")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("h2"): (PlayerEnum.white, PieceEnum.bishop)
                              },
                              move_from=Position.from_str("e5"),
                              move_to=Position.from_str("h2")
                              )

    def test_bishop_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.bishop)
                              }, turn=PlayerEnum.white),
                              move_from=Position.from_str("e5"),
                              move_to=Position.from_str("e1")
                              )

    def test_bishop_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.bishop),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("e6")
                              )


class WhiteQueenMoveTests(unittest.TestCase):

    def test_queen_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("e5")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("h2"): (PlayerEnum.white, PieceEnum.queen)
                              },
                              move_from=Position.from_str("e5"),
                              move_to=Position.from_str("h2")
                              )

    def test_queen_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("e5"): (PlayerEnum.white, PieceEnum.queen)
                              },
                                  turn=PlayerEnum.white),
                              move_from=Position.from_str("e5"),
                              move_to=Position.from_str("g6")
                              )

    def test_queen_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
            Position.from_str("d5"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("d5"),
                              move_to=Position.from_str("e6")
                              )


class WhiteKingMoveTests(unittest.TestCase):

    def test_king_move(self):
        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("a2"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("a2")
                              )

        check_move_is_allowed(self,
                              prepare_board(config={
                                  Position.from_str("a2"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              after_config_expected={
                                  Position.from_str("b2"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=Position.from_str("a2"),
                              move_to=Position.from_str("b2")
                              )

    def test_king_move_illegal(self):
        check_move_is_illegal(self,
                              prepare_board(config={
                                  Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king)
                              },
                                  turn=PlayerEnum.white),
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("a3")
                              )

    def test_king_move_illegal_in_check(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("a1"),
                              move_to=Position.from_str("a2")
                              )


class WhiteKingQueenSideCastlingTests(unittest.TestCase):

    def test_king_castling_queen_side(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  Position.from_str("c1"): (PlayerEnum.white, PieceEnum.rook),
                                  Position.from_str("b1"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1"),
                              is_queen_side_castle=True,
                              to_move=[(Position.from_str("e1"),Position.from_str("b1")),
                                       (Position.from_str("a1"),Position.from_str("c1"))
                              ]
                              )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_unaffected(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a2"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        board.move(ActionMove(Position.from_str("a2"), Position.from_str("a3")))

        self.assertEqual(True, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_disabled_after_rook_move(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.move(ActionMove(Position.from_str("a1"), Position.from_str("a2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_disabled_after_king_move(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True
        board.move(ActionMove(Position.from_str("e1"), Position.from_str("e2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_queen_side)

    def test_king_castling_queen_side_illegal_when_threaten(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("e8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

    def test_king_castling_queen_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("d8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("c8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("b8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

    def test_king_castling_queen_side_illegal_when_something_between(self):
        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("b1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("c1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )

        board = prepare_board(config={
            Position.from_str("a1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("d1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_queen_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("b1")
                              )


class WhiteKingKingSideCastlingTests(unittest.TestCase):

    def test_king_castling_king_side(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_allowed(self,
                              board,
                              after_config_expected={
                                  Position.from_str("f1"): (PlayerEnum.white, PieceEnum.rook),
                                  Position.from_str("g1"): (PlayerEnum.white, PieceEnum.king)
                              },
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1"),
                              is_king_side_castle=True,
                              to_move=[
                                  (Position.from_str("e1"), Position.from_str("g1")),
                                  (Position.from_str("h1"), Position.from_str("f1")),
                              ]
                              )

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_unaffected(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("a2"): (PlayerEnum.white, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        board.move(ActionMove(Position.from_str("a2"), Position.from_str("a3")))

        self.assertEqual(True, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_disabled_after_rook_move(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.move(ActionMove(Position.from_str("h1"), Position.from_str("h2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_disabled_after_king_move(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king)
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True
        board.move(ActionMove(Position.from_str("e1"), Position.from_str("e2")))

        self.assertEqual(False, board.specific[PlayerEnum.white].can_castle_king_side)

    def test_king_castling_king_side_illegal_when_threaten(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("e8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1")
                              )

    def test_king_castling_king_side_illegal_when_threaten_between(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("f8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1")
                              )

        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("g8"): (PlayerEnum.black, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1")
                              )

    def test_king_castling_king_side_illegal_when_something_between(self):
        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("g1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1")
                              )

        board = prepare_board(config={
            Position.from_str("h1"): (PlayerEnum.white, PieceEnum.rook),
            Position.from_str("e1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("f1"): (PlayerEnum.white, PieceEnum.queen),
        },
            turn=PlayerEnum.white)
        board.specific[PlayerEnum.white].can_castle_king_side = True

        check_move_is_illegal(self,
                              board,
                              move_from=Position.from_str("e1"),
                              move_to=Position.from_str("g1")
                              )


class ThreatenTests(unittest.TestCase):

    def test_king_threaten_by_pawn(self):
        board = prepare_board(config={
            Position.from_str("g1"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("g2"): (PlayerEnum.black, PieceEnum.rook),
            Position.from_str("f3"): (PlayerEnum.black, PieceEnum.pawn),
        },
            turn=PlayerEnum.white)

        legal_moves = board.get_legal_moves(Position.from_str("g1"))
        expected_legal_moves = [
            ActionMove(Position.from_str("g1"), Position.from_str("f1")),
            ActionMove(Position.from_str("g1"), Position.from_str("h1")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

    def test_king_threaten_by_bishop(self):
        board = prepare_board(config={
            Position.from_str("c7"): (PlayerEnum.black, PieceEnum.king),
            Position.from_str("e7"): (PlayerEnum.white, PieceEnum.bishop)
        },
            turn=PlayerEnum.black)

        legal_moves = board.get_legal_moves(Position.from_str("c7"))
        expected_legal_moves = [
            ActionMove(Position.from_str("c7"), Position.from_str("c8")),
            ActionMove(Position.from_str("c7"), Position.from_str("c6")),
            ActionMove(Position.from_str("c7"), Position.from_str("b6")),
            ActionMove(Position.from_str("c7"), Position.from_str("b7")),
            ActionMove(Position.from_str("c7"), Position.from_str("b8")),
            ActionMove(Position.from_str("c7"), Position.from_str("d7")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

    def test_king_threaten_by_king(self):
        board = prepare_board(config={
            Position.from_str("d8"): (PlayerEnum.white, PieceEnum.king),
            Position.from_str("d6"): (PlayerEnum.black, PieceEnum.king)
        },
            turn=PlayerEnum.white)

        legal_moves = board.get_legal_moves(Position.from_str("d8"))
        expected_legal_moves = [
            ActionMove(Position.from_str("d8"), Position.from_str("c8")),
            ActionMove(Position.from_str("d8"), Position.from_str("e8")),
        ]

        self.assertCountEqual(expected_legal_moves, legal_moves)

class ScratchTests(unittest.TestCase):

    def test_scratch(self):
        pass


if __name__ == '__main__':
    unittest.main()
