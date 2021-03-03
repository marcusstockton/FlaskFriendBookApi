from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')

    interest = api.model('interest', {
        'id': fields.Integer(description="Id field", attribute='id'),
        'value': fields.String(required=True, description='The interest', attribute='value')
    })

    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'first_name': fields.String(required=False, description='First Name'),
        'last_name': fields.String(required=False, description='Last Name'),
        'dob': fields.Date(required=False, description='Date Of Birth dd-mm-yyyy', attribute="date_of_birth"),
        'city': fields.String(description='City'),
        'gender_id': fields.Integer(description='Gender'),
        'public_id': fields.String(description='user Identifier'),
    })

    user_details = api.model('user', {
        'email': fields.String(required=True, description='user email address', attribute='email'),
        'username': fields.String(required=True, description='user username', attribute='username'),
        'first_name': fields.String(required=False, description='First Name', attribute='first_name'),
        'last_name': fields.String(required=False, description='Last Name', attribute='last_name'),
        'dob': fields.Date(required=False, description='Date Of Birth dd-mm-yyyy', attribute=lambda x: x.date_of_birth),
        'city': fields.String(description='City', attribute='city'),
        'gender_id': fields.Integer(description='Gender', attribute='gender_id'),
        'public_id': fields.String(description='user Identifier', attribute='public_id'),
        'interests': fields.List(fields.Nested(interest), required=False, description='interests', attribute='interests')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


