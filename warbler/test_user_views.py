import unittest
from app import app, db
from models import User

class UserViewsTestCase(unittest.TestCase):
    """Tests for the views and routes related to the User model."""

    def setUp(self):
        """Set up the test database and create test data."""

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Create the test database
        db.create_all()

        # Create a test user
        self.user = User.signup(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            image_url=None
        )
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""

        db.session.rollback()
        db.drop_all()

    def test_signup_route(self):
        """Test the signup route."""

        response = self.client.post('/signup', data={
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, newuser!", response.data)
        # Check if the new user is created in the database
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)

    def test_login_route(self):
        """Test the login route."""

        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, testuser!", response.data)

    def test_logout_route(self):
        """Test the logout route."""

        # Log in the test user first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
        })

        response = self.client.get('/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been successfully logged out.", response.data)

    def test_user_profile_route(self):
        """Test the user profile route."""

        # Log in the test user first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
        })

        response = self.client.get('/users/1')  # Assuming the test user has ID 1

        self.assertEqual(response.status_code, 200)
        # Add more assertions to check if the profile page displays the user's information correctly

    # Add more tests as needed for other view functions and routes related to the User model

if __name__ == '__main__':
    unittest.main()