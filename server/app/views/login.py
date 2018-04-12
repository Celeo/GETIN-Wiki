from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from jose import jwt

from ..shared import db, eveapi, config
from ..models import User


class EVE_SSO_Resource(Resource):

    def get(self):
        """ Get the EVE SSO login URL """
        return {
            'url': eveapi['preston'].get_authorize_url()
        }

    def post(self):
        """ Log the user in using the EVE SSO and ESI """
        try:
            code = request.json['code']
            auth = eveapi['preston'].authenticate(code)
            char_info = auth.whoami()
            char_name = char_info['CharacterName']
            print(f'Char name for code {code} is {char_name}; fetching affiliation')
            basic_char_info = eveapi['preston'].get_op('get_characters_character_id', character_id=char_info['CharacterID'])
            corporation_id = basic_char_info['corporation_id']
            alliance_id = basic_char_info['alliance_id']
            corporation_info = eveapi['preston'].get_op('get_corporations_corporation_id', corporation_id=corporation_id)
            corporation = corporation_info['name']
            alliance_info = eveapi['preston'].get_op('get_alliances_alliance_id', alliance_id=alliance_id)
            alliance = alliance_info['name']
            user = User.query.filter_by(name=char_name).first()
            if user:
                user.corporation = corporation
                user.alliance = alliance
            else:
                user = User(char_name, corporation, alliance)
                db.session.add(user)
            db.session.commit()
            if not user.in_alliance:
                print(f'${user.name} is not in the alliance, denying login')
                return {}, 403
            token_data = {
                'name': char_name,
                'corporation': corporation,
                'inAlliance': user.in_alliance,
                'editor': user.editor,
                'admin': user.admin,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            long_token = jwt.encode(token_data, config['SECRET_KEY'])
            token_data['exp'] = datetime.utcnow() + timedelta(hours=6)
            short_token = jwt.encode(token_data, config['SECRET_KEY'])
            return {
                'sessionToken': long_token,
                'localToken': short_token
            }
        except Exception as e:
            print(f'Exception: {e}')
            return {}, 500
