# from sqlalchemy import func
#
# from virtual_item_price_database.models_old import BuffItemValue
#
#
# def update_oldest_buff_item_value():
#     distinct = BuffItemValue.query.with_entities(
#         BuffItemValue.item_id, func.max(BuffItemValue.timestamp).label('max_timestamp')
#     ).group_by(
#         BuffItemValue.item_id
#     ).distinct().subquery()
#
#     query = BuffItemValue.query.join(
#         distinct, BuffItemValue.item_id == distinct.c.item_id
#     ).filter(
#         BuffItemValue.item_id == distinct.c.item_id, BuffItemValue.timestamp == distinct.c.max_timestamp
#     )
#
#     least_up_to_date_item = query.first().item
#     least_up_to_date_item.update()
#
#     return least_up_to_date_item
