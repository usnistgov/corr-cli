from ..core import db
import datetime
import json
from bson import ObjectId

class StatModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    # Shape the display for: 10 for years. to have a 10 year view. 
    # 12 for monthly to have a yearly view and 7 for a week view.
    interval = db.StringField(required=True) # "2015_01-2015_12", "2015_08_1-2015_08_31", "2015_08_14_0_0_0-2015_08_14_23_59_59"
    possible_category = ["user", "project", "record", "storage", "message", "application", "comment", "undefined"]
    category = db.StringField(default="undefined", choices=possible_category)
    possible_periode = ["yearly", "monthly", "daily", "undefined"]
    periode = db.StringField(default="undefined", choices=possible_periode)
    traffic = db.LongField(default=0) # rename volume later.
    extend = db.DictField()

    def info(self):
        data = {'created':str(self.created_at), 'interval':str(self.interval), 'category': str(self.category), 
        'periode':str(self.periode), 'volume':self.traffic}
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