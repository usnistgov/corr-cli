import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '33stanlake#'

DEBUG = True

APP_TITLE = 'Cloud of Reproducible Record cloud service'

VERSION = '0.1-dev'

MONGODB_SETTINGS = {
    'db': 'corr-production',
    'host': '0.0.0.0',
    'port': 27017
}

STORMPATH_API_KEY_FILE = 'apiKey.properties'
STORMPATH_APPLICATION = 'sumatra-cloud'
STORMPATH_REDIRECT_URL = '/cloud'


