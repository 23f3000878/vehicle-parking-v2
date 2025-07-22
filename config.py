import os

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'app.sqlite3')

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'THIS_is_VERY_secret_KEY;;;blahhhhblahh'