class Controller:
    def __init__(self, model, view):
        self.__model = model
        self._view = view

    def start(self):
        self.__model.setup(self)
        self._view.setup(self)

        self._view.start_main_loop()
