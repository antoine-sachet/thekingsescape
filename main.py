from game import Game
from player import Player
from view import TextView


def main():
    p1 = Player("Antoine")
    p2 = Player("Johanna")

    g = Game(attackingPlayer=p1, defendingPlayer=p2)
    v = TextView(g)

    v.render()


if(__name__ == "__main__"):
    main()
