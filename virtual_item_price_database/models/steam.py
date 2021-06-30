import json
import requests

from virtual_item_price_database import db
from virtual_item_price_database.models.abstract import Item, ItemValue

from sqlalchemy.orm import declared_attr

steam_currency_id = 3   # EUR

steam_price_overview_url = "https://steamcommunity.com/market/priceoverview/?" \
                           "appid={app_id}&" \
                           "currency={currency}&" \
                           "market_hash_name={market_hash_name}"


class SteamItem(Item, db.Model):
    __abstract__ = True
    steam_hash_name = db.Column(db.Unicode, unique=True)
    steam_app_id = db.Column(db.Integer)

    @declared_attr
    def steam_value_history(self):
        return db.relationship(
            'SteamItemValue',
            secondary=self.get_item_steam_value_association(self),
            order_by='desc(SteamItemValue.timestamp)',
            backref='item',
            lazy='dynamic'
        )

    def get_item_steam_value_association(self):
        pass

    def fetch_steam_value(self):
        response = requests.get(steam_price_overview_url.format(
            app_id=self.steam_app_id,
            currency=steam_currency_id,
            market_hash_name=self.steam_hash_name
        ))
        data = json.loads(response.text)

        try:
            return {
                'success': data['success'],
                'median_price': int(float(data['median_price'][0:-1].replace(',', '.')) * 100),
                'lowest_price': int(float(data['lowest_price'][0:-1].replace(',', '.')) * 100),
                'volume': int(data['volume'].replace(',', ''))
            }
        except KeyError:
            return data

    def update_steam_value(self, data=None):
        if not data:
            data = self.fetch_steam_value()

        try:
            new_value = SteamItemValue(
                lowest_price=data['lowest_price'],
                median_price=data['median_price'],
                volume=data['volume']
            )

            self.steam_value_history.append(new_value)
            db.session.add(new_value)
            db.session.commit()
        except KeyError:
            pass

    def latest_buff_value(self):
        if self.buff_value_history.count() <= 0:
            return None

        return self.buff_value_history[0]

    def to_dict(self):
        return {**super().to_dict(), **{
            'steam_hash_name': self.steam_hash_name,
            'steam_app_id': self.steam_app_id,
            'steam_value_history': [value.to_dict() for value in self.steam_value_history[0:5]]
        }}


class SteamItemValue(ItemValue, db.Model):
    median_price = db.Column(db.Integer)
    volume = db.Column(db.Integer)

    def to_dict(self):
        return {**super().to_dict(), **{
            'median_price': self.median_price,
            'volume': self.volume
        }}
