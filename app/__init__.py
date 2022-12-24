import os
from config import config
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from .models import db, Admin, User, Activity
# logging config
from logging.config import dictConfig
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,  # not covering default
        "formatters": {  # output format
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",  # 控制台输出
                "level": "DEBUG",
                "formatter": "default",
            },
            "log_info_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "default",   # output format -> formatters
                "filename": "./logs/info.log",  # set storage path for logging
                "maxBytes": 20*1024*1024,   # max size 20M
                "backupCount": 10,          # max number of file: 10
                "encoding": "utf8",
            },
            "log_warning_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "WARNING",
                "formatter": "default",   # output format -> formatters
                "filename": "./logs/warning.log",  # set storage path for logging
                "maxBytes": 20*1024*1024,   # max size 20M
                "backupCount": 10,          # max number of file: 10
                "encoding": "utf8",
            },

        },
        "root": {
            "level": "DEBUG",  # # level of handler will cover this level
            "handlers": ["console", "log_info_file", "log_warning_file"],
        },
    }
)


def create_app(config_name=None):
    app = Flask(__name__)
    configure_app(app, config_name)  # import argument
    db.init_app(app)  # initialize 'app'
    migrate = Migrate(app, db)
    CORS(app, resources=r'/*')
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    # import and register blueprints
    from app.views import main_routes
    app.register_blueprint(main_routes)
    return app


def configure_app(app, config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    if config_name in config:
        app.config.from_object(config[config_name])
