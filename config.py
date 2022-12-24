import os

basedir = os.path.abspath(os.path.dirname(__file__))
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
CHARSET = os.environ.get('CHARSET')


class BaseConfig:
    # SQLALCHEMY config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = 'dev'
    DEBUG = True
    DATABASE = 'world_cup'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USER, PASSWORD, HOST, PORT, DATABASE, CHARSET)
    SQLALCHEMY_DATABASE_URI = DB_URI


class TestingConfig(BaseConfig):
    SECRET_KEY = 'test'
    DB_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/world_cup_test?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = DB_URI


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE = 'world_cup'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USER, PASSWORD, HOST, PORT, DATABASE, CHARSET)
    SQLALCHEMY_DATABASE_URI = DB_URI


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}