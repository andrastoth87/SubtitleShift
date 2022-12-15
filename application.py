from controller import Controller
from view import View
from model import Model


class Application:
    def __init__(self):
        controller = Controller(Model(), View())
        controller.start()





