from cell import CellType


class Pawn:
    def __init__(self, player):
        self.owner = player
        self.cell = None

    def setPosition(self, cell):
        self.cell = cell

    def belongs_to(self):
        return self.owner

    def can_go_on(self, cell):
        return cell.type == CellType.NORMAL

    def __str__(self):
        return 'P'


class Attacker(Pawn):
    def __str__(self):
        return '♂'


class Defender(Pawn):
    def __str__(self):
        return '♀'


class King(Pawn):
    def can_go_on(self, cellType):
        cellType in [CellType.NORMAL, CellType.CASTLE]

    def __str__(self):
        return '♦'
