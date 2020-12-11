import unittest
from chess_backend.common import PlayerEnum, PieceEnum
from chess_backend import BoardState

class BoardStateTests(unittest.TestCase):

    def test_clean(self):
        state = BoardState.BoardState()
        for file in range(8):
            for rank in range(8):
                state.board[file][rank].piece = PieceEnum.pawn
                state.board[file][rank].player = PlayerEnum.white

        state.clear_board()

        for file in range(8):
            for rank in range(8):
                self.assertEqual(None, state.board[file][rank].piece)
                self.assertEqual(None, state.board[file][rank].player)


if __name__ == '__main__':
    unittest.main()
