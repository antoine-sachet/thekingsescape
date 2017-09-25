from .game import Game
from .player import Player
from .movefactory import MoveFactory
from .move import IllegalMoveException


class Controller:
    """Main entry point, this class controls the i/o of the game.

    A concrete implementation of this class should be
    instantiated in order to play the game.

    Main methods:
    - start() : starts the game

    - registerView(view) : registers the given view as an observer of the game.
    The render() method of all registered views is executed after each
    game update.
    """

    def __init__(self):
        self.p1 = Player("Player 1")
        self.p2 = Player("Player 2")
        self.game = Game(attackingPlayer=self.p1,
                         defendingPlayer=self.p2)
        self.views = []

    def registerView(self, view):
        """Registers the given view as an observer of the game.
        More than one view can be registered.
        The render() method of all registered views is executed after each
        game update."""
        self.views.append(view)

    def _updateViews(self):
        """Calls the render() method of all registered views."""
        for view in self.views:
            view.render(self.game)

    def start(self):
        """Starts the game.
        Concrete controllers should implement this method."""
        raise NotImplementedError("A concrete controller should be used.")

    def __repr__(self):
        return ("Controller(p1=%r, p2=%r, game=%r)" &
                (self.p1, self.p2, self.game))


class TextController(Controller):
    """Concrete controller with textual inputs from a specified stream.
    Commonly this stream should be sys.stdout.

    This controller will typically be used with a TextView,
    which should be registered via method registerView()
    """

    def __init__(self, stream):
        super().__init__()
        self.stream = stream
        self.moveFactory = MoveFactory(self.game)

    def _turn(self, player):
        print("It is " + str(player.name) + " s turn to play!")
        print("Write your move and press Enter:")
        validInput = False
        while(not validInput):
            moveStr = input()
            try:
                move = self.moveFactory.buildMoveFromString(moveStr, player)
                self.game.execute(move)
                validInput = True
            except ValueError:
                print("Could not parse move.")
                print("Please enter a correct move, e.g. A4 to B12:")
            except IllegalMoveException as e:
                print("Move not legal: " + str(e))
                print("Please enter a legal move:")

    def start(self):
        players = (self.p1, self.p2)
        turnCount = 0
        self._updateViews()
        while(not self.game.isOver()):
            nextPlayer = players[turnCount % 2]
            self._turn(nextPlayer)
            self._updateViews()
            turnCount = turnCount + 1
        print(self.game.getStatus())

    def __repr__(self):
        return ("TextController(stream=%r, p1=%r, p2=%r, game=%r)" &
                (self.stream, self.p1, self.p2, self.game))
