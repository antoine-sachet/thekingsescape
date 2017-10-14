#!/usr/bin/python3
from sys import stdout
import logging

logger = logging.Logger("thekingsescape",
                        level=logging.DEBUG)
handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def app_text():
    from thekingsescape.text_app.controller import TextController
    from thekingsescape.text_app.view import TextView

    controller = TextController(stdout)
    v = TextView(stdout)
    controller.registerView(v)

    controller.start()


def app_web():
    from thekingsescape.webcontroller import WebController
    wc = WebController()
    wc.start()


if(__name__ == "__main__"):
    app_web()
