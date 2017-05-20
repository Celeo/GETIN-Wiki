from flask_restful import Resource, marshal_with

from ..util import restrict_editor, get_user_from_token
from ..models import db, Page, Edit, Category


class EditResource(Resource):

    method_decorators = [restrict_editor]

    @marshal_with(Edit.resource_fields_full)
    def get(self, page_id):
        """ Return all edits for this page """
        page = Page.query.get(page_id)
        return page.edits.order_by(Edit.id.desc()).all()


class RollbackResource(Resource):

    method_decorators = [restrict_editor]

    def put(self, id):
        """ Set the selected edit id as the current page's data - revert the page """
        selected_edit = Edit.query.get(id)
        page = Page.query.get(selected_edit.page_id)
        db.session.add(Edit(
            selected_edit.page_id,
            selected_edit.category_name,
            get_user_from_token().id,
            selected_edit.new_name,
            selected_edit.new_content,
            selected_edit.deleted
        ))
        page.name = selected_edit.new_name
        # There's a chance that the category from this revision no longer exists, or exists
        # under a different name. If this is the case, don't change the page's category.
        # Otherwise, when possible, revert it to the category the page was under at the
        # time of the selected edit.
        matching_category = Category.query.filter_by(name=selected_edit.category_name).first()
        if matching_category:
            page.category_id = matching_category.id
        page.content = selected_edit.new_content
        page.deleted = selected_edit.deleted
        db.session.commit()
        return {
            'name': page.name,
            'category': page.category_name
        }
