import datetime
from ..core import db
from ..models import UserModel
from ..models import FileModel
from ..models import CommentModel
from ..models import EnvironmentModel
from ..models import ApplicationModel
import json
from bson import ObjectId
          
class ProjectModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    application = db.ReferenceField(ApplicationModel)
    logo = db.ReferenceField(FileModel)
    owner = db.ReferenceField(UserModel, reverse_delete_rule=db.CASCADE, required=True)
    name = db.StringField(required=True)
    description = db.StringField()
    goals = db.StringField()
    tags = db.ListField(db.StringField())
    possible_access = ["private", "protected", "public"]
    access = db.StringField(default="private", choices=possible_access)
    history = db.ListField(db.StringField())
    cloned_from = db.StringField(max_length=256)
    resources = db.ListField(db.StringField()) #files ids
    possible_group = ["computational", "experimental", "hybrid", "undefined"]
    group = db.StringField(default="undefined", choices=possible_group)
    comments = db.ListField(db.StringField()) #comments ids
    # TOREPLACE BY comments = db.ListField(db.StringField()) #comments ids
    extend = db.DictField()

    def _history(self):
        history = []
        for env_id in self.history:
            env = EnvironmentModel.objects.with_id(env_id)
            if env != None:
                history.append(env)
        return history

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

    def clone(self):
        self.cloned_from = str(self.id)
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'updated':str(self.last_updated), 'id': str(self.id), 
        'owner':str(self.owner.id), 'name': self.name, 'access':self.access, 'tags':len(self.tags), 
        'duration': str(self.duration), 'records':self.record_count, 'environments':len(self.history),
        'diffs':self.diff_count, 'comments':len(self.comments), 'resources':len(self.resources)}
        if self.application != None:
            data['application'] = str(self.application.id)
        else:
            data['application'] = None
        if self.logo != None:
            data['logo'] = str(self.logo.id)
        else:
            data['logo'] = ''
        return data

    def extended(self):
        data = self.info()
        if self.application != None:
            data['application'] = self.application.info()
        else:
            data['application'] = {}
        data['tags'] = self.tags
        data['goals'] = self.goals
        data['history'] = [env.extended() for env in self._history()]
        data['description'] = self.description
        data['comments'] = [comment.extended() for comment in self._comments()]
        data['resources'] = [resource.extended() for resource in self._resources()]
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def summary_json(self):
        data = self.info()
        data['tags'] = len(self.tags)
        if self.goals != None:
            data['goals'] = self.goals[0:96]+"..." if len(self.goals) >=100 else self.goals
        else:
            data['goals'] = None
        if self.description != None:
            data['description'] = self.description[0:96]+"..." if len(self.description) >=100 else self.description
        else:
            data['description'] = None
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def activity_json(self, public=False):
        if not public:
            records_summary = [json.loads(r.summary_json()) for r in self.records]
            return json.dumps({'project':self.extended(), "records":records_summary}, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            if project.access == 'public':
                records_summary = []
                for record in self.records:
                    if record.access == 'public':
                        records_summary.append(json.loads(r.summary_json()))
                return json.dumps({'project':self.extended(), "records":records_summary}, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                return json.dumps({}, sort_keys=True, indent=4, separators=(',', ': '))


    def compress(self):
        data = self.extended()
        data['records'] = [record.extended() for record in self.records]
        data['diffs'] = [diff.extended() for diff in self.diffs]
        return data

    @property
    def record_count(self):
        return self.records.count()

    @property
    def diff_count(self):
        from ..models import DiffModel
        diffs = []
        for diff in DiffModel.objects():
            if diff.record_from.project == self:
                diffs.append(diff)
            if diff.record_to.project == self:
                diffs.append(diff)
        return len(diffs)

    @property
    def diffs(self):
        from ..models import DiffModel
        diffs = []
        for diff in DiffModel.objects():
            if diff.record_from.project == self:
                diffs.append(diff)
            if diff.record_to.project == self:
                diffs.append(diff)
        return diffs

    @property
    def records(self):
        from ..models import RecordModel
        return RecordModel.objects(project=self).order_by('+created_at')
    
    @property
    def last_updated(self):
        if self.record_count >0:
            return self.records.order_by('-updated_at').limit(1).first().updated_at
        else:
            return self.created_at

    @property
    def duration(self):
        if self.records == None or len(self.records) == 0:
            return 0
        else:
            last_updated_strp = datetime.datetime.strptime(str(self.last_updated), '%Y-%m-%d %H:%M:%S.%f')
            created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S.%f')
            # try:
            #     last_updated_strp = datetime.datetime.strptime(str(self.last_updated), '%Y-%m-%d %H:%M:%S.%f')
            # except:
            #     last_updated_strp = datetime.datetime.strptime(str(self.last_updated), '%Y-%m-%d %H:%M:%S')

            # try:
            #     created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S.%f')
            # except:
            #     created_strp = datetime.datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S')

            # print "Duration: %s"%str(last_updated_strp-created_strp)
            return last_updated_strp-created_strp