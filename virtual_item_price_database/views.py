from flask import request, jsonify
from virtual_item_price_database import app, db
from virtual_item_price_database.models import csgo, buff


@app.route('/')
def home():
    item = csgo.CsgoItem("Gamma Case", 34989)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 200


@app.route('/register')
def register_item():
    buff_goods_id = request.args.get('buff_goods_id')
    steam_hash_name = request.args.get('steam_hash_name')

    item = csgo.CsgoItem.query.filter_by(
        steam_hash_name=steam_hash_name,
        buff_goods_id=buff_goods_id
    ).first()

    if item:
        return {'message': 'Item already exists'}, 200

    try:
        item = csgo.CsgoItem(steam_hash_name, buff_goods_id)
        db.session.add(item)
        db.session.commit()

        return jsonify(item.to_dict()), 200
    except ValueError:
        return {'message': 'Invalid parameters'}, 418


@app.route('/item/csgo/<steam_hash_name>')
def get_item_by_name(steam_hash_name):
    item = csgo.CsgoItem.query.filter_by(steam_hash_name=steam_hash_name).first()
    return jsonify(item.to_dict()), 200


@app.route('/market/buff/<buff_goods_id>')
def get_item_by_buff_id(buff_goods_id):
    values = buff.BuffItemValue.query.filter_by(buff_goods_id=buff_goods_id).all()
    return jsonify([item.to_dict() for item in values]), 200


@app.route('/debug/drop_all_tables')
def drop_all():
    db.drop_all()
    db.create_all()
    return jsonify({'message': 'success'}), 200
