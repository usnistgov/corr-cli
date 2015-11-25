import json

from flask.ext.api import status
import flask as fk

from api import app, check_access
from corrdb.common.models import UserModel
from corrdb.common.models import ProjectModel
from corrdb.common.models import RecordModel
from corrdb.common.models import TrafficModel
from corrdb.common.models import StatModel
import mimetypes
import json
import traceback

# from flask.ext.stormpath import user

API_VERSION = 1
API_URL = '/api/v{0}'.format(API_VERSION)

#Only redirects to pages that signify the state of the problem or the result.
#The API will return some json response at all times. 
#I will handle my own status and head and content and stamp

# @app.route(API_URL + '/public/projects', methods=['GET'])
# def public_projects():
#     if fk.request.method == 'GET':
#         projects = ProjectModel.objects()
#         summaries = [json.loads(p.summary_json()) for p in projects if not p.private]
#         return fk.Response(json.dumps({'number':len(summaries), 'projects':summaries}), mimetype='application/json')
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/users', methods=['GET'])
# def public_users():
#     if fk.request.method == 'GET':
#         users = UserModel.objects()
#         summaries = [json.loads(u.activity_json()) for u in users]
#         return fk.Response(json.dumps({'number':len(users), 'users':summaries}), mimetype='application/json')
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>', methods=['GET'])
# def public_user(user_id):
#     if fk.request.method == 'GET':
#         user = UserModel.objects(id=user_id).first_or_404()
#         return fk.Response(user.activity_json(), mimetype='application/json')
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>/project/activity/<project_name>', methods=['GET'])
# def public_activity_project(user_id, project_name):
#     if fk.request.method == 'GET':
#         project = ProjectModel.objects(name=project_name, owner=user_id).first_or_404()
#         return fk.Response(project.activity_json(), mimetype='application/json')
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>/project/pull/<project_name>', methods=['GET'])
# def public_pull_project(user_id, project_name):
#     if fk.request.method == 'GET':
#         user = UserModel.objects(id=user_id).first_or_404()
#         project = ProjectModel.objects(name=project_name, owner=user).first_or_404()
#         if not project.private:
#             return fk.Response(project.summary_json(), mimetype='application/json')
#         else:
#             return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>/record/display/<project_name>/<record_id>', methods=['GET'])
# def public_display_record(user_id, project_name, record_id):
#     if fk.request.method == 'GET':
#         user = UserModel.objects(id=user_id).first_or_404()
#         project = ProjectModel.objects(name=project_name, owner=user).first_or_404()
#         if not project.private:
#             record = RecordModel.objects.with_id(record_id)
#             return fk.Response(record.to_json(), mimetype='application/json')
#         else:
#             return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>/record/pull/<project_name>/<record_id>', methods=['GET'])
# def public_pull_record(user_id, project_name, record_id):
#     if fk.request.method == 'GET':
#         user = UserModel.objects(id=user_id).first_or_404()
#         project = ProjectModel.objects(name=project_name, owner=user).first_or_404()
#         if not project.private:
#             record = RecordModel.objects.with_id(record_id)
#             if record is not None:
#                 # print str(record)
#                 if record.image and record.image['location']:
#                     image = load_image(record)
#                     print image[1]
#                     return fk.send_file(
#                         image[0],
#                         mimetypes.guess_type(image[1])[0],
#                         as_attachment=True,
#                         attachment_filename=str(user_id)+"-"+project_name+"-"+str(record_id)+"-record.tar",
#                     )
#                 else:
#                     return fk.make_response('Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
#             else:
#                 return fk.make_response('Could not find this record.', status.HTTP_204_NO_CONTENT)
#         else:
#             return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

# @app.route(API_URL + '/public/<user_id>/record/against/<project_name>/<record_id>', methods=['POST'])
# def public_against_record(user_id, project_name, record_id):
#     if fk.request.method == 'POST':
#         user = UserModel.objects(id=user_id).first_or_404()
#         project = ProjectModel.objects(name=project_name, owner=user).first_or_404()
#         if not project.private:
#             record = RecordModel.objects.with_id(record_id)
#             if fk.request.files:
#                 try:
#                     if fk.request.files['signature']:
#                         signature_obj = fk.request.files['signature']
#                         try:
#                             report = against_handler(None, record, signature_obj)
#                         except Exception, e:
#                             print traceback.print_exc()
#                             return fk.make_response('Nothing to report. An error occured while doing the matching.', status.HTTP_204_NO_CONTENT)
#                 except Exception, e:
#                     traceback.print_exc()
#                     return fk.make_response('Nothing to report. Signature file mandatory', status.HTTP_204_NO_CONTENT)
#                 return fk.Response(report, mimetype='application/json')
#             else:
#                 return fk.make_response('Nothing to report. Signature file mandatory', status.HTTP_204_NO_CONTENT)
#         else:
#             return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)