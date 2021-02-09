from flask_testing import TestCase
from app.main import db
from manage import app
from app.main.model.user import Gender


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

        # Generate some genders for unit tests.
        male = Gender(value='Male', active=True)
        female = Gender(value='Female', active=True)
        db.session.add(male)
        db.session.add(female)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
