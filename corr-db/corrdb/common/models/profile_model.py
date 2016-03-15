import datetime
from ..core import db
from ..models import UserModel
from ..models import FileModel
import json
from bson import ObjectId
          
class ProfileModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    user = db.ReferenceField(UserModel, reverse_delete_rule=db.CASCADE, required=True)
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    picture = db.ReferenceField(FileModel)
    organisation = db.StringField()
    about = db.StringField()
    extend = db.DictField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 
        'user':str(self.user.id), 'fname': self.fname, 'lname': self.lname, 'picture':str(self.picture.id)}
        return data

    def extended(self):
        data = self.info()
        data['organisation'] = self.organisation
        data['about'] = self.about
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def summary_json(self):
        data = self.info()
        data['organisation'] = self.organisation
        if self.about != None:
            data['about'] = self.about[0:96]+"..." if len(self.about) >=100 else self.about
        else:
            data['about'] = None
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
