from enum import Enum


class CellException(Exception):
    """Cell related exceptions, typically thrown when trying
    to take a pawn from an empty cell"""
    pass


class CellType(Enum):
    """Cell type enumeration.
    Cells use composition around a cell type rather than inheritance"""
    NORMAL = 1
    CASTLE = 2
    HWALL = 3
    VWALL = 4


CellChars = {
    CellType.NORMAL: ' ',
    CellType.CASTLE: 'Ω',
    CellType.HWALL: '-',
    CellType.VWALL: '|'
}


class Cell:
    """Class for board cells.

    A cell has a type (of class CellType) and can have an occupant (a pawn).
    Cells get attributed a position in the game when the board is created.
    """

    def __init__(self, cellType):
        self.pawn = None
        self.type = cellType
        self.position = (None, None)

    def setPosition(self, xy_tuple):
        """Sets the position of the cell,
        for use by Game class when creating the board"""
        self.position = xy_tuple

    def isOccupied(self):
        """Return True if the cell has an occupant."""
        return not self.isEmpty()

    def isEmpty(self):
        """Return True if the cell does not have an occupant."""
        return self.pawn is None

    def getPawn(self):
        """Returns the cell occupant. Raises CellException if cell is empty."""
        if self.isEmpty():
            raise CellException("Cannot get pawn of empty cell")
        return self.pawn

    def placePawn(self, newPawn):
        """Sets the given pawn as the new occupant.
        Raises CellException if cell is already occupied."""
        if(not self.isEmpty()):
            raise CellException("Cannot place pawn on non-empty cell")
        self.pawn = newPawn
        newPawn.setPosition(self)

    def takePawn(self):
        """Returns the cell occupant with the side of effect of freeing the cell.
        Code equivalent of grabbing the pawn off the board."""
        occ = self.getPawn()
        occ.setPosition(None)
        self.pawn = None
        return occ

    def __str__(self):
        return (str(self.type) +
                str(self.position) + "[" +
                str(self.pawn) + "]")

    def __repr__(self):
        return ("Cell(type=%r, row=%r, col=%r, occupant=%r)" %
                (self.type, self.position[0], self.position[1], self.occupant))

    def glimpse(self):
        """Returns the cell symbol to use in a text view of the game"""
        if(self.isOccupied()):
            return str(self.pawn)
        else:
            return CellChars.get(self.type, 'Error')

    def render(self):
        """Used to create a text view of the game"""
        if(self.type == CellType.VWALL):
            return ''
        if(self.type == CellType.HWALL):
            return 4 * self.glimpse()
        else:
            return '| ' + self.glimpse() + ' '

    def isBlockingTo(self, pawn):
        """Returns true if the cell or its occupant is blocking the given pawn.
        If a pawn is blocked on two opposite sides, it is taken.
        This method is used to check if a pawn is taken after a move."""
        if(self.type != CellType.NORMAL):
            return True
        if(self.isOccupied()):
            if(self.getPawn().owner != pawn.owner):
                return True
        return False
