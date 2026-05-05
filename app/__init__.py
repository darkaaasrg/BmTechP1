import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch
from flask import Flask, request, has_request_context, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

def get_locale():
    if has_request_context():
        return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'en'


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) \
        if app.config['ELASTICSEARCH_URL'] else None

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        if not app.debug:
            if app.config['MAIL_SERVER']:
                auth = None
                if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                    auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                secure = None
                if app.config['MAIL_USE_TLS']:
                    secure = ()
                mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'],
                    subject='Microblog Failure',
                    credentials=auth,
                    secure=secure
                )
                mail_handler.setLevel(logging.ERROR)
                app.logger.addHandler(mail_handler)
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler(
                    'logs/microblog.log',
                    maxBytes=app.config['LOG_MAX_BYTES'],
                    backupCount=app.config['LOG_BACKUP_COUNT']
                )

                file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
                file_handler.setLevel(app.config['LOG_LEVEL'])
                app.logger.addHandler(file_handler)

    return app


from app import models


