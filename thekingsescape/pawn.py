from .cell import CellType


class Pawn:
    def __init__(self, player):
        self.owner = player
        self.cell = None

    def setPosition(self, cell):
        self.cell = cell

    def belongs_to(self, player):
        return self.owner == player

    def can_go_on(self, cell):
        return cell.type == CellType.NORMAL

    def __str__(self):
        return 'P'

    def __repr__(self):
        return "Pawn(player=%r)" % self.player


class Attacker(Pawn):
    def __str__(self):
        return '♂'

    def __repr__(self):
        return "Attacker(player=%r)" % self.player


class Defender(Pawn):
    def __str__(self):
        return '♀'

    def __repr__(self):
        return "Defender(player=%r)" % self.player


class King(Pawn):
    def can_go_on(self, cell):
        return cell.type in [CellType.NORMAL, CellType.CASTLE]

    def __str__(self):
        return '♦'

    def __repr__(self):
        return "King(player=%r)" % self.player
