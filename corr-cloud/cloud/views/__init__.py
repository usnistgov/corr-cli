from cloud import app
import flask as fk
import dashboard_cloud
# import project_view
# import record_view
import user_cloud
import project_cloud
import record_cloud
import diff_cloud

#Only redirects to pages that signify the state of the problem or the result.
#The API will return some json response at all times. 
#I will handle my own status and head and content and stamp

# @app.route('/')
# @app.route('/index')
# def index_view():
#     return fk.render_template('index.html')

# @app.route('/learn')
# def learn_view():
#     return fk.redirect(fk.url_for('index_view'))



