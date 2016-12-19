import sys

import flask_whooshalchemy as whooshalchemy
from hashlib import md5

from app import app, db


if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def follow(self, user):
        """Follow another user.

        Args:
            user: [User] The user to follow.
        Returns:
            [User] Object that has to be added to the database session and
            committed.
        """
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """Unfollow a user that is currently being followed.

        Args:
            user: [User] The currently followed user that has to be unfollowed.
        Returns:
            [User] An object that has to be added to the database session and
            committed.
        """
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        """Check if the user is following the user passed as argument.

        Args:
            user: [User] The user that you want to check if is being followed.
        Returns:
            [Bool] True is the user passed as argument is being followed by the
            'self' user. False if the 'self' user is not following the user
            passed in the argument of the function."""
        return self.followed.filter(followers.c.followed_id == user.id).\
                count() > 0

    def followed_posts(self):
        """Get followed posts, so those published by followed users.

        Returns:
            [flask_sqlalchemy.BaseQuery] Query object.
        """
        return Post.query.join(followers,
                               (followers.c.followed_id == Post.user_id)).\
                filter(followers.c.follower_id == self.id).\
                order_by(Post.timestamp.desc())

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/{}?d=mm&s={}'.\
                format(md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User {}'.format(self.nickname)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


if enable_search:
    whooshalchemy.whoosh_index(app, Post)
