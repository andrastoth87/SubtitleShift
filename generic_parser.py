import re


class GenericParser:
    def __init__(self, time_format):
        self._time_format = time_format

        # h=Hours, m=minutes, s=seconds, x=milliseconds
        self._time_chars = ('h', 'm', 's', 'x')

        self._regex = ''

        self._blueprint = []

        self._initialize()

    def get_regex(self):
        return self._regex

    def _initialize(self):
        self._regex = self._construct_regex_from_time_format(self._time_format)

    def _construct_regex_from_time_format(self, time_format):
        regex = ''

        position = 0

        while position < len(time_format):
            char = time_format[position]

            if char in self._time_chars:
                temp_regex = char + '+'

                match = re.search(temp_regex, time_format)

                if match is not None:
                    start, end = match.span()
                    position = end

                    char_count = end - start

                    regex += '(\d{1,' + str(char_count) + '})'

                    self._blueprint.append(_CharInfo(char, char_count))

            else:
                regex += char

                self._blueprint.append(char)

                position += 1

        return regex

    def construct_timestamp(self, hours, minutes, seconds, milliseconds):
        joined_timestamp = ''

        for char_info in self._blueprint:
            try:
                char = char_info.get_char()
                char_count = char_info.get_char_count()

                if char == 'h':
                    joined_timestamp += hours[-char_count:].rjust(char_count, '0')
                elif char == 'm':
                    joined_timestamp += minutes[-char_count:].rjust(char_count, '0')
                elif char == 's':
                    joined_timestamp += seconds[-char_count:].rjust(char_count, '0')
                elif char == 'x':
                    joined_timestamp += milliseconds[-char_count:].ljust(char_count, '0')
            except AttributeError:
                joined_timestamp += char_info

        return joined_timestamp


class _CharInfo:
    def __init__(self, char, char_count):
        self._char = char
        self._char_count = char_count

    def get_char(self):
        return self._char

    def get_char_count(self):
        return self._char_count