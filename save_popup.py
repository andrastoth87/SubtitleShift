import tkinter as tk
import widget_helpers
from widget_helpers import WidgetHelper


class SavePopup(tk.Toplevel, WidgetHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Save File")
        self.withdraw()
        self.resizable(False, False)
        self.return_value = tk.StringVar()

        self.protocol('WM_DELETE_WINDOW', lambda: self._set_value(None, 'cancel'))  # root is your root window

        self._create_gui()

    def _create_gui(self):
        if 'main_frame':
            main_frame = tk.Frame(self)
            main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')

            tk.Label(main_frame, text="The subtitle was successfully shifted, select how you would like save the file.").grid(row=0, column=0, columnspan=2)

            if 'button_container':
                button_container = tk.Frame(main_frame)
                button_container.grid(row=1, column=0, sticky='w', pady=(20, 0))

                tk.Button(button_container, text="Overwrite", command=lambda: self._set_value(None, 'overwrite')).grid(
                    row=0, column=0, ipadx=10)
                tk.Button(button_container, text="Save As...", command=lambda: self._set_value(None, 'save_as')).grid(
                    row=0, column=1, ipadx=10, padx=(10, 0))

            tk.Button(main_frame, text="Cancel", command=lambda: self._set_value(None, 'cancel')).grid(row=1, column=1, ipadx=10, pady=(20, 0), sticky='e')

    def _set_value(self, event, value):
        self.return_value.set(value)

        self.destroy()

    def wait_value(self):
        # make root window unclickable
        self.grab_set()
        self.focus_set()

        self.center_widget()
        self.deiconify()

        self.wait_window()

        self.grab_release()

        return self.return_value.get()