from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from preston.crest import Preston as CREST
from preston.xmlapi import Preston as XMLAPI

from .models import db
from .shared import eveapi, config
from .views.login import EVE_SSO_Resource
from .views.account import Account_Resource
from .views.category import CategoriesResource, CategoryResource, IndexResource
from .views.page import PagesResource, PageResource, LookupResource
from .views.history import HistoryResource
from .views.admin import UserResource


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
config.update(app.config)

CORS(app)
api = Api(app)

db.app = app
db.init_app(app)

eveapi['user_agent'] = '? for GETIN alliance'
eveapi['crest'] = CREST(
    user_agent=eveapi['user_agent'],
    client_id=app.config['EVE_OAUTH_CLIENT_ID'],
    client_secret=app.config['EVE_OAUTH_SECRET'],
    callback_url=app.config['EVE_OAUTH_CALLBACK']
)
eveapi['xml'] = XMLAPI(user_agent=eveapi['user_agent'])


@app.route('/')
def index():
    return jsonify({
        'message': 'API index page'
    })


api.add_resource(EVE_SSO_Resource, '/eve/sso')
api.add_resource(Account_Resource, '/account')
api.add_resource(CategoriesResource, '/category')
api.add_resource(UserResource, '/admin')
api.add_resource(CategoryResource, '/category/<int:id>')
api.add_resource(PagesResource, '/page')
api.add_resource(PageResource, '/page/<int:id>')
api.add_resource(HistoryResource, '/history/<int:page_id>')
api.add_resource(LookupResource, '/lookup/<category_name>/<page_name>')
api.add_resource(IndexResource, '/index')
