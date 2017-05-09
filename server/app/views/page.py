from flask import request
from flask_restful import Resource, marshal_with

from ..util import authenticate, restrict_editor
from ..models import db, Page, Edit, get_user_from_token


class PagesResource(Resource):

    @authenticate
    @marshal_with(Page.resource_fields)
    def get(self):
        return Page.query.filter_by(deleted=False).all()

    @restrict_editor
    def post(self):
        db.session.add(Page(
            name=request.json['name'],
            category_id=request.json['category_id'],
            content=request.json['content']
        ))
        db.session.commit()
        return {}, 204


class PageResource(Resource):

    method_decorators = [restrict_editor]

    def put(self, id):
        page = Page.query.get(id)
        db.session.add(Edit(
            page.id,
            page.category_id,
            get_user_from_token(),
            request.json['content']
        ))
        page.category_id = int(request.json['category_id'])
        page.content = int(request.json['content'])
        db.session.commit()
        return {}, 204

    def delete(self, id):
        page = Page.query.get(id)
        db.session.add(Edit(
            page.id,
            page.category_id,
            get_user_from_token(),
            request.json['content'],
            deleted=True
        ))
        page.deleted = True
        db.session.commit()
        return {}, 204
