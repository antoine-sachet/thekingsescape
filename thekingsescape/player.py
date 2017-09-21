class Player:
    def __init__(self, name):
        self.name = name

    def perform(self, move):
        move.do_with(self)
