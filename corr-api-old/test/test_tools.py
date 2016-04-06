from flask.ext.testing import LiveServerTestCase
import twill

class LogicTest(LiveServerTestCase):

    def create_app(self):
        try:
            browser = twill.get_browser()
            browser.go("http://0.0.0.0:5100/")
            import api
            api.app.config['LIVESERVER_PORT'] = 5110
            api.app.config['TESTING'] = True
            api.app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': '0.0.0.0','port': 27017}
        except:
            import api
            api.app.config['LIVESERVER_PORT'] = 5100
            api.app.config['TESTING'] = True
            api.app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': '0.0.0.0','port': 27017}

        return api.app

    def setUp(self):
        # Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_Logic(self):
        
        print "This is a test to check that the api endpoints are working properly."
        # assert self.app.config['MONGODB_SETTINGS'] == {'db': 'corr-integrate', 'host': '0.0.0.0', 'port': 27017}
        browser = twill.get_browser()
        browser.go("http://0.0.0.0:%d/api/v1/project0/"%self.app.config['LIVESERVER_PORT'])
        self.assertTrue(browser.get_code() in (401, 404))

    def tearDown(self):
        del self.app
        print "Supposed to tear down the testcase."
        print "Which most likely means to clear the database of all records."
