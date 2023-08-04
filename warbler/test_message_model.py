import unittest
from app import app, db
from models import Message, User

class MessageModelTestCase(unittest.TestCase):
    """Tests for the Message model."""

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

        # Create a test message
        self.message = Message(
            text='Test message',
            user_id=self.user.id
        )
        db.session.add(self.message)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""

        db.session.rollback()
        db.drop_all()

    def test_message_repr(self):
        """Test the __repr__ method of the Message model."""

        self.assertEqual(repr(self.message), f"<Message id={self.message.id} text=Test message>")

    def test_message_properties(self):
        """Test the properties of the Message model."""

        # Test text property
        self.assertEqual(self.message.text, 'Test message')

        # Test timestamp property
        # Assuming you have a datetime field named 'timestamp' in the Message model
        self.assertIsNotNone(self.message.timestamp)

        # Test user property
        self.assertEqual(self.message.user, self.user)

    def test_message_create(self):
        """Test creating a new message."""

        new_message = Message(
            text='New test message',
            user_id=self.user.id
        )
        db.session.add(new_message)
        db.session.commit()

        self.assertIsNotNone(new_message.id)
        self.assertEqual(new_message.text, 'New test message')
        self.assertEqual(new_message.user, self.user)

    # Add more tests as needed to cover other methods or behavior of the Message model

if __name__ == '__main__':
    unittest.main()