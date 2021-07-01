from setuptools import setup
from setuptools import find_packages

setup(
    name='virtual_item_price_database',
    version='1.0.0',
    description='This package is a Flask REST API for virtual item data, and market prices.',
    author='Rick van Sloten',
    author_email='rick@tabuu.nl',
    url='https://github.com/Tabuu/virtual_item_price_database',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'bs4',                  # Parsing HTML.
        'requests',             # Making JSON requests.
        'flask',                # General REST API framework.
        'flask_sqlalchemy',     # Flask version of SQLAlchemy.
        'selenium',             # Webpage renderer to scrape pages that need JavaScript rendering.
        'sqlalchemy',           # Managing the database structure, and CRUD functionality.
        'flask_restful'
    ]
)
