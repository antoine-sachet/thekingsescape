from thekingsescape.controller import TextController
from thekingsescape.view import TextView, WebView
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

    controller = TextController(stdout)
    v = WebView()
    controller.registerView(v)

    controller.start()


if(__name__ == "__main__"):
    app_web()
