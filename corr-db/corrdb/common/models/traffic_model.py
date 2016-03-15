from ..core import db
import datetime
import json
from bson import ObjectId

class TrafficModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    possible_service = ["api", "cloud", "web", "undefined"]
    service = db.StringField(default="undefined", choices=possible_service)
    endpoint = db.StringField()
    interactions = db.LongField(default=0)
    extend = db.DictField()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 
        'service':str(self.service), 'endpoint':self.endpoint}
        return data

    def extended(self):
        data = self.info()
        data['interactions'] = self.interactions
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def summary_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))