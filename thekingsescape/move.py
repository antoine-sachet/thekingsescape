from thekingsescape.cell import CellException


class IllegalMoveException(Exception):
    pass


class Move:
    def __init__(self,
                 startCell,
                 endCell,
                 game,
                 player):
        self.startCell = startCell
        self.endCell = endCell
        self.game = game
        self.player = player

    def do_with(self, player):
        if(not self.isLegal()):
            raise IllegalMoveException(self.whyNotLegal(player))
        pawn = self.startCell.takePawn()
        self.endCell.placePawn(pawn)

    def _checkCells(self):
        if(self.startCell.isEmpty()):
            raise IllegalMoveException("No pawn in start cell")
        if(self.endCell.isOccupied()):
            raise IllegalMoveException("Targeted cell is already occupied")
        return True

    def _checkPawn(self):
        pawn = self.startCell.getPawn()
        if(not pawn.can_go_on(self.endCell)):
            message = ("This pawn (" + str(pawn) +
                       ") cannot go on this type of cell (" +
                       str(self.endCell.type) + ")")
            raise IllegalMoveException(message)
        return True

    def _checkPlayer(self):
        pawn = self.startCell.getPawn()
        if(not pawn.owner == self.player):
            message = ("Player (" + self.player +
                       "is not allowed to move that pawn (" +
                       pawn + ")")
            raise IllegalMoveException(message)

    def _checkPath(self):
        if(not self._isStraightLine()):
            raise IllegalMoveException("Move is not a straight line")
        path = self._getPath()
        if(any(cell.isOccupied() for cell in path)):
            raise IllegalMoveException("There are pawns on the path")
        return True

    def _getLegalityStatus(self):
        try:
            self._checkPawn()
            self._checkPlayer()
            self._checkPath()
            self._checkCells()
        except (IllegalMoveException, CellException) as errorMessage:
            return (False, errorMessage)
        return (True, "Legal move")

    def isLegal(self):
        return self._getLegalityStatus()[0]

    def whyNotLegal(self):
        return self._getLegalityStatus()[1]

    def __str__(self):
        return str(self.startCell) + "->" + str(self.endCell)

    def _isStraightLine(self):
        zippedPos = zip(self.startCell.position,
                        self.endCell.position)
        posDiff = [pos[0] - pos[1] for pos in zippedPos]
        isStraightLine = 0 in posDiff
        return isStraightLine

    def _getPath(self):
        """Yields cells on the path of the move,
        start and end cells excluded"""
        (startRow, startCol) = self.startCell.position
        (endRow, endCol) = self.endCell.position
        if(startRow - endRow == 0):
            for col in range(min(endCol, startCol) + 1,
                             max(endCol, startCol)):
                yield self.game.getCell(startRow, col)
        elif(startCol - endCol == 0):
            for row in range(min(startRow, endRow) + 1,
                             max(startRow, endRow)):
                yield self.game.getCell(row, startCol)
        else:
            raise ValueError("Move is not straight line")
