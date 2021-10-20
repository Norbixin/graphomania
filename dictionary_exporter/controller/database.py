import configparser
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *

logger = logging.getLogger('DatabaseController')


class DatabaseController:

    def __init__(self):
        con_str = self.create_con_str()
        logger.debug(f'Connection string = "{con_str}"')
        self._engine = create_engine(con_str)

    def __del__(self):
        self._engine.dispose()

    @staticmethod
    def create_con_str() -> str:
        config = configparser.ConfigParser()
        config.read('conf.ini')
        return 'mysql+mysqldb://' + config['mysql']['user'] + \
               ':' + config['mysql']['password'] + \
               '@' + config['mysql']['host'] + \
               '/' + config['mysql']['db']

    def insert_word(self, word: str, language: str):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Inserting word: {word}')
        word = Word(word=word, language=language)
        session.add(word)
        try:
            session.commit()
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()
