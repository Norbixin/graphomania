import logging

from exception import DataException

logger = logging.getLogger('FileReader')


class DictReader:

    def __init__(self):
        self._file = None
        pass

    def __del__(self):
        del self._file

    def open_file(self, file_path: str):
        encoding = self.get_encoding(file_path).strip()
        logger.debug(f'File encoding = "{encoding}"')
        self._file = open(file_path, encoding=encoding)
        self._file.readline()

    @staticmethod
    def get_encoding(file_path: str) -> str:
        try:
            with open(file_path, encoding='ISO-8859-1') as file:
                return file.readline()
        except Exception:
            raise DataException('Can\'t get encoding')

    def get_word_with_meaning_groups(self) -> []:
        with self._file as fp:
            for line in fp:
                yield line.strip().split('|')

    def get_synonym_with_types(self) -> []:
        for synonym in self._file.readline().strip().split('|')[1:]:
            types = [cur_type.strip()[:-1] for cur_type in synonym.split('(')[1:]]
            synonym = synonym.split('(')[0].strip()
            yield synonym, types
