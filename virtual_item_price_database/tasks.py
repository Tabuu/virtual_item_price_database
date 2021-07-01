from sqlalchemy import func

from virtual_item_price_database.models.csgo import CsgoItem


def update_oldest_csgo_item():
    return CsgoItem.find_least_up_to_date_item()

    # distinct = BuffItemValue.query.with_entities(
    #     BuffItemValue.buff_goods_id, func.max(BuffItemValue.timestamp).label('max_timestamp')
    # ).group_by(
    #     BuffItemValue.buff_goods_id
    # ).distinct().subquery()
    #
    # query = BuffItemValue.query.join(
    #     distinct, BuffItemValue.buff_goods_id == distinct.c.buff_goods_id
    # ).filter(
    #     BuffItemValue.buff_goods_id == distinct.c.buff_goods_id, BuffItemValue.timestamp == distinct.c.max_timestamp
    # )
    #
    # least_up_to_date_item = query.first().items[0]
    # least_up_to_date_item.update_buff_value()
    #
    # return least_up_to_date_item
