# States of this program
class State:
    UNINITIALIZED = 'UNINITIALIZED'
    INITIALIZED = 'INITIALIZED'
    LOADED = 'LOADED'


class Controller:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

        self.__state = State.UNINITIALIZED

    def start(self):
        self.__model.setup(self)
        self.__view.setup(self)

        self.__view.start_main_loop()

    def _change_state(self, new_state: str) -> None:
        """ Sets the new state of the application. """
        self.__state = new_state

        if self.__state == State.INITIALIZED:
            self.__view.on_state_initialized()
        elif self.__state == State.LOADED:
            self.__view.on_state_loaded()

    def get_supported_extensions_str(self, leading_chars, separator, sort=True) -> str:
        """ Construct, sort and return a string with the supported extensions.
        To make the function more generic leading chars and separators can be added. """

        extensions = self.__model.get_supported_extensions_str()

        if sort:
            extensions.sort()

        extensions = [leading_chars + x for x in extensions]

        return separator.join(extensions)

    def get_supported_extensions_list(self, sort=True) -> list[str]:
        """ Returns a list of the supported extensions. """

        extensions = self.__model.get_supported_extensions_str()

        if sort:
            extensions.sort()

        return extensions

    def get_subtitle_path(self) -> str:
        return self.__model.get_subtitle_path()

    def set_subtitle_path(self, path: str) -> None:
        """ Sets the path of the subtitle. """
        self.__model.set_subtitle_path(path)

    @staticmethod
    def _read_file(path: str) -> str:
        """ Read the file from the path and return the content as string. """
        if not path:
            return ''

        with open(path, 'r') as f:
            return f.read()

    def _reset(self):
        """
        Reset all the values to the initialized state
        """
        self.__model.set_subtitle_path('')
        self.__view.reset_fields()

        self._change_state(State.INITIALIZED)

    def _process_file(self, shift_amount: int) -> None:
        """ This is where the magic happens :) """

        subtitle_path = self.__model.get_subtitle_path()

        subtitle_text = ''

        try:
            subtitle_text = self._read_file(subtitle_path)
        except FileNotFoundError:
            # Reset to initialized state and return
            self.__view.show_error_messagebox('SubShifter', f'File not found:\n{subtitle_path}')

            self._reset()

            return

        # This is where the magic happens! The processor will get the timestamps from the sub file and shift them.
        processor = self.supported_extensions[self._get_extension_from_path(self.open_file_path)]
        shifted_subtitle_text = processor.shift(subtitle_text, shift_amount)

        while True:
            user_choice = self.__view.show_save_popup()
            save_path = ''

            # If the cancel button was pressed, do nothing
            if user_choice == 'cancel':
                return

            # Ask the user for overwrite confirmation
            elif user_choice == 'overwrite':
                answer = self.__view.show_ask_question_messagebox('Confirm overwrite', 'Are you sure you want to overwrite the file?')

                if answer == 'no':
                    continue

                save_path = subtitle_path

                break

            # Prompt the user for the save location
            elif user_choice == 'save_as':
                path = self._get_save_path()

                if not path:
                    continue

                save_path = path

                break

        self._save_file(save_path, shifted_subtitle_text)


