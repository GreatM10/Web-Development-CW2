import unittest

from app import create_app, db, User, Activity, Admin


class AppTestCase(unittest.TestCase):

    def setUp(self):

        app = create_app('testing')
        app.config.update(TESTING=True)
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(name='test_user', username='test_user')
        user.set_password('test_user')
        admin = Admin(name='test_admin', username='test_admin')
        admin.set_password('test_admin')
        activity = Activity(activity_name='test_game', activity_info='test_info',
                            price=1, limit=2,
                            time='2022-12-12 20:00:00', deadline='2022-12-11')
        db.session.add_all([user, admin, activity])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exit(self):
        self.assertIsNotNone(self.app)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Recent Game', data)
        self.assertIn('Login', data)
        self.assertEqual(response.status_code, 200)

    def login(self):
        self.client.post('/login', data=dict(
            username='test_user',
            password='test_user',
        ), follow_redirects=True)

    def login_admin(self):
        self.client.post('/admin/login', data=dict(
            username='test_admin',
            password='test_admin',
        ), follow_redirects=True)

    # Login protection test
    def test_login_protect(self):
        response = self.client.get('/detail/1')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)

    # Login test
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test_user',
            password='test_user'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Logout', data)
        self.assertIn('My Information', data)

        # Login with wrong password
        response = self.client.post('/login', data=dict(
            username='test',
            password='456'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Wrong username or password!', data)

        # Login with wrong username
        response = self.client.post('/login', data=dict(
            username='wrong',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Wrong username or password!', data)

        # Login with empty username
        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Wrong Input!', data)

        # Login with empty password
        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Wrong Input!', data)

    # Logout test
    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)


if __name__ == "__main__":
    unittest.main()
