import re
import string
from .move import Move


class MoveFactory:
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
            raise ValueError("Incorrect cell definition:" + (row, col))
        return cell

    def _extractCells(self, moveStr):
        captured_groups = self.moveRegex.findall(moveStr)
        if(len(captured_groups) != 1):
            raise ValueError("Could not parse the move: " + moveStr)
        cells_str = captured_groups[0]
        cells = [self._str2cell(s) for s in cells_str]
        return cells

    def buildMoveFromString(self, moveStr, player):
        cells = self._extractCells(moveStr)
        return Move(cells[0], cells[1], self.game, player)
