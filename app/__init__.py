from flask_restx import Api
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service',
          security='Bearer Auth',
          authorizations=authorizations
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)


# Global Error Handlers:
@api.errorhandler(IntegrityError)
def integrity_exception_handler(error: IntegrityError):
    """Default error handler"""
    return {'message': error.args}, 500


@api.errorhandler(Exception)
def generic_exception_handler(error: Exception):
    """Default error handler"""
    return {'message': str(error)}, getattr(error, 'code', 500)
