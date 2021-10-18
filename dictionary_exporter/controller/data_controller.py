import _io
import logging

from exception import DataException

logger = logging.getLogger('DataController')


class DataController:

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
