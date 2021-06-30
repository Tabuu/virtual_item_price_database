import json

import requests
from sqlalchemy.orm import declared_attr

from virtual_item_price_database import db
from virtual_item_price_database.models.steam import SteamItem
from virtual_item_price_database.models.buff import BuffItem


csgo_search_url = 'https://steamcommunity.com/market/search/render/?' \
                    'query="{steam_hash_name}"&' \
                    'start=0&' \
                    'count=1&' \
                    'sort_column=name' \
                    '&sort_dir=asc&' \
                    'appid=730&' \
                    'norender=1'


csgo_item_steam_value_association = db.Table(
    'csgo_item_steam_value_association',
    db.Model.metadata,
    db.Column('item_id', db.Integer, db.ForeignKey('csgo_item.id')),
    db.Column('value_id', db.Integer, db.ForeignKey('steam_item_value.id'))
)

csgo_item_buff_value_association = db.Table(
    'csgo_item_buff_value_association',
    db.Model.metadata,
    db.Column('item_id', db.Integer, db.ForeignKey('csgo_item.id')),
    db.Column('value_id', db.Integer, db.ForeignKey('buff_item_value.id'))
)


class CsgoItem(SteamItem, BuffItem, db.Model):
    type = db.Column(db.Unicode)
    exterior = db.Column(db.Unicode)

    def get_item_steam_value_association(self):
        return csgo_item_steam_value_association

    def get_item_buff_value_association(self):
        return csgo_item_buff_value_association

    def fetch_csgo_item_metadata(self):
        response = requests.get(csgo_search_url.format(
            market_hash_name=self.steam_hash_name
        ))
        data = json.loads(response.text)

        info = data['results'][0]

        print(data['assets'])

        # image = data['assets']['730']['2']
        #
        # try:
        #     return {
        #         'success': data['success'],
        #         'median_price': int(float(data['median_price'][0:-1].replace(',', '.')) * 100),
        #         'lowest_price': int(float(data['lowest_price'][0:-1].replace(',', '.')) * 100),
        #         'volume': int(data['volume'].replace(',', ''))
        #     }
        # except KeyError:
        #     return data

    def __init__(self, steam_hash_name, buff_goods_id, **kwargs):
        super().__init__(**kwargs)
        self.steam_hash_name = steam_hash_name
        self.buff_goods_id = buff_goods_id
        self.steam_app_id = 730
        self.name = steam_hash_name

        steam_data = self.fetch_steam_value()

        if not steam_data or not steam_data['success']:
            raise ValueError

        buff_data = self.fetch_buff_value()

        if not buff_data or not buff_data['name'] == steam_hash_name:
            raise ValueError

        self.update_steam_value(steam_data)
        self.update_buff_value(buff_data)
