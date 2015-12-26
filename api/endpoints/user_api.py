import json

from flask.ext.api import status
import flask as fk

from api import app, API_URL, crossdomain, check_api, check_app, api_response, s3_delete_file, s3_get_file, web_get_file, s3_upload_file, data_pop, merge_dicts, logStat, logTraffic, logAccess, prepare_env, prepare_record, prepare_project
from corrdb.common.models import UserModel
from corrdb.common.models import AccessModel
from corrdb.common.models import TrafficModel
from corrdb.common.models import FileModel
from corrdb.common.models import ProfileModel
from corrdb.common.models import StatModel
from corrdb.common.models import ProjectModel
from corrdb.common.models import RecordModel
from corrdb.common.models import RecordBodyModel
from corrdb.common.models import DiffModel
from corrdb.common.models import ApplicationModel
from corrdb.common.models import CommentModel
from corrdb.common.models import MessageModel
from corrdb.common.models import EnvironmentModel
from corrdb.common.models import BundleModel
from corrdb.common.models import VersionModel

import mimetypes
import json
import traceback
import datetime
import random
import string
import os
import thread

# logAccess(app,'root', '')

#User info
@app.route(API_URL + '/<api_token>/<app_token>/user/status', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_status(api_token, app_token):
    logTraffic(endpoint='<api_token>/<app_token>/user/status')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
        	return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '<api_token>/<app_token>/user/status')
            if fk.request.method == 'GET':
                return api_response(200, 'User %s credentials are authorized'%str(current_user.id), current_user.info())
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/connectivity', methods=['GET'])
def user_app_connectivity(api_token, app_token):
    logTraffic(endpoint='<api_token>/<app_token>/connectivity')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<app_token>/connectivity')
            if fk.request.method == 'GET':
                name = current_app.name if current_app.name != '' and current_app.name != None else 'unknown'
                return api_response(200, 'Application %s is accessible'%name, current_app.info())
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/user/search/<user_name>', methods=['GET'])
def user_search(api_token, app_token, user_name):
    logTraffic(endpoint='<api_token>/<app_token>/user/search/<user_name>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '<api_token>/<app_token>/user/search/<user_name>')
            if fk.request.method == 'GET':
                names = user_name.split('-')
                users = []
                for user in UserModel.objects():
                    exists = [False for name in names]
                    condition = [True for name in names]
                    profile = ProfileModel.objects(user=user).first()
                    index = 0
                    for name in names:
                        if name != '':
                            if name in profile.fname or name in profile.lname:
                                exists[index] = True
                        else:
                            exists[index] = True
                        index += 1
                    if exists == condition:
                        users.append(user)

                # for name in names:
                #     users_1 = ProfileModel.objects(fname__icontains=name)
                #     for pf in users_1:
                #         if pf.user not in users:
                #             users.append(pf.user)
                #     users_2 = ProfileModel.objects(lname__icontains=name)
                #     for pf in users_2:
                #         if pf.user not in users:
                #             users.append(pf.user)
                users_dict = {'total_users':len(users), 'users':[user.info() for user in users]}
                return api_response(200, 'Search results for user with name containing: %s'%user_name.split('-'), users_dict)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/user/picture', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_picture(api_token, app_token):
    logTraffic(endpoint='/<api_token>/<app_token>/user/picture')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            if fk.request.method == 'GET':
                profile = ProfileModel.objects(user=current_user).first()
                if profile == None:
                    picture_buffer = s3_get_file('picture', 'default-picture.png')
                    if picture_buffer == None:
                        return api_response(404, 'No picture found', 'We could not fetch the picture [default-picture.png].')
                    else:
                        return fk.send_file(picture_buffer, attachment_filename='default-picture.png', mimetype='image/png')
                else:
                    picture = profile.picture
                    if picture.location == 'local' and 'http://' not in picture.storage:
                        picture_buffer = s3_get_file('picture', picture.storage)
                        if picture_buffer == None:
                            return api_response(404, 'No picture found', 'We could not fetch the picture [%s].'%logo.storage)
                        else:
                            return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
                    elif picture.location == 'remote':
                        picture_buffer = web_get_file(picture.storage)
                        if picture_buffer != None:
                            return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
                        else:
                            picture_buffer = s3_get_file('picture', 'default-picture.png')
                            if picture_buffer == None:
                                return api_response(404, 'No picture found', 'We could not fetch the picture [default-picture.png].')
                            else:
                                return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
                    else:
                        # solve the file situation and return the appropriate one.
                        if 'http://' in picture.storage:
                            picture.location = 'remote'
                            picture.save()
                            picture_buffer = web_get_file(picture.storage)
                            if picture_buffer != None:
                                return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
                            else:
                                picture_buffer = s3_get_file('picture', 'default-picture.png')
                                if picture_buffer == None:
                                    return api_response(404, 'No picture found', 'We could not fetch the picture [%s].'%picture.storage)
                                else:
                                    return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
                        else:
                            picture.location = 'local'
                            picture.save()
                            picture_buffer = s3_get_file('picture', picture.storage)
                            if picture_buffer == None:
                                return api_response(404, 'No picture found', 'We could not fetch the picture [%s].'%picture.storage)
                            else:
                                return fk.send_file(picture_buffer, attachment_filename=picture.name, mimetype=picture.mimetype)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/user/home', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_home(api_token, app_token):
    logTraffic(endpoint='<api_token>/<app_token>/user/home')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '<api_token>/<app_token>/user/home')
            if fk.request.method == 'GET':
                return api_response(200, 'User %s Home'%str(current_user.id), current_user.home())
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')


# User picture:
# http://0.0.0.0:5100/api/v1/private/07366337c49a026cda30d1cb99679a1b86f7dffb9a44cf9765975a5991d6a849/dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a/user/picture

#Projects

#Records

#Environments

#Comments

#Files

#Messages
@app.route(API_URL + '/<api_token>/<app_token>/messages', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_messages(api_token, app_token):
    logTraffic(endpoint='/<api_token>/<app_token>/messages')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/messages')
            if fk.request.method == 'GET':
                messages = []
                messages.extend(MessageModel.objects(sender=current_user))
                messages.extend(MessageModel.objects(receiver=current_user))
                messages_dict = {'total_messages':len(messages), 'messages':[]}
                for message in messages:
                    messages_dict['messages'].append(message.extended())
                return api_response(200, 'Messages list', messages_dict)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/message/create', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_message_create(api_token, app_token):
    logTraffic(endpoint='/<api_token>/<app_token>/message/create')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/message/create')
            if fk.request.method == 'POST':
                if fk.request.data:
                    data = json.loads(fk.request.data)
                    receiver_id = data.get('receiver', None)
                    title = data.get('title', '')
                    content = data.get('content', '')
                    attachments = data.get('attachments', [])
                    if receiver_id == '':
                        return api_response(400, 'Missing mandatory fields', 'A message should have a receiver.')
                    else:
                        if title == '' and content == '':
                            return api_response(400, 'Missing mandatory fields', 'A message cannot have title and content empty.')
                        
                        receiver = UserModel.objects.with_id(receiver_id)
                        message, created = MessageModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), sender=current_user, receiver=receiver, title=title, attachments=attachments, content=content)
                        if receiver == None:
                            return api_response(400, 'Missing mandatory fields', 'A message should have an existing receiver.')
                        if not created:
                            # Impossible only if the time field fails
                            return api_response(200, 'Message already exists', message.info())
                        else:
                            logStat(message=message)
                            return api_response(201, 'Message created', message.info())
                else:
                    return api_response(204, 'Nothing created', 'You must provide the message information.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

@app.route(API_URL + '/<api_token>/<app_token>/message/show/<message_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_message_show(api_token, app_token, message_id):
    logTraffic(endpoint='/<api_token>/<app_token>/message/show/<message_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/message/create')
            if fk.request.method == 'GET':
                message = MessageModel.objects.with_id(message_id)
                if message == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this message.')
                else:
                    if message.sender == current_user or message.receiver == current_user:
                        return api_response(200, 'Message %s'%str(message.id), message.extended())
                    else:
                        return api_response(401, 'Unauthorized action', 'You must be part of the conversation to read it.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/message/delete/<message_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_message_delete(api_token, app_token, message_id):
    logTraffic(endpoint='/<api_token>/<app_token>/message/delete/<message_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/message/create')
            if fk.request.method == 'GET':
                message = MessageModel.objects.with_id(message_id)
                if message == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this message.')
                else:
                    if message.sender == current_user or message.receiver == current_user:
                        # Delete attachements maybe??
                        message.delete()
                        logStat(deleted=True, message=message)
                        return api_response(200, 'Deletion succeeded', 'The message %s was succesfully deleted.'%str(message.id))
                    else:
                        return api_response(401, 'Unauthorized action', 'You must be part of the conversation to read it.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/message/update/<message_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_message_update(api_token, app_token, message_id):
    logTraffic(endpoint='/<api_token>/<app_token>/message/update/<message_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/message/create')
            if fk.request.method == 'POST':
                message = MessageModel.objects.with_id(message_id)
                if message == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this message.')
                else:
                    if message.sender == current_user or message.receiver == current_user:
                        if fk.request.data:
                            data = json.loads(fk.request.data)
                            sender_id = data.get('sender', None)
                            receiver_id = data.get('receiver', None)
                            title = data.get('title', message.title)
                            content = data.get('content', message.content)
                            attachments = data.get('attachments', [])
                            sender = None
                            receiver = None
                            if sender_id == None:
                                sender = message.sender
                            else:
                                sender = UserModel.objects(session=sender_id).first()
                                if sender == None:
                                    sender = message.sender
                            if receiver_id == None:
                                receiver = message.receiver
                            else:
                                receiver = UserModel.objects.with_id(receiver_id)
                                if receiver == None:
                                    receiver = message.receiver
                            message.sender = sender
                            message.receiver = receiver
                            message.title = title
                            message.content = content
                            message.attachments.extend(attachments)
                            message.save()
                            return api_response(201, 'Message updated', message.info())
                        else:
                            return api_response(204, 'Nothing created', 'You must provide the message information.')
                    else:
                        return api_response(401, 'Unauthorized action', 'You must be part of the conversation to read it.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

# Files
@app.route(API_URL + '/<api_token>/<app_token>/files', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_files(api_token, app_token):
    logTraffic(endpoint='/<api_token>/<app_token>/files')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/files')
            if fk.request.method == 'GET':
                files = []
                for p in ProjectModel.objects(owner=current_user):
                    for rs_id in p.resources:
                        rs = FileModel.objects.with_id(rs_id)
                        if rs != None:
                            files.append(rs.info())
                    for cm_id in p.comments:
                        cm = CommentModel.objects.with_id(cm_id)
                        for at_id in cm.attachments:
                            at = FileModel.objects.with_id(at_id)
                            if at != None:
                                files.append(at.info())
                    for re in RecordModel.objects(project=p):
                        for rs_id in re.resources:
                            rs = FileModel.objects.with_id(rs_id)
                            if rs != None:
                                files.append(rs.info())
                        for cm_id in re.comments:
                            cm = CommentModel.objects.with_id(cm_id)
                            for at_id in cm.attachments:
                                at = FileModel.objects.with_id(at_id)
                                if at != None:
                                    files.append(at.info())
                    for env_id in p.history:
                        env = EnvironmentModel.objects.with_id(env_id)
                        if env != None:
                            files.append(env.bundle.info())

                    for f in FileModel.objects():
                        if f.group == 'file' and f.owner == str(current_user.id):
                            files.append(f.info())

                files_dict = {'total_files':len(files), 'files':[]}
                for _file in files:
                    files_dict['files'].append(_file)
                return api_response(200, 'Files list', files_dict)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/upload/<group>/<item_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_upload(api_token, app_token, group, item_id):
    logTraffic(endpoint='/<api_token>/<app_token>/file/upload/<group>/<item_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user == None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/upload/<group>/<item_id>')
            if fk.request.method == 'POST':
                if group not in ["input", "output", "dependencie", "file", "descriptive", "diff", "resource-record", "resource-env", "resource-app", "attach-comment", "attach-message", "picture" , "logo-project" , "logo-app" , "resource", "bundle"]:
                    return api_response(405, 'Method Group not allowed', 'This endpoint supports only a specific set of groups.')
                else:
                    if fk.request.files:
                        file_obj = fk.request.files['file']
                        filename = '%s_%s'%(item_id, file_obj.filename)
                        _file, created = FileModel.objects.get_or_create(created_at=datetime.datetime.utcnow(), name=filename)
                        if not created:
                            return api_response(200, 'File already exists with same name for this item', _file.info())
                        else:
                            encoding = ''
                            if file_obj != None:
                                old_file_position = file_obj.tell()
                                file_obj.seek(0, os.SEEK_END)
                                size = file_obj.tell()
                                file_obj.seek(old_file_position, os.SEEK_SET)
                            else:
                                size = 0
                            storage = '%s_%s'%(item_id, file_obj.filename)
                            location = 'local'
                            mimetype = mimetypes.guess_type(storage)[0]
                            group_ = group
                            description = ''
                            item = None
                            owner = None
                            if group == 'input':
                                item = RecordModel.objects.with_id(item_id)
                                owner = item.project.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is an input file for the record %s'%(file_obj.filename, str(item.id))
                            elif group == 'output':
                                item = RecordModel.objects.with_id(item_id)
                                owner = item.project.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is an output file for the record %s'%(file_obj.filename, str(item.id))
                            elif group == 'dependencie':
                                item = RecordModel.objects.with_id(item_id)
                                owner = item.project.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is an dependency file for the record %s'%(file_obj.filename, str(item.id))
                            elif group == 'descriptive':
                                item = ProjectModel.objects.with_id(item_id)
                                owner = item.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is a resource file for the project %s'%(file_obj.filename, str(item.id))
                            elif group == 'diff':
                                item = DiffModel.objects.with_id(item_id)
                                owner1 = item.sender
                                owner2 = item.targeted
                                if current_user != owner1 and current_user != owner2:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is a resource file for the collaboration %s'%(file_obj.filename, str(item.id))
                            elif 'attach' in group:
                                if 'message' in group:
                                    item = MessageModel.objects.with_id(item_id)
                                    owner1 = item.sender
                                    owner2 = item.receiver
                                    if current_user != owner1 and current_user != owner2:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is an attachement file for the message %s'%(file_obj.filename, str(item.id))
                                elif 'comment' in group:
                                    item = CommentModel.objects.with_id(item_id)
                                    owner = item.sender
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is an attachement file for the comment %s'%(file_obj.filename, str(item.id))
                                group_ = group.split('-')[0]
                            elif group == 'bundle':
                                item = BundleModel.objects.with_id(item_id)
                                env = EnvironmentModel.objects(bundle=item).first()
                                rec_temp = RecordModel.objects(environment=env).first()
                                owner = rec_temp.project.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            elif group == 'picture':
                                item = ProfileModel.objects.with_id(item_id)
                                owner = item.user
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                description = '%s is the picture file of the profile %s'%(file_obj.filename, str(item.id))
                                _file.delete()
                                _file = item.picture
                            elif 'logo' in group:
                                if 'app' in group:
                                    item = ApplicationModel.objects.with_id(item_id)
                                    owner = item.developer
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is the logo file of the application %s'%(file_obj.filename, str(item.id))
                                elif 'project' in group:
                                    item = ProjectModel.objects.with_id(item_id)
                                    owner = item.owner
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is the logo file of the project %s'%(file_obj.filename, str(item.id))
                                _file.delete()
                                _file = item.logo
                            elif 'resource' in group:
                                if 'record' in group:
                                    item = RecordModel.objects.with_id(item_id)
                                    owner = item.project.owner
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is an resource file for the record %s'%(file_obj.filename, str(item.id))
                                elif 'env' in group:
                                    item = EnvironmentModel.objects.with_id(item_id)
                                    rec_temp = RecordModel.objects(environment=item).first()
                                    owner = rec_temp.project.owner
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is a resource file for the environment %s'%(file_obj.filename, str(item.id))
                                elif 'app' in group:
                                    item = ApplicationModel.objects.with_id(item_id)
                                    owner = item.developer
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    description = '%s is a resource file for the app %s'%(file_obj.filename, str(item.id))
                                group_ = group.split('-')[0]

                            if item == None:
                                if group != 'picture' or group != 'logo':
                                    return api_response(400, 'Missing mandatory instance', 'A file should reference an existing item.')
                            else:
                                _file.description = description
                                _file.encoding = encoding
                                _file.size = size
                                # _file.path = path
                                _file.owner = current_user
                                _file.storage = storage
                                _file.location = location
                                _file.mimetype = mimetype
                                _file.group = group_
                                _file.save()
                                uploaded = s3_upload_file(_file, file_obj)
                                if not uploaded[0]:
                                    _file.delete()
                                    return api_response(500, 'An error occured', "%s"%uploaded[1])
                                else:
                                    if group == 'input':
                                        item.resources.append(str(_file.id))
                                    elif group == 'output':
                                        item.resources.append(str(_file.id))
                                    elif group == 'dependencie':
                                        item.resources.append(str(_file.id))
                                    elif group == 'descriptive':
                                        item.resources.append(str(_file.id))
                                    elif group == 'diff':
                                        item.resources.append(str(_file.id))
                                    elif group == 'bundle':
                                        _file.delete()
                                        if item.location != storage:
                                            s3_delete_file('bundle',item.location)
                                        item.encoding = encoding
                                        item.size = size
                                        item.scope = 'local'
                                        item.location = storage
                                        item.mimetype = mimetype
                                        item.save()
                                    elif 'attach' in group:
                                        item.attachments.append(str(_file.id))
                                    elif group == 'picture':
                                        if item.picture.location != storage:
                                            s3_delete_file('picture',item.picture.storage)
                                        if item != None:
                                            item.picture = _file
                                    elif 'logo' in group:
                                        if item.logo.location != storage:
                                            s3_delete_file('logo',item.logo.storage)
                                        if item != None:
                                            item.logo = _file
                                    elif 'resource' in group:
                                        item.resources.append(str(_file.id))
                                    if item != None:
                                        item.save()
                                    logStat(file_obj=_file)
                                    return api_response(201, 'New file created', _file.info())
                    else:
                        return api_response(204, 'Nothing created', 'You must provide the file information.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/download/<file_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_download(api_token, app_token, file_id):
    logTraffic(endpoint='/<api_token>/<app_token>/file/download/<file_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/download/<file_id>')
            if fk.request.method == 'GET':
                file_meta = FileModel.objects.with_id(file_id)
                if file_meta == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this file.')
                else:
                    if file_meta.owner != 'public' and file_meta.owner != str(current_user.id):
                        return api_response(401, 'Unauthorized access', 'This file is private and you are not the owner.')
                    else:
                        file_obj = None
                        if file_meta.location == 'remote':
                            file_obj = web_get_file(file_meta.storage)
                        elif file_meta.location == 'local':
                            file_obj = s3_get_file(file_meta.group, file_meta.storage)

                        if file_obj == None:
                            return api_response(404, 'Request suggested an empty response', 'No content found for this file.')
                        else:
                            # return fk.send_file(
                            #     file_obj,
                            #     file_meta.mimetype,
                            #     # as_attachment=True,
                            #     attachment_filename=file_meta.name,
                            # )
                            if file_meta.group == 'logo' or file_meta.group == 'picture':
                                return fk.send_file(
                                    file_obj,
                                    file_meta.mimetype,
                                    # as_attachment=True,
                                    attachment_filename=file_meta.name,
                                )
                            else:
                                # if file_meta.name.split('.')[1] in ['jpg', 'pdf', 'txt']:
                                #     return fk.send_file(
                                #         file_obj,
                                #         file_meta.mimetype,
                                #         # as_attachment=True,
                                #         attachment_filename=file_meta.name,
                                #     )
                                # else:
                                    # Check the mimetype for media files to just provide them without attachment.
                                return fk.send_file(
                                        file_obj,
                                        file_meta.mimetype,
                                        as_attachment=True,
                                        attachment_filename=file_meta.name,
                                    )
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/create', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_create(api_token, app_token):
    logTraffic(endpoint='/<api_token>/<app_token>/file/create')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/create')
            if fk.request.method == 'POST':
                if fk.request.data:
                    data = json.loads(fk.request.data)
                    encoding = data.get('encoding', '')
                    size = data.get('size', 0)
                    name = data.get('name', '')
                    access = data.get('access', 'public') # Allow the creation of public files.
                    storage = data.get('storage', '')
                    location = data.get('location', 'undefined')
                    mimetype = data.get('mimetype', mimetypes.guess_type(location)[0])
                    group = data.get('group', 'undefined')
                    description = data.get('description', '')
                    owner = current_user
                    if storage == '' or name == '':
                        return api_response(400, 'Missing mandatory fields', 'A file should have at least a name and a storage reference (s3 key or url).')
                    else:
                        
                        if 'http://' in storage or 'https://' in storage:
                            file_buffer = web_get_file(storage)
                            location = 'remote'
                        else:
                            file_buffer = s3_get_file(group, storage)
                            location = 'local'
                        if file_buffer != None:
                            old_file_position = file_buffer.tell()
                            file_buffer.seek(0, os.SEEK_END)
                            size = file_buffer.tell()
                            file_buffer.seek(old_file_position, os.SEEK_SET)
                        else:
                            return api_response(400, 'Could not reach the file location', 'We could not find the file raw content at the location provided.')
                        if access == 'public':
                            _file, created = FileModel.objects.get_or_create(encoding=encoding, name=name, mimetype=mimetype, size=size, storage=storage, location=location, group=group, description=description)
                        else:
                            _file, created = FileModel.objects.get_or_create(owner=owner, encoding=encoding, name=name, mimetype=mimetype, size=size, storage=storage, location=location, group=group, description=description)
                        if not created:
                            return api_response(200, 'File already exists', _file.info())
                        else:
                            logStat(file_obj=_file)
                            return api_response(201, 'File created', _file.info())
                else:
                    return api_response(204, 'Nothing created', 'You must provide the file information.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/show/<file_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_show(api_token, app_token, file_id):
    logTraffic(endpoint='/<api_token>/<app_token>/file/show/<file_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/show/<file_id>')
            if fk.request.method == 'GET':
                _file = FileModel.objects.with_id(file_id)
                if _file == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this file.')
                else:
                    print _file.extended()
                    if _file.owner != 'public' and _file.owner != str(current_user.id):
                        return api_response(401, 'Unauthorized access', 'This file is private and you are not the owner.')
                    else:
                        return api_response(200, 'File %s'%_file.name, _file.extended())
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/delete/<item_id>/<file_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_delete(api_token, app_token, item_id, file_id):
    logTraffic(endpoint='/<api_token>/<app_token>/file/delete/<item_id>/<file_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/delete/<item_id>/<file_id>')
            if fk.request.method == 'GET':
                _file = FileModel.objects.with_id(file_id)
                if _file == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this file.')
                else:
                    item = None
                    if _file.group == 'input':
                        item = RecordModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.project.owner
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                _file.delete()
                                item.inputs.remove(file_id)
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                    elif _file.group == 'output':
                        item = RecordModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.project.owner
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                _file.delete()
                                item.outputs.remove(file_id)
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                    elif _file.group == 'dependencie':
                        item = RecordModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.project.owner
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                _file.delete()
                                item.dependencies.remove(file_id)
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                    elif _file.group == 'diff':
                        item = DiffModel.objects.with_id(item_id)
                        if item != None:
                            owner1 = item.sender
                            owner2 = item.targeted
                            if current_user != owner1 and current_user != owner2:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                _file.delete()
                                item.resources.remove(file_id)
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                    elif _file.group == 'attach':
                        item = MessageModel.objects.with_id(item_id)
                        if item != None:
                            owner1 = item.sender
                            owner2 = item.receiver
                            if current_user != owner1 and current_user != owner2:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                _file.delete()
                                item.attachments.remove(file_id)
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                        else:
                            item = CommentModel.objects.with_id(item_id)
                            if item != None:
                                owner = item.sender
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                try:
                                    _file.delete()
                                    item.attachments.remove(file_id)
                                    if _file.location == 'local':
                                        s3_delete_file(_file.group, _file.storage)
                                except ValueError:
                                    pass
                    elif _file.group == 'picture':
                        item = ProfileModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.user
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            _file.storage = 'default-picture.png'
                            picture_buffer = s3_get_file('picture', 'default-picture.png')
                            _file.name = 'default-picture.png'
                            _file.location = 'local'
                            _file.group = 'picture'
                            _file.description = 'This is the default image used for the user profile picture in case none is provided.'
                            if picture_buffer != None:
                                old_file_position = picture_buffer.tell()
                                picture_buffer.seek(0, os.SEEK_END)
                                p_file.size = picture_buffer.tell()
                                picture_buffer.seek(old_file_position, os.SEEK_SET)
                            else:
                                _file.size = 0
                            _file.save()
                            if _file.location == 'local':
                                s3_delete_file(_file.group, _file.storage)

                    elif _file.group == 'logo':
                        item = ApplicationModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.developer
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            _file.storage = 'default-logo.png'
                            logo_buffer = s3_get_file('logo', 'default-logo.png')
                            _file.name = 'default-logo.png'
                            _file.location = 'local'
                            _file.group = 'logo'
                            _file.description = 'This is the default image used for the app logo in case none is provided.'
                            if logo_buffer != None:
                                old_file_position = logo_buffer.tell()
                                logo_buffer.seek(0, os.SEEK_END)
                                p_file.size = logo_buffer.tell()
                                logo_buffer.seek(old_file_position, os.SEEK_SET)
                            else:
                                _file.size = 0
                            _file.save()
                            if _file.location == 'local':
                                s3_delete_file(_file.group, _file.storage)
                        else:
                            item = ProjectModel.objects.with_id(item_id)
                            if item != None:
                                owner = item.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                _file.storage = 'default-project.png'
                                logo_buffer = s3_get_file('logo', 'default-project.png')
                                _file.name = 'default-project.png'
                                _file.location = 'local'
                                _file.group = 'logo'
                                _file.description = 'This is the default image used for the project logo in case none is provided.'
                                if logo_buffer != None:
                                    old_file_position = logo_buffer.tell()
                                    logo_buffer.seek(0, os.SEEK_END)
                                    p_file.size = logo_buffer.tell()
                                    logo_buffer.seek(old_file_position, os.SEEK_SET)
                                else:
                                    _file.size = 0
                                _file.save()
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)

                    elif _file.group == 'resource':
                        item = RecordModel.objects.with_id(item_id)
                        if item != None:
                            owner = item.project.owner
                            if current_user != owner:
                                return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                            try:
                                item.resources.remove(file_id)
                                _file.delete()
                                if _file.location == 'local':
                                    s3_delete_file(_file.group, _file.storage)
                            except ValueError:
                                pass
                        else:
                            item = EnvironmentModel.objects.with_id(item_id)
                            if item != None:
                                rec_temp = RecordModel.objects(environment=item).first()
                                if rec_temp == None:
                                    for p in ProjectModel.objects():
                                        if str(item.id) in p.history:
                                            owner = p.owner
                                            break
                                else:
                                    owner = rec_temp.project.owner
                                if current_user != owner:
                                    return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                try:
                                    item.resources.remove(file_id)
                                    _file.delete()
                                    if _file.location == 'local':
                                        s3_delete_file(_file.group, _file.storage)
                                except ValueError:
                                    pass
                            else:
                                item = ProjectModel.objects.with_id(item_id)
                                if item != None:
                                    owner = item.owner
                                    if current_user != owner:
                                        return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                    try:
                                        item.resources.remove(file_id)
                                        _file.delete()
                                        if _file.location == 'local':
                                            s3_delete_file(_file.group, _file.storage)
                                    except ValueError:
                                        pass
                                else:
                                    item = ApplicationModel.objects.with_id(item_id)
                                    if item != None:
                                        owner = item.developer
                                        if current_user != owner:
                                            return api_response(401, 'Unauthorized access', 'You are not an owner of this item.')
                                        try:
                                            item.resources.remove(file_id)
                                            _file.delete()
                                            if _file.location == 'local':
                                                s3_delete_file(_file.group, _file.storage)
                                        except ValueError:
                                            pass
                    if item == None:
                        if item_id in _file.storage or item_id in _file.name:
                            _file.delete()
                            s3_delete_file(_file.group, _file.storage)
                            logStat(deleted=True, file_obj=_file)
                            return api_response(200, 'Deletion succeeded', 'The file %s was succesfully deleted.'%_file.name)
                        else:
                            return api_response(400, 'Missing mandatory instance', 'A file should reference an existing item.')
                    else:
                        item.save()
                    logStat(deleted=True, file_obj=_file)
                    return api_response(200, 'Deletion succeeded', 'The file %s was succesfully deleted.'%_file.name)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/<api_token>/<app_token>/file/update/<file_id>', methods=['GET','POST','PUT','UPDATE','DELETE','POST'])
@crossdomain(origin='*')
def user_file_update(api_token, app_token, file_id):
    logTraffic(endpoint='/<api_token>/<app_token>/file/update/<file_id>')
    current_user = check_api(api_token)
    current_app = check_app(app_token)
    if current_user ==None:
        return api_response(401, 'Unauthorized access', 'The user credential is not authorized.')
    else:
        if current_app ==None:
            return api_response(401, 'Unauthorized access', 'This app credential is not authorized.')
        else:
            logAccess(current_app,'api', '/<api_token>/<app_token>/file/update/<file_id>')
            if fk.request.method == 'POST':
                _file = FileModel.objects.with_id(file_id)
                if _file == None:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this file.')
                else:
                    if _file.owner != 'public' and _file.owner != str(current_user.id):
                        return api_response(401, 'Unauthorized access', 'This file is private and you are not the owner.')
                    else:
                        if fk.request.data:
                            data = json.loads(fk.request.data)
                            encoding = data.get('encoding', _file.encoding)
                            size = data.get('size', _file.size)
                            name = data.get('name', _file.name)
                            path = data.get('path', _file.path)
                            storage = data.get('storage', _file.storage)
                            location = data.get('location', _file.location)
                            mimetype = data.get('mimetype', _file.mimetype)
                            group = data.get('group', _file.group)
                            description = data.get('description', _file.description)
                            if name == '':
                                name = _file.name
                            if location == '':
                                location = _file.location
                            _file.encoding = encoding
                            _file.size = size
                            _file.name = name
                            _file.path = path
                            _file.storage = storage
                            _file.location = location
                            _file.mimetype = mimetype
                            _file.group = group
                            _file.description = description
                            _file.save()
                            return api_response(201, 'File updated', _file.info())
                        else:
                            return api_response(204, 'Nothing created', 'You must provide the file information.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

# Custom:
# Item resolver: Take an id and try to find the conresponding object and return it with all the meta api
# functions that can be called on it.
# Can be used with a command line tool to enhance a very good way of using an API.