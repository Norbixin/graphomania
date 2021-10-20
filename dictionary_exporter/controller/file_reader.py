import _io
import logging
import re
from abc import ABC

from exception import DataException

logger = logging.getLogger('FileReader')


class FileReader(ABC):

    def __init__(self):
        self._file = None
        pass

    def __del__(self):
        del self._file

    def open_file(self, file_path: str, encoding: str = 'UTF-8'):
        logger.debug(f'File encoding = "{encoding}"')
        self._file = open(file_path, encoding=encoding)


class DictReader(FileReader):

    def open_file(self, file_path: str):
        encoding = self.get_encoding(file_path).strip()
        super().open_file(file_path, encoding)
        self._file.readline()

    @staticmethod
    def get_encoding(file_path: str) -> str:
        try:
            with open(file_path, encoding='ISO-8859-1') as file:
                return file.readline()
        except Exception:
            raise DataException('Can\'t get encoding')


class DictIdxReader(DictReader):

    def get_words(self):
        words_number = int(self._file.readline().strip())
        logger.debug(f'Number of words = "{words_number}"')
        for line_num in range(words_number):
            yield re.sub(r'\|.*', '', self._file.readline().strip())
