import datetime
from ..core import db
import json
from bson import ObjectId

from ..models import UserModel
from ..models import FileModel
import hashlib
          
class ApplicationModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    developer = db.ReferenceField(UserModel, required=True)
    name = db.StringField(required=True, unique=True)
    about = db.StringField()
    logo = db.ReferenceField(FileModel)
    possible_access = ["activated", "blocked", "deactivated"]
    access = db.StringField(default="deactivated", choices=possible_access)
    app_token = db.StringField(max_length=256, unique=True)
    users = db.ListField(db.StringField()) #users ids
    resources = db.ListField(db.StringField())
    storage = db.LongField()
    network = db.StringField(default="0.0.0.0")
    visibile = db.BooleanField(default=False)
    extend = db.DictField()

    def _users(self):
        users = []
        for u_id in self.users:
            u = UserModel.objects.with_id(u_id)
            if u != None:
                users.append(u)
        return users

    def _resources(self):
        resources = []
        for f_id in self.resources:
            f = FileModel.objects.with_id(f_id)
            if f != None:
                resources.append(f)
        return resources

    def save(self, *args, **kwargs):
        if not self.app_token:
            self.app_token = hashlib.sha256(b'CoRRApp_%s'%(str(datetime.datetime.utcnow()))).hexdigest()

        return super(ApplicationModel, self).save(*args, **kwargs)

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def retoken(self):
        self.api_token = hashlib.sha256(b'CoRRApp_%s_%s'%(str(self.developer.id), str(datetime.datetime.utcnow()))).hexdigest()
        self.save()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'developer':str(self.developer.id), 'name':self.name,
        'about':self.about, 'access':self.access, 'network':self.network, 'visibile':self.visibile}
        if self.logo != None:
            data['logo'] = str(self.logo.id)
        else:
            data['logo'] = ''
        data['resources'] = len(self.resources)
        return data

    def extended(self):
        data = self.info()
        data['resources'] = [resource.extended() for resource in self._resources()]
        data['extend'] = self.extend
        data['token'] = self.app_token
        data['users'] = self._users()
        data['storage'] = self.storage
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def summary_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))