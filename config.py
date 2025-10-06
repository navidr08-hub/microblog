import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "localhost"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MS_TRANSLATOR_KEY = os.getenv("MS_TRANSLATOR_KEY")
    MS_TRANSLATOR_REGION = os.getenv('MS_TRANSLATOR_REGION')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    LANGUAGES = ['en', 'es']
    ADMINS = ['abdurrahmant507@gmail.com', 'navidrahman5@gmail.com']
    POSTS_PER_PAGE = 25
