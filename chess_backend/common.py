from enum import Enum

class PieceEnum(Enum):
    king = 'K'
    queen = 'Q'
    rook = 'R'
    bishop = 'B'
    knight = 'N'
    pawn = 'P'

class PlayerEnum(Enum):
    white = 0
    black = 1

class Position:
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__

class IllegalMoveException(Exception):
    pass