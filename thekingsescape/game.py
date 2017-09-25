from .cell import Cell, CellType
from .pawn import Attacker, Defender, King
from enum import Enum


class GameStatus(Enum):
    IN_PROGRESS = 1
    DEFENDER_WON = 2
    ATTACKER_WON = 3
    DRAW = 4


class Game:
    """Class managing the logic of the game.
    Constructed from 2 players with default size 11.

    Note that instantiation should be left to a Controller.

    Main methods:

    - execute(move) : performs a move properly.
    This is the only correct way to perform a move

    - getStatus() : returns the status of the game (Enum class GameStatus)

    - isOver() : True is the game is over (won or lost)

    - getCell(row, col) : only way to get a cell from a position
    """

    def __init__(self, attackingPlayer, defendingPlayer, size=11):
        """Creates a game of the given size (width) with the two given players.
        Creates the board of cells and populates it with pawns."""
        self.width = size
        self.cells = Game.createCells(self.width)
        self.attackingPlayer = attackingPlayer
        self.defendingPlayer = defendingPlayer
        self.king = King(self.defendingPlayer)
        self.populate()

    def execute(self, move):
        """Performs the given move and all side effects.
        This is the only correct way to execute a move."""
        move.do_unsafe()
        potentiallyTaken = self.getNeighbouringCells(move.endCell)
        potentialKiller = move.endCell.getPawn()
        for cell in potentiallyTaken:
            if cell.isOccupied():
                potentialVictim = cell.getPawn()
                if(self.isTakenBy(potentialVictim, potentialKiller)):
                    cell.takePawn()

    def getStatus(self):
        "Returns the current status of the game (see Enum class GameStatus)"
        if(self.king.cell.type == CellType.CASTLE):
            return GameStatus.DEFENDER_WON
        cellsAroundKing = self.getNeighbouringCells(self.king.cell)
        if(all(cell.isBlockingTo(self.king) for cell in cellsAroundKing)):
            return GameStatus.ATTACKER_WON
        return GameStatus.IN_PROGRESS

    def isOver(self):
        "Returns True if the game is over (won or lost)"
        return self.getStatus() in [GameStatus.ATTACKER_WON,
                                    GameStatus.DEFENDER_WON]

    def getCell(self, rowIndex, colIndex):
        "Returns cell at the corresponding (row, column)"
        return self.cells[rowIndex][colIndex]

    def _withinLimits(self, index):
            return index >= 0 & index < self.width

    def getNeighbouringCells(self, cell):
        """Returns the 4 directly neighbouring cells of the given cell.
        May return less than 4 cells if a border cell is given."""
        (row, col) = cell.position
        neighbouringPos = [(row + 1, col), (row - 1, col),
                           (row, col + 1), (row, col - 1)]
        for (r, c) in neighbouringPos:
            if(self._withinLimits(r) & self._withinLimits(c)):
                yield self.getCell(r, c)

    def isTakenBy(self, victim, killer):
        """Returns True if victim pawn is taken by killer pawn,
        assuming killer just moved.
        Returns False if victim is the King as capture rules are different."""
        if(victim == self.king):
            return False
        (row, col) = victim.cell.position
        nhood1 = [self.getCell(r, c)
                  for (r, c) in [(row + 1, col), (row - 1, col)]
                  if self._withinLimits(r) & self._withinLimits(c)]
        nhood2 = [self.getCell(r, c)
                  for (r, c) in [(row, col + 1), (row, col - 1)]
                  if self._withinLimits(r) & self._withinLimits(c)]

        def neighbourhoodIsBlocking(nhood):
            return all(cell.isBlockingTo(victim) for cell in nhood)

        def neighbourhoodContainsTarget(nhood):
            def predicates():
                for cell in nhood:
                    if cell.isOccupied():
                        yield(cell.getPawn() == killer)
            return any(predicates())

        def check(nhood):
            return (neighbourhoodIsBlocking(nhood) &
                    neighbourhoodContainsTarget(nhood))

        return check(nhood1) | check(nhood2)

    def populate(self):
        """Fills in the board with pawns in starting position"""
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
        """Creates a n-by-n 2D list of cells as a valid game board:
        normal cells surrounded by walls with castles in the 4 corners."""

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

    def __repr__(self):
        return ("Game(attackingPlayer=%r, defendingPlayer=%r, size=%r)" %
                (self.attackingPlayer, self.defendingPlayer, self.width))
