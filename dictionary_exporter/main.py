import sys
import getopt
from controller import *
from exception import *

config = configparser.ConfigParser()
config.read('conf.ini')
logging.basicConfig(filename=config['logging']['file'],
                    filemode='w',
                    level=config['logging']['level'],
                    format=config['logging']['format'])
logger = logging.getLogger('Main')


def get_word_id(word: str, language: str, db_controller: DatabaseController) -> int:
    try:
        word_id = db_controller.get_word_id(word, language)
    except DBException as dbe:
        logger.debug(dbe)
        word_id = db_controller.insert_word(word=word, language=language)
    logger.debug(f'Word id = "{word_id}"')

    return word_id


def insert_synonym(word_id: int, synonym_word_id: int, meaning_group: int, db_controller: DatabaseController) -> int:
    try:
        synonym_id = db_controller.insert_synonym(word_id, synonym_word_id, meaning_group)
    except DBException as dbe:
        logger.debug(dbe)
        synonym_id = db_controller.get_synonym_id(word_id, synonym_word_id, meaning_group)
    logger.debug(f'Synonym id = "{synonym_id}"')

    return synonym_id


def insert_synonyms(file_path: str, language: str):
    logger.info('Started inserting synonyms')
    dict_reader: DictReader = DictReader()

    try:
        dict_reader.open_file(file_path)
    except DataException as e:
        logger.error(e)
        sys.exit(1)

    db_controller = DatabaseController()

    for word, meaning_groups in dict_reader.get_word_with_meaning_groups():
        logger.debug(f'Word = "{word}", number of meaning groups = "{meaning_groups}"')
        word_id = get_word_id(word, language, db_controller)
        for meaning_group_idx in range(int(meaning_groups)):
            for synonym, types in dict_reader.get_synonym_with_types():
                logger.debug(f'Synonym = "{synonym}", types = "{types}"')
                synonym_word_id = get_word_id(synonym, language, db_controller)
                synonym_id = insert_synonym(word_id, synonym_word_id, meaning_group_idx, db_controller)
                for word_type in types:
                    try:
                        db_controller.insert_type(synonym_id, word_type)
                    except DBException as dbe:
                        logger.debug(dbe)

    logger.info('Finished inserting synonyms')


def main():
    file_path = config['dictionary']['file']
    language = config['dictionary']['language']

    insert_synonyms(file_path, language)


if __name__ == "__main__":
    main()
