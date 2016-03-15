import datetime
from ..core import db
import json
from bson import ObjectId
          
class BundleModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    possible_scope = ["local", "remote", "unknown"]
    scope = db.StringField(default="unknown", choices=possible_scope)
    location = db.StringField()
    mimetype = db.StringField()
    size = db.LongField()
    extend = db.DictField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'scope':self.scope,
        'location':self.location, 'size':self.size, 'mimetype':self.mimetype}
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