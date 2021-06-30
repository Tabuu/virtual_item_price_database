from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


def create_app(test_config=None):
    application = Flask(__name__, instance_relative_config=True)

    # create and configure the app
    application.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///../data.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    db.init_app(application)
    db.app = application

    return application


db = SQLAlchemy()
app = create_app()

import virtual_item_price_database.models
import virtual_item_price_database.views
import virtual_item_price_database.tasks
