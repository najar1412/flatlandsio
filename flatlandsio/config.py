"""Contains flatlandsio configution code"""

import os


# flask
SECRET_KEY = 'jkhkjhkjh23423423k4h2k3j4h'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# flask-sqlalchemy, sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///flatlands.db'

