import string


class View:

    def __init__(self, game):
        self.game = game

    def render(self):
        pass

    def glimpse(self):
        def row2str(row):
            return ''.join([cell.glimpse() for cell in row])

        body = '\n'.join([row2str(row) for row in self.game.cells])
        return body


class TextView(View):
    def toString(self):
        def row2str(row, i):
            if(i in [0, self.game.width + 1]):
                numstr = 2 * ' '
            else:
                numstr = str(i).ljust(2)
            rowstr = ''.join([cell.render() for cell in row])
            return numstr + rowstr + '|'

        # toprow = ''.join(
        #    [str(i).ljust(2) + '  ' for i in range(1, game.width + 1)])
        # toprow = 4 * ' ' + numrow + ' '

        toprow = list(string.ascii_uppercase)
        toprow = toprow[:self.game.width]
        toprow = 4 * ' ' + '   '.join(toprow)

        body = '\n'.join(
            [row2str(self.game.cells[i], i)
             for i in range(len(self.game.cells))])
        return toprow + '\n' + body

    def render(self):
        print(self.toString())

    def __str___(self):
        return "Text view of game: " + str(self.game)
