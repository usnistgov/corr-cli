import json

from flask.ext.api import status
import flask as fk

from api import app, check_api, upload_bundle, api_response, delete_project_files, delete_record_files, API_URL
from corrdb.common.models import ProjectModel
from corrdb.common.models import EnvironmentModel
from corrdb.common.models import UserModel
from corrdb.common.models import RecordModel
from corrdb.common.models import TrafficModel
from corrdb.common.models import StatModel

from hurry.filesize import size

import mimetypes

import traceback

import datetime
import calendar

# from flask.ext.stormpath import user

# API_VERSION = 1
# API_URL = '/api/v{0}/private'.format(API_VERSION)

#Only redirects to pages that signify the state of the problem or the result.
#The API will return some json response at all times. 
#I will handle my own status and head and content and stamp

@app.route(API_URL + '/<api_token>/project/push/<project_name>', methods=['POST'])
def push_project(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/push/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()

    print api_token
    current_user = check_api(api_token)
    if current_user is not None:
        # user = UserModel.objects(email=user.email).first_or_404()
        if fk.request.method == 'POST': # POST to create a new one only.
            project, created = ProjectModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), name=project_name, owner=current_user)

            if created:

                # created_at = db.DateTimeField(default=datetime.datetime.now())
                # owner = db.ReferenceField(UserModel, reverse_delete_rule=db.CASCADE, required=True)
                # name = db.StringField(max_length=300, required=True)
                # description = db.StringField(max_length=10000)
                # goals = db.StringField(max_length=500)
                # private = db.BooleanField(default=False)
                # history = db.ListField(db.EmbeddedDocumentField(ContainerModel))

                project.description = 'No description provided.'
                project.goals = 'No goals provided.'
                if fk.request.data:
                    data = json.loads(fk.request.data)
                    # project.private = data.get('private', True) No private anymore but access
                    project.description = data.get('description', project.description)
                    project.goals = data.get('goals', project.goals)
                    project.group = data.get('group', project.group)

                project.save()

                today = datetime.date.today()
                (stat, created) = StatModel.objects.get_or_create(interval="%s_%s_%s_0_0_0-%s_%s_%s_23_59_59"%(today.year, today.month, today.day, today.year, today.month, today.day))
                if not created:
                    stat.created_at=datetime.datetime.utcnow()
                    stat.category="storage"
                    stat.periode="daily"
                    stat.traffic += 1 
                    stat.save()

                return api_response(201, "Project created", str(project.id))
                # return fk.make_response("Project created.", status.HTTP_201_CREATED)
            else:
                return api_response(401, "Project not created", "Duplication issue or Database failure.")
                # return fk.make_response('Push refused. Project name already used.', status.HTTP_401_UNAUTHORIZED)
        else:
            return api_response(405, "Project not created", "Only POST Method allowed")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project not created", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)


@app.route(API_URL + '/<api_token>/project/sync/<project_name>', methods=['PUT', 'POST'])
def sync_project(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/sync/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()

    current_user = check_api(api_token)
    if current_user is not None:
        # user = UserModel.objects(email=user.email).first_or_404()
        if fk.request.method == 'PUT': # PUT to update an existing one only.
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
            if fk.request.data:
                data = json.loads(fk.request.data)
                project.name = data.get('name', project.name)
                project.access = data.get('access', project.access)
                project.description = data.get('description', project.description)
                project.goals = data.get('goals', project.goals)
            project.save()
            return api_response(201, "Project synchronized", str(project.id))
            # return fk.make_response('Project synchronized.', status.HTTP_201_CREATED)
        elif fk.request.method == 'POST':
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
            environment = EnvironmentModel()
            if fk.request.files:
                print "Contains some request files..."
                try:
                    if fk.request.files['data']:
                        data_obj = fk.request.files['data']
                        data = json.loads(data_obj.read())
                        print str(data)
                        # environment = {}
                        if data.get('group','unknown') != 'unknown':
                            environment.group = data.get('group', 'unknown')
                            del data['group']
                        else:
                            environment.group = 'unknown'
                        print "Project Group: "+str(environment.group)

                        if data.get('system','undefined') != 'undefined':
                            environment.system = data.get('system', 'undefined')
                            del data['system']
                        else:
                            environment.system = 'undefined'
                        print "Project System: "+str(environment.system)

                        if len(data.get('specifics',{})) != 0:
                            environment.specifics = data.get('specifics',{})
                            del data['specifics']
                        else:
                            environment.specifics = {}
                            print "Project Specifics: "+str(environment.specifics)

                        if len(data.get('version',{})) != 0:
                            environment.version = data.get('version',{})
                            del data['version']
                        else:
                            environment.version = {}
                        print "Project Version Control: "+str(environment.version)

                        if len(data.get('bundle',{})) != 0:
                            environment.bundle = data.get('bundle',{'scope':'unknown'})
                            del data['bundle']
                        else:
                            environment.bundle = {'scope':'unknown'} # unknown, local, remote
                        print "Project Image Scope: "+str(environment.bundle)
                        environment.save()
                except Exception, e:
                    return api_response(400, "Project not synchronized", str(traceback.print_exc()))
                    # return fk.make_response(str(traceback.print_exc()), status.HTTP_400_BAD_REQUEST)
                # if len(record.image) == 0:
                #     print "Image to record..."
                if environment.bundle['scope'] == 'local':
                    try:
                        #Check the quota here. image_obj.tell()
                        if fk.request.files['bundle']:
                            bundle_obj = fk.request.files['bundle']

                            if current_user.quota+bundle_obj.tell() > 5000000000:
                                return fk.make_response("You have exceeded your 5Gb of quota. You will have to make some space.", status.HTTP_403_FORBIDDEN)
                            else:
                                try: 
                                    environment.save()
                                    uploaded = upload_bundle(current_user, environment, bundle_obj)
                                    if uploaded:
                                        project.history.append(str(environment.id))
                                        print str(project.history[-1])
                                        today = datetime.date.today()
                                        (stat, created) = StatModel.objects.get_or_create(interval="%s_%s_%s_0_0_0-%s_%s_%s_23_59_59"%(today.year, today.month, today.day, today.year, today.month, today.day))
                                        if not created:
                                            stat.created_at=datetime.datetime.utcnow()
                                            stat.category="storage"
                                            stat.periode="daily"
                                            stat.traffic += bundle_obj.tell()
                                            stat.save()
                                            project.save()
                                            return api_response(200, "Bundle uploaded", str(environment.id))
                                            # return fk.make_response("Image uploaded with success.", status.HTTP_200_OK)
                                        else:
                                            return api_response(500, "Bundle not uploaded", "There was an issue adding the bundle size to the stats. A database issue???")
                                            # return fk.make_response("Could not create storage states.", status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    else:
                                        environment.delete()
                                        return api_response(500, "Bundle not uploaded", "There was an issue uploading the file. Check the storage size or boto.")
                                        # return fk.make_response("Could not upload the file.", status.HTTP_500_INTERNAL_SERVER_ERROR)
                                except Exception, e:
                                    environment.delete()
                                    return api_response(400, "Bundle not uploaded", str(traceback.print_exc()))
                                    # return fk.make_response(str(traceback.print_exc()), status.HTTP_400_BAD_REQUEST)
                    except Exception, e:
                        return api_response(400, "Bundle not uploaded", str(traceback.print_exc()))
                        # return fk.make_response(str(traceback.print_exc()), status.HTTP_400_BAD_REQUEST)
                return api_response(201, "Bundle link added", "The project is at a new staged environment remote bundle")
                # return fk.make_response('Project is at the new staged environment bundle.', status.HTTP_201_CREATED)
            else:
                return api_response(204, "Bundle not uploaded", "No environment found")
                # return fk.make_response('No environment bundle staged here.', status.HTTP_204_NO_CONTENT)
        else:
            return api_response(405, "Bundle not uploaded", "Only POST and PUT Methods allowed")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Bundle not uploaded", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

# @app.route(API_URL + '/<api_token>/<user_id>/project/clone/<project_name>', methods=['GET'])
# def clone_project(api_token, user_id, project_name):
#     current_user = check_api(api_token)
#     if current_user is not None:
#         if fk.request.method == 'GET':
#             owner = UserModel.objects(id=user_id).first_or_404()
#             project = ProjectModel.objects(name=project_name, owner=owner).first_or_404()
#             if not project.private:
#                 clo_project = ProjectModel.objects(name=project_name, owner=current_user).first()
#                 if clo_project == None:
#                     clo_project = project.clone()
#                     clo_project.owner = current_user
#                     clo_project.status = {'origin':str(user_id)+":"+project_name+":"+str(record_id)}
#                     clo_project.save()
#                 else:
#                     return fk.Response("Project already exist in your workspace!", status.HTTP_201_CREATED)
#             else:
#                 return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/project/pull', methods=['GET'])
def pull_project_all(api_token):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/pull")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            projects = ProjectModel.objects(owner=current_user)
            summaries = [json.loads(p.summary_json()) for p in projects]
            return api_response(200, "User projects pulled", {'number':len(summaries), 'projects':summaries})
            # return fk.Response(json.dumps({'number':len(summaries), 'projects':summaries}), mimetype='application/json')
        else:
            return api_response(405, "User projects not pulled", "Only GET Method allowed")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "User project not pulled", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/project/pull/<project_name>', methods=['GET'])
def pull_project(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/pull/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            # user = UserModel.objects(email=user.email).first_or_404()
            # if project_name is not None:
            project = ProjectModel.objects(name=project_name).first()
            if project == None:
                return api_response(204, "Project activate not loaded", "No project found for this name.")
                # return fk.make_response('Project not found.', status.HTTP_204_NO_CONTENT)
            else:
                return api_response(200, "Project activate loaded", project.activity_json())
                # return fk.Response(project.activity_json(), mimetype='application/json')
            # else:
            #     projects = ProjectModel.objects(owner=current_user)
            #     summaries = [p.summary_json() for p in projects]
            #     return fk.Response(json.dumps({'projects':summaries}), mimetype='application/json')
        else:
            return api_response(405, "Project activate not loaded", "Only GET Method allowed")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project activate not loaded", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/project/remove/<project_name>', methods=['DELETE'])
def remove_project(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/remove/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'DELETE':
            # user = UserModel.objects(email=user.email).first_or_404()
            # if project_name is not None:
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
            project.delete()
            return api_response(200, "Project deleted", "All the project dependencies have been deleted")
                # return fk.Response('Project deleted', status.HTTP_200_OK)
            # else:
            #     projects = ProjectModel.objects(owner=current_user)
            #     for project in projects:
            #         delete_record_files(project)
            #         delete_project_files(project)
            #         project.delete()
            #     return api_response(200, "All the user projects have been deleted", "All their dependencies also deleted")
                # return fk.Response('All projects deleted', status.HTTP_200_OK)
        else:
            return api_response(405, "Project not deleted", "Only DELETE Methode accepeted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project not deleted", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)


@app.route(API_URL + '/<api_token>/project/dashboard', methods=['GET'])
def dashboard_project(api_token):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/project/dashboard")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            projects = ProjectModel.objects(owner=current_user)
            summaries = []
            for p in projects:
                project = {"project":p.summary_json()}
                records = RecordModel.pbjects(project=p)
                project["activity"] = {"number":len(records), "records":[{"id":record.id, "created":record.created_at} for record in records]}
                summaries.append(project)
            return api_response(200, "Project dashboard loaded", {'number':len(summaries), 'projects':summaries})
            # return fk.Response(json.dumps({'number':len(summaries), 'projects':summaries}), mimetype='application/json')
        else:
            return api_response(405, "Project dashboard not loaded", "Only GET Method accepeted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(204, "Project dashboard not loaded", "Unauthorized API token")
        # return fk.make_response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)