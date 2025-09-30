import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = "1"
    MAIL_USERNAME = "abdurrahmant507@gmail.com"
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    ADMINS = ['abdurrahmant507@gmail.com', 'navidrahman5@gmail.com']
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.getenv("MS_TRANSLATOR_KEY")
    MS_TRANSLATOR_REGION = os.getenv('MS_TRANSLATOR_REGION')