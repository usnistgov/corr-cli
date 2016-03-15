import datetime
from ..core import db
import json
from bson import ObjectId
          
class VersionModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    possible_system = ["git", "mercurial", "subversion", "cvs", "bazaar", "arch", "monotone", "aegis", "fastcst", "opencm", "vesta", "codeville", "darcs", "bitkeeper", "perforce", "clearcase" , "unknown"]
    system = db.StringField(default="unknown", choices=possible_system)
    baseline = db.StringField()
    marker = db.StringField()
    extend = db.DictField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'system':self.system,
        'baseline':self.baseline, 'marker':self.marker}
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