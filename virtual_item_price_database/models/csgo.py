import virtual_item_price_database.models.buff
from virtual_item_price_database.db import db
from virtual_item_price_database.models.buff import BuffItem
from virtual_item_price_database.models.steam import SteamItem


csgo_search_url = 'https://steamcommunity.com/market/search/render/?' \
                    'query="{steam_hash_name}"&' \
                    'start=0&' \
                    'count=1&' \
                    'sort_column=name' \
                    '&sort_dir=asc&' \
                    'appid=730&' \
                    'norender=1'


class CsgoItem(SteamItem, BuffItem, db.Model):
    _steam_value_association = db.Table(
        'csgo_item_steam_value_association',
        db.Model.metadata,
        db.Column('item_id', db.Integer, db.ForeignKey('csgo_item.id')),
        db.Column('value_id', db.Integer, db.ForeignKey('steam_item_value.id'))
    )

    _buff_value_association = db.Table(
        'csgo_item_buff_value_association',
        db.Model.metadata,
        db.Column('item_id', db.Integer, db.ForeignKey('csgo_item.id')),
        db.Column('value_id', db.Integer, db.ForeignKey('buff_item_value.id'))
    )

    type = db.Column(db.Unicode)
    exterior = db.Column(db.Unicode)

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

    @classmethod
    def find_least_up_to_date_item(cls):
        buff_item = cls.query.join(
            cls._buff_value_association,
            cls.id == cls._buff_value_association.c.value_id
        ).add_columns(virtual_item_price_database.models.buff.BuffItemValue.timestamp).first()

        return buff_item
