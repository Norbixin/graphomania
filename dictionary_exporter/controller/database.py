import configparser
import logging
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from model import *
from exception import *

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

    def get_synonym_id(self, word_id: int, synonym_id: int, meaning_group: int) -> int:
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Searching for word_id = "{word_id}", synonym_id = "{synonym_id}", ' +
                     f'meaning_group = "{meaning_group}"')
        try:
            row = session.query(Synonym.id).filter(Synonym.word_id == word_id,
                                                   Synonym.synonym_id == synonym_id,
                                                   Synonym.meaning_group == meaning_group).first()
            if row is None:
                raise DBException(f'Can\'t find word_id = "{word_id}", synonym_id = "{synonym_id}", ' +
                                  f'meaning_group = "{meaning_group}" in database')
            return row.id
        except DBException as dbe:
            raise dbe
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()

    def get_word_id(self, word: str, language: str) -> int:
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Searching for word = "{word}", language = "{language}"')
        try:
            row = session.query(Word.id).filter(Word.word == word).first()
            if row is None:
                raise DBException(f'Can\'t find word = "{word}", language = "{language}", in database')
            return row.id
        except DBException as dbe:
            raise dbe
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()

    def insert_word(self, word: str, language: str):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Inserting word = "{word}", language = "{language}"')
        word_dao = Word(word=word, language=language)
        session.add(word_dao)
        try:
            session.commit()
            return word_dao.id
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()

    def insert_synonym(self, word_id: int, synonym_id: int, meaning_group: int) -> int:
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Inserting synonym relation for word_id = "{word_id}", synonym_id = "{synonym_id}", ' +
                     f'meaning_group = "{meaning_group}"')
        synonym_dao = Synonym(word_id=word_id, synonym_id=synonym_id, meaning_group=meaning_group)
        session.add(synonym_dao)
        try:
            session.commit()
            logger.debug(f'Synonym id = "{synonym_dao.id}"')
            return synonym_dao.id
        except exc.IntegrityError:
            raise DBException(f'Synonym relation for word_id = "{word_id}", synonym_id = "{synonym_id}", ' +
                              f'meaning_group = "{meaning_group}" already exists in database')
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()

    def insert_type(self, synonym_id: int, word_type: str):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        logger.debug(f'Inserting synonym type = "{word_type}" for synonym_id = "{synonym_id}"')
        word_type_dao = WordType(synonym_id=synonym_id, type=word_type)
        session.add(word_type_dao)
        try:
            session.commit()
        except exc.IntegrityError:
            raise DBException(f'Type = "{word_type}" for synonym_id = "{synonym_id}" already exists in database')
        except Exception as e:
            logger.warning(e)
            session.rollback()
        finally:
            session.close()
