from tkinter import messagebox as tkMessagebox


class ProcessorTemplate:
    """
    A small template to use for the subtitle processors.
    """
    def __init__(self, regex):
        self._regex = regex

    def shift(self, text, amount):
        raise NotImplementedError

    def _show_error(self, title, error_text):
        tkMessagebox.showerror(title, error_text)
