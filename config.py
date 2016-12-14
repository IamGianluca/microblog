import os


# database settings
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = ''.join(['sqlite:///',
                                   os.path.join(basedir, 'app.db')])
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# security options
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['MICROBLOG_SECRET']

# login format for OpenID providers
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    {'name': 'AOL', 'url': r'http://openid.aol.com/<username>' },
    {'name': 'Flickr', 'url': r'http://www.flickr.com/<username>' },
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWD = None

# administrator list
ADMINS = [os.environ['ADMIN_MAIL_ADDRESS']]
