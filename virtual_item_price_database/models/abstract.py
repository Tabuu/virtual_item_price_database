import re

from virtual_item_price_database.db import db
from sqlalchemy.orm import declared_attr
from datetime import datetime as dt


class Item(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

    @declared_attr
    def __tablename__(self):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()

    def to_dict(self):
        return {
            'name': self.name
        }


class ItemValue(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    lowest_price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=dt.utcnow())

    @declared_attr
    def __tablename__(self):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()

    def to_dict(self):
        return {
            'lowest_price': self.lowest_price,
            'timestamp': self.timestamp.__str__()
        }
