from flask import request
from flask_restful import Resource, marshal_with

from ..util import restrict_admin
from ..models import db, Category


class CategoriesResource(Resource):

    method_decorators = [restrict_admin]

    @marshal_with(Category.resource_fields)
    def get(self):
        return Category.query.all()

    def post(self):
        db.session.add(Category(request.json['name']))
        db.session.commit()
        return {}, 204


class CategoryResource(Resource):

    method_decorators = [restrict_admin]

    def put(self, id):
        Category.query.get(id).name = request.json['name']
        db.session.commit()
        return {}, 204

    def delete(self, id):
        db.session.delete(Category.query.get(id))
        db.session.commit()
        return 204, {}
