# import flask as fk
# from cloud import app
# from corrdb.common.models import ProjectModel
# from corrdb.common.models import RecordModel
# from flask.ext.stormpath import login_required
# import json

# @app.route('/project/view/<objectid:id>')
# @login_required
# def project_view(id):
#     project = ProjectModel.objects.with_id(id)
#     records = RecordModel.objects(project=project)
#     return fk.render_template('project.html', project=project, records=records, user_model=project.owner)

# @app.route('/project/all', methods=['GET'])
# @login_required
# def public_projects():
#     if fk.request.method == 'GET':
#         projects = ProjectModel.objects()
#         summaries = [json.loads(p.summary_json()) for p in projects if not p.private]
#         return fk.Response(json.dumps({'number':len(summaries), 'projects':summaries}), mimetype='application/json')
#     else:
#         return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)