from colorama import Fore, Style, Back, init
from chess_backend.common import PlayerEnum
import os

if 'PYCHARM_HOSTED' not in os.environ:
    init(convert=True)

class PositionState:
    def __init__(self, piece=None, player=None):
        self.piece = piece
        self.player = player

    def __str__(self):
        return f"{self.piece.name} ({self.player.name})"

class BoardState:
    def __init__(self):
        self.clear_board()

    def clear_board(self):
        self.turn = None
        self.board = [[PositionState() for i in range(8)] for i in range(8)]

    def __str__(self):
        ret = ""
        for rank in reversed(range(8)):
            ret += str(rank + 1)
            for file in range(8):
                field_str = " "
                if self.board[file][rank].piece is not None:
                    if self.board[file][rank].player == PlayerEnum.white:
                        color = Fore.MAGENTA
                    else:
                        color = Fore.GREEN

                    field_str = color+self.board[file][rank].piece.value

                if (file + rank) % 2 == 1:
                    bgcolor = Back.LIGHTWHITE_EX
                else:
                    bgcolor = Back.BLACK
                ret += bgcolor+field_str+Style.RESET_ALL
            ret += "\n"
        ret += " abcdefgh"
        return ret