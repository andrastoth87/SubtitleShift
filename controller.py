# States of this program
import os


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

    def change_state(self, new_state: str) -> None:
        """ Sets the new state of the application. """
        self.__state = new_state

        if self.__state == State.INITIALIZED:
            self.__view.on_state_initialized()
        elif self.__state == State.LOADED:
            self.__view.on_state_loaded()

    def get_supported_extensions_str(self, leading_chars, separator, sort=True) -> str:
        """ Construct, sort and return a string with the supported extensions.
        To make the function more generic leading chars and separators can be added. """

        extensions = self.__model.get_supported_extensions()

        if sort:
            extensions.sort()

        extensions = [leading_chars + x for x in extensions]

        return separator.join(extensions)

    def get_supported_extensions_list(self, sort=True) -> list[str]:
        """ Returns a list of the supported extensions. """

        extensions = self.__model.get_supported_extensions()

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

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()

    def _reset(self):
        """
        Reset all the values to the initialized state
        """
        self.__model.set_subtitle_path('')
        self.__view.reset_fields()

        self.change_state(State.INITIALIZED)

    def process_file(self, shift_amount: int) -> None:
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
        processor = self.__model.get_processor(self.get_extension_from_path(subtitle_path))

        if processor is None:
            self.__view.show_error_messagebox('Error', 'Could not get the processor.')

            return

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
                path = self.__view.get_save_path()

                if not path:
                    continue

                save_path = path

                break

        self._save_file(save_path, shifted_subtitle_text)

    @staticmethod
    def get_extension_from_path(path: str) -> str:
        """  Return the extension from the supplied path. """
        filename, file_extension = os.path.splitext(path)

        return file_extension[1:]

    def _save_file(self, save_path, text) -> None:
        """ Write the supplied string to the disk. """
        if not save_path:
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except UnicodeEncodeError:
            with open(save_path, 'w', encoding='latin-1') as f:
                f.write(text)


