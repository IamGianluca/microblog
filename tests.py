#!/home/gianluca/.virtualenvs/microblog/bin/python3

import os
from nose.tools import assert_equal, assert_not_equal

from config import basedir
from app import app, db
from app.models import User


class TestCase():
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
                os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='john', email='john@email.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/41193cdbffbf06be0cdf231b28c54b18'
        assert_equal(avatar[0:len(expected)], expected)

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@email.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert_not_equal(nickname, 'john')

        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert_not_equal(nickname2, 'john')
        assert_not_equal(nickname2, nickname)
