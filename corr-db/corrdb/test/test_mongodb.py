from pymongo import MongoClient
from corrdb.common.core import setup_app
from flask.ext.testing import TestCase
import time
import twill

class MongodbTest(TestCase):

    def create_app(self):
        try:
            browser = twill.get_browser()
            browser.go("http://localhost:5200/")
            app = setup_app(__name__, 'corrdb.test.integrate')
            app.config['LIVESERVER_PORT'] = 5210
            app.config['TESTING'] = True
            app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': 'localhost','port': 27017}
        except:
            app = setup_app(__name__, 'corrdb.test.integrate')
            app.config['LIVESERVER_PORT'] = 5200
            app.config['TESTING'] = True
            app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': 'localhost','port': 27017}
        return app

    def setUp(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['corr-integrate'] 
        self.user_collection = self.db['usermodel']
        self.project_collection = self.db['projectmodel']
        self.record_collection = self.db['recordmodel']
        # Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_Mongodb(self):

        print "This is a test to check that the api endpoints are working properly."
        # time.sleep(30)
        browser = twill.get_browser()
        browser.go("http://localhost:27017/")
        self.assertTrue(browser.get_code() in (200, 201))

    def test_MongodbRest(self):

        print "This is a test to check that the api endpoints are working properly."
        # time.sleep(30)
        browser = twill.get_browser()
        browser.go("http://localhost:28017/")
        self.assertTrue(browser.get_code() in (200, 201))

    def tearDown(self):
        print "Supposed to tear down the testcase."
        print "Which most likely means to clear the database of all records."