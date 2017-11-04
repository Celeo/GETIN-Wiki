from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from jose import jwt

from ..shared import config
from ..models import User


class Token_Resource(Resource):

    def post(self):
        """ Check the app's localStorage token and return a new sessionStorage token if valid """
        try:
            token = request.json['token']
            token_data = jwt.decode(token, config['SECRET_KEY'])
            user = User.query.filter_by(name=token_data['name']).first()
            if not user:
                return {}, 404
            if not user.in_alliance:
                print(f'${user.name} is not in the alliance, denying login')
                return {}, 403
            token_data['exp'] = datetime.utcnow() + timedelta(hours=24)
            return {
                'token': jwt.encode(token_data, config['SECRET_KEY'])
            }
        except Exception as e:
            print(f'Exception: {e}')
            return {}, 500
