import json

from flask.ext.api import status
import flask as fk

from api import app, check_access, load_bundle, api_response, delete_project_files, delete_record_files, API_URL
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
        
    current_user = check_access(api_token)
    if current_user is not None:
        if fk.request.method == 'POST':
            # user = UserModel.objects(email=user.email).first_or_404()
            project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()

            # label = db.StringField(max_length=300)
            # created_at = db.DateTimeField(default=datetime.datetime.now())
            # updated_at = db.DateTimeField(default=datetime.datetime.now())
            # system = db.DictField() # {''}
            # program = db.DictField() # {'version_control':'git|hg|svn|cvs', 'scope':'local|remote', 'location':'hash|https://remote_version.com/repository_id'}
            # inputs = db.ListField(db.DictField()) # [{}]
            # outputs = db.ListField(db.DictField()) # [{}]
            # dependencies = db.ListField(db.DictField())# [{}]

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
                # return fk.make_response('No metadata provided.', status.HTTP_204_NO_CONTENT)
            # if fk.request.files:
            #     try:
            #         if fk.request.files['data']:
            #             data_obj = fk.request.files['data']
            #             data = json.loads(data_obj.read())

            #             if len(data.get('image',[])) != 0:
            #                 record.image = data.get('image',[])
            #                 del data['image']
            #             else:
            #                 record.image = {}
            #             print "Record Image: "+str(record.image)

            #             if len(data.get('signature',{})) != 0:
            #                 record.signature = data.get('signature',{})
            #                 del data['signature']
            #             else:
            #                 record.signature = {}
            #             print "Record Signature: "+str(record.signature)
            #             record.update(data)
            #     except:
            #         pass
            #     # if len(record.image) == 0:
            #     #     print "Image to record..."
            #     try:
            #         if fk.request.files['docker']:
            #             image_obj = fk.request.files['docker']
            #             try: 
            #                 record.save()
            #                 upload_handler(current_user, record, image_obj, 'docker')
            #                 print str(record.image)
            #             except Exception, e:
            #                 traceback.print_exc()
            #                 print "Uploading docker image failed!"

            #         if fk.request.files['binary']:
            #             image_obj = fk.request.files['binary']
            #             try: 
            #                 record.save()
            #                 upload_handler(current_user, record, image_obj, 'binary')
            #                 print str(record.image)
            #             except Exception, e:
            #                 traceback.print_exc()
            #                 print "Uploading executable image failed!"

            #         if fk.request.files['source']:
            #             image_obj = fk.request.files['source']
            #             try: 
            #                 record.save()
            #                 upload_handler(current_user, record, image_obj, 'source')
            #                 print str(record.image)
            #             except Exception, e:
            #                 traceback.print_exc()
            #                 print "Uploading source image failed!"
            #     except:
            #         pass
            #     # else:
            #     #     print "Remote link provided."

            #     # if len(record.signature) == 0:
            #     #     print "Signature to record..."
            #     try:
            #         if fk.request.files['signature']:
            #             signature_obj = fk.request.files['signature']
            #             try: 
            #                 record.save()
            #                 upload_handler(current_user, record, signature_obj, 'signature')
            #                 print str(record.signature)
            #             except Exception, e:
            #                 traceback.print_exc()
            #                 print "Uploading signature failed!"
            #     except:
            #         pass
            #     # else:
            #     #     print "Remote link provided."
            # return fk.Response(str(record.id), status.HTTP_201_CREATED)
        else:
            return api_response(405, "Project record not loaded", "Only POST Method accepted")
            # return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return api_response(401, "Project record not loaded", "Unauthorized API token")
        # return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

# @app.route(API_URL + '/<api_token>/raw/push/<project_name>', methods=['POST'])
# def push_raw(api_token, project_name):
#     current_user = check_access(api_token)
#     if current_user is not None:
#         if fk.request.method == 'POST':
#             # user = UserModel.objects(email=user.email).first_or_404()
#             project, created = ProjectModel.objects.get_or_create(name=project_name, owner=current_user)
#             record = RecordModel(project=project)
#             # record.save()

#             record.label=str(record.id)
#             record.status="started"
#             record.reason="No reason specified."
#             record.outcome="No outcome expected."

#             print record.label
#             print record.status

#             # if created:
#             if fk.request.data:
#                 try:
#                     data = json.loads(fk.request.data)
#                     if created:
#                         project.private = data.get('private', project.private)
#                         project.status = {'origin':"root"}
#                         project.description = data.get('description', "No description provided.")
#                         project.readme = data.get('readme', "No readme content to show.")
#                         del data['private']
#                         del data['status']
#                         del data['description']
#                         del data['readme']
#                         project.save()
        
#                     if len(data.get('image',[])) != 0:
#                         record.image = data.get('image',[])
#                         del data['image']
#                     else:
#                         record.image = {}
#                     print "Record Image: "+str(record.image)

#                     if len(data.get('signature',{})) != 0:
#                         record.signature = data.get('signature',{})
#                         del data['signature']
#                     else:
#                         record.signature = {}
#                     print "Record Signature: "+str(record.signature)

#                     record.update(data)

#                     print record.label
#                     print record.status
#                 except:
#                     print "No json data provided."

#             if fk.request.files:
#                 try:
#                     if fk.request.files['data']:
#                         data_obj = fk.request.files['data']
#                         data = json.loads(data_obj.read())

#                         if len(data.get('image',[])) != 0:
#                             record.image = data.get('image',[{}])
#                             del data['image']
#                         else:
#                             record.image = {}
#                         print "Record Image: "+str(record.image)

#                         if len(data.get('signature',{})) != 0:
#                             record.signature = data.get('signature',{})
#                             del data['signature']
#                         else:
#                             record.signature = {}
#                         print "Record Signature: "+str(record.signature)
#                         record.update(data)
#                 except:
#                     pass

#                 # if len(record.image) == 0:
#                 #     try:
#                 #         if fk.request.files['image']:
#                 #             image_obj = fk.request.files['image']
#                 #             try: 
#                 #                 record.save()
#                 #                 upload_handler(current_user, record, image_obj, 'record')
#                 #             except Exception, e:
#                 #                 traceback.print_exc()
#                 #                 print "Uploading image failed!"
#                 #     except Exception, e:
#                 #         traceback.print_exc()
#                 # else:
#                 #     print "Remote link provided."

#                 if fk.request.files['docker']:
#                     image_obj = fk.request.files['docker']
#                     try: 
#                         record.save()
#                         upload_handler(current_user, record, image_obj, 'docker')
#                         print str(record.image)
#                     except Exception, e:
#                         traceback.print_exc()
#                         print "Uploading docker image failed!"

#                 if fk.request.files['binary']:
#                     image_obj = fk.request.files['binary']
#                     try: 
#                         record.save()
#                         upload_handler(current_user, record, image_obj, 'binary')
#                         print str(record.image)
#                     except Exception, e:
#                         traceback.print_exc()
#                         print "Uploading executable image failed!"

#                 if fk.request.files['source']:
#                     image_obj = fk.request.files['source']
#                     try: 
#                         record.save()
#                         upload_handler(current_user, record, image_obj, 'source')
#                         print str(record.image)
#                     except Exception, e:
#                         traceback.print_exc()
#                         print "Uploading source image failed!"

#                 # if len(record.signature) == 0:
#                 try:
#                     if fk.request.files['signature']:
#                         signature_obj = fk.request.files['signature']
#                         try: 
#                             record.save()
#                             upload_handler(current_user, record, signature_obj, signature)
#                         except Exception, e:
#                             traceback.print_exc()
#                             print "Uploading signature failed!"
#                 except Exception, e:
#                     traceback.print_exc()
#                 # else:
#                 #     print "Remote link provided."
#             return fk.Response(str(record.id), status.HTTP_201_CREATED)
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/record/sync/<project_name>/<label>', methods=['PUT'])
def sync_record(api_token, project_name, label):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/sync/<project_name>/<record_id>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_access(api_token)
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
                #To handle source code versioning ourself in case.
                # try:
                #     if fk.request.files['src']:
                #         src_obj = fk.request.files['src']
                #         try: 
                #             record.save()
                #             upload_handler(current_user, record, src_obj, 'record')
                #             print str(record.src)
                #         except Exception, e:
                #             traceback.print_exc()
                #             print "Uploading image failed!"
                # except:
                #     pass
            return api_response(201, "Project record synchronized", str(record.id))
            # return fk.Response("Record synchronized.", status.HTTP_201_CREATED)
            # else:
            #     return api_response(401, "Project record not synchronized", "Unauthorized sync on another project record")
            #     return fk.Response("Record sync rejected.", status.HTTP_401_UNAUTHORIZED)
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
        
    current_user = check_access(api_token)
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

# @app.route(API_URL + '/<api_token>/<user_id>/record/clone/<project_name>/<record_id>', methods=['GET'])
# def clone_record(api_token, user_id, project_name, record_id):
#     current_user = check_access(api_token)
#     if current_user is not None:
#         if fk.request.method == 'GET':
#             owner = UserModel.objects(id=user_id).first_or_404()
#             project = ProjectModel.objects(name=project_name, owner=owner).first_or_404()
#             if not project.private:
#                 record = RecordModel.objects.with_id(record_id)
#                 clo_project = ProjectModel.objects(name=project_name, owner=current_user).first()
#                 if clo_project == None:
#                     clo_project = project.clone()
#                     clo_project.user = current_user
#                     clo_project.status = {'origin':str(user_id)+":"+project_name+":"+str(record_id)}
#                     clo_project.save()
#                 clo_record = RecordModel.objects.with_id(record_id)
#                 if clo_record == None or (clo_record != None and clo_record.project != clo_project):
#                     clo_record = record.clone()
#                     clo_record.project = clo_project
#                     clo_record.save()
#                     return fk.Response("Record cloned.", status.HTTP_201_CREATED)
#                 else:
#                     return fk.Response("Record already cloned!", status.HTTP_201_CREATED)
#             else:
#                 return fk.make_response('Access denied. Private project.', status.HTTP_401_UNAUTHORIZED)
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

@app.route(API_URL + '/<api_token>/record/display/<project_name>/<record_id>', methods=['GET'])
def pull_record_single(api_token, project_name, record_id):
    (traffic, created) = TrafficModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), service="api", endpoint="/record/display/<project_name>/<record_id>")
    if not created:
        traffic.interactions += 1 
        traffic.save()
        
    current_user = check_access(api_token)
    if current_user is not None:
        if fk.request.method == 'GET':
            # user = UserModel.objects(email=user.email).first_or_404()
            record = RecordModel.objects.with_id(record_id)
            project = ProjectModel.objects.with_id(record.project.id)
            if (project.access != 'public' and (project.owner == current_user)) or (project.access == 'public'):
                # if record_id is not None:
                return api_response(200, "Project record displayed", json.loads(record.to_json))
                    # return fk.Response(record.to_json(), mimetype='application/json')
                # else:
                #     project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
                #     records = [json.loads(record.summary_json()) for record in RecordModel.objects(project=project)]
                #     return api_response(200, "User project records displayed", {'project':json.loads(project.to_json()), 'records':records})
                    # return fk.Response(json.dumps({'project':project.to_json(), 'records':records}), mimetype='application/json')
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
        
    current_user = check_access(api_token)
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

#Delete this if the one remove with / at the end really delete all the records.
# @app.route(API_URL + '/<api_token>/record/remove/<project_name>', methods=['DELETE'])
# def remove_all_record(api_token, project_name):
#     current_user = check_access(api_token)
#     if current_user is not None:
#         if fk.request.method == 'DELETE':
#             # user = UserModel.objects(email=user.email).first_or_404()
#             project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
#             records = RecordModel.objects(project=project)
#             for record in records:
#                 record.delete()
#             return fk.Response("All records deleted.", status.HTTP_201_CREATED)
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

# @app.route(API_URL + '/<api_token>/record/remove/<project_name>/<record_id>', methods=['DELETE'])
# def remove_record(api_token, project_name, record_id):
#     current_user = check_access(api_token)
#     if current_user is not None:
#         if fk.request.method == 'DELETE':
#             # user = UserModel.objects(email=user.email).first_or_404()
#             project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
#             record = RecordModel.objects.with_id(record_id)
#             if record.project == project:
#                 if record_id is not None:
#                     record.delete()
#                     return fk.Response("Record deleted.", status.HTTP_201_CREATED)
#                 else:
#                     records = RecordModel.objects(project=project)
#                     for record in records:
#                         record.delete()
#                     return fk.Response("All records deleted.", status.HTTP_201_CREATED)
#             else:
#                 return fk.Response("Record delete rejected.", status.HTTP_401_UNAUTHORIZED)
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)

# @app.route(API_URL + '/<api_token>/record/dashboard/<project_name>', methods=['GET'])
# def dashboard_record(api_token, project_name):
#     current_user = check_access(api_token)
#     if current_user is not None:
#         if fk.request.method == 'GET':
#             project = ProjectModel.objects(name=project_name, owner=current_user).first_or_404()
#             records = [json.loads(record.summary_json()) for record in RecordModel.objects(project=project)]
#             return fk.Response(json.dumps({'project':project.to_json(), 'records':records}), mimetype='application/json')
#         else:
#             return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
#     else:
#         return fk.Response('Unauthorized api token.', status.HTTP_401_UNAUTHORIZED)