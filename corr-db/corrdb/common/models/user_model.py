import datetime
from ..core import db
import json
import hashlib
import time

# @TODO Issue with connected_at and datetime in general that makes it not stable in mongodb.
# Here i had to remove the msecondes from connected_at to make it stable from renew to allowance.
# I know it doesn't make sense. But it does the trick for now.
# This is a bug that i will have to fix later on for sure.

class UserModel(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    connected_at = db.StringField(default=str(datetime.datetime.utcnow()))
    email = db.StringField(required=True, unique=True)
    api_token = db.StringField(max_length=256, unique=True)
    session = db.StringField(max_length=256, unique=True)
    possible_group = ["admin", "user", "developer", "public", "unknown"]
    group = db.StringField(default="unknown", choices=possible_group)
    extend = db.DictField()

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

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = str(datetime.datetime.utcnow())

        if not self.connected_at:
            self.connected_at = str(datetime.datetime.utcnow())

        if not self.api_token:
            self.api_token = hashlib.sha256(b'CoRRToken_%s'%(str(datetime.datetime.utcnow()))).hexdigest()

        if not self.session:
            self.session = hashlib.sha256(b'CoRRSession_%s'%(str(datetime.datetime.utcnow()))).hexdigest()

        return super(UserModel, self).save(*args, **kwargs)

    def sess_sync(self, unic):
        self.session = str(hashlib.sha256(b'CoRRSession_%s_%s_%s'%(self.email, str(self.connected_at), unic)).hexdigest())
        self.save()

    def renew(self, unic):
        # print "renew unic: %s"%unic
        print "connected_at: %s"%str(self.connected_at)
        self.connected_at = str(datetime.datetime.utcnow())
        print "connected_at: %s"%str(self.connected_at)
        print "session: %s"%str(self.session)
        self.session = str(hashlib.sha256(b'CoRRSession_%s_%s_%s'%(self.email, str(self.connected_at), unic)).hexdigest())
        self.save()
        print "connected_at: %s"%str(self.connected_at)
        print "session: %s"%str(self.session)

    def retoken(self):
        self.api_token = hashlib.sha256(b'CoRRToken_%s_%s'%(self.email, str(datetime.datetime.utcnow()))).hexdigest()
        self.save()

    def allowed(self, unic):
        # print "allowed unic: %s"%unic
        print "connected_at: %s"%str(self.connected_at)
        print "session: %s"%str(self.session)
        allowed = hashlib.sha256(b'CoRRSession_%s_%s_%s'%(self.email, str(self.connected_at), unic)).hexdigest()
        print "allowed: %s"%str(allowed)
        return str(allowed)

    def info(self):
        data = {'created':str(self.created_at), 'id': str(self.id), 'email' : self.email, 'group':self.group, 'total_projects' : len(self.projects), 'total_duration':self.duration, 'total_records':self.record_count}
        return data

    def extended(self):
        data = self.info()
        data['apiToken'] = self.api_token
        data['session'] = self.session
        data['extend'] = self.extend
        return data

    def home(self):
        from ..models import ProfileModel
        data = {}
        data['account'] = self.extended()
        data['profile'] = ProfileModel.objects(user=self).first().extended()
        data['activity'] = {}
        data['activity']['quota'] = self.quota
        data['activity']['apps'] = {'size':len(self.apps), 'list':[app.info() for app in self.apps]}
        data['activity']['statistics'] = {'size_project':len(self.projects), 'size_records':len(self.records), 'duration':self.duration}
        return data


    def to_json(self):
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def activity_json(self, admin=False):
        projects_summary = [json.loads(p.summary_json()) for p in self.projects if not p.private or admin]
        return json.dumps({'user':self.extended(), 'projects' : projects_summary}, sort_keys=True, indent=4, separators=(',', ': '))

    @property
    def projects(self):
        from ..models import ProjectModel
        return ProjectModel.objects(owner=self)

    @property
    def apps(self):
        from ..models import ApplicationModel
        return [p.application for p in self.projects]

    @property
    def records(self):
        records = []
        for project in self.projects:
            records.extend(project.records)
        return records

    @property
    def quota(self):
        #Add the filemodel to the quota check.
        from ..models import FileModel
        from ..models import EnvironmentModel
        from ..models import CommentModel
        occupation = 0
        for project in self.projects:
            for env in project.history:
                environment = EnvironmentModel.objects.with_id(env)
                if environment != None and environment.bundle != None:
                    try:
                        occupation = occupation + environment.bundle.size
                    except:
                        pass
            for file_id in project.resources:
                _file = FileModel.objects.with_id(file_id)
                if _file != None:
                    try:
                        occupation = occupation + _file.size
                    except:
                        pass
            for file_id in project.resources:
                _file = FileModel.objects.with_id(file_id)
                if _file != None:
                    try:
                        occupation = occupation + _file.size
                    except:
                        pass
            for comment_id in project.comments:
                _comment = CommentModel.objects.with_id(comment_id)
                if _comment != None:
                    for file_id in _comment.attachments:
                        _file = FileModel.objects.with_id(file_id)
                        if _file != None:
                            try:
                                occupation = occupation + _file.size
                            except:
                                pass
            for record in self.records:
                for file_id in record.resources:
                    _file = FileModel.objects.with_id(file_id)
                    if _file != None:
                        try:
                            occupation = occupation + _file.size
                        except:
                            pass
                for comment_id in record.comments:
                    _comment = CommentModel.objects.with_id(comment_id)
                    if _comment != None:
                        for file_id in _comment.attachments:
                            _file = FileModel.objects.with_id(file_id)
                            if _file != None:
                                try:
                                    occupation = occupation + _file.size
                                except:
                                    pass

        return occupation
    
    @property
    def record_count(self):
        return sum([p.record_count for p in self.projects])

    @property
    def duration(self):
        d = 0
        for p in self.projects:
            try:
                d += p.duration.total_seconds()
            except:
                d = d + p.duration
        return str(datetime.timedelta(seconds=d))


            
