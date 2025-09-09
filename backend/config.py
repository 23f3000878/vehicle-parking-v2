import os
from celery.schedules import crontab
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'app.sqlite3')

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'THIS_IS_VERY_SECRET_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=45)
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_DB = 0
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_ENABLE_UTC = False

    CELERY_BEAT_SCHEDULE = {
    'daily-reminder-job': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=10, minute=0),  # every day at 10:00 AM
        # 'schedule': timedelta(seconds=10),  # testing
        # 'schedule': crontab(minute='*/1') # testing
    },
    'monthly-report-job': {
    'task': 'tasks.generate_all_monthly_reports',
    'schedule': crontab(day_of_month=1, hour=0, minute=0) # First day of every month
    }

    }
    EXPORT_DIR = './exports'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@gmail.com'
    MAIL_PASSWORD = 'drre ykwk rayz ldnf'
    MAIL_DEFAULT_SENDER = 'your-mail@gmail.com'
