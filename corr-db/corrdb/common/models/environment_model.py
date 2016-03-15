import datetime
from ..core import db
import json
from bson import ObjectId
from ..models import BundleModel
from ..models import VersionModel
from ..models import CommentModel
from ..models import FileModel
          
class EnvironmentModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    possible_group = ["computational", "experimental", "hybrid", "unknown"]
    group = db.StringField(default="unknown", choices=possible_group)
    possible_system = ["container-based", "vm-based", "tool-based", "cloud-based", "device-based", "lab-based", "custom-based", "undefined"]
    system = db.StringField(default="undefined", choices=possible_system)
    # specifics: infos about the system used.
    # {'container-system':'docker|rocket', 'container-version':'1.0'}
    # {'tool-system':'guilogger', 'tool-version':'1.0'} 
    # {'device-system':'dft-machine', 'device-version':'electron 2700'}
    specifics = db.DictField() 
    version = db.ReferenceField(VersionModel)
    bundle = db.ReferenceField(BundleModel)
    comments = db.ListField(db.StringField()) #comments ids
    resources = db.ListField(db.StringField()) #files ids
    extend = db.DictField()

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
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'group':self.group,
        'system':self.system, 'specifics':self.specifics}
        if self.version != None:
            data['version'] = str(self.version.id)
        else:
            data['version'] = ''

        if self.bundle != None:
            data['bundle'] = str(self.bundle.id)
        else:
            data['bundle'] = ''

        data['comments'] = len(self.comments)
        data['resources'] = len(self.resources)

        return data

    def extended(self):
        data = self.info()
        data['comments'] = [comment.extended() for comment in self._comments()]
        data['resources'] = [resource.extended() for resource in self._resources()]
        data['extend'] = self.extend
        if self.version != None:
            data['version'] = self.version.extended()
        else:
            data['version'] = ''

        if self.bundle != None:
            data['bundle'] = self.bundle.extended()
        else:
            data['bundle'] = ''
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def summary_json(self):
        data = self.info()
        data['comments'] = len(self.comments)
        data['resources'] = len(self.resources)
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))