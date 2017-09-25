from thekingsescape.controller import TextController
from thekingsescape.view import TextView
from sys import stdout
import logging


def main():
    logger = logging.Logger("thekingsescape",
                            level=logging.DEBUG)
    handler = logging.StreamHandler(stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    controller = TextController(stdout)
    v = TextView(stdout)
    controller.registerView(v)

    controller.start()


if(__name__ == "__main__"):
    main()
