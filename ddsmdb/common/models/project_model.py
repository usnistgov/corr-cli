from ..core import db
from ..models import UserModel
import json
import datetime


class ProjectModel(db.Document):
    user = db.ReferenceField(UserModel, reverse_delete_rule=db.CASCADE, required=True)
    name = db.StringField(max_length=300, required=True)
    
    def to_smt_json(self, request):
        from ..models import RecordModel
        query = RecordModel.objects(project=self)
        records = [r.to_json() for r in query]
        return json.dumps({'project' : self.name, 'url' : request.url, 'records' : records})

    @property
    def record_count(self):
        return self.records.count()

    @property
    def records(self):
        from ..models import RecordModel
        return RecordModel.objects(project=self)
    
    @property
    def last_updated(self):
        return self.records.order_by('-last_updated').limit(1).first().last_updated

    @property
    def duration(self):
        return self.records.sum('duration')

        
            
