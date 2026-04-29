import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DATABASE_URL')
            or 'sqlite:///' + os.path.join(basedir, 'app.db'))
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['kisildarina09@gmail.com']
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    LOG_MAX_BYTES = 10240
    LOG_BACKUP_COUNT = 10
    LOG_LEVEL = 'INGO'
