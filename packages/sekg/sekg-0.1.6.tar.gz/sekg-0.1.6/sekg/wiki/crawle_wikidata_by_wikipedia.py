# coding=utf-8
import json
import traceback

import gevent

from sekg.wiki.WikiDataItem import WikiDataItem
from sekg.wiki.wiki_model import WikidataAndWikipediaData
import tagme


class WikidataCrawle:
    def __init__(self, mysql_session):
        self.session = mysql_session

    def crawle_wikidata(self, title):
        try:
            wikidata_and_wikipedia_data = self.session.query(WikidataAndWikipediaData).filter(
                WikidataAndWikipediaData.wikipedia_title == title).first()

            if wikidata_and_wikipedia_data and WikiDataItem.is_valid_json_string(wikidata_and_wikipedia_data.data_json):
                return

            if WikidataAndWikipediaData.is_exist_wikipedia_title(session=self.session, wikipedia_title=title):
                return
            item = WikiDataItem(None, init_at_once=False)
            item.init_wikidata_item_from_wikipedia_title(title)
            try:
                if not item.is_init:
                    return
                print(item.get_en_name())
                title = item.get_en_wiki_title()
                url = tagme.title_to_uri(title)
                item_data_json_string = json.dumps(item.source_wd_dict_json)
                if wikidata_and_wikipedia_data is None:
                    data_item = WikidataAndWikipediaData(wd_item_id=item.wd_item_id, wd_item_name=None,
                                                         data_json=item_data_json_string, wikipedia_title=title,
                                                         wikipedia_url=url, wikipedia_text=None)
                    data_item.find_or_create(session=self.session, autocommit=False)
                    return data_item
                else:
                    wikidata_and_wikipedia_data.data_json = item_data_json_string
                self.session.commit()
                return wikidata_and_wikipedia_data
            except Exception as e:
                traceback.print_exc()
        except Exception as e:
            print(e)
