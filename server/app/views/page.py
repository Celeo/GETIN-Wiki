from flask import request
from flask_restful import Resource, marshal_with

from ..util import authenticate, restrict_editor, get_user_from_token
from ..models import db, Page, Edit


class PagesResource(Resource):

    @authenticate
    @marshal_with(Page.resource_fields)
    def get(self):
        return Page.query.filter_by(deleted=False).all()

    @restrict_editor
    def post(self):
        name = request.json['name']
        category_id = request.json['category_id']
        page = Page.query.filter_by(name=name, category_id=category_id).first()
        if not page:
            page = Page(name=name, category_id=category_id)
            db.session.add(page)
            db.session.commit()
        return {
            'category': page.category.name,
            'page': page.name,
        }


class PageResource(Resource):

    @authenticate
    @marshal_with(Page.resource_fields_full)
    def get(self, id):
        return Page.query.get(id)

    @restrict_editor
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

    @restrict_editor
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


class LookupResource(Resource):

    method_decorators = [authenticate]

    @marshal_with(Page.resource_fields_full)
    def get(self, category_name, page_name):
        for page in Page.query.filter_by(name=page_name).all():
            if page.category.name == category_name:
                return page
        return {}, 404
