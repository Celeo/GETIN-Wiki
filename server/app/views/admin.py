from flask import request
from flask_restful import Resource, marshal_with

from ..util import restrict_admin
from ..models import db, User


class UserResource(Resource):

    method_decorators = [restrict_admin]

    @marshal_with(User.resource_fields)
    def get(self):
        return User.query.order_by('id').all()

    def post(self):
        user = User.query.get(int(request.json['id']))
        if request.json['role'] == 'editor':
            user.editor = request.json['action'] == 'promote'
        if request.json['role'] == 'admin':
            user.admin = request.json['action'] == 'promote'
        db.session.commit()
        return {}, 204
