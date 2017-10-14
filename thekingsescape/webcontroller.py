from .game.player import Player
from .game.game import Game
from .web_app.app import app
from bottle import run


class WebController():

    def __init__(self):
        self.p1 = Player("Player 1")
        self.p2 = Player("Player 2")
        self.game = Game(attackingPlayer=self.p1,
                         defendingPlayer=self.p2)

    def start(self):
        run(app, host='localhost', port=8080, debug=True)

    @staticmethod
    def pawn2html(pawn):
        return ("<div class=%s></div>" %
                type(pawn).__name__)

    @staticmethod
    def cell2html(cell):
        pawn_html = ""
        if(cell.isOccupied()):
            pawn_html = WebController.cell2html(cell.pawn)
        return ("<td class=%s, row=%s, col=%s>%s</td>" %
                (type(cell).__name__, pawn_html,
                 cell.position[1], cell.position[2]))

    @staticmethod
    def game2html(game):
        def row2html(row):
            for cell in row:
                    yield(WebController.cell2html(cell))

        def body_html():
            for row in game.cells:
                yield "<tr>" + "".join(row2html(row)) + "</tr>"

        return ("<table>\n%s\n</table>" %
                '\n'.join(body_html()))
