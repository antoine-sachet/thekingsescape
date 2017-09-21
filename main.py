from game import Game
from player import Player
from view import TextView
from movefactory import MoveFactory


def main():
    p1 = Player("Antoine")
    p2 = Player("Johanna")

    g = Game(attackingPlayer=p1, defendingPlayer=p2)
    v = TextView(g)

    v.render()

    mf = MoveFactory(g)
    m = mf.buildMoveFromString("A4 to E4", p1)
    print(m)

    p1.perform(m)

    v.render()


if(__name__ == "__main__"):
    main()
