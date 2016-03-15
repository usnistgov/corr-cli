import datetime
from ..core import db
from ..models import UserModel
from ..models import FileModel
from ..models import CommentModel
from ..models import RecordModel
from ..models import ProfileModel
import json
from bson import ObjectId

class DiffModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    sender = db.ReferenceField(UserModel, required=True)
    targeted = db.ReferenceField(UserModel, required=True)
    record_from = db.ReferenceField(RecordModel, reverse_delete_rule=db.CASCADE, required=True)
    record_to = db.ReferenceField(RecordModel, reverse_delete_rule=db.CASCADE, required=True)
    possible_method = ["default", "visual", "custom", "undefined"]
    method = db.StringField(default="undefined", choices=possible_method)
    resources = db.ListField(db.StringField()) #files ids
    possible_proposition = ["repeated", "reproduced", "replicated", "non-replicated", "non-repeated", "non-reproduced", "undefined"]
    proposition = db.StringField(default="undefined", choices=possible_proposition)
    possible_status = ["proposed", "agreed", "denied", "undefined", "altered"]
    status = db.StringField(default="undefined", choices=possible_status)
    comments = db.ListField(db.StringField()) #comments ids
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
        data = {'created':str(self.created_at), 'id': str(self.id), 
        'from':str(self.record_from.id), 'to': str(self.record_to.id), 'proposition':self.proposition, 
        'method': self.method, 'status': self.status}
        data['sender'] = str(self.sender.id)
        data['targeted'] = str(self.targeted.id)
        data['resources'] = len(self.resources)
        data['comments'] = len(self.comments)
        return data

    def extended(self):
        data = self.info()
        sender_profile = ProfileModel.objects(user=self.sender).first()
        targeted_profile = ProfileModel.objects(user=self.targeted).first()
        if sender_profile == None:
            data['sender'] = self.sender.email
        else:
            data['sender'] = sender_profile.extended()
        if targeted_profile == None:
            data['targeted'] = self.targeted.email
        else:
            data['targeted'] = targeted_profile.extended()
        data['resources'] = [resource.extended() for resource in self._resources()]
        data['comments'] = [comment.extended() for comment in self._comments()]
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def summary_json(self):
        data = self.info()
        data['sender'] = str(self.sender.id)
        data['targeted'] = str(self.targeted.id)
        data['comments'] = len(self.comments)
        data['resources'] = len(self.resources)
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))