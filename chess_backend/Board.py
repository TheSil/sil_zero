class PositionState:
    def __init__(self, piece=None, player=None):
        self.piece = piece
        self.player = player

    def __str__(self):
        return f"{self.piece.name} ({self.player.name})"


class Board:
    def __init__(self):
        self.clear_board()

    def clear_board(self):
        self.turn = None
        self.board = [[PositionState() for _ in range(8)] for _ in range(8)]
