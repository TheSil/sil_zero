

class Session:
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1
        self.player2 = player2
        self.history = []
        self.stats = []
        self.on_move_before = []
        self.on_move_after = []

    def play(self):
        while self.game.is_running():
            for callback in self.on_move_before:
                callback()
            player = self.player1 if self.turn() % 2 == 0 else self.player2
            action, stats = player.select_action(self.game)
            self.history.append((self.game.clone(), action))
            self.stats.append(stats)
            self.game.apply(action)
            for callback in self.on_move_after:
                callback()

    def turn(self):
        return len(self.history)

    def before_move(self, callback):
        self.on_move_before.append(callback)

    def after_move(self, callback):
        self.on_move_after.append(callback)
