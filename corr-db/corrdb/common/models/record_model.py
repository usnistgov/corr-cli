from ..core import db
from ..models import FileModel
from ..models import CommentModel
from ..models import ProjectModel
from ..models import EnvironmentModel
from ..models import ApplicationModel
import datetime
import json
from bson import ObjectId

class RecordModel(db.Document):
    project = db.ReferenceField(ProjectModel, reverse_delete_rule=db.CASCADE, required=True)
    application = db.ReferenceField(ApplicationModel)
    parent = db.StringField(max_length=256)# parent record id #db.ReferenceField(RecordModel, reverse_delete_rule=db.CASCADE)
    label = db.StringField()
    tags = db.ListField(db.StringField())
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=str(datetime.datetime.utcnow()))
    system = db.DictField() # look into providing os version, gpu infos, compiler infos.
    execution = db.DictField()
    preparation = db.DictField() # What are the steps to get this ready to be recorded.
    inputs = db.ListField(db.DictField())
    outputs = db.ListField(db.DictField())
    dependencies = db.ListField(db.DictField()) # check for c++ libs here. {'type':lib|compiler|interpretor|language|software|prorietary}
    possible_status = ["starting", "started", "paused", "sleeping", "finished", "crashed", "terminated", "resumed", "running", "unknown"]
    status = db.StringField(default="unknown", choices=possible_status)
    environment = db.ReferenceField(EnvironmentModel, reverse_delete_rule=db.CASCADE)
    cloned_from = db.StringField(max_length=256)
    possible_access = ["private", "protected", "public"]
    access = db.StringField(default="private", choices=possible_access)
    resources = db.ListField(db.StringField()) #files ids
    rationels = db.ListField(db.StringField()) #Why did you do this record. What is different from others.
    comments = db.ListField(db.StringField()) #comments ids
    extend = db.DictField()

    def clone(self):
        self.cloned_from = str(self.id)
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(RecordModel, self).save(*args, **kwargs)
    
    def update_fields(self, data):
        for k, v in self._fields.iteritems():
            if not v.required:
                if k != 'created_at':
                        yield k, v
    
    def update(self, data):
        for k, v in self.update_fields(data):
            if k in data.keys():
                if k == 'created_at':
                    #self.created_at = datetime.datetime.strptime(data[k], '%Y-%m-%d %X')
                    pass
                else:
                    setattr(self, k, data[k])
                del data[k]
        self.save()       
        if data:
            body, created = RecordBodyModel.objects.get_or_create(head=self)
            body.data.update(data)
            body.save()

    # @property
    # def files(self):
    #     from ..models import FileModel
    #     return FileModel.objects(record=self).order_by('+created_at')

    @property
    def body(self):
        return RecordBodyModel.objects(head=self).first()

    @property
    def duration(self):
        updated_strp = datetime.datetime.strptime(str(self.updated_at), '%Y-%m-%d %H:%M:%S.%f')
        created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S.%f')
        # try:
        #     updated_strp = datetime.datetime.strptime(str(self.updated_at), '%Y-%m-%d %H:%M:%S.%f')
        # except:
        #     updated_strp = datetime.datetime.strptime(str(self.updated_at), '%Y-%m-%d %H:%M:%S')

        # try:
        #     created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S.%f')
        # except:
        #     created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S')

        # print str(updated_strp-created_strp)
        return updated_strp-created_strp

    def info(self):
        data = {}
        data['head'] = {'updated':str(self.updated_at),
         'id': str(self.id), 'project':str(self.project.id), 
         'label': self.label, 'created':str(self.created_at), 'status' : self.status, 'access':self.access}
        data['head']['tags'] = self.tags
        data['head']['comments'] = len(self.comments)
        data['head']['resources'] = len(self.resources)
        data['head']['inputs'] = len(self.inputs)
        data['head']['outputs'] = len(self.outputs)
        data['head']['dependencies'] = len(self.dependencies)
        if self.application != None:
            data['head']['application'] = str(self.application.id)
        else:
            data['head']['application'] = None
        if self.environment != None:
            data['head']['environment'] = str(self.environment.id)
        else:
            data['head']['environment'] = None
        if self.parent != None:
            data['head']['parent'] = self.parent
        else:
            data['head']['parent'] = None
        if self.body != None:
            data['body'] = str(self.body.id)
        else:
            data['body'] = None
        return data

    def _comments(self):
        comments = []
        for com_id in self.comments:
            com = CommentModel.objects.with_id(com_id)
            if com != None:
                comments.append(com)
        return comments

    def _resources(self):
        resources = []
        for f_id in self.resources:
            f = FileModel.objects.with_id(f_id)
            if f != None:
                resources.append(f)
        return resources

    def extended(self):
        data = self.info()
        data['head']['system'] = self.system
        data['head']['execution'] = self.execution
        data['head']['preparation'] = self.preparation
        data['head']['inputs'] = self.inputs
        data['head']['outputs'] = self.outputs
        data['head']['dependencies'] = self.dependencies
        data['head']['comments'] = [comment.extended() for comment in self._comments()]
        data['head']['resources'] = [resource.extended() for resource in self._resources()]
        data['head']['rationels'] = self.rationels
        data['extend'] = self.extend
        if self.application != None:
            data['head']['application'] = self.application.info()
        else:
            data['head']['application'] = {}
        if self.environment != None:
            data['head']['environment'] = self.environment.extended()
        else:
            data['head']['environment'] = {}
        if self.parent != '':
            data['head']['parent'] = RecordModel.objects.with_id(self.parent).info()
        else:
            data['head']['parent'] = {}
        if self.body != None:
            data['body'] = self.body.extended()
        else:
            data['body'] = {}
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def summary_json(self):
        data = self.info()
        data['head']['inputs'] = len(self.inputs)
        data['head']['outputs'] = len(self.outputs)
        data['head']['dependencies'] = len(self.dependencies)
        data['head']['comments'] = len(self.comments)
        data['head']['resources'] = len(self.resources)
        data['head']['rationels'] = len(self.rationels)
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class RecordBodyModel(db.Document):
    updated_at = db.StringField(default=str(datetime.datetime.utcnow()))
    head = db.ReferenceField(RecordModel, reverse_delete_rule=db.CASCADE, unique=True, required=True)
    data = db.DictField()
    extend = db.DictField()

    def info(self):
        data = {}
        data['head'] = str(self.head.id)
        data['body'] = {'updated':str(self.updated_at), 'id':str(self.id), 'content':self.data}
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


        

