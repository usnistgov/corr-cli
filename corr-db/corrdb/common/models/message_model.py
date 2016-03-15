import datetime
from ..core import db
import json
from bson import ObjectId

from ..models import UserModel
from ..models import FileModel
          
class MessageModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    sender = db.ReferenceField(UserModel, required=True)
    receiver = db.ReferenceField(UserModel, required=True)
    title = db.StringField()
    content = db.StringField()
    attachments = db.ListField(db.StringField()) #files ids
    extend = db.DictField()

    def _attachments(self):
        attachments = []
        for f_id in self.attachments:
            f = FileModel.objects.with_id(f_id)
            if f != None:
                attachments.append(f)
        return attachments

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'sender':str(self.sender.id),
        'receiver':str(self.receiver.id), 'title':self.title}
        data['attachments'] = len(self.attachments)
        return data

    def extended(self):
        data = self.info()
        data['content'] = self.content
        data['attachments'] = [attachment.extended() for attachment in self._attachments()]
        data['extend'] = self.extend
        return data

    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def summary_json(self):
        data = self.info()
        if self.content != None:
            data['content'] = self.content[0:96]+"..." if len(self.content) >=100 else self.content
        else:
            data['content'] = None
        if self.attachments != None:
            data['attachments'] = len(self.attachments)
        else:
            data['attachments'] = None
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))