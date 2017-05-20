from flask_restful import Resource, marshal_with

from ..util import restrict_editor
from ..models import Page, Edit


class HistoryResource(Resource):

    method_decorators = [restrict_editor]

    @marshal_with(Edit.resource_fields)
    def get(self, page_id):
        page = Page.query.get(page_id)
        return page.edits.order_by(Edit.id.desc()).all()

    def put(self, page_id):
        # TODO "restore" the page to the specific version
        return {}, 204
