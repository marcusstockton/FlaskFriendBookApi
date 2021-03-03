from flask import request, g
from flask_restx import Resource

from ..util.decorator import token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_user, delete_user

api = UserDto.api
_user = UserDto.user
_user_detail = UserDto.user_details


@api.route('/')
class UserList(Resource):
    @token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user_detail)
    def get(self):
        """List all registered users"""
        current_user = g.current_user
        all_users = get_all_users()
        return [x for x in all_users if x.id != current_user.id]  # Filters out the logged in user..

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@token_required
@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
class User(Resource):
    @api.doc('get a user')
    @api.response(404, 'User not found.')
    @api.marshal_with(_user_detail)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('update a user')
    @api.response(200, 'User updated.')
    @api.expect([_user_detail], validate=True)
    @api.marshal_with(_user_detail)
    def put(self, public_id):
        data = api.payload
        data['date_of_birth'] = data.pop('dob')
        return update_user(public_id, data)

    @api.doc('delete a user')
    @api.response(204, 'User deleted.')
    def delete(self, public_id):
        return delete_user(public_id)

