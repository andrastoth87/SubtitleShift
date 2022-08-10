from tkinter import messagebox as tkMessagebox


class ProcessorTemplate:
    def __init__(self, regex):
        self._regex = regex

        # self._initialize()

    # def _initialize(self):
    #     raise NotImplementedError

    def shift(self, text, amount):
        raise NotImplementedError

    def _show_error(self, title, error_text):
        tkMessagebox.showerror(title, error_text)
