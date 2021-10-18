import sys
import getopt
import logging
from controller import DataController
from exception import *

logging.basicConfig(filename='graphomania.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s: %(name)s [%(levelname)s] - %(message)s')
logger = logging.getLogger('main')


def main(argv):
    file_path: str = ''

    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        logger.info('main.py -f <thesaurus_data_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logger.info('main.py -f <thesaurus_data_file_path>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file_path = arg

    if file_path == '':
        logger.warning('File path is empty')
        sys.exit()

    data_controller: DataController = DataController()

    try:
        data_controller.open_file(file_path)
    except DataException as e:
        logger.error(e)
        sys.exit(1)

    del data_controller


if __name__ == "__main__":
    main(sys.argv[1:])
