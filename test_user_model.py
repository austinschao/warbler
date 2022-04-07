"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from typing import Type
from unittest import TestCase

from psycopg2 import IntegrityError
import sqlalchemy

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
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
        password="HASHED_PASSWORD_2"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.u1 = u1
        self.u2 = u2



    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(len(self.u1.following), 0)
        self.assertEqual(self.u1.username, "testuser1")
        self.assertEqual(self.u1.email, "test1@test.com")

    def test_user_model_repr(self):
        """tests repr in user model"""
        self.assertEqual(self.u1.__repr__(), f"<User #{self.u1.id}: {self.u1.username}, {self.u1.email}>")
        self.assertNotEqual(self.u1.__repr__(), f"<User #{self.u2.id}: {self.u2.username}, {self.u2.email}>")

    def test_user_model_is_followed_by(self):
        """Tests if user is followed by another user"""

        u2_follow_u1 = Follows(user_being_followed_id=self.u1.id, user_following_id=self.u2.id)

        db.session.add(u2_follow_u1)
        db.session.commit()
        self.assertEqual(self.u1.is_followed_by(self.u2), True)
        self.assertEqual(self.u2.is_followed_by(self.u1), False)


    def test_user_model_is_following(self):
        """Tests if user is following another user"""

        u2_follow_u1 = Follows(user_being_followed_id=self.u1.id, user_following_id=self.u2.id)
        db.session.add(u2_follow_u1)
        db.session.commit()

        self.assertEqual(self.u1.is_following(self.u2), False)
        self.assertEqual(self.u2.is_following(self.u1), True)

    

    def test_user_model_sign_up(self):
        """Testing for authenticate function"""
        test_user = User.signup(email="test3@test.com",
                            username="testuser3",
                            password="HASHED_PASSWORD",
                            image_url="")
        
        db.session.commit()


        self.assertIn(test_user, User.query.all())
        self.assertNotIn("test4", User.query.all())
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            failed_unique_value_user = User.signup(email="test3@test.com",
                            username="testuser3",
                            password="HASHED_PASSWORD",
                            image_url="")
            db.session.commit()
        with self.assertRaises(TypeError):
            failed_non_null_field_user = User.signup(email="test4@test.com",
                            username="testuser4",
                            password="HASHED_PASSWORD")
            db.session.commit()

    def test_user_model_authenticate(self):
        """Testing for authenticate function"""









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