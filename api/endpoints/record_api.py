import json

from flask.ext.api import status
import flask as fk

from api import app, check_api, load_bundle, api_response, delete_project_files, delete_record_files, API_URL
from corrdb.common.models import UserModel
from corrdb.common.models import ProjectModel
from corrdb.common.models import RecordModel
from corrdb.common.models import RecordBodyModel
from corrdb.common.models import EnvironmentModel
from corrdb.common.models import TrafficModel
from corrdb.common.models import StatModel
from corrdb.common.tools.basic_auth import requires_auth
import traceback
import mimetypes
import datetime
import calendar

# from flask.ext.stormpath import user

# API_VERSION = 1
# API_URL = '/api/v{0}/private'.format(API_VERSION)

#Only redirects to pages that signify the state of the problem or the result.
#The API will return some json response at all times. 
#I will handle my own status and head and content and stamp
#TODO: Add an endpoint to request a bare record creation for its id: generaly for distributed codes.

@app.route(API_URL + '/<api_token>/record/push/<project_name>', methods=['POST'])
def push_record(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/push/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'POST':
            # user = UserModel.objects(email=user.email).first_or_404()
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()

            if len(project.history) > 0:
                record = RecordModel(project=project, environment=EnvironmentModel.objects.with_id(project.history[-1]))
            else:
                record = RecordModel(project=project)

            record.created_at = datetime.datetime.now()

            record.label=str(record.id)

            if fk.request.data:
                try:
                    data = json.loads(fk.request.data)

                    if len(data.get('inputs',[])) != 0:
                        record.inputs = data.get('inputs',[])
                        del data['inputs']
                    else:
                        record.inputs = []

                    if len(data.get('outputs',[])) != 0:
                        record.outputs = data.get('outputs',[])
                        del data['outputs']
                    else:
                        record.outputs = []

                    if len(data.get('dependencies',[])) != 0:
                        record.dependencies = data.get('dependencies',[])
                        del data['dependencies']
                    else:
                        record.dependencies = []

                    if len(data.get('system',{})) != 0:
                        record.system = data.get('system',{})
                        del data['system']
                    else:
                        record.system = {}

                    if len(data.get('program',{})) != 0:
                        record.program = data.get('program',{})
                        del data['program']
                    else:
                        record.program = {}

                    if data.get('status','unknown') != 'unknown':
                        record.status = data.get('status','unknown')
                        del data['status']
                    else:
                        record.status = 'unknown'

                    if data.get('access','private') != 'private':
                        record.access = data.get('access','private')
                        del data['access']
                    else:
                        record.access = 'private'

                    record.update(data)

                    today = datetime.date.today()
                    (stat, created) = StatModel.objects.get_or_create(interval="%s_%s_%s_0_0_0-%s_%s_%s_23_59_59"%(today.year, today.month, today.day, today.year, today.month, today.day))
                    if not created:
                        stat.created_at=datetime.datetime.utcnow()
                        stat.category="storage"
                        stat.periode="daily"
                        stat.traffic += 1 
                        stat.save()

                    return api_response(201, "Project record created", str(record.id))
                    # return fk.Response(str(record.id), status.HTTP_201_CREATED)
                except Exception, e:
                    return api_response(400, "Project record not created", str(traceback.print_exc()))
                    # return fk.make_response(str(traceback.print_exc()), status.HTTP_400_BAD_REQUEST)
            else:
                return api_response(204, "Project record not loaded", "No metadata provided")

        else:
            return api_response(405, "Project record not loaded", "Only POST Method accepted")
    else:
        return api_response(401, "Project record not loaded", "Unauthorized API token")

@app.route(API_URL + '/<api_token>/record/sync/<project_name>/<label>', methods=['PUT'])
def sync_record(api_token, project_name, label):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/sync/<project_name>/<record_id>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'PUT':
            # user = UserModel.objects(email=user.email).first_or_404()
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
            record, created = RecordModel.objects.get_or_create(label=label, project=project)
            if created:
                record.created_at=datetime.datetime.utcnow()
                record.save()
            print "In sync..."
            # if record.project == project:
            if fk.request.data:
                data = json.loads(fk.request.data)

                if data.get('status','unknown') != 'unknown':
                    record.status = data.get('status','unknown')
                    del data['status']
                # else:
                #     record.status = 'unknown'

                if data.get('access','private') != 'private':
                    record.access = data.get('access','private')
                    del data['access']
                # else:
                #     record.access = 'private'

                if len(data.get('inputs',[])) != 0:
                    for inp in data.get('inputs',[]):
                        already = False

                        for current in record.inputs:
                            if cmp(current, inp) == 0:
                                already = True
                                break

                        if not already:
                            record.inputs.append(inp)
                    del data['inputs']

                if len(data.get('outputs',[])) != 0:
                    for out in data.get('outputs',[]):
                        already = False

                        for current in record.outputs:
                            if cmp(current, out) == 0:
                                already = True
                                break

                        if not already:
                            record.outputs.append(out)
                    del data['outputs']

                if len(data.get('dependencies',[])) != 0:
                    for dep in data.get('dependencies',[]):
                        already = False

                        for current in record.dependencies:
                            if cmp(current, dep) == 0:
                                already = True
                                break

                        if not already:
                            record.dependencies.append(dep)
                    del data['dependencies']

                if len(data.get('system',{})) != 0:
                    record.system = data.get('system',{})
                    del data['system']

                if len(data.get('program',{})) != 0:
                    record.program = data.get('program',{})
                    del data['program']

                record.update(data)
            if fk.request.files:
                try:
                    if fk.request.files['data']:
                        data_obj = fk.request.files['data']
                        data = json.loads(data_obj.read())

                        if data.get('status','unknown') != 'unknown':
                            record.status = data.get('status','unknown')
                            del data['status']
                        else:
                            record.status = 'unknown'

                        if len(data.get('inputs',[])) != 0:
                            for inp in data.get('inputs',[]):
                                already = False

                            for current in record.inputs:
                                if cmp(current, inp) == 0:
                                    already = True
                                    break

                            if not already:
                                record.inputs.append(inp)
                            del data['inputs']

                        if len(data.get('outputs',[])) != 0:
                            for out in data.get('outputs',[]):
                                already = False

                            for current in record.outputs:
                                if cmp(current, out) == 0:
                                    already = True
                                    break

                            if not already:
                                record.outputs.append(out)
                            del data['outputs']

                        if len(data.get('dependencies',[])) != 0:
                            for dep in data.get('dependencies',[]):
                                already = False

                            for current in record.dependencies:
                                if cmp(current, dep) == 0:
                                    already = True
                                    break

                            if not already:
                                record.dependencies.append(dep)
                            del data['dependencies']

                        if len(data.get('system',{})) != 0:
                            record.system = data.get('system',{})
                            del data['system']

                        if len(data.get('program',{})) != 0:
                            record.program = data.get('program',{})
                            del data['program']

                        record.update(data)
                except:
                    pass
            return api_response(201, "Project record synchronized", str(record.id))
        else:
            return api_response(405, "Project record not synchronized", "Only PUT Method accepted")
    else:
        return api_response(401, "Project record not synchronized", "Unauthorized API token")
        # return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

#Delete this if the pull with the / at the end really pulls all the project activity.
@app.route(API_URL + '/<api_token>/record/pull/<project_name>', methods=['GET'])
def pull_record_all(api_token, project_name):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/pull/<project_name>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
            records = [json.loads(record.summary_json()) for record in RecordModel.objects(project=project)]
            return api_response(200, "Project record pulled", {'project':project.to_json(), 'records':records})
            # return fk.Response(json.dumps({'project':project.to_json(), 'records':records}), mimetype='application/json')
        else:
            return api_response(405, "Project record not pulled", "Only GET Method accepted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project dashboard not loaded", "Unauthorized API token")
        # return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/record/display/<project_name>/<record_id>', methods=['GET'])
def pull_record_single(api_token, project_name, record_id):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/display/<project_name>/<record_id>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            # user = UserModel.objects(email=user.email).first_or_404()
            record = RecordModel.objects.with_id(record_id)
            project = ProjectModel.objects.with_id(record.project.id)
            if (project.access != 'public' and (project.owner == current_user)) or (project.access == 'public'):
                # if record_id is not None:
                return api_response(200, "Project record displayed", json.loads(record.to_json))
            else:
                return api_response(401, "Project record not displayed", "Unauthorized access")
                # return fk.Response('Record pull rejected.', status.HTTP_401_UNAUTHORIZED)
        else:
            return api_response(405, "Project record not displayed", "Only GET Method accepted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project record not displayed", "Unauthorized API token")
        # return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/record/pull/<project_name>/<record_id>', methods=['GET'])
def pull_record(api_token, project_name, record_id):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/pull/<project_name>/<record_id>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_api(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            # user = UserModel.objects(email=user.email).first_or_404()
            record = RecordModel.objects.with_id(record_id)
            project = ProjectModel.objects.with_id(record.project.id)
            if (project.access != 'public' and (project.owner == current_user)) or (project.access == 'public'):
                # if record_id is not None:
                if record.environment:
                    environment = record.environment
                    if environment.bundle['location']:
                        bundle = load_bundle(environment)
                        print bundle[1]
                        return fk.send_file(
                            bundle[0],
                            mimetypes.guess_type(bundle[1])[0],
                            as_attachment=True,
                            attachment_filename=str(current_user.id)+"-"+project_name+"-"+str(record_id)+"-record.%s"%bundle[1].split('.')[1],
                        )
                    else:
                        return api_response(204, "Project record download failed", "Empty location")
                        # return fk.make_response('Empty location. Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
                else:
                    return api_response(204, "Project record download failed", "No environment bundle")
                    # return fk.make_response('No environment bundle. Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
                # else:
                #     return api_response(204, "Project record download failed", "No corresponding record")
                    # return fk.make_response('Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
            else:
                return api_response(401, "Project record download failed", "Access denied. Project/Record must be private")
                # return fk.Response('Record pull rejected.', status.HTTP_401_UNAUTHORIZED)
        else:return api_response(405, "Project record download failed", "Only GET Method accepted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project record download failed", "Unauthorized API token")
        # return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)