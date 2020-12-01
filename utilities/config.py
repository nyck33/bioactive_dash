import configparser
import os
from sqlalchemy import create_engine
import pymysql

#config = configparser.ConfigParser()
#config.read('config.txt')

#engine = create_engine(config.get('database', 'con'))
# echo=True show SQL in console
config_str = "mysql+pymysql://root:tennis33@localhost/dashcnf?charset=utf8mb4"
engine = create_engine(config_str, echo=True)

'''
conn=pymysql.connect(host='localhost',
                     user='root',
                     password='tennis33',
                     db='dashcnf')
'''

class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = {'username': 'root',
             #'email': 'admin',
             'password': 'tennis33'}

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None

    CSRF_ENABLES = True
    WTF_CSRF_SECRET_KEY = 'csrf key'

    # Flask-Mail settings
    # For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
    # Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    # MAIL_USERNAME = gmail_credentials[0]
    # MAIL_PASSWORD = gmail_credentials[1]
    MAIL_USERNAME = "nobu.kim66@gmail.com"
    MAIL_PASSWORD = ""
    # ADMINS = ['"Admin One" <admin@gmail.com>,]


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True
    MONGODB_HOST = os.getenv('CNF_MONGO_HOST', 'localhost')
    # for docker:
    # MONGODB_HOST = 'db'
    MONGODB_PORT = int(os.getenv('CNF_MONGO_PORT', 27017))
    # Todo: should get a dev_cnf db
    MONGODB_DB = os.getenv('CNF_MONGO_DB', 'cnf')
    # configuration from env variables, 12 factor cnf documentation
    #DEBUG = (os.getenv('CNF_DEBUG', 'True') == 'True')
    FLASK_DEBUG = DEBUG


class TestingConfig(Config):
    MONGODB_HOST = os.getenv('CNF_MONGO_HOST', 'localhost')
    #for docker:
    #MONGODB_HOST = 'db'
    MONGODB_PORT = int(os.getenv('CNF_MONGO_PORT', 27017))
    MONGODB_DB = os.getenv('CNF_MONGO_DB', 'cnf_test')  # name of db

    TESTING = (os.getenv('CNF_TESTING', 'True') == 'True')


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
    'Testing': TestingConfig,
    'default': DebugConfig
}
