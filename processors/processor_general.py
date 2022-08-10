from processors.processor_template import ProcessorTemplate
import re
import math


class ProcessorGENERAL(ProcessorTemplate):
    def __init__(self, regex):
        ProcessorTemplate.__init__(self, regex)

    def shift(self, text, amount):
        matches = re.finditer(self._regex, text)

        for match in matches:
            try:
                separators = re.findall(r'\D', match[0])
                time_values = match.groups()

                shifted = self._shift_timestamp(*time_values, amount)
                new_timestamp = ''

                # Reconstruct timestamp
                for i in range(len(separators)):
                    new_timestamp += shifted[i].rjust(len(time_values[i]), '0')
                    new_timestamp += separators[i]

                    if i == len(separators) - 1:
                        new_timestamp += shifted[i + 1].ljust(len(time_values[i]), '0')

                text = text.replace(match[0], new_timestamp)

            except ValueError:
                self._show_error('Value Error', 'Something went wrong! Please try again or try another file.')

                return

        return text

    def _shift_timestamp(self, hours, minutes, seconds, milliseconds, offset_in_milliseconds):
        # Convert everything to seconds
        hours = int(hours) * 60 * 60
        minutes = int(minutes) * 60
        seconds = int(seconds)
        # Converting milliseconds to seconds is usually straight forward if we assume that the millisecond is three chars long
        # Because it`s not guaranteed that the millisecond will be 3 chars long, we have to shift the decimal place with the length of the millisecond string
        milliseconds = float(milliseconds) / int('1'.ljust(len(milliseconds)+1, '0'))

        # Sum everything up and add offset
        offset_time = hours + minutes + seconds + milliseconds + (offset_in_milliseconds / 1000)
        # Covert back to hours
        offset_time = offset_time / 60 / 60

        hours = math.trunc(offset_time)
        offset_time -= hours

        # Convert to minutes
        offset_time = offset_time * 60

        minutes = math.trunc(offset_time)
        offset_time -= minutes

        # Convert to seconds
        offset_time = offset_time * 60
        seconds = math.trunc(offset_time)
        offset_time -= seconds

        # Round milliseconds to 3 decimals convert to string and remove '0.'
        milliseconds = str(round(offset_time, 3))[2:]

        return [str(hours), str(minutes), str(seconds), str(milliseconds)]