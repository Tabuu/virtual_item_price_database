from flask_restful import Resource, reqparse

import virtual_item_price_database.tasks
from virtual_item_price_database.models.buff import BuffItemValue


class BuffMarket(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('buff_goods_id', type=int, required=True)

    @staticmethod
    def get():
        data = BuffMarket.parser.parse_args()
        buff_goods_id = data['buff_goods_id']

        prices = BuffItemValue.find_price_history_by_buff_goods_id(buff_goods_id)

        if prices:
            return [price.to_dict() for price in prices], 200
        else:
            return 'Not found.', 404
