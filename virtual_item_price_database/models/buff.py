import re

from sqlalchemy.orm import declared_attr

from virtual_item_price_database import db
from virtual_item_price_database.models.abstract import Item, ItemValue

from bs4 import BeautifulSoup
from selenium import webdriver

firefox_option = webdriver.FirefoxOptions()
firefox_option.headless = False

buff_goods_page_url = "https://buff.163.com/market/goods?" \
                      "goods_id={goods_id}#" \
                      "tab={tab}"


class BuffItem(Item, db.Model):
    __abstract__ = True
    buff_goods_id = db.Column(db.Integer, unique=True)

    @declared_attr
    def buff_value_history(self):
        return db.relationship(
            'BuffItemValue',
            secondary=self.get_item_buff_value_association(self),
            order_by='desc(BuffItemValue.timestamp)',
            backref='items',
            lazy='dynamic'
        )

    def get_item_buff_value_association(self):
        pass

    def fetch_buff_value(self):
        driver = webdriver.Firefox(options=firefox_option)
        try:
            driver.get(buff_goods_page_url.format(
                goods_id=self.buff_goods_id,
                tab='buying'  # To get buy price
            ))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            cru_goods_text = soup.find('span', {'class': 'cru-goods'}).text

            ref_price_div = soup.find('div', {'class': 'detail-cont'}).find('strong', {'class': 'f_Strong'})
            match = re.search(r"^¥\s(\d+)\.?(\d*)", ref_price_div.text)
            ref_price = int(match.group(1) + match.group(2).ljust(2, '0'))

            price_text = soup.find("table", {"class": "list_tb"}).find_all("tr")[1].find('p', {'class': 'hide-cny'})
            min_sell_price = int(float(price_text.text[3:-1]) * 100)

        except Exception:
            return None

        finally:
            driver.close()

        return {
            'name': cru_goods_text,
            'lowest_price': min_sell_price,
            'reference_price': ref_price
        }

    def update_buff_value(self, data=None):
        if not data:
            data = self.fetch_buff_value()

        try:
            new_value = BuffItemValue(
                buff_goods_id=self.buff_goods_id,
                lowest_price=data['lowest_price'],
                reference_price=data['reference_price']
            )

            self.buff_value_history.append(new_value)
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
            'buff_goods_id': self.buff_goods_id,
            'buff_value_history': [value.to_dict() for value in self.buff_value_history[0:5]]
        }}


class BuffItemValue(ItemValue, db.Model):
    buff_goods_id = db.Column(db.Integer)
    reference_price = db.Column(db.Integer)

    def to_dict(self):
        return {**super().to_dict(), **{
            'reference_price': self.reference_price,
        }}
