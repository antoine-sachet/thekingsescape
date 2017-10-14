#!/usr/bin/python3
from thekingsescape.textgame.controller import TextController
from thekingsescape.textgame.view import TextView
from sys import stdout
import logging

logger = logging.Logger("thekingsescape",
                        level=logging.DEBUG)
handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def app_text():

    controller = TextController(stdout)
    v = TextView(stdout)
    controller.registerView(v)

    controller.start()


def app_web():
    pass


if(__name__ == "__main__"):
    app_text()
