from processors.processor_template import ProcessorTemplate
import re

class ProcessorSUB(ProcessorTemplate):
    def __init__(self, regex):
        ProcessorTemplate.__init__(self, regex)

    def shift(self, text, amount):
        matches = re.finditer(self._regex, text)

        for match in matches:
            try:
                # Use comma after the variable to unpack a tuple with a single element to a single variable
                frames, = match.groups()
                frames = int(frames)
                frames += amount

                text = text.replace(match[0], '{' + str(frames) + '}')
            except ValueError:
                self._show_error('Value Error', 'Something went wrong! Please try again or try another file.')

                return

        return text