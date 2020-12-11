from colorama import Fore, Style, Back, init
from chess_backend.common import PlayerEnum
import os

if 'PYCHARM_HOSTED' not in os.environ:
    init(convert=True)

def draw_board(board):
    ret = ""
    ret += Back.RED + "                                            " + Style.RESET_ALL
    ret += "\n"
    for rank in reversed(range(8)):
        for i in range(3):
            ret += Back.RED
            if i == 1:
                ret += str(rank + 1)+" "
            else:
                ret += "  "
            ret += Style.RESET_ALL
            for file in range(8):
                field_str = "     "
                if board.board[file][rank].piece is not None and i == 1:
                    if board.board[file][rank].player == PlayerEnum.white:
                        color = Fore.MAGENTA
                    else:
                        color = Fore.GREEN

                    field_str = color+"  "+board.board[file][rank].piece.value+"  "

                if (file + rank) % 2 == 1:
                    bgcolor = Back.LIGHTWHITE_EX
                else:
                    bgcolor = Back.BLACK
                ret += bgcolor+field_str+Style.RESET_ALL

            ret += Back.RED
            ret += "  "
            ret += Style.RESET_ALL
            ret += "\n"
    ret += Back.RED + "    a    b    c    d    e    f    g    h    " + Style.RESET_ALL
    print(ret)