import datetime
from ..core import db


class UserModel(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    email = db.StringField(max_length=120, required=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def projects(self):
        from ..models import ProjectModel
        return ProjectModel.objects(user=self)
    
    @property
    def record_count(self):
        return sum([p.record_count for p in self.projects])

    @property
    def records(self):
        records = []
        for project in self.projects:
            records += project.records
        return records

    @property
    def duration(self):
        return sum([p.duration for p in self.projects])


            
