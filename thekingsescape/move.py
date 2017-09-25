from .cell import CellException


class IllegalMoveException(Exception):
    """Exception thrown when an illegal move is executed."""
    pass


class Move:
    """Class containing a pawn move.

    Instantiated with Move(startCell, endCell, game, player).
    Each instance represents a move from startCell to endCell
    by the given player in the given game.


    Main public methods are:
    - isLegal(self) : returns a boolean indicating legeality of the move
    - whyNotLegal(self) : returns a string describing the legality of the move
    - do_unsafe(self) : should not be called!
    Move must be executed via method 'execute' in class 'Game'.
    """

    def __init__(self,
                 startCell,
                 endCell,
                 game,
                 player):
        self.startCell = startCell
        self.endCell = endCell
        self.game = game
        self.player = player

    def do_unsafe(self):
        """Should not be called - execute the move via game.execute(move)
        Raises IllegalMoveException is the move is not legal."""
        if(not self.isLegal()):
            raise IllegalMoveException(self.whyNotLegal())
        pawn = self.startCell.takePawn()
        self.endCell.placePawn(pawn)

    def _checkCells(self):
        """Check that start cell contains a pawn and end cell is free.
        Raises IllegalMoveException otherwise."""
        if(self.startCell.isEmpty()):
            raise IllegalMoveException("No pawn in start cell")
        if(self.endCell.isOccupied()):
            raise IllegalMoveException("Targeted cell is already occupied")
        return True

    def _checkPawn(self):
        """Check that the moved pawn can be moved to the target cell.
        Raises IllegalMoveException otherwise."""
        pawn = self.startCell.getPawn()
        if(not pawn.can_go_on(self.endCell)):
            message = ("This pawn (%r) cannot go on this type of cell (%r)" %
                       (pawn, self.endCell.type))
            raise IllegalMoveException(message)
        return True

    def _checkPlayer(self):
        """Check that the player is authorised to move the pawn.
        Raises IllegalMoveException otherwise."""
        pawn = self.startCell.getPawn()
        if(not pawn.owner == self.player):
            message = ("Player (%r) is not allowed to move that pawn (%r)" %
                       (self.player, pawn))
            raise IllegalMoveException(message)

    def _checkPath(self):
        """Check that move spans a straight and unobstructed path.
        Raises IllegalMoveException otherwise."""
        if(not self._isStraightLine()):
            raise IllegalMoveException("Move is not a straight line")
        path = self._getPath()
        if(any(cell.isOccupied() for cell in path)):
            raise IllegalMoveException("There are pawns on the path")
        return True

    def _getLegalityStatus(self):
        """Returns a tuple (bool, description)
        where bool is True if the move is legal
        and description is a string describing the legality"""
        try:
            self._checkPawn()
            self._checkPlayer()
            self._checkPath()
            self._checkCells()
        except (IllegalMoveException, CellException) as errorMessage:
            return (False, errorMessage)
        return (True, "Legal move")

    def isLegal(self):
        "Returns True if move is legal, False otherwise."
        return self._getLegalityStatus()[0]

    def whyNotLegal(self):
        """Returns a string describing the legality status.
        Useful for error messages."""
        return self._getLegalityStatus()[1]

    def __str__(self):
        return str(self.startCell) + "->" + str(self.endCell)

    def __repr__(self):
        return ("Move(startCell=%r, endCell=%r, game=%r, player=%r)" %
                (self.startCell, self.endCell, self.game, self.player))

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
