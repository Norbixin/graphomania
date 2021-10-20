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


def insert_words(file_path: str, language: str):
    logger.info('Started inserting words from idx file')
    dict_idx_reader: DictIdxReader = DictIdxReader()

    try:
        dict_idx_reader.open_file(file_path)
    except DataException as e:
        logger.error(e)
        sys.exit(1)

    db_controller = DatabaseController()

    for word in dict_idx_reader.get_words():
        db_controller.insert_word(word, language)

    del db_controller
    del dict_idx_reader
    logger.info('Finished inserting words from idx file')


def main(argv):
    idx_file_path = ''
    data_file_path = ''
    language = ''

    try:
        opts, args = getopt.getopt(argv, "hi:d:l:", ["index-file=", "data-file=", "language="])
    except getopt.GetoptError:
        logger.warning('main.py -i, --index-file= <index_file_path> '
                       '-d, --data-file= <data_file_path> -l, --language= <language>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logger.warning('main.py -i, --index-file= <index_file_path> '
                           '-d, --data-file= <data_file_path> -l, --language= <language>')
            sys.exit()
        elif opt in ("-i", "--index-file"):
            idx_file_path = arg
        elif opt in ("-d", "--data-file"):
            data_file_path = arg
        elif opt in ("-l", "--language"):
            language = arg

    if idx_file_path == '' or data_file_path == '' or language == '':
        logger.warning('Index and data files and language must be provided')
        sys.exit()

    insert_words(idx_file_path, language)


if __name__ == "__main__":
    main(sys.argv[1:])
