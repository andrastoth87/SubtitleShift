from processors.processor_sub import ProcessorSUB
from processors.processor_general import ProcessorGENERAL
from processors.processor_template import ProcessorTemplate

class Model:
    def __init__(self) -> None:
        self.__controller = None

        self.__subtitle_path = ''

        # Add here the supported file extensions and the regex to use to extract the timestamps, frames etc...
        self.__supported_extensions = {
            'sub': ProcessorSUB(r'{(\d+)}'),
            'srt': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ass': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ssa': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'vtt': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'scc': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'sbv': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})'),
            'ttml': ProcessorGENERAL(r'(\d{1,2}):(\d{2}):(\d{2})[,.:](\d{1,3})')
        }

    def setup(self, controller):
        self.__controller = controller

    def get_supported_extensions(self) -> list[str]:
        """ Gets the supported file formats. """
        return list(self.__supported_extensions.keys())

    def get_subtitle_path(self) -> str:
        """ Gets the path of the subtitle. """
        return self.__subtitle_path

    def get_processor(self, extension: str) -> ProcessorTemplate:
        """ Returns the processor for the extension. """
        return self.__supported_extensions.get(extension, None)

    def set_subtitle_path(self, path: str) -> None:
        """ Sets the path of the subtitle. """
        self.__subtitle_path = path