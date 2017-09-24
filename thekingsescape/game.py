from .cell import Cell, CellType
from .pawn import Attacker, Defender, King


class Game:
    """World (map of cells)"""

    def __init__(self, attackingPlayer, defendingPlayer):
        self.width = 11
        self.cells = Game.createCells(self.width)
        self.attackingPlayer = attackingPlayer
        self.defendingPlayer = defendingPlayer
        self.king = King(self.defendingPlayer)
        self.populate()

    def getCell(self, rowIndex, colIndex):
        return self.cells[rowIndex][colIndex]

    def populate(self):
        def a():
            return Attacker(self.attackingPlayer)

        def d():
            return Defender(self.defendingPlayer)

        for i in range(4, 9):
            self.cells[i][1].placePawn(a())
            self.cells[i][self.width].placePawn(a())
            self.cells[1][i].placePawn(a())
            self.cells[self.width][i].placePawn(a())
        self.cells[6][2].placePawn(a())
        self.cells[2][6].placePawn(a())
        self.cells[10][6].placePawn(a())
        self.cells[6][10].placePawn(a())

        self.cells[6][6].placePawn(self.king)

        for i in [4, 5, 7, 8]:
                self.cells[i][6].placePawn(d())
                self.cells[6][i].placePawn(d())
        for i in [5, 7]:
            for j in [5, 7]:
                self.cells[i][j].placePawn(d())

    @staticmethod
    def createCells(n):
        "Creates a n-by-n 2D list of cells"

        def wallrow():
            wall = [Cell(CellType.VWALL)]
            wall.extend([Cell(CellType.HWALL) for _ in range(n)])
            wall.append(Cell(CellType.VWALL))
            return wall

        def normalrow():
            out = [Cell(CellType.VWALL)]
            out.extend([Cell(CellType.NORMAL) for _ in range(n)])
            out.append(Cell(CellType.VWALL))
            return out

        def castlerow():
            out = [Cell(CellType.VWALL), Cell(CellType.CASTLE)]
            out.extend([Cell(CellType.NORMAL) for _ in range(n - 2)])
            out.extend([Cell(CellType.CASTLE), Cell(CellType.VWALL)])
            return out

        cells = [wallrow()]
        cells.append(castlerow())
        cells.extend([normalrow() for _ in range(n - 2)])
        cells.append(castlerow())
        cells.append(wallrow())

        for i in range(n + 2):
            for j in range(n + 2):
                cells[i][j].setPosition((i, j))

        return cells
