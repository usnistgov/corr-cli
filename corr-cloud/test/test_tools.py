from flask.ext.testing import LiveServerTestCase
import twill

class LogicTest(LiveServerTestCase):

    def create_app(self):
        try:
            browser = twill.get_browser()
            browser.go("http://0.0.0.0:5000/")
            import cloud
            cloud.app.config['LIVESERVER_PORT'] = 5010
            cloud.app.config['TESTING'] = True
            cloud.app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': '0.0.0.0','port': 27017}
        except:
            import cloud
            cloud.app.config['LIVESERVER_PORT'] = 5000
            cloud.app.config['TESTING'] = True
            cloud.app.config['MONGODB_SETTINGS'] = {'db': 'corr-integrate','host': '0.0.0.0','port': 27017}
            
        return cloud.app

    def setUp(self):
        # Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_Logic(self):
        # time.sleep(30)
        browser = twill.get_browser()
        browser.go("http://0.0.0.0:%d/"%self.app.config['LIVESERVER_PORT'])
        self.assertTrue(browser.get_code() in (200, 201))
        html = browser.get_html()
        # self.assertTrue(html.count('slashdot') > 150)
        print "This is a test to check that the api endpoints are working properly."

    def tearDown(self):
        del self.app
        print "Supposed to tear down the testcase."
        print "Which most likely means to clear the database of all records."