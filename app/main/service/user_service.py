import uuid
import datetime

from app.main import db
from app.main.model.user import User, Gender


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    gender = Gender.query.filter_by(id=data['gender_id']).first()
    if not user and gender:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.datetime.strptime(data['dob'], '%d-%m-%Y') if 'dob' in data else None,
            city=data['city'],
            gender=gender,
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
