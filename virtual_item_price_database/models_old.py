# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.orm import declared_attr
#
# from virtual_item_price_database import db
# from datetime import datetime as dt
# from selenium import webdriver
# from bs4 import BeautifulSoup
#
# import json, requests, string, random, datetime, re
#
#
# class ItemValue(db.Model):
#     __abstract__ = True
#     id = db.Column(db.Integer, primary_key=True)
#     lowest_price = db.Column(db.Integer)
#     timestamp = db.Column(db.DateTime, default=dt.utcnow())
#
#     @declared_attr
#     def item_id(self):
#         return db.Column(db.Integer, db.ForeignKey('item.id'))
#
#     @declared_attr
#     def __tablename__(self):
#         return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()
#
#
# class SteamItemValue(ItemValue, db.Model):
#     median_price = db.Column(db.Integer)
#     volume = db.Column(db.Integer)
#
#     @property
#     def serialize(self):
#         return {
#             'lowest_price': self.min_sell_price,
#             'median_price': self.median_sell_price,
#             'volume': self.sell_volume,
#             'timestamp': self.timestamp
#         }
#
#
# class BuffItemValue(ItemValue, db.Model):
#     reference_price = db.Column(db.Integer)
#
#     @property
#     def serialize(self):
#         return {
#             'lowest_price': self.min_sell_price,
#             'reference_price': self.reference_price,
#             'timestamp': self.timestamp
#         }
#
#
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     buff_id = db.Column(db.Integer, unique=True)
#     buff_value_history = db.relationship(
#         'BuffItemValue',
#         order_by='desc(temValue.timestamp)',
#         backref='item',
#         lazy='dynamic'
#     )
#
#     steam_id = db.Column(db.Unicode, unique=True)
#     steam_value_history = db.relationship(
#         'SteamItemValue',
#         order_by='desc(ItemValue.timestamp)',
#         backref='item',
#         lazy='dynamic'
#     )
#
#     @property
#     def serialize_buff_value_history(self):
#         return [item.serialize for item in self.buff_value_history[0:6]]
#
#     @property
#     def serialize_steam_value_history(self):
#         return [item.serialize for item in self.steam_value_history[0:6]]
#
#     @hybrid_property
#     def last_buff_value(self):
#         buff_values = self.buff_value_history
#         if buff_values.count() <= 0:
#             return None
#
#         return buff_values[0].timestamp
#
#     @hybrid_property
#     def last_steam_value(self):
#         steam_values = self.steam_value_history
#         if steam_values.count() <= 0:
#             return None
#
#         return steam_values[0].timestamp
#
#     @property
#     def serialize(self):
#         return {
#             'id': self.id,
#             'buff_id': self.buff_id,
#             'steam_id': self.steam_id,
#             'buff_value_history': self.serialize_buff_value_history,
#             'steam_value_history': self.serialize_steam_value_history,
#         }
#
#     def update(self, force=False):
#         last_buff_update = self.last_buff_value
#         last_steam_update = self.last_steam_value
#
#         if force or not last_buff_update or \
#                 dt.utcnow() - last_buff_update > datetime.timedelta(hours=5):
#             new_buff_value = self.fetch_buff_value()
#             self.buff_value_history.append(new_buff_value)
#             db.session.add(new_buff_value)
#
#         if force or not last_steam_update or \
#                 dt.utcnow() - last_steam_update > datetime.timedelta(hours=5):
#             new_steam_value = self.fetch_steam_value()
#             self.steam_value_history.append(new_steam_value)
#             db.session.add(new_steam_value)
#
#         db.session.commit()
#
#     def fetch_buff_value(self):
#         options = webdriver.FirefoxOptions()
#         options.headless = True
#
#         driver = webdriver.Firefox(options=options)
#         driver.get(f'https://buff.163.com/market/goods?goods_id={self.buff_id}#tab=buying')
#
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#         ref_price_div = soup.find('div', {'class': 'detail-cont'}).find('strong', {'class': 'f_Strong'})
#         match = re.search(r"^¥\s(\d+)\.?(\d*)", ref_price_div.text)
#         ref_price = int(match.group(1) + match.group(2).ljust(2, '0'))
#
#         price_text = soup.find("table", {"class": "list_tb"}).find_all("tr")[1].find('p', {'class': 'hide-cny'})
#         price = int(float(price_text.text[3:-1]) * 100)
#
#         item_value = BuffItemValue(min_sell_price=price, reference_price=ref_price)
#
#         driver.close()
#
#         return item_value
#
#     def fetch_steam_value(self):
#         response = requests.get(
#             f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={self.steam_id}")
#         data = json.loads(response.text)
#
#         median_price = int(float(data['median_price'][0:-1].replace(',', '.')) * 100)
#         lowest_price = int(float(data['lowest_price'][0:-1].replace(',', '.')) * 100)
#         volume = int(data['volume'].replace(',', ''))
#
#         item_value = SteamItemValue(min_sell_price=lowest_price, median_sell_price=median_price, sell_volume=volume)
#
#         return item_value
#
#
# class APIKey(db.Model):
#     api_key = db.Column(db.String(64), primary_key=True, unique=True)
#     description = db.Column(db.String(64), default="")
#
#     limit_cache_calls = db.Column(db.Integer, default=1000)
#     limit_steam_calls = db.Column(db.Integer, default=100)
#     limit_buff_calls = db.Column(db.Integer, default=50)
#
#     limit_refresh_interval = db.Column(db.Interval, default=datetime.timedelta(hours=1))
#     last_limit_refresh = db.Column(db.DateTime, default=dt.utcnow())
#
#     api_calls_total = db.Column(db.Integer, default=0)
#     api_calls_interval = db.Column(db.Integer, default=0)
#
#     last_api_call = db.Column(db.DateTime, default=dt.utcnow())
#
#     def __init__(self, description="None"):
#         self.description = description
#         self.api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
#
#     def do_api_call(self):
#         if dt.utcnow() - self.last_refresh > datetime.timedelta(hours=1):
#             self.last_refresh = dt.utcnow()
#             self.hourly_api_calls = 0
#
#         if self.hourly_limit and self.hourly_limit <= self.hourly_api_calls:
#             return False
#
#         self.hourly_api_calls += 1
#         self.last_api_call = dt.utcnow()
#         return True
#
#     def serialize(self):
#         return {"description": self.description, "key": self.api_key, "hourly_limit": self.hourly_limit}
#
#
# db.create_all()
