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





