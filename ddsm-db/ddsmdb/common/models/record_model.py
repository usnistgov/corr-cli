from ..core import db
from ..models import ProjectModel
import datetime

class RecordModel(db.Document):
    project = db.ReferenceField(ProjectModel, reverse_delete_rule=db.CASCADE, required=True)
    label = db.StringField(max_length=300, required=True)
    timestamp = db.DateTimeField(verbose_name="time stamp")
    duration = db.FloatField(default=0.0)
    reason = db.StringField(max_length=10000)
    outcome = db.StringField(max_length=10000)
    possible_status = ["crashed", "unknown", "started", "running", "finished"]
    status = db.StringField(default="unknown", choices=possible_status)
    tags = db.ListField(db.StringField(max_length=100))
    last_updated = db.DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        self.last_updated = datetime.datetime.now()
        return super(RecordModel, self).save(*args, **kwargs)
    
    def update_fields(self, data):
        for k, v in self._fields.iteritems():
            if not v.required:
                if k != 'created_at':
                    yield k, v
    
    def update(self, data):
        for k, v in self.update_fields(data):
            if k in data.keys():
                if k == 'timestamp':
                    self.timestamp = datetime.datetime.strptime(data[k], '%Y-%m-%d %X')
                else:
                    setattr(self, k, data[k])
                del data[k]
                
        self.save()
        if data:
            body, created = RecordBodyModel.objects.get_or_create(head=self)
            body.data.update(data)
            body.save()

class RecordBodyModel(db.Document):
    head = db.ReferenceField(RecordModel, reverse_delete_rule=db.CASCADE, unique=True)
    data = db.DictField()


        

