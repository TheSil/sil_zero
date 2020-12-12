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

    def __str__(self):
        return chr(ord('a')+self.file) + str(self.rank + 1)

    def __hash__(self):
        return hash((self.file, self.rank))

    @classmethod
    def from_str(cls, text_coords):
        return cls(ord(text_coords[0]) - ord('a'), ord(text_coords[1]) - ord('1'))

def POS(text_coords):
    return Position(text_coords)

class IllegalMoveException(Exception):
    pass