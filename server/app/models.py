from datetime import datetime

from flask_restful import fields

from .shared import db


class User(db.Model):

    __tablename__ = 'getin_user'

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'corporation': fields.String,
        'alliance': fields.String,
        'editor': fields.Boolean,
        'admin': fields.Boolean,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    corporation = db.Column(db.String)
    alliance = db.Column(db.String)
    editor = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, corporation, alliance, editor=False, admin=False):
        self.name = name
        self.corporation = corporation
        self.alliance = alliance
        self.editor = editor
        self.admin = admin

        # TODO remove test code
        if name == 'Celeo Servasse':
            self.admin = True
            self.editor = True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def in_alliance(self):
        return self.alliance == 'The Society For Unethical Treatment Of Sleepers'

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return '<User-{}>'.format(self.name)


class Category(db.Model):

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pages = db.relationship('Page', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Page(db.Model):

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'category_id': fields.Integer,
        'deleted': fields.Integer,
    }

    resource_fields_full = {
        'id': fields.Integer,
        'name': fields.String,
        'content': fields.String,
        'category_id': fields.Integer,
        'deleted': fields.Integer,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.String)
    deleted = db.Column(db.Boolean)

    def __init__(self, name, category_id, content=''):
        self.name = name
        self.category_id = category_id
        self.content = content
        self.deleted = False


class Edit(db.Model):

    resource_fields = {
        'id': fields.Integer,
        'page_id': fields.Integer,
        'category_id': fields.Integer,
        'user_id': fields.Integer,
        'new_content': fields.String,
        'deleted': fields.Boolean,
        'timestamp': fields.DateTime,
        'approved_by': fields.String,
    }

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('getin_user.id'))
    new_content = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    approved_by = db.Column(db.String)

    def __init__(self, page_id, category_id, user_id, new_content, deleted=False, approved_by='*server*'):
        self.page_id = page_id
        self.category_id = category_id
        self.user_id = user_id
        self.new_content = new_content
        self.deleted = deleted
        self.timestamp = datetime.utcnow()
        self.approved_by = approved_by
