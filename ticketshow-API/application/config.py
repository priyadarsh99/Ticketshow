#config file which stores various configurations for further use
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "ticketShow@admin.com"
SENDER_PASSWORD = ""

class Config():
    DEBUG = False 
    SQLITE_DB_DIR = None 
    SQLALCHEMY_DATABASE_URI = None 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    UPLOAD_FOLDER = ''
    JWT_SECRET_KEY = 'pd'

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR,'master-db.db') #connecting database to python
    DEBUG = False 

    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKENED = 'redis://localhost:6379/2'
    #CELERY_REDIS_USERNAME = 'priyadarsh'
    #CELERY_REDIS_PASSWORD = pd99'
    CELERY_TIMEZONE = 'Asia/Kolkata'

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_URL = "redis://localhost:6379"
    CACHE_DEFAULT_TIMEOUT = 150


