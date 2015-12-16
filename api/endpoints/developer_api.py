import json

from flask.ext.api import status
import flask as fk

from api import app, API_URL, check_api, api_response, s3_get_file, web_get_file
from corrdb.common.models import UserModel
from corrdb.common.models import AccessModel
from corrdb.common.models import FileModel
from corrdb.common.models import ApplicationModel

import mimetypes
import json
import traceback

@app.route(API_URL + '/<api_token>/applications', methods=['GET'])
def apps_get(api_token):
    current_user = check_api(api_token)
    if current_user is not None:
        if current_user.group == "developer":
            if fk.request.method == 'GET':
                apps = ApplicationModel.objects(developer=current_user)
                apps_json = {'total_apps':len(apps), 'apps':[]}
                for application in apps:
                    apps_json['apps'].append(application.extended())
                return api_response(200, 'Developer\'s applications', apps_json)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
        else:
            return api_response(401, 'Unauthorized access to the API', 'This is not a developer account.')
    else:
        return api_response(401, 'Unauthorized access to the API', 'This API token is not authorized.')

@app.route(API_URL + '/<api_token>/application/logo/<app_id>', methods=['GET'])
def app_logo(api_token, app_id):
    current_user = check_api(api_token)
    if current_user is not None:
        if current_user.group == "developer":
            if fk.request.method == 'GET':
                app = ApplicationModel.objects.with_id(app_id)
                if app != None:
                    if app.developer == current_user or app.visibile:
                        name = app.name if app.name != '' and app.name != None else 'unknown'
                        logo = app.logo
                        if logo.location == 'local' and 'http://' not in logo.storage:
                            logo_buffer = s3_get_file('logo', logo.storage)
                            if logo_buffer == None:
                                return api_response(404, 'No logo found', 'We could not fetch the logo at [%s].'%logo.storage)
                            else:
                                return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                        elif logo.location == 'remote':
                            logo_buffer = web_get_file(logo.storage)
                            if logo_buffer != None:
                                return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                            else:
                                logo_buffer = s3_get_file('logo', 'app-default-logo.png')
                                if logo_buffer == None:
                                    return api_response(404, 'No logo found', 'We could not fetch the logo at %s.'%logo.storage)
                                else:
                                    return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                        else:
                            # solve the file situation and return the appropriate one.
                            if 'http://' in logo.storage:
                                logo.location = 'remote'
                                logo.save()
                                logo_buffer = web_get_file(logo.storage)
                                if logo_buffer != None:
                                    return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                                else:
                                    logo_buffer = s3_get_file('logo', 'app-default-logo.png')
                                    if logo_buffer == None:
                                        return api_response(404, 'No logo found', 'We could not fetch the logo at %s.'%logo.storage)
                                    else:
                                        return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                            else:
                                logo.location = 'local'
                                logo.save()
                                logo_buffer = s3_get_file('logo', logo.storage)
                                if logo_buffer == None:
                                    return api_response(404, 'No logo found', 'We could not fetch the logo at %s.'%logo.storage)
                                else:
                                    return fk.send_file(logo_buffer, attachment_filename=logo.name, mimetype=logo.mimetype)
                    else:
                        return api_response(405, 'Application access request denied', 'You are not the developer of this application.')
                else:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this application.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
        else:
            return api_response(401, 'Unauthorized access to the API', 'This is not a developer account.')
    else:
        return api_response(401, 'Unauthorized access to the API', 'This API token is not authorized.')

@app.route(API_URL + '/<api_token>/application/access/<app_id>', methods=['GET'])
def app_access(api_token, app_id):
    current_user = check_api(api_token)
    if current_user is not None:
        if current_user.group == "developer":
            if fk.request.method == 'GET':
                app = ApplicationModel.objects.with_id(app_id)
                if app != None:
                    if app.developer == current_user:
                        app_access = AccessModel.application_access(app)
                        name = app.name if app.name != '' and app.name != None else 'unknown'
                        api_response(200, 'Application %s access hsistory'%name, app_access)
                    else:
                        return api_response(405, 'Application access request denied', 'You are not the developer of this application.')
                else:
                    return api_response(404, 'Request suggested an empty response', 'Unable to find this application.')
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
        else:
            return api_response(401, 'Unauthorized access to the API', 'This is not a developer account.')
    else:
        return api_response(401, 'Unauthorized access to the API', 'This API token is not authorized.')

@app.route(API_URL + '/<api_token>/application/search/<app_name>', methods=['GET'])
def app_search(api_token, app_name):
    current_user = check_api(api_token)
    if current_user is not None:
        if current_user.group == "developer":
            if fk.request.method == 'GET':
                apps = ApplicationModel.objects(name=app_name)
                apps_dict = {'total_apps':0, 'apps':[]}
                for application in apps:
                    if application.developer == current_user:
                        apps_dict['apps'].append(application.info())
                    else:
                        # Only visible apps from other researchers can be searched for.
                        if application.visibile:
                            apps_dict['apps'].append(application.info())
                apps_dict['total_apps'] = len(apps_dict['apps'])
                return api_response(200, 'Search results for application with name: %s'%app_name, apps_dict)
            else:
                return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
        else:
            return api_response(401, 'Unauthorized access to the API', 'This is not a developer account.')
    else:
        return api_response(401, 'Unauthorized access to the API', 'This API token is not authorized.')

# Link for the application tool to test connectivity
@app.route(API_URL + '/<app_token>/connectivity', methods=['GET'])
def app_connectivity(app_token):
    current_app = check_api(app_token)
    if current_app is not None:
        if fk.request.method == 'GET':
            name = current_app.name if current_app.name != '' and current_app.name != None else 'unknown'
            return api_response(200, 'Application %s is accessible'%name, current_app.info())
        else:
            return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
    else:
        api_response(401, 'Unauthorized access to the API', 'This is not a developer account.')