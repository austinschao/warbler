"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


from ast import Assert
import os
from typing import Type
from unittest import TestCase

from psycopg2 import IntegrityError
import sqlalchemy

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.u1 = u1
        self.u2 = u2


        message1 = Message(
            text="Hello World!",
            user_id=self.u1.id
        )

        message2 = Message(
            text="Goodbye World!",
            user_id=self.u1.id
        )

        message3 = Message(
            text="Whats up World!",
            user_id=self.u1.id
        )

        db.session.add_all([message1, message2, message3])
        db.session.commit()

        self.message1 = message1
        self.message2 = message2
        self.message3 = message3

        liked_message1 = Likes(user_id=self.u2.id, message_id=self.message1.id)
        liked_message2 = Likes(user_id=self.u2.id, message_id=self.message2.id)

        db.session.add_all([liked_message1, liked_message2])
        db.session.commit()


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_message_model(self):
        """Does basic model work?"""

        # check message model attributes
        self.assertEqual(self.message1.text, "Hello World!")
        self.assertEqual(self.message1.user_id, self.u1.id)

        self.assertNotEqual(self.message2.text, "No goodbye world!")
        self.assertNotEqual(self.message2.user_id, 0)

        # check message/user relationship
        self.assertEqual(self.u1, self.message1.user)
        self.assertEqual(len(self.u1.messages), 3)

        # # check message __repr__
        # self.assertEqual(self.message1, f"<Message {self.message1.id}>")

    def test_liked_message(self):
        """ Does liked messages work? """

        # check if a message is in a user's list of liked messages
        self.assertIn(self.message1, self.u2.liked_messages)
        self.assertNotIn(self.message3, self.u2.liked_messages)

        # Check if user can like the same message twice
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            liked_own_message = Likes(user_id=self.u2.id, message_id=self.message1.id)
            db.session.add(liked_own_message)
            db.session.commit()



# Check model attributes
# Does the repr method work as expected?
# Does is_following successfully detect when user1 is following user2?
# Does is_following successfully detect when user1 is not following user2?
# Does is_followed_by successfully detect when user1 is followed by user2?
# Does is_followed_by successfully detect when user1 is not followed by user2?
# Does User.signup successfully create a new user given valid credentials?
# Does User.signup fail to create a new user if any of the validations (eg uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?