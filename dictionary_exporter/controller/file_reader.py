import _io
import logging
import re

from exception import DataException

logger = logging.getLogger('DataController')


class FileReader:

    def __init__(self):
        self._file: _io.TextIOWrapper = None
        pass

    def __del__(self):
        del self.file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, new_file):
        self._file = new_file

    @file.deleter
    def file(self):
        self.file.close()

    @staticmethod
    def get_encoding(file_path: str) -> str:
        try:
            with open(file_path, encoding='ISO-8859-1') as file:
                return file.readline()
        except Exception:
            raise DataException('Can\'t get encoding')

    def open_file(self, file_path: str):
        encoding: str = self.get_encoding(file_path).strip()
        logger.debug(f'File encoding = "{encoding}"')
        self.file = open(file_path, encoding=encoding)
        self.file.readline()

    def get_words(self):
        words_number: int = int(self.file.readline().strip())
        logger.debug(f'Number of words = "{words_number}"')
        for line_num in range(words_number):
            yield re.sub('\|.*', '', self.file.readline().strip())
