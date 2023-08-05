import traceback
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, MetaData, ForeignKey, DateTime, Index, Boolean, func, Table, \
    SmallInteger, Float, or_
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_fulltext import FullText

Base = declarative_base()


class WikidataAndWikipediaData(Base):
    __tablename__ = 'wikidata_wikipedia_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wd_item_id = Column(String(32), nullable=True, index=True)
    wd_item_name = Column(String(256), nullable=True, index=True)
    wikipedia_url = Column(String(256), nullable=True, index=True)
    wikipedia_title = Column(String(128), nullable=True, index=True)
    wikipedia_text = Column(LONGTEXT(), nullable=True)
    data_json = Column(LONGTEXT(), nullable=True)

    __table_args__ = ({
        "mysql_charset": "utf8",
    })

    def __init__(self, wd_item_id, wd_item_name, wikipedia_url, wikipedia_title, wikipedia_text, data_json):
        self.wd_item_id = wd_item_id
        self.wd_item_name = wd_item_name
        self.data_json = data_json
        self.wikipedia_url = wikipedia_url
        self.wikipedia_title = wikipedia_title
        self.wikipedia_text = wikipedia_text

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance

    @staticmethod
    def is_exist_wikidata_json(session, wd_item_id):

        try:
            if wd_item_id:
                result = session.query(WikidataAndWikipediaData).filter(
                    WikidataAndWikipediaData.wd_item_id == wd_item_id).first()
                if result:
                    return True
            return False
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def is_exist_wikipedia_url(session, wikipeida_url):

        try:
            if wikipeida_url:
                result = session.query(WikidataAndWikipediaData).filter(
                    WikidataAndWikipediaData.wikipedia_url == wikipeida_url).first()
                if result:
                    return True
            return False
        except Exception:
            traceback.print_exc()
            return False
    @staticmethod
    def is_exist_wikipedia_title(session, wikipedia_title):

        try:
            if wikipedia_title:
                result = session.query(WikidataAndWikipediaData).filter(
                    WikidataAndWikipediaData.wikipedia_title == wikipedia_title).first()
                if result:
                    return True
            return False
        except Exception:
            traceback.print_exc()
            return False
    def get_remote_object(self, session):
        if self.id:
            return self
        else:
            try:
                if self.wd_item_id:
                    result = session.query(WikidataAndWikipediaData).filter(
                        WikidataAndWikipediaData.wd_item_id == self.wd_item_id).first()
                    if result:
                        return result
                if self.wikipedia_url:
                    result = session.query(WikidataAndWikipediaData).filter(
                        WikidataAndWikipediaData.wikipedia_url == self.wikipedia_url).first()

                    return result
            except Exception:
                traceback.print_exc()
                return None
