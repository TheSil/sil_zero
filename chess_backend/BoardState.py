class PositionState:
    def __init__(self, piece=None, player=None):
        self.piece = piece
        self.player = player

class BoardState:
    def __init__(self):
        self.turn = None
        self.placed_pieces = []
        self.board = [[PositionState() for i in range(8)] for i in range(8)]

    def clear_board(self):
        pass

    def place_piece(self, piece, position, player):
        self.board[position.file][position.rank].piece = piece
        self.board[position.file][position.rank].player = player

    def __str__(self):
        ret = ""
        for rank in reversed(range(8)):
            for file in range(8):
                if self.board[file][rank].piece is not None:
                    ret += self.board[file][rank].piece.value
                else:
                    ret += " "
            ret += "\n"
        return ret