import unittest
import json

from app.test.base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='example@gmail.com',
            username='username',
            password='123456',
            first_name='Mark',
            last_name='Twain',
            date_of_birth='1982-2-3',
            city='Exeter',
            gender_id=1
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='example@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data)
            self.assertTrue('Authorization' in response_data)
            self.assertTrue(str, type(response_data['Authorization']))
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data)
            self.assertTrue('token' in data)
            self.assertEqual(login_response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data)
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data)
            self.assertTrue(data['token'])
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        login_response.data
                    )['token']
                )
            )
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
