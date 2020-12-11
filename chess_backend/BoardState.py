from colorama import Fore, Style
from common import PlayerEnum

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
            for file in range(8):
                if self.board[file][rank].piece is not None:
                    if self.board[file][rank].player == PlayerEnum.white:
                        color = Fore.GREEN
                    else:
                        color = Fore.BLUE
                    ret += color+self.board[file][rank].piece.value+Style.RESET_ALL
                else:
                    ret += " "
            ret += "\n"
        return ret