from flask_caching import Cache
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
cache = Cache()
celery = Celery()