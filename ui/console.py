from colorama import Fore, Style, Back, init
from chess_backend.common import PlayerEnum
import os

class ConsoleUi:

    def __init__(self):
        if 'PYCHARM_HOSTED' not in os.environ:
            init(convert=True)

    def draw_board(self, board, colors=True):
        os.system('cls')
        ret = ""
        space = " "

        if colors:
            bg_board_color = Back.RED
            style_end = Style.RESET_ALL
            black_piece_color = Fore.GREEN
            white_piece_color = Fore.MAGENTA
            black_bgcolor = Back.BLACK
            white_bgcolor = Back.LIGHTWHITE_EX
        else:
            bg_board_color = ""
            style_end = ""
            black_piece_color = ""
            white_piece_color = ""
            black_bgcolor = ""
            white_bgcolor = ""

        ret += bg_board_color
        ret += 44*space
        ret += style_end
        ret += "\n"
        for rank in reversed(range(8)):
            for i in range(3):
                ret += bg_board_color
                if i == 1:
                    ret += str(rank + 1) + space
                else:
                    ret += 2*space
                ret += style_end
                for file in range(8):
                    field_str = 5*space
                    if board.board[file][rank].piece is not None and i == 1:
                        field_str = ""
                        if board.board[file][rank].player == PlayerEnum.white:
                            color = white_piece_color
                        else:
                            color = black_piece_color

                        field_str += color
                        field_str += 2*space
                        field_str += board.board[file][rank].piece.value
                        field_str += 2*space

                    if (file + rank) % 2 == 1:
                        bgcolor = white_bgcolor
                    else:
                        bgcolor = black_bgcolor

                    ret += bgcolor
                    ret += field_str
                    ret += style_end

                ret += bg_board_color
                ret += 2*space
                ret += style_end
                ret += "\n"
        ret += bg_board_color
        ret += 2*space
        for c in ("a", "b", "c", "d", "e", "f", "g", "h"):
            ret += 2*space + c + 2*space
        ret += 2*space
        ret += style_end
        print(ret)
