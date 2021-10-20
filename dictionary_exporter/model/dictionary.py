from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import FetchedValue


Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    language = Column(String)
    last_updated = Column(TIMESTAMP, server_default=FetchedValue())

    def __repr__(self):
        return "<Words(word='%s', language='%s', last_updated='%s')>" % (
            self.word, self.language, self.last_updated)


class Synonym(Base):
    __tablename__ = 'synonyms'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer)
    synonym_id = Column(Integer)
    meaning_group = Column(Integer)
    last_updated = Column(TIMESTAMP, server_default=FetchedValue())

    def __repr__(self):
        return "<Words(word_id='%s', synonym_id='%s', meaning_group='%s', last_updated='%s')>" % (
            self.word_id, self.synonym_id, self.meaning_group, self.last_updated)


class WordType(Base):
    __tablename__ = 'word_types'
    id = Column(Integer, primary_key=True)
    synonym_id = Column(Integer)
    type = Column(String)
    last_updated = Column(TIMESTAMP, server_default=FetchedValue())

    def __repr__(self):
        return "<Words(synonym_id='%s', type='%s', last_updated='%s')>" % (
            self.word_id, self.type, self.last_updated)
