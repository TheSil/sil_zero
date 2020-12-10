import unittest
from common import Position, PlayerEnum, PieceEnum, IllegalMoveException
import ChessRulesDefault

class SetupTests(unittest.TestCase):

    def test_setup(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.setup_board()
        self.assertEqual(None, rules.last_move_double_file)
        self.assertEqual(True, rules.specific[PlayerEnum.white].can_castle_queen_side)
        self.assertEqual(True, rules.specific[PlayerEnum.white].can_castle_king_side)
        self.assertEqual(True, rules.specific[PlayerEnum.black].can_castle_queen_side)
        self.assertEqual(True, rules.specific[PlayerEnum.black].can_castle_king_side)

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

class WhitePawnLegalTests(unittest.TestCase):

    def test_pawn_legal_moves_out_of_turn(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][1].player = PlayerEnum.white
        rules.state.board[1][1].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.black
        legal_moves = rules.get_legal_moves(Position(1, 1))
        self.assertEqual(0, len(legal_moves))

    def test_pawn_legal_moves(self):
        rules = ChessRulesDefault.ChessRulesDefault()

        rules.state.board[1][1].player = PlayerEnum.white
        rules.state.board[1][1].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        legal_moves = rules.get_legal_moves(Position(1, 1))
        self.assertEqual(2, len(legal_moves))
        expected_legal_moves = [
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(1, 1),
                                                            Position(1, 2)),
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(1, 1),
                                                            Position(1, 3)),
        ]
        self.assertEqual(expected_legal_moves, legal_moves)

        rules.state.board[3][3].player = PlayerEnum.white
        rules.state.board[3][3].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        legal_moves = rules.get_legal_moves(Position(3, 3))
        self.assertEqual(1, len(legal_moves))
        expected_legal_moves = [
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(3, 3),
                                                            Position(3, 4)),
        ]
        self.assertEqual(expected_legal_moves, legal_moves)

        rules.state.board[3][4].player = PlayerEnum.black
        rules.state.board[3][4].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        legal_moves = rules.get_legal_moves(Position(3, 3))
        self.assertEqual(0, len(legal_moves))

        rules.state.board[4][4].player = PlayerEnum.black
        rules.state.board[4][4].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        legal_moves = rules.get_legal_moves(Position(3, 3))
        self.assertEqual(1, len(legal_moves))
        expected_legal_moves = [
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(3, 3),
                                                            Position(4, 4)),
        ]
        self.assertEqual(expected_legal_moves, legal_moves)

    def test_pawn_legal_en_passant(self):
        rules = ChessRulesDefault.ChessRulesDefault()

        rules.state.board[3][4].player = PlayerEnum.white
        rules.state.board[3][4].piece = PieceEnum.pawn
        rules.state.board[4][4].player = PlayerEnum.black
        rules.state.board[4][4].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        rules.last_move_double_file = 4

        legal_moves = rules.get_legal_moves(Position(3, 4))
        self.assertEqual(2, len(legal_moves))
        expected_legal_moves = [
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(3, 4),
                                                            Position(3, 5)),
            ChessRulesDefault.ChessRulesDefault.MoveDetails(Position(3, 4),
                                                            Position(4, 5)),
        ]
        self.assertEqual(expected_legal_moves, legal_moves)

class WhitePawnMoveTests(unittest.TestCase):

    def test_pawn_move_single(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][1].player = PlayerEnum.white
        rules.state.board[1][1].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        rules.do_move(Position(1, 1),
                      Position(1, 2))

        self.assertEqual(None, rules.state.board[1][1].player)
        self.assertEqual(None, rules.state.board[1][1].piece)
        self.assertEqual(PlayerEnum.white, rules.state.board[1][2].player)
        self.assertEqual(PieceEnum.pawn, rules.state.board[1][2].piece)
        self.assertEqual(PlayerEnum.black, rules.state.turn)

    def test_pawn_move_double(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][1].player = PlayerEnum.white
        rules.state.board[1][1].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        rules.do_move(Position(1, 1),
                      Position(1, 3))

        self.assertEqual(None, rules.state.board[1][1].player)
        self.assertEqual(None, rules.state.board[1][1].piece)
        self.assertEqual(None, rules.state.board[1][2].player)
        self.assertEqual(None, rules.state.board[1][2].piece)
        self.assertEqual(PlayerEnum.white, rules.state.board[1][3].player)
        self.assertEqual(PieceEnum.pawn, rules.state.board[1][3].piece)
        self.assertEqual(PlayerEnum.black, rules.state.turn)

    def test_pawn_move_double_not_allowed(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][2].player = PlayerEnum.white
        rules.state.board[1][2].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white

        with self.assertRaises(IllegalMoveException):
            rules.do_move(Position(1, 2),
                          Position(1, 4))

    def test_pawn_move_en_passant(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[3][4].player = PlayerEnum.white
        rules.state.board[3][4].piece = PieceEnum.pawn
        rules.state.board[4][4].player = PlayerEnum.black
        rules.state.board[4][4].piece = PieceEnum.pawn
        rules.state.turn = PlayerEnum.white
        rules.last_move_double_file = 4

        rules.do_move(Position(3, 4),
                      Position(4, 5))

        self.assertEqual(None, rules.state.board[3][4].player)
        self.assertEqual(None, rules.state.board[3][4].piece)
        self.assertEqual(PlayerEnum.white, rules.state.board[4][5].player)
        self.assertEqual(PieceEnum.pawn, rules.state.board[4][5].piece)
        self.assertEqual(None, rules.state.board[4][4].player)
        self.assertEqual(None, rules.state.board[4][4].piece)
        self.assertEqual(PlayerEnum.black, rules.state.turn)


class WhiteRookMoveTests(unittest.TestCase):

    def test_rook_move_horizontal(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][1].player = PlayerEnum.white
        rules.state.board[1][1].piece = PieceEnum.rook
        rules.state.turn = PlayerEnum.white
        rules.do_move(Position(1, 1),
                      Position(1, 0))

        self.assertEqual(None, rules.state.board[1][1].player)
        self.assertEqual(None, rules.state.board[1][1].piece)
        self.assertEqual(PlayerEnum.white, rules.state.board[1][0].player)
        self.assertEqual(PieceEnum.rook, rules.state.board[1][0].piece)
        self.assertEqual(PlayerEnum.black, rules.state.turn)

        rules.state.turn = PlayerEnum.white
        rules.do_move(Position(1, 0),
                      Position(1, 7))
        self.assertEqual(None, rules.state.board[1][0].player)
        self.assertEqual(None, rules.state.board[1][0].piece)
        self.assertEqual(PlayerEnum.white, rules.state.board[1][7].player)
        self.assertEqual(PieceEnum.rook, rules.state.board[1][7].piece)
        self.assertEqual(PlayerEnum.black, rules.state.turn)

    def test_rook_move_horizontal_blocked(self):
        rules = ChessRulesDefault.ChessRulesDefault()
        rules.state.board[1][0].player = PlayerEnum.white
        rules.state.board[1][0].piece = PieceEnum.rook
        rules.state.turn = PlayerEnum.white

        rules.state.board[1][5].player = PlayerEnum.black
        rules.state.board[1][5].piece = PieceEnum.rook

        with self.assertRaises(IllegalMoveException):
            rules.do_move(Position(1, 0),
                          Position(1, 7))




if __name__ == '__main__':
    unittest.main()
