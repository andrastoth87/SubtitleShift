import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkMessagebox
from tkinter import filedialog as tkFileDialog
from save_popup import SavePopup
import re
from controller import State
import os


class View:
    def __init__(self) -> None:
        self.__controller = None

        # Default constant values to use.
        self.FONT_INFORMATION_ITALIC = ('TkDefaultFont', 9, 'italic')
        self.COLOR_RED = '#ffaaaa'
        self.COLOR_LIGHT_YELLOW = '#fff6d5'
        self.COLOR_YELLOW = '#ffeeaa'
        self.COLOR_LIGHT_GREEN = '#e5ffd5'
        self.COLOR_GREEN = '#ccffaa'

        # The value of the radio button that will determine if we shift the subtitle in a positive or negative direction. 0 = positive, 1 = negative.
        self.radiobutton_val = tk.IntVar()

    def setup(self, controller):
        self.__controller = controller

        self._create_gui()
        self.__controller.check_for_open_orders()

    def _create_gui(self):
        self.root = tk.Tk()

        self.root.title('SubShifter')
        self.root.resizable(False, False)
        # Hide the GUI until it is created and centered.
        self.root.withdraw()

        if "main_container":
            main_container = tk.Frame(self)
            main_container.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')

            if "open_container":
                open_container = tk.Frame(main_container)
                open_container.grid(row=0, column=0, columnspan=2, sticky='ew')
                open_container.columnconfigure(0, weight=0)
                open_container.columnconfigure(1, weight=1)

                self.button_open = tk.Button(open_container, text="Open File", command=self._get_open_path, borderwidth=1, relief=tk.SOLID)
                self.button_open.grid(row=0, column=0, ipadx=10, sticky='w')
                self.label_file_path = tk.Label(open_container, text="No file chosen")
                self.label_file_path.grid(row=0, column=1, sticky='we', padx=(10, 0))

                extensions = self.__controller.get_supported_extensions_str('', ', ')
                tk.Label(open_container, text=f"Supported subtitle formats: {extensions}", font=self.FONT_INFORMATION_ITALIC).grid(row=1, column=0, columnspan=2, sticky='w')

            if "option_container":
                option_container = tk.Frame(main_container)
                option_container.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
                option_container.columnconfigure(0, weight=1)
                option_container.columnconfigure(1, weight=1)

                tk.Radiobutton(option_container, text="Add offset", variable=self.radiobutton_val, value=1).grid(row=0, column=0)
                tk.Radiobutton(option_container, text="Remove offset", variable=self.radiobutton_val, value=-1).grid(row=0, column=1)

            if "entry_container":
                entry_container = tk.Frame(main_container)
                entry_container.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
                entry_container.columnconfigure(0, weight=1)
                entry_container.columnconfigure(1, weight=1)

                tk.Label(entry_container, text="Offset amount (in milliseconds):").grid(row=0, column=0, sticky='w')

                validate_cmd = (main_container.register(self._validate_input))
                self.entry_offset_amount = tk.Entry(entry_container, validate='all', validatecommand=(validate_cmd, '%P'))
                self.entry_offset_amount.grid(row=0, column=1, padx=(10, 0), sticky='w')

                tk.Label(entry_container, text="1 second = 1000 milliseconds", font=self.FONT_INFORMATION_ITALIC).grid(row=1, column=0, columnspan=2, sticky='w')

            self.button_sync = tk.Button(main_container, text="Synchronise Subtitle", command=lambda: self.__controller.process_file(self._get_shift_amount, ), borderwidth=1, relief=tk.SOLID)
            self.button_sync.grid(row=3, column=0, columnspan=2, ipadx=10, ipady=5, pady=(10, 0), sticky='ew')

        self._center_widget()

        # Show GUI
        self.root.deiconify()

    def _center_widget(self):
        # Center window
        self.root.update()

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    @staticmethod
    def _validate_input(value_if_allowed: str) -> bool:
        """ Validation for the offset amount entry to only allow positive numbers. """

        pattern = re.compile(r'^[1-9]\d*$')

        if pattern.match(value_if_allowed) or value_if_allowed == '':
            return True
        else:
            return False

    def on_state_initialized(self):
        """ Change the variables associated with this state. """
        self.button_sync.config(state='disabled', bg='grey85')
        self.button_open.config(bg=self.COLOR_YELLOW, activebackground=self.COLOR_LIGHT_YELLOW)

    def on_state_loaded(self):
        """ Change the variables associated with this state. """
        self._fit_text_to_label(self.label_file_path, self.__controller.get_subtitle_path())
        self.button_sync.config(state='normal', bg=self.COLOR_GREEN, activebackground=self.COLOR_LIGHT_GREEN)
        self.button_open.config(bg=self.COLOR_GREEN, activebackground=self.COLOR_LIGHT_GREEN)

    def _get_open_path(self):
        """ Get the path of the subtitle file. """
        extensions = self.__controller.get_supported_extensions_str('*.', ' ')

        filetypes = (
            (f'Subtitle Files ({extensions})', extensions),
            ('All files *.*', '*.*')
        )

        # Use Tkinter's file dialogue to select a file
        open_path = tkFileDialog.askopenfilename(title='Open Subtitle...', initialdir='/', filetypes=filetypes)

        # If there was no file selected or if the file is not supported then return.
        if not open_path:
            return

        if not self._get_extension_from_path(open_path) in self.__controller.get_supported_extensions_list():
            tkMessagebox.showwarning('Warning', 'Unsupported filetype! Please select a different file!')

            return

        # The filepath is valid then change the state of the program.
        self.__controller.set_subtitle_path(open_path)
        self.__controller.change_state(State.LOADED)

    @staticmethod
    def _get_extension_from_path(path: str) -> str:
        """  Return the extension from the supplied path. """
        filename, file_extension = os.path.splitext(path)

        return file_extension[1:]

    def _fit_text_to_label(self, label_widget: tk.Widget, text: str) -> None:
        """
        Fit the text to the available label size by removing the first char until the text width is smaller than the available label width.
        If the desired length is met than add ... to the beginning.
        We do this because we are only interested in the filename that is open and do not necessarily wand to show the whole path.
        """
        font = tkFont.nametofont(label_widget.cget("font"))

        self.root.update()

        max_width = label_widget.winfo_width()
        actual_width = font.measure(text)

        if actual_width <= max_width:
            # the original text fits; no need to add ellipsis
            label_widget.configure(text=text)
        else:
            # the original text won't fit. Keep shrinking
            # until it does
            while actual_width > max_width and len(text) > 1:
                text = text[1:]
                actual_width = font.measure("..." + text)

            label_widget.configure(text="..." + text)

    def _get_shift_amount(self) -> int:
        """ Returns the offset amount. """

        value = self.entry_offset_amount.get()
        value.lstrip("0")

        if not value:
            return 0

        try:
            return int(value) * self.radiobutton_val.get()
        except ValueError:
            return 0

    @staticmethod
    def show_save_popup() -> str:
        """ Shows the save file popup. """
        return SavePopup().wait_value()

    @staticmethod
    def show_ask_question_messagebox(tile: str, text: str) -> str:
        return tkMessagebox.askquestion(tile, text, icon='warning')

    @staticmethod
    def show_error_messagebox(tile: str, text: str) -> str:
        return tkMessagebox.showerror(tile, text, icon='warning')

    def reset_fields(self) -> None:
        self.radiobutton_val.set(1)
        self.entry_offset_amount.delete(0, 'end')
        self.label_file_path.config(text="No file chosen")
