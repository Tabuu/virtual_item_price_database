from flask import Flask
from flask_restful import Api

from virtual_item_price_database.db import db
from virtual_item_price_database.entries.market import BuffMarket


def create_app():
    application = Flask(__name__)

    # create and configure the app
    application.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///../data.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    api = Api(application)

    api.add_resource(BuffMarket, '/buff_market')

    db.init_app(application)

    return application


if __name__ == '__main__':
    create_app().run(port=5000, debug=True)
