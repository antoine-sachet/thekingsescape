class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Player(name=%s)" % repr(self.name)
