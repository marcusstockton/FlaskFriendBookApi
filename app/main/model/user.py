from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key


# helper table
interests = db.Table('interests',
                     db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                     )


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(200), nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    gender = db.relationship("Gender")
    interests = db.relationship('Interest', secondary=interests, lazy='subquery',
                                backref=db.backref('users', lazy=True))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])

            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Gender(db.Model):
    """ Gender Model for storing user gender """
    __tablename__ = "gender"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(20), unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Gender '{}'>".format(self.value)


class Interest(db.Model):
    """ Gender Model for storing user interests """
    __tablename__ = "interest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(20), unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)



