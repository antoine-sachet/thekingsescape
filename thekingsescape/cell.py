from enum import Enum


class CellException(Exception):
    pass


class CellType(Enum):
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
    def __init__(self, cellType):
        self.pawn = None
        self.type = cellType
        self.position = (None, None)

    def setPosition(self, xy_tuple):
        self.position = xy_tuple

    def isOccupied(self):
        return not self.isEmpty()

    def isEmpty(self):
        return self.pawn is None

    def getPawn(self):
        if self.isEmpty():
            raise CellException("Cannot get pawn of empty cell")
        return self.pawn

    def placePawn(self, newPawn):
        if(not self.isEmpty()):
            raise CellException("Cannot place pawn on non-empty cell")
        self.pawn = newPawn
        newPawn.setPosition(self)

    def takePawn(self):
        occ = self.getPawn()
        occ.setPosition(None)
        self.pawn = None
        return occ

    def __str__(self):
        return (str(self.type) +
                str(self.position) + "[" +
                str(self.pawn) + "]")

    def glimpse(self):
        if(self.isOccupied()):
            return str(self.pawn)
        else:
            return CellChars.get(self.type, 'Error')

    def render(self):
        if(self.type == CellType.VWALL):
            return ''
        if(self.type == CellType.HWALL):
            return 4 * self.glimpse()
        else:
            return '| ' + self.glimpse() + ' '
