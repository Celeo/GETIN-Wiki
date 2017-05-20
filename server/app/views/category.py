from flask import request
from flask_restful import Resource, marshal, marshal_with

from ..util import authenticate, restrict_admin
from ..models import db, Category, Page


class CategoriesResource(Resource):

    @authenticate
    @marshal_with(Category.resource_fields)
    def get(self):
        """ Return all categories """
        return Category.query.all()

    @restrict_admin
    def post(self):
        """ Create a new category """
        db.session.add(Category(request.json['name']))
        db.session.commit()
        return {}, 204


class CategoryResource(Resource):

    method_decorators = [restrict_admin]

    def put(self, id):
        """ Change the name of the category """
        Category.query.get(id).name = request.json['name']
        db.session.commit()
        return {}, 204

    def delete(self, id):
        """ Delete the category """
        db.session.delete(Category.query.get(id))
        db.session.commit()
        return 204, {}


class IndexResource(Resource):

    method_decorators = [authenticate]

    def get(self):
        """ Return a listing of all categories and their pages """
        return [
            {
                'name': category.name,
                'pages': [
                    marshal(page, Page.resource_fields) for page in
                    category.pages.filter_by(deleted=False).order_by(Page.name.desc()).all()
                ]
            } for category in Category.query.order_by(Category.name.desc()).all()
        ]
