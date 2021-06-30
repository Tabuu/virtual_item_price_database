from setuptools import setup

setup(
    name='virtual_item_price_database',
    packages=['virtual_item_price_database'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'selenium',
        'bs4',
        'requests',
        'sqlalchemy',
    ]
)
