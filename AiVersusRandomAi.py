from agents.AiAgent import AiAgent
from agents.RandomAiAgent import RandomAiAgent
from chess_backend.GameState import GameState
from chess_backend.Session import Session
from ui.console import ConsoleUi


class DummyNetwork:

    def __call__(self, game_state):
        count = len(game_state.legal_moves)
        policy = [1/count] * count
        value = 0
        return policy, value


def main(do_print=True):
    game = GameState()
    game.start_new()

    # setup custom position
    '''
    game.board.clear_board()
    custom_white = {POS("a6"): PieceEnum.pawn,
                    POS("h1"): PieceEnum.king}
    custom_black = {POS("e1"): PieceEnum.knight,
                    POS("h2"): PieceEnum.pawn,
                    POS("h3"): PieceEnum.king}
    for pos, piece in custom_white.items():
        game.board.board[pos.file][pos.rank].player = PlayerEnum.white
        game.board.board[pos.file][pos.rank].piece = piece
    for pos, piece in custom_black.items():
        game.board.board[pos.file][pos.rank].player = PlayerEnum.black
        game.board.board[pos.file][pos.rank].piece = piece
    game.specific[PlayerEnum.white].can_castle_queen_side = False
    game.specific[PlayerEnum.white].can_castle_king_side = False
    game.specific[PlayerEnum.black].can_castle_queen_side = False
    game.specific[PlayerEnum.black].can_castle_king_side = False
    game.board.turn = PlayerEnum.black
    game.update_legal_moves()
    '''

    net = DummyNetwork()
    white = RandomAiAgent()
    black = AiAgent(net)
    ui = ConsoleUi()

    session = Session(game, white, black)
    session.before_move(lambda : ui.draw_board(game.board))
    session.play()

    if do_print:
        if game.state == game.WHITE_WON:
            print(f"Game finished, white won")
        elif game.state == game.BLACK_WON:
            print(f"Game finished, black won")
        elif game.state == game.STALEMATE:
            print(f"Game finished, stalemate")
        elif game.state == game.DRAW:
            print(f"Game finished, draw")


if __name__ == '__main__':
    main()

    # import cProfile
    # cProfile.run('main(do_print=False)', sort="tottime")
