import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as tkMessagebox
import re
from save_popup import SavePopup
from enum import Enum
import os
from widget_helpers import WidgetHelper
from controller import Controller
from view import View
from model import Model


class Application:
    def __init__(self):
        controller = Controller(Model(), View())
        controller.start()

    def _save_file(self, save_path, text) -> None:
        """
        Write the supplied string to the disk.
        """
        if not save_path:
            return

        with open(save_path, 'w') as f:
            f.write(text)

    def _get_save_path(self):
        filetypes = []

        filename, file_extension = os.path.splitext(self.open_file_path)
        filetypes.append((f'Subtitle Files *{file_extension}', f'*{file_extension}'))
        filetypes.append(('All Files *.*', '*.*'))

        try:
            return fd.asksaveasfile(filetypes=filetypes, defaultextension=filetypes).name
        except AttributeError:
            return ''





