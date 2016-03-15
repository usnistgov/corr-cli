import datetime
from ..core import db
import json
import hashlib
from ..models import ApplicationModel

class AccessModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow())) #datetime.datetime.now())
    application = db.ReferenceField(ApplicationModel)
    possible_scope = ["api", "cloud", "root"]
    scope = db.StringField(default="root", choices=possible_scope)
    endpoint = db.StringField(max_length=256) #api/v1/push
    extend = db.DictField()

    def __repr__(self):
        return '<Access %r>' % (self.created_at)

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 
        'scope':str(self.scope), 'endpoint': str(self.endpoint)}
        if self.application != None:
            data['application'] = str(self.application.id)
        else:
            data['application'] = None
        return data

    def extended(self):
        data = self.info()
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def summary_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    @staticmethod
    def application_access(application=None):
        data = {}
        if application != None:
            data = {'total':len(AccessModel.objects(application=application))}
            data['access'] = [acc.info() for acc in AccessModel.objects(application=application).order_by('-created_at')]
            return data
        return data
    
    @staticmethod
    def activity_json():
        data = {}
        data['api'] = {'total':len(AccessModel.objects(scope='api')), 'endpoints':[]}
        data['api']['endpoints'] = AccessModel.objects(scope='api').order_by('-endpoint')
        data['cloud'] = {'total':len(AccessModel.objects(scope='cloud')), 'endpoints':[]}
        data['cloud']['endpoints'] = AccessModel.objects(scope='cloud').order_by('-endpoint')
        
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))