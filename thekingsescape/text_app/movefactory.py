import re
import string
from ..game.move import Move


class MoveFactory:
    """Helper class to create moves from user text inputs.

    Regex are used to extract the cell from strings of the form
    '<Letter><Number> to <Letter><Number>'

    Useful public method is buildMoveFromString()

    This class is used by the TextController class.
    """

    def __init__(self,
                 game,
                 moveRegex=r"([A-Za-z]\d+) *to *([A-Za-z]\d+)",
                 cellRegex=r"([A-Za-z])(\d+)"):
        self.moveRegex = re.compile(moveRegex)
        self.cellRegex = re.compile(cellRegex)
        self.game = game

    @staticmethod
    def _letter2index(letter):
        alphabet = string.ascii_uppercase
        return alphabet.find(letter.upper()) + 1

    def _str2cell(self, cellStr):
        captured_groups = self.cellRegex.findall(cellStr)
        if(len(captured_groups) != 1):
            raise ValueError("Could not parse the cell: " + cellStr)
        (col, row) = captured_groups[0]
        col = MoveFactory._letter2index(col)
        try:
            row = int(row)
            cell = self.game.getCell(row, col)
        except IndexError:
            raise ValueError("Incorrect cell definition:" + repr((row, col)))
        return cell

    def _extractCells(self, moveStr):
        captured_groups = self.moveRegex.findall(moveStr)
        if(len(captured_groups) != 1):
            raise ValueError("Could not parse the move: " + moveStr)
        cells_str = captured_groups[0]
        cells = [self._str2cell(s) for s in cells_str]
        return cells

    def buildMoveFromString(self, moveStr, player):
        """ Returns a Move from a user-entered string and a player"""

        cells = self._extractCells(moveStr)
        return Move(cells[0], cells[1], self.game, player)

    def __repr__(self):
        return "MoveFactory(game=%r)" % self.game
