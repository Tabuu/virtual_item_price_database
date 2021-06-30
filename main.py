# from bs4 import BeautifulSoup
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from selenium import webdriver
# from datetime import datetime as dt
#
# from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
# from sqlalchemy.orm import relationship
#
# import datetime, string, random, json, requests
#
#
# @app.route('/')
# def home():
#     return 'Hello World'
#
#
# @app.route('/create_api_key', methods=["GET"])
# def create_api_key():
#     key = APIKey(request.args.get('description'))
#     db.session.add(key)
#     db.session.commit()
#     return jsonify(key.serialize())
#
#
# @app.route('/buff', methods=["GET"])
# def buff():
#     _id = request.args.get('id')
#     key = APIKey.query.filter_by(api_key=request.args.get('api_key')).first()
#     if not key:
#         return jsonify({"message": "Invalid API key"}), 401
#
#     if not key.do_api_call():
#         db.session.commit()
#         return jsonify({"message": "Too many requests"}), 429
#
#     item = get_buff_item(_id)
#     return jsonify(item.serialize()), 200
#
#
# @app.route('/steam', methods=["GET"])
# def steam():
#     name = request.args.get('name')
#
#     key = APIKey.query.filter_by(api_key=request.args.get('api_key')).first()
#     if not key:
#         return jsonify({"message": "Invalid API key"}), 401
#
#     if not key.do_api_call():
#         db.session.commit()
#         return jsonify({"message": "Too many requests"}), 429
#
#     item = get_steam_item(name)
#
#     return jsonify(item.serialize()), 200
#
#
# def get_steam_item(name):
#     item = SteamItem.query.filter_by(item_name=name).first()
#     if not item:
#         item = SteamItem(name)
#         db.session.add(item)
#         db.session.commit()
#
#     elif item.needs_update():
#         item.update()
#         db.session.commit()
#
#     return item
#
#
# def get_buff_item(_id):
#     item = BuffItem.query.filter_by(_id=_id).first()
#     if not item:
#         item = BuffItem(_id)
#         db.session.add(item)
#         db.session.commit()
#
#     elif item.needs_update():
#         item.update()
#         db.session.commit()
#
#     return item
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
#     def consume_market_item(self, market_item):
#
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
#
