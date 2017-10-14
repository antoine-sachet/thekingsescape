import string
# app is also imported from flaskapp.app
# when a WebView is instantiated.


class AbstractView:
    """Abstract base class for views

    A view allows to render graphically a game.
    A view should be registered with the game controller:
    controller.registerView(myView)

    The main method to implement is render(self, game).
    """

    def __init__(self):
        pass

    def render(self, game):
        raise NotImplementedError("AbstractView should not be instantiated")

    def glimpse(self, game):
        def row2str(row):
            return ''.join([cell.glimpse() for cell in row])

        body = '\n'.join([row2str(row) for row in game.cells])
        return body


class TextView(AbstractView):
    """ Concrete implementation of a textual view."""

    def __init__(self, stream):
        self.stream = stream

    def _toString(self, game):
        def row2str(row, i):
            if(i in [0, game.width + 1]):
                numstr = 2 * ' '
            else:
                numstr = str(i).ljust(2)
            rowstr = ''.join([cell.render() for cell in row])
            return numstr + rowstr + '|'

        # toprow = ''.join(
        #    [str(i).ljust(2) + '  ' for i in range(1, game.width + 1)])
        # toprow = 4 * ' ' + numrow + ' '

        toprow = list(string.ascii_uppercase)
        toprow = toprow[:game.width]
        toprow = 4 * ' ' + '   '.join(toprow)

        body = '\n'.join(
            [row2str(game.cells[i], i)
             for i in range(len(game.cells))])
        return toprow + '\n' + body

    def render(self, game):
        """Prints a text rendering of the current state
        of the game to the stream provided."""
        print(self._toString(game))

    def __repr___(self):
        return "TextView(game=%r, stream=%r)" % (self.game, self.stream)


class WebView(AbstractView):

    def __init__(self):
        from .flaskapp import app
        self.app = app
        self.app.run(debug=True)

    @staticmethod
    def pawn2html(pawn):
        return ("<div class=%s></div>" %
                type(pawn).__name__)

    @staticmethod
    def cell2html(cell):
        pawn_html = ""
        if(cell.isOccupied()):
            pawn_html = WebView.cell2html(cell.pawn)
        return ("<td class=%s>%s</td>" %
                (type(cell).__name__, pawn_html))

    @staticmethod
    def game2html(game):
        def row2html(row):
            for cell in row:
                    yield(WebView.cell2html(cell))

        def body_html():
            for row in game.cells:
                yield "<tr>" + "".join(row2html(row)) + "</tr>"

        return ("<table>\n%s\n</table>" %
                '\n'.join(body_html()))

    def render(self, game):
        pass
