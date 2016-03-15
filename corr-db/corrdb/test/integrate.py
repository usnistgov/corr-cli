import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '33stanlake#'

DEBUG = True
TESTING = True
LIVESERVER_PORT = 5000

APP_TITLE = 'Cloud of Reproducible Records Database'

VERSION = '0.1-dev'

MONGODB_SETTINGS = {
    'db': 'corr-integrate',
    'host': 'localhost',
    'port': 27017
}