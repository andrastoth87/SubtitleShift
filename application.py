import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter import messagebox as tkMessagebox
import re
from save_popup import SavePopup
from enum import Enum
import os
from widget_helpers import WidgetHelper
from processors.processor_sub import ProcessorSUB
from processors.processor_general import ProcessorGENERAL

# States of this program
class State(Enum):
    INITIALIZED = 0
    LOADED = 1

class Application(tk.Tk, WidgetHelper):
    def __init__(self):
        super().__init__()

        self.title('SubShifter')
        self.resizable(False, False)
        self.withdraw()

        self.state = None

        # The value of the radio button that will determine if we shift the subtitle in a positive or negative direction. 0 = positive, 1 = negative.
        self.radiobutton_val = tk.IntVar()

        self.open_file_path = ''

        # Default constant values
        self.FONT_INFORMATION_ITALIC = ('TkDefaultFont', 9, 'italic')
        self.COLOR_RED = '#ffaaaa'
        self.COLOR_LIGHT_YELLOW = '#fff6d5'
        self.COLOR_YELLOW = '#ffeeaa'
        self.COLOR_LIGHT_GREEN = '#e5ffd5'
        self.COLOR_GREEN = '#ccffaa'

        self.supported_extensions = {
            'sub': ProcessorSUB(r'{(\d+)}'),
            'srt': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ass': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ssa': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'vtt': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'scc': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'sbv': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ttml': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})')
        }

        self._create_gui()

        self.center_widget()

        self.deiconify()

        self._change_state(State.INITIALIZED)

        self.mainloop()

    def _create_gui(self):
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

                extensions = self._get_supported_extensions('', ', ')
                tk.Label(open_container, text=f"Supported subtitle formats: {extensions}", font=self.FONT_INFORMATION_ITALIC).grid(row=1, column=0, columnspan=2, sticky='w')

            if "option_container":
                option_container = tk.Frame(main_container)
                option_container.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
                option_container.columnconfigure(0, weight=1)
                option_container.columnconfigure(1, weight=1)

                tk.Radiobutton(option_container, text="Add offset", variable=self.radiobutton_val, value=0).grid(row=0, column=0)
                tk.Radiobutton(option_container, text="Remove offset", variable=self.radiobutton_val, value=1).grid(row=0, column=1)

            if "entry_container":
                entry_container = tk.Frame(main_container)
                entry_container.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
                entry_container.columnconfigure(0, weight=1)
                entry_container.columnconfigure(1, weight=1)

                tk.Label(entry_container, text="Offset amount (in milliseconds):").grid(row=0, column=0, sticky='w')

                validate_cmd = (self.register(self._validate))
                self.entry_offset_amount = tk.Entry(entry_container, validate='all', validatecommand=(validate_cmd, '%P'))
                self.entry_offset_amount.grid(row=0, column=1, padx=(10, 0), sticky='w')

                tk.Label(entry_container, text="1 second = 1000 milliseconds", font=self.FONT_INFORMATION_ITALIC).grid(row=1, column=0, columnspan=2, sticky='w')

            self.button_sync = tk.Button(main_container, text="Synchronise Subtitle", command=lambda: self._process_file(self.open_file_path), borderwidth=1, relief=tk.SOLID)
            self.button_sync.grid(row=3, column=0, columnspan=2, ipadx=10, ipady=5, pady=(10, 0), sticky='ew')

    def _validate(self, value_if_allowed):
        pattern = re.compile(r'^[1-9]\d*$')

        if pattern.match(value_if_allowed) or value_if_allowed == '':
            return True
        else:
            return False

    def _get_open_path(self):
        extensions = self._get_supported_extensions('*.', ' ')

        filetypes = (
            (f'Subtitle Files ({extensions})', extensions),
            ('All files *.*', '*.*')
        )

        open_path = fd.askopenfilename(title='Open Subtitle...', initialdir='/', filetypes=filetypes)

        if not open_path:
            return

        if not self._get_extension_from_path(open_path) in self.supported_extensions:
            tkMessagebox.showwarning('Warning', 'Unsupported filetype! Please select a different file!')

            return

        self.open_file_path = open_path
        self._change_state(State.LOADED)

    def _read_file(self, open_path):
        """
        Read the file from the path and return the content as string.
        """
        if not open_path:
            return

        with open(open_path, 'r') as f:
            return f.read()

    def _save_file(self, save_path, text):
        """
        Write the supplied string to the disk.
        """
        if not save_path:
            return

        with open(save_path, 'w') as f:
            f.write(text)

    def _get_offset_amount(self):
        value = self.entry_offset_amount.get()
        value.lstrip("0")

        if not value:
            return 0

        try:
            return int(value)
        except ValueError:
            return 0

    def _process_file(self, path):
        shift_amount = self._get_offset_amount()

        if self.radiobutton_val.get() == 1:
            shift_amount *= -1

        subtitle_text = self._read_file(path)

        processor = self.supported_extensions[self._get_extension_from_path(self.open_file_path)]
        shifted_subtitle_text = processor.shift(subtitle_text, shift_amount)

        while True:
            user_choice = SavePopup().wait_value()
            save_path = ''

            if user_choice == 'cancel':
                return

            elif user_choice == 'overwrite':
                answer = tkMessagebox.askquestion("Confirm Overwrite", "Are you sure you want to overwrite the file?", icon='warning')

                if answer == 'no':
                    continue

                save_path = self.open_file_path

                break

            elif user_choice == 'save_as':
                path = self._get_save_path()

                if not path:
                    continue

                save_path = path

                break

        self._save_file(save_path, shifted_subtitle_text)

    def _get_save_path(self):
        filetypes = []

        filename, file_extension = os.path.splitext(self.open_file_path)
        filetypes.append((f'Subtitle Files *{file_extension}', f'*{file_extension}'))
        filetypes.append(('All Files *.*', '*.*'))

        try:
            return fd.asksaveasfile(filetypes=filetypes, defaultextension=filetypes).name
        except AttributeError:
            return ''

    def _change_state(self, new_state):
        """

        """
        self.state = new_state

        if self.state == State.INITIALIZED:
            self._on_state_initialized()
        elif self.state == State.LOADED:
            self._on_state_loaded()

    def _get_supported_extensions(self, leading_chars, separator):
        """
        Construct and return a string with the supported extensions.
        To make the function more generic leading chars and separators can be added.
        """
        extensions = [leading_chars + x for x in self.supported_extensions.keys()]
        return separator.join(extensions)

    def _get_extension_from_path(self, path):
        """
        Return the extension from the supplied path
        """
        filename, file_extension = os.path.splitext(path)
        return file_extension[1:]

    def _on_state_initialized(self):
        """
        Change the variables associated with this state.
        """
        self.button_sync.config(state='disabled', bg='grey85')
        self.button_open.config(bg=self.COLOR_YELLOW, activebackground=self.COLOR_LIGHT_YELLOW)

    def _on_state_loaded(self):
        """
        Change the variables associated with this state.
        """
        self._fit_text_to_label(self.label_file_path, self.open_file_path)
        self.button_sync.config(state='normal', bg=self.COLOR_GREEN, activebackground=self.COLOR_LIGHT_GREEN)
        self.button_open.config(bg=self.COLOR_GREEN, activebackground=self.COLOR_LIGHT_GREEN)

    def _fit_text_to_label(self, label_widget, text):
        """
        Fit the text to the available label size by removing the first char until the text width is smaller than the available label width.
        If the desired length is met than add ... to the beginning.
        We do this because we are only interested in the filename that is open and do not necessarily wand to show the whole path.
        """
        font = tkFont.nametofont(label_widget.cget("font"))

        self.update()

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





